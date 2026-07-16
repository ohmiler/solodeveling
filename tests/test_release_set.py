from __future__ import annotations

import hashlib
import io
import json
import tarfile
from pathlib import Path

import pytest

from scripts.assemble_release_set import (
    ReleaseSetError,
    assemble_release_set,
    verify_release_set,
)
from scripts.build_native import native_target
from solodeveling_protocol import release


REVISION = "a" * 40
TARGETS = (
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


def _candidate(root: Path) -> Path:
    root.mkdir()
    wheel = root / "solodeveling-0.1.1-py3-none-any.whl"
    sdist = root / "solodeveling-0.1.1.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")
    base = release.artifact_manifest("0.1.1", [wheel, sdist])
    (root / "release-manifest.json").write_text(json.dumps(base), encoding="utf-8")
    (root / "SHA256SUMS").write_text("base\n", encoding="utf-8")
    sbom = root.parent / "generated.cdx.json"
    sbom.write_text(
        json.dumps(
            {
                "bomFormat": "CycloneDX",
                "specVersion": "1.6",
                "version": 1,
                "metadata": {
                    "component": {
                        "type": "library",
                        "name": "solodeveling",
                        "version": "0.1.1",
                    }
                },
                "components": [
                    {"type": "library", "name": "PyYAML", "version": "6.0.3"},
                    {"type": "library", "name": "jsonschema", "version": "4.26.0"},
                ],
            }
        ),
        encoding="utf-8",
    )
    notes = root.parent / "notes.md"
    notes.write_text("release notes\n", encoding="utf-8")
    release.finalize_candidate_bundle(
        root,
        source_revision=REVISION,
        sbom_path=sbom,
        release_notes_path=notes,
        build_inputs={"python": "3.14", "cyclonedx_bom": "7.3.0"},
    )
    return root


def _native(root: Path) -> tuple[Path, dict[str, dict[str, object]]]:
    root.mkdir()
    records = {}
    for system, machine in TARGETS:
        key, filename = native_target(system, machine)
        artifact = root / filename
        artifact.write_bytes(("native-" + key).encode())
        records[key] = _record(artifact)
    return root, records


def _npm_tarball(
    path: Path,
    records: dict[str, dict[str, object]],
    *,
    symlink: bool = False,
    unsafe_path: bool = False,
) -> Path:
    metadata = json.dumps({"name": "solodeveling", "version": "0.1.1"}).encode()
    manifest = json.dumps(
        {"schema": 1, "version": "0.1.1", "artifacts": records}
    ).encode()
    with tarfile.open(path, "w:gz") as archive:
        for name, content in (
            ("package/package.json", metadata),
            ("package/artifacts.json", manifest),
        ):
            member = tarfile.TarInfo(name)
            member.size = len(content)
            archive.addfile(member, io.BytesIO(content))
        if symlink:
            member = tarfile.TarInfo("package/unsafe")
            member.type = tarfile.SYMTYPE
            member.linkname = "../../outside"
            archive.addfile(member)
        if unsafe_path:
            content = b"unsafe"
            member = tarfile.TarInfo("package/../../outside")
            member.size = len(content)
            archive.addfile(member, io.BytesIO(content))
    return path


def _inputs(tmp_path: Path):
    candidate = _candidate(tmp_path / "candidate")
    native, records = _native(tmp_path / "native")
    npm = _npm_tarball(tmp_path / "solodeveling-0.1.1.tgz", records)
    return candidate, native, npm


def test_assemble_and_verify_complete_release_set(tmp_path: Path) -> None:
    candidate, native, npm = _inputs(tmp_path)
    output = tmp_path / "release-set"

    manifest = assemble_release_set(
        candidate, native, npm, output, source_revision=REVISION
    )
    verified = verify_release_set(output, source_revision=REVISION)

    assert verified == manifest
    assert manifest["solodeveling_release_set_schema"] == 1
    assert manifest["version"] == "0.1.1"
    assert manifest["source_revision"] == REVISION
    assert "generated_at" not in manifest
    roles = [record["role"] for record in manifest["artifacts"]]
    assert roles.count("python-distribution") == 2
    assert roles.count("native-executable") == 6
    assert roles.count("npm-package") == 1
    assert roles.count("sbom") == 1
    assert roles.count("release-notes") == 1
    assert len((output / "SHA256SUMS").read_text("utf-8").splitlines()) == 11


def test_assembly_rejects_npm_manifest_that_does_not_bind_native_bytes(
    tmp_path: Path,
) -> None:
    candidate = _candidate(tmp_path / "candidate")
    native, records = _native(tmp_path / "native")
    records["linux-x64"]["sha256"] = "0" * 64
    npm = _npm_tarball(tmp_path / "solodeveling-0.1.1.tgz", records)

    with pytest.raises(ReleaseSetError, match="npm native manifest"):
        assemble_release_set(
            candidate, native, npm, tmp_path / "output", source_revision=REVISION
        )


