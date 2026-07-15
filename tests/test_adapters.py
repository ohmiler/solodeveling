from __future__ import annotations

import json
from pathlib import Path

import pytest

from solodeveling_protocol import adapters
from solodeveling_protocol.adapters import (
    AdapterError,
    RUNTIME_PATHS,
    check_adapter,
    install_adapter,
    manifest_path,
    uninstall_adapter,
)


def write_skill(root: Path, name: str, extra: str = "") -> Path:
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\n"
        f"description: Use {name} for a concrete workflow.\n---\n"
        f"# {name}\n\nFollow the canonical workflow.\n{extra}",
        encoding="utf-8",
    )
    references = skill / "references"
    references.mkdir()
    (references / "protocol.md").write_bytes(b"canonical\r\nbytes\n")
    return skill


@pytest.fixture
def source_skills(tmp_path: Path) -> Path:
    source = tmp_path / "skills"
    write_skill(source, "solodeveling")
    write_skill(source, "solodeveling-verifying")
    return source


def test_runtime_paths_are_native_and_semantics_neutral() -> None:
    assert RUNTIME_PATHS == {
        "codex": Path(".agents/skills"),
        "claude-code": Path(".claude/skills"),
        "cursor": Path(".cursor/skills"),
        "generic": Path(".agents/skills"),
    }


