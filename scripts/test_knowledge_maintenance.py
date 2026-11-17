"""Regression checks for editorial data loss, rebuilds and archive integrity.

Uses temporary copies only; does not fetch sources or invoke a model/game.
"""

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import merge_term_contexts as merger
import validate_knowledge as validator

ROOT = Path(__file__).resolve().parents[1]


def read(root, path):
    return json.loads((root / path).read_text(encoding="utf-8"))


def sandbox(destination):
    for folder in ("scripts", "knowledge", "data"):
        shutil.copytree(ROOT / folder, destination / folder, ignore=shutil.ignore_patterns("__pycache__"))


def run_writer(root, script):
    return subprocess.run([sys.executable, str(root / "scripts" / script)], cwd=root,
                          capture_output=True, text=True, encoding="utf-8",
                          env={**os.environ, "PYTHONUTF8": "1"})


class KnowledgeMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.glossary = read(ROOT, "knowledge/glossary.json")

    def test_current_merge_preserves_complete_records(self):
        if any((ROOT / "knowledge/wiki/revisions").glob("*/*.json")):
            self.skipTest("Online edits require manual reconciliation with canonical records")
        self.assertEqual(merger.merge_contexts(copy.deepcopy(self.glossary)), self.glossary)

    def test_repeated_merge_is_idempotent(self):
        first = merger.merge_contexts(copy.deepcopy(self.glossary))
        self.assertEqual(merger.merge_contexts(copy.deepcopy(first)), first)

    def test_template_keeps_reviewed_body_flags_citations_and_contexts(self):
        term = {"id": "example", "term": "示例", "aliases": ["当前别名"], "definition": "当前释义",
                "detailed_description": "已有人工正文", "outdated": True, "status": "unverified",
                "source_ids": ["editorial-source"], "context_notes": [{"context_id": "kept"}],
                "context_refs": [{"path": "kept.json", "context_id": "kept"}]}
        incoming = {"id": "example", "term": "示例", "aliases": [], "definition": "核查后的简述",
                    "detailed_description": "", "outdated": False, "status": "source_supported",
                    "source_ids": ["canonical-source"]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "knowledge/tools/example/terminology.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"terms": [incoming], "enrichments": []}), encoding="utf-8")
            with patch.object(merger, "ROOT", root):
                actual = merger.merge_contexts({"terms": [copy.deepcopy(term)]})["terms"][0]
        for field in ("detailed_description", "outdated", "context_notes", "context_refs"):
            self.assertEqual(actual[field], term[field], field)
        self.assertEqual(set(actual["source_ids"]), {"editorial-source", "canonical-source"})
        self.assertEqual(actual["status"], "source_supported")
        self.assertIn("当前别名", actual["aliases"])

    def test_official_rebuild_preserves_all_reviewed_fields(self):
        if any((ROOT / "knowledge/wiki/revisions").glob("*/*.json")):
            self.skipTest("Online history blocks rebuilds")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sandbox(root)
            for _ in range(2):
                result = run_writer(root, "build_official_index.py")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(read(root, "knowledge/glossary.json"), self.glossary)

    def test_online_history_blocks_both_writers_without_changing_glossary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sandbox(root)
            history = root / "knowledge/wiki/revisions/2000-01-01/test-only.json"
            history.parent.mkdir(parents=True, exist_ok=True)
            history.write_text("{}", encoding="utf-8")
            before = (root / "knowledge/glossary.json").read_bytes()
            for script in ("merge_term_contexts.py", "build_official_index.py"):
                result = run_writer(root, script)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("已有在线编辑历史", result.stderr + result.stdout)
                self.assertEqual((root / "knowledge/glossary.json").read_bytes(), before)

    def test_corrupted_provided_document_is_rejected(self):
        source = next(s for s in read(ROOT, "knowledge/sources.json")["sources"] if s["id"] == "attachment-qqbot")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / source["local_path"]
            path.parent.mkdir(parents=True)
            path.write_bytes((ROOT / source["local_path"]).read_bytes() + b"corruption")
            (root / "knowledge").mkdir(exist_ok=True)
            (root / "knowledge/sources.json").write_text(json.dumps({"sources": [source]}), encoding="utf-8")
            with patch.object(validator, "ROOT", root), patch.object(sys, "argv", ["validate_knowledge.py"]):
                with self.assertRaisesRegex(AssertionError, "Source file hash mismatch"):
                    validator.main()


if __name__ == "__main__":
    unittest.main()
