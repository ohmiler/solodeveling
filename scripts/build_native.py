from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Sequence

from solodeveling_protocol import __version__


class NativeBuildError(RuntimeError):
    pass


Runner = Callable[[Sequence[str], Path], int]


def native_target(system: str, machine: str) -> tuple[str, str]:
    normalized = machine.lower()
    architecture = {
        "amd64": "x64",
        "x86_64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
    }.get(normalized)
    operating_system = {
        "win32": "windows",
        "darwin": "macos",
        "linux": "linux",
    }.get(system)
    if architecture is None or operating_system is None:
        raise NativeBuildError(
            f"unsupported native build target: {system}-{machine}"
        )
    key = f"{system}-{architecture}"
    suffix = ".exe" if system == "win32" else ""
    filename = (
        f"solodeveling-{__version__}-{operating_system}-{architecture}{suffix}"
    )
    return key, filename


def _default_runner(argv: Sequence[str], cwd: Path) -> int:
    process = subprocess.run(
        tuple(argv),
        cwd=cwd,
        check=False,
        shell=False,
    )
    return process.returncode


def build_native(
    project_root: Path,
    output_root: Path,
    *,
    system: str = sys.platform,
    machine: str = platform.machine(),
    runner: Runner = _default_runner,
) -> Path:
    project_root = project_root.resolve()
    output_root = output_root.resolve()
    _, filename = native_target(system, machine)
    destination = output_root / filename
    if destination.exists() or destination.is_symlink():
        raise NativeBuildError(f"native output already exists: {destination}")

    required = (
        project_root / "src",
        project_root / "src" / "solodeveling_protocol" / "templates",
        project_root / "src" / "solodeveling_protocol" / "schemas",
        project_root / "skills",
        project_root / "evals",
        project_root / "scripts" / "native_entry.py",
    )
    if any(not path.exists() or path.is_symlink() for path in required):
        raise NativeBuildError("native build input is missing or unsafe")

    output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".solodeveling-native-", dir=output_root
    ) as temporary:
        stage = Path(temporary)
        dist = stage / "dist"
        work = stage / "work"
        spec = stage / "spec"
        separator = os.pathsep
        argv = (
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--onefile",
            "--noupx",
            "--collect-data",
            "rfc3987_syntax",
            "--name",
            "solodeveling",
            "--paths",
            str(project_root / "src"),
            "--add-data",
            str(project_root / "skills")
            + separator
            + "solodeveling_protocol/resources/skills",
            "--add-data",
            str(project_root / "evals")
            + separator
            + "solodeveling_protocol/resources/evals",
            "--add-data",
            str(project_root / "src" / "solodeveling_protocol" / "templates")
            + separator
            + "solodeveling_protocol/templates",
            "--add-data",
            str(project_root / "src" / "solodeveling_protocol" / "schemas")
            + separator
            + "solodeveling_protocol/schemas",
            "--distpath",
            str(dist),
            "--workpath",
            str(work),
            "--specpath",
            str(spec),
            str(project_root / "scripts" / "native_entry.py"),
        )
        if runner(argv, project_root) != 0:
            raise NativeBuildError("PyInstaller native build failed")
        built = dist / ("solodeveling.exe" if system == "win32" else "solodeveling")
        if not built.is_file() or built.is_symlink():
            raise NativeBuildError("PyInstaller did not produce the expected executable")
        shutil.move(str(built), str(destination))
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the current-platform Solodeveling executable without publishing."
    )
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--project-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    arguments = parser.parse_args()
    try:
        built = build_native(arguments.project_root, arguments.output)
    except (NativeBuildError, OSError) as error:
        print(f"native-build-error: {error}")
        return 1
    print(built)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
