---
name: solodeveling-planning-work
description: Convert a shaped Solodeveling work item into a proportional, independently reviewable implementation and verification plan. Use when the user requests a plan, execution is not authorized yet, or material sequencing, boundary, security, migration, or recovery choices must be resolved before implementation. Skip clear authorized Standard mutations that can use solodeveling-standard-delivery.
---

# Planning Work

Plan for one primary agent. Base the plan on inspected code, project conventions,
current dependency versions, and available capabilities; do not plan from filenames
or framework memory alone.

## Choose proportional depth

- Quick: write the smallest useful plan: intended edit, one verification method, and
  rollback only if it is not obvious. Do not create ceremony for a reversible change.
- Standard: identify affected components and interfaces, ordered implementation
  slices, tests for each behavior, final verification, documentation or migration
  effects, and meaningful rollback. Store this concise plan in the existing WORK
  item; do not create a separate plan artifact unless complexity requires independent
  review.
- Critical: include threat or abuse cases, security controls, sensitive-data impact,
  migration safety, staged verification, recovery and rollback, and authorization
  checkpoints before irreversible or production effects. Reuse one attack-surface
  matrix in WORK; do not restate the same actors, risks, controls, tests, and recovery
  in separate planning and security artifacts.

## Build the plan

1. Confirm the shaped goal, scope, out of scope, acceptance criteria, level, risks,
   and decisions. Return to shaping if any material boundary is unresolved.
2. Inspect relevant implementation and tests. Name paths or components only after
   discovery; preserve user changes and established sources of truth.
3. Split work into independently verifiable slices. For behavior changes, begin with
   a failing regression where practical. Separate focused per-slice checks from broad
   checkpoint gates. Include exact non-interactive commands only when confirmed.
4. Map every acceptance criterion to planned verification. Label checks that cannot
   run in the current environment rather than assuming they will pass.
5. Include security and recovery whenever triggers or irreversible effects apply.
   Do not hide them in a generic final checklist.
6. Record dependencies, decision points, risks, and the next executable action.

Mark the work item `ready` only when another session can execute the plan without
recovering missing intent or making an unapproved material decision. Store concise
steps in the work item or a linked project plan; do not copy source code into it.
