from pathlib import Path

import pytest

from solodeveling_protocol.frontmatter import ArtifactReadError, read_artifact


def test_read_artifact_returns_metadata_and_body(tmp_path: Path) -> None:
    path = tmp_path / "work.md"
    path.write_text(
        "---\nsolodeveling_schema: 1\nid: WORK-001\n---\n# Notes\n",
        encoding="utf-8",
    )

    document = read_artifact(path)

    assert document.path == path
    assert document.metadata == {"solodeveling_schema": 1, "id": "WORK-001"}
    assert document.body == "# Notes\n"


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("# Missing frontmatter\n", "must start with YAML frontmatter"),
        ("---\n[invalid\n---\n", "contains invalid YAML"),
        ("---\n- not-a-mapping\n---\n", "frontmatter must be a mapping"),
        ("---\nid: WORK-001\n---\n", "solodeveling_schema must equal 1"),
    ],
)
def test_read_artifact_rejects_invalid_documents(
    tmp_path: Path, content: str, message: str
) -> None:
    path = tmp_path / "invalid.md"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ArtifactReadError, match=message):
        read_artifact(path)
