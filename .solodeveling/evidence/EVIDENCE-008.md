---
solodeveling_schema: 1
id: EVIDENCE-008
work_item: WORK-008
claim: Solodeveling 0.1.0 has a non-publishing, source-bound release-candidate path that generates and strictly validates a CycloneDX 1.6 runtime SBOM, verifies complete artifact identity and tamper resistance, passes installed-wheel and dependency-security checks, and keeps provenance and publication behind explicit manual authority.
method: Failing candidate identity and SBOM contract tests, exact Git revision and clean-worktree enforcement, isolated wheel build and installation, official CycloneDX generation from a target venv without build tools, dynamic-version binding, strict official schema validation, complete inventory and SHA-256 verification, tamper tests, installed command and adapter smoke, pip-audit from a separate tool environment, full regression, official skill validation, protocol validation, cross-platform CI, compilation, dependency health, and diff inspection.
command: python -m pytest -q; python scripts/validate_skill_suite.py; quick_validate.py for all ten skills; python -m solodeveling_protocol.cli .; python scripts/build_candidate.py C:\tmp\solodeveling-work008-168bc7c --source-revision 168bc7c6708439b7fa012f65cd793c00f7bc4990; python scripts/verify_candidate.py against the same revision; install the exact wheel in a fresh Python 3.14 venv; python scripts/smoke_installed.py from C:\tmp; pip-audit 2.10.1 --path against the target site-packages from a separate tool venv; compileall; pip check; git diff --check; GitHub Actions run 29429717783.
result: passed
scope: Candidate manifest and exact source binding, wheel, source distribution, versioned release notes, CycloneDX JSON SBOM, runtime dependency inventory, checksums, manual full-SHA-pinned GitHub provenance workflow, PyPI Trusted Publishing boundary documentation, ordinary least-privilege CI, local Windows installed smoke, Ubuntu candidate build, and Windows/Ubuntu/macOS regression matrices on Python 3.10 and 3.14.
limitations:
- The verified candidate is a pre-merge review candidate from commit 168bc7c6708439b7fa012f65cd793c00f7bc4990. Publication requires a complete rebuild from the eventual merge commit on main.
- Pull request 8 remains open. No version tag, GitHub Release, GitHub environment, PyPI project, OIDC token, artifact attestation, signature, or registry upload was created.
- The manual provenance workflow was inspected and parsed by GitHub but was not invoked, so no attestation claim is made.
- The candidate package job ran on Ubuntu with Python 3.14 and local installed smoke ran on Windows with Python 3.14. macOS ran regression and protocol checks rather than candidate installation.
- Runtime dependencies are resolved within declared ranges at build time and bound in the SBOM; a future rebuild can resolve different safe versions and must produce new digests.
- pip-audit reported no known dependency vulnerabilities but skipped unpublished solodeveling-protocol because it was not found on PyPI.
- The package-name 404 result is time-sensitive and is not a reservation.
- Cursor live behavior and the complete Tier 1 matrix remain unverified.
---
# Verification summary

On 2026-07-15, 152 tests passed locally. The suite validator, all ten official skill
validations, protocol validation, compilation, dependency health, and diff checks
passed. GitHub Actions run
[29429717783](https://github.com/ohmiler/solodeveling/actions/runs/29429717783)
passed the Ubuntu candidate package job plus six regression combinations across
Windows, Ubuntu, and macOS with Python 3.10 and 3.14.

The source-bound candidate from commit `168bc7c6708439b7fa012f65cd793c00f7bc4990`
passed the base distribution verifier, candidate inventory verifier, and official
CycloneDX strict JSON validator. SHA-256 identities were:

- wheel: `a80212ae52f60681e2ffef5501242b5c929b08b12e3982943a06c3bb5635ceb4`
- source distribution: `d3bd7ceeb58c323963f33f3202ca55591d2def2c9f620e637ab639c73cb29e01`
- release notes: `2e397c0a679ca0a8bd3f569c61ec601ae3fa50ce0eab584e39ec1d47e8364a4c`
- CycloneDX SBOM: `f9ed68307dc9420690f7b31ae4bf699cfe5ed2d7d2777908f3d597de470cb156`
- candidate manifest: `71328fad2abee3eeb9a24020cb9d6f245b6d2effb7fefe6b54e342a6be54c63f`

The SBOM root was `solodeveling-protocol` 0.1.0 and contained the resolved runtime
graph for PyYAML, jsonschema, attrs, jsonschema-specifications, referencing, and
rpds-py. It contained no pip, build, wheel, setuptools, or cyclonedx-bom component.
Installing the exact wheel and dependencies in a fresh environment passed every
installed command and runtime-adapter smoke. pip-audit 2.10.1 found no known
vulnerabilities in the auditable dependencies.

## Security and recovery evidence

Ordinary push and pull-request CI retains only `contents: read`. OIDC and attestation
permissions exist only in a manual workflow with no push or pull-request trigger,
full-SHA action pins, an exact source-revision input, and no publication action. The
candidate builder rejects a mutable or mismatched revision, dirty worktree, existing
output, unsafe evidence paths, duplicate filenames, build-tool-contaminated SBOM,
conflicting project version, incomplete inventory, and changed hashes or sizes.
Failure leaves only disposable paths under `C:\tmp`; no tag, release, attestation,
environment, registry, canonical skill, or user runtime path is changed.