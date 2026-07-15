from __future__ import annotations

from pathlib import Path

from solodeveling_protocol.adapter_cli import main


def write_skill(root: Path) -> None:
    skill = root / "solodeveling"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: solodeveling\n"
        "description: Use Solodeveling for software work.\n---\n"
        "Follow the protocol.\n",
        encoding="utf-8",
    )


def test_adapter_cli_install_check_uninstall(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "skills"
    project = tmp_path / "project"
    write_skill(source)

    assert main(
        [
            "install",
            "--runtime",
            "codex",
            "--source",
            str(source),
            "--project-root",
            str(project),
        ]
    ) == 0
    assert "installed" in capsys.readouterr().out

    assert main(
        [
            "check",
            "--runtime",
            "codex",
            "--source",
            str(source),
            "--project-root",
            str(project),
        ]
    ) == 0
    assert "conformant" in capsys.readouterr().out

    assert main(
        [
            "uninstall",
            "--runtime",
            "codex",
            "--project-root",
            str(project),
        ]
    ) == 0
    assert "uninstalled" in capsys.readouterr().out


def test_adapter_cli_returns_nonzero_for_drift(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "skills"
    project = tmp_path / "project"
    write_skill(source)
    main(
        [
            "install",
            "--runtime",
            "cursor",
            "--source",
            str(source),
            "--project-root",
            str(project),
        ]
    )
    capsys.readouterr()
    (project / ".cursor/skills/solodeveling/SKILL.md").write_text(
        "modified", encoding="utf-8"
    )

    assert main(
        [
            "check",
            "--runtime",
            "cursor",
            "--source",
            str(source),
            "--project-root",
            str(project),
        ]
    ) == 1
    assert "modified" in capsys.readouterr().out
