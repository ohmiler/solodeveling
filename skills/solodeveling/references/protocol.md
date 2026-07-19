# Core protocol

## Contents

- Intent and read budgets
- Lifecycle and persistence
- Boundary and effect profiles
- Iteration batches and checkpoints
- Evidence and reconciliation

## Intent and read budgets

Classify the user's authority before loading project memory:

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

A request to remember an idea authorizes only a minimal state or roadmap update. It
does not authorize implementation or justify creating WORK, EVIDENCE, acceptance
matrices, or lifecycle transitions in advance.

## Lifecycle and persistence

Tracked work uses `captured -> shaped -> ready -> active -> verifying -> done`.
`blocked` and `deferred` are explicit side states with a reason and return action.
Ephemeral Quick creates no lifecycle artifact but still reports focused proof before
a completion claim.

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

`state.md` is a current dashboard, not history. `active_work` references only work
that is actively resumable; deferred and archived work is loaded only when requested
or resumed. Coalesce uninterrupted memory writes and never create a transition-only
commit to demonstrate protocol use.

## Boundary and effect profiles

Classify backend work by the boundary changed and effect produced:

`pure -> query -> local mutation -> privileged mutation -> external effect ->
financial/security effect -> migration`

- Pure local helpers may remain Quick with a focused unit check. Server-side queries
  and API handlers default to Standard even when authentication and data boundaries
  remain unchanged.
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

For security-bearing work, keep one attack-surface matrix in WORK with `Boundary`,
`Risk`, `Control`, `Verification`, and `Recovery`. Shaping, planning, securing, and
verification update that matrix rather than restating actors and threats in separate
artifacts.

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

Use proportional backend checks:

- Pure helper: focused unit test; full unit suite at checkpoint when inexpensive.
- Read-only endpoint: auth contract, validation, mapping, empty, and error paths;
  affected tests and lint at checkpoint.
- Local mutation: focused transaction and failure tests; neighboring regressions,
  lint, and build at checkpoint.
- Identity, payment, webhook, or security boundary: boundary, replay, failure, and
  recovery tests plus all applicable broad gates.

A broad result remains current across slices until a later change touches a file,
behavior, environment, dependency, or boundary covered by that result. Do not rerun
an unchanged broad gate solely because the user asks to commit after verification.
Prefer fake timers or component tests for long deterministic animation sequences;
keep browser tests focused on integration behavior rather than waiting through every
frame or character.

Record canonical non-interactive commands in project standards, including how to run
tests once instead of watch mode. Confirm commands from the repository; for Vitest a
project might use `npm run test -- --run` or define a dedicated `test:run` script.

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

Update roadmap only when a milestone, priority, ordering, or deferred-work decision
changes. Completion alone is not a roadmap event. Validate memory after memory or
schema changes, suspected invalidity, before committing memory, and before tracked
completion; do not repeat unchanged validation within one session.
