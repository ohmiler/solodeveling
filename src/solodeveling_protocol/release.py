from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable

from solodeveling_protocol import __version__


class ReleaseError(RuntimeError):
    """Raised when a release bundle cannot be built safely."""


Runner = Callable[[tuple[str, ...], Path], subprocess.CompletedProcess[str]]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _record(path: Path) -> dict[str, object]:
    return {
        "filename": path.name,
        "sha256": _sha256(path),
        "size": path.stat().st_size,
    }


def artifact_manifest(
    version: str,
    artifacts: Iterable[Path],
    *,
    canonical_resources: Iterable[Path] = (),
    resource_root: Path | None = None,
) -> dict[str, object]:
    artifact_paths = sorted((Path(path) for path in artifacts), key=lambda p: p.name)
    root = Path(resource_root) if resource_root is not None else None
    resources = []
    for path in sorted((Path(path) for path in canonical_resources), key=str):
        record = _record(path)
        record["filename"] = (
            path.relative_to(root).as_posix() if root is not None else path.name
        )
        resources.append(record)
    return {
        "solodeveling_release_manifest_schema": 1,
        "version": version,
        "artifacts": [_record(path) for path in artifact_paths],
        "canonical_resources": resources,
    }


def _default_runner(
    argv: tuple[str, ...], cwd: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        shell=False,
    )


def canonical_files(project_root: Path) -> tuple[Path, ...]:
    roots = (
        project_root / "skills",
        project_root / "evals" / "scenarios",
    )
    invalid_roots = [
        root for root in roots if not root.is_dir() or root.is_symlink()
    ]
    if invalid_roots:
        raise ReleaseError(
            "canonical release roots are missing or unsafe: "
            + ", ".join(str(path) for path in invalid_roots)
        )
    files_found = [
        path
        for root in roots
        for path in root.rglob("*")
        if path.is_file()
    ]
    files_found.extend(
        [
            project_root / "evals" / "evaluation-response.schema.json",
            project_root / "evals" / "evaluation-result.schema.json",
        ]
    )
    missing = [path for path in files_found if not path.is_file()]
    symlinks = [path for path in files_found if path.is_symlink()]
    if missing:
        raise ReleaseError(
            "canonical release resources are missing: "
            + ", ".join(str(path) for path in missing)
        )
    if symlinks:
        raise ReleaseError(
            "canonical release resources contain symlinks: "
            + ", ".join(str(path) for path in symlinks)
        )
    return tuple(sorted(set(files_found), key=str))


def build_release_bundle(
    project_root: Path,
    output_directory: Path,
    *,
    runner: Runner = _default_runner,
) -> dict[str, object]:
    project_root = Path(project_root).resolve()
    output_directory = Path(output_directory).resolve()
    if output_directory.exists():
        raise ReleaseError(
            f"release output already exists: {output_directory}"
        )
    if not (project_root / "pyproject.toml").is_file():
        raise ReleaseError(f"project root is invalid: {project_root}")

    output_directory.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="solodeveling-build-"
    ) as build_temporary, tempfile.TemporaryDirectory(
        prefix=".solodeveling-release-",
        dir=output_directory.parent,
    ) as staging_temporary:
        build_output = Path(build_temporary) / "dist"
        command = (
            sys.executable,
            "-m",
            "build",
            "--outdir",
            str(build_output),
            str(project_root),
        )
        process = runner(command, project_root)
        if process.returncode != 0:
            raise ReleaseError(
                f"distribution build failed with exit code {process.returncode}"
            )
        artifacts = tuple(sorted(build_output.glob("*"), key=lambda path: path.name))
        wheels = [path for path in artifacts if path.suffix == ".whl"]
        sdists = [path for path in artifacts if path.name.endswith(".tar.gz")]
        if len(wheels) != 1 or len(sdists) != 1 or len(artifacts) != 2:
            raise ReleaseError("build must produce exactly one wheel and one sdist")

        stage = Path(staging_temporary) / "bundle"
        stage.mkdir()
        copied = []
        for artifact in artifacts:
            destination = stage / artifact.name
            shutil.copy2(artifact, destination)
            copied.append(destination)
        canonical = canonical_files(project_root)
        manifest = artifact_manifest(
            __version__,
            copied,
            canonical_resources=canonical,
            resource_root=project_root,
        )
        (stage / "release-manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        checksum_lines = [
            f"{item['sha256']}  {item['filename']}"
            for item in manifest["artifacts"]
        ]
        (stage / "SHA256SUMS").write_text(
            "\n".join(checksum_lines) + "\n",
            encoding="utf-8",
        )
        stage.replace(output_directory)
    return manifest
