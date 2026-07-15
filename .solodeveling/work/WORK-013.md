---
solodeveling_schema: 1
id: WORK-013
title: Reconcile pre-release readiness
status: verifying
level: standard
type: change
goal: Make release documentation and project memory accurately describe the reviewed main revision and the remaining owner-controlled 0.1.0 release gates.
scope: Remove completed merge gates, record the current main and CI evidence, distinguish source readiness from public registry availability, and identify the next explicit authorization checkpoint.
out_of_scope: Creating environments, configuring registries or trusted publishers, invoking a candidate workflow, creating a tag or GitHub Release, signing binaries, or publishing npm or PyPI packages.
acceptance:
- Release readiness and roadmap contain no pending merge claims for work already merged into main.
- Project state identifies the current reviewed main revision and recent successful CI without claiming registry or release availability.
- Remaining release gates retain separate authorization boundaries for GitHub settings, candidate creation, tag, release, and registry publication.
- Project memory validation, documentation policy checks, and diff review pass.
risks:
- Stale readiness text could cause an operator to repeat completed work or skip an uncompleted release gate.
- Overstating readiness could imply that npx or pip installation works before registry publication.
decisions:
- Treat the current source as ready for release preparation, not publicly released.
- Keep every production-changing release action outside this work item.
verification:
- Validate Solodeveling project memory and canonical skill suite.
- Run release/documentation policy tests and inspect all changed text and whitespace.
next_action: Submit the verified documentation reconciliation for pull-request CI; remain in verifying until that CI passes.
security_considerations:
- Preserve least-privilege and trusted-publication requirements without recording credentials or secret values.
recovery:
- Revert this documentation-only change if it misstates repository or registry state; no external release state changes in this work item.
evidence:
- EVIDENCE-013
---
# Implementation plan

1. Reconcile completed work and exact main/CI identity in project memory.
2. Remove stale merge gates while preserving all uncompleted release controls.
3. Validate memory, release policy, skill packaging, and the final diff.
4. Record bounded evidence and archive the work item without invoking release workflows.
