from __future__ import annotations

import argparse
import importlib.metadata
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from solodeveling_protocol import __version__
from solodeveling_protocol.release import (
    ReleaseError,
    build_release_bundle,
    finalize_candidate_bundle,
)


class CandidateBuildError(RuntimeError):
    pass


def _run(argv: tuple[str, ...], cwd: Path, label: str) -> None:
    process = subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        shell=False,
    )
    if process.returncode != 0:
        raise CandidateBuildError(
            f"{label} failed with exit code {process.returncode}"
        )


def _capture(argv: tuple[str, ...], cwd: Path, label: str) -> str:
    process = subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        shell=False,
    )
    if process.returncode != 0:
        raise CandidateBuildError(
            f"{label} failed with exit code {process.returncode}"
        )
    return process.stdout.strip()


def _runtime_python(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def build_candidate(
    project_root: Path, output: Path, *, source_revision: str
) -> dict[str, object]:
    project_root = project_root.resolve()
    output = output.resolve()
    if output.exists():
        raise CandidateBuildError(f"candidate output already exists: {output}")
    actual_revision = _capture(
        ("git", "rev-parse", "HEAD"), project_root, "source revision check"
    )
    if actual_revision != source_revision:
        raise CandidateBuildError("requested source revision is not the checked-out HEAD")
    if _capture(("git", "status", "--porcelain"), project_root, "worktree check"):
        raise CandidateBuildError("candidate build requires a clean worktree")
    notes = project_root / "docs" / "releases" / f"{__version__}.md"
    if not notes.is_file() or notes.is_symlink():
        raise CandidateBuildError("versioned release notes are missing or unsafe")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".solodeveling-candidate-", dir=output.parent
    ) as temporary:
        root = Path(temporary)
        bundle = root / "bundle"
        build_release_bundle(project_root, bundle)
        wheel = next(bundle.glob("*.whl"))
        runtime = root / "runtime"
        _run((sys.executable, "-m", "venv", str(runtime)), project_root, "venv creation")
        runtime_python = _runtime_python(runtime)
        _run(
            (
                str(runtime_python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                str(wheel),
            ),
            project_root,
            "candidate installation",
        )
        sbom = root / f"solodeveling-protocol-{__version__}.cdx.json"
        _run(
            (
                sys.executable,
                "-m",
                "cyclonedx_py",
                "environment",
                str(runtime_python),
                "--pyproject",
                str(project_root / "pyproject.toml"),
                "--mc-type",
                "library",
                "--spec-version",
                "1.6",
                "--output-reproducible",
                "--output-format",
                "JSON",
                "--output-file",
                str(sbom),
                "--validate",
            ),
            project_root,
            "CycloneDX SBOM generation",
        )
        manifest = finalize_candidate_bundle(
            bundle,
            source_revision=source_revision,
            sbom_path=sbom,
            release_notes_path=notes,
            build_inputs={
                "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "build": importlib.metadata.version("build"),
                "cyclonedx_bom": importlib.metadata.version("cyclonedx-bom"),
            },
        )
        shutil.move(str(bundle), str(output))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a source-bound Solodeveling candidate without publishing."
    )
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument(
        "--project-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    arguments = parser.parse_args()
    try:
        manifest = build_candidate(
            arguments.project_root,
            arguments.output,
            source_revision=arguments.source_revision,
        )
    except (CandidateBuildError, ReleaseError, OSError, StopIteration) as error:
        print(f"candidate-error: {error}")
        return 1
    print(
        f"built non-publishing candidate {manifest['version']} "
        f"from {manifest['source_revision']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())