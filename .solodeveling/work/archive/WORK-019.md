---
solodeveling_schema: 1
id: WORK-019
title: Memory Workflow Simplification
status: done
level: standard
type: change
goal: Make small Solodeveling tasks feel immediate while preserving durable continuity, verification, and sensitive boundaries when they are actually needed.
scope: Define an ephemeral Quick path, compact current-state policy, active/deferred loading rules, event-driven memory validation, impact-based verification, measurable routing scenarios, and a fail-safe memory-only CI path.
out_of_scope: npm publication, release workflow consolidation, a CLI workflow engine, schema migration, GitHub branch-protection changes, and any change to candidate 0.1.0 or its verified release set.
acceptance:
- A one-session local reversible Quick task with no durable or sensitive boundary requires no WORK, EVIDENCE, state, or roadmap write while still receiving focused verification.
- Cross-session work and durable decisions persist a compact work item; Standard, Critical, security, release, migration, and production work retain lifecycle evidence and authorization boundaries.
- The core router reads only current active work, excludes deferred work from active_work, keeps state as a compact current dashboard, and validates memory only on a relevant event or suspicion.
- Verification depth scales from focused Quick checks through affected Standard regression to broad Critical gates, with failures escalating rather than being hidden.
- Behavioral scenarios cover Quick fast-path metrics and escalation cases for resumable, dependency or security, production, and failed-verification work.
- CI runs a focused memory validation path only when every changed file is under .solodeveling, otherwise falls back to the full gate; feature branches do not run duplicate push and pull-request workflows.
- No part of this work changes candidate 0.1.0 or its verified release set.
risks:
- Premature simplification could remove continuity or verification information needed for safe resumptions.
- Incorrect CI path classification could skip tests for runtime or packaged skill behavior.
- Over-broad Quick classification could bypass durable security or authorization context.
decisions:
- Record only what a later session needs; do not record every task by default.
- Keep the ephemeral Quick fast path in the core skill and load specialized workflows only on a genuine boundary or escalation.
- Treat only .solodeveling/** as memory-only CI; skills/** remains product behavior and always receives the full gate.
- Make ambiguous CI classification fail safe to the full gate.
- Keep branch-protection terminology or configuration correction separate from this performance work.
- Preserve candidate 0.1.0 identity at 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
verification:
- Run focused routing, lifecycle, skill-suite, project-memory, and CI-policy regressions.
- Validate canonical skills and project memory from source.
- Run the applicable full Python regression gate after focused checks pass.
next_action: Use the simplified workflow on the next real small task and observe the first remote CI run.
security_considerations:
- Retain secret-handling, authorization-boundary, and evidence requirements while simplifying the workflow.
recovery:
- Revert the protocol and CI routing together if regression evidence shows lost continuity, verification, or authorization boundaries.
evidence:
- EVIDENCE-019
---

# Implementation plan

1. Add behavioral scenarios and CI-policy tests that express the fast path, escalation,
   active/deferred loading, validation events, and fail-safe classification.
2. Update the core protocol and lifecycle skills without changing schema or adding a
   workflow CLI.
3. Compact current state and ensure only genuinely active work is referenced.
4. Route memory-only pull requests and main pushes through one focused job; retain the
   full matrix for every other path.
5. Run focused checks, the full local regression gate, skill validation, and memory
   validation before reconciling evidence.
