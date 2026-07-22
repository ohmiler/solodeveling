---
solodeveling_schema: 1
id: EVIDENCE-044
work_item: WORK-044
claim: Public GitHub, PyPI, and npm 0.3.0 bind exact candidate SHA
  1bdfadd137c30f64b4d6308fe49975e81988644d and pass scoped post-publication checks.
method: Protected merge and CI; candidate assembly and independent verification;
  immutable release verification; protected OIDC publication; npm staged owner
  review; registry digest and provenance inspection; isolated installation smoke.
command: PR 50; candidate run 29927763248; publish run 29931781583; gh release and
  attestation verification; PyPI Integrity API and pypi-attestations; pip install;
  uvx; npm view and attestations API; clean-cache npx.
result: accepted-gap
scope: Solodeveling 0.3.0 public release, candidate SHA
  1bdfadd137c30f64b4d6308fe49975e81988644d, and Windows post-publication smoke.
limitations:
- The owner accepted missing live routing evidence for this exact public release;
  tenant policy prevented the three calls, so runtime semantic routing is unverified.
- Native executables remain unsigned and Tier 1 remains unverified.
- Fresh executable smoke ran on Windows; CI built and smoked all six native targets.
- pipx was unavailable locally and did not run.
---
# Evidence

| Criterion | Result | Evidence | Limitation |
| --- | --- | --- | --- |
| Exact candidate | Passed | PR 50 and main CI passed; run 29927763248 assembled and attested 11 payload artifacts plus manifest and checksums from the exact SHA | No platform signing |
| GitHub release | Passed | Annotated v0.3.0 resolves to the candidate; release is immutable, non-draft, and all 13 remote asset digests/attestations verify | GitHub integrity is bounded provenance evidence |
| PyPI | Passed | Run 29931781583 uploaded the exact wheel and sdist with OIDC; public SHA-256 values match the release; Integrity API identifies ohmiler/solodeveling, publish.yml, and pypi; offline pypi-attestations verification passed for both files | Initial online verifier hit Windows symlink privilege limits before a controlled local-file offline verification passed |
| npm | Passed | Stage 3860fd61-a8a4-473b-8eb4-1693eebe3cb9 was owner-approved; public latest is 0.3.0; integrity and SHA-1 match the staged tarball; provenance identifies publish.yml, main, npm, and the exact SHA | Approval required owner 2FA outside agent access |
| Clean install | Passed | New no-cache Python venv, isolated uvx cache, and clean npm/native caches each report 0.3.0; downloaded Windows x64 SHA-256 is 829b94816e829e8c873d8067fc7a1cc6187ce34ae56a52220973db194a2e769b | pipx unavailable |

The 30-call comparison did not run and no performance or comparative quality claim is
supported. Corrections require a newly reviewed version rather than replacing bytes.
