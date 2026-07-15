from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator

from solodeveling_protocol.frontmatter import ArtifactReadError, read_artifact
from solodeveling_protocol.models import ArtifactDocument, ValidationIssue
from solodeveling_protocol.secrets import detect_secret_kinds


SCHEMA_FILES = {
    "project": "project.schema.json",
    "security-finding": "security-finding.schema.json",
    "work-item": "work-item.schema.json",
    "state": "state.schema.json",
    "evidence": "evidence.schema.json",
}


def _load_schema(kind: str) -> dict:
    resource = files("solodeveling_protocol").joinpath("schemas", SCHEMA_FILES[kind])
    return json.loads(resource.read_text(encoding="utf-8"))


def validate_document(
    document: ArtifactDocument, kind: str
) -> list[ValidationIssue]:
    if kind not in SCHEMA_FILES:
        return [
            ValidationIssue(
                path=document.path,
                code="unknown-kind",
                message=f"Unknown artifact kind: {kind}",
            )
        ]

    validator = Draft202012Validator(_load_schema(kind))
    errors = sorted(
        validator.iter_errors(document.metadata), key=lambda error: list(error.path)
    )
    return [
        ValidationIssue(
            path=document.path,
            code="schema",
            message=f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}",
        )
        for error in errors
    ]


def _artifact_kind(path: Path) -> str | None:
    normalized = path.as_posix()
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    if normalized.endswith("/.solodeveling/project.md"):
        return "project"
    if normalized.endswith("/.solodeveling/state.md"):
        return "state"
    if "/.solodeveling/work/" in normalized:
        return "work-item"
    if "/.solodeveling/evidence/" in normalized:
        return "evidence"
    if "/.solodeveling/security/findings/" in normalized:
        return "security-finding"
    return None


def validate_project(root: Path) -> list[ValidationIssue]:
    memory_root = root / ".solodeveling"
    if not memory_root.is_dir():
        return [
            ValidationIssue(
                memory_root,
                "missing-memory",
                ".solodeveling directory is missing",
            )
        ]

    issues: list[ValidationIssue] = []
    required_paths = {
        "missing-project": memory_root / "project.md",
        "missing-state": memory_root / "state.md",
        "missing-active-work": memory_root / "work" / "active",
        "missing-work-archive": memory_root / "work" / "archive",
        "missing-evidence-directory": memory_root / "evidence",
    }
    for code, path in required_paths.items():
        exists = path.is_file() if path.suffix else path.is_dir()
        if not exists:
            issues.append(
                ValidationIssue(
                    path,
                    code,
                    f"Required project-memory path is missing: {path.name}",
                )
            )

    work_items: dict[str, ArtifactDocument] = {}
    evidence_ids: set[str] = set()

    for path in sorted(memory_root.rglob("*.md")):
        try:
            raw_text = path.read_text(encoding="utf-8")
        except OSError as error:
            issues.append(ValidationIssue(path, "read-error", str(error)))
            continue
        for secret_kind in detect_secret_kinds(raw_text):
            issues.append(
                ValidationIssue(
                    path,
                    "secret-like-material",
                    f"High-confidence {secret_kind} pattern detected; value omitted",
                )
            )

        kind = _artifact_kind(path)
        if kind is None:
            continue
        try:
            document = read_artifact(path)
        except (ArtifactReadError, OSError) as error:
            issues.append(ValidationIssue(path, "read-error", str(error)))
            continue

        issues.extend(validate_document(document, kind))
        if kind == "work-item" and isinstance(document.metadata.get("id"), str):
            work_items[document.metadata["id"]] = document
        if kind == "evidence" and isinstance(document.metadata.get("id"), str):
            evidence_ids.add(document.metadata["id"])

    for document in work_items.values():
        metadata = document.metadata
        references = set(metadata.get("evidence", []))
        for evidence_id in sorted(references - evidence_ids):
            issues.append(
                ValidationIssue(
                    document.path,
                    "missing-evidence",
                    f"Referenced evidence does not exist: {evidence_id}",
                )
            )
        if metadata.get("status") == "done":
            gaps = metadata.get("accepted_verification_gaps", [])
            if not references and not gaps:
                issues.append(
                    ValidationIssue(
                        document.path,
                        "done-without-evidence",
                        "Done work requires evidence or an accepted verification gap",
                    )
                )
            if metadata.get("level") == "critical" and (
                not metadata.get("security_considerations")
                or not metadata.get("recovery")
            ):
                issues.append(
                    ValidationIssue(
                        document.path,
                        "critical-completion-gap",
                        "Critical done work requires security and recovery consideration",
                    )
                )

    return issues