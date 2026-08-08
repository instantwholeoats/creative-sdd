from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / ".agents" / "skills"
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"\'')
    return result


def task_states(root: Path) -> list[tuple[bool, str]]:
    text = (root / ".creative" / "work" / "tasks.md").read_text(encoding="utf-8")
    tasks: list[tuple[bool, str]] = []
    current_complete: bool | None = None
    current_acceptance = "pending"
    for line in text.splitlines():
        match = re.match(r"^- \[([ xX])\] [0-9]+\.", line)
        if match:
            if current_complete is not None:
                tasks.append((current_complete, current_acceptance))
            current_complete = match.group(1).lower() == "x"
            current_acceptance = "pending"
        elif current_complete is not None and line.strip().startswith("- Acceptance:"):
            current_acceptance = line.split(":", 1)[1].strip()
    if current_complete is not None:
        tasks.append((current_complete, current_acceptance))
    return tasks


def status_equivalent(root: Path) -> str:
    work = root / ".creative" / "work"
    spec = work / "spec.md"
    if not spec.exists():
        return "discovery"
    if metadata(spec).get("status") != "approved":
        return "spec_approval"
    design = work / "design.md"
    if not design.exists():
        return "planning"
    if metadata(design).get("status") != "approved":
        return "plan_approval"
    states = task_states(root)
    if any(not complete for complete, _ in states):
        return "drafting"
    if states and all(acceptance == "accepted" for _, acceptance in states):
        return "complete"
    return "manuscript_acceptance"


class ApprovalGateContractTests(unittest.TestCase):
    def test_spec_requires_presentation_and_explicit_current_approval(self) -> None:
        skill = read_skill("creative-spec")
        self.assertIn("その内容がユーザーへ提示済み", skill)
        self.assertIn("ユーザーの最新発言", skill)
        self.assertIn("status: approved", skill)
        self.assertIn("frontmatterの`status`だけ", skill)

    def test_plan_requires_approved_spec_and_separate_plan_approval(self) -> None:
        skill = read_skill("creative-plan")
        self.assertIn("Specが`approved`", skill)
        self.assertIn("Planの内容が現在の会話でユーザーへ提示済み", skill)
        self.assertIn("Plan全体への明確な承認", skill)

    def test_draft_requires_both_approval_gates_and_one_task(self) -> None:
        skill = read_skill("creative-draft")
        self.assertIn("Specの`status`が`approved`", skill)
        self.assertIn("Planの`status`が`approved`", skill)
        self.assertIn("一度に複数taskを執筆しない", skill)
        self.assertIn("`Acceptance`を`pending`", skill)

    def test_review_and_revision_keep_finding_approval_separate(self) -> None:
        review = read_skill("creative-review")
        revise = read_skill("creative-revise")
        self.assertIn("status: proposed", review)
        self.assertIn("特定の指摘を明示的に承認", review)
        self.assertIn("`status: approved`の未解決指摘", revise)
        self.assertIn("`proposed`、`rejected`、`resolved`な指摘はRevision対象にしない", revise)

    def test_revision_acceptance_reconciles_before_final_states(self) -> None:
        revise = read_skill("creative-revise")
        continuity = revise.index("continuity、対応Summary")
        drift = revise.index("Narrative Driftを検出")
        final_state = revise.index("状態同期がすべて正常に完了した最後")
        self.assertLess(continuity, final_state)
        self.assertLess(drift, final_state)


class FixtureWorkflowTests(unittest.TestCase):
    def test_fiction_fixture_records_narrative_drift_without_rewriting_reality(self) -> None:
        root = FIXTURES / "fiction-minimal"
        manuscript = (root / "manuscript" / "001.md").read_text(encoding="utf-8")
        summary = (root / ".creative" / "work" / "summaries" / "001.md").read_text(encoding="utf-8")
        continuity = (root / ".creative" / "work" / "continuity.md").read_text(encoding="utf-8")
        outline = (root / ".creative" / "work" / "outline.md").read_text(encoding="utf-8")

        self.assertIn("横浜に残る", manuscript)
        self.assertIn("東京行きの列車へ乗る予定", summary)
        self.assertIn("原稿を尊重", summary)
        self.assertIn("Character Knowledge", continuity)
        self.assertIn("Reader Knowledge", continuity)
        self.assertIn("Unit 002: 横浜での朝", outline)

    def test_fiction_fixture_is_revision_accepted_and_reconciled(self) -> None:
        root = FIXTURES / "fiction-minimal"
        review = metadata(root / ".creative" / "work" / "reviews" / "001.md")
        tasks = task_states(root)

        self.assertEqual(review["verdict"], "revise")
        self.assertEqual(review["revision_status"], "accepted")
        self.assertEqual(tasks[0], (True, "accepted"))
        self.assertTrue((root / ".creative" / "work" / "continuity.md").is_file())
        self.assertTrue((root / ".creative" / "work" / "summaries" / "001.md").is_file())
        self.assertTrue((root / ".creative" / "work" / "canon" / "characters.md").is_file())

    def test_profiles_resolve_from_fixture_work_type(self) -> None:
        for fixture, expected in (("fiction-minimal", "fiction.md"), ("blog-minimal", "blog.md")):
            with self.subTest(fixture=fixture):
                work_type = metadata(FIXTURES / fixture / ".creative" / "work" / "spec.md")["work_type"]
                self.assertEqual(f"{work_type}.md", expected)
                self.assertTrue((REPO_ROOT / "profiles" / expected).is_file())

    def test_status_equivalent_for_fixture_and_example(self) -> None:
        self.assertEqual(status_equivalent(FIXTURES / "fiction-minimal"), "plan_approval")
        self.assertEqual(status_equivalent(FIXTURES / "blog-minimal"), "complete")
        self.assertEqual(status_equivalent(REPO_ROOT / "examples" / "fiction-mini"), "drafting")


if __name__ == "__main__":
    unittest.main()
