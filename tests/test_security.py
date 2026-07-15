import pytest

from solodeveling_protocol.models import SecurityProfile
from solodeveling_protocol.security import classify_security_profiles


@pytest.mark.parametrize(
    ("summary", "expected"),
    [
        ("Expose a public web API", SecurityProfile.WEB_APPLICATION),
        ("Build an Android mobile app", SecurityProfile.MOBILE),
        ("Change login sessions and authorization", SecurityProfile.IDENTITY_ACCESS),
        ("Store personal health data", SecurityProfile.SENSITIVE_DATA),
        ("Run a destructive database migration", SecurityProfile.DATA_MIGRATION),
        ("Update package build provenance and SBOM", SecurityProfile.SUPPLY_CHAIN),
        ("Deploy Terraform and Kubernetes infrastructure", SecurityProfile.INFRASTRUCTURE),
        ("Give an LLM agent RAG and tool access", SecurityProfile.AI_AGENTIC),
        ("Process card payments at checkout", SecurityProfile.PAYMENTS),
    ],
)
def test_security_profile_triggers_are_observable(
    summary: str, expected: SecurityProfile
) -> None:
    assert expected in classify_security_profiles(summary)


def test_multiple_attack_surfaces_activate_multiple_profiles() -> None:
    profiles = classify_security_profiles(
        "Add login to a mobile app that calls a public API and stores personal data"
    )

    assert set(profiles) >= {
        SecurityProfile.MOBILE,
        SecurityProfile.WEB_APPLICATION,
        SecurityProfile.IDENTITY_ACCESS,
        SecurityProfile.SENSITIVE_DATA,
    }


def test_local_documentation_does_not_activate_a_specific_profile() -> None:
    assert classify_security_profiles("Correct a local documentation typo") == ()