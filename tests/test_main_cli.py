from __future__ import annotations

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from pathlib import Path

import pytest

from solodeveling_protocol import __version__
from solodeveling_protocol.main_cli import main


def test_public_metadata_has_one_name_and_one_entry_point() -> None:
    metadata = tomllib.loads(Path("pyproject.toml").read_text("utf-8"))

    assert metadata["project"]["name"] == "solodeveling"
    assert metadata["project"]["scripts"] == {
        "solodeveling": "solodeveling_protocol.main_cli:main"
    }


@pytest.mark.parametrize("command", ["install", "check", "uninstall"])
def test_unified_cli_routes_adapter_commands(
    command: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[list[str], str]] = []

    def fake_main(argv, *, prog):
        calls.append((list(argv), prog))
        return 7

    monkeypatch.setattr(
        "solodeveling_protocol.main_cli.adapter_main", fake_main
    )

    assert main([command, "--runtime", "codex"]) == 7
    assert calls == [
        ([command, "--runtime", "codex"], f"solodeveling {command}")
    ]


@pytest.mark.parametrize(
    ("command", "target"),
    [
        ("init", "memory_main"),
        ("validate", "validate_main"),
        ("eval", "evaluation_main"),
    ],
)
def test_unified_cli_routes_component_commands(
    command: str,
    target: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[list[str], str]] = []

    def fake_main(argv, *, prog):
        calls.append((list(argv), prog))
        return 8

    monkeypatch.setattr(f"solodeveling_protocol.main_cli.{target}", fake_main)

    assert main([command, "argument"]) == 8
    assert calls == [(["argument"], f"solodeveling {command}")]


def test_unified_cli_reports_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == f"solodeveling {__version__}"


def test_unified_cli_help_has_complete_public_surface(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--help"]) == 0
    output = capsys.readouterr().out

    for command in (
        "install",
        "check",
        "uninstall",
        "init",
        "validate",
        "eval",
        "version",
    ):
        assert command in output


def test_unified_cli_rejects_unknown_command(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["adapt"]) == 2
    assert "unknown command" in capsys.readouterr().err
