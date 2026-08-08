#!/usr/bin/env python3
"""CreativeSDDの決定論的なMarkdown構造検査。"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SPEC_STATUSES = {"draft", "approved"}
WORK_TYPES = {"fiction", "blog"}
ACCEPTANCE_STATUSES = {"pending", "accepted"}
VERDICTS = {"pass", "revise"}
REVISION_STATUSES = {"not_required", "pending", "applied", "accepted"}
SEVERITIES = {"BLOCKER", "MAJOR", "MINOR", "OPTIONAL"}
FINDING_STATUSES = {"proposed", "approved", "rejected", "resolved"}
TASK_REQUIRED_FIELDS = {"Goal", "Boundary", "Output", "Outline unit", "Depends"}
REVIEW_REQUIRED_HEADINGS = {
    "Verdict",
    "Blockers",
    "Major Findings",
    "Minor Findings",
    "Optional Editorial Suggestions",
    "Continuity Findings",
    "Spec Compliance",
    "Recommended Revision Scope",
}
FINDING_REQUIRED_FIELDS = {"severity", "status", "location", "issue", "evidence", "recommendation"}


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    path: str
    message: str


@dataclass
class Task:
    task_id: str
    complete: bool
    fields: dict[str, str]
    line: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return metadata, True
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return metadata, False
        key, value = line.split(":", 1)
        metadata[key.strip()] = unquote(value)
    return metadata, False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_tasks(text: str) -> tuple[list[Task], list[tuple[int, str]]]:
    tasks: list[Task] = []
    malformed: list[tuple[int, str]] = []
    current: Task | None = None
    valid_pattern = re.compile(r"^- \[([ xX])\] ([0-9]+)\.\s+.+$")
    task_like_pattern = re.compile(r"^- \[[ xX]\] (.+?)\.\s+.+$")
    field_pattern = re.compile(r"^\s{2,}- ([A-Za-z][A-Za-z ]*):\s*(.*)$")

    for line_number, line in enumerate(text.splitlines(), 1):
        match = valid_pattern.match(line)
        if match:
            current = Task(
                task_id=match.group(2),
                complete=match.group(1).lower() == "x",
                fields={},
                line=line_number,
            )
            tasks.append(current)
            continue
        if task_like_pattern.match(line):
            malformed.append((line_number, line))
            current = None
            continue
        field_match = field_pattern.match(line)
        if current and field_match:
            current.fields[field_match.group(1)] = field_match.group(2).strip()
    return tasks, malformed


def parse_findings(text: str) -> list[tuple[str, dict[str, str], int]]:
    findings: list[tuple[str, dict[str, str], int]] = []
    lines = text.splitlines()
    heading_pattern = re.compile(r"^### (RV-[0-9]{3})\s*$")
    field_pattern = re.compile(r"^- ([a-z_]+):\s*(.*)$")
    index = 0
    while index < len(lines):
        match = heading_pattern.match(lines[index])
        if not match:
            index += 1
            continue
        finding_id = match.group(1)
        fields: dict[str, str] = {}
        line_number = index + 1
        index += 1
        while index < len(lines):
            if lines[index].startswith("## ") or heading_pattern.match(lines[index]):
                break
            field_match = field_pattern.match(lines[index])
            if field_match:
                fields[field_match.group(1)] = field_match.group(2).strip()
            index += 1
        findings.append((finding_id, fields, line_number))
    return findings


class Linter:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.issues: list[Issue] = []
        self.work = self.root / ".creative" / "work"
        self.tasks: list[Task] = []

    def add(self, level: str, code: str, path: Path, message: str) -> None:
        self.issues.append(Issue(level, code, display_path(path, self.root), message))

    def error(self, code: str, path: Path, message: str) -> None:
        self.add("ERROR", code, path, message)

    def warning(self, code: str, path: Path, message: str) -> None:
        self.add("WARNING", code, path, message)

    def check_markdown_heading(self, path: Path) -> None:
        text = read_text(path)
        body = text
        if text.startswith("---\n"):
            parts = text.split("---", 2)
            body = parts[2] if len(parts) == 3 else ""
        if not re.search(r"(?m)^#\s+\S", body):
            self.error("markdown.missing_h1", path, "H1 headingがありません")

    def check_frontmatter_file(
        self,
        path: Path,
        required: dict[str, set[str] | None],
    ) -> dict[str, str]:
        metadata, valid = parse_frontmatter(read_text(path))
        if not valid:
            self.error("frontmatter.invalid", path, "閉じたYAML frontmatterが必要です")
            return metadata
        for key, values in required.items():
            value = metadata.get(key, "")
            if not value:
                self.error("frontmatter.missing_key", path, f"{key}がありません")
            elif values is not None and value not in values:
                allowed = ", ".join(sorted(values))
                self.error(
                    "frontmatter.invalid_value",
                    path,
                    f"{key}={value}は無効です（{allowed}）",
                )
        return metadata

    def check_spec_and_plan(self) -> str | None:
        spec_path = self.work / "spec.md"
        work_type: str | None = None
        if spec_path.exists():
            metadata = self.check_frontmatter_file(
                spec_path,
                {"status": SPEC_STATUSES, "work_type": WORK_TYPES, "language": None},
            )
            work_type = metadata.get("work_type")
            self.check_markdown_heading(spec_path)
        else:
            self.warning("project.missing_spec", spec_path, "Specはまだありません")

        design_path = self.work / "design.md"
        if design_path.exists():
            self.check_frontmatter_file(design_path, {"status": SPEC_STATUSES})
            self.check_markdown_heading(design_path)
        return work_type

    def check_outline(self) -> None:
        outline_path = self.work / "outline.md"
        if not outline_path.exists():
            return
        self.check_markdown_heading(outline_path)
        unit_ids = re.findall(r"(?m)^## Unit\s+([^:\s]+)", read_text(outline_path))
        seen: set[str] = set()
        for unit_id in unit_ids:
            if unit_id in seen:
                self.error("outline.duplicate_unit_id", outline_path, f"Unit ID {unit_id}が重複しています")
            seen.add(unit_id)

    def safe_output_path(self, output: str) -> Path | None:
        candidate = Path(output)
        if candidate.is_absolute() or ".." in candidate.parts:
            return None
        if not candidate.parts or candidate.parts[0] != "manuscript":
            return None
        return self.root / candidate

    def check_tasks(self, work_type: str | None) -> dict[str, Task]:
        tasks_path = self.work / "tasks.md"
        by_output: dict[str, Task] = {}
        if not tasks_path.exists():
            return by_output
        self.check_markdown_heading(tasks_path)
        self.tasks, malformed = parse_tasks(read_text(tasks_path))
        for line, _ in malformed:
            self.error("task.invalid_id", tasks_path, f"line {line}: task IDは数値で記述してください")

        seen_ids: set[str] = set()
        seen_outputs: set[str] = set()
        for task in self.tasks:
            normalized_task_id = str(int(task.task_id))
            if normalized_task_id in seen_ids:
                self.error("task.duplicate_id", tasks_path, f"Task ID {task.task_id}が重複しています")
            seen_ids.add(normalized_task_id)

            for field in sorted(TASK_REQUIRED_FIELDS - task.fields.keys()):
                self.error("task.missing_field", tasks_path, f"Task {task.task_id}に{field}がありません")

            output = task.fields.get("Output", "")
            if not output:
                self.error("task.missing_output", tasks_path, f"Task {task.task_id}にOutputがありません")
                continue
            output_path = self.safe_output_path(output)
            if output_path is None:
                self.error("task.invalid_output", tasks_path, f"Task {task.task_id}のOutputはmanuscript/配下にしてください")
                continue
            if output in seen_outputs and work_type == "fiction":
                self.error("task.duplicate_output", tasks_path, f"fictionのOutput {output}が重複しています")
            seen_outputs.add(output)
            by_output[output] = task

            filename = Path(output).name
            if work_type == "fiction" and not re.fullmatch(r"[0-9]{3}\.md", filename):
                self.error("task.invalid_fiction_filename", tasks_path, f"Task {task.task_id}のfiction原稿名は3桁連番.mdにしてください")
            if work_type == "blog" and filename != "article.md":
                self.warning("task.unusual_blog_filename", tasks_path, f"Task {task.task_id}のblog原稿名は通常article.mdです")

            acceptance = task.fields.get("Acceptance")
            if acceptance is None:
                acceptance = "pending"
                self.warning("task.missing_acceptance", tasks_path, f"Task {task.task_id}は旧形式のためAcceptanceをpendingとして扱います")
            elif acceptance not in ACCEPTANCE_STATUSES:
                self.error("task.invalid_acceptance", tasks_path, f"Task {task.task_id}のAcceptance={acceptance}は無効です")

            if task.complete and not output_path.is_file():
                self.error("task.missing_manuscript", tasks_path, f"完了Task {task.task_id}の{output}がありません")
            if acceptance == "accepted" and not task.complete:
                self.error("task.accepted_incomplete", tasks_path, f"Task {task.task_id}は未完了なのにacceptedです")
            if acceptance == "accepted" and not output_path.is_file():
                self.error("task.accepted_missing_manuscript", tasks_path, f"accepted Task {task.task_id}の原稿がありません")
        return by_output

    def check_manuscripts(self, by_output: dict[str, Task]) -> None:
        manuscript_dir = self.root / "manuscript"
        if not manuscript_dir.exists():
            return
        referenced = set(by_output)
        for path in sorted(manuscript_dir.glob("*.md")):
            self.check_markdown_heading(path)
            relative = display_path(path, self.root)
            if relative not in referenced:
                self.warning("task.unreferenced_manuscript", path, "対応するtask Outputがありません")

    def check_reviews(self) -> None:
        reviews_dir = self.work / "reviews"
        if not reviews_dir.exists():
            return
        for path in sorted(reviews_dir.glob("*.md")):
            review_text = read_text(path)
            metadata = self.check_frontmatter_file(
                path,
                {
                    "unit": None,
                    "manuscript": None,
                    "manuscript_sha256": None,
                    "verdict": VERDICTS,
                    "revision_status": REVISION_STATUSES,
                },
            )
            self.check_markdown_heading(path)
            headings = set(re.findall(r"(?m)^##\s+(.+?)\s*$", review_text))
            for heading in sorted(REVIEW_REQUIRED_HEADINGS - headings):
                self.error("review.missing_heading", path, f"## {heading}がありません")
            unit = metadata.get("unit", "")
            task: Task | None = None
            if not re.fullmatch(r"[0-9]+", unit):
                self.error("review.invalid_unit", path, "unitは数値Task IDで記録してください")
            else:
                expected_filename = f"{int(unit):03d}.md"
                if path.name != expected_filename:
                    self.error("review.filename_mismatch", path, f"unit {unit}のReview名は{expected_filename}です")
                normalized_unit = str(int(unit))
                task = next(
                    (candidate for candidate in self.tasks if str(int(candidate.task_id)) == normalized_unit),
                    None,
                )
                if task is None:
                    self.error("review.unmatched_task", path, f"unit {unit}に対応するtaskがありません")
            manuscript = metadata.get("manuscript", "")
            manuscript_path = self.safe_output_path(manuscript) if manuscript else None
            if manuscript_path is None:
                self.error("review.invalid_manuscript", path, "manuscriptはmanuscript/配下を指定してください")
            elif not manuscript_path.is_file():
                self.error("review.missing_manuscript", path, f"対象原稿{manuscript}がありません")
            else:
                recorded_hash = metadata.get("manuscript_sha256", "")
                if not re.fullmatch(r"[0-9a-f]{64}", recorded_hash):
                    self.error("review.invalid_hash", path, "manuscript_sha256は64桁の小文字hexで記録してください")
                elif recorded_hash != sha256(manuscript_path):
                    self.warning("review.stale", path, "Review作成後に対象原稿が変更されています。再Reviewが必要です")

            findings = parse_findings(review_text)
            seen_findings: set[str] = set()
            has_required_finding = False
            approved = False
            for finding_id, fields, line in findings:
                if finding_id in seen_findings:
                    self.error("review.duplicate_finding_id", path, f"line {line}: {finding_id}が重複しています")
                seen_findings.add(finding_id)
                for field in sorted(FINDING_REQUIRED_FIELDS - fields.keys()):
                    self.error("review.missing_finding_field", path, f"{finding_id}に{field}がありません")
                for field in sorted(FINDING_REQUIRED_FIELDS & fields.keys()):
                    if not fields[field]:
                        self.error("review.empty_finding_field", path, f"{finding_id}の{field}が空です")
                severity = fields.get("severity", "")
                status = fields.get("status", "")
                if severity not in SEVERITIES:
                    self.error("review.invalid_severity", path, f"{finding_id}のseverity={severity}は無効です")
                if status not in FINDING_STATUSES:
                    self.error("review.invalid_finding_status", path, f"{finding_id}のstatus={status}は無効です")
                if severity in {"BLOCKER", "MAJOR", "MINOR"}:
                    has_required_finding = True
                if status == "approved":
                    approved = True

            verdict = metadata.get("verdict")
            revision_status = metadata.get("revision_status")
            if verdict == "pass" and has_required_finding:
                self.error("review.verdict_conflict", path, "必須指摘があるReviewはverdict: passにできません")
            if verdict == "revise" and not has_required_finding:
                self.error("review.verdict_conflict", path, "必須指摘がないReviewはverdict: reviseにできません")
            if verdict == "revise" and revision_status == "not_required":
                self.error("review.revision_status_conflict", path, "verdict: reviseでnot_requiredは使用できません")
            if revision_status in {"applied", "accepted"} and approved:
                self.error("review.unapplied_approved_finding", path, "Revision適用後もapproved指摘が残っています")

            if task and task.fields.get("Output", "") != manuscript:
                self.error(
                    "review.task_manuscript_mismatch",
                    path,
                    f"unit {unit}のtask Outputとmanuscriptが一致しません",
                )
            if revision_status == "applied" and task and task.fields.get("Acceptance", "pending") != "pending":
                self.error("review.applied_acceptance_conflict", path, "Revision applied時のAcceptanceはpendingです")
            if revision_status == "accepted" and task and task.fields.get("Acceptance", "pending") != "accepted":
                self.error("review.accepted_acceptance_conflict", path, "Revision accepted時のAcceptanceはacceptedです")

    def run(self) -> list[Issue]:
        agents_path = self.root / "AGENTS.md"
        if not agents_path.is_file():
            self.error("project.missing_agents", agents_path, "AGENTS.mdがありません")
        work_type = self.check_spec_and_plan()
        self.check_outline()
        by_output = self.check_tasks(work_type)
        self.check_manuscripts(by_output)
        self.check_reviews()
        return sorted(set(self.issues), key=lambda item: (item.level != "ERROR", item.path, item.code, item.message))


def main() -> int:
    parser = argparse.ArgumentParser(description="CreativeSDDの決定論的な構造を検査する")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="作品Repositoryのroot")
    args = parser.parse_args()

    issues = Linter(args.root).run()
    for issue in issues:
        print(f"{issue.level} {issue.code} {issue.path}: {issue.message}")
    errors = sum(issue.level == "ERROR" for issue in issues)
    warnings = sum(issue.level == "WARNING" for issue in issues)
    result = "pass" if errors == 0 else "fail"
    print(f"creative-lint: {result} ({errors} errors, {warnings} warnings)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
