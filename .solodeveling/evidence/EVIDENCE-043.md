---
solodeveling_schema: 1
id: EVIDENCE-043
work_item: WORK-043
claim: Solodeveling 0.3.0 source revision d0e9bcbaef88b301561fe4f6a530e0897378b2c9
  produced a verified local Python candidate and smoke-tested Windows x64 native
  executable; missing live routing evidence remains an owner-accepted local-only gap.
method: Preregister and offline-check three routing scenarios; record the tenant
  policy denial; apply the bounded owner acceptance; align version surfaces and
  release notes; run exact-source Python, npm, compile, dependency, skill, and
  protocol gates; build and verify Python/SBOM artifacts; install the wheel in a
  fresh environment; build and smoke the current-platform native executable.
command: python -m pytest -q; python scripts/validate_skill_suite.py; python -m
  solodeveling_protocol.cli .; npm test --prefix packages/npm; python -m compileall
  -q src scripts; python -m pip check; build_candidate.py and verify_candidate.py at
  source d0e9bcb; smoke_installed.py; build_native.py; smoke_native.py.
result: accepted-gap
scope: Local Solodeveling 0.3.0 Python candidate and Windows x64 native candidate
  bound to source revision d0e9bcbaef88b301561fe4f6a530e0897378b2c9.
limitations:
- The owner supplied informed approval, but tenant policy still forbids sending
  private-workspace skill and scenario text externally from this environment.
- Owner acceptance applies only through local candidate inspection and expires before
  any tag, GitHub Release, registry publication, or public readiness claim.
- Cross-platform native builds, npm release tarball, complete release set, CI
  attestations, platform signing, and post-publication checks did not run.
---
# Evidence

| AC | Result | Evidence | Limitation |
| --- | --- | --- | --- |
| AC1 | Passed | Three versioned scenarios; deterministic route expectations; 35 evaluation tests | Scenarios are self-authored |
| AC2 | Accepted gap | Codex CLI 0.145.0 available; exactly three read-only calls in dry-run; owner accepted missing live evidence for local candidate construction | No live call or semantic result; acceptance expires before public release |
| AC3 | Passed | Python, npm, artifacts, native naming, current-version tests, and release notes agree on 0.3.0; pinned comparison remains 0.2.0 | No public release |
| AC4 | Passed | Exact clean revision: 281 pytest; skill/protocol; npm 8 passed and 1 Windows symlink skip; compile/pip; candidate, fresh-wheel, and Windows native smoke | Other five native targets and complete release set require CI |
| AC5 | Passed | Candidate manifest and hashes below; no external release action occurred | Live routing and public-release gates remain open |

## Observation log

- A second live invocation after exact informed approval was denied by tenant policy.
  The policy explicitly forbids this external transmission from the current
  environment even with user approval. No runtime output or result file was created.

## Candidate identity

- Version: 0.3.0
- Source: d0e9bcbaef88b301561fe4f6a530e0897378b2c9
- Python wheel SHA-256: e8898b324edf33978e01905396702d1841f892cc21c1b281f509ddacd4b41f67
- Python sdist SHA-256: 8bc9ae2cec4e9e7e0dedaa7be21f466e3484ee76a89a3242cb3cc824db060c0e
- CycloneDX SBOM SHA-256: 435930da6bbfd847d9085541a3193786bdfc002ed0181ee973efc54db24563f0
- Windows x64 native SHA-256: cab76a3c49af00beef50fcbfa2e5549aebfdcb46bcae51295a807ad765e4957f
- Local candidate directory: C:/tmp/solodeveling-candidate-0.3.0-d0e9bcb
- Local native directory: C:/tmp/solodeveling-native-0.3.0-d0e9bcb
