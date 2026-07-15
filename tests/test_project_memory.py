from pathlib import Path

from solodeveling_protocol.models import ArtifactDocument
from solodeveling_protocol.validation import validate_document, validate_project


def test_valid_project_document_has_no_issues() -> None:
    document = ArtifactDocument(
        Path(".solodeveling/project.md"),
        {
            "solodeveling_schema": 1,
            "name": "Solodeveling",
            "purpose": "Provide a portable SDLC workflow for solo developers.",
            "users": ["Solo software developers"],
            "architecture": "Protocol-first portable skill suite.",
            "stack": ["Markdown", "Python"],
            "constraints": ["No correctness path requires subagents."],
            "sources": ["docs/superpowers/specs/2026-07-15-solodeveling-design.md"],
        },
        "# Project\n",
    )

    assert validate_document(document, "project") == []


def test_project_memory_requires_resume_artifacts_and_lifecycle_directories(
    tmp_path: Path,
) -> None:
    memory_root = tmp_path / ".solodeveling"
    memory_root.mkdir()

    issues = validate_project(tmp_path)

    assert {issue.code for issue in issues} == {
        "missing-project",
        "missing-state",
        "missing-active-work",
        "missing-work-archive",
        "missing-evidence-directory",
    }

def test_relative_dot_root_validates_nested_artifacts(
    tmp_path: Path, monkeypatch: object
) -> None:
    from solodeveling_protocol.memory import ProjectFacts, initialize_memory

    initialize_memory(
        tmp_path,
        ProjectFacts(
            name="Relative root fixture",
            purpose="Exercise validation from a dot root.",
            users=("Validator contributors",),
            architecture="Markdown project memory.",
            stack=("Python",),
        ),
        current_goal="Detect malformed work.",
        next_action="Validate from the project directory.",
    )
    (tmp_path / ".solodeveling/work/active/WORK-001.md").write_text(
        "---\nsolodeveling_schema: 1\n-verification: malformed\n---\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

    issues = validate_project(Path("."))

    assert any(issue.code == "schema" for issue in issues)
