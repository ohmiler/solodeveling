---
solodeveling_schema: 1
id: WORK-009
title: Unify the Solodeveling name and installation experience
status: done
level: critical
type: change
goal: Give every user one public name and command, solodeveling, with easy Python and Node.js installation paths that run the same canonical implementation.
scope: Rename the unpublished Python distribution and console entry point, add unified CLI subcommands, create a thin npm/npx launcher for verified native artifacts, add cross-platform binary builds, tests, CI, installation documentation, and non-publishing release preparation.
out_of_scope: Publishing to npm or PyPI, reserving registry names, creating a version tag or GitHub Release, configuring trusted publishers or registry credentials, downloading mutable latest assets, executing unverified binaries, or promising support for platforms not exercised by CI.
acceptance:
- The only public package and executable name is solodeveling; legacy split executables are absent from built package metadata.
- solodeveling exposes install, check, uninstall, init, validate, eval, and version while preserving existing behavior and exit codes.
- uvx solodeveling, uv tool install solodeveling, pipx install solodeveling, npm install -g solodeveling, and npx solodeveling are documented with copyable commands and honest prerequisites.
- The npm package contains no install lifecycle script and invokes the same canonical implementation through an exact-version platform binary whose SHA-256 is verified before execution.
- Unsupported platforms, network failures, corrupt downloads, unsafe manifest paths, and hash mismatches fail closed with actionable errors and never execute an unverified file.
- Native artifacts are built per supported operating-system and architecture, include required skills and evaluations, and pass installed smoke tests.
- Python and npm packages can be built and exercised locally without publishing, and CI verifies representative install and command flows.
- No npm/PyPI publication, tag, GitHub Release, trusted-publisher configuration, or production mutation occurs in WORK-009.
risks:
- A launcher that downloads executable code creates a supply-chain execution boundary.
- Duplicating the implementation in JavaScript and Python would cause behavioral and security drift.
- PyInstaller artifacts are platform-specific and may omit package resources without explicit collection and smoke tests.
- Registry-name availability can change before publication and is not guaranteed by a successful lookup.
- An npm package may install successfully before matching release assets exist unless the release process enforces version alignment.
decisions:
- Use solodeveling as the sole public command and both registry distribution names; retain solodeveling_protocol only as an internal Python import namespace.
- Remove unpublished legacy console entry points instead of carrying aliases into 0.1.0.
- Keep Python as the canonical implementation and make npm a dependency-free JavaScript launcher, not a second implementation.
- Avoid postinstall downloads; fetch only on explicit command invocation, verify a package-bundled exact-version manifest and SHA-256, cache atomically, then spawn without a shell.
- Initially support only the OS/architecture matrix built and smoke-tested in CI; return a clear fallback message elsewhere.
- Prepare publication workflows and evidence but stop at an explicit authorization boundary before external publication.
verification:
- Start with regression tests for unified parsing, package metadata, launcher platform mapping, hash verification, containment, caching, and failure behavior.
- Build and install Python wheel in an isolated environment and exercise every top-level command.
- Pack the npm package, install/run it from a local tarball, and exercise the launcher against local verified fixtures without registry publication.
- Build standalone binaries on the supported CI matrix and verify embedded skills/evaluation resources plus representative commands.
- Run the complete Python suite, Node tests, package-content inspections, dependency/security checks, protocol validation, and clean-diff review.
next_action: Review and integrate pull request 9; publication, tags, releases, attestations, and registry configuration remain separately authorized actions.
security_considerations:
- Never execute before digest verification; never use mutable latest URLs, shell command composition, PATH lookup for downloaded artifacts, or writable manifest-selected traversal paths.
- Bind npm version, release tag, asset names, sizes, and hashes; download to a temporary file and atomically promote only after validation.
- Do not store tokens, credentials, private paths, or environment inventories in package artifacts or logs.
- Future npm and PyPI publishing must use protected environments, OIDC trusted publishing, provenance, least permissions, and an explicit human checkpoint.
recovery:
- Keep the existing merged main commit as the last known-good state and isolate changes on feat/unified-cli-installation.
- Delete only launcher cache entries created for a failed exact version; never modify user projects during download/verification.
- If version or asset identity drifts, rebuild all packages and artifacts from the reviewed source commit rather than editing generated manifests.
- Do not publish partial ecosystems; release Python, npm, manifests, and native assets only from one reviewed version-bound release process.
evidence:
- EVIDENCE-009
---
# Implementation plan

1. Replace split Python entry points with a single dispatching solodeveling CLI and rename the unpublished distribution.
2. Add a dependency-free npm package whose solodeveling bin securely resolves, verifies, caches, and runs version-bound native artifacts.
3. Add reproducible platform binary construction and smoke tests for embedded resources and representative commands.
4. Update documentation and release validation for npm, npx, uvx, uv tool, pipx, and the unified command surface.
5. Run Critical verification, record evidence, and stop before any registry publication or external release mutation.
