from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from solodeveling_protocol import release


REVISION = "a" * 40


def _write(path: Path, content: bytes) -> Path:
    path.write_bytes(content)
    return path


def _sbom(path: Path, version: str = "0.1.0") -> Path:
    document = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {
            "component": {
                "type": "library",
                "name": "solodeveling",
                "version": version,
            }
        },
        "components": [
            {"type": "library", "name": "PyYAML", "version": "6.0.3"},
            {"type": "library", "name": "jsonschema", "version": "4.26.0"},
        ],
    }
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def test_candidate_manifest_binds_revision_and_all_subjects(tmp_path: Path) -> None:
    wheel = _write(tmp_path / "package.whl", b"wheel")
    sdist = _write(tmp_path / "package.tar.gz", b"sdist")
    sbom = _sbom(tmp_path / "solodeveling-0.1.0.cdx.json")
    notes = _write(tmp_path / "RELEASE-NOTES.md", b"notes")

    manifest = release.candidate_manifest(
        "0.1.0",
        REVISION,
        [wheel, sdist],
        [sbom, notes],
        build_inputs={"python": "3.14", "cyclonedx_bom": "7.3.0"},
    )

    assert manifest["solodeveling_candidate_manifest_schema"] == 1
    assert manifest["source_revision"] == REVISION
    assert manifest["target"] == (
        "Python input for coordinated GitHub Release, PyPI, and npm release "
        "(not published)"
    )
    assert [item["filename"] for item in manifest["distributions"]] == [
        "package.tar.gz",
        "package.whl",
    ]
    assert [item["filename"] for item in manifest["evidence"]] == [
        "RELEASE-NOTES.md",
        "solodeveling-0.1.0.cdx.json",
    ]
    assert manifest["build_inputs"]["cyclonedx_bom"] == "7.3.0"
    assert manifest["evidence"][0]["sha256"] == hashlib.sha256(b"notes").hexdigest()
    assert "generated_at" not in manifest


@pytest.mark.parametrize("revision", ["main", "abc", "g" * 40, "A" * 40])
def test_candidate_manifest_rejects_mutable_or_invalid_revision(
    tmp_path: Path, revision: str
) -> None:
    with pytest.raises(release.ReleaseError, match="source revision"):
        release.candidate_manifest("0.1.0", revision, [], [])


def test_candidate_sbom_rejects_wrong_project_or_missing_runtime_dependency(
    tmp_path: Path,
) -> None:
    sbom = _sbom(tmp_path / "candidate.cdx.json")
    document = json.loads(sbom.read_text("utf-8"))
    document["metadata"]["component"]["name"] = "other-project"
    document["components"] = []
    sbom.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(release.ReleaseError, match="SBOM"):
        release.validate_candidate_sbom(sbom, version="0.1.0")


def test_release_candidate_docs_and_manual_workflow_are_bounded() -> None:
    notes = Path("docs/releases/0.1.2.md").read_text("utf-8")
    publishing = Path("docs/publishing.md").read_text("utf-8")
    workflow = Path(".github/workflows/release-candidate.yml").read_text("utf-8")
    pyproject = Path("pyproject.toml").read_text("utf-8")
    ci = Path(".github/workflows/ci.yml").read_text("utf-8")

    for phrase in (
        "0.1.2",
        "Tier 1 remains unverified",
        "solodeveling uninstall",
        "SHA-256",
    ):
        assert phrase in notes
    for phrase in (
        "ohmiler/solodeveling",
        "solodeveling",
        "release-candidate.yml",
        "pypi",
        "explicit authorization",
    ):
        assert phrase in publishing
    assert re.search(r"^on:\n  workflow_dispatch:", workflow, re.MULTILINE)
    assert "pull_request:" not in workflow
    assert "push:" not in workflow
    assert "id-token: write" in workflow
    assert "attestations: write" in workflow
    assert "pypa/gh-action-pypi-publish" not in workflow
    assert "twine upload" not in workflow.lower()
    uses = re.findall(r"uses:\s*([^\s#]+)", workflow)
    assert uses and all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", item) for item in uses)
    assert "cyclonedx-bom==7.3.0" in pyproject
    builder = Path("scripts/build_candidate.py").read_text("utf-8")
    assert "    bind_candidate_sbom_identity," in builder
    assert "build_candidate.py" in ci
    assert "verify_candidate.py" in ci
    assert "id-token: write" not in ci

