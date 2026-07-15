---
solodeveling_schema: 1
---
# Risks

- The stacked feature history is not merged into `main`; release publication remains premature.
- Release bundle checksums prove byte integrity only; artifacts are not signed, attested, or accompanied by an SBOM.
- One representative live scenario does not prove stable behavior across the full core matrix, model versions, repetitions, or sessions.
- cursor-agent is unavailable locally, so Cursor behavior and complete Tier 1 support remain unverified.
- Co-installing native runtime adapters may surface duplicate skills in clients that scan compatibility paths.
- High-confidence secret detection is a bounded output and project-memory safeguard, not a complete repository scanner.
- Security standards, runtime CLIs, structured-output schema subsets, authentication, and billing behavior evolve; exact claims require current primary-source verification.
