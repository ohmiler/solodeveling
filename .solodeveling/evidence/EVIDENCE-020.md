---
solodeveling_schema: 1
id: EVIDENCE-020
work_item: WORK-020
claim: GitHub Release v0.1.0 is non-draft, immutable, bound through the existing tag to the exact verified candidate commit, and contains exactly the 13 independently verified release-set files without invoking registry publication.
method: Candidate artifact API inspection and download, independent release-set verification, strict per-file provenance verification, one-time GitHub Release creation from the existing tag, GitHub immutable-release verification, per-asset digest verification, and publication-run inspection.
command: gh run download 29452526223; python scripts/verify_release_set.py; gh attestation verify for 13 files; gh release create v0.1.0 with 13 files and verify-tag; gh release view/verify/verify-asset; gh run list for publish.yml.
result: passed
scope: Candidate artifact 8358101583, source commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4, tag v0.1.0, GitHub Release v0.1.0, and its 13 assets.
limitations:
- No PyPI or npm registry action, protected-environment approval, OIDC exchange, staging, bootstrap, or publication was invoked.
- Native executables remain unsigned by platform-specific code-signing identities, and provenance does not establish categorical safety or a SLSA level.
---

# Evidence

## Release input

- Artifact 8358101583 from candidate run 29452526223 was available and unexpired
  with archive digest
  sha256:f9a7d408a0527a224570204bde62369fb906c5940798dae39d42a8350881e53b.
- The downloaded set contained exactly 13 expected files and passed
  verify_release_set.py for source revision
  700a9b9dafc877507232b84a94ff3d6eaf7afda4.
- Strict GitHub attestation verification passed separately for every file against
  repository ohmiler/solodeveling, release-candidate.yml, refs/heads/main, the exact
  source digest, and denial of self-hosted runners.

## Immutable GitHub Release

- GitHub Release v0.1.0 was created once from the existing verified tag with title
  Solodeveling 0.1.0 and the candidate release notes.
- GitHub reported isDraft false, isImmutable true, and publication timestamp
  2026-07-16T09:04:21Z.
- GitHub release verification passed and all 13 local verified files passed
  gh release verify-asset against the published release.
- The release URL is
  https://github.com/ohmiler/solodeveling/releases/tag/v0.1.0.

## Authorization boundary

No publish workflow run, registry approval, token exchange, PyPI action, npm
bootstrap, npm staging, or registry publication was invoked.
