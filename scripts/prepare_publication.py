from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Mapping

try:
    from scripts.assemble_release_set import verify_release_set
except ModuleNotFoundError as error:
    if error.name != "scripts":
        raise
    from assemble_release_set import verify_release_set
from solodeveling_protocol import __version__


class PublicationError(RuntimeError):
    pass


_SOURCE_REVISION = re.compile(r"[0-9a-f]{40}")
_SAFE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,254}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_name(value: object) -> str:
    if (
        not isinstance(value, str)
        or _SAFE_NAME.fullmatch(value) is None
        or Path(value).name != value
        or "/" in value
        or "\\" in value
    ):
        raise PublicationError("publication filename is unsafe")
    return value


def _selected_records(
    manifest: Mapping[str, object],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not all(
        isinstance(item, dict) for item in artifacts
    ):
        raise PublicationError("release-set artifact inventory is malformed")
    python = [dict(item) for item in artifacts if item.get("role") == "python-distribution"]
    npm = [dict(item) for item in artifacts if item.get("role") == "npm-package"]
    if len(python) != 2 or len(npm) != 1:
        raise PublicationError("release set does not contain exact publication package roles")
    python.sort(key=lambda item: str(item.get("filename")))
    names = [_safe_name(item.get("filename")) for item in python]
    wheel = [name for name in names if name.endswith(".whl")]
    expected_sdist = f"solodeveling-{__version__}.tar.gz"
    if (
        len(wheel) != 1
        or not wheel[0].startswith(f"solodeveling-{__version__}-")
        or set(names) != {wheel[0], expected_sdist}
    ):
        raise PublicationError("Python publication package identity is invalid")
    npm_name = _safe_name(npm[0].get("filename"))
    if npm_name != f"solodeveling-{__version__}.tgz":
        raise PublicationError("npm publication package identity is invalid")
    return python, npm[0]


def _plan_record(record: Mapping[str, object]) -> dict[str, object]:
    name = _safe_name(record.get("filename"))
    sha256 = record.get("sha256")
    size = record.get("size")
    if (
        not isinstance(sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", sha256) is None
        or not isinstance(size, int)
        or isinstance(size, bool)
        or size <= 0
    ):
        raise PublicationError(f"publication record is malformed: {name}")
    return {"filename": name, "sha256": sha256, "size": size}


def prepare_publication_inputs(
    release_set: Path,
    output: Path,
    *,
    source_revision: str,
) -> dict[str, object]:
    if _SOURCE_REVISION.fullmatch(source_revision) is None:
        raise PublicationError("source revision must be a lowercase 40-character Git SHA")
    release_input = Path(release_set)
    output_input = Path(output)
    if release_input.is_symlink():
        raise PublicationError("release-set input is missing or unsafe")
    if output_input.exists() or output_input.is_symlink():
        raise PublicationError(f"publication output already exists: {output_input}")
    release_set = release_input.resolve()
    output = output_input.resolve()
    manifest = verify_release_set(release_set, source_revision=source_revision)
    if manifest.get("version") != __version__:
        raise PublicationError("release-set version does not match the package")
    python_records, npm_record = _selected_records(manifest)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".solodeveling-publication-", dir=output.parent
    ) as temporary:
        stage = Path(temporary) / "publication"
        pypi = stage / "pypi"
        npm = stage / "npm"
        pypi.mkdir(parents=True)
        npm.mkdir()
        prepared_python = []
        for record in python_records:
            expected = _plan_record(record)
            source = release_set / str(expected["filename"])
            destination = pypi / source.name
            shutil.copyfile(source, destination)
            actual = {
                "filename": destination.name,
                "sha256": _sha256(destination),
                "size": destination.stat().st_size,
            }
            if actual != expected:
                raise PublicationError(f"publication input changed during copy: {source.name}")
            prepared_python.append(actual)
        expected_npm = _plan_record(npm_record)
        npm_source = release_set / str(expected_npm["filename"])
        npm_destination = npm / npm_source.name
        shutil.copyfile(npm_source, npm_destination)
        actual_npm = {
            "filename": npm_destination.name,
            "sha256": _sha256(npm_destination),
            "size": npm_destination.stat().st_size,
        }
        if actual_npm != expected_npm:
            raise PublicationError(
                f"publication input changed during copy: {npm_source.name}"
            )
        plan: dict[str, object] = {
            "solodeveling_publication_plan_schema": 1,
            "version": __version__,
            "source_revision": source_revision,
            "target": "registry upload inputs (not published)",
            "pypi": prepared_python,
            "npm": actual_npm,
        }
        (stage / "publication-plan.json").write_text(
            json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        verify_publication_inputs(stage, source_revision=source_revision)
        stage.replace(output)
    return plan


def _verify_record(root: Path, value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise PublicationError("publication plan record is malformed")
    expected = _plan_record(value)
    path = root / str(expected["filename"])
    if not path.is_file() or path.is_symlink():
        raise PublicationError(f"publication input is missing or unsafe: {path.name}")
    if path.stat().st_size != expected["size"]:
        raise PublicationError(f"publication size mismatch: {path.name}")
    if _sha256(path) != expected["sha256"]:
        raise PublicationError(f"publication hash mismatch: {path.name}")
    return expected


def verify_publication_inputs(
    publication: Path, *, source_revision: str
) -> dict[str, object]:
    if _SOURCE_REVISION.fullmatch(source_revision) is None:
        raise PublicationError("source revision must be a lowercase 40-character Git SHA")
    publication_input = Path(publication)
    if publication_input.is_symlink():
        raise PublicationError("publication input directory is missing or unsafe")
    publication = publication_input.resolve()
    if not publication.is_dir():
        raise PublicationError("publication input directory is missing or unsafe")
    try:
        plan = json.loads((publication / "publication-plan.json").read_text("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise PublicationError("publication plan is malformed") from error
    if not isinstance(plan, dict) or plan.get("solodeveling_publication_plan_schema") != 1:
        raise PublicationError("publication plan schema is unsupported")
    if plan.get("version") != __version__:
        raise PublicationError("publication plan version does not match the package")
    if plan.get("source_revision") != source_revision:
        raise PublicationError("publication plan source revision does not match")
    if plan.get("target") != "registry upload inputs (not published)":
        raise PublicationError("publication plan target is invalid")
    if {path.name for path in publication.iterdir()} != {
        "publication-plan.json",
        "pypi",
        "npm",
    }:
        raise PublicationError("publication root inventory is incomplete or contains extras")
    pypi = publication / "pypi"
    npm = publication / "npm"
    if (
        not pypi.is_dir()
        or pypi.is_symlink()
        or not npm.is_dir()
        or npm.is_symlink()
    ):
        raise PublicationError("publication package directories are missing or unsafe")
    pypi_values = plan.get("pypi")
    if not isinstance(pypi_values, list) or len(pypi_values) != 2:
        raise PublicationError("publication plan Python inventory is malformed")
    expected_python = [_verify_record(pypi, item) for item in pypi_values]
    expected_npm = _verify_record(npm, plan.get("npm"))
    if {path.name for path in pypi.iterdir()} != {
        str(item["filename"]) for item in expected_python
    }:
        raise PublicationError("PyPI publication inventory is incomplete or contains extras")
    if {path.name for path in npm.iterdir()} != {str(expected_npm["filename"])}:
        raise PublicationError("npm publication inventory is incomplete or contains extras")
    synthetic = {
        "artifacts": [
            {**item, "role": "python-distribution"} for item in expected_python
        ]
        + [{**expected_npm, "role": "npm-package"}]
    }
    _selected_records(synthetic)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare exact Solodeveling registry inputs without publishing."
    )
    parser.add_argument("release_set", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()
    try:
        if arguments.verify_only:
            plan = verify_publication_inputs(
                arguments.release_set, source_revision=arguments.source_revision
            )
        else:
            plan = prepare_publication_inputs(
                arguments.release_set,
                arguments.output,
                source_revision=arguments.source_revision,
            )
    except (OSError, ValueError, KeyError, PublicationError) as error:
        print(f"publication-error: {error}")
        return 1
    print(
        f"prepared Solodeveling {plan['version']} registry inputs from "
        f"{plan['source_revision']} without publishing"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())