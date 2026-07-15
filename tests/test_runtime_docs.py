from pathlib import Path


def test_runtime_adapter_documentation_covers_safe_operations_and_evidence() -> None:
    text = Path("docs/runtime-adapters.md").read_text("utf-8")

    for phrase in (
        ".agents/skills",
        ".claude/skills",
        ".cursor/skills",
        "install",
        "check",
        "uninstall",
        "--dry-run",
        "modified managed",
        "unmanaged collisions",
        "behavioral claim",
        "live behavior is unverified",
    ):
        assert phrase in text


def test_adapter_cli_is_packaged() -> None:
    text = Path("pyproject.toml").read_text("utf-8")

    assert (
        'solodeveling-adapt = "solodeveling_protocol.adapter_cli:main"'
        in text
    )
