from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from solodeveling_protocol.frontmatter import read_artifact
from solodeveling_protocol.lifecycle import (
    LifecycleError,
    archive_work,
    record_evidence,
    transition_work,
)
from solodeveling_protocol.lifecycle_cli import main
from solodeveling_protocol.memory import ProjectFacts, initialize_memory
from solodeveling_protocol.models import WorkStatus
from solodeveling_protocol.validation import validate_project


def _render(metadata: dict[str, object], body: str = "# Work\n") -> str:
    frontmatter = yaml.safe_dump(metadata, sort_keys=False)
    return f"---\n{frontmatter}---\n{body}"


def _project(tmp_path: Path) -> Path:
    initialize_memory(
        tmp_path,
        ProjectFacts(
            name="Example",
            purpose="Exercise lifecycle automation.",
            users=("Solo developers",),
            architecture="Protocol-first project.",
            stack=("Python",),
        ),
        current_goal="Complete tracked work.",
        next_action="Start WORK-001.",
    )
    work = tmp_path / ".solodeveling" / "work" / "active" / "WORK-001.md"
    work.write_text(
        _render(
            {
                "solodeveling_schema": 1,
                "id": "WORK-001",
                "title": "Improve lifecycle automation",
                "status": "active",
                "level": "standard",
                "type": "change",
                "goal": "Reduce repetitive memory commands.",
                "scope": "Lifecycle helper.",
                "out_of_scope": "Release automation.",
                "acceptance": ["Evidence and archive updates remain valid."],
                "risks": [],
                "decisions": [],
                "verification": ["Run lifecycle tests."],
                "next_action": "Record focused evidence.",
            }
        ),
        encoding="utf-8",
    )
    return tmp_path


def test_one_evidence_file_accumulates_follow_up_observations(tmp_path: Path) -> None:
    root = _project(tmp_path)
    created = record_evidence(
        root,
        "WORK-001",
        claim="Focused lifecycle test passes",
        method="Automated test",
        result="passed",
        scope="Lifecycle helper",
        command="pytest tests/test_lifecycle_cli.py",
    )
    appended = record_evidence(
        root,
        "WORK-001",
        claim="Follow-up archive test passes",
        method="Automated test",
        result="passed",
        scope="Archive behavior",
    )

    assert created.evidence_path == appended.evidence_path
    evidence = created.evidence_path.read_text(encoding="utf-8")
    assert "## Focused lifecycle test passes" in evidence
    assert "## Follow-up archive test passes" in evidence
    work = read_artifact(created.work_path)
    assert work.metadata["evidence"] == ["EVIDENCE-001"]
    summary = read_artifact(created.evidence_path)
    assert summary.metadata["claim"] == "Follow-up archive test passes"
    assert summary.metadata["result"] == "passed"
    assert validate_project(root) == []


def test_transition_and_archive_update_state_without_manual_edits(tmp_path: Path) -> None:
    root = _project(tmp_path)
    record_evidence(
        root,
        "WORK-001",
        claim="Acceptance is verified",
        method="Automated test",
        result="passed",
        scope="Lifecycle helper",
    )
    transition_work(
        root,
        "WORK-001",
        WorkStatus.VERIFYING,
        next_action="Review the evidence.",
    )
    active = read_artifact(
        root / ".solodeveling" / "work" / "active" / "WORK-001.md"
    )
    assert active.metadata["next_action"] == "Review the evidence."
    transition_work(
        root,
        "WORK-001",
        WorkStatus.DONE,
        next_action="Archive WORK-001.",
    )
    result = archive_work(
        root,
        "WORK-001",
        next_action="Select the next priority.",
        current_goal="Choose the next delivery.",
        state_summary="WORK-001 is complete and no tracked work remains.",
    )

    assert result.work_path == (
        root / ".solodeveling" / "work" / "archive" / "WORK-001.md"
    )
    assert not (
        root / ".solodeveling" / "work" / "active" / "WORK-001.md"
    ).exists()
    archived = read_artifact(result.work_path)
    assert archived.metadata["next_action"] == "None; archived."
    state = read_artifact(root / ".solodeveling" / "state.md")
    assert state.metadata["active_work"] == []
    assert state.metadata["current_goal"] == "Choose the next delivery."
    assert state.metadata["next_action"] == "Select the next priority."
    assert state.body == (
        "# State\n\nWORK-001 is complete and no tracked work remains.\n"
    )
    assert validate_project(root) == []


