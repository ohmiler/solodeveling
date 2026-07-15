# Core protocol

## Lifecycle

`captured -> shaped -> ready -> active -> verifying -> done`

`blocked` and `deferred` are explicit side states with a reason and return action.
Quick work may cross several states in one session but never skips `verifying`.

## Workflow selection

- Missing memory or unclear project context: onboarding.
- Unclear intent, scope, acceptance, or alternatives: `solodeveling-shaping-work`.
- Shaped work lacking an executable approach: `solodeveling-planning-work`.
- Ready or active implementation: `solodeveling-executing-work`.
- Failure, defect, or unexpected behavior: `solodeveling-debugging` before changing code.
- Implementation awaiting proof or a completion claim: `solodeveling-verifying`.
- Security trigger or finding: securing, combined with the current lifecycle stage.
- Deployment, migration, rollback, or readiness: releasing.
- Dependency, vulnerability, incident, debt, or operational work: maintaining.

If a specialized workflow is unavailable, preserve the lifecycle and evidence rules,
record that limitation, and use a minimal loop: understand, define acceptance,
inspect, plan proportionally, implement, verify, reconcile memory.

## Evidence

Evidence records the claim, method, command or procedure, result, scope, and
limitations. Prefer automated checks, then reproducible manual checks, static
inspection, inference, and accepted gaps. Never present inference as execution.

`done` requires evidence or an explicitly accepted verification gap for every
acceptance criterion. Critical completion also requires documented security and
recovery consideration.

## State reconciliation

Before completion, reconcile current requirements, source behavior, tests, work
item, state, and evidence. Surface conflicts. Preserve durable decisions and useful
verification summaries; omit raw logs, secrets, caches, and conversation history.