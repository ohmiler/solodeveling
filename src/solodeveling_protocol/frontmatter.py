from __future__ import annotations

from pathlib import Path

import yaml

from solodeveling_protocol import SCHEMA_VERSION
from solodeveling_protocol.models import ArtifactDocument


class ArtifactReadError(ValueError):
    """Raised when a protocol artifact cannot be read safely."""


def read_artifact(path: Path) -> ArtifactDocument:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ArtifactReadError(f"{path} must start with YAML frontmatter")

    closing = text.find("\n---\n", 4)
    if closing == -1:
        raise ArtifactReadError(f"{path} must close YAML frontmatter with ---")

    raw_metadata = text[4:closing]
    body = text[closing + 5 :]
    try:
        metadata = yaml.safe_load(raw_metadata)
    except yaml.YAMLError as error:
        raise ArtifactReadError(f"{path} contains invalid YAML: {error}") from error

    if not isinstance(metadata, dict):
        raise ArtifactReadError(f"{path} frontmatter must be a mapping")
    if metadata.get("solodeveling_schema") != SCHEMA_VERSION:
        raise ArtifactReadError(
            f"{path} solodeveling_schema must equal {SCHEMA_VERSION}"
        )

    return ArtifactDocument(path=path, metadata=metadata, body=body)
