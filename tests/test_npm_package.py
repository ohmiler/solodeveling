from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.build_native import native_target
from scripts.prepare_npm_package import NpmPackageError, prepare_npm_package


TARGETS = (
    ("win32", "AMD64"),
    ("win32", "ARM64"),
    ("darwin", "x86_64"),
    ("darwin", "arm64"),
    ("linux", "x86_64"),
    ("linux", "aarch64"),
)


def write_native_set(root: Path) -> None:
    root.mkdir()
    for system, machine in TARGETS:
        key, filename = native_target(system, machine)
        (root / filename).write_bytes(("native-" + key).encode())


def test_prepare_npm_package_binds_complete_native_inventory(
    tmp_path: Path,
) -> None:
    native = tmp_path / "native"
    output = tmp_path / "package"
    write_native_set(native)

    manifest = prepare_npm_package(Path("."), native, output)

    assert manifest["version"] == "0.1.0"
    assert set(manifest["artifacts"]) == {
        "win32-x64",
        "win32-arm64",
        "darwin-x64",
        "darwin-arm64",
        "linux-x64",
        "linux-arm64",
    }
    written = json.loads((output / "artifacts.json").read_text("utf-8"))
    assert written == manifest
    assert all(
        len(record["sha256"]) == 64 and record["size"] > 0
        for record in manifest["artifacts"].values()
    )


def test_prepare_npm_package_refuses_missing_native_target(
    tmp_path: Path,
) -> None:
    native = tmp_path / "native"
    write_native_set(native)
    (native / "solodeveling-0.1.0-linux-arm64").unlink()

    with pytest.raises(NpmPackageError, match="missing or unsafe"):
        prepare_npm_package(Path("."), native, tmp_path / "package")


def test_prepare_npm_package_refuses_extra_artifact(
    tmp_path: Path,
) -> None:
    native = tmp_path / "native"
    write_native_set(native)
    (native / "unexpected").write_bytes(b"extra")

    with pytest.raises(NpmPackageError, match="contains extras"):
        prepare_npm_package(Path("."), native, tmp_path / "package")


def test_prepare_npm_package_script_is_directly_executable(
    tmp_path: Path,
) -> None:
    import subprocess
    import sys

    native = tmp_path / "native"
    write_native_set(native)
    output = tmp_path / "package"
    process = subprocess.run(
        (
            sys.executable,
            "scripts/prepare_npm_package.py",
            str(native),
            str(output),
        ),
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )

    assert process.returncode == 0, process.stderr + process.stdout
    assert (output / "artifacts.json").is_file()

def test_prepare_npm_package_refuses_existing_output(
    tmp_path: Path,
) -> None:
    native = tmp_path / "native"
    write_native_set(native)
    output = tmp_path / "package"
    output.mkdir()

    with pytest.raises(NpmPackageError, match="already exists"):
        prepare_npm_package(Path("."), native, output)
