from __future__ import annotations

import hashlib
import json
import re
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from pathlib import Path

import pytest

from solodeveling_protocol.release import (
    ReleaseError,
    artifact_manifest,
    build_release_bundle,
)


def test_python_310_compatibility_shims_are_explicit() -> None:
    runner = Path(
        "src/solodeveling_protocol/evaluation_runner.py"
    ).read_text("utf-8")
    this_test = Path(__file__).read_text("utf-8")

    assert "from datetime import UTC" not in runner
    assert "timezone.utc" in runner
    assert "import tomli as tomllib" in this_test

def test_public_package_metadata_and_resource_mappings() -> None:
    metadata = tomllib.loads(Path("pyproject.toml").read_text("utf-8"))
    project = metadata["project"]
    wheel = metadata["tool"]["hatch"]["build"]["targets"]["wheel"]

    assert project["readme"] == "README.md"
    assert project["authors"][0]["name"]
    assert project["urls"]["Source"].endswith("ohmiler/solodeveling")
    assert project["urls"]["Issues"].endswith("ohmiler/solodeveling/issues")
    assert all("==" not in dependency for dependency in project["dependencies"])
    assert "build>=1.2,<2" in project["optional-dependencies"]["dev"]
    assert wheel["force-include"]["skills"] == (
        "solodeveling_protocol/resources/skills"
    )
    assert wheel["force-include"]["evals"] == (
        "solodeveling_protocol/resources/evals"
    )


def test_readme_has_safe_multi_runtime_install_and_evidence_language() -> None:
    readme = Path("README.md").read_text("utf-8")

    for phrase in (
        "single primary agent",
        "solodeveling install --runtime codex",
        "solodeveling install --runtime claude-code",
        "solodeveling install --runtime cursor",
        "solodeveling check",
        "--dry-run",
        "Tier 1 remains unverified",
        "Apache-2.0",
    ):
        assert phrase in readme
    assert "--source ./skills" not in readme


def test_ci_is_least_privilege_pinned_and_non_publishing() -> None:
    workflow = Path(".github/workflows/ci.yml").read_text("utf-8")

    assert "permissions:\n  contents: read" in workflow
    assert "pull_request_target" not in workflow
    assert "id-token: write" not in workflow
    assert "pytest" in workflow
    assert "validate_skill_suite.py" in workflow
    assert "build_candidate.py" in workflow
    assert "verify_candidate.py" in workflow
    candidate_verifier = Path("scripts/verify_candidate.py").read_text("utf-8")
    assert "from verify_release import" in candidate_verifier
    assert "smoke_installed.py" in workflow
    lowered = workflow.lower()
    for forbidden in (
        "twine upload",
        "pypa/gh-action-pypi-publish",
        "gh release create",
    ):
        assert forbidden not in lowered
    uses = re.findall(r"uses:\s*([^\s#]+)", workflow)
    assert uses
    assert all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", value) for value in uses)


def test_public_governance_and_release_boundary_docs() -> None:
    security = Path("SECURITY.md").read_text("utf-8")
    contributing = Path("CONTRIBUTING.md").read_text("utf-8")
    readiness = Path("docs/release-readiness.md").read_text("utf-8")

    assert "Do not open a public issue" in security
    assert "private vulnerability reporting" in security
    assert "single-agent-first" in contributing
    assert "build_release.py" in contributing
    assert "does not publish" in readiness
    assert "Python 3.10 and 3.14" in readiness
    assert "Tier 1" in readiness
    assert "separate external action" in readiness

def test_artifact_manifest_is_sorted_and_hashes_exact_bytes(tmp_path: Path) -> None:
    second = tmp_path / "b.whl"
    first = tmp_path / "a.tar.gz"
    second.write_bytes(b"wheel")
    first.write_bytes(b"source")

    manifest = artifact_manifest("0.1.0", [second, first])

    assert [item["filename"] for item in manifest["artifacts"]] == [
        "a.tar.gz",
        "b.whl",
    ]
    assert manifest["artifacts"][0]["sha256"] == hashlib.sha256(
        b"source"
    ).hexdigest()
    assert "generated_at" not in manifest


def test_release_builder_refuses_existing_output_before_runner(
    tmp_path: Path,
) -> None:
    output = tmp_path / "release"
    output.mkdir()
    called = False

    def runner(argv, cwd):
        nonlocal called
        called = True
        raise AssertionError("runner must not execute")

    with pytest.raises(ReleaseError, match="already exists"):
        build_release_bundle(tmp_path, output, runner=runner)

    assert not called


def test_release_manifest_json_is_deterministic() -> None:
    document = {"version": "0.1.0", "artifacts": []}
    first = json.dumps(document, indent=2, sort_keys=True) + "\n"
    second = json.dumps(document, indent=2, sort_keys=True) + "\n"
    assert first == second
