---
solodeveling_schema: 1
id: WORK-001
title: Validate protocol foundation
status: verifying
level: standard
type: build
goal: Prove that versioned project artifacts validate consistently.
scope: State, active work item, and evidence fixtures.
out_of_scope: Runtime adapters.
acceptance:
  - The project validator returns no issues.
risks: []
decisions: []
verification:
  - Run solodeveling-validate against the fixture.
next_action: Run the project validator.
evidence:
  - EVIDENCE-001
---
# Work notes
