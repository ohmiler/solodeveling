from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable, Mapping

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


_SOURCE_REVISION = re.compile(r"[0-9a-f]{40}")


def candidate_manifest(
    version: str,
    source_revision: str,
    distributions: Iterable[Path],
    evidence: Iterable[Path],
    *,
    build_inputs: Mapping[str, str] | None = None,
) -> dict[str, object]:
    """Describe immutable candidate subjects without publishing them."""
    if _SOURCE_REVISION.fullmatch(source_revision) is None:
        raise ReleaseError("source revision must be a lowercase 40-character Git SHA")
    distribution_paths = sorted(
        (Path(path) for path in distributions), key=lambda path: path.name
    )
    evidence_paths = sorted(
        (Path(path) for path in evidence), key=lambda path: path.name
    )
    all_paths = distribution_paths + evidence_paths
    missing = [path for path in all_paths if not path.is_file()]
    unsafe = [path for path in all_paths if path.is_symlink()]
    names = [path.name for path in all_paths]
    if missing:
        raise ReleaseError(
            "candidate subjects are missing: "
            + ", ".join(str(path) for path in missing)
        )
    if unsafe:
        raise ReleaseError(
            "candidate subjects contain symlinks: "
            + ", ".join(str(path) for path in unsafe)
        )
    if len(names) != len(set(names)):
        raise ReleaseError("candidate subject filenames must be unique")
    return {
        "solodeveling_candidate_manifest_schema": 1,
        "version": version,
        "source_revision": source_revision,
        "target": (
            "Python input for coordinated GitHub Release, PyPI, and npm release "
            "(not published)"
        ),
        "distributions": [_record(path) for path in distribution_paths],
        "evidence": [_record(path) for path in evidence_paths],
        "build_inputs": dict(sorted((build_inputs or {}).items())),
    }


def _normalized_component_name(value: object) -> str:
    return re.sub(r"[-_.]+", "-", str(value).strip().lower())