def test_install_copies_exact_bytes_and_records_manifest(
    source_skills: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    report = install_adapter(source_skills, project, "codex")

    assert report.ok
    installed = project / ".agents/skills/solodeveling/references/protocol.md"
    assert installed.read_bytes() == (
        source_skills / "solodeveling/references/protocol.md"
    ).read_bytes()

    manifest = json.loads(manifest_path(project, "codex").read_text("utf-8"))
    assert manifest["solodeveling_adapter_schema"] == 1
    assert manifest["runtime"] == "codex"
    assert manifest["adapter_root"] == ".agents/skills"
    assert manifest["source_digest"].startswith("sha256:")
    assert manifest["files"]["solodeveling/SKILL.md"].startswith("sha256:")
    assert manifest["files"]["solodeveling/references/protocol.md"].startswith(
        "sha256:"
    )


def test_install_preflight_rejects_unmanaged_collision_without_partial_write(
    source_skills: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    collision = project / ".agents/skills/solodeveling/SKILL.md"
    collision.parent.mkdir(parents=True)
    collision.write_text("user-owned", encoding="utf-8")

    with pytest.raises(AdapterError, match="unmanaged collision"):
        install_adapter(source_skills, project, "codex")

    assert collision.read_text("utf-8") == "user-owned"
    assert not (project / ".agents/skills/solodeveling-verifying").exists()
    assert not manifest_path(project, "codex").exists()


def test_invalid_skill_is_rejected_before_target_write(
    source_skills: Path, tmp_path: Path
) -> None:
    skill_file = source_skills / "solodeveling/SKILL.md"
    skill_file.write_text(
        "---\nname: wrong-name\ndescription: Invalid identity.\n---\n",
        encoding="utf-8",
    )
    project = tmp_path / "project"

    with pytest.raises(AdapterError, match="name must match"):
        install_adapter(source_skills, project, "claude-code")

    assert not (project / ".claude").exists()


def test_check_reports_modified_missing_unexpected_and_source_drift(
    source_skills: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    install_adapter(source_skills, project, "cursor")
    root = project / ".cursor/skills"
    (root / "solodeveling/SKILL.md").write_text("modified", encoding="utf-8")
    (root / "solodeveling/references/protocol.md").unlink()
    (root / "solodeveling/unexpected.txt").write_text("extra", encoding="utf-8")
    (source_skills / "solodeveling-verifying/SKILL.md").write_text(
        "---\nname: solodeveling-verifying\n"
        "description: Changed canonical source.\n---\n",
        encoding="utf-8",
    )

    report = check_adapter(source_skills, project, "cursor")

    assert not report.ok
    assert {issue.code for issue in report.issues} == {
        "modified",
        "missing",
        "unexpected",
        "source-drift",
    }


def test_uninstall_refuses_modified_managed_file_and_preserves_everything(
    source_skills: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    install_adapter(source_skills, project, "claude-code")
    root = project / ".claude/skills"
    modified = root / "solodeveling/SKILL.md"
    modified.write_text("user modification", encoding="utf-8")
    unrelated = root / "user-skill/SKILL.md"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("user owned", encoding="utf-8")

    with pytest.raises(AdapterError, match="modified managed file"):
        uninstall_adapter(project, "claude-code")

    assert modified.read_text("utf-8") == "user modification"
    assert unrelated.read_text("utf-8") == "user owned"
    assert (root / "solodeveling-verifying/SKILL.md").exists()
    assert manifest_path(project, "claude-code").exists()


def test_uninstall_removes_only_managed_files(
    source_skills: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    install_adapter(source_skills, project, "cursor")
    root = project / ".cursor/skills"
    unrelated = root / "user-skill/SKILL.md"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("user owned", encoding="utf-8")

    report = uninstall_adapter(project, "cursor")

    assert report.ok
    assert unrelated.read_text("utf-8") == "user owned"
    assert not (root / "solodeveling").exists()
    assert not (root / "solodeveling-verifying").exists()
    assert not manifest_path(project, "cursor").exists()


def test_dry_run_never_changes_target(source_skills: Path, tmp_path: Path) -> None:
    project = tmp_path / "project"

    install_report = install_adapter(source_skills, project, "generic", dry_run=True)

    assert install_report.dry_run
    assert not project.exists()

    install_adapter(source_skills, project, "generic")
    before = {
        path.relative_to(project): path.read_bytes()
        for path in project.rglob("*")
        if path.is_file()
    }
    uninstall_report = uninstall_adapter(project, "generic", dry_run=True)
    after = {
        path.relative_to(project): path.read_bytes()
        for path in project.rglob("*")
        if path.is_file()
    }

    assert uninstall_report.dry_run
    assert after == before


def test_install_rolls_back_files_created_by_failed_attempt(
    source_skills: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    original = adapters._atomic_copy
    calls = 0

    def fail_second(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated write failure")
        original(source, destination)

    monkeypatch.setattr(adapters, "_atomic_copy", fail_second)

    with pytest.raises(AdapterError, match="rolled back"):
        install_adapter(source_skills, project, "codex")

    assert not any(
        path.is_file()
        for path in (project / ".agents/skills").rglob("*")
    )
    assert not manifest_path(project, "codex").exists()


def test_tampered_manifest_cannot_escape_project(
    source_skills: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    install_adapter(source_skills, project, "codex")
    victim = tmp_path / "victim.txt"
    victim.write_text("do not delete", encoding="utf-8")
    path = manifest_path(project, "codex")
    manifest = json.loads(path.read_text("utf-8"))
    manifest["files"]["../../../victim.txt"] = "sha256:malicious"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(AdapterError, match="unsafe manifest path"):
        uninstall_adapter(project, "codex")

    assert victim.read_text("utf-8") == "do not delete"

def test_parent_path_collision_is_rejected_before_copy(
    source_skills: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    (project / ".agents").write_text("not a directory", encoding="utf-8")
    calls = 0

    def count_copy(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1

    monkeypatch.setattr(adapters, "_atomic_copy", count_copy)

    with pytest.raises(AdapterError, match="target parent is not a directory"):
        install_adapter(source_skills, project, "codex")

    assert calls == 0


def test_managed_update_replaces_canonical_bytes_and_removes_obsolete_file(
    source_skills: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    install_adapter(source_skills, project, "generic")
    obsolete = source_skills / "solodeveling/references/protocol.md"
    obsolete.unlink()
    changed = source_skills / "solodeveling/SKILL.md"
    changed.write_text(
        "---\nname: solodeveling\n"
        "description: Updated canonical workflow.\n---\n"
        "Updated bytes.\n",
        encoding="utf-8",
    )

    report = install_adapter(source_skills, project, "generic")

    assert report.ok
    root = project / ".agents/skills"
    assert (root / "solodeveling/SKILL.md").read_bytes() == changed.read_bytes()
    assert not (root / "solodeveling/references/protocol.md").exists()
    assert check_adapter(source_skills, project, "generic").ok


@pytest.mark.parametrize("runtime", sorted(RUNTIME_PATHS))
def test_real_canonical_suite_is_byte_identical_and_conformant(
    runtime: str, tmp_path: Path
) -> None:
    source = Path("skills")
    project = tmp_path / runtime

    install_adapter(source, project, runtime)

    root = project / RUNTIME_PATHS[runtime]
    source_files = {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    }
    installed_files = {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and path.name != adapters.MANIFEST_NAME
    }
    assert installed_files == source_files
    assert check_adapter(source, project, runtime).ok
    assert uninstall_adapter(project, runtime).ok

def test_dangling_target_symlink_is_rejected_in_preflight(
    source_skills: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    simulated_link = project / ".agents"
    original = Path.is_symlink

    def report_simulated_link(path: Path) -> bool:
        return path == simulated_link or original(path)

    monkeypatch.setattr(Path, "is_symlink", report_simulated_link)

    with pytest.raises(AdapterError, match="target symlink is not allowed"):
        install_adapter(source_skills, project, "codex")

    assert not (project / ".agents/skills").exists()
