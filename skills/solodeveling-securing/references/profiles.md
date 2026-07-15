# Security profiles

Activate all profiles supported by observable architecture or work-item evidence.

- **web-application:** trust boundaries, input handling, output encoding, browser and
  API controls, authentication, authorization, session, transport, SSRF and abuse
  cases. Use current OWASP ASVS requirements when detailed verification is needed.
- **mobile:** storage, cryptography, authentication, network, platform interaction,
  code quality, resilience, and privacy. Use current MASVS control groups and MASTG
  tests; do not assume legacy L1, L2, or R levels.
- **identity-access:** identity lifecycle, authentication strength, account recovery,
  authorization at trusted boundaries, session creation/rotation/revocation, audit,
  rate limits, and privilege escalation.
- **sensitive-data:** classification, minimization, purpose, consent where applicable,
  retention, deletion, access, encryption using platform mechanisms, logging,
  residency, backup, and incident impact.
- **data-migration:** preconditions, authorization, backups, integrity constraints,
  edge-case data, rehearsal, monitoring, rollback or forward recovery, and evidence
  that transition and recovery both work.
- **supply-chain:** inventory, dependency identity, lockfiles, vulnerability analysis,
  build isolation, provenance, signing, SBOM, release artifacts, and remediation.
- **infrastructure:** shared responsibility, IAM and least privilege, network exposure,
  secret injection, configuration drift, containers, policy, observability, backup,
  and rollback.
- **AI-agentic:** prompt and goal manipulation, untrusted retrieval, model and data
  provenance, memory poisoning, sensitive disclosure, tool misuse, excessive agency,
  output handling, identity, privilege, human approval, and resource limits.
- **payments:** trusted provider boundaries, transaction authorization, amount and
  recipient integrity, idempotency, reconciliation, webhook authenticity, sensitive
  payment data scope, audit, dispute, and recovery.

A profile is a routing aid, not proof. Tailor threats, controls, and tests to the
actual system and record why a profile or control is applicable.