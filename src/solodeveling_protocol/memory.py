from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from string import Template
from tempfile import TemporaryDirectory

import yaml

from solodeveling_protocol.validation import validate_project


class MemoryInitializationError(RuntimeError):
    """Raised when project memory cannot be initialized without data loss."""


@dataclass(frozen=True)
class ProjectFacts:
    name: str
    purpose: str
    users: tuple[str, ...]
    architecture: str
    stack: tuple[str, ...]
    constraints: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("name", "purpose", "architecture"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must not be blank")
        for field_name in ("users", "stack"):
            values = getattr(self, field_name)
            if not values or any(not value.strip() for value in values):
                raise ValueError(f"{field_name} must contain non-blank values")
        for field_name in ("constraints", "sources"):
            if any(not value.strip() for value in getattr(self, field_name)):
                raise ValueError(f"{field_name} must contain non-blank values")


@dataclass(frozen=True)
class InitializationResult:
    memory_root: Path
    created: bool


def _render(template_name: str, metadata: dict[str, object]) -> str:
    template_path = files("solodeveling_protocol").joinpath(
        "templates", template_name
    )
    template = Template(template_path.read_text(encoding="utf-8"))
    frontmatter = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    return template.substitute(frontmatter=frontmatter)


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def initialize_memory(
    root: Path,
    facts: ProjectFacts,
    current_goal: str,
    next_action: str,
) -> InitializationResult:
    """Create validated project memory without changing an existing tree."""
    if not current_goal.strip():
        raise ValueError("current_goal must not be blank")
    if not next_action.strip():
        raise ValueError("next_action must not be blank")

    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    memory_root = root / ".solodeveling"
    if memory_root.exists():
        issues = validate_project(root)
        if issues:
            raise MemoryInitializationError(
                "Existing .solodeveling memory is incomplete; refusing to overwrite it"
            )
        return InitializationResult(memory_root, created=False)

    with TemporaryDirectory(prefix=".solodeveling-init-", dir=root) as temporary:
        staging_root = Path(temporary)
        staged_memory = staging_root / ".solodeveling"
        for relative in ("decisions", "work/active", "work/archive", "evidence"):
            directory = staged_memory / relative
            directory.mkdir(parents=True, exist_ok=True)
            _write(directory / ".gitkeep", "")

        _write(
            staged_memory / "project.md",
            _render(
                "project.md",
                {
                    "solodeveling_schema": 1,
                    "name": facts.name,
                    "purpose": facts.purpose,
                    "users": list(facts.users),
                    "architecture": facts.architecture,
                    "stack": list(facts.stack),
                    "constraints": list(facts.constraints),
                    "sources": list(dict.fromkeys(facts.sources)),
                },
            ),
        )
        _write(
            staged_memory / "state.md",
            _render(
                "state.md",
                {
                    "solodeveling_schema": 1,
                    "current_goal": current_goal,
                    "active_work": [],
                    "blockers": [],
                    "risks": [],
                    "next_action": next_action,
                },
            ),
        )
        for name in ("roadmap", "standards", "risks"):
            _write(
                staged_memory / f"{name}.md",
                _render(f"{name}.md", {"solodeveling_schema": 1}),
            )

        issues = validate_project(staging_root)
        if issues:
            details = "; ".join(f"{issue.code}: {issue.message}" for issue in issues)
            raise MemoryInitializationError(
                f"Staged project memory failed validation: {details}"
            )
        staged_memory.rename(memory_root)

    return InitializationResult(memory_root, created=True)
