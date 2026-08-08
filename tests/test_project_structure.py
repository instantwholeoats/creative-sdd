from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
EXPECTED_SKILLS = {
    "creative-discovery",
    "creative-spec",
    "creative-plan",
    "creative-draft",
    "creative-review",
    "creative-revise",
    "creative-status",
}
EXPECTED_TEMPLATES = {
    "brief.md",
    "spec-fiction.md",
    "spec-blog.md",
    "design.md",
    "outline.md",
    "tasks.md",
    "continuity.md",
    "summary.md",
    "review.md",
    "canon-characters.md",
    "canon-world.md",
    "canon-timeline.md",
    "canon-terminology.md",
}


def frontmatter(text: str) -> dict[str, str]:
    self_closing = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not self_closing:
        return {}
    metadata: dict[str, str] = {}
    for line in self_closing.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"\'')
    return metadata


class ProjectStructureTests(unittest.TestCase):
    def test_all_v01_skills_have_valid_required_metadata(self) -> None:
        actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(actual, EXPECTED_SKILLS)

        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                skill_path = SKILLS_ROOT / name / "SKILL.md"
                metadata = frontmatter(skill_path.read_text(encoding="utf-8"))
                self.assertEqual(metadata.get("name"), name)
                self.assertGreaterEqual(len(metadata.get("description", "")), 20)

                openai_yaml = (SKILLS_ROOT / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertRegex(openai_yaml, r"(?m)^interface:\s*$")
                self.assertRegex(openai_yaml, r"(?m)^  display_name: \"[^\"]+\"$")
                self.assertRegex(openai_yaml, r"(?m)^  short_description: \"[^\"]+\"$")
                self.assertIn(f'"${name} ', openai_yaml)

    def test_required_templates_and_profiles_exist(self) -> None:
        templates = {path.name for path in (REPO_ROOT / "templates").glob("*.md")}
        self.assertTrue(EXPECTED_TEMPLATES <= templates)
        self.assertTrue((REPO_ROOT / "profiles" / "fiction.md").is_file())
        self.assertTrue((REPO_ROOT / "profiles" / "blog.md").is_file())

    def test_fixture_kinds_and_example_exist(self) -> None:
        self.assertTrue((REPO_ROOT / "tests" / "fixtures" / "fiction-minimal").is_dir())
        self.assertTrue((REPO_ROOT / "tests" / "fixtures" / "blog-minimal").is_dir())
        self.assertTrue((REPO_ROOT / "examples" / "fiction-mini").is_dir())

    def test_work_type_skills_reference_profiles_without_using_them_as_forms(self) -> None:
        for name in ("creative-discovery", "creative-spec", "creative-plan", "creative-draft", "creative-review"):
            with self.subTest(skill=name):
                text = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("../../../profiles/fiction.md", text)
                self.assertIn("../../../profiles/blog.md", text)

        discovery = (SKILLS_ROOT / "creative-discovery" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("固定質問票として網羅しない", discovery)

    def test_readme_documented_paths_and_commands_are_real(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        paths = [
            ".agents/skills",
            "templates",
            "profiles",
            "scripts/creative_lint.py",
            "examples/fiction-mini",
            "tests/fixtures/fiction-minimal",
            "tests/fixtures/blog-minimal",
        ]
        for relative in paths:
            with self.subTest(path=relative):
                self.assertIn(relative, readme)
                self.assertTrue((REPO_ROOT / relative).exists())

        self.assertIn("python3 -m unittest discover -s tests -v", readme)
        self.assertIn("python3 scripts/creative_lint.py --root examples/fiction-mini", readme)
        self.assertIn("test -e /path/to/my-work/AGENTS.md || cp", readme)

    def test_readme_starts_from_plain_language_and_covers_the_lifecycle(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        intro = readme[:1000]
        self.assertIn("書きたいものを普通の言葉で話してください", intro)
        self.assertIn("$creative-discovery", intro)

        required_terms = [
            "Spec",
            "Plan",
            "Draft",
            "原稿受理",
            "Review",
            "Revision",
            "Reconciliation",
            "$creative-status",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, readme)


if __name__ == "__main__":
    unittest.main()
