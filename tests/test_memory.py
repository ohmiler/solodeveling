from pathlib import Path

import pytest

from solodeveling_protocol.memory import (
    MemoryInitializationError,
    ProjectFacts,
    initialize_memory,
)
from solodeveling_protocol.validation import validate_project


def facts() -> ProjectFacts:
    return ProjectFacts(
        name="Example",
        purpose="Demonstrate non-destructive project onboarding.",
        users=("Solo developers",),
        architecture="A small portable fixture.",
        stack=("Python",),
        constraints=("Preserve existing documentation.",),
        sources=("README.md", "AGENTS.md"),
    )


def test_initialize_memory_creates_a_valid_minimum_tree(tmp_path: Path) -> None:
    result = initialize_memory(
        tmp_path,
        facts(),
        current_goal="Ship a safe first increment.",
        next_action="Shape WORK-001.",
    )

    assert result.created is True
    assert validate_project(tmp_path) == []
    assert (tmp_path / ".solodeveling/roadmap.md").is_file()
    assert (tmp_path / ".solodeveling/standards.md").is_file()
    assert (tmp_path / ".solodeveling/risks.md").is_file()
    project_text = (tmp_path / ".solodeveling/project.md").read_text("utf-8")
    assert "README.md" in project_text
    assert "AGENTS.md" in project_text


def test_initialize_memory_is_idempotent_for_a_valid_tree(tmp_path: Path) -> None:
    first = initialize_memory(tmp_path, facts(), "Goal", "Next")
    before = (first.memory_root / "project.md").read_bytes()

    second = initialize_memory(tmp_path, facts(), "Different goal", "Different next")

    assert second.created is False
    assert (second.memory_root / "project.md").read_bytes() == before


def test_initialize_memory_refuses_to_overwrite_partial_memory(tmp_path: Path) -> None:
    memory_root = tmp_path / ".solodeveling"
    memory_root.mkdir()
    existing = memory_root / "project.md"
    existing.write_text("human-owned content", encoding="utf-8")

    with pytest.raises(MemoryInitializationError, match="refusing to overwrite"):
        initialize_memory(tmp_path, facts(), "Goal", "Next")

    assert existing.read_text("utf-8") == "human-owned content"


@pytest.mark.parametrize("field", ["name", "purpose", "architecture"])
def test_project_facts_reject_blank_required_text(field: str) -> None:
    values = facts().__dict__ | {field: "  "}

    with pytest.raises(ValueError, match=field):
        ProjectFacts(**values)
