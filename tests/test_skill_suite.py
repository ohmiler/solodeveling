from __future__ import annotations

import importlib.util
from pathlib import Path


def load_validator() -> object:
    path = Path("scripts/validate_skill_suite.py")
    spec = importlib.util.spec_from_file_location("validate_skill_suite", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_skill_suite_is_structurally_valid() -> None:
    validator = load_validator()

    assert validator.validate_suite(Path(".")) == []  # type: ignore[attr-defined]


def test_validator_reports_a_broken_skill_reference(tmp_path: Path) -> None:
    skill = tmp_path / "skills/example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: example\n"
        "description: Use for a concrete example workflow.\n---\n"
        "Read [missing](references/missing.md).\n" + ("x" * 10001),
        encoding="utf-8",
    )

    validator = load_validator()
    issues = validator.validate_suite(tmp_path)  # type: ignore[attr-defined]

    assert any("broken reference" in issue for issue in issues)
    assert any("exceeds 2500-token budget" in issue for issue in issues)


def test_router_stays_within_token_budget() -> None:
    validator = load_validator()
    text = Path("skills/solodeveling/SKILL.md").read_text("utf-8")

    assert validator.estimate_tokens(text) <= 1200  # type: ignore[attr-defined]


def test_all_core_lifecycle_skills_exist() -> None:
    required = {
        "solodeveling-shaping-work",
        "solodeveling-planning-work",
        "solodeveling-executing-work",
        "solodeveling-debugging",
        "solodeveling-verifying",
    }
    installed = {path.name for path in Path("skills").iterdir() if path.is_dir()}

    assert required <= installed


def test_validator_discovers_every_scenario_file() -> None:
    validator = load_validator()

    discovered = validator.scenario_files(Path("."))  # type: ignore[attr-defined]

    assert {path.name for path in discovered} == {
        "router-onboarding.yaml",
        "lifecycle-workflows.yaml",
        "security.yaml",
        "release-maintenance.yaml",
    }


def test_securing_skill_exists() -> None:
    assert Path("skills/solodeveling-securing/SKILL.md").is_file()


def test_release_and_maintenance_skills_exist() -> None:
    assert Path("skills/solodeveling-releasing/SKILL.md").is_file()
    assert Path("skills/solodeveling-maintaining/SKILL.md").is_file()
