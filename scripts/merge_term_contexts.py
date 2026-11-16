"""Merge tool and community terminology and contextual explanations."""

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def merge_contexts(glossary):
    terms = {term["id"]: term for term in glossary["terms"]}
    files = [file for folder in ("tools", "community")
             for file in sorted((ROOT / "knowledge" / folder).rglob("terminology.json"))]
    # Load definitions before explanations, so contexts can refer to any dataset.
    for file in files:
        data = json.loads(file.read_text(encoding="utf-8"))
        for term in data.get("terms", []):
            incoming = copy.deepcopy(term)
            previous = terms.get(term["id"], {})
            for field in ("detailed_description", "outdated"):
                if field in previous:
                    incoming[field] = previous[field]
            terms[term["id"]] = incoming
    for file in files:
        data = json.loads(file.read_text(encoding="utf-8"))
        context_path = file.relative_to(ROOT / "knowledge").as_posix()
        for enrichment in data.get("enrichments", []):
            target = terms[enrichment["term_id"]]
            if enrichment.get("definition"):
                target["definition"] = enrichment["definition"]
            if enrichment.get("category"):
                target["category"] = enrichment["category"]
            target["aliases"] = list(dict.fromkeys(target["aliases"] + enrichment.get("aliases_add", [])))
            target["source_ids"] = list(dict.fromkeys(target["source_ids"] + enrichment["source_ids"]))
            note = {"context_id": enrichment["context_id"], "scope": enrichment["scope"],
                    "explanation": enrichment["explanation"], "source_ids": enrichment["source_ids"],
                    "checked_at": enrichment["checked_at"]}
            notes = target.setdefault("context_notes", [])
            notes[:] = [old for old in notes if old["context_id"] != note["context_id"]]
            notes.append(note)
            refs = target.setdefault("context_refs", [])
            ref = {"path": context_path, "context_id": enrichment["context_id"]}
            if ref not in refs:
                refs.append(ref)
    for term in terms.values():
        term.pop("scope", None)
        term.setdefault("detailed_description", "")
        term.setdefault("outdated", False)
    glossary["terms"] = list(terms.values())
    return glossary


def main():
    if any((ROOT / "knowledge/wiki/revisions").glob("*/*.json")):
        raise SystemExit("已有在线编辑历史，请先人工合并；停止覆盖当前术语表。")
    file = ROOT / "knowledge/glossary.json"
    result = merge_contexts(json.loads(file.read_text(encoding="utf-8")))
    with file.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"Merged contextual knowledge: {len(result['terms'])} terms.")


if __name__ == "__main__":
    main()
