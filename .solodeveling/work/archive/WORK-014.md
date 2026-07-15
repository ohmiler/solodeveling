---
solodeveling_schema: 1
id: WORK-014
title: Configure owner-controlled release prerequisites
status: done
level: critical
type: change
goal: Enable immutable GitHub Releases and create approval-gated pypi/npm deployment environments restricted to main without invoking any release or publication workflow.
scope: Enable repository release immutability; create pypi and npm environments; require the owner as reviewer; allow owner self-review for the solo-developer workflow; restrict deployments to the exact main branch; verify the resulting external state; record security and recovery evidence.
out_of_scope: Protecting the main branch, configuring PyPI or npm registry trusted publishers, adding environment secrets or variables, invoking a release candidate, creating a tag or GitHub Release, staging, approving, or publishing a package.
acceptance:
- Repository immutable releases reports enabled true and is not disabled during this work.
- Environments pypi and npm each require reviewer ohmiler, permit owner self-review, and use custom deployment branch policy main only.
- No environment secrets or variables are added.
- No workflow, candidate, tag, GitHub Release, registry staging, approval, or publication is invoked.
- External configuration is re-read after mutation and project memory records exact evidence and recovery.
risks:
- An incorrect deployment policy could allow publication from a non-main branch or block the solo owner from approving a valid release.
- GitHub reports can_admins_bypass true for both environments; an administrator can explicitly bypass the ordinary reviewer gate.
- Disabling immutable releases later would weaken guarantees for future releases.
- Environment protection does not configure or reserve either public registry package name.
decisions:
- Use custom branch policy main because the main branch is not currently protected.
- Require GitHub user ohmiler as the sole reviewer and set prevent_self_review false so the solo owner can approve a workflow they initiated.
- Retain and disclose GitHub's default admin-bypass recovery path because the documented REST API cannot change it and no browser backend is available; reconsider disabling it in the UI before first publication.
- Keep registry identity setup and every release or publication action separately authorized.
verification:
- Re-read immutable-release status and full environment protection rules through the GitHub REST API.
- List deployment branch policies, environment secret names, variable names, tags, releases, and relevant workflow runs.
- Validate project memory, run documentation/release policy tests, and inspect the diff.
next_action: Decide whether to disable administrator bypass in the GitHub UI and obtain separate authority before configuring the PyPI pending publisher or invoking any release action.
security_considerations:
- Configuration uses the authenticated repository administrator and least-privilege environment gates; no token, credential, secret, or variable was added or recorded.
- Exact main-only policy and manual review reduce unauthorized publication paths but do not prove registry or artifact security; admin bypass remains an explicit residual control.
recovery:
- Because both environments were absent at baseline, delete pypi/npm to restore the environment baseline if configuration is incorrect.
- Because immutable releases was disabled at baseline, use the repository immutable-releases DELETE endpoint only if rollback is explicitly required before any release exists.
- Correct reviewer or branch policy in place rather than deleting a valid environment when a narrower configuration repair is sufficient.
evidence:
- EVIDENCE-014
---
# Execution plan

1. Record the observed baseline and authorization boundary.
2. Enable immutable releases and verify the server response.
3. Create each environment with the owner reviewer and custom deployment policy, then add only the exact main branch rule.
4. Re-read all settings and absence checks before recording evidence.
5. Submit the memory/documentation update through normal review without invoking release workflows.
