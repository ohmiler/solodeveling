---
solodeveling_schema: 1
id: WORK-021
title: Publish Solodeveling 0.1.0 to PyPI
status: done
level: critical
type: release
goal: Publish the exact verified Solodeveling 0.1.0 Python distributions to PyPI through the protected OIDC workflow and prove clean installation without performing any npm action.
scope: Dispatch publish.yml from protected main for version 0.1.0 and source commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4 with PyPI enabled and npm skipped; observe validation and protected deployment; verify PyPI metadata, files, provenance where exposed, and clean pip, uvx, and pipx execution.
out_of_scope: npm bootstrap, npm staging or publication, changing release assets, rebuilding the candidate, or modifying package code.
acceptance:
- Exactly one authorized publish.yml run validates the immutable release and succeeds for PyPI with npm skipped.
- PyPI exposes solodeveling version 0.1.0 with the exact verified wheel and sdist digests.
- Clean pip, uvx, and pipx paths install or execute version 0.1.0 outside the repository.
- No npm action or publication occurs.
risks:
- First-use pending-publisher OIDC matching may fail and require correction in the authenticated PyPI UI.
- Published registry bytes cannot be replaced; an incorrect release must be yanked and superseded.
decisions:
- Publish PyPI only and defer npm.
- Use the exact immutable GitHub Release and candidate source identity; do not rebuild.
verification:
- Observe every workflow job and protected deployment result.
- Compare PyPI file digests with the immutable GitHub Release assets.
- Exercise clean pip, uvx, and pipx commands without relying on the checkout.
next_action: Close the 0.1.0 PyPI release; keep npm deferred and return to WORK-019 shaping only when the next release is opened.
security_considerations:
- Use OIDC only; do not introduce or expose registry tokens.
- Preserve protected-environment review and least-privilege workflow permissions.
recovery:
- On OIDC or validation failure, stop without retrying blindly and correct only the mismatched configuration.
- On incorrect publication, preserve evidence, stop further publication, and make an explicit yank/superseding-release decision.
evidence:
- EVIDENCE-021
---

# Execution plan

1. Reconfirm immutable release identity, current main, absent publish run, and PyPI name state.
2. Dispatch one PyPI-only workflow with the exact confirmation and candidate SHA.
3. Observe validation, environment approval, OIDC publication, and workflow conclusion.
4. Verify PyPI files and clean installation paths.
5. Reconcile memory and close 0.1.0 with npm deferred.
