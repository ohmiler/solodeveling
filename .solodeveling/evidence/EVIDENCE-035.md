---
solodeveling_schema: 1
id: EVIDENCE-035
work_item: WORK-035
claim: GitHub Release v0.1.2 is exact, immutable, complete, independently verified,
  and registry-neutral
method: Annotated tag creation and peeled-SHA verification; exact candidate upload;
  GitHub release state and release attestation verification; per-asset name, size,
  SHA-256, upload-state, and release-attestation comparison; release-note and registry
  boundary checks
command: git tag and ls-remote; gh release create/view/verify/verify-asset; GitHub
  immutable-releases API; local SHA-256 comparison; npm view; pip index versions
result: passed
scope: Annotated tag v0.1.2, immutable non-draft latest GitHub Release, all 13 assets
  from candidate run 29521649767, release notes, and unchanged npm/PyPI registries
limitations:
- Native executables remain unsigned despite exact checksum, candidate provenance,
  and release attestation verification.
- PyPI and npm remain at 0.1.1; no registry publication or staging action was authorized
  or run.
- Tier 1 and controlled cross-framework speed claims remain unverified; Pilot-4 was
  not run.
---
# Evidence

## GitHub Release v0.1.2 is exact, immutable, complete, independently verified, and registry-neutral

- Method: Annotated tag creation and peeled-SHA verification; exact candidate upload; GitHub release state and release attestation verification; per-asset name, size, SHA-256, upload-state, and release-attestation comparison; release-note and registry boundary checks
- Result: passed
- Scope: Annotated tag v0.1.2, immutable non-draft latest GitHub Release, all 13 assets from candidate run 29521649767, release notes, and unchanged npm/PyPI registries
- Command: git tag and ls-remote; gh release create/view/verify/verify-asset; GitHub immutable-releases API; local SHA-256 comparison; npm view; pip index versions
- Limitations:
  - Native executables remain unsigned despite exact checksum, candidate provenance, and release attestation verification.
  - PyPI and npm remain at 0.1.1; no registry publication or staging action was authorized or run.
  - Tier 1 and controlled cross-framework speed claims remain unverified; Pilot-4 was not run.
