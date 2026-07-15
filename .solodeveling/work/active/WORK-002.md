---
solodeveling_schema: 1
id: WORK-002
title: Deliver the core development workflow suite
status: verifying
level: standard
type: build
goal: Let one primary agent shape, plan, execute, debug, and verify ordinary software work using Solodeveling alone.
scope: Five portable workflow skills, router integration, deterministic structural checks, lifecycle scenarios, and end-to-end dogfood evidence.
out_of_scope: Dedicated security profiles, release and maintenance workflows, runtime-specific adapters, and live cross-agent evaluation.
acceptance:
- Shaping produces bounded intent, acceptance criteria, alternatives, and an explicit readiness decision.
- Planning is proportional to Quick, Standard, or Critical work and includes verification and recovery where applicable.
- Execution maintains one-agent continuity, handles dirty worktrees safely, and updates durable state without mandatory subagents or worktrees.
- Debugging requires reproducible evidence and root-cause analysis before implementation changes.
- Verification maps every completion claim to recent evidence and prevents invalid done transitions.
- A complete scenario moves a work item from captured through verifying without relying on Superpowers.
- Core router plus one selected workflow remains within progressive-disclosure budgets.
risks:
- Copying Superpowers wording could preserve unwanted team-oriented ceremony or licensing ambiguity.
- Structural assertions alone may not prove agent behavior under pressure.
- The dogfood run missed the active-state checkpoint before implementation; it was surfaced and reconciled before verification.
decisions:
- Reimplement protocol behavior from the approved Solodeveling design rather than copying Superpowers skill text.
- Keep each workflow runtime-neutral and fully correct with one primary agent.
- Reserve dedicated security, release, and maintenance workflows for later increments.
verification:
- Run official structural validation for every skill.
- Run suite checks for references, metadata, token budgets, and prohibited subagent requirements.
- Run scenarios for Quick work, ordinary planning, root-cause repair, verification failure, missing capabilities, and lifecycle resumption.
- Dogfood WORK-002 using only Solodeveling artifacts and workflows.
next_action: Run the clean release gate and record EVIDENCE-002.
---
# Implementation plan

1. Define deterministic scenario contracts and expected routing for all five workflows.
2. Scaffold each portable skill with standard metadata and only necessary references.
3. Implement shaping and planning, then execution and debugging, then verification.
4. Integrate router workflow names and progressive-disclosure budgets.
5. Exercise the lifecycle on WORK-002, record evidence, reconcile memory, and push.
## Dogfood observation

The first execution pass left the durable status at `ready` while implementation was
in progress. The discrepancy was detected during reconciliation, recorded rather
than hidden, and corrected to `verifying`. Automated lifecycle coverage now exercises
captured through verifying; future live runs must checkpoint `active` at execution entry.
