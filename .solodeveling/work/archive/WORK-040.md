---
solodeveling_schema: 1
id: WORK-040
title: Reduce uninterrupted Standard delivery overhead
status: done
level: standard
type: change
goal: Make clear Standard work run through one compact delivery workflow without weakening
  risk routing, evidence, or completion gates.
scope: Add a combined Standard delivery skill; tighten lifecycle persistence, compact
  WORK/EVIDENCE guidance, evidence reuse, failure triage, and browser-artifact policy;
  update routing, scenarios, metadata, documentation, and focused tests.
out_of_scope: Critical, release, production, security-boundary, schema-version, publication,
  commit, push, and changes to managed runtime copies under .agents/.
acceptance:
- AC1 — A clear Standard mutation routes through one skill covering shape, plan, execute,
  and verify; ambiguous, Critical, diagnosis-only, and verification-only work still
  route to specialized skills.
- AC2 — Uninterrupted Standard work persists active once and done/archive once; intermediate
  phases persist only for a session boundary, blocker, handoff, scope/risk change,
  or user checkpoint.
- AC3 — Standard WORK/EVIDENCE guidance is compact and avoids duplicate plans, mappings,
  logs, and transient browser paths while retaining required risk context.
- AC4 — Verification reuses current evidence and triages one plausible transient failure
  before opening a debugging investigation.
- AC5 — Focused workflow tests, full tests, skill validation, protocol validation,
  official skill validation where available, and diff integrity pass.
risks:
- Combined routing could hide ambiguity or Critical boundaries if triggers are broad.
- Over-compression could remove context needed to resume or audit work safely.
decisions:
- Keep specialized workflows for genuine boundaries and standalone invocation.
- Treat line counts as a soft brevity target; required risk and recovery data wins.
- Make browser artifacts transient by default and durable only by explicit need.
verification:
- Add scenarios/tests for combined routing, persistence exceptions, evidence reuse,
  failure triage, and artifact policy; run repository gates after canonical edits.
next_action: None; archived.
evidence:
- EVIDENCE-040
---