def test_archived_follow_up_reuses_existing_evidence(tmp_path: Path) -> None:
    root = _project(tmp_path)
    first = record_evidence(
        root,
        "WORK-001",
        claim="Initial verification passes",
        method="Automated test",
        result="passed",
        scope="Initial delivery",
    )
    transition_work(root, "WORK-001", WorkStatus.VERIFYING)
    transition_work(root, "WORK-001", WorkStatus.DONE)
    archive_work(root, "WORK-001")

    follow_up = record_evidence(
        root,
        "WORK-001",
        claim="Production follow-up is verified",
        method="Reproducible production check",
        result="passed",
        scope="Existing delivery boundary",
    )

    assert follow_up.evidence_path == first.evidence_path
    assert "Production follow-up is verified" in first.evidence_path.read_text(
        encoding="utf-8"
    )
    assert validate_project(root) == []


def test_cli_rejects_invalid_transition_without_mutation(
    tmp_path: Path,
    capsys: object,
) -> None:
    root = _project(tmp_path)
    work = root / ".solodeveling" / "work" / "active" / "WORK-001.md"
    before = work.read_text(encoding="utf-8")

    assert main(["transition", str(root), "WORK-001", "done"]) == 2

    assert work.read_text(encoding="utf-8") == before
    assert "not changed" in capsys.readouterr().out.lower()  # type: ignore[attr-defined]


def test_failed_latest_evidence_blocks_done(tmp_path: Path) -> None:
    root = _project(tmp_path)
    record_evidence(
        root,
        "WORK-001",
        claim="Focused verification fails",
        method="Automated test",
        result="failed",
        scope="Lifecycle helper",
    )
    transition_work(root, "WORK-001", WorkStatus.VERIFYING)

    with pytest.raises(LifecycleError, match="has result failed"):
        transition_work(root, "WORK-001", WorkStatus.DONE)

    work = read_artifact(
        root / ".solodeveling" / "work" / "active" / "WORK-001.md"
    )
    assert work.metadata["status"] == "verifying"
    assert validate_project(root) == []


def test_passing_observation_supersedes_failed_summary(tmp_path: Path) -> None:
    root = _project(tmp_path)
    first = record_evidence(
        root,
        "WORK-001",
        claim="Initial verification fails",
        method="Automated test",
        result="failed",
        scope="Lifecycle helper",
    )
    record_evidence(
        root,
        "WORK-001",
        claim="Corrective verification passes",
        method="Automated test",
        result="passed",
        scope="Lifecycle helper",
    )
    transition_work(root, "WORK-001", WorkStatus.VERIFYING)
    transition_work(root, "WORK-001", WorkStatus.DONE)

    evidence = read_artifact(first.evidence_path)
    assert evidence.metadata["result"] == "passed"
    assert "## Initial verification fails" in evidence.body
    assert "## Corrective verification passes" in evidence.body


def test_archived_work_rejects_non_passing_follow_up(tmp_path: Path) -> None:
    root = _project(tmp_path)
    evidence = record_evidence(
        root,
        "WORK-001",
        claim="Initial verification passes",
        method="Automated test",
        result="passed",
        scope="Initial delivery",
    )
    transition_work(root, "WORK-001", WorkStatus.VERIFYING)
    transition_work(root, "WORK-001", WorkStatus.DONE)
    archive_work(root, "WORK-001")
    before = evidence.evidence_path.read_text(encoding="utf-8")

    with pytest.raises(LifecycleError, match="requires new or reopened work"):
        record_evidence(
            root,
            "WORK-001",
            claim="Production check fails",
            method="Reproducible production check",
            result="failed",
            scope="Existing delivery",
        )

    assert evidence.evidence_path.read_text(encoding="utf-8") == before


def test_cli_rejects_invalid_work_identifier(tmp_path: Path, capsys: object) -> None:
    root = _project(tmp_path)
    state = root / ".solodeveling" / "state.md"
    before = state.read_text(encoding="utf-8")

    assert main(["transition", str(root), "../../state", "active"]) == 2

    assert state.read_text(encoding="utf-8") == before
    assert "invalid work id" in capsys.readouterr().out.lower()  # type: ignore[attr-defined]
