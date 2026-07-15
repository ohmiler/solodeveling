---
solodeveling_schema: 1
current_goal: Make ordinary Solodeveling installation zero-config while preserving safe advanced overrides.
active_work:
- WORK-012
blockers: []
risks:
- No protected GitHub npm or pypi environment or registry trusted-publisher configuration exists.
- npm and PyPI package names remain unreserved and time-sensitive until successful publication.
- The manual provenance workflow has not been invoked and no complete main release set or attestation exists.
- npm first-package bootstrap requires a separate owner-controlled interactive publication with two-factor authentication.
- Native executables are not platform-signed, and Cursor plus complete Tier 1 behavior remain unverified.
next_action: Review, commit, and push WORK-012 for cross-platform GitHub CI without publishing.
---
# State

WORK-012 is verifying on `feat/zero-config-install`. It shortens ordinary project setup
to `solodeveling install`, with automatic project-local runtime discovery and safe
managed-install discovery for check/uninstall. Advanced flags remain compatible but
leave the primary UX. Release prerequisites and all external publication actions
remain unchanged and unperformed. Solodeveling remains the single-agent workflow;
Superpowers and subagents are not used.
