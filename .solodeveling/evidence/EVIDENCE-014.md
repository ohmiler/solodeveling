---
solodeveling_schema: 1
id: EVIDENCE-014
work_item: WORK-014
claim: Repository release immutability is enabled and the pypi/npm GitHub environments require owner review and exact main-only deployment policy without secrets, variables, release artifacts, or publication activity.
method: Baseline and post-change GitHub REST API inspection with explicit assertions; repository tag, release, and workflow-run absence checks; project-memory and documentation verification.
command: gh api repos/ohmiler/solodeveling/immutable-releases; gh api repos/ohmiler/solodeveling/environments/{pypi,npm}; gh api deployment-branch-policies, environment secrets, and environment variables endpoints; git ls-remote --tags origin; gh release list; gh run list --workflow release-candidate.yml; gh run list --workflow publish.yml; python -m pytest -q; npm test --prefix packages/npm; python -m compileall -q src tests scripts; python -m pip check; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.main_cli validate .; git diff --check.
result: passed
scope: GitHub repository immutable-release setting; pypi and npm required reviewer, self-review, custom branch policy, secret and variable inventory; absence of tags, releases, candidate runs, and publication runs.
limitations:
- GitHub reports can_admins_bypass true for both environments. Ordinary deployments require reviewer action, but a repository administrator can explicitly bypass protection; the documented REST API cannot change this field and no browser backend was available.
- Environment configuration does not create PyPI or npm Trusted Publishers, reserve package names, sign native executables, or verify registry authentication.
- No candidate, tag, GitHub Release, attestation, registry staging, approval, or publication was invoked.
---
# Evidence

## Baseline

- Repository `ohmiler/solodeveling` was public, default branch `main`, and the
  authenticated `ohmiler` account had admin permission.
- Immutable releases reported `enabled: false`; no environments existed; `main` had
  no branch protection rule; no tag or GitHub Release existed.

## Applied and verified

- `PUT /repos/ohmiler/solodeveling/immutable-releases` succeeded and a fresh GET
  reported `enabled: true` and `enforced_by_owner: false`.
- Environments `pypi` and `npm` each contain one required-reviewer rule for GitHub
  user `ohmiler` (ID 11663259), with `prevent_self_review: false`.
- Both environments use custom deployment branch policies and each policy list
  contains exactly one branch entry: `main` of type `branch`.
- Both environment secret and variable inventories reported zero entries.
- Fresh remote tag and GitHub Release lists were empty. Candidate and publish workflow
  run lists were also empty.

## Local verification

- Focused release, candidate, publication, release-set, and installation-documentation
  tests: 39 passed.
- Full Python suite: 203 passed.
- Node launcher suite: 8 passed and 1 skipped because file symlinks were unavailable
  in the local Windows environment.
- Compilation, dependency health, canonical skill-suite validation, project-memory
  validation, and diff whitespace review passed.
- Pull-request GitHub Actions run 29448771069 passed the cross-platform Python,
  package, six-native-target, and npm pack/npx matrix at commit
  `aa5e85cda0a98f8d9bbb630c4c9ff42abc252c26`.

## Security and recovery

- The exact main-only rule prevents environment deployment from other branches.
- Owner review provides an intentional manual checkpoint while allowing the solo
  owner to approve their own initiated workflow.
- GitHub's default `can_admins_bypass: true` remains visible as a residual recovery
  path. Disabling it requires an authenticated UI action not available in this run.
- Recovery endpoints and the original absent/disabled baseline are recorded in
  WORK-014; no automatic rollback is appropriate after successful verification.
