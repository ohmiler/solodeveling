---
solodeveling_schema: 1
id: WORK-042
title: Separate verified changes and prepare the 0.3.0 release boundary
status: done
level: standard
type: release
goal: Preserve the completed benchmark and workflow-feedback work as reviewable local
  commits, then record the exact boundary before a 0.3.0 version bump or candidate.
scope: Inspect and separate the verified benchmark harness from the frontend/backend
  workflow changes, create local commits with explicit file lists, preserve raw
  feedback outside Git, and update release readiness with current evidence and the
  remaining pilot decision.
out_of_scope: Live-agent benchmark or routing calls, version bump, clean candidate
  build, push, pull request, tag, GitHub Release, registry publication, signing,
  attestation, and production mutation.
acceptance:
- AC1 — Benchmark harness and WORK/EVIDENCE-038/039 are isolated in one local commit.
- AC2 — Workflow skills, contracts, scenarios, docs, and WORK/EVIDENCE-040/041 are
  isolated in a second local commit.
- AC3 — Raw feedback remains untracked and unchanged; no unrelated path is staged.
- AC4 — Release readiness identifies 0.3.0 as the next feature version and keeps the
  live routing pilot and version bump as explicit later gates.
- AC5 — Scoped and full repository verification pass against the resulting source.
risks:
- README changes describe both changesets and must remain internally consistent.
- Stale 0.2.0 readiness text could be mistaken for the current release state.
- A version bump before routing evidence would hide the remaining product-risk gate.
decisions:
- Keep both README files with the workflow commit instead of staging partial hunks.
- Keep feedback/ untracked and use an exact committed source revision for any future
  candidate.
- Stop before live calls and the version bump because they remain separate decisions.
verification:
- Review staged name/status and diff checks before each commit; run the repository
  test suite, skill-suite validator, protocol validator, and final Git inspection.
next_action: None; archived.
evidence:
- EVIDENCE-042
---
