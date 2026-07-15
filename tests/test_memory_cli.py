from pathlib import Path

from solodeveling_protocol.memory_cli import main
from solodeveling_protocol.validation import validate_project


def arguments(root: Path) -> list[str]:
    return [
        str(root),
        "--name",
        "Example",
        "--purpose",
        "Exercise portable onboarding.",
        "--user",
        "Solo developers",
        "--architecture",
        "Protocol-first skill suite.",
        "--stack",
        "Markdown",
        "--source",
        "README.md",
        "--goal",
        "Initialize project memory.",
        "--next-action",
        "Shape the first work item.",
    ]


def test_memory_cli_initializes_and_reports_success(
    tmp_path: Path, capsys: object
) -> None:
    assert main(arguments(tmp_path)) == 0

    output = capsys.readouterr().out  # type: ignore[attr-defined]
    assert "created" in output.lower()
    assert validate_project(tmp_path) == []


def test_memory_cli_reports_idempotent_initialization(
    tmp_path: Path, capsys: object
) -> None:
    assert main(arguments(tmp_path)) == 0
    capsys.readouterr()  # type: ignore[attr-defined]

    assert main(arguments(tmp_path)) == 0

    output = capsys.readouterr().out  # type: ignore[attr-defined]
    assert "already initialized" in output.lower()
