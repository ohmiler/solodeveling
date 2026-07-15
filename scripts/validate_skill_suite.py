from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Sequence

import yaml


REFERENCE_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)")
FORBIDDEN_REQUIREMENTS = (
    "subagents are required",
    "must use subagent",
    "must spawn subagent",
    "requires a subagent",
)


def estimate_tokens(text: str) -> int:
    """Return a conservative language-independent approximation."""
    return math.ceil(len(text.encode("utf-8")) / 4)


def _frontmatter(path: Path, text: str) -> tuple[dict[str, object], str, list[str]]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}, text, [f"{path}: missing YAML frontmatter"]
    try:
        boundary = lines.index("---", 1)
    except ValueError:
        return {}, text, [f"{path}: unterminated YAML frontmatter"]
    try:
        metadata = yaml.safe_load("\n".join(lines[1:boundary]))
    except yaml.YAMLError as error:
        return {}, text, [f"{path}: invalid YAML frontmatter: {error}"]
    if not isinstance(metadata, dict):
        return {}, text, [f"{path}: frontmatter must be a mapping"]
    return metadata, "\n".join(lines[boundary + 1 :]), []


def _validate_skill(skill: Path) -> tuple[list[str], str]:
    issues: list[str] = []
    skill_file = skill / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill}: missing SKILL.md"], ""
    text = skill_file.read_text(encoding="utf-8-sig")
    metadata, body, metadata_issues = _frontmatter(skill_file, text)
    issues.extend(metadata_issues)
    name = metadata.get("name")
    description = metadata.get("description")
    if set(metadata) != {"name", "description"}:
        issues.append(f"{skill_file}: frontmatter must contain only name and description")
    if name != skill.name:
        issues.append(f"{skill_file}: name must match folder {skill.name}")
    if not isinstance(description, str) or not description.strip():
        issues.append(f"{skill_file}: description must be non-empty")
    if "TODO" in text or "[TODO" in text:
        issues.append(f"{skill_file}: unresolved placeholder")

    lowered = text.lower()
    for phrase in FORBIDDEN_REQUIREMENTS:
        if phrase in lowered:
            issues.append(f"{skill_file}: forbidden subagent requirement: {phrase}")

    for target in REFERENCE_PATTERN.findall(body):
        referenced = skill / target
        if not referenced.is_file():
            issues.append(f"{skill_file}: broken reference: {target}")

    metadata_file = skill / "agents" / "openai.yaml"
    if metadata_file.is_file() and isinstance(name, str):
        try:
            interface = yaml.safe_load(metadata_file.read_text("utf-8"))["interface"]
            default_prompt = interface["default_prompt"]
        except (KeyError, TypeError, yaml.YAMLError) as error:
            issues.append(f"{metadata_file}: invalid interface metadata: {error}")
        else:
            if f"${name}" not in default_prompt:
                issues.append(f"{metadata_file}: default_prompt must mention ${name}")

    if skill.name == "solodeveling" and estimate_tokens(text) > 1200:
        issues.append(
            f"{skill_file}: router exceeds 1200-token budget "
            f"({estimate_tokens(text)} estimated)"
        )
    return issues, body


def _scenario_issues(root: Path, skills: dict[str, str]) -> list[str]:
    scenario_path = root / "tests" / "scenarios" / "router-onboarding.yaml"
    if not scenario_path.is_file():
        return []
    document = yaml.safe_load(scenario_path.read_text("utf-8"))
    scenarios = document.get("scenarios", []) if isinstance(document, dict) else []
    issues: list[str] = []
    if not isinstance(scenarios, list):
        return [f"{scenario_path}: scenarios must be a list"]
    identifiers: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            issues.append(f"{scenario_path}: scenario must be a mapping")
            continue
        identifier = scenario.get("id")
        skill_name = scenario.get("skill")
        if not isinstance(identifier, str) or identifier in identifiers:
            issues.append(f"{scenario_path}: scenario IDs must be unique strings")
            continue
        identifiers.add(identifier)
        if skill_name not in skills:
            issues.append(f"{identifier}: unknown skill {skill_name}")
            continue
        haystack = skills[skill_name].lower()
        for phrase in scenario.get("must_contain", []):
            if str(phrase).lower() not in haystack:
                issues.append(f"{identifier}: missing protocol phrase: {phrase}")
        for phrase in scenario.get("must_not_contain", []):
            if str(phrase).lower() in haystack:
                issues.append(f"{identifier}: forbidden protocol phrase: {phrase}")
    return issues


def _duplicate_paragraph_issues(bodies: dict[str, str]) -> list[str]:
    owners: dict[str, list[str]] = defaultdict(list)
    for name, body in bodies.items():
        for paragraph in re.split(r"\n\s*\n", body):
            normalized = " ".join(paragraph.split())
            if len(normalized) >= 160:
                owners[normalized].append(name)
    return [
        f"duplicate long paragraph across skills: {', '.join(names)}"
        for names in owners.values()
        if len(set(names)) > 1
    ]


def validate_suite(root: Path) -> list[str]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return [f"{skills_root}: skills directory is missing"]
    issues: list[str] = []
    bodies: dict[str, str] = {}
    combined: dict[str, str] = {}
    for skill in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_issues, body = _validate_skill(skill)
        issues.extend(skill_issues)
        bodies[skill.name] = body
        references = "\n".join(
            path.read_text("utf-8")
            for path in sorted((skill / "references").glob("*.md"))
        )
        combined[skill.name] = f"{body}\n{references}"
    issues.extend(_duplicate_paragraph_issues(bodies))
    issues.extend(_scenario_issues(root, combined))
    return issues


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Solodeveling skill suite")
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    arguments = parser.parse_args(argv)
    issues = validate_suite(arguments.root.resolve())
    if issues:
        for issue in issues:
            print(issue)
        return 1
    print("Solodeveling skill suite is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
