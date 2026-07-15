from pathlib import Path

from solodeveling_protocol.models import ArtifactDocument
from solodeveling_protocol.validation import validate_document


def document(metadata: dict) -> ArtifactDocument:
    return ArtifactDocument(Path("artifact.md"), metadata, "")


def test_valid_work_item_has_no_issues() -> None:
    metadata = {
        "solodeveling_schema": 1,
        "id": "WORK-001",
        "title": "Add password reset",
        "status": "active",
        "level": "critical",
        "type": "build",
        "goal": "Provide a safe password reset flow.",
        "scope": "Request and completion flows.",
        "out_of_scope": "Manual support recovery.",
        "acceptance": ["Expired tokens are rejected."],
        "risks": ["Leaked tokens could enable account takeover."],
        "decisions": [],
        "verification": ["Integration test expired and replayed tokens."],
        "next_action": "Write the failing expired-token test.",
        "security_considerations": ["Tokens are single-use and short-lived."],
        "recovery": ["Disable reset issuance and invalidate outstanding tokens."],
    }

    assert validate_document(document(metadata), "work-item") == []


def test_quick_work_item_accepts_compact_contract() -> None:
    metadata = {
        "solodeveling_schema": 1,
        "id": "WORK-002",
        "title": "Fix documentation typo",
        "status": "active",
        "level": "quick",
        "type": "change",
        "goal": "Correct a reversible documentation typo.",
        "next_action": "Correct and inspect the rendered sentence.",
    }

    assert validate_document(document(metadata), "work-item") == []


def test_work_item_reports_all_schema_failures() -> None:
    metadata = {"solodeveling_schema": 1, "id": "bad id", "status": "unknown"}

    issues = validate_document(document(metadata), "work-item")

    assert len(issues) > 1
    assert {issue.code for issue in issues} == {"schema"}


def test_unknown_artifact_kind_is_reported() -> None:
    issues = validate_document(document({"solodeveling_schema": 1}), "unknown")

    assert [(issue.code, issue.message) for issue in issues] == [
        ("unknown-kind", "Unknown artifact kind: unknown")
    ]


def test_valid_project_fixture_has_no_issues() -> None:
    from solodeveling_protocol.validation import validate_project

    root = Path("tests/fixtures/valid-project")
    assert validate_project(root) == []


def test_done_project_without_evidence_is_rejected() -> None:
    from solodeveling_protocol.validation import validate_project

    root = Path("tests/fixtures/invalid-done-project")
    issues = validate_project(root)

    assert any(issue.code == "done-without-evidence" for issue in issues)
