---
solodeveling_schema: 1
id: EVIDENCE-007
work_item: WORK-007
claim: Solodeveling 0.1.0 can be built as a portable wheel and source distribution whose bundled canonical skills and evaluation resources are verified byte-for-byte, installed outside the checkout, exercised through all console entry points and runtime adapter mappings, and checked by least-privilege cross-platform CI without publishing.
method: Resource inventory and identity tests, distribution build and archive inspection, deterministic manifest and SHA-256 verification, fresh virtual-environment installation outside the checkout, installed command and safe adapter lifecycle smoke tests, full regression, suite and official skill validation, protocol validation, compilation, dependency health, dependency vulnerability audit, diff inspection, and GitHub Actions on Windows, Linux, and macOS with Python 3.10 and 3.14.
command: python -m pytest -q; python scripts/validate_skill_suite.py; quick_validate.py for all ten skills; python -m solodeveling_protocol.cli .; python scripts/build_release.py C:\tmp\solodeveling-work007-final-1d6a22d; python scripts/verify_release.py C:\tmp\solodeveling-work007-final-1d6a22d; install the exact wheel into a fresh Python 3.14 virtual environment; python scripts/smoke_installed.py from C:\tmp; compileall; pip check; git diff --check; GitHub Actions push and pull_request CI.
result: passed
scope: Packaged defaults and explicit source overrides, all ten canonical skills, evaluation scenarios and schemas, four console entry points, Codex, Claude Code, Cursor, and generic Agent Skills adapter mappings, collision and safe-uninstall behavior, public package metadata, non-publishing release construction, secure pinned CI, Windows installed smoke, Ubuntu package smoke, and regression matrices across three operating systems.
limitations:
- Pull request 7 remains open and the stacked feature history is not merged into main.
- No version tag, GitHub Release, PyPI upload, signature, provenance attestation, or SBOM was created.
- The local installed-distribution smoke used Windows with Python 3.14; CI's package job used Ubuntu with Python 3.14. macOS ran the regression and protocol matrix but not the installed-package smoke job.
- CI directly covers Python 3.10 and 3.14, not every intermediate supported Python minor version.
- Cursor live behavioral evaluation and the complete Tier 1 matrix remain unverified; adapter packaging success is not a Tier 1 behavior claim.
- PyPI name availability and vulnerability data are time-sensitive and must be rechecked from the exact release commit before publication.
---
# Verification summary

On 2026-07-15, 141 tests passed locally. The suite validator, all ten official
skill validations, protocol validation, compilation, dependency health, and diff
checks passed. GitHub Actions push run 29425874350 and pull-request run 29425877305
both passed all seven jobs: six test combinations across Windows, Ubuntu, and macOS
with Python 3.10 and 3.14, plus the Ubuntu package build, verification, installed
smoke, and artifact upload job. Third-party actions use reviewed full commit SHAs and
the workflow grants only `contents: read`.

The final local bundle was built from commit 1d6a22d and passed
`verify_release.py`. The wheel SHA-256 is
`6055590863c021ac28839ea996703081e22fbaa445f6753519bb47a988c30a93`; the source
distribution SHA-256 is
`9672053da1559464b0131f075946267482397bb9cd900612826218f92fc89354`. Installing
that exact wheel and its dependencies into a fresh Python 3.14 virtual environment
outside the checkout passed init, validation, evaluation dry-run, and safe
install/check/uninstall smoke tests for every runtime adapter mapping.

## Security and recovery evidence

The release builder refused overwrite, built in temporary staging, accepted only
reviewed repository roots, rejected symlinked files, emitted exactly one wheel and
one source distribution, and never published. The verifier checked artifact hashes,
sizes, duplicate archive entries, canonical resource bytes, metadata, entry points,
and absence of evaluation results. `pip-audit` 2.10.1 reported no known
vulnerabilities in installed dependencies; the unpublished project itself was
skipped because it was not on PyPI. Checksums remain integrity evidence rather than
publisher identity. Recovery is deletion of only the disposable bundle, virtual
environment, and smoke project; canonical repository skills and user runtime paths
were not modified.