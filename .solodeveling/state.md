---
solodeveling_schema: 1
current_goal: Decide whether to disable environment admin bypass and configure the PyPI pending publisher without invoking a candidate or publishing.
active_work: []
blockers: []
risks:
- GitHub reports can_admins_bypass true for both registry environments; the solo admin can explicitly bypass the ordinary reviewer gate.
- PyPI and npm Trusted Publishers are not configured, and both package names remain unreserved and time-sensitive until successful publication.
- The manual provenance workflow has not been invoked and no complete main release set or attestation exists.
- npm first-package bootstrap requires a separate owner-controlled interactive publication with two-factor authentication.
- Native executables are not platform-signed, and Cursor plus complete Tier 1 behavior remain unverified.
next_action: Obtain explicit owner authority before changing environment admin bypass in the GitHub UI or configuring the PyPI pending publisher; candidate, tag, release, staging, approval, and publication remain separate.
---
# State

WORK-014 enabled GitHub Release immutability and created `pypi` and `npm`
environments with EVIDENCE-014. Both require reviewer `ohmiler`, permit solo-owner
self-review, contain only exact `main` branch deployment policy, and contain no
environment secrets or variables. GitHub reports admin bypass remains enabled.

Pull-request CI run 29448771069 passed the complete matrix for the configuration
record. Post-change checks found no tag, GitHub Release, candidate workflow run,
publication workflow run, registry staging action, approval, or publication.
Solodeveling remained the single-agent workflow; Superpowers and subagents were not
used.