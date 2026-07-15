import pytest

from solodeveling_protocol.models import WorkLevel
from solodeveling_protocol.routing import classify_level


def test_low_impact_reversible_work_can_be_quick() -> None:
    decision = classify_level("Fix a typo in local documentation", WorkLevel.QUICK)

    assert decision.level is WorkLevel.QUICK
    assert decision.triggers == ()


def test_unspecified_ordinary_feature_defaults_to_standard() -> None:
    decision = classify_level("Add filtering to the product list")

    assert decision.level is WorkLevel.STANDARD


@pytest.mark.parametrize(
    ("summary", "trigger"),
    [
        ("Change authorization checks for admin accounts", "identity-access"),
        ("Migrate sensitive customer data", "sensitive-data"),
        ("Rotate production encryption secrets", "cryptography-secrets"),
        ("Deploy a destructive database migration", "destructive-migration"),
        ("Change payment transaction settlement", "payments"),
    ],
)
def test_critical_trigger_forces_critical_level(summary: str, trigger: str) -> None:
    decision = classify_level(summary)

    assert decision.level is WorkLevel.CRITICAL
    assert trigger in decision.triggers


def test_critical_work_cannot_be_silently_downgraded() -> None:
    decision = classify_level(
        "Change login authentication", requested_level=WorkLevel.STANDARD
    )

    assert decision.level is WorkLevel.CRITICAL
    assert decision.downgrade_warning is not None


def test_explicit_risk_acceptance_allows_downgrade() -> None:
    decision = classify_level(
        "Change login authentication",
        requested_level=WorkLevel.STANDARD,
        downgrade_accepted=True,
    )

    assert decision.level is WorkLevel.STANDARD
    assert decision.downgrade_warning is not None
