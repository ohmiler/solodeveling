---
solodeveling_schema: 1
current_goal: Verify explicitly authorized GitHub release prerequisites without invoking a candidate or publishing.
active_work:
- WORK-014
blockers: []
risks:
- GitHub reports can_admins_bypass true for both registry environments; the solo admin can explicitly bypass the ordinary reviewer gate.
- PyPI and npm Trusted Publishers are not configured, and both package names remain unreserved and time-sensitive until successful publication.
- The manual provenance workflow has not been invoked and no complete main release set or attestation exists.
- npm first-package bootstrap requires a separate owner-controlled interactive publication with two-factor authentication.
- Native executables are not platform-signed, and Cursor plus complete Tier 1 behavior remain unverified.
next_action: Submit WORK-014 documentation and evidence for pull-request CI without invoking any release or publication action.
---
# State

With explicit owner authorization, WORK-014 enabled GitHub Release immutability and
created `pypi` and `npm` environments. Both require reviewer `ohmiler`, permit solo
owner self-review, contain only an exact `main` branch deployment rule, and contain
no environment secrets or variables. GitHub reports admin bypass remains enabled.

Post-change checks found no tag, GitHub Release, candidate workflow run, publication
workflow run, registry staging action, approval, or publication. EVIDENCE-014 records
the settings, residual control, and recovery baseline. Solodeveling remained the
single-agent workflow; Superpowers and subagents were not used.
