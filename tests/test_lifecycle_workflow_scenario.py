from pathlib import Path

from solodeveling_protocol.models import WorkStatus
from solodeveling_protocol.transitions import validate_transition


def test_portable_workflow_suite_reaches_verifying_without_superpowers() -> None:
    trace = [
        (WorkStatus.CAPTURED, WorkStatus.SHAPED, "solodeveling-shaping-work"),
        (WorkStatus.SHAPED, WorkStatus.READY, "solodeveling-planning-work"),
        (WorkStatus.READY, WorkStatus.ACTIVE, "solodeveling-executing-work"),
        (WorkStatus.ACTIVE, WorkStatus.VERIFYING, "solodeveling-verifying"),
    ]
    current = WorkStatus.CAPTURED
    metadata = {"level": "standard"}

    for expected_current, target, skill_name in trace:
        assert current is expected_current
        skill_text = Path(f"skills/{skill_name}/SKILL.md").read_text("utf-8")
        assert "superpowers:" not in skill_text.lower()
        validate_transition(current, target, metadata)
        current = target

    debugging = Path("skills/solodeveling-debugging/SKILL.md").read_text("utf-8")
    assert "root cause" in debugging.lower()
    assert current is WorkStatus.VERIFYING


def test_standard_delivery_owns_the_uninterrupted_standard_trace() -> None:
    skill = Path('skills/solodeveling-standard-delivery/SKILL.md').read_text('utf-8')

    for phrase in (
        'Shape, plan, execute, and verify',
        'Persist `active` once',
        'persist `done`, and archive once',
        'controlled condition',
    ):
        assert phrase.lower() in skill.lower()

    current = WorkStatus.CAPTURED
    for target in (
        WorkStatus.SHAPED,
        WorkStatus.READY,
        WorkStatus.ACTIVE,
        WorkStatus.VERIFYING,
    ):
        validate_transition(current, target, {'level': 'standard'})
        current = target

    assert current is WorkStatus.VERIFYING
