---
solodeveling_schema: 1
---
# Risks

- WORK-008 remains unmerged and any public candidate must be rebuilt from the eventual `main` release commit.
- Candidate checksums and SBOM prove bounded integrity and inventory only; no final `main` candidate is signed or attested.
- One representative live scenario does not prove stable behavior across the full core matrix, model versions, repetitions, or sessions.
- cursor-agent is unavailable locally, so Cursor behavior and complete Tier 1 support remain unverified.
- Co-installing native runtime adapters may surface duplicate skills in clients that scan compatibility paths.
- High-confidence secret detection is a bounded output and project-memory safeguard, not a complete repository scanner.
- Security standards, runtime CLIs, structured-output schema subsets, authentication, and billing behavior evolve; exact claims require current primary-source verification.
