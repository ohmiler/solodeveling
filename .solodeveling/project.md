---
solodeveling_schema: 1
name: Solodeveling
purpose: Provide a portable, evidence-driven SDLC skill suite for solo developers
  using one primary coding agent.
users:
- Solo software developers using coding agents
architecture: Protocol-first portable Agent Skills with plain Markdown project memory
  and optional Python validation tooling.
stack:
- Markdown
- YAML
- JSON Schema Draft 2020-12
- Python 3.10+
constraints:
- No correctness path requires subagents.
- Core protocol semantics remain runtime-neutral.
- Python tooling is optional at skill runtime.
- Repository content is Apache-2.0 licensed.
sources:
- docs/superpowers/specs/2026-07-15-solodeveling-design.md
- docs/protocol-contract.md
- pyproject.toml
---
# Project

This file records durable project facts. Update it when the product purpose,
architecture, stack, constraints, or authoritative sources change.
