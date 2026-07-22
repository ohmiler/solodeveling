# Core protocol

## Contents

- Intent and read budgets
- Lifecycle and persistence
- Boundary and effect profiles
- Backend delivery profiles
- Iteration batches and checkpoints
- Verification reuse, triage, and artifacts
- Evidence and reconciliation

## Intent and read budgets

Classify the user's authority before reading project memory.
General Q&A reads no repository. Distinguish static inspection from runtime
verification and inference:

- General knowledge: answer directly; read no repository or memory.
- Repository explanation: read only the relevant source and describe static behavior.
- Review or analysis: inspect the requested scope and report findings; do not repair.
- Diagnosis: reproduce and identify root cause when needed; do not implement a fix
  unless the user authorized repair.
- Advice or planning: answer inline; persist only when the user asks to save it.
- Mutation: choose persistence and enter the lifecycle.

Use this memory budget for read-only project questions:

- Status: current state plus Git status.
- Current-work detail: add the referenced WORK item.
- Proof or completion basis: add the relevant EVIDENCE file.
- History: add only the requested archive entries.

Do not run tests or builds for a static explanation. Run a focused reproduction or
check only when the question asks about current runtime behavior or diagnosis. Label
the result explicitly as static inspection, executed behavior, or inference.

For status, read `.solodeveling/state.md` and Git status. Do not load deferred work
or archives unless the user asks for history or resumes that item.

A request to remember an idea authorizes only a minimal state or roadmap update. It
does not authorize implementation or justify creating WORK, EVIDENCE, acceptance
matrices, or lifecycle transitions in advance.

## Lifecycle and persistence

Tracked work uses `captured -> shaped -> ready -> active -> verifying -> done`.
`blocked` and `deferred` are explicit side states with a reason and return action.
Ephemeral Quick creates no lifecycle artifact but still reports focused proof before
a completion claim.

Ephemeral Quick targets `memory writes: 0`, `persistent artifacts: 0`, and
`focused verification: at least 1`. Ephemeral Quick takes precedence for a bounded
safe follow-up. Reuse WORK/EVIDENCE only when the continuation must survive a session,
changes a durable decision, or remains in the same active tracked batch.

Lifecycle state is semantic continuously but persistent only at useful checkpoints.
For uninterrupted Standard delivery, persist `active` once before implementation,
then persist final evidence plus `done` and archive once after verification. Persist
`captured`, `shaped`, `ready`, or `verifying` only when work crosses a session, is
blocked, needs handoff, changes scope or risk, or the user requests a checkpoint.

Apply this precedence:

1. Use Ephemeral Quick for a bounded, same-session, reversible follow-up that crosses
   no durable or sensitive boundary, even when the surface previously had Standard
   work. Do not reopen archived work merely to change one local detail.
2. Reuse the existing Standard WORK/EVIDENCE pair when the continuation must survive
   another session, changes a durable decision, or remains part of an active tracked
   batch with the same goal, acceptance, authority, risk, release, and rollback.
3. Create new work only when one of those boundaries materially changes.

If an Ephemeral slice belongs to an active tracked batch, leave the parent work item
unchanged during the slice and reconcile durable contract changes at its checkpoint.
Do not append evidence or transition state after every micro-change.

Standard work owns one WORK item and one cumulative EVIDENCE file. Audited work keeps
the full contract, security, authority, recovery, and evidence needed for Critical,
release, production, destructive, or sensitive effects. Existing memory, Git, a PR,
or lifecycle history never escalates work by itself.

A Standard WORK item normally targets roughly 30–40 lines and keeps intent, scope and
out of scope, acceptance with verification methods, material risks and decisions,
confirmed commands, and next action. Brevity is a target, not a reason to remove
required risk or recovery context. Do not duplicate an implementation plan and a
verification mapping when acceptance already identifies how it will be checked.
Keep EVIDENCE as a short current `AC -> result -> evidence -> limitation` table and
log only material failures, decisions, or limitations.

`state.md` is a current dashboard, not history. `active_work` references only work
that is actively resumable; deferred and archived work is loaded only when requested
or resumed. Coalesce uninterrupted memory writes and never create a transition-only
commit to demonstrate protocol use.

Cross-session or otherwise resumable work must persist the exact next action; a
same-session phase change alone does not justify a write.

## Boundary and effect profiles

Classify backend work by the boundary changed and effect produced:

`pure -> query -> local mutation -> privileged mutation -> external effect ->
financial/security effect -> migration`

- Pure local helpers may remain Quick with a focused unit check. Server-side queries
  and API handlers default to Standard. A bounded read-only mapping, sorting, copy,
  or observationally equivalent refactor remains Quick only when every carve-out in
  [backend-delivery.md](backend-delivery.md) is demonstrably true.
- A local database mutation is Standard when authority, data sensitivity, rollback,
  and external effects remain ordinary and bounded.
- Privileged mutations require authorization-boundary tests; become Critical when
  the change alters role, permission, ownership, or access decisions.
- External effects require retry, duplication, failure, and recovery consideration.
  Provider presence alone is not Critical; financial fulfillment or a changed trust
  boundary is.
- An authenticated route is not automatically Critical. Sorting, mapping, or copy
  behind login remains proportional unless the change alters identity or access.
- Additive reversible migrations with no material backfill are normally Standard.
Constraint changes, backfills, and data transformations are Critical when failure
can corrupt or expose data. Destructive schema/data changes are Critical and need
explicit authority plus recovery.

