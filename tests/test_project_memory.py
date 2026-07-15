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
