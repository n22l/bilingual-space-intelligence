"""Privacy tests use invented sentinel text, never real private material."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("research_search", ROOT / "src" / "research_search.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        # Tests must not inherit a user's production-data selection.
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        os.environ.pop("TECH_RESEARCH_DATA_DIR", None)
        os.environ.pop("SPACE_DATA_DIR", None)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.private = Path(self.temp.name).resolve()
        app.external_directory(self.private)

    def run_app(self, arguments):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = app.main(arguments)
        return status, out.getvalue(), err.getvalue()

    def corpus(self):
        manifest = [{"id": "fixture", "title": "Invented private test",
                     "publisher": "Synthetic", "source_url": "synthetic:test",
                     "publication_date": "unknown", "language": "en", "file": "source.txt"}]
        (self.private / "documents.json").write_text(json.dumps(manifest), encoding="utf-8")
        (self.private / "source.txt").write_text("SENTINEL_TEST_ONLY rocket inspection", encoding="utf-8")
        (self.private / "questions.json").write_text(json.dumps([
            {"id": "test", "question": "rocket inspection", "answerable": True,
             "expected_passage_ids": ["fixture:p1"]}]), encoding="utf-8")

    def snapshot(self):
        return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.relative_to(ROOT).parts}

    def test_demo_without_private_access(self):
        with patch.dict(os.environ, {"SPACE_DATA_DIR": str(self.private / "does-not-exist"),
                                    "TECH_RESEARCH_DATA_DIR": str(self.private / "also-absent")}), patch.object(
                app, "external_directory", side_effect=AssertionError("Private access forbidden")):
            code, out, err = self.run_app(["--mode", "demo", "evaluate"])
        self.assertEqual(code, 0)
        result = json.loads(out)
        self.assertEqual((result["hits_at_5"], result["answerable_questions"]), (6, 6))
        self.assertEqual(result["manually_labeled_unanswerable_questions"], 2)
        self.assertEqual(err, "")

    def test_original_passages_and_metadata_in_both_languages(self):
        passages = app.load_passages(app.demo_directory())
        for question, expected in [("refurbishment replacement parts", "demo-en-cost:p1"),
                                   ("翻修 工时 零件", "demo-zh-cost:p1")]:
            result = app.search(passages, question)[0]
            self.assertEqual(result["passage_id"], expected)
            self.assertTrue(all(key in result["source"] for key in
                                ("title", "publisher", "source_url", "publication_date", "language")))
            self.assertEqual(result["passage"], next(p["passage"] for p in passages if p["passage_id"] == expected))

    def test_missing_and_invalid_private_setting(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(self.run_app(["--mode", "private", "evaluate"])[0], 2)
        for value in (str(self.private / "absent"), str(ROOT), str(ROOT / "data")):
            with self.assertRaises(app.SafeError):
                app.external_directory(value)

    def test_rejects_other_git_tree_and_worktree_marker(self):
        repo = self.private / "other"
        repo.mkdir()
        subprocess.run(["git", "init", str(repo)], capture_output=True, check=True)
        child = repo / "nested"
        child.mkdir()
        with self.assertRaises(app.SafeError):
            app.external_directory(child)
        linked = self.private / "linked"
        linked.mkdir()
        (linked / ".git").write_text("gitdir: missing-test-worktree", encoding="utf-8")
        with self.assertRaises(app.SafeError):
            app.external_directory(linked)

    def test_symlink_to_repository_rejected(self):
        link = self.private / "alias"
        try:
            link.symlink_to(ROOT, target_is_directory=True)
        except OSError:
            self.skipTest("Creating symlinks requires OS permission")
        with self.assertRaises(app.SafeError):
            app.external_directory(link)

    def test_windows_junction_to_repository_rejected(self):
        if os.name != "nt":
            self.skipTest("Windows-only junction test")
        link = self.private / "junction"
        created = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(ROOT)], capture_output=True)
        self.assertEqual(created.returncode, 0)
        try:
            with self.assertRaises(app.SafeError):
                app.external_directory(link)
        finally:
            link.rmdir()  # Remove only the junction, never its target.

    def test_private_outputs_external_and_repository_unchanged(self):
        self.corpus()
        before = self.snapshot()
        with patch.dict(os.environ, {"SPACE_DATA_DIR": str(self.private)}):
            for args in (["--mode", "private", "search", "--question", "inspection"],
                         ["--mode", "private", "evaluate"]):
                code, out, err = self.run_app(args)
                self.assertEqual(code, 0)
                self.assertFalse("SENTINEL_TEST_ONLY" in out + err)
        self.assertEqual(before, self.snapshot())
        results = list(self.private.glob("result-*.json"))
        self.assertEqual(len(results), 2)
        self.assertTrue(any("SENTINEL_TEST_ONLY" in p.read_text(encoding="utf-8") for p in results))

    def test_errors_do_not_disclose_text(self):
        self.corpus()
        (self.private / "documents.json").write_text("SENTINEL_TEST_ONLY broken JSON", encoding="utf-8")
        with patch.dict(os.environ, {"SPACE_DATA_DIR": str(self.private)}):
            code, out, err = self.run_app(["--mode", "private", "evaluate"])
        self.assertEqual(code, 2)
        self.assertFalse("SENTINEL_TEST_ONLY" in out + err)
        self.assertFalse("Traceback" in out + err)
        self.assertFalse(str(self.private) in out + err)
        code, out, err = self.run_app(["--mode", "SENTINEL_TEST_ONLY", "evaluate"])
        self.assertEqual(code, 2)
        self.assertFalse("SENTINEL_TEST_ONLY" in out + err)

    def test_escape_and_linked_source_rejected(self):
        self.corpus()
        for path in ("../outside.txt", str(ROOT / "README.md"), "source.txt:stream"):
            with self.assertRaises(app.SafeError):
                app.safe_file(self.private, path)
        link = self.private / "source-link.txt"
        try:
            link.symlink_to(self.private / "source.txt")
        except OSError:
            self.skipTest("Creating symlinks requires OS permission")
        with self.assertRaises(app.SafeError):
            app.safe_file(self.private, "source-link.txt")

    def test_nested_git_source_rejected(self):
        nested = self.private / "nested"
        nested.mkdir()
        (nested / ".git").mkdir()
        (nested / "source.txt").write_text("synthetic", encoding="utf-8")
        with self.assertRaises(app.SafeError):
            app.safe_file(self.private, "nested/source.txt")

    def test_git_unavailable_fails_closed(self):
        with patch.object(app.subprocess, "run", side_effect=FileNotFoundError):
            with self.assertRaises(app.SafeError):
                app.external_directory(self.private)

    def test_unknown_expected_evidence_rejected(self):
        self.corpus()
        questions = [{"id": "q", "question": "inspection", "answerable": True,
                      "expected_passage_ids": ["missing:p1"]}]
        (self.private / "questions.json").write_text(json.dumps(questions), encoding="utf-8")
        with self.assertRaises(app.SafeError):
            app.evaluate(self.private, app.load_passages(self.private))

    def test_private_question_file_and_write_failure_no_fallback(self):
        self.corpus()
        (self.private / "question.txt").write_text("inspection", encoding="utf-8")
        before = self.snapshot()
        with patch.dict(os.environ, {"SPACE_DATA_DIR": str(self.private)}):
            code, out, err = self.run_app(["--mode", "private", "search", "--question-file", "question.txt"])
            self.assertEqual(code, 0)
            self.assertFalse("SENTINEL_TEST_ONLY" in out + err)
            with patch.object(app.os, "open", side_effect=PermissionError("SENTINEL_TEST_ONLY")):
                code, out, err = self.run_app(["--mode", "private", "evaluate"])
            self.assertEqual(code, 2)
            self.assertFalse("SENTINEL_TEST_ONLY" in out + err)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(len(list(self.private.glob("result-*.json"))), 1)

    def test_hardlinked_input_rejected(self):
        self.corpus()
        os.link(self.private / "source.txt", self.private / "hardlink.txt")
        with self.assertRaises(app.SafeError):
            app.safe_file(self.private, "hardlink.txt")

    def test_existing_output_never_followed(self):
        destination = self.private / "result-fixed.json"
        destination.write_text("unchanged", encoding="utf-8")
        class Fixed:
            hex = "fixed"
        with patch.object(app.uuid, "uuid4", return_value=Fixed()):
            with self.assertRaises(FileExistsError):
                app.private_output(self.private, {"synthetic": True})
        self.assertEqual(destination.read_text(encoding="utf-8"), "unchanged")

    def test_demo_rejects_linked_data_directory(self):
        with patch.object(app, "DEMO", self.private / "demo"), patch.object(Path, "is_symlink", return_value=True):
            with self.assertRaises(app.SafeError):
                app.demo_directory()

    def test_generic_private_setting_precedence_and_legacy_fallback(self):
        self.corpus()
        with patch.dict(os.environ, {"TECH_RESEARCH_DATA_DIR": str(self.private),
                                    "SPACE_DATA_DIR": str(ROOT)}):
            self.assertEqual(app.private_directory(), self.private)
            code, out, err = self.run_app(["--mode", "private", "evaluate"])
            self.assertEqual(code, 0)
            self.assertNotIn(str(self.private), out + err)
        self.assertEqual(len(list(self.private.glob("result-*.json"))), 1)
        with patch.dict(os.environ, {"SPACE_DATA_DIR": str(self.private)}):
            self.assertEqual(app.private_directory(), self.private)
            for invalid in ("", str(ROOT), str(self.private / "absent")):
                with patch.dict(os.environ, {"TECH_RESEARCH_DATA_DIR": invalid}):
                    with self.assertRaises(app.SafeError):
                        app.private_directory()

    def test_optional_domain_and_language_metadata_without_taxonomy(self):
        self.corpus()
        manifest_path = self.private / "documents.json"
        records = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertNotIn("domain", app.load_passages(self.private)[0]["source"])
        for language in ("en", "zh", "zh-Hans", "fr"):
            records[0].update(language=language, domain="synthetic-test")
            manifest_path.write_text(json.dumps(records), encoding="utf-8")
            source = app.load_passages(self.private)[0]["source"]
            self.assertEqual(source["language"], language)
            self.assertEqual(source["domain"], "synthetic-test")
        for field, invalid in (("language", "English Chinese"), ("language", "en_US"),
                               ("domain", ""), ("domain", 42)):
            broken = {**records[0], field: invalid}
            manifest_path.write_text(json.dumps([broken]), encoding="utf-8")
            with self.assertRaises(app.SafeError):
                app.load_passages(self.private)

    def test_legacy_and_generic_cli_match(self):
        for command in (["evaluate"], ["search", "--question", "refurbishment replacement parts"],
                        ["search", "--question", "翻修 工时 零件"]):
            results = []
            for script in ("research_search.py", "space_search.py"):
                completed = subprocess.run([sys.executable, "-B", str(ROOT / "src" / script),
                                            "--mode", "demo", *command], capture_output=True,
                                           encoding="utf-8", check=True)
                self.assertEqual(completed.stderr, "")
                results.append(json.loads(completed.stdout))
            self.assertEqual(*results)


if __name__ == "__main__":
    unittest.main()
