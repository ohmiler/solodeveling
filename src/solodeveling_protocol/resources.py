from __future__ import annotations

import shutil
import tempfile
from contextlib import contextmanager
from importlib.resources import as_file, files
from pathlib import Path, PurePosixPath
from typing import Iterator


_RESOURCE_PATHS = {
    "skills": "skills",
    "evals/scenarios": "evals/scenarios",
    "evals/evaluation-response.schema.json": (
        "evals/evaluation-response.schema.json"
    ),
    "evals/evaluation-result.schema.json": (
        "evals/evaluation-result.schema.json"
    ),
}


def _copy_traversable(source, destination: Path) -> None:
    if source.is_dir():
        destination.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            _copy_traversable(child, destination / child.name)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as input_stream, destination.open("wb") as output_stream:
        shutil.copyfileobj(input_stream, output_stream)


def _packaged_resource(relative: str):
    resource = files("solodeveling_protocol").joinpath("resources")
    for part in PurePosixPath(relative).parts:
        resource = resource.joinpath(part)
    return resource


@contextmanager
def resource_path(
    relative: str,
    override: Path | None = None,
) -> Iterator[Path]:
    """Yield a stable path for a known canonical package resource."""
    if relative not in _RESOURCE_PATHS:
        raise ValueError(f"unknown Solodeveling resource: {relative}")
    if override is not None:
        yield Path(override)
        return

    packaged = _packaged_resource(_RESOURCE_PATHS[relative])
    if packaged.is_file():
        with as_file(packaged) as path:
            yield Path(path)
        return
    if packaged.is_dir():
        if isinstance(packaged, Path):
            yield packaged
            return
        with tempfile.TemporaryDirectory(
            prefix="solodeveling-resource-"
        ) as temporary:
            target = Path(temporary) / PurePosixPath(relative).name
            _copy_traversable(packaged, target)
            yield target
        return

    development = Path(__file__).resolve().parents[2] / _RESOURCE_PATHS[relative]
    if not development.exists():
        raise FileNotFoundError(
            f"packaged Solodeveling resource is unavailable: {relative}"
        )
    yield development
