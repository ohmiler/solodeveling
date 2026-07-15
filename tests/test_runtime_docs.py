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

    assert 'solodeveling = "solodeveling_protocol.main_cli:main"' in text
    assert "solodeveling-adapt" not in text


def test_primary_installation_ux_requires_no_flags() -> None:
    readme = Path("README.md").read_text("utf-8")
    quick_start = readme.split("## Quick start", 1)[1].split(
        "## Automatic project installation", 1
    )[0]
    assert "npx solodeveling install" in quick_start
    assert "--runtime" not in quick_start
    assert "--dry-run" not in quick_start

    installation = Path("docs/installation.md").read_text("utf-8")
    primary = installation.split("## Choose an installation path", 1)[1].split(
        "## Supported release targets", 1
    )[0]
    assert "npx solodeveling install" in primary
    assert "--runtime" not in primary
    assert "--dry-run" not in primary