def bind_candidate_sbom_identity(path: Path, *, version: str) -> dict[str, object]:
    """Bind Hatch's dynamic version after CycloneDX reads PEP 621 metadata."""
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ReleaseError("candidate SBOM is missing or unsafe")
    try:
        document = json.loads(path.read_text("utf-8"))
        component = document["metadata"]["component"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ReleaseError("candidate SBOM is malformed") from error
    if (
        component.get("type") != "library"
        or _normalized_component_name(component.get("name"))
        != "solodeveling"
    ):
        raise ReleaseError("candidate SBOM root identity is invalid")
    existing = component.get("version")
    if existing is not None and existing != version:
        raise ReleaseError("candidate SBOM version conflicts with the package")
    component["version"] = version
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return document
def validate_candidate_sbom(path: Path, *, version: str) -> dict[str, object]:
    """Apply project identity gates after official CycloneDX schema validation."""
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ReleaseError("candidate SBOM is missing or unsafe")
    try:
        document = json.loads(path.read_text("utf-8"))
        metadata = document["metadata"]
        component = metadata["component"]
        components = document["components"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ReleaseError("candidate SBOM is malformed") from error
    if (
        document.get("bomFormat") != "CycloneDX"
        or document.get("specVersion") != "1.6"
        or component.get("type") != "library"
        or _normalized_component_name(component.get("name"))
        != "solodeveling"
        or component.get("version") != version
        or not isinstance(components, list)
    ):
        raise ReleaseError("candidate SBOM identity does not match the release")
    names = {
        _normalized_component_name(item.get("name"))
        for item in components
        if isinstance(item, dict)
    }
    missing = {"pyyaml", "jsonschema"} - names
    if missing:
        raise ReleaseError(
            "candidate SBOM is missing runtime dependencies: "
            + ", ".join(sorted(missing))
        )
    forbidden = {"pip", "setuptools", "wheel", "build", "cyclonedx-bom"} & names
    if forbidden:
        raise ReleaseError(
            "candidate SBOM contains build tools: "
            + ", ".join(sorted(forbidden))
        )
    return document

def _candidate_records(manifest: Mapping[str, object]) -> list[dict[str, object]]:
    distributions = manifest.get("distributions")
    evidence = manifest.get("evidence")
    if not isinstance(distributions, list) or not isinstance(evidence, list):
        raise ReleaseError("candidate manifest subject lists are malformed")
    if len(distributions) != 2 or len(evidence) != 2:
        raise ReleaseError("candidate manifest must bind two distributions and two evidence files")
    records = distributions + evidence
    if not all(isinstance(item, dict) for item in records):
        raise ReleaseError("candidate manifest records are malformed")
    return records


def finalize_candidate_bundle(
    bundle: Path,
    *,
    source_revision: str,
    sbom_path: Path,
    release_notes_path: Path,
    build_inputs: Mapping[str, str],
) -> dict[str, object]:
    """Add source-bound evidence to a disposable non-publishing release bundle."""
    bundle = Path(bundle).resolve()
    if not bundle.is_dir() or bundle.is_symlink():
        raise ReleaseError("candidate bundle is missing or unsafe")
    candidate_path = bundle / "candidate-manifest.json"
    if candidate_path.exists():
        raise ReleaseError("candidate bundle is already finalized")
    release_manifest_path = bundle / "release-manifest.json"
    try:
        release_manifest = json.loads(release_manifest_path.read_text("utf-8"))
        version = release_manifest["version"]
        release_records = release_manifest["artifacts"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ReleaseError("base release manifest is malformed") from error
    if version != __version__ or not isinstance(release_records, list):
        raise ReleaseError("base release version does not match the package")
    distributions = tuple(
        sorted(
            [*bundle.glob("*.whl"), *bundle.glob("*.tar.gz")],
            key=lambda path: path.name,
        )
    )
    if len(distributions) != 2 or any(path.is_symlink() for path in distributions):
        raise ReleaseError("candidate requires one safe wheel and one safe sdist")
    if [_record(path) for path in distributions] != release_records:
        raise ReleaseError("base release artifacts do not match their manifest")
    validate_candidate_sbom(sbom_path, version=version)
    release_notes_path = Path(release_notes_path)
    if not release_notes_path.is_file() or release_notes_path.is_symlink():
        raise ReleaseError("candidate release notes are missing or unsafe")
    sbom_destination = bundle / f"solodeveling-{version}.cdx.json"
    notes_destination = bundle / "RELEASE-NOTES.md"
    if sbom_destination.exists() or notes_destination.exists():
        raise ReleaseError("candidate evidence destination already exists")
    shutil.copy2(sbom_path, sbom_destination)
    shutil.copy2(release_notes_path, notes_destination)
    manifest = candidate_manifest(
        version,
        source_revision,
        distributions,
        (sbom_destination, notes_destination),
        build_inputs=build_inputs,
    )
    candidate_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    records = _candidate_records(manifest)
    (bundle / "SHA256SUMS").write_text(
        "".join(f"{item['sha256']}  {item['filename']}\n" for item in records),
        encoding="utf-8",
    )
    return manifest


def verify_candidate_bundle(
    bundle: Path, *, source_revision: str
) -> dict[str, object]:
    """Verify candidate identity, complete inventory, hashes, and project SBOM gates."""
    bundle = Path(bundle).resolve()
    if not bundle.is_dir() or bundle.is_symlink():
        raise ReleaseError("candidate bundle is missing or unsafe")
    manifest_path = bundle / "candidate-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as error:
        raise ReleaseError("candidate manifest is malformed") from error
    if manifest.get("solodeveling_candidate_manifest_schema") != 1:
        raise ReleaseError("candidate manifest schema is unsupported")
    if manifest.get("version") != __version__:
        raise ReleaseError("candidate version does not match the package")
    if manifest.get("source_revision") != source_revision:
        raise ReleaseError("candidate source revision does not match")
    if _SOURCE_REVISION.fullmatch(source_revision) is None:
        raise ReleaseError("candidate source revision is invalid")
    records = _candidate_records(manifest)
    names = [str(item.get("filename")) for item in records]
    if len(names) != len(set(names)) or any(Path(name).name != name for name in names):
        raise ReleaseError("candidate manifest filenames are unsafe or duplicated")
    for item, name in zip(records, names):
        path = bundle / name
        if not path.is_file() or path.is_symlink():
            raise ReleaseError(f"candidate subject is missing or unsafe: {name}")
        if _sha256(path) != item.get("sha256"):
            raise ReleaseError(f"candidate hash mismatch: {name}")
        if path.stat().st_size != item.get("size"):
            raise ReleaseError(f"candidate size mismatch: {name}")
    expected_names = set(names) | {
        "candidate-manifest.json",
        "release-manifest.json",
        "SHA256SUMS",
    }
    actual_names = {path.name for path in bundle.iterdir() if path.is_file()}
    if actual_names != expected_names:
        raise ReleaseError("candidate bundle inventory is incomplete or contains extras")
    expected_sums = [
        f"{item['sha256']}  {item['filename']}" for item in records
    ]
    if (bundle / "SHA256SUMS").read_text("utf-8").splitlines() != expected_sums:
        raise ReleaseError("candidate SHA256SUMS does not match the manifest")
    sbom_names = [name for name in names if name.endswith(".cdx.json")]
    if sbom_names != [f"solodeveling-{__version__}.cdx.json"]:
        raise ReleaseError("candidate SBOM filename is missing or ambiguous")
    validate_candidate_sbom(bundle / sbom_names[0], version=__version__)
    return manifest
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
