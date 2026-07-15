from __future__ import annotations

import json
from pathlib import Path

from solodeveling_protocol.adapter_cli import main as adapter_main
from solodeveling_protocol.evaluation_cli import main as evaluation_main
from solodeveling_protocol.resources import resource_path


def _relative_hashes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_default_resource_paths_match_repository_canonical_bytes() -> None:
    with resource_path("skills") as packaged_skills:
        assert _relative_hashes(packaged_skills) == _relative_hashes(Path("skills"))
    with resource_path("evals/scenarios") as scenarios:
        assert (scenarios / "core.yaml").read_bytes() == Path(
            "evals/scenarios/core.yaml"
        ).read_bytes()
    with resource_path("evals/evaluation-response.schema.json") as schema:
        assert schema.read_bytes() == Path(
            "evals/evaluation-response.schema.json"
        ).read_bytes()


def test_adapter_cli_uses_canonical_resource_without_source_flag(
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()

    installed = adapter_main(
        ["install", "--runtime", "codex", "--project-root", str(project)]
    )
    checked = adapter_main(
        ["check", "--runtime", "codex", "--project-root", str(project)]
    )
    removed = adapter_main(
        ["uninstall", "--runtime", "codex", "--project-root", str(project)]
    )

    assert (installed, checked, removed) == (0, 0, 0)
    assert not (project / ".agents" / "skills" / "solodeveling").exists()


def test_evaluation_dry_run_uses_packaged_defaults_outside_checkout(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.chdir(tmp_path)

    result = evaluation_main(
        [
            "run",
            "--runtime",
            "codex",
            "--smoke",
            "--scenario",
            "quick-local-documentation",
            "--dry-run",
        ]
    )

    document = json.loads(capsys.readouterr().out)
    assert result == 0
    assert document["plan"][0]["scenario_id"] == "quick-local-documentation"
