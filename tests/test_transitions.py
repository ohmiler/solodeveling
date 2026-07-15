import pytest

from solodeveling_protocol.models import WorkStatus
from solodeveling_protocol.transitions import TransitionError, validate_transition


def metadata(**overrides: object) -> dict:
    value = {
        "level": "standard",
        "evidence": ["EVIDENCE-001"],
        "accepted_verification_gaps": [],
        "security_considerations": [],
        "recovery": [],
    }
    value.update(overrides)
    return value


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (WorkStatus.CAPTURED, WorkStatus.SHAPED),
        (WorkStatus.SHAPED, WorkStatus.READY),
        (WorkStatus.READY, WorkStatus.ACTIVE),
        (WorkStatus.ACTIVE, WorkStatus.VERIFYING),
        (WorkStatus.VERIFYING, WorkStatus.DONE),
        (WorkStatus.ACTIVE, WorkStatus.BLOCKED),
        (WorkStatus.BLOCKED, WorkStatus.ACTIVE),
        (WorkStatus.ACTIVE, WorkStatus.DEFERRED),
    ],
)
def test_allowed_transition(current: WorkStatus, target: WorkStatus) -> None:
    validate_transition(current, target, metadata())


def test_cannot_skip_verifying() -> None:
    with pytest.raises(TransitionError, match="not allowed"):
        validate_transition(WorkStatus.ACTIVE, WorkStatus.DONE, metadata())


def test_done_requires_evidence_or_accepted_gap() -> None:
    with pytest.raises(TransitionError, match="evidence or an accepted verification gap"):
        validate_transition(
            WorkStatus.VERIFYING,
            WorkStatus.DONE,
            metadata(evidence=[], accepted_verification_gaps=[]),
        )


def test_critical_done_requires_security_and_recovery() -> None:
    with pytest.raises(TransitionError, match="security and recovery"):
        validate_transition(
            WorkStatus.VERIFYING,
            WorkStatus.DONE,
            metadata(level="critical"),
        )


def test_critical_done_accepts_security_and_recovery() -> None:
    validate_transition(
        WorkStatus.VERIFYING,
        WorkStatus.DONE,
        metadata(
            level="critical",
            security_considerations=["Threat model reviewed."],
            recovery=["Rollback procedure verified."],
        ),
    )
