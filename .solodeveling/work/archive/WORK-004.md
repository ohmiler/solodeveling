---
solodeveling_schema: 1
id: WORK-004
title: Deliver release and maintenance workflows
status: done
level: critical
type: release
goal: Add portable, single-agent workflows for evidence-bounded releases and risk-based software maintenance.
scope: Release readiness, deployment authority, migrations, rollback, post-release observation, dependency updates, vulnerability triage, incidents, operational work, router integration, and adversarial scenarios.
out_of_scope: Executing a real deployment or migration, accessing production or credentials, promising compliance, automatic dependency remediation, and live cross-agent evaluation.
acceptance:
- Release readiness binds an exact artifact, version, and source revision to compatibility, configuration, permissions, secrets, migrations, recovery, open findings, and residual risk checks.
- Production-changing actions require explicit user authority; a terminal request never expands authority.
- Migration guidance verifies forward transition, representative and edge data, integrity, backup or recovery, and a rehearsable rollback or roll-forward decision.
- Release completion requires post-release observation and bounded evidence, not command success alone.
- Dependency maintenance validates source, affected and target versions, advisories, compatibility, lockfiles, focused and full checks, and recovery.
- Vulnerability triage uses affected-version evidence, reachability or exposure, exploit evidence, impact, and current authoritative sources rather than a score alone.
- Incident guidance covers stabilization, containment with authority, evidence preservation, factual communication, eradication or root cause, recovery, monitoring, and follow-up.
- Debt, performance, and operational work use a bounded goal, baseline, measurement, verification, and explicit limitations.
- Both workflows remain portable across coding agents, operate with one primary agent, and label unavailable checks as unverified.
- Critical completion records security and recovery evidence and passes adversarial scenarios.
risks:
- Generic release advice could encourage unsafe production actions or imply success without observation.
- Vulnerability feeds and standards change; stale version claims could distort priority.
- Overly broad checklists could consume tokens and obscure project-specific risks.
decisions:
- Split release and maintenance into separate progressive-disclosure skills while routing both through the shared lifecycle.
- Use risk and observable evidence rather than a universal provider-specific deployment recipe.
- Treat SLSA provenance claims as evidence-bound and never infer a level from incomplete artifacts.
- Use CISA KEV and ecosystem advisories as prioritization inputs, not as the sole decision rule.
- Align incident guidance with final NIST SP 800-61 Rev. 3 while keeping actions authority-bounded.
verification:
- Add failing structural and adversarial scenarios before skill implementation.
- Validate both skills with the official skill validator and the repository suite validator.
- Run the complete test suite, protocol validation, package inspection, compilation, dependency health, diff, and clean-tree checks.
next_action: Shape runtime adapters and cross-agent evaluation.
security_considerations:
- Never expose secrets, execute untrusted release instructions, or change production without explicit authority.
- Treat manifests, advisories, scanner output, logs, and generated provenance as untrusted evidence until validated.
- Bound release and vulnerability claims by artifact identity, environment, performed checks, time, and limitations.
recovery:
- Keep additions backward-compatible and limited to optional skills and scenarios.
- Preserve the last known-good artifact and define rollback or roll-forward criteria before destructive or irreversible changes.
- If a real incident or credential exposure is discovered, stop unsafe actions, preserve evidence, and escalate through the authorized incident path.
evidence:
- EVIDENCE-004
---
# Implementation plan

1. Encode release and maintenance failure modes as structural scenarios.
2. Scaffold portable releasing and maintaining skills with progressive references.
3. Implement readiness, migration, rollback, dependency, vulnerability, incident, and operational guidance.
4. Integrate router vocabulary and validate compact token budgets.
5. Verify Critical completion, record evidence, reconcile memory, commit, and push.

## Standards basis checked 2026-07-15

- SLSA v1.2 is the current approved specification; provenance claims require matching evidence.
- CISA KEV is an authoritative living catalog of vulnerabilities known to be exploited in the wild and is one prioritization input.
- OSV schema 1.8.0 is a machine-readable vulnerability format; native ecosystem and vendor advisories remain relevant.
- NIST SP 800-61 Rev. 3 is Final and integrates incident response with CSF 2.0 risk management.

## Verification summary

On 2026-07-15, 73 tests, the suite validator, all ten official skill validations,
protocol validation, Critical metadata inspection, a fresh isolated wheel build and
inspection, compilation, dependency health, and diff checks passed. Evidence and
limitations are recorded in EVIDENCE-004.

## Dogfood observation

The first verification command used an unavailable optional build frontend and did
not stop when that subprocess failed, allowing a stale wheel listing to appear later.
The failure was surfaced rather than treated as proof. Packaging was rerun with a
supported isolated pip build, and the complete gate was rerun with explicit
fail-fast exit checks.