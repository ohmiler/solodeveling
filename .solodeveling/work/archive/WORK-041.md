---
solodeveling_schema: 1
id: WORK-041
title: Make backend delivery proportional and evidence-efficient
status: done
level: standard
type: change
goal: Reduce backend ceremony for bounded work while preserving authorization, transaction,
  provider, migration, and recovery safeguards.
scope: Add one backend delivery contract; refine the Quick API/query carve-out, boundary
  records, effect-specific gates, environment triage, additive migrations, routing,
  deterministic scenarios, documentation, and managed runtime copies.
out_of_scope: A combined Critical backend skill, production/database operations, real
  credentials, live-agent benchmark calls, release, commit, and push.
acceptance:
- AC1 — Backend API/query work is Quick only under explicit read-only, contract-stable,
  non-sensitive, no-effect conditions with a focused contract test.
- AC2 — WORK owns one boundary record covering authority, invariant, failure, control,
  verification, and recovery; later phases reference it without duplication.
- AC3 — Query, mutation, webhook, and migration gates define focused minimums and
  when affected broad tests, lint, build, or full suite are actually applicable.
- AC4 — Backend triage distinguishes source, harness, environment, provider capability,
  and migration-target failures without weakening tests or claiming missing smoke
  proof.
- AC5 — Additive migration guidance remains Standard and proportional; scenarios,
  focused/full tests, skill/protocol validation, adapter conformance, and diff checks
  pass.
risks:
- A broad Quick carve-out could underclassify observable API contract changes.
- A rigid gate table could miss project-specific invariants or encourage checklists.
decisions:
- Keep API/query work Standard unless every Quick condition is demonstrably true.
- Keep Critical security/release routing specialized until real backend pilots justify
  change.
- Put detailed backend rules in one progressive-disclosure reference.
verification:
- Add static contract scenarios and focused tests, then run all repository gates and
  official skill validation without touching paused benchmark behavior.
next_action: None; archived.
evidence:
- EVIDENCE-041
---
