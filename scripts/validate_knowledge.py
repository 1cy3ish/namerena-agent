"""Validate knowledge references, archive bytes, coverage and local links."""

import hashlib
import argparse
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-checkout", type=Path, help="Optional local tswn checkout for immutable Git source verification")
    args = parser.parse_args()
    sources = read("knowledge/sources.json")["sources"]
    ids = {source["id"] for source in sources}
    assert len(ids) == len(sources), "Duplicate source IDs"
    for source in sources:
        assert source.get("url") or source.get("local_path"), source["id"]
        if source.get("type") == "repository":
            assert re.fullmatch(r"[0-9a-f]{40}", source["commit"]), source["id"]
            assert re.fullmatch(r"[0-9a-f]{64}", source["sha256"]), source["id"]
            assert source["commit"] in source["url"], source["id"]
            assert 1 <= source["line_start"] <= source["line_end"], source["id"]

    glossary = read("knowledge/glossary.json")
    term_ids = {term["id"] for term in glossary["terms"]}

    def walk(value, file):
        if isinstance(value, dict):
            if "source_ids" in value:
                assert set(value["source_ids"]) <= ids, f"Unresolved source in {file}"
            if "term_id" in value:
                assert value["term_id"] in term_ids, f"Unresolved term in {file}: {value['term_id']}"
            for ref in value.get("context_refs", []):
                context = read("knowledge/" + ref["path"])
                match = [entry for entry in context["enrichments"] if entry["context_id"] == ref["context_id"]]
                assert len(match) == 1 and match[0]["term_id"] == value["id"], f"Broken contextual reference in {file}"
            for key in ("checked_at", "accessed_at", "recorded_at"):
                if key in value:
                    date.fromisoformat(value[key])
            for key in ("local_path", "snapshot_path"):
                if key in value:
                    assert (ROOT / value[key]).exists(), f"Missing {key} in {file}: {value[key]}"
            if "details_path" in value:
                details = read("knowledge/" + value["details_path"])
                entries = next(v for v in details.values() if isinstance(v, list))
                assert value["details_id"] in {entry["id"] for entry in entries}, value["id"]
            for item in value.values():
                walk(item, file)
        elif isinstance(value, list):
            records = [item for item in value if isinstance(item, dict) and "id" in item]
            assert len({item["id"] for item in records}) == len(records), f"Duplicate IDs in {file}"
            contexts = [item["context_id"] for item in value if isinstance(item, dict) and "context_id" in item]
            assert len(set(contexts)) == len(contexts), f"Duplicate context IDs in {file}"
            for item in value:
                walk(item, file)

    files = list((ROOT / "knowledge").rglob("*.json")) + list((ROOT / "evals").rglob("*.json"))
    for file in files:
        walk(json.loads(file.read_text(encoding="utf-8")), file)
    if args.source_checkout:
        verified = {}
        for source in sources:
            if source.get("type") != "repository":
                continue
            identity = source["commit"] + ":" + source["repository_path"]
            if identity not in verified:
                content = subprocess.check_output(["git", "show", identity], cwd=args.source_checkout)
                verified[identity] = (hashlib.sha256(content).hexdigest(), len(content.decode("utf-8").splitlines()))
            digest, lines = verified[identity]
            assert source["sha256"] == digest and source["line_end"] <= lines, source["id"]
        print(f"Verified {len(verified)} immutable source files from the supplied checkout.")
    manifest = read("knowledge/official/crawl-manifest.json")
    assert not manifest["pending"], "Archive stopped before discovery queue was exhausted"
    assert manifest["summary"]["pending_due_to_limit"] == 0
    downloaded = [entry for entry in manifest["files"] if "local_path" in entry]
    for entry in downloaded:
        content = (ROOT / entry["local_path"]).read_bytes()
        assert len(content) == entry["bytes"], entry["url"]
        assert hashlib.sha256(content).hexdigest() == entry["sha256"], entry["url"]
    failures = {(entry["url"], entry["status"]) for entry in manifest["files"] if "error" in entry}
    known = {(entry["url"], entry["status"]) for entry in read("knowledge/official/coverage.json")["known_unavailable"]}
    assert failures == known, f"Unreviewed archive failures: {failures ^ known}"
    urls = {entry["url"] for entry in manifest["files"]}
    assert all(link["url"] in urls for link in manifest["links"] if link["in_scope"]), "Unvisited in-scope link"
    for file in list(ROOT.glob("*.md")) + [p for folder in ("knowledge", "agents", "skills", "mcp", "docs", "scripts") for p in (ROOT / folder).rglob("*.md")]:
        for target in re.findall(r"\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
            if "://" in target or target.startswith(("#", "//", "mailto:")):
                continue
            assert (file.parent / target.split("#", 1)[0]).exists(), f"Broken link in {file}: {target}"
    print(f"Validated {len(files)} JSON files, {len(sources)} sources, {len(read('knowledge/glossary.json')['terms'])} terms, {len(downloaded)} archived URL records and local links.")
    print(f"Known upstream gaps retained: {len(known)} unavailable URL; ladder live results not collected.")


if __name__ == "__main__":
    main()
