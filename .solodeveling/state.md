---
solodeveling_schema: 1
current_goal: Run the authorized three-task routing pilot and, only if it passes,
  build and verify a local Solodeveling 0.3.0 candidate.
active_work:
- WORK-043
blockers: []
risks:
- Synthetic fixtures and self-authored evaluation are not independent comparative
  proof; speed or quality claims still require a controlled repeated benchmark.
- The authorized three-task live pilot consumes signed-in Codex capacity; the
  separate 30-call comparative benchmark remains unauthorized.
- Native executables remain unsigned; launcher integrity checks reduce substitution
  risk but do not provide platform code signing.
- Combined Standard routing must not bypass ambiguity, Critical, security, release,
  diagnosis-only, or verification-only boundaries.
- Backend Quick routing must fail closed when API compatibility or sensitivity is
  unclear.
next_action: Bump all current release surfaces to 0.3.0 and build local Python and
  Windows candidates from an exact clean source revision.
---
# State

WORK-043 has owner acceptance for the missing AC2 live evidence through local
candidate inspection only. Version surfaces are advancing to 0.3.0; AC2 remains
unverified and acceptance expires before public release. Push, tag, publication, the
30-call comparison, and production remain unauthorized.
