from pathlib import Path

from solodeveling_protocol.models import ArtifactDocument
from solodeveling_protocol.validation import validate_document


def finding(**overrides: object) -> ArtifactDocument:
    metadata = {
        "solodeveling_schema": 1,
        "id": "FINDING-001",
        "title": "Authorization bypass",
        "severity": "high",
        "confidence": "high",
        "source": "manual-review",
        "affected_asset": "Admin API",
        "evidence": ["A non-admin request reached the admin handler."],
        "impact": "Unauthorized administrative action.",
        "recommendation": "Enforce authorization at the trusted boundary.",
        "status": "open",
        "verification": [],
    }
    metadata.update(overrides)
    return ArtifactDocument(Path("FINDING-001.md"), metadata, "")


def test_valid_open_security_finding_has_no_issues() -> None:
    assert validate_document(finding(), "security-finding") == []


def test_scanner_finding_cannot_be_confirmed_without_manual_confirmation() -> None:
    issues = validate_document(
        finding(source="automated-scanner", confidence="confirmed"),
        "security-finding",
    )

    assert any("confirmation" in issue.message for issue in issues)


def test_accepted_risk_requires_owner_rationale_and_review_condition() -> None:
    issues = validate_document(finding(status="accepted-risk"), "security-finding")

    assert any("risk_acceptance" in issue.message for issue in issues)


def test_false_positive_can_preserve_verification_evidence() -> None:
    document = finding(
        status="false-positive",
        confidence="confirmed",
        verification=["Validated the generated call path is unreachable."],
    )

    assert validate_document(document, "security-finding") == []