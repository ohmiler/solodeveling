---
name: solodeveling-shaping-work
description: Turn an unclear software request into bounded, decision-ready work with intent, users, outcomes, scope, acceptance criteria, risks, and alternatives. Use for new features, meaningful changes, explorations, or repairs whose desired behavior or boundaries are not yet clear. Skip when an existing work item is already shaped and its acceptance criteria remain valid.
---

# Shaping Work

Shape the problem before choosing implementation. Keep one primary agent and ask only
questions whose answers materially change the outcome, scope, safety, or authority.

## Establish intent

1. Read current state, project facts, relevant existing behavior, and authoritative
   requirements. Separate confirmed facts, inference, proposals, and unknowns.
2. State the user or system problem, affected users, desired outcome, and why it
   matters. Do not convert future wants into current requirements.
3. Define scope and out of scope in observable terms. Surface conflicts with current
   behavior or documentation instead of resolving them by guesswork.
4. Write acceptance criteria that can be verified. Prefer behavior and outcomes over
   implementation choices.
5. Classify Quick, Standard, or Critical from observable triggers. Record product,
   technical, security, privacy, operational, and UX risks that actually apply.
6. Consider alternatives: at least the recommended approach, the smallest credible option,
   and doing nothing when the trade-off is meaningful. Record binding decisions.

## Readiness decision

Mark the item `shaped` when intent, boundaries, acceptance criteria, and material
risks are clear. Route to planning before `ready` unless the Quick item already has
the smallest executable approach and verification method.

Do not mark ready when a material unknown affects architecture, irreversible action,
security, cost, or acceptance. Record the blocker and precise next discovery action.
Update the work item and state; keep notes concise and never preserve a transcript.