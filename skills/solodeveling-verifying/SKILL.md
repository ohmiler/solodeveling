---
name: solodeveling-verifying
description: Verify implemented Solodeveling work against every acceptance criterion and bind completion claims to recent, scoped evidence. Use before saying work is done, fixed, passing, secure, ready, or releasable; after implementation or debugging; and whenever a prior verification failed or capabilities are missing.
---

# Verifying

Verification is the only path from `verifying` to `done`. Evidence must be recent,
reproducible where possible, and collected after the latest relevant change.

## Build the evidence matrix

1. Re-read the current requirement, work item, decisions, implementation diff, and
   project Definition of Done. Surface conflicts before testing.
2. Map every acceptance criterion to a method: automated test, build or lint,
   reproducible manual check, static inspection, inference, or accepted gap.
3. Run the narrow checks first and the applicable full gate afterward. Inspect exit
   status and meaningful output; command invocation alone is not evidence.
4. Check scope integrity, unintended changes, documentation, migration, UX,
   compatibility, security, privacy, operations, and recovery when applicable.
5. Record each claim, method or command, result, scope, and limitations in an evidence
   artifact. Mark unavailable or unexecuted checks `unverified`; never present them as
   passing.

## Decide

If any acceptance criterion fails, lacks evidence, or has an unaccepted gap, the item
must not transition to done. Return it to `active` with the failure, impact, known
facts, and next action, or mark it `blocked` when progress truly cannot continue.

Transition to `done` only when every criterion has recent evidence or an explicitly
accepted verification gap, applicable project checks pass, and state, work item,
source, decisions, and evidence agree. Critical work also requires recorded security
and recovery consideration. Archive the item, update state and roadmap, and report
limitations alongside the bounded completion claim.