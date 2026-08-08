from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LINTER = REPO_ROOT / "scripts" / "creative_lint.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def run_lint(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(LINTER), "--root", str(root)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class CreativeLintHealthyFixtureTests(unittest.TestCase):
    def test_fiction_fixture_passes_without_warnings(self) -> None:
        result = run_lint(FIXTURES / "fiction-minimal")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("creative-lint: pass (0 errors, 0 warnings)", result.stdout)

    def test_blog_fixture_passes_without_warnings(self) -> None:
        result = run_lint(FIXTURES / "blog-minimal")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("creative-lint: pass (0 errors, 0 warnings)", result.stdout)

    def test_small_example_project_passes(self) -> None:
        result = run_lint(REPO_ROOT / "examples" / "fiction-mini")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("creative-lint: pass (0 errors, 0 warnings)", result.stdout)


class CreativeLintFailureTests(unittest.TestCase):
    def copy_fixture(self, name: str) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / name
        shutil.copytree(FIXTURES / name, root)
        return temporary, root

    def assert_lint_error(self, root: Path, code: str) -> None:
        result = run_lint(root)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"ERROR {code}", result.stdout)
        self.assertIn("creative-lint: fail", result.stdout)

    def test_missing_agents_is_an_error(self) -> None:
        temporary, root = self.copy_fixture("blog-minimal")
        self.addCleanup(temporary.cleanup)
        (root / "AGENTS.md").unlink()

        self.assert_lint_error(root, "project.missing_agents")

    def test_invalid_spec_approval_state_is_an_error(self) -> None:
        temporary, root = self.copy_fixture("blog-minimal")
        self.addCleanup(temporary.cleanup)
        spec = root / ".creative" / "work" / "spec.md"
        spec.write_text(spec.read_text(encoding="utf-8").replace("status: approved", "status: accepted"), encoding="utf-8")

        self.assert_lint_error(root, "frontmatter.invalid_value")

    def test_output_outside_manuscript_is_an_error(self) -> None:
        temporary, root = self.copy_fixture("blog-minimal")
        self.addCleanup(temporary.cleanup)
        tasks = root / ".creative" / "work" / "tasks.md"
        tasks.write_text(tasks.read_text(encoding="utf-8").replace("manuscript/article.md", "draft/article.md"), encoding="utf-8")

        self.assert_lint_error(root, "task.invalid_output")

    def test_accepted_incomplete_task_is_an_error(self) -> None:
        temporary, root = self.copy_fixture("blog-minimal")
        self.addCleanup(temporary.cleanup)
        tasks = root / ".creative" / "work" / "tasks.md"
        tasks.write_text(tasks.read_text(encoding="utf-8").replace("- [x] 1.", "- [ ] 1."), encoding="utf-8")

        self.assert_lint_error(root, "task.accepted_incomplete")

    def test_missing_completed_manuscript_is_an_error(self) -> None:
        temporary, root = self.copy_fixture("blog-minimal")
        self.addCleanup(temporary.cleanup)
        (root / "manuscript" / "article.md").unlink()

        self.assert_lint_error(root, "task.missing_manuscript")

    def test_duplicate_outline_unit_is_an_error(self) -> None:
        temporary, root = self.copy_fixture("blog-minimal")
        self.addCleanup(temporary.cleanup)
        outline = root / ".creative" / "work" / "outline.md"
        outline.write_text(outline.read_text(encoding="utf-8") + "\n## Unit 001: 重複\n", encoding="utf-8")

        self.assert_lint_error(root, "outline.duplicate_unit_id")

    def test_review_state_conflict_is_an_error(self) -> None:
        temporary, root = self.copy_fixture("fiction-minimal")
        self.addCleanup(temporary.cleanup)
        review = root / ".creative" / "work" / "reviews" / "001.md"
        review.write_text(review.read_text(encoding="utf-8").replace("status: resolved", "status: approved"), encoding="utf-8")

        self.assert_lint_error(root, "review.unapplied_approved_finding")

    def test_changed_manuscript_makes_review_stale_but_not_structurally_invalid(self) -> None:
        temporary, root = self.copy_fixture("blog-minimal")
        self.addCleanup(temporary.cleanup)
        manuscript = root / "manuscript" / "article.md"
        manuscript.write_text(manuscript.read_text(encoding="utf-8") + "\n追記。\n", encoding="utf-8")

        result = run_lint(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARNING review.stale", result.stdout)
        self.assertIn("creative-lint: pass (0 errors, 1 warnings)", result.stdout)

    def test_missing_spec_is_reported_as_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")

            result = run_lint(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARNING project.missing_spec", result.stdout)


if __name__ == "__main__":
    unittest.main()
