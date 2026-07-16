---
solodeveling_schema: 1
id: EVIDENCE-028
work_item: WORK-028
claim: Solodeveling 0.1.1 is an exact, immutable, provenance-backed patch release whose npm and PyPI landing content is current and whose public Python and Node installation paths pass clean first-run verification.
method: Correct registry-facing source content and version metadata; add packaging and CI regressions; run local and protected-main verification; create one explicitly authorized source-bound candidate; independently verify its complete release set and attestations; create an explicitly authorized immutable GitHub Release; publish through protected PyPI OIDC and npm staged Trusted Publishing; approve the exact staged npm bytes with owner 2FA; and run clean registry smoke tests.
command: python -m pytest -q; npm test --prefix packages/npm; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python scripts/verify_release_set.py; gh attestation verify for 13 subjects; gh release verify and verify-asset for 13 assets; GitHub runs 29498213788, 29498362312, 29498802715, and 29499788127; PyPI JSON and no-cache pip install; npm stage view/download; npm view/pack; clean npx version/install/check
result: passed
scope: Version 0.1.1 source and package metadata, registry-facing README content, dynamic npm CI smoke paths, Python/npm/native release inventory, complete 13-file GitHub Release, PyPI publication, npm staged publication and owner approval, registry digests and provenance, and clean first-run behavior.
limitations:
- Native executables remain unsigned; the npm launcher verifies exact versioned sizes and SHA-256 values but does not provide platform code signing.
- Tier 1 remains unverified; Codex and Claude Code retain one bounded live scenario each and Cursor retains structural evidence only.
- No controlled cross-framework speed or quality benchmark was run; public comparisons remain limited to documented defaults and measured local workflow overhead.
- npm staged approval required owner proof-of-presence in npmjs.com; registry identity, digests, provenance, and post-approval behavior were then independently verified.
---

# Results

- Pull request 31 merged the reviewed source through full run 29498213788. Post-merge
  main run 29498362312 passed Python 3.10 and 3.14 across Windows, Ubuntu, and macOS,
  package verification, all six native builds and smokes, and npm pack/npx smoke.
- Exact candidate run 29498802715 used source commit
  889e07a47a8cbdca15765d00348dbbd7f9849f03. Its 13-file release set passed manifest,
  checksum, inventory, wheel-description, npm-README, six-target npm-manifest, and
  strict attestation verification for every subject.
- Annotated tag v0.1.1 peels to the exact candidate source. GitHub Release v0.1.1 is
  non-draft, non-prerelease, immutable, and contains all 13 verified assets. GitHub
  release verification and per-asset comparison against the candidate set passed.
- Protected publication run 29499788127 reverified the immutable release and exact
  candidate. PyPI published through OIDC; npm staged through stage-only Trusted
  Publishing and skipped the direct-publish step.
- PyPI exposes version 0.1.1 with two files. The wheel SHA-256 is
  2fde58b59382340228a7386f0ef5a4ce8edafc697a9de01f23b3beee92a61bb5 and the source
  distribution SHA-256 is
  8adaffbf60697ff9206f8ab7d57c8077f8813059a59eb833167be61d4ad3f3ce; both match the
  immutable release. Its long description contains the corrected positioning.
- npm staged ID b392e261-12d3-4390-aa42-76bcbe081751 identified
  solodeveling@0.1.1, public access, latest tag, and GitHub Actions trusted automation.
  The downloaded staged tarball SHA-256
  98de3300acd465c8e6dd55906a7d820dfae2c008040f97a24879ac82b9c2dd62 matched the
  immutable release before owner approval.
- Public npm integrity is
  sha512-HfeImrNK8UhCZLVRDq9Y97vPaXLNuBxWyBoPT84rgfEEdHsITf1g+QTlcugnYVEi6uvH15H9bxQrBuhG75Zm5A==
  and shasum 242c2580465233366e1070327f192d1012f126f5. The public tarball remains
  byte-identical to the verified release asset and exposes SLSA provenance.
- A no-cache PyPI installation and a clean-cache public npx invocation each reported
  solodeveling 0.1.1, installed 31 managed files into a temporary project, and passed
  solodeveling check. Python dependency health also passed.
- Immutable 0.1.0 registry and GitHub Release objects were not modified or replaced.
