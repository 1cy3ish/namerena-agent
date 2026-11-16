"""Generate the static wiki and its data from the shared knowledge base."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist/wiki"


def build():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for asset in (ROOT / "web").iterdir():
        if asset.suffix in {".html", ".css", ".mjs", ".svg"}:
            shutil.copyfile(asset, OUTPUT / asset.name)
    terms = json.loads((ROOT / "knowledge/glossary.json").read_text(encoding="utf-8"))["terms"]
    sources = json.loads((ROOT / "knowledge/sources.json").read_text(encoding="utf-8"))["sources"]
    assert len({term["id"] for term in terms}) == len(terms), "Duplicate term IDs"
    source_ids = {source["id"] for source in sources}
    assert all(set(term["source_ids"]) <= source_ids for term in terms), "Unresolved sources"
    fields = {"id", "title", "url", "type", "notes", "scope", "accessed_at", "recorded_at", "commit"}
    public_sources = [{key: value for key, value in source.items() if key in fields} for source in sources]
    for source, public in zip(sources, public_sources):
        if source.get("snapshot_kind") == "curated_observations":
            public["notes"] = "根据公开页面或指定帖子整理；赛事和活动安排请以当期说明为准。"
    details = {}
    for file in ("attributes.json", "skills.json", "special-names.json"):
        data = json.loads((ROOT / "knowledge/official" / file).read_text(encoding="utf-8"))
        for rows in data.values():
            if isinstance(rows, list):
                details.update({row["id"]: row for row in rows if isinstance(row, dict) and "id" in row})
    payload = {"schema_version": "0.1", "checked_at": max(term["checked_at"] for term in terms),
               "terms": terms, "sources": public_sources, "details": details}
    data_dir = OUTPUT / "data"
    data_dir.mkdir(exist_ok=True)
    with (data_dir / "knowledge.json").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
    return OUTPUT


if __name__ == "__main__":
    print(f"Built static wiki: {build()}")
