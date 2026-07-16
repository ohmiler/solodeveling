---
solodeveling_schema: 1
id: WORK-030
title: Comparative Pilot Runtime Recovery
status: done
level: standard
type: repair
goal: Recover the controlled comparative pilot after all authorized attempts failed before inference because the preregistered model alias was absent from the local Codex catalog.
scope: Preserve the invalid pilot boundary, preregister an exact available model slug, fail closed against the local model catalog before any call, classify runtime failures without retaining raw output, exclude Python cache artifacts from change metrics, add regressions, and deliver through protected main without rerunning the live pilot.
out_of_scope: Any additional model call, treating failed attempts as comparative evidence, changing task fixtures or methodology pins, publishing a speed claim, or modifying release 0.1.1.
acceptance:
- The original pilot specification remains auditable as invalid and its 18 failed attempts are summarized without raw prompts or logs.
- A successor pilot uses exact model slug gpt-5.6-sol with medium reasoning while preserving task, methodology, order, timeout, and claim boundaries.
- Offline probe and live execution reject a model absent from the local Codex catalog before the first call.
- Sanitized failures record only bounded diagnostic codes and process return codes.
- A pre-inference runtime failure stops before the next call and cannot resume under the same preregistration.
- Python cache files do not inflate changed-file metrics.
- Focused and full verification pass, then protected-main CI passes before requesting new live authorization.
risks:
- A local model catalog can be stale; the harness must fail closed rather than infer aliases.
- The shared cache writer version can lag the executable version; executable identity remains authoritative while cache metadata is recorded for audit.
- Changing the model slug invalidates the prior preregistration and requires fresh live authorization.
- Retaining process diagnostics can leak prompts or account data unless reduced to fixed codes.
decisions:
- Treat pilot-1 as invalid runtime evidence with zero correct pairs and no speed interpretation.
- Use the exact account-visible slug gpt-5.6-sol rather than the undocumented local alias gpt-5.6.
- Do not reuse or overwrite the pilot-1 checkpoint for pilot-2.
verification:
- Test catalog acceptance/rejection, non-live probe, fixed diagnostic classification, cache-free change metrics, checkpoint boundaries, and exact 18-run plan.
- Run the complete suite, protocol and skill validators, compileall, dependency health, package build, and diff checks.
next_action: Request fresh owner authorization for pilot-2 only after protected-main delivery, naming gpt-5.6-sol medium and the new confirmation phrase.
evidence:
- EVIDENCE-030
---

# Failed execution boundary

The authorized pilot-1 command made 18 process attempts. Every attempt exited in
2.1-3.4 seconds with zero tokens, zero tool calls, visible fixture baselines still
passing, hidden checks failing, and no correct pair. The harness did not retain the
upstream stderr, so the exact service message is unavailable. The fresh local model
catalog contains `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna`, but not
`gpt-5.6`; current config selects `gpt-5.6-sol` with medium reasoning. This is a
runtime-preflight failure, not comparative methodology evidence.

# Verification

- Pilot-1 is archived with status `invalid-runtime`; the live status gate rejects it.
- Pilot-2 preserves all tasks, source pins, fixed ordering, timeouts, isolation, and
  claim limits while using exact catalog slug `gpt-5.6-sol` with medium reasoning.
- Offline probe verifies executable 0.144.5, exact model/reasoning availability,
  clean methodology sources, and the resolved command without a model call.
- Fourteen focused recovery tests and the complete 236-test suite pass.
- Protocol and skill validation, compileall, dependency health, diff checks, and
  temporary wheel/source-distribution builds pass.
- No model call occurred during recovery. Pilot-2 has no checkpoint or result.
