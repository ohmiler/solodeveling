---
solodeveling_schema: 1
id: EVIDENCE-010
work_item: WORK-010
claim: Solodeveling can assemble and fail-closed verify one deterministic non-publishing release set that binds Python distributions, six native executables, an npm package, SBOM, and release notes to one exact source revision, with a manually dispatched least-privilege attestation workflow.
method: Focused adversarial release-set tests, full Python and Node regression, official and project skill validation, protocol validation, compilation, dependency health, workflow YAML and policy inspection, diff review, and two cross-platform GitHub Actions CI runs.
command: python -m pytest -q; npm test --prefix packages/npm; python scripts/validate_skill_suite.py; official quick_validate.py for ten skills; python -m solodeveling_protocol.cli .; python -m compileall -q src tests scripts; python -m pip check; workflow YAML parse; git diff --check; GitHub Actions runs 29436818797 and 29436838206.
result: passed
scope: Release-set assembly and verification, Python candidate identity, six native target inventory, npm archive and native-manifest binding, SBOM and notes, source/version/digest containment, manual workflow permissions and non-publishing boundary, documentation, security controls, and recovery.
limitations:
- The manual complete-release-set workflow was not invoked, so no final release set or attestation was created.
- Native executables are not platform-signed or attached to a GitHub Release.
- npm and PyPI identities and protected Trusted Publisher environments remain unconfigured and time-sensitive.
- No tag, GitHub Release, registry publication, or downstream public-install observation occurred.
- Cursor and the complete Tier 1 behavioral matrix remain unverified.
---
# Evidence

## Claims and results

- Complete release-set assembly is deterministic and binds one exact lowercase Git SHA, package version, two Python distributions, six native executables, one npm tarball, CycloneDX SBOM, and release notes. Focused fixture assembly and verification passed.
- The verifier fails closed for incomplete/extra native inventory, npm/native digest drift, npm archive links and path traversal, unsafe or invalid source revisions, extra output files, size/hash changes, version/role filename drift, and malformed inventories. Twelve focused release-set tests passed.
- Assembly validates inputs before copying, rechecks expected size and SHA-256 after copying into a disposable staging directory, verifies the staged set, and only then atomically promotes it. Static code review and focused tests passed.
- The manual workflow accepts only an exact commit SHA, checks out the same revision in every job, builds/smokes six native targets, builds/verifies the Python candidate, packs and locally exercises npm, assembles the final set, attests exact subjects, and uploads temporary artifacts. Workflow YAML and bounded-policy regression checks passed.
- Workflow permissions remain `contents: read` globally; only the final assembly job receives `id-token: write` and `attestations: write`. No contents/package write, environment, tag, GitHub Release, registry configuration, or publish command exists. Static policy regression passed.
- Documentation distinguishes bounded integrity/provenance preparation from signing, publication, categorical security, SLSA level, and Tier 1 behavior, and requires whole-set rebuild recovery. Documentation regression passed.

## Verification performed

- `python -m pytest -q`: 190 passed after the final relevant change.
- `npm test --prefix packages/npm`: 8 passed, 1 skipped locally because Windows did not permit file symlinks; GitHub Ubuntu CI exercised the symlink case successfully as part of passing runs.
- `python scripts/validate_skill_suite.py`: canonical suite valid.
- Official skill-creator `quick_validate.py`: all ten skill directories valid.
- `python -m solodeveling_protocol.cli .`: protocol validation passed.
- `python -m compileall -q src tests scripts`: passed.
- `python -m pip check`: no broken requirements.
- All GitHub workflow YAML parsed successfully; `git diff --check` passed.
- GitHub Actions push run 29436818797: success across Python/package, six native targets, and npm-package.
- GitHub Actions pull-request run 29436838206: success across the same matrix.

## Security and recovery

- npm archives are inspected without extraction and reject duplicate names, non-canonical trust-boundary paths, links, special files, oversized members, missing identity metadata, and native manifest drift.
- Flat artifact names, exact inventories, symlink rejection, size and SHA-256 recomputation, version binding, role binding, and immutable source revision constrain artifact mixing and filesystem traversal.
- Hashes and manifests provide integrity evidence, not authenticity or safety. The optional GitHub attestation step does not sign native executables or establish a SLSA level by itself.
- Recovery before publication is to delete only disposable output and rebuild the entire set from the reviewed exact commit. Generated manifests and individual artifacts must not be repaired or replaced in place.

## Limitations

- `.github/workflows/release-candidate.yml` was not manually invoked in WORK-010. No complete release set or attestation was created; only implementation, fixture behavior, ordinary CI, and static workflow policy were verified.
- Native executables are not platform-signed and are not attached to a GitHub Release.
- npm/PyPI names, protected environments, and Trusted Publishers remain unconfigured and time-sensitive.
- No tag, GitHub Release, registry publication, or downstream public-install observation occurred.
- Cursor and the complete Tier 1 behavioral matrix remain unverified.