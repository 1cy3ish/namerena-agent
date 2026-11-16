"""Merge repository-derived terms and contextual explanations into the glossary."""

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def merge_contexts(glossary):
    terms = {term["id"]: term for term in glossary["terms"]}
    for file in sorted((ROOT / "knowledge/tools").rglob("terminology.json")):
        data = json.loads(file.read_text(encoding="utf-8"))
        context_path = file.relative_to(ROOT / "knowledge").as_posix()
        for term in data.get("terms", []):
            terms[term["id"]] = copy.deepcopy(term)
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
    glossary["terms"] = list(terms.values())
    return glossary


def main():
    file = ROOT / "knowledge/glossary.json"
    result = merge_contexts(json.loads(file.read_text(encoding="utf-8")))
    with file.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"Merged contextual knowledge: {len(result['terms'])} terms.")


if __name__ == "__main__":
    main()
