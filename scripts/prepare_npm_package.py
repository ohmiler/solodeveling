from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from solodeveling_protocol import __version__
try:
    from scripts.build_native import native_target
except ModuleNotFoundError as error:
    if error.name != "scripts":
        raise
    from build_native import native_target


class NpmPackageError(RuntimeError):
    pass


_TARGETS = (
    ("win32", "AMD64"),
    ("win32", "ARM64"),
    ("darwin", "x86_64"),
    ("darwin", "arm64"),
    ("linux", "x86_64"),
    ("linux", "aarch64"),
)


def _record(path: Path) -> dict[str, object]:
    return {
        "filename": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size": path.stat().st_size,
    }


def prepare_npm_package(
    project_root: Path,
    native_root: Path,
    output: Path,
) -> dict[str, object]:
    project_root = project_root.resolve()
    native_root = native_root.resolve()
    output = output.resolve()
    source = project_root / "packages" / "npm"
    if output.exists() or output.is_symlink():
        raise NpmPackageError(f"npm package output already exists: {output}")
    if not source.is_dir() or source.is_symlink():
        raise NpmPackageError("npm package source is missing or unsafe")

    metadata = json.loads((source / "package.json").read_text("utf-8"))
    if metadata.get("name") != "solodeveling":
        raise NpmPackageError("npm package name must be solodeveling")
    if metadata.get("version") != __version__:
        raise NpmPackageError("npm and Python package versions do not match")
    scripts = metadata.get("scripts", {})
    if any(name in scripts for name in ("preinstall", "install", "postinstall")):
        raise NpmPackageError("npm lifecycle install scripts are forbidden")
    if metadata.get("dependencies"):
        raise NpmPackageError("npm launcher must remain dependency-free")

    artifacts: dict[str, dict[str, object]] = {}
    expected_names = set()
    for system, machine in _TARGETS:
        key, filename = native_target(system, machine)
        expected_names.add(filename)
        artifact = native_root / filename
        if (
            not artifact.is_file()
            or artifact.is_symlink()
            or artifact.resolve().parent != native_root
        ):
            raise NpmPackageError(f"native artifact is missing or unsafe: {filename}")
        if artifact.stat().st_size <= 0:
            raise NpmPackageError(f"native artifact is empty: {filename}")
        artifacts[key] = _record(artifact)

    actual_names = {
        path.name
        for path in native_root.iterdir()
        if path.is_file() or path.is_symlink()
    }
    if actual_names != expected_names:
        raise NpmPackageError("native artifact inventory is incomplete or contains extras")

    manifest = {
        "schema": 1,
        "version": __version__,
        "artifacts": dict(sorted(artifacts.items())),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, output, symlinks=True)
    for path in output.rglob("*"):
        if path.is_symlink():
            shutil.rmtree(output)
            raise NpmPackageError("npm package source contains a symlink")
    (output / "artifacts.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + chr(10),
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare a version-bound npm package without publishing."
    )
    parser.add_argument("native_root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--project-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    arguments = parser.parse_args()
    try:
        manifest = prepare_npm_package(
            arguments.project_root,
            arguments.native_root,
            arguments.output,
        )
    except (NpmPackageError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"npm-package-error: {error}")
        return 1
    print(
        f"prepared solodeveling {manifest['version']} npm package "
        f"for {len(manifest['artifacts'])} targets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
