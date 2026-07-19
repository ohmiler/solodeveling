---
name: solodeveling-verifying
description: Verify implemented Solodeveling work against every acceptance criterion and bind completion claims to recent, scoped evidence. Use before saying work is done, fixed, passing, secure, ready, or releasable; after implementation or debugging; and whenever a prior verification failed or capabilities are missing.
---

# Verifying

Verification is the only path from `verifying` to `done`. Evidence must be recent,
reproducible where possible, and collected after the latest relevant change.

## Build the evidence matrix

1. Re-read the current requirement, decisions, implementation diff, and project
   Definition of Done. For tracked work, keep one Current acceptance matrix at the
   top of cumulative evidence. Mark replaced requirements `Superseded by ...` rather
   than appending a conflicting full matrix. Surface conflicts before testing.
2. Map every current acceptance criterion to a method: automated test, build or lint,
   reproducible manual check, static inspection, inference, or accepted gap.
3. Match depth to impact and checkpoint. Quick runs at least one focused check.
   Standard slices run the affected regression and focused checks, then run relevant broad gates once at commit,
   handoff, changed boundary, or closure. Critical runs applicable broad gates with
   security and recovery coverage. Reuse a broad result until a later change crosses
   what it covered. Inspect exit status and meaningful output; invocation alone is
   not evidence.
4. Check scope integrity, unintended changes, documentation, migration, UX,
   compatibility, security, privacy, operations, and recovery when applicable.
5. For persistent work, record each claim, method or command, result, scope,
   limitations, and important invariant proved. Keep follow-up history as a short
   changelog below the current matrix. Ephemeral Quick reports the focused result
   inline and creates no artifact. Mark unavailable or unexecuted checks `unverified`;
   never present them as passing.

For external providers, accept code-level mocks, signature fixtures, retry,
idempotency, and failure tests as implementation evidence. Keep owner-controlled
target-environment smoke checks as release evidence; do not block code completion on
production credentials when deployment is outside scope.

## Decide

If any acceptance criterion fails, lacks evidence, or has an unaccepted gap, the item
must not transition to done. If Ephemeral Quick verification fails, leave the fast
path and classify the resulting repair. Return tracked work to `active` with the
failure, impact, known facts, and next action, or mark it `blocked` when progress truly
cannot continue.

Transition to `done` only at a real checkpoint and when every criterion has recent evidence or an explicitly
accepted verification gap, applicable project checks pass, and state, work item,
source, decisions, and evidence agree. Critical work also requires recorded security
and recovery consideration. Archive the item and update current state. Update roadmap
only when priority, milestone, ordering, or a deferred-work decision changed. Combine
Standard closure memory with its delivery change when possible; do not create one
commit per transition. Report limitations alongside the bounded completion claim.
