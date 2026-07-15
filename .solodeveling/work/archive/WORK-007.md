---
solodeveling_schema: 1
id: WORK-007
title: Prepare portable public packaging and installation UX
status: done
level: critical
type: release
goal: Make Solodeveling installable and verifiable from a built distribution outside the repository, with clear multi-runtime onboarding, secure CI, reproducible release inputs, and evidence-bounded support claims.
scope: Bundled canonical skills and evaluation resources, package-resource resolution, source override compatibility, isolated wheel and sdist installation tests, repository README and runtime quickstarts, complete package metadata, version consistency, least-privilege CI, release artifact inventory and checksums, documentation reconciliation, and release-readiness evidence.
out_of_scope: Publishing to PyPI, creating or pushing a version tag, creating a GitHub Release, merging branches, changing repository visibility, claiming complete Tier 1 support, installing globally into user projects, collecting telemetry, or introducing a required subagent workflow.
acceptance:
- A fresh wheel and sdist contain every canonical skill file, required evaluation scenario/schema, Python module, template, and schema with an explicit inventory test.
- solodeveling-adapt install and check default to immutable packaged canonical skills while preserving an explicit --source override for repository development and audits.
- solodeveling-eval defaults to packaged scenarios, response schema, and canonical skills while allowing explicit local overrides; local result output remains outside package resources.
- An isolated virtual environment can install the wheel, run all console entry points from outside the checkout, install/check/uninstall each runtime adapter safely, and validate byte identity against the packaged canonical suite.
- Repository-level onboarding explains the single-agent-first model, supported runtimes, evidence tiers, prerequisites, safe install/check/uninstall, upgrade, recovery, and current limitations without duplicating skill instructions.
- Package metadata includes a readme, author identity supplied by the repository owner where available, project URLs, keywords, classifiers, supported Python versions, and one authoritative version check.
- CI runs tests, official skill validation, protocol validation, package build, artifact inspection, and isolated installed smoke checks with least privilege and pinned third-party actions.
- A local release command creates wheel and sdist artifacts plus a deterministic manifest and SHA-256 checksums without publishing, signing, or overwriting an existing release directory.
- Release readiness records dependency, security, provenance, recovery, platform, and support-claim limitations; no publication occurs automatically from an unreviewed branch.
- Critical completion passes full regression, all ten official skill validations, protocol validation, isolated package tests, fresh build inspection, compilation, dependency health, and diff checks.
risks:
- Bundled resources can drift from repository canonical files or be omitted by one distribution format.
- Public dependency ranges or package metadata can create conflicts, misleading compatibility claims, or supply-chain exposure.
- Installation automation can overwrite user skills or make unsafe removal appear easier than it is.
- CI and release workflows can gain excessive token permissions or publish from untrusted code if designed carelessly.
- The stacked feature history is not merged into main, so release publication is premature.
decisions:
- Treat repository skills as canonical inputs and verify byte identity inside every built distribution rather than maintaining a second hand-copied suite.
- Resolve packaged resources through Python importlib.resources and materialize only when an existing filesystem API requires a stable Path.
- Keep explicit local source overrides for contributors, audits, and forward development.
- Provide one package-driven installation path across Codex, Claude Code, Cursor, and generic Agent Skills clients; runtime differences remain adapter mappings only.
- Build and verify release artifacts locally and in CI, but require separate human authority for merge, tag, release, signing, or registry publication.
- Keep runtime execution single-agent-first; packaging and CI correctness never depend on subagents.
verification:
- Start with failing wheel-content, resource-default, override, isolated-install, metadata, documentation, CI, and release-bundle tests.
- Build wheel and sdist in a fresh directory and inspect exact resource inventories and console entry points.
- Install the wheel into a fresh isolated environment outside the checkout and exercise init, validate, adapt, and eval dry-run commands.
- Test safe adapter install/check/uninstall for all runtime mappings against disposable projects and confirm unrelated files survive.
- Run full tests, suite and official skill validators, protocol validation, compilation, dependency health, and staged diff checks.
next_action: Review pull request 7, then explicitly authorize integration into main; tagging, signing, GitHub Release creation, and PyPI publication remain separate decisions.
security_considerations:
- Do not embed credentials, user paths, live evaluation output, repository tokens, or mutable external downloads in package resources.
- Pin CI actions to reviewed commit SHAs, grant minimum permissions, avoid pull-request secret access, and never execute untrusted artifacts with publication credentials.
- Preserve adapter collision, symlink, containment, atomic-copy, drift, and safe-uninstall controls when changing resource defaults.
- Treat checksums and inventories as integrity evidence, not publisher identity or cryptographic signing.
recovery:
- Keep release builds in new explicit output directories and refuse overwrite so failed builds can be discarded safely.
- Preserve --source for rollback to repository resources and keep installed manifests sufficient for drift checks and safe uninstall.
- On package smoke failure, discard only the temporary environment and project; never modify canonical skills or user runtime directories.
- Do not tag, publish, release, or merge until the reviewed commit and recorded artifact hashes are explicitly authorized.
evidence:
- EVIDENCE-007
---
# Implementation plan

1. Define package-resource, installed-CLI, metadata, documentation, CI, and release-artifact contracts with failing tests.
2. Bundle canonical resources without semantic forks and make CLI defaults distribution-aware.
3. Add public onboarding, package metadata, secure CI, and a local non-publishing release builder.
4. Verify wheel and sdist from isolated environments on available platforms and record unavailable coverage honestly.
5. Record Critical evidence, reconcile project memory, commit, and push for review without publishing.
