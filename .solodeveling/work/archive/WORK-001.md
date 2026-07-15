---
solodeveling_schema: 1
id: WORK-001
title: Deliver the core router and onboarding increment
status: done
level: standard
type: build
goal: Make Solodeveling discoverable, resumable, and safe to initialize across coding-agent runtimes.
scope: Portable core and onboarding skills, project-memory initialization, validation, and structural scenarios.
out_of_scope: Complete SDLC workflow skills, security profiles, release workflows, and runtime-specific adapters.
acceptance:
- Core and onboarding are valid standard skill folders with runtime-neutral semantics.
- Brownfield initialization cannot overwrite an existing partial memory tree.
- A new session can reconstruct current work from project artifacts.
- Router token and onboarding scenario regressions run deterministically.
risks:
- A partial workflow could be mistaken for a complete Superpowers replacement.
decisions:
- Keep detailed onboarding separate from the compact core router.
- Make Python initialization optional and preserve a plain Markdown fallback.
verification:
- Run the complete Python test suite.
- Run official skill validators and the Solodeveling suite validator.
- Build and inspect the wheel, then validate this repository memory.
next_action: Shape the core lifecycle workflow increment.
evidence:
- EVIDENCE-001
---
# Work item

Completed as the second independently testable delivery step in the approved design.