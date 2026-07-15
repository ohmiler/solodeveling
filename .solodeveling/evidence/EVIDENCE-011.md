---
solodeveling_schema: 1
id: EVIDENCE-011
work_item: WORK-011
claim: Solodeveling prepares exact registry upload inputs from one verified release set and defines a manual, environment-gated OIDC publication path that fails closed on source, tag, immutable-release, asset, digest, attestation, permission, or confirmation drift.
method: Adversarial publication-input fixtures, static workflow policy regression, full Python and Node regression, official and project skill validation, protocol validation, compilation, dependency health, workflow YAML parsing, and diff review.
command: python -m pytest -q; npm test --prefix packages/npm; python scripts/validate_skill_suite.py; official quick_validate.py for ten skills; python -m solodeveling_protocol.cli .; python -m compileall -q src tests scripts; python -m pip check; workflow YAML parse; git diff --check.
result: passed
scope: Deterministic publication input selection, plan verification, tamper rejection, exact source/version binding, release-candidate provenance guard, manual publication workflow policy, immutable GitHub Release and asset verification, build attestation identity, protected environments, OIDC-only registry permissions, owner setup documentation, post-publication smoke, and recovery.
limitations:
- The publication workflow was not invoked, so its live GitHub, PyPI, and npm behavior is not yet observed.
- No GitHub registry environment, PyPI pending publisher, npm Trusted Publisher, tag, immutable GitHub Release, release attestation, staged package, or registry publication was created.
- npm 0.1.0 still requires a separately authorized owner-controlled interactive first publication with two-factor authentication.
- GitHub-hosted workflow command compatibility remains subject to the branch CI and later explicitly authorized dry/live release sequence.
- Native executables remain unsigned, and Cursor plus the complete Tier 1 behavioral matrix remain unverified.
---
# Evidence

## Claims and results

- `prepare_publication.py` accepts only a complete verified release set for one lowercase 40-character source revision, selects exactly one wheel, one source distribution, and one npm tarball, preserves SHA-256 and size, writes a deterministic plan, verifies the staged tree, and atomically promotes it. Focused fixture tests passed.
- Preparation and verification reject existing outputs, unsafe names, missing package roles, changed bytes, extra files, source drift, version drift, and malformed inventories. Adversarial regression tests passed.
- `release-candidate.yml` now requires dispatch from `refs/heads/main` and requires the requested source revision to equal `GITHUB_SHA` before producing attestations, preventing a newer workflow identity from attesting an arbitrary older checkout.
- `publish.yml` is manual-only. It requires exact version, source SHA, workflow revision, main ref, typed confirmation, and a non-no-op target; resolves the exact tag; requires a non-draft immutable GitHub Release; verifies the release attestation and every downloaded release asset; verifies release-set structure and build attestations against `ohmiler/solodeveling/.github/workflows/release-candidate.yml` and the exact source SHA.
- Global and validation permissions are read-only. Only the separate `pypi` and `npm` environment jobs receive `id-token: write`. All actions use full commit SHAs; the workflow contains no registry password, long-lived token, contents write, packages write, tag creation, release mutation, or approval automation.
- PyPI uses its official pinned Trusted Publishing action. npm uses Node 24 and npm 11.15.0 with separately guarded skip, staged, and direct publication choices. Documentation recommends stage-only trust after the separate first-package bootstrap.

## Verification performed

- `python -m pytest -q`: 196 passed.
- `npm test --prefix packages/npm`: 8 passed and 1 skipped because file symlinks were unavailable on local Windows.
- `python scripts/validate_skill_suite.py`: canonical suite valid.
- Official skill-creator `quick_validate.py`: all ten skill directories valid.
- `python -m solodeveling_protocol.cli .`: protocol validation passed.
- `python -m compileall -q src tests scripts`: passed.
- `python -m pip check`: no broken requirements.
- Both workflow YAML files parsed; `git diff --check` passed.

## Security and recovery

- Downloaded GitHub Release files remain untrusted until release immutability, release attestation, asset identity, complete-set inventory, size, SHA-256, exact signer workflow, source ref, and source digest all verify.
- Workflow input values are transferred through environment variables and constrained before use; target actions are fixed boolean/choice branches rather than constructed shell commands.
- Registry permissions use short-lived OIDC only behind named protected environments. npm first-package creation is deliberately excluded because staged publishing requires an existing package.
- Before publication, discard disposable output and rebuild the entire set after any mismatch. After an incorrect publication, preserve evidence, stop further releases, yank or deprecate as appropriate, and publish a corrected new version instead of replacing registry bytes.

## Limitations

- This evidence proves local behavior and static workflow policy, not a successful registry operation.
- `publish.yml`, `release-candidate.yml`, tag creation, immutable release creation, environment setup, trusted-publisher setup, npm staging/approval, and publication all remain separate external authorization checkpoints.
- Registry name availability is time-sensitive and no lookup reserves a name.
- Native platform signing and complete Tier 1 multi-agent-runtime behavior remain open.
