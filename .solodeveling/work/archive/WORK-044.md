---
solodeveling_schema: 1
id: WORK-044
title: Publish and verify Solodeveling 0.3.0
status: done
level: critical
type: release
goal: Publish the exact verified 0.3.0 candidate through immutable GitHub, protected
  PyPI OIDC, and owner-approved npm staging, then prove clean installation.
scope: Main merge, candidate workflow, independent release-set verification, explicit
  live-routing risk acceptance, annotated tag, immutable GitHub Release, protected
  PyPI publication, npm staging and owner approval, provenance checks, and clean
  pip, uvx, and npx smoke tests.
out_of_scope: The 30-call comparison, new source behavior, platform code signing,
  Tier 1 claims, credential handling, release-byte replacement, or another version.
acceptance:
- The complete 13-file release set is built from exact SHA
  1bdfadd137c30f64b4d6308fe49975e81988644d and independently verified.
- Tag v0.3.0 and its immutable non-draft GitHub Release bind that exact candidate.
- PyPI wheel/sdist and npm tarball match the release and expose verified provenance.
- npm is staged for owner review before approval and latest then resolves to 0.3.0.
- Clean pip, uvx, and npx paths report 0.3.0 without using the source checkout.
risks:
- Registry and immutable release bytes cannot be replaced in place.
- Native executables remain unsigned.
- Live routing evidence is missing; the owner explicitly accepted this release-level
  gap for this exact source and artifact set on 2026-07-22.
decisions:
- Use only candidate run 29927763248 and the immutable v0.3.0 release set.
- Publish through protected environments with PyPI OIDC and npm staged 2FA review.
- Keep performance, comparative quality, and Tier 1 claims out of the release.
verification:
- Observe PR 50, main CI, candidate run 29927763248, and publish run 29931781583.
- Verify release assets and attestations, public registry metadata and provenance,
  and clean Windows pip, uvx, and npx installation paths.
security_considerations:
- Bind source, workflow, environment, tag, release, assets, registry digests, stage,
  and provenance without recording credentials, OIDC tokens, OTPs, or recovery codes.
recovery:
- Preserve evidence and yank or deprecate an incorrect registry version as
  appropriate; publish corrections only as a newly reviewed version.
next_action: None; archived.
evidence:
- EVIDENCE-044
---
# Authorization

The owner separately authorized merge, candidate invocation, the accepted live-routing
gap, tag and immutable GitHub Release creation, PyPI publication, npm staging, and
then approved npm stage 3860fd61-a8a4-473b-8eb4-1693eebe3cb9 with 2FA.