def test_finalize_and_verify_candidate_bundle(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    wheel = _write(bundle / "package.whl", b"wheel")
    sdist = _write(bundle / "package.tar.gz", b"sdist")
    base = release.artifact_manifest("0.1.2", [wheel, sdist])
    (bundle / "release-manifest.json").write_text(
        json.dumps(base), encoding="utf-8"
    )
    (bundle / "SHA256SUMS").write_text("base", encoding="utf-8")
    sbom = _sbom(tmp_path / "generated.cdx.json", "0.1.2")
    notes = _write(tmp_path / "notes.md", b"release notes")

    manifest = release.finalize_candidate_bundle(
        bundle,
        source_revision=REVISION,
        sbom_path=sbom,
        release_notes_path=notes,
        build_inputs={"python": "3.14", "cyclonedx_bom": "7.3.0"},
    )
    verified = release.verify_candidate_bundle(
        bundle, source_revision=REVISION
    )

    assert verified == manifest
    assert (bundle / "RELEASE-NOTES.md").read_bytes() == b"release notes"
    assert (bundle / "solodeveling-0.1.2.cdx.json").is_file()
    sums = (bundle / "SHA256SUMS").read_text("utf-8").splitlines()
    assert len(sums) == 4
    assert all(re.fullmatch(r"[0-9a-f]{64}  [^/\\]+", line) for line in sums)


def test_candidate_verifier_rejects_wrong_revision_and_tampering(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    wheel = _write(bundle / "package.whl", b"wheel")
    sdist = _write(bundle / "package.tar.gz", b"sdist")
    base = release.artifact_manifest("0.1.2", [wheel, sdist])
    (bundle / "release-manifest.json").write_text(
        json.dumps(base), encoding="utf-8"
    )
    (bundle / "SHA256SUMS").write_text("base", encoding="utf-8")
    release.finalize_candidate_bundle(
        bundle,
        source_revision=REVISION,
        sbom_path=_sbom(tmp_path / "generated.cdx.json", "0.1.2"),
        release_notes_path=_write(tmp_path / "notes.md", b"notes"),
        build_inputs={"python": "3.14", "cyclonedx_bom": "7.3.0"},
    )

    with pytest.raises(release.ReleaseError, match="source revision"):
        release.verify_candidate_bundle(bundle, source_revision="b" * 40)
    (bundle / "RELEASE-NOTES.md").write_bytes(b"tampered")
    with pytest.raises(release.ReleaseError, match="hash mismatch"):
        release.verify_candidate_bundle(bundle, source_revision=REVISION)

def test_dynamic_project_version_is_bound_before_sbom_validation(
    tmp_path: Path,
) -> None:
    sbom = _sbom(tmp_path / "dynamic.cdx.json")
    document = json.loads(sbom.read_text("utf-8"))
    document["metadata"]["component"].pop("version")
    sbom.write_text(json.dumps(document), encoding="utf-8")

    release.bind_candidate_sbom_identity(sbom, version="0.1.0")

    rebound = json.loads(sbom.read_text("utf-8"))
    assert rebound["metadata"]["component"]["version"] == "0.1.0"
    release.validate_candidate_sbom(sbom, version="0.1.0")


def test_sbom_rejects_build_tools_and_conflicting_bound_version(
    tmp_path: Path,
) -> None:
    sbom = _sbom(tmp_path / "unsafe.cdx.json")
    document = json.loads(sbom.read_text("utf-8"))
    document["metadata"]["component"]["version"] = "9.9.9"
    document["components"].append(
        {"type": "library", "name": "pip", "version": "26.1.2"}
    )
    sbom.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(release.ReleaseError, match="conflicts"):
        release.bind_candidate_sbom_identity(sbom, version="0.1.0")
    with pytest.raises(release.ReleaseError, match="build tools"):
        release.validate_candidate_sbom(sbom, version="9.9.9")
