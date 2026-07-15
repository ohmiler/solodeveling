from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

from scripts import prepare_publication
from scripts.prepare_publication import (
    PublicationError,
    prepare_publication_inputs,
    verify_publication_inputs,
)


REVISION = "a" * 40


def _record(path: Path, role: str) -> dict[str, object]:
    return {
        "filename": path.name,
        "role": role,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "size": path.stat().st_size,
    }


def _release_set(root: Path) -> tuple[Path, dict[str, object]]:
    root.mkdir()
    wheel = root / "solodeveling-0.1.0-py3-none-any.whl"
    sdist = root / "solodeveling-0.1.0.tar.gz"
    npm = root / "solodeveling-0.1.0.tgz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")
    npm.write_bytes(b"npm")
    records = [
        _record(wheel, "python-distribution"),
        _record(sdist, "python-distribution"),
        _record(npm, "npm-package"),
    ]
    manifest = {
        "solodeveling_release_set_schema": 1,
        "version": "0.1.0",
        "source_revision": REVISION,
        "target": "coordinated release input (not published)",
        "artifacts": sorted(records, key=lambda item: str(item["filename"])),
    }
    return root, manifest


def test_prepare_and_verify_publication_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    release_set, manifest = _release_set(tmp_path / "release-set")
    monkeypatch.setattr(
        prepare_publication,
        "verify_release_set",
        lambda path, *, source_revision: manifest,
    )
    output = tmp_path / "publication"

    plan = prepare_publication_inputs(
        release_set, output, source_revision=REVISION
    )
    verified = verify_publication_inputs(output, source_revision=REVISION)

    assert verified == plan
    assert plan["solodeveling_publication_plan_schema"] == 1
    assert plan["version"] == "0.1.0"
    assert plan["source_revision"] == REVISION
    assert "generated_at" not in plan
    assert sorted(path.name for path in (output / "pypi").iterdir()) == [
        "solodeveling-0.1.0-py3-none-any.whl",
        "solodeveling-0.1.0.tar.gz",
    ]
    assert [path.name for path in (output / "npm").iterdir()] == [
        "solodeveling-0.1.0.tgz"
    ]


def test_publication_verifier_rejects_tampering_and_extras(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    release_set, manifest = _release_set(tmp_path / "release-set")
    monkeypatch.setattr(
        prepare_publication,
        "verify_release_set",
        lambda path, *, source_revision: manifest,
    )
    output = tmp_path / "publication"
    prepare_publication_inputs(release_set, output, source_revision=REVISION)

    wheel = next((output / "pypi").glob("*.whl"))
    original = wheel.read_bytes()
    wheel.write_bytes(bytes([original[0] ^ 1]) + original[1:])
    with pytest.raises(PublicationError, match="hash mismatch"):
        verify_publication_inputs(output, source_revision=REVISION)
    wheel.write_bytes(original)
    (output / "npm" / "unexpected").write_bytes(b"extra")
    with pytest.raises(PublicationError, match="inventory"):
        verify_publication_inputs(output, source_revision=REVISION)


def test_publication_preparation_rejects_existing_output_and_missing_role(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    release_set, manifest = _release_set(tmp_path / "release-set")
    output = tmp_path / "publication"
    output.mkdir()
    monkeypatch.setattr(
        prepare_publication,
        "verify_release_set",
        lambda path, *, source_revision: manifest,
    )
    with pytest.raises(PublicationError, match="already exists"):
        prepare_publication_inputs(release_set, output, source_revision=REVISION)

    output.rmdir()
    manifest["artifacts"] = [
        item for item in manifest["artifacts"] if item["role"] != "npm-package"
    ]
    with pytest.raises(PublicationError, match="package roles"):
        prepare_publication_inputs(release_set, output, source_revision=REVISION)


def test_publish_workflow_is_manual_pinned_oidc_only_and_environment_gated() -> None:
    workflow = Path(".github/workflows/publish.yml").read_text("utf-8")
    assert re.search(r"^on:\n  workflow_dispatch:", workflow, re.MULTILINE)
    assert "push:" not in workflow
    assert "pull_request:" not in workflow
    assert "pull_request_target:" not in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "CONFIRM publish solodeveling" in workflow
    assert "scripts/publication_gate.py" in workflow
    assert "source_revision must equal the publish workflow commit" not in workflow
    assert "fetch-depth: 0" in workflow
    assert "release is draft" in workflow
    assert "release is not immutable" in workflow
    assert "gh release verify " in workflow
    assert "gh release verify-asset" in workflow
    assert "verify_release_set.py" in workflow
    assert "prepare_publication.py" in workflow
    assert "gh attestation verify" in workflow
    assert "--signer-workflow ohmiler/solodeveling/.github/workflows/release-candidate.yml" in workflow
    assert "environment: pypi" in workflow
    assert "environment: npm" in workflow
    assert workflow.count("id-token: write") == 2
    assert "contents: write" not in workflow
    assert "packages: write" not in workflow
    assert "secrets." not in workflow
    assert "NPM_TOKEN" not in workflow
    assert "NODE_AUTH_TOKEN" not in workflow
    assert "password:" not in workflow
    assert "npm@11.15.0" in workflow
    assert "npm stage publish" in workflow
    assert "npm publish" in workflow
    assert "if: inputs.npm_action == 'stage'" in workflow
    assert "if: inputs.npm_action == 'publish'" in workflow
    uses = re.findall(r"uses:\s*([^\s#]+)", workflow)
    assert uses and all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", item) for item in uses)


def test_release_candidate_attestation_is_bound_to_main_workflow_commit() -> None:
    workflow = Path(".github/workflows/release-candidate.yml").read_text("utf-8")
    assert "GITHUB_REF" in workflow
    assert "refs/heads/main" in workflow
    assert "GITHUB_SHA" in workflow
    assert "source_revision must equal the workflow commit" in workflow


def test_publication_docs_cover_owner_setup_bootstrap_and_recovery() -> None:
    docs = Path("docs/publishing.md").read_text("utf-8")
    normalized = " ".join(docs.split())
    for phrase in (
        "pending publisher",
        "npm package does not exist",
        "first npm publication",
        "two-factor authentication",
        "environment: pypi",
        "environment: npm",
        "publish.yml",
        "ancestor",
        "rebuild the entire set",
        "post-publication smoke",
    ):
        assert phrase in normalized