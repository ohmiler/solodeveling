---
solodeveling_schema: 1
id: EVIDENCE-017
work_item: WORK-017
claim: The protected publication workflow can safely validate the verified 0.1.0 ancestor candidate from current main, reads its canonical dynamic version without executing candidate code, and rejects revisions outside the current workflow history while preserving all downstream release and registry gates.
method: Root-cause inspection, regression-first executable Git graph tests, real candidate validation, workflow structure assertions, YAML parsing, full local project verification, and GitHub push/pull-request CI matrices.
command: python -m pytest -q; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.cli .; python -m compileall -q src scripts tests; python -m pip check; PyYAML parse of publish.yml; python scripts/publication_gate.py against the real candidate and adversarial revisions; GitHub Actions runs 29454177208 and 29454180651.
result: passed
scope: Candidate ancestry and canonical-version validation in .github/workflows/publish.yml, scripts/publication_gate.py, focused publication regressions, release documentation, and unchanged downstream tag, immutable-release, artifact, attestation, permission, and environment gates.
limitations:
- publish.yml was not dispatched because no tag, GitHub Release, registry action, or publication workflow invocation was authorized; inline GitHub publication validation remains unexecuted end to end until a separately authorized action.
- actionlint was unavailable locally; the workflow was parsed with PyYAML and accepted in the repository while both complete GitHub CI matrices passed.
- The repair proves bounded input validation and ancestry behavior, not registry availability, first-use PyPI OIDC matching, npm bootstrap success, platform code signing, or categorical security.
---
# Evidence

## Confirmed root causes

- Candidate `700a9b9dafc877507232b84a94ff3d6eaf7afda4` is an ancestor of the
  current reviewed `main`, not its current HEAD after evidence-only commits.
- The former equality check required `source_revision == github.sha`, which made the
  verified candidate unusable from current protected `main`.
- The former package-version shell read expected static `project.version` in
  `pyproject.toml`, while the project canonically uses dynamic version metadata from
  `src/solodeveling_protocol/__init__.py`.

## Repair behavior

- The validation job first checks out the current workflow revision with full Git
  history and still requires `refs/heads/main`.
- The new gate validates exact SHA syntax, commit existence, candidate ancestry, and
  expected SemVer. It reads the candidate's canonical version through `git show` and
  Python AST parsing, without importing or executing candidate code.
- Exact tag target, immutable GitHub Release, asset verification, release-set hashes
  and inventory, provenance signer/source/ref, GitHub-hosted runner, least privilege,
  and protected `pypi`/`npm` environment checks remain present.

## Verification results

- Regression-first reproduction failed before `scripts/publication_gate.py` existed.
- Focused publication tests passed: 15 tests, including accepted ancestor and rejected
  descendant, unrelated, malformed, missing, version-mismatched, and executable
  version-source cases.
- Full local suite passed: 212 tests. Canonical skill validation, protocol validation,
  compilation, dependency health, YAML parsing, and diff whitespace review passed.
- The real 0.1.0 candidate passed against both the pre-repair main revision and the
  repair branch commit. Explicit descendant and missing revisions returned the
  expected rejection status.
- GitHub Actions push run 29454177208 and pull-request run 29454180651 passed the
  complete cross-platform CI matrix for commit
  `ae6ec6d1c35f3f4f6b2b40eb968e36335aa5e16d`.

## Authorization boundary

No `v0.1.0` tag, GitHub Release, publish workflow run, registry stage, environment
approval, token exchange, or publication was created. Fresh explicit tag authority
is required after this repair is merged and post-merge CI passes.
