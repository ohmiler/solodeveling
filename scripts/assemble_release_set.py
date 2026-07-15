from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Mapping

try:
    from scripts.build_native import native_target
except ModuleNotFoundError as error:
    if error.name != "scripts":
        raise
    from build_native import native_target
from solodeveling_protocol import __version__
from solodeveling_protocol.release import (
    ReleaseError,
    validate_candidate_sbom,
    verify_candidate_bundle,
)


class ReleaseSetError(RuntimeError):
    pass


_SOURCE_REVISION = re.compile(r"[0-9a-f]{40}")
_TARGETS = (
    ("win32", "AMD64"),
    ("win32", "ARM64"),
    ("darwin", "x86_64"),
    ("darwin", "arm64"),
    ("linux", "x86_64"),
    ("linux", "aarch64"),
)
_MAX_NPM_MEMBERS = 100
_MAX_NPM_MEMBER_SIZE = 5 * 1024 * 1024
_MAX_NPM_TOTAL_SIZE = 20 * 1024 * 1024


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _record(path: Path, role: str, *, platform: str | None = None) -> dict[str, object]:
    record: dict[str, object] = {
        "filename": path.name,
        "role": role,
        "sha256": _sha256(path),
        "size": path.stat().st_size,
    }
    if platform is not None:
        record["platform"] = platform
    return record


def _safe_flat_name(value: object) -> str:
    if (
        not isinstance(value, str)
        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,254}", value) is None
        or Path(value).name != value
        or "/" in value
        or "\\" in value
        or value in {".", ".."}
    ):
        raise ReleaseSetError("release-set artifact filename is unsafe")
    return value


def _expected_native() -> dict[str, str]:
    return {
        key: filename
        for system, machine in _TARGETS
        for key, filename in (native_target(system, machine),)
    }


def _native_records(native_root: Path) -> dict[str, dict[str, object]]:
    native_input = Path(native_root)
    if native_input.is_symlink():
        raise ReleaseSetError("native artifact root is missing or unsafe")
    native_root = native_input.resolve()
    if not native_root.is_dir():
        raise ReleaseSetError("native artifact root is missing or unsafe")
    expected = _expected_native()
    entries = list(native_root.iterdir())
    actual_names = {path.name for path in entries}
    if len(entries) != len(actual_names) or actual_names != set(expected.values()):
        raise ReleaseSetError("native artifact inventory is incomplete or contains extras")
    records: dict[str, dict[str, object]] = {}
    for platform, filename in expected.items():
        path = native_root / filename
        if not path.is_file() or path.is_symlink() or path.stat().st_size <= 0:
            raise ReleaseSetError(f"native artifact is missing or unsafe: {filename}")
        records[platform] = {
            "filename": filename,
            "sha256": _sha256(path),
            "size": path.stat().st_size,
        }
    return records


def _read_tar_json(archive: tarfile.TarFile, member: tarfile.TarInfo) -> object:
    stream = archive.extractfile(member)
    if stream is None:
        raise ReleaseSetError(f"npm archive member is unreadable: {member.name}")
    try:
        return json.loads(stream.read().decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ReleaseSetError(f"npm archive JSON is malformed: {member.name}") from error


def _inspect_npm_package(
    npm_package: Path,
    native_records: Mapping[str, Mapping[str, object]],
) -> None:
    npm_input = Path(npm_package)
    if npm_input.is_symlink():
        raise ReleaseSetError(
            "npm package is missing, empty, unsafe, or version-drifted"
        )
    npm_package = npm_input.resolve()
    expected_name = f"solodeveling-{__version__}.tgz"
    if (
        not npm_package.is_file()
        or npm_package.is_symlink()
        or npm_package.name != expected_name
        or npm_package.stat().st_size <= 0
    ):
        raise ReleaseSetError("npm package is missing, empty, unsafe, or version-drifted")
    try:
        with tarfile.open(npm_package, "r:gz") as archive:
            members = archive.getmembers()
            if not members or len(members) > _MAX_NPM_MEMBERS:
                raise ReleaseSetError("npm archive member inventory is unsafe")
            names = [member.name for member in members]
            if len(names) != len(set(names)):
                raise ReleaseSetError("npm archive contains duplicate member names")
            total_size = 0
            by_name: dict[str, tarfile.TarInfo] = {}
            for member in members:
                name = member.name
                path = PurePosixPath(name)
                if (
                    "\\" in name
                    or path.is_absolute()
                    or ".." in path.parts
                    or not path.parts
                    or path.parts[0] != "package"
                ):
                    raise ReleaseSetError("npm archive member path is unsafe")
                if member.issym() or member.islnk():
                    raise ReleaseSetError("npm archive contains a link")
                if not (member.isfile() or member.isdir()):
                    raise ReleaseSetError("npm archive contains a special file")
                if member.size < 0 or member.size > _MAX_NPM_MEMBER_SIZE:
                    raise ReleaseSetError("npm archive member size is unsafe")
                total_size += member.size
                by_name[name] = member
            if total_size > _MAX_NPM_TOTAL_SIZE:
                raise ReleaseSetError("npm archive expanded size is unsafe")
            try:
                metadata_member = by_name["package/package.json"]
                manifest_member = by_name["package/artifacts.json"]
            except KeyError as error:
                raise ReleaseSetError("npm archive metadata is incomplete") from error
            if not metadata_member.isfile() or not manifest_member.isfile():
                raise ReleaseSetError("npm archive metadata is not a regular file")
            metadata = _read_tar_json(archive, metadata_member)
            manifest = _read_tar_json(archive, manifest_member)
    except (tarfile.TarError, OSError) as error:
        raise ReleaseSetError("npm package is not a readable gzip tar archive") from error
    if not isinstance(metadata, dict) or (
        metadata.get("name") != "solodeveling"
        or metadata.get("version") != __version__
    ):
        raise ReleaseSetError("npm package identity does not match the release")
    if not isinstance(manifest, dict) or (
        manifest.get("schema") != 1
        or manifest.get("version") != __version__
        or manifest.get("artifacts") != dict(native_records)
    ):
        raise ReleaseSetError("npm native manifest does not match native artifact bytes")


def _candidate_artifacts(
    candidate_root: Path, source_revision: str
) -> list[tuple[Path, str, dict[str, object]]]:
    candidate_input = Path(candidate_root)
    if candidate_input.is_symlink():
        raise ReleaseSetError("Python candidate root is missing or unsafe")
    candidate_root = candidate_input.resolve()
    try:
        manifest = verify_candidate_bundle(
            candidate_root, source_revision=source_revision
        )
    except ReleaseError as error:
        raise ReleaseSetError(f"Python candidate verification failed: {error}") from error
    if manifest.get("version") != __version__:
        raise ReleaseSetError("Python candidate version does not match the release")
    result: list[tuple[Path, str, dict[str, object]]] = []
    distributions = manifest.get("distributions")
    evidence = manifest.get("evidence")
    if not isinstance(distributions, list) or not isinstance(evidence, list):
        raise ReleaseSetError("Python candidate inventory is malformed")
    for item in distributions:
        if not isinstance(item, dict):
            raise ReleaseSetError("Python candidate inventory is malformed")
        name = _safe_flat_name(item.get("filename"))
        result.append((candidate_root / name, "python-distribution", item))
    for item in evidence:
        if not isinstance(item, dict):
            raise ReleaseSetError("Python candidate inventory is malformed")
        name = _safe_flat_name(item.get("filename"))
        role = "sbom" if name.endswith(".cdx.json") else "release-notes"
        result.append((candidate_root / name, role, item))
    return result


def _validate_revision(source_revision: str) -> None:
    if _SOURCE_REVISION.fullmatch(source_revision) is None:
        raise ReleaseSetError("source revision must be a lowercase 40-character Git SHA")


def assemble_release_set(
    candidate_root: Path,
    native_root: Path,
    npm_package: Path,
    output: Path,
    *,
    source_revision: str,
) -> dict[str, object]:
    _validate_revision(source_revision)
    candidate_root = Path(candidate_root)
    native_root = Path(native_root)
    npm_package = Path(npm_package)
    output_input = Path(output)
    if output_input.exists() or output_input.is_symlink():
        raise ReleaseSetError(f"release-set output already exists: {output_input}")
    output = output_input.resolve()
    candidate_artifacts = _candidate_artifacts(candidate_root, source_revision)
    native_records = _native_records(native_root)
    _inspect_npm_package(npm_package, native_records)
    sources: list[tuple[Path, str, str | None, Mapping[str, object]]] = [
        (path, role, None, expected) for path, role, expected in candidate_artifacts
    ]
    for platform, record in native_records.items():
        sources.append((native_root / str(record["filename"]), "native-executable", platform, record))
    sources.append((npm_package, "npm-package", None, _record(npm_package, "npm-package")))
    names = [path.name for path, _, _, _ in sources]
    if len(names) != len(set(names)):
        raise ReleaseSetError("release-set artifact filenames are duplicated")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".solodeveling-release-set-", dir=output.parent) as temporary:
        stage = Path(temporary) / "release-set"
        stage.mkdir()
        records = []
        for source, role, platform, expected in sources:
            if not source.is_file() or source.is_symlink():
                raise ReleaseSetError(f"release-set input is missing or unsafe: {source.name}")
            destination = stage / source.name
            shutil.copyfile(source, destination)
            copied = _record(destination, role, platform=platform)
            if copied["sha256"] != expected.get("sha256") or copied["size"] != expected.get("size"):
                raise ReleaseSetError(f"release-set input changed during assembly: {source.name}")
            records.append(copied)
        records.sort(key=lambda item: str(item["filename"]))
        manifest: dict[str, object] = {"solodeveling_release_set_schema": 1, "version": __version__, "source_revision": source_revision, "target": "coordinated release input (not published)", "artifacts": records}
        (stage / "release-set-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (stage / "SHA256SUMS").write_text("".join(f"{record['sha256']}  {record['filename']}\n" for record in records), encoding="utf-8")
        verify_release_set(stage, source_revision=source_revision)
        stage.replace(output)
    return manifest


def _records(manifest: Mapping[str, object]) -> list[dict[str, object]]:
    value = manifest.get("artifacts")
    if not isinstance(value, list) or len(value) != 11 or not all(
        isinstance(item, dict) for item in value
    ):
        raise ReleaseSetError("release-set artifact inventory is malformed")
    return value


def verify_release_set(output: Path, *, source_revision: str) -> dict[str, object]:
    _validate_revision(source_revision)
    output_input = Path(output)
    if output_input.is_symlink():
        raise ReleaseSetError("release-set directory is missing or unsafe")
    output = output_input.resolve()
    if not output.is_dir():
        raise ReleaseSetError("release-set directory is missing or unsafe")
    manifest_path = output / "release-set-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReleaseSetError("release-set manifest is malformed") from error
    if not isinstance(manifest, dict) or manifest.get("solodeveling_release_set_schema") != 1:
        raise ReleaseSetError("release-set manifest schema is unsupported")
    if manifest.get("version") != __version__:
        raise ReleaseSetError("release-set version does not match the package")
    if manifest.get("source_revision") != source_revision:
        raise ReleaseSetError("release-set source revision does not match")
    if manifest.get("target") != "coordinated release input (not published)":
        raise ReleaseSetError("release-set target is invalid")

    records = _records(manifest)
    names = [_safe_flat_name(item.get("filename")) for item in records]
    if names != sorted(names) or len(names) != len(set(names)):
        raise ReleaseSetError("release-set artifact filenames are unsorted or duplicated")
    actual_names = {path.name for path in output.iterdir()}
    expected_names = set(names) | {"release-set-manifest.json", "SHA256SUMS"}
    if actual_names != expected_names:
        raise ReleaseSetError("release-set inventory is incomplete or contains extras")

    roles = [item.get("role") for item in records]
    if {
        "python-distribution": roles.count("python-distribution"),
        "native-executable": roles.count("native-executable"),
        "npm-package": roles.count("npm-package"),
        "sbom": roles.count("sbom"),
        "release-notes": roles.count("release-notes"),
    } != {
        "python-distribution": 2,
        "native-executable": 6,
        "npm-package": 1,
        "sbom": 1,
        "release-notes": 1,
    }:
        raise ReleaseSetError("release-set artifact roles are incomplete")

    python_names = {
        name
        for item, name in zip(records, names)
        if item.get("role") == "python-distribution"
    }
    wheel_names = {
        name
        for name in python_names
        if name.startswith(f"solodeveling-{__version__}-") and name.endswith(".whl")
    }
    if (
        python_names != wheel_names | {f"solodeveling-{__version__}.tar.gz"}
        or len(wheel_names) != 1
    ):
        raise ReleaseSetError("release-set Python distribution identity is invalid")
    expected_role_names = {
        "npm-package": f"solodeveling-{__version__}.tgz",
        "sbom": f"solodeveling-{__version__}.cdx.json",
        "release-notes": "RELEASE-NOTES.md",
    }
    for role, expected_name in expected_role_names.items():
        role_names = [
            name for item, name in zip(records, names) if item.get("role") == role
        ]
        if role_names != [expected_name]:
            raise ReleaseSetError(f"release-set {role} identity is invalid")

    expected_sums = []
    native_records: dict[str, dict[str, object]] = {}
    for item, name in zip(records, names):
        path = output / name
        if not path.is_file() or path.is_symlink():
            raise ReleaseSetError(f"release-set artifact is missing or unsafe: {name}")
        if path.stat().st_size != item.get("size"):
            raise ReleaseSetError(f"release-set size mismatch: {name}")
        actual_hash = _sha256(path)
        if actual_hash != item.get("sha256"):
            raise ReleaseSetError(f"release-set hash mismatch: {name}")
        expected_sums.append(f"{actual_hash}  {name}")
        if item.get("role") == "native-executable":
            platform = item.get("platform")
            if not isinstance(platform, str) or platform in native_records:
                raise ReleaseSetError("release-set native platform is invalid or duplicated")
            native_records[platform] = {
                "filename": name,
                "sha256": actual_hash,
                "size": path.stat().st_size,
            }
        elif "platform" in item:
            raise ReleaseSetError("release-set platform is only valid for native artifacts")
    if native_records.keys() != _expected_native().keys() or {
        key: value["filename"] for key, value in native_records.items()
    } != _expected_native():
        raise ReleaseSetError("release-set native artifact inventory is invalid")
    if (output / "SHA256SUMS").read_text("utf-8").splitlines() != expected_sums:
        raise ReleaseSetError("release-set SHA256SUMS does not match the manifest")

    npm_record = next(item for item in records if item.get("role") == "npm-package")
    _inspect_npm_package(output / str(npm_record["filename"]), native_records)
    sbom_record = next(item for item in records if item.get("role") == "sbom")
    try:
        validate_candidate_sbom(output / str(sbom_record["filename"]), version=__version__)
    except ReleaseError as error:
        raise ReleaseSetError(f"release-set SBOM is invalid: {error}") from error
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assemble a verified cross-ecosystem Solodeveling release set without publishing."
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument("native", type=Path)
    parser.add_argument("npm_package", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-revision", required=True)
    arguments = parser.parse_args()
    try:
        manifest = assemble_release_set(
            arguments.candidate,
            arguments.native,
            arguments.npm_package,
            arguments.output,
            source_revision=arguments.source_revision,
        )
    except (OSError, ValueError, KeyError, ReleaseSetError) as error:
        print(f"release-set-error: {error}")
        return 1
    print(
        f"assembled non-publishing Solodeveling {manifest['version']} release set "
        f"from {manifest['source_revision']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
