---
solodeveling_schema: 1
id: EVIDENCE-034
work_item: WORK-034
claim: Solodeveling 0.1.2 candidate run 29521649767 is exact, complete, provenance-verified,
  smoke-tested, and not published
method: Protected PR and main CI; exact workflow dispatch; independent release-set
  verification; strict per-subject GitHub attestation verification; downloaded wheel,
  native, npm, and source-blob smoke checks
command: PR 40; CI runs 29521154779 and 29521416708; candidate run 29521649767; verify_release_set.py;
  gh attestation verify with repository, signer workflow, signer/source SHA, and main
  ref; downloaded wheel/native/npm version smoke; git blob comparison
result: passed
scope: Version 0.1.2 candidate at SHA 00efc22a01daad1cddb544b4d97ffb6a45b283fc, all
  13 release-set files, six native targets, Python and npm packages, CycloneDX SBOM,
  checksums, notes, manifest, and provenance
limitations:
- Native executables remain unsigned despite exact checksum and provenance verification.
- Tier 1 and controlled cross-framework speed claims remain unverified; Pilot-4 was
  not run.
- No tag, GitHub Release, PyPI, npm staging, or npm publication action occurred.
---
# Evidence

## Solodeveling 0.1.2 source preparation passes the complete local release gate

- Method: Focused and complete regressions, package build and install smoke, Windows native build and smoke, protocol and skill validation
- Result: passed
- Scope: 0.1.2 version metadata, release notes, Python and npm packages, native executable, lifecycle resources, and non-publishing source boundary
- Command: python -m pytest -q; npm.cmd test --prefix packages/npm; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.main_cli validate .; python -m compileall -q src tests scripts; python -m pip check; python -m build; python scripts/build_native.py; python scripts/smoke_native.py
- Limitations:
  - Protected pull-request and main CI have not run for this source change yet.
  - The exact 13-file candidate and GitHub attestations do not exist until after protected-main merge.
  - No tag, GitHub Release, PyPI, or npm action was run.

## Solodeveling 0.1.2 candidate run 29521649767 is exact, complete, provenance-verified, smoke-tested, and not published

- Method: Protected PR and main CI; exact workflow dispatch; independent release-set verification; strict per-subject GitHub attestation verification; downloaded wheel, native, npm, and source-blob smoke checks
- Result: passed
- Scope: Version 0.1.2 candidate at SHA 00efc22a01daad1cddb544b4d97ffb6a45b283fc, all 13 release-set files, six native targets, Python and npm packages, CycloneDX SBOM, checksums, notes, manifest, and provenance
- Command: PR 40; CI runs 29521154779 and 29521416708; candidate run 29521649767; verify_release_set.py; gh attestation verify with repository, signer workflow, signer/source SHA, and main ref; downloaded wheel/native/npm version smoke; git blob comparison
- Limitations:
  - Native executables remain unsigned despite exact checksum and provenance verification.
  - Tier 1 and controlled cross-framework speed claims remain unverified; Pilot-4 was not run.
  - No tag, GitHub Release, PyPI, npm staging, or npm publication action occurred.
