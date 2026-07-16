---
solodeveling_schema: 1
id: EVIDENCE-034
work_item: WORK-034
claim: Solodeveling 0.1.2 source preparation passes the complete local release gate
method: Focused and complete regressions, package build and install smoke, Windows
  native build and smoke, protocol and skill validation
command: python -m pytest -q; npm.cmd test --prefix packages/npm; python scripts/validate_skill_suite.py;
  python -m solodeveling_protocol.main_cli validate .; python -m compileall -q src
  tests scripts; python -m pip check; python -m build; python scripts/build_native.py;
  python scripts/smoke_native.py
result: passed
scope: 0.1.2 version metadata, release notes, Python and npm packages, native executable,
  lifecycle resources, and non-publishing source boundary
limitations:
- Protected pull-request and main CI have not run for this source change yet.
- The exact 13-file candidate and GitHub attestations do not exist until after protected-main
  merge.
- No tag, GitHub Release, PyPI, or npm action was run.
---
# Evidence

## Solodeveling 0.1.2 source preparation passes the complete local release gate

- Method: Focused and complete regressions, package build and install smoke, Windows native build and smoke, protocol and skill validation
- Result: passed
- Scope: 0.1.2 version metadata, release notes, Python and npm packages, native executable, lifecycle resources, and non-publishing source boundary
- Command: python -m pytest -q; npm.cmd test --prefix packages/npm; python scripts/validate_skill_suite.py; python -m solodeveling_protocol.main_cli validate .; python -m compileall -q src tests scripts; python -m pip check; python -m build; python scripts/build_native.py; python scripts/smoke_native.py
- Limitations:
  - Protected pull-request and main CI have not run for this source change yet.
  - The exact 13-file candidate and GitHub attestations do not exist until after protected-main merge.
  - No tag, GitHub Release, PyPI, or npm action was run.
