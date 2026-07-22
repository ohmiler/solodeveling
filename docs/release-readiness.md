# Release readiness

This document defines the current non-publishing candidate and public-release gates
for Solodeveling. Ordinary CI verifies source, packages, six native targets, and npm
packaging; it does not publish, tag, create a GitHub Release, or mutate a registry.

## Local candidate gate

1. Run the full Python suite, skill-suite validation, protocol validation,
   compilation, dependency checks, Node launcher tests, and diff review.
2. Build the current-platform executable into a new path:

       python scripts/build_native.py C:/tmp/solodeveling-native-0.3.0

3. Exercise embedded templates, schemas, skills, evaluations, and unified commands:

       python scripts/smoke_native.py C:/tmp/solodeveling-native-0.3.0 C:/tmp/native-smoke-0.3.0

4. Build the Python candidate from a clean exact commit and verify its checksums,
   contents, SBOM, release notes, and manifest.
5. Verify that installed wheel and native resources include every canonical skill,
   including `solodeveling-brainstorming`, and run the representative routing
   scenarios against the exact candidate bytes.
6. Review manifests and SHA-256 values. Integrity hashes are not signatures,
   attestations, or proof of publisher identity.

Builders refuse unsafe or existing destinations, require exact inventories, use
temporary staging, and never upload to a registry.

Python 3.10 and 3.14 remain the supported CI bounds. Candidate invocation, tag
creation, GitHub Release creation, environment changes, PyPI publication, npm
staging, and npm publication are each a separate external action and authorization
checkpoint.

## 0.3.0 published status — 2026-07-22

- Exact protected-main source revision
  `1bdfadd137c30f64b4d6308fe49975e81988644d` passed main CI and candidate run
  `29927763248`, including all six native targets and complete release-set assembly.
- Annotated tag `v0.3.0` and the immutable non-draft GitHub Release contain the exact
  13 verified and attested files from that candidate.
- Protected publish run `29931781583` published the matching wheel and sdist to PyPI
  through OIDC and staged the matching npm tarball for owner review. Owner 2FA
  approval published npm stage `3860fd61-a8a4-473b-8eb4-1693eebe3cb9`.
- Public PyPI/npm digests and provenance match the release. Clean no-cache pip,
  isolated uvx, and clean-cache npx report 0.3.0; the downloaded Windows x64 native
  executable matches the release manifest.
- The owner explicitly accepted missing three-call live routing evidence for this
  exact public release after tenant policy prevented execution. The 30-call
  comparison did not run and supports no performance or comparative quality claim.

Tier 1 remains unverified because the complete behavioral matrix has not passed on
Codex, Claude Code, and Cursor. Native executables remain unsigned. Corrections must
use a newly reviewed version; immutable release or registry bytes must not be replaced.

## Post-release follow-up

- Continue representative dogfooding and record escaped regressions or any Critical
  under-classification.
- Keep live-routing, Tier 1, signing, and comparative-evidence limitations visible.
- Do not rerun the preregistered 30-call comparison without exact authorization.

## Complete release-set gate

After all upstream checks pass, assemble the coordinated non-publishing input from
one exact source revision:

    python scripts/assemble_release_set.py <candidate> <native> <npm-tarball> <release-set> --source-revision <sha>
    python scripts/verify_release_set.py <release-set> --source-revision <sha>

`release-set-manifest.json` must describe exactly two Python distributions, six
native executables, one npm tarball, one CycloneDX SBOM, and release notes. The
verifier recomputes size and SHA-256, checks the flat inventory, validates the npm
archive without extraction, and requires its platform manifest to match all six
native bytes. This gate provides bounded integrity and provenance input; it is not
publication, platform signing, or Tier 1 behavior proof.

Recovery before publication is to discard only disposable output and rebuild the
entire set from the reviewed commit. Do not edit a generated manifest or replace an
individual artifact. Candidate invocation, tag creation, GitHub Release creation,
PyPI publication, npm staging, and npm publication remain separate authorization
checkpoints.
