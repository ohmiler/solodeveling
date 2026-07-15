---
solodeveling_schema: 1
id: EVIDENCE-013
work_item: WORK-013
claim: Pre-release documentation and project memory accurately distinguish reviewed source readiness from unavailable public registry installation while preserving separate authorization gates for every production-changing release action.
method: GitHub pull request, release, tag, and workflow inspection; direct npm and PyPI registry lookups; project-memory and skill-suite validation; focused release/documentation policy tests; full Python and Node regressions; compilation, dependency health, and diff review.
command: gh pr view 8..12; gh release list; git tag --list; npm view solodeveling version --json; PyPI JSON endpoint lookup; python -m pytest -q; npm test --prefix packages/npm; python -m compileall -q src tests scripts; python -m pip check; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.main_cli validate .; git diff --check.
result: passed
scope: WORK-008 through WORK-012 merge status, reviewed main and CI identity, current npm/PyPI availability, tag and GitHub Release absence, remaining protected-environment and publication gates, roadmap, release-readiness documentation, and project state.
limitations:
- npm and PyPI availability is time-sensitive and must be rechecked immediately before publication.
- Pull-request GitHub Actions for WORK-013 are pending; this evidence currently binds the local verification only.
- No candidate workflow, protected environment, registry configuration, tag, GitHub Release, attestation, staging action, approval, or publication was invoked.
- Cursor live behavior, complete Tier 1 evaluation, and native platform signing remain unverified.
---
# Evidence

## Verified facts

- GitHub reports pull requests 8 through 12 as merged. The inspected pre-release base
  was `main` commit `cda0f4854359384f79ea45c50a8ad06f9eba6baf`, whose push run
  29442409991 completed successfully.
- The repository had no version tag or GitHub Release. npm and PyPI returned not
  found for `solodeveling` on 2026-07-16, so public registry installation was not
  claimed.
- Release readiness now removes the completed WORK-011 merge gate and preserves
  explicit authorization boundaries for GitHub settings, candidate creation, tag,
  release, registry setup, staging, approval, and publication.
- Roadmap and state now account for WORK-008 through WORK-012 without implying that
  guarded workflows have been invoked.

## Local verification

- Focused release, release-set, and installation documentation tests: 22 passed.
- Full Python suite: 203 passed.
- Node launcher suite: 8 passed and 1 skipped because file symlinks were unavailable
  in the local Windows environment.
- Compilation, dependency health, canonical skill-suite validation, project-memory
  validation, and diff whitespace review passed.

## Boundary

This evidence supports documentation reconciliation and readiness for the next
owner-controlled preparation decision only. It is not release, registry,
provenance, signing, security-certification, or cross-runtime Tier 1 evidence.