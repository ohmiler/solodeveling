# Core protocol

## Lifecycle

`captured -> shaped -> ready -> active -> verifying -> done`

`blocked` and `deferred` are explicit side states with a reason and return action.
Tracked Quick work may cross several states in one session but never skips
`verifying`. Ephemeral Quick work does not create lifecycle artifacts; it still
performs and reports focused verification before a completion claim.

## Persistence and artifact budget

- Ephemeral Quick stays in-session and creates no WORK, EVIDENCE, state, or roadmap
  edit. Use it only for reversible non-production work with no durable or sensitive
  boundary. Existing memory, Git usage, or a PR does not require tracking.
- Tracked Standard uses one WORK item and one cumulative EVIDENCE file. Store the
  executable plan in WORK and append checks or same-boundary follow-ups to EVIDENCE.
  Add another artifact only for a genuinely separate decision or claim.
- Resumable work persists the compact Standard pair and current state whenever another
  session must continue, a blocker exists, or a durable decision must survive.
- Audited work persists the full lifecycle and evidence contract for Critical,
  security, release, migration, production, destructive, or sensitive work.

Keep a bounded follow-up in the original work/evidence pair when goal, acceptance,
authority, risk, release or incident window, and rollback remain unchanged. Create
new work when any of those boundaries changes. Do not create separate artifacts for
shaping, planning, execution, verification, and closure phases of the same Standard
work.

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
One cumulative evidence file may contain multiple short observations for the same
work item; an observation is not a reason to allocate a new evidence ID.

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

Update roadmap only when a milestone, priority, ordering, or deferred-work decision
changes. Completion alone is not a roadmap event. Avoid standalone memory-only
commits for intermediate Standard states; combine memory with the implementation
delivery when possible. Post-deploy evidence may justify one bounded append to the
existing evidence, not a new work item.