@pytest.mark.parametrize("change", ["missing", "extra"])
def test_assembly_rejects_incomplete_or_extra_native_inventory(
    tmp_path: Path, change: str
) -> None:
    candidate, native, npm = _inputs(tmp_path)
    if change == "missing":
        next(native.iterdir()).unlink()
    else:
        (native / "unexpected").write_bytes(b"extra")

    with pytest.raises(ReleaseSetError, match="native artifact inventory"):
        assemble_release_set(
            candidate, native, npm, tmp_path / "output", source_revision=REVISION
        )


def test_assembly_rejects_symlink_in_npm_archive(tmp_path: Path) -> None:
    candidate = _candidate(tmp_path / "candidate")
    native, records = _native(tmp_path / "native")
    npm = _npm_tarball(
        tmp_path / "solodeveling-0.1.1.tgz", records, symlink=True
    )

    with pytest.raises(ReleaseSetError, match="link"):
        assemble_release_set(
            candidate, native, npm, tmp_path / "output", source_revision=REVISION
        )


def test_assembly_rejects_path_traversal_in_npm_archive(tmp_path: Path) -> None:
    candidate = _candidate(tmp_path / "candidate")
    native, records = _native(tmp_path / "native")
    npm = _npm_tarball(
        tmp_path / "solodeveling-0.1.1.tgz", records, unsafe_path=True
    )

    with pytest.raises(ReleaseSetError, match="path is unsafe"):
        assemble_release_set(
            candidate, native, npm, tmp_path / "output", source_revision=REVISION
        )

def test_verifier_rejects_tampering_extras_and_wrong_revision(tmp_path: Path) -> None:
    candidate, native, npm = _inputs(tmp_path)
    output = tmp_path / "release-set"
    assemble_release_set(candidate, native, npm, output, source_revision=REVISION)

    with pytest.raises(ReleaseSetError, match="source revision"):
        verify_release_set(output, source_revision="b" * 40)
    (output / "unexpected").write_bytes(b"extra")
    with pytest.raises(ReleaseSetError, match="inventory"):
        verify_release_set(output, source_revision=REVISION)
    (output / "unexpected").unlink()
    native_output = next(output.glob("solodeveling-*-linux-x64"))
    original = native_output.read_bytes()
    native_output.write_bytes(bytes([original[0] ^ 1]) + original[1:])
    with pytest.raises(ReleaseSetError, match="hash mismatch"):
        verify_release_set(output, source_revision=REVISION)


@pytest.mark.parametrize("revision", ["main", "A" * 40, "g" * 40])
def test_assembly_rejects_mutable_or_invalid_source_revision(
    tmp_path: Path, revision: str
) -> None:
    candidate, native, npm = _inputs(tmp_path)
    with pytest.raises(ReleaseSetError, match="source revision"):
        assemble_release_set(
            candidate, native, npm, tmp_path / "output", source_revision=revision
        )

def test_manual_release_set_workflow_is_pinned_bounded_and_non_publishing() -> None:
    import re

    workflow = Path(".github/workflows/release-candidate.yml").read_text("utf-8")
    assert re.search(r"^on:\n  workflow_dispatch:", workflow, re.MULTILINE)
    assert "pull_request:" not in workflow
    assert "push:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "assemble_release_set.py" in workflow
    assert "verify_release_set.py" in workflow
    assert "release-set/*" in workflow
    assert "id-token: write" in workflow
    assert "attestations: write" in workflow
    assert "packages: write" not in workflow
    assert "contents: write" not in workflow
    assert "environment:" not in workflow
    lowered = workflow.lower()
    for forbidden in (
        "npm publish",
        "twine upload",
        "pypa/gh-action-pypi-publish",
        "gh release create",
        "git tag",
    ):
        assert forbidden not in lowered
    uses = re.findall(r"uses:\s*([^\s#]+)", workflow)
    assert uses and all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", item) for item in uses)

def test_release_set_docs_define_non_publishing_boundary_and_recovery() -> None:
    publishing = Path("docs/publishing.md").read_text("utf-8")
    readiness = Path("docs/release-readiness.md").read_text("utf-8")
    contributing = Path("CONTRIBUTING.md").read_text("utf-8")
    notes = Path("docs/releases/0.1.1.md").read_text("utf-8")
    publishing_normalized = " ".join(publishing.split())
    for phrase in (
        "complete release set",
        "not publish",
        "rebuild the entire set",
        "separate explicit authorization",
    ):
        assert phrase in publishing_normalized
    assert "assemble_release_set.py" in readiness
    assert "verify_release_set.py" in readiness
    assert "release-set-manifest.json" in readiness
    assert "assemble_release_set.py" in contributing
    assert "complete cross-ecosystem release set" in notes
