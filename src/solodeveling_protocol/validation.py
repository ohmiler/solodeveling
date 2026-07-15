from __future__ import annotations

import json
from importlib.resources import files

from jsonschema import Draft202012Validator

from solodeveling_protocol.models import ArtifactDocument, ValidationIssue


SCHEMA_FILES = {
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
