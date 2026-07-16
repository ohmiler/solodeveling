---
solodeveling_schema: 1
id: WORK-001
title: Improve title formatting
status: active
level: standard
type: change
goal: Keep title formatting predictable and verified.
scope: formatter.py, focused tests, and cumulative evidence.
out_of_scope: New packages and unrelated cleanup.
acceptance:
- Title formatting matches the approved requirement.
- Focused tests pass.
risks: []
decisions:
- Reuse this work item for bounded formatter follow-ups.
verification:
- Run all unit tests.
next_action: Implement the approved max-length follow-up.
evidence:
- EVIDENCE-001
---
# Work

This item owns formatter behavior and bounded follow-ups.
