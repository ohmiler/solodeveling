---
name: solodeveling-standard-delivery
description: Deliver a clear, authorized, non-Critical Solodeveling Standard change end to end with one primary agent and one WORK/EVIDENCE pair. Use when scope and acceptance are discoverable without a material user decision and the work can proceed through shape, plan, execute, and verify in one workflow. Do not use for diagnosis-only, verification-only, security, release, production, destructive, sensitive-boundary, or materially ambiguous requests; route those to the specialized workflow.
---

# Standard Delivery

Deliver clear Standard work without loading a lifecycle skill for every phase. Read
the [core protocol](../solodeveling/references/protocol.md) once, then keep this skill
active through verified closure unless a genuine boundary appears.

For a backend change, read the [backend delivery contract](../solodeveling/references/backend-delivery.md)
once. If every Quick carve-out condition is true, exit to the Ephemeral direct loop
before creating WORK or EVIDENCE; otherwise keep the Standard path.

## Enter the combined path

1. Confirm mutation authority, Standard impact, discoverable scope, observable
   acceptance, and no material product, architecture, safety, or authority question.
2. Read state, referenced active work, relevant source and standards, and Git status.
   Preserve user changes and do not reopen unrelated or archived work.
3. Route unresolved scope or acceptance to shaping, an independently reviewed plan
   to planning, a reproducible defect to debugging, and a verification-only audit or
   Critical final gate to verifying. Route security, release, production,
   destructive, and sensitive effects to their specialized workflows.

## Keep one compact contract

- Own one WORK item and one cumulative EVIDENCE file. A Standard WORK item normally
  targets roughly 30–40 lines, but required risk or recovery context takes priority.
- Keep intent, scope and out of scope, acceptance with its verification method,
  material risks and decisions, next action, and confirmed commands. Do not repeat
  the same content as both an implementation plan and a verification mapping.
- Keep EVIDENCE as a short current `AC -> result -> evidence -> limitation` table.
  Add observations only for a material failure, decision, or limitation; do not
  narrate routine execution.

## Shape, plan, execute, and verify

1. **Shape:** Inspect current behavior; state the outcome and users; bound scope;
   write verifiable acceptance; classify effects and material risks; choose the
   smallest credible approach. Stop only for a material unknown.
2. **Plan:** Identify affected boundaries and the smallest ordered slices. Attach a
   focused check to each behavior and broad gates to the real checkpoint. Confirm
   non-interactive commands from the repository.
3. **Activate:** Persist `active` once before the first implementation edit. During
   an uninterrupted session, keep `shaped`, `ready`, and `verifying` semantic rather
   than writing each transition.
4. **Execute:** Make one coherent slice at a time, add a failing regression when
   practical, run its focused check, inspect the result, and preserve unrelated work.
5. **Verify:** Reconcile every acceptance criterion with recent evidence after the
   last relevant change. Run affected broad gates once at closure and record honest
   limitations. Never claim completion from implementation alone.
6. **Close:** When all criteria pass or have an explicitly accepted gap, write the
   final evidence, persist `done`, and archive once in one coherent checkpoint.

Persist `captured`, `shaped`, `ready`, or `verifying` only when work must cross a
session, is blocked, needs handoff, changes scope or risk, or the user requests a
checkpoint. Record the exact next action whenever persistence is necessary.

## Reuse evidence and triage failures

- Reuse a current result until a later change crosses the file, behavior,
  dependency, environment, or boundary it covered. Do not repeat an E2E path merely
  to collect the same responsive or overflow proof manually.
- Use manual browser review for gaps automation does not prove, such as hierarchy,
  visual balance, computed color, hover, and focus. Browser screenshots, traces, and
  videos are transient by default; record the observed result, not an ephemeral
  path. Persist an artifact only when acceptance or review explicitly needs it and
  place it in a deliberate project-owned location.
- On a plausible transient verification failure, inspect exit status, logs,
  screenshots, and environment first. Without editing source, rerun once under one
  controlled condition such as a warmed server or reduced concurrency. Continue
  only when evidence isolates a transient harness or environment cause and record
  the limitation; otherwise route the reproducible or unexplained failure to
  debugging.
