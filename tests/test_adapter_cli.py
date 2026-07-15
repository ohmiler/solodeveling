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


def test_zero_config_install_check_and_uninstall_use_standard_path(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "skills"
    project = tmp_path / "project"
    write_skill(source)

    assert main(
        ["install", "--source", str(source), "--project-root", str(project)]
    ) == 0
    assert "installed" in capsys.readouterr().out
    assert (
        project / ".agents/skills/.solodeveling-manifest.json"
    ).is_file()

    assert main(
        ["check", "--source", str(source), "--project-root", str(project)]
    ) == 0
    assert "conformant" in capsys.readouterr().out

    assert main(["uninstall", "--project-root", str(project)]) == 0
    assert "uninstalled" in capsys.readouterr().out
    assert not (
        project / ".agents/skills/.solodeveling-manifest.json"
    ).exists()


def test_zero_config_install_detects_all_distinct_project_runtimes(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "skills"
    project = tmp_path / "project"
    write_skill(source)
    (project / ".claude").mkdir(parents=True)
    (project / ".cursor").mkdir()

    assert main(
        ["install", "--source", str(source), "--project-root", str(project)]
    ) == 0
    output = capsys.readouterr().out
    assert "claude-code" in output
    assert "cursor" in output
    assert (project / ".claude/skills/.solodeveling-manifest.json").is_file()
    assert (project / ".cursor/skills/.solodeveling-manifest.json").is_file()
    assert not (project / ".agents/skills").exists()


def test_zero_config_install_preflights_every_runtime_before_writing(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "skills"
    project = tmp_path / "project"
    write_skill(source)
    (project / ".codex").mkdir(parents=True)
    collision = project / ".cursor/skills/solodeveling/SKILL.md"
    collision.parent.mkdir(parents=True)
    collision.write_text("user-owned", encoding="utf-8")

    assert main(
        ["install", "--source", str(source), "--project-root", str(project)]
    ) == 1
    assert "unmanaged collision" in capsys.readouterr().out
    assert collision.read_text("utf-8") == "user-owned"
    assert not (project / ".agents/skills").exists()


def test_zero_config_check_and_uninstall_fail_when_nothing_is_managed(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "skills"
    project = tmp_path / "project"
    write_skill(source)

    assert main(
        ["check", "--source", str(source), "--project-root", str(project)]
    ) == 1
    assert "no managed Solodeveling installation" in capsys.readouterr().out
    assert main(["uninstall", "--project-root", str(project)]) == 1
    assert "no managed Solodeveling installation" in capsys.readouterr().out
