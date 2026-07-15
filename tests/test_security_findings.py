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

def test_project_validator_discovers_security_findings(tmp_path: Path) -> None:
    from solodeveling_protocol.memory import ProjectFacts, initialize_memory
    from solodeveling_protocol.validation import validate_project

    initialize_memory(
        tmp_path,
        ProjectFacts(
            name="Finding fixture",
            purpose="Validate nested security findings.",
            users=("Security contributors",),
            architecture="Markdown project memory.",
            stack=("Python",),
        ),
        current_goal="Validate a finding.",
        next_action="Inspect validation issues.",
    )
    findings = tmp_path / ".solodeveling/security/findings"
    findings.mkdir(parents=True)
    (findings / "FINDING-001.md").write_text(
        "---\n"
        "solodeveling_schema: 1\n"
        "id: FINDING-001\n"
        "title: Scanner result\n"
        "severity: medium\n"
        "confidence: confirmed\n"
        "source: automated-scanner\n"
        "affected_asset: Build artifact\n"
        "evidence: [Scanner output requires confirmation.]\n"
        "impact: Potential dependency exposure.\n"
        "recommendation: Confirm reachability.\n"
        "status: open\n"
        "verification: []\n"
        "---\n",
        encoding="utf-8",
    )

    issues = validate_project(tmp_path)

    assert any("confirmation" in issue.message for issue in issues)
