from __future__ import annotations

from collections.abc import Mapping

from solodeveling_protocol.models import WorkStatus


class TransitionError(ValueError):
    """Raised when a work-item state transition violates the protocol."""


ALLOWED_TRANSITIONS: dict[WorkStatus, frozenset[WorkStatus]] = {
    WorkStatus.CAPTURED: frozenset({WorkStatus.SHAPED, WorkStatus.DEFERRED}),
    WorkStatus.SHAPED: frozenset({WorkStatus.READY, WorkStatus.DEFERRED}),
    WorkStatus.READY: frozenset(
        {WorkStatus.ACTIVE, WorkStatus.BLOCKED, WorkStatus.DEFERRED}
    ),
    WorkStatus.ACTIVE: frozenset(
        {WorkStatus.VERIFYING, WorkStatus.BLOCKED, WorkStatus.DEFERRED}
    ),
    WorkStatus.VERIFYING: frozenset(
        {WorkStatus.ACTIVE, WorkStatus.DONE, WorkStatus.BLOCKED}
    ),
    WorkStatus.BLOCKED: frozenset({WorkStatus.ACTIVE, WorkStatus.DEFERRED}),
    WorkStatus.DEFERRED: frozenset({WorkStatus.ACTIVE}),
    WorkStatus.DONE: frozenset(),
}


def validate_transition(
    current: WorkStatus, target: WorkStatus, metadata: Mapping[str, object]
) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise TransitionError(f"Transition {current} -> {target} is not allowed")

    if target is not WorkStatus.DONE:
        return

    evidence = metadata.get("evidence") or []
    gaps = metadata.get("accepted_verification_gaps") or []
    if not evidence and not gaps:
        raise TransitionError(
            "done requires evidence or an accepted verification gap"
        )

    if metadata.get("level") == "critical":
        security = metadata.get("security_considerations") or []
        recovery = metadata.get("recovery") or []
        if not security or not recovery:
            raise TransitionError(
                "critical done requires security and recovery consideration"
            )
