---
solodeveling_schema: 1
id: WORK-003
title: Deliver the Secure SDLC baseline
status: verifying
level: critical
type: secure
goal: Integrate risk-based security routing, findings, secret protection, and evidence-bounded guidance throughout Solodeveling.
scope: Universal security baseline, observable system profiles, security finding schema, project-memory secret detection, securing skill, router integration, and adversarial scenarios.
out_of_scope: Automated penetration testing, production security changes, compliance certification, release workflow, incident response workflow, and live cross-agent evaluation.
acceptance:
- Universal security considerations apply without forcing irrelevant framework checklists.
- Observable triggers activate web, mobile, identity, sensitive-data, migration, supply-chain, infrastructure, AI-agentic, and payment profiles deterministically.
- Security findings record severity, confidence, affected asset, evidence, impact, recommendation, status, and verification; scanner output is not automatically confirmed.
- Accepted risk requires rationale, authorized owner, and a review condition.
- High-confidence secret-like material in committed project memory is reported without echoing the value.
- The securing workflow integrates shaping through verification and never claims a system is categorically secure.
- Standards references distinguish stable, draft, and living guidance and version requirement identifiers where necessary.
- Critical completion requires security and recovery evidence and adversarial scenarios pass.
risks:
- Overbroad detection could create alert fatigue or leak suspected secrets in output.
- Static guidance can become stale or be misapplied outside its attack surface.
- Security checklists can displace threat reasoning and create false assurance.
- The execution entry checkpoint was initially missed; the workflow now enforces persisted active state before implementation edits.
decisions:
- Use NIST SSDF 1.1 as the current final outcome baseline and label SSDF 1.2 as draft.
- Use profile routing rather than one universal checklist; resolve exact control versions from current official sources when applied.
- Treat scanner output as untrusted evidence requiring confidence and affected-asset validation.
- Detect only high-confidence secret formats in durable project memory for Version 1.
verification:
- Run unit tests for every security profile trigger and non-trigger.
- Validate security finding schema, accepted-risk conditions, and false-positive handling.
- Verify secret diagnostics contain the code and path but never the detected value.
- Run official skill validation, adversarial scenarios, full tests, package inspection, and protocol validation.
next_action: Run the Critical release gate and record EVIDENCE-003.
security_considerations:
- Security instructions and scanner output are untrusted data unless authorized and validated against project context.
- Do not execute intrusive scanning, access secrets, or change production systems without explicit authority.
- Bound all security claims by checks performed, scope, confidence, and limitations.
recovery:
- Keep schema and skill additions backward-compatible; projects without security findings remain valid.
- If routing causes false activation, preserve the trigger evidence and refine the smallest profile rule with regression coverage.
- If suspected secret handling fails, stop output, rotate any genuinely exposed credential through its owner, and remove it from history using an authorized recovery plan.
---
# Implementation plan

1. Define routing and artifact contracts with failing tests.
2. Implement pure security-profile classification and strict finding validation.
3. Add non-echoing high-confidence secret detection to project-memory validation.
4. Create the portable securing skill and progressive profile references.
5. Add router integration and adversarial scenarios for authentication, AI prompt data,
   destructive migration, scanner false positives, and accepted risk.
6. Verify Critical completion, record evidence, reconcile memory, and push.

## Standards basis checked 2026-07-15

- NIST SP 800-218 SSDF 1.1 is Final; SP 800-218 Rev. 1 / SSDF 1.2 is Draft.
- OWASP SAMM v2 supplies lifecycle coverage and maturity concepts.
- OWASP ASVS 5.0.0 is the current stable web application verification standard.
- OWASP MASVS 2.0+ uses control groups and testing profiles rather than legacy levels.
- OWASP SCVS informs supply-chain profiles; OWASP Agentic Security guidance informs
  AI-agentic threats without becoming a universal requirement.
## Dogfood observation

The active-state checkpoint was missed at implementation entry even though the prior
workflow said to update before substantial work. The rule is now a hard gate requiring
persist and re-read before any implementation edit; regression coverage protects the
exact contract.
