from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
import zipfile
from pathlib import Path

from solodeveling_protocol.release import canonical_files


class VerificationError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_bytes(project_root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(project_root).as_posix(): path.read_bytes()
        for path in canonical_files(project_root)
    }


def _unique(names: list[str], archive: str) -> None:
    if len(names) != len(set(names)):
        raise VerificationError(f"duplicate entries in {archive}")


def verify_bundle(project_root: Path, bundle: Path) -> None:
    project_root = project_root.resolve()
    bundle = bundle.resolve()
    manifest_path = bundle / "release-manifest.json"
    sums_path = bundle / "SHA256SUMS"
    manifest = json.loads(manifest_path.read_text("utf-8"))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 2:
        raise VerificationError("manifest must describe two artifacts")
    expected_sums = []
    for record in artifacts:
        artifact = bundle / record["filename"]
        actual = _sha256(artifact)
        if actual != record["sha256"]:
            raise VerificationError(f"artifact hash mismatch: {artifact.name}")
        if artifact.stat().st_size != record["size"]:
            raise VerificationError(f"artifact size mismatch: {artifact.name}")
        expected_sums.append(f"{actual}  {artifact.name}")
    actual_sums = sums_path.read_text("utf-8").splitlines()
    if actual_sums != expected_sums:
        raise VerificationError("SHA256SUMS does not match the manifest")

    canonical = _canonical_bytes(project_root)
    wheel = next(bundle.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        _unique(names, wheel.name)
        for relative, expected in canonical.items():
            packaged = f"solodeveling_protocol/resources/{relative}"
            if packaged not in names or archive.read(packaged) != expected:
                raise VerificationError(f"wheel resource mismatch: {relative}")
        for required in (
            "solodeveling_protocol/resources.py",
            "solodeveling_protocol/release.py",
        ):
            if required not in names:
                raise VerificationError(f"wheel module missing: {required}")
        entry_name = next(
            name for name in names if name.endswith(".dist-info/entry_points.txt")
        )
        entries = archive.read(entry_name).decode("utf-8")
        for command in (
            "solodeveling-adapt",
            "solodeveling-eval",
            "solodeveling-init",
            "solodeveling-validate",
        ):
            if command not in entries:
                raise VerificationError(f"wheel entry point missing: {command}")
        metadata_name = next(
            name for name in names if name.endswith(".dist-info/METADATA")
        )
        metadata = archive.read(metadata_name).decode("utf-8")
        if "# Solodeveling" not in metadata:
            raise VerificationError("wheel long description is missing")
        if any("evals/results/" in name for name in names):
            raise VerificationError("local evaluation results entered the wheel")

    sdist = next(bundle.glob("*.tar.gz"))
    with tarfile.open(sdist, "r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        _unique(names, sdist.name)
        roots = {name.split("/", 1)[0] for name in names if "/" in name}
        if len(roots) != 1:
            raise VerificationError("sdist must have one top-level directory")
        root = next(iter(roots))
        for relative, expected in canonical.items():
            packaged = f"{root}/{relative}"
            try:
                member = archive.getmember(packaged)
            except KeyError as error:
                raise VerificationError(
                    f"sdist resource missing: {relative}"
                ) from error
            stream = archive.extractfile(member)
            if stream is None or stream.read() != expected:
                raise VerificationError(f"sdist resource mismatch: {relative}")
        if f"{root}/README.md" not in names:
            raise VerificationError("sdist README is missing")
        if any("evals/results/" in name for name in names):
            raise VerificationError("local evaluation results entered the sdist")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify Solodeveling release bundle contents and checksums."
    )
    parser.add_argument("bundle", type=Path)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    arguments = parser.parse_args()
    try:
        verify_bundle(arguments.project_root, arguments.bundle)
    except (OSError, ValueError, KeyError, VerificationError) as error:
        print(f"distribution-error: {error}")
        return 1
    print("Solodeveling release bundle is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
