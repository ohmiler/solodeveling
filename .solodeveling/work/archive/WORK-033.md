---
solodeveling_schema: 1
id: WORK-033
title: Enforce low-ceremony workflow tiers
status: done
level: standard
type: change
goal: Make small and ordinary Solodeveling work faster without weakening audited work.
scope: Skill routing, memory ownership, lifecycle helper commands, tests, and user
  documentation.
out_of_scope: Release 0.1.1 artifacts, Pilot-4 execution, and external Codex sandbox
  repair.
acceptance:
- Ephemeral Quick work creates no WORK, EVIDENCE, state, or roadmap artifact and runs
  focused verification.
- Standard work defaults to one WORK item and one cumulative EVIDENCE file.
- Same-boundary follow-ups reuse existing artifacts and roadmap changes only on priority
  events.
- Lifecycle helper commands safely record evidence, transition status, and archive
  work.
- Skill validation and the complete automated test suite pass.
risks:
- Automation could leave memory inconsistent after a partial write.
- Cumulative evidence could hide a failed latest observation.
decisions:
- Keep detailed artifact rules in protocol.md so the router remains within its token
  budget.
- Treat evidence frontmatter as the latest cumulative summary while retaining observation
  history in the body.
verification:
- Run the skill-suite validator and focused lifecycle regression tests.
- Run the complete pytest suite, compilation, packaging, and repository checks.
next_action: None; archived.
evidence:
- EVIDENCE-033
---
# Work

Apply the user feedback as enforceable routing, artifact budgets, and deterministic
memory operations. Keep this Standard delivery to one work item and one evidence file.
