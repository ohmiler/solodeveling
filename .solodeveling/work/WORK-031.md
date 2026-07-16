---
solodeveling_schema: 1
id: WORK-031
title: Comparative Pilot Methodology Activation Recovery
status: active
level: standard
type: repair
goal: Preserve pilot-2 as invalid methodology-activation evidence and make the successor benchmark install both workflow suites at Codex's actual project adapter path.
scope: Score and classify the sanitized pilot-2 result, identify the shared zero-change cause, archive its preregistration, align methodology installation with .agents/skills, verify the named root skill before timing, add regression coverage, preregister pilot-3, update documentation and memory, and deliver through protected main without another model call.
out_of_scope: Running pilot-3, publishing a comparative speed claim, changing fixtures, order, model, reasoning, source pins, timeout, or release 0.1.1.
acceptance:
- Pilot-2 remains auditable as 18 completed inference processes with zero correct runs and is explicitly rejected as comparative evidence.
- Both methodologies install at the Codex adapter path .agents/skills and the named root SKILL.md is verified before repository initialization and timing.
- Archived pilot-2 cannot pass the live-ready gate.
- Pilot-3 preserves the prior model, reasoning, pins, tasks, order, timeouts, and claim policy with a distinct identity, hash, checkpoint, and confirmation.
- Focused and full offline verification pass before protected-main delivery.
risks:
- A process return code of zero does not prove that the requested methodology was activated.
- A third live attempt consumes additional account capacity and requires separate explicit authorization.
- Synthetic pilot evidence remains insufficient for any public faster claim.
decisions:
- Classify pilot-2 as invalid methodology-activation evidence rather than a tie or speed result.
- Use the product's canonical Codex adapter path .agents/skills instead of a benchmark-only path.
- Do not run pilot-3 as part of this recovery.
verification:
- Validate the ignored sanitized pilot-2 result against the committed schema and score it offline.
- Test the exact installation path, named root-skill verification, archived status gate, deterministic plan, fixtures, full suite, protocol/skill validators, compilation, dependency health, package build, and diff checks.
next_action: Deliver the repair through protected main, then request a fresh pilot-3 authorization only if another 18 live calls are worthwhile.
evidence:
- EVIDENCE-031
---

# Pilot-2 boundary

Pilot-2 ran the authorized 18 processes with Codex CLI 0.144.5,
`gpt-5.6-sol`, medium reasoning, and the exact pinned methodology commits. All
processes returned zero after genuine inference and tool activity, but every
worktree remained unchanged. Visible fixture baselines passed, hidden checks
failed, and both methodologies scored 0/9. The harness had copied skills to
`.codex/skills` while the Codex adapter contract uses `.agents/skills`.

# Successor boundary

Pilot-3 changes only methodology activation and benchmark identity. It has not
been run. Its exact confirmation is `RUN CONTROLLED PILOT 3 18`, which is not
authorized by the pilot-2 confirmation.
