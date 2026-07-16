# Core protocol

## Lifecycle

`captured -> shaped -> ready -> active -> verifying -> done`

`blocked` and `deferred` are explicit side states with a reason and return action.
Tracked Quick work may cross several states in one session but never skips
`verifying`. Ephemeral Quick work does not create lifecycle artifacts; it still
performs and reports focused verification before a completion claim.

## Persistence

- Ephemeral Quick stays in-session and creates no WORK, EVIDENCE, state, or roadmap
  edit. Use it only for local, reversible work with no durable or sensitive boundary.
- Resumable work persists a compact WORK item and current state whenever another
  session must continue, a blocker exists, or a durable decision must survive.
- Audited work persists the full lifecycle and evidence contract for Standard,
  Critical, security, release, migration, production, destructive, or sensitive work.

`state.md` is a current dashboard, not a history log. `active_work` references only
unfinished work being actively resumed; deferred work remains discoverable through
its work item or roadmap and is loaded only when explicitly resumed.

## Workflow selection

- Missing memory or unclear project context: onboarding.
- Unclear intent, scope, acceptance, or alternatives: `solodeveling-shaping-work`.
- Shaped work lacking an executable approach: `solodeveling-planning-work`.
- Ready or active implementation: `solodeveling-executing-work`.
- Failure, defect, or unexpected behavior: `solodeveling-debugging` before changing code.
- Implementation awaiting proof or a completion claim: `solodeveling-verifying`.
- Security trigger or finding: `solodeveling-securing`, combined with the current lifecycle stage.
- Deployment, migration, rollback, or readiness: `solodeveling-releasing`.
- Dependency, vulnerability, incident, debt, or operational work: `solodeveling-maintaining`.

If a specialized workflow is unavailable, preserve the lifecycle and evidence rules,
record that limitation, and use a minimal loop: understand, define acceptance,
inspect, plan proportionally, implement, verify, reconcile memory.

## Evidence

Evidence records the claim, method, command or procedure, result, scope, and
limitations. Prefer automated checks, then reproducible manual checks, static
inspection, inference, and accepted gaps. Never present inference as execution.

Scale verification by impact: Ephemeral Quick needs at least one focused check;
Standard needs affected tests and relevant regression; Critical needs the applicable
broad gate plus security and recovery checks. A failed Quick check escalates out of
the fast path.

`done` requires evidence or an explicitly accepted verification gap for every
acceptance criterion. Critical completion also requires documented security and
recovery consideration.

## State reconciliation

Before completion, reconcile current requirements, source behavior, tests, work
item, state, and evidence. Surface conflicts. Preserve durable decisions and useful
verification summaries; omit raw logs, secrets, caches, and conversation history.

Validate memory on an event: after memory or schema changes, when invalidity is
suspected, before committing memory, and before tracked completion. Do not repeat the
same validation in one session while memory is unchanged.