Changes to role/permission/ownership decisions cross an access boundary. Never silently lower Critical work.

For backend work, read [backend-delivery.md](backend-delivery.md) when classifying a
query/API Quick carve-out, mutation or webhook gates, environment failure, or additive
migration. Keep one boundary record in WORK. For security-bearing work this is the
attack-surface matrix, extended with `ID`, `Boundary`, `Authority`, `Invariant`,
`Failure`, `Risk / Control`, `Verification`, and `Recovery`. Shaping, planning,
securing, execution, and evidence update or reference the same record by ID.

For provider integrations, separate:

- Code-level evidence: mocks or fixtures, signature handling, retries, idempotency,
  failure behavior, and redacted logs.
- Release-level evidence: an owner-controlled smoke check against the target
  environment with redacted output.

Implementation may complete with the release check explicitly out of scope and
unverified; lack of production credentials does not by itself block code completion.

## Iteration batches and checkpoints

Keep a same-surface frontend design batch active while the user is iterating and no
new risk boundary appears. Treat commit, handoff, a move to another surface, a new
risk boundary, or explicit confirmation that the section is finished as a
checkpoint. Run focused verification for each slice, broad affected gates once at the
checkpoint, and archive at most once.

Use proportional frontend checks:

- Copy, color, or small spacing: focused browser/visual check plus diff integrity.
- Responsive layout: affected viewports during the slice; affected responsive suite
  and lint at checkpoint.
- Local interaction: component test or focused E2E; affected regression and build at
  checkpoint when required.
- Shared primitives or multiple routes: Standard affected tests, lint, and build.
- Auth, payment, sensitive data, or changed trust boundaries: Critical applicable
  gates.

Use proportional backend checks with the effect-specific minimums and broad-gate
conditions in [backend-delivery.md](backend-delivery.md):

- Pure helper: focused unit test; full unit suite at checkpoint when inexpensive.
- Read-only endpoint: auth contract, validation, mapping, empty, and error paths;
  affected tests and lint at checkpoint.
- Local mutation: focused transaction and failure tests; neighboring regressions,
  lint, and build at checkpoint.
- Identity, payment, webhook, or security boundary: boundary, replay, failure, and
  recovery tests plus only applicable broad gates.

For backend work, `applicable` means the gate can detect a regression in a changed
file, behavior, dependency, generated artifact, environment, or boundary. Stack
presence alone never makes every test, lint, build, or E2E gate applicable.

A broad result remains current across slices until a later change touches a file,
behavior, environment, dependency, or boundary covered by that result. Do not rerun
an unchanged broad gate solely because the user asks to commit after verification.
Prefer fake timers or component tests for long deterministic animation sequences;
keep browser tests focused on integration behavior rather than waiting through every
frame or character.

Record canonical non-interactive commands in project standards, including how to run
tests once instead of watch mode. Confirm commands from the repository; for Vitest a
project might use `npm run test -- --run` or define a dedicated `test:run` script.

## Verification reuse, triage, and artifacts

Reuse recent evidence until a later edit crosses the file, behavior, dependency,
environment, or boundary it covered. For example, a current responsive E2E result
may prove navigation, overflow, and viewport behavior; a manual browser audit should
then sample only gaps such as hierarchy, visual balance, computed color, hover, and
focus rather than repeat every route and viewport.

Before routing an unexpected verification failure to debugging:

1. Inspect exit status, logs, screenshots, traces, and relevant environment state.
2. If evidence plausibly indicates a transient harness or environment condition,
   make no source edit and rerun once under one controlled condition such as a warmed
   server or reduced concurrency.
3. Continue only when evidence isolates the transient cause, and record the first
   failure plus limitation. Route a repeated or unexplained failure to debugging.

For backend failures, use the source, harness, local environment, provider capability,
and migration-target outcomes in [backend-delivery.md](backend-delivery.md). Never
weaken a contract test, introduce real credentials, or mutate an uncertain database
to manufacture a passing rerun.

Browser screenshots, traces, and videos are transient by default. Evidence records
the observed result and limitation, not an ephemeral path. Persist an artifact only
when acceptance, audit, or review explicitly requires it; store it in a deliberate
project-owned location with intentional ignore or tracking policy.

## Evidence and reconciliation

Keep one Current acceptance matrix at the top of cumulative evidence. Update it when
requirements change. Mark replaced requirements `Superseded by ...` and keep only a
short chronological observation log below; do not append a complete new matrix for
every follow-up.

Evidence records the claim, method or command, result, scope, limitations, and the
important invariant proved. For backend work, emphasize who may act, validation,
transaction boundaries, duplicate/retry behavior, recovery, provider mocks, and
unverified production behavior rather than accumulating raw command logs.

Before `done`, reconcile current requirements, source behavior, tests, WORK, state,
and evidence. A failed or unverified acceptance criterion blocks completion unless an
authorized owner explicitly accepts the gap. Critical completion also requires
security and recovery evidence. Preserve concise durable summaries; omit raw logs,
secrets, caches, and conversation history.

When a required capability is missing, mark it unverified and reduce claim strength.

Update roadmap only when a milestone, priority, ordering, or deferred-work decision
changes. Completion alone is not a roadmap event. Validate memory after memory or
schema changes, suspected invalidity, before committing memory, and before tracked
completion; do not repeat unchanged validation within one session.
