---
solodeveling_schema: 1
current_goal: Unify Solodeveling under one public name and make installation easy through Python and Node.js ecosystems without publishing.
active_work:
- WORK-009
blockers: []
risks:
- Downloading native executables through npm creates a supply-chain boundary that must fail closed before execution.
- No protected GitHub npm or pypi environment or registry trusted-publisher configuration exists.
- Package-name availability and vulnerability data are time-sensitive.
- The manual provenance workflow has not been invoked and no attestation exists.
- cursor-agent remains unavailable locally and complete Tier 1 behavior is unverified.
next_action: Commit and push WORK-009, require all Python, native, and npm CI jobs to pass, then record source-bound evidence.
---
# State

WORK-008 was merged as pull request 8 and a candidate was rebuilt from main commit
b211ff16b4e5f4f1f60a9c2b25432a5d4e6ca7b2; nothing has been tagged, attested,
released, configured on PyPI, or published. WORK-009 is active on
feat/unified-cli-installation to provide one public name and comprehensive install
UX. Solodeveling remains the single-agent workflow; Superpowers and subagents are
not used.
