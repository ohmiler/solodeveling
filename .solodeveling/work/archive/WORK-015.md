---
solodeveling_schema: 1
id: WORK-015
title: Verify owner release setup
status: done
level: critical
type: change
goal: Reconcile independently verified GitHub environment hardening and owner-confirmed PyPI pending publisher setup before any release candidate is invoked.
scope: Verify admin bypass, reviewer, branch policy, immutable releases, clean main, CI, and absence of release activity; record the owner's PyPI pending publisher confirmation with its public-verification limitation; update release memory and documentation.
out_of_scope: Testing PyPI OIDC by minting a token, invoking a candidate or publish workflow, creating a tag or GitHub Release, configuring npm Trusted Publishing, staging, approving, or publishing a package.
acceptance:
- GitHub API reports immutable releases enabled and can_admins_bypass false for pypi and npm while reviewer and exact main-only policy remain correct.
- Project memory records the PyPI pending publisher as owner-confirmed, not independently API-verified, and retains the unreserved-name risk.
- No candidate/publish workflow run, tag, GitHub Release, registry staging, approval, or publication occurs.
- Focused release/publication documentation checks and project validation pass.
risks:
- A typo in the pending publisher identity cannot be detected until authenticated UI review or first authorized OIDC use.
- The pending publisher does not reserve the PyPI project name before first publication.
- Overstating owner confirmation as API verification would create false release confidence.
decisions:
- "Accept the owner's direct confirmation as manual evidence bounded to the exact requested identity: project solodeveling, owner ohmiler, repository solodeveling, workflow publish.yml, environment pypi."
- Keep OIDC matching and first publication unverified until a separately authorized publish action.
verification:
- Re-read GitHub settings and release activity through official APIs.
- Confirm the public PyPI project remains absent, which is expected and does not prove or disprove a pending publisher.
- Run focused project-memory, release, publication, and documentation checks.
next_action: Obtain explicit owner authorization before invoking the 0.1.0 release-candidate workflow from the exact reviewed main commit.
security_considerations:
- No token, session, OIDC credential, secret value, or PyPI account data is accessed or recorded.
- Disabling admin bypass strengthens the required-review gate; self-review remains permitted for the solo owner.
recovery:
- Correct the pending publisher in the PyPI authenticated UI if first-use OIDC matching reports invalid-pending-publisher.
- Restore documentation from Git history if the owner-confirmed identity was recorded incorrectly; do not test by unauthorized publication.
evidence:
- EVIDENCE-015
---
# Execution plan

1. Persist the verified-versus-owner-confirmed evidence boundary.
2. Reconcile project state, risks, roadmap, publishing, and readiness guidance.
3. Run focused verification and inspect the diff.
4. Mark done, archive, and submit through PR/CI without invoking release workflows.