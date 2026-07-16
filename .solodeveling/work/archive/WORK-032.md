---
solodeveling_schema: 1
id: WORK-032
title: Comparative Pilot Sandbox Execution Recovery
status: done
level: standard
type: repair
goal: Preserve Pilot-3 as invalid execution-sandbox evidence and prevent another multi-call benchmark when Codex cannot execute sandboxed tools or the first mutation-required task changes nothing.
scope: Validate and score sanitized Pilot-3, inspect bounded local sandbox capability evidence, archive its preregistration, require the Windows sandbox setup helper before live calls, classify zero-mutation completion as an execution failure, stop and forbid resume after one such call, add regressions, preregister Pilot-4 without running it, and deliver through protected main.
out_of_scope: Repairing the external Codex installation, running Pilot-4, bypassing the sandbox, retaining raw prompts or model output, publishing a comparative claim, or changing release 0.1.1.
acceptance:
- Pilot-3 remains auditable as 18 completed inference processes, zero correct runs, zero changed files, and invalid comparative evidence.
- Windows probe and live execution fail before a model call when codex-windows-sandbox-setup.exe is unavailable.
- A completed mutation-required run with zero changed files is recorded as zero-mutation execution failure and stops before the next call.
- A checkpoint containing zero-mutation execution failure cannot resume.
- Pilot-4 preserves model, reasoning, pins, tasks, order, timeout, and claim policy with a distinct identity and confirmation but is not run.
- Focused/full verification and protected-main CI pass.
risks:
- The missing helper is strong shared-environment evidence but raw per-run diagnostics are unavailable by design.
- Checking helper presence proves availability, not that every future sandbox command will succeed.
- Any future Pilot-4 execution consumes account capacity and requires separate authorization after environment repair.
decisions:
- Classify Pilot-3 as invalid execution-sandbox evidence, not a tie.
- Fail closed before inference on Windows when the sandbox helper cannot be found.
- Treat zero mutation on these fixtures as a non-resumable execution failure.
- Do not bypass sandbox protections to obtain benchmark results.
verification:
- Validate and score sanitized Pilot-3 offline.
- Test helper acceptance/rejection, archived live gate, zero-mutation checkpoint rejection, deterministic plan, full suite, validators, compilation, dependencies, package build, and diff checks.
next_action: Repair Codex Windows sandbox support and pass the non-live Pilot-4 probe before considering any live authorization.
evidence:
- EVIDENCE-032
---

# Execution boundary

Pilot-3 used the approved Codex CLI, model, reasoning level, methodology commits,
fixed 18-run order, corrected `.agents/skills` path, and isolated worktrees. All
processes returned zero after inference and tool activity, yet no worktree
changed. Local Codex sandbox logs independently record repeated attempts to
launch `codex-windows-sandbox-setup.exe` ending in `program not found`,
including the Solodeveling project cwd.

# Successor boundary

Pilot-4 is a non-live successor. It cannot pass local probe or live preflight
while the helper remains missing. Its confirmation is
`RUN CONTROLLED PILOT 4 18`, which has not been authorized.

# Delivery

PR #37 passed the full CI matrix and merged as
`28c11ed2e1ddc1a8386debb7784d83452184ead9`. Post-merge main CI run
`29516757752` also passed. Pilot-4 remains blocked and not run.
