---
solodeveling_schema: 1
id: WORK-025
title: Narrow Docs-only CI Path
status: verifying
level: standard
type: change
goal: Reduce verified docs-only pull-request and main-push CI time without weakening tests for documentation contracts or broad gates for product changes.
scope: Add a docs-only classifier for changes entirely under docs/**, one Ubuntu docs job with the full Python test suite and range-aware diff checking, fail-safe mixed-change routing, regression coverage, GitHub confirmation, and one real docs-only dogfood change.
out_of_scope: README.md, root Markdown, skills, source, tests, workflows, packages, release behavior, npm publication, schema changes, and any change to v0.1.0.
acceptance:
- Changes entirely under docs/** select docs-only and do not select memory-only.
- Empty, malformed, README, root Markdown, memory-plus-docs, skill, source, test, workflow, package, and mixed changes select the full gate.
- The docs-only job runs the complete Python regression suite on Ubuntu and checks the exact base-to-head diff for whitespace errors.
- Full test, package, native, npm, main-push, pull-request, and v* tag behavior remains fail-safe for every non-docs-only change.
- Automated classifier and workflow-policy regressions pass together with the full local gate.
- A GitHub-hosted docs-only PR and its main merge run select only changes and docs-only while broad jobs are skipped.
- Candidate v0.1.0 remains unchanged at 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
risks:
- An over-broad docs allowlist could skip packaging or runtime checks for files that affect distributed behavior.
- A shallow checkout or wrong comparison base could make diff checking ineffective.
- Documentation contract tests could be missed if the focused job ran only selected tests.
decisions:
- Allow only docs/** in the first docs-only path; README.md and all other root Markdown remain full-gate inputs.
- Run the entire Python test suite rather than maintaining a fragile docs-test list.
- Use the same verified base SHA logic as classification and fetch complete history for range-aware diff checking.
- Mixed memory and docs changes fall back to full CI rather than combining fast paths.
verification:
- Add failing classifier and workflow-policy regressions before implementation.
- Run focused CI-policy tests, the complete local Python suite, skill and protocol validation, compile, dependency health, YAML parsing, and diff checks.
- Confirm docs-only routing on GitHub for both pull request and main push.
next_action: Confirm the implementation through full GitHub PR and main CI, then dogfood a docs-only PR and record evidence.
security_considerations:
- Keep least-privilege contents-read permissions and pinned GitHub Actions.
- Treat unknown, malformed, empty, and mixed paths as full-gate inputs.
recovery:
- Revert docs-only classification and job conditions together to restore all changes to the full gate.
evidence: []
---

# Plan

1. Extend classifier tests for docs-only, exclusions, mixed paths, and dual outputs.
2. Add docs-only output and fail-safe classification without broadening memory-only.
3. Add one range-aware Ubuntu docs job and exclude both fast modes from broad jobs.
4. Run focused and full local gates, then deliver through a full-gate implementation PR.
5. Dogfood with one eligible docs-only correction and capture GitHub PR/main timing.
