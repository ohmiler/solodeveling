from pathlib import Path

from solodeveling_protocol.memory import ProjectFacts, initialize_memory
from solodeveling_protocol.secrets import detect_secret_kinds
from solodeveling_protocol.validation import validate_project


def test_detect_secret_kinds_returns_labels_not_values() -> None:
    value = "ghp_abcdefghijklmnopqrstuvwxyzABCDEFGHIJ123456"

    kinds = detect_secret_kinds(f"token: {value}")

    assert kinds == ("github-token",)
    assert value not in repr(kinds)


def test_project_validation_reports_secret_without_echoing_it(tmp_path: Path) -> None:
    initialize_memory(
        tmp_path,
        ProjectFacts(
            name="Secret fixture",
            purpose="Verify non-echoing secret diagnostics.",
            users=("Security contributors",),
            architecture="Markdown project memory.",
            stack=("Python",),
        ),
        current_goal="Detect a secret safely.",
        next_action="Run project validation.",
    )
    value = "AKIAABCDEFGHIJKLMNOP"
    (tmp_path / ".solodeveling/risks.md").write_text(
        f"---\nsolodeveling_schema: 1\n---\n{value}\n", encoding="utf-8"
    )

    issues = validate_project(tmp_path)
    secret_issues = [issue for issue in issues if issue.code == "secret-like-material"]

    assert secret_issues
    assert all(value not in issue.message for issue in secret_issues)


def test_placeholders_do_not_trigger_high_confidence_detection() -> None:
    assert detect_secret_kinds("token: <YOUR_TOKEN_HERE>") == ()