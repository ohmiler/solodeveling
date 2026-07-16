---
solodeveling_schema: 1
id: EVIDENCE-021
work_item: WORK-021
claim: Solodeveling 0.1.0 was published to PyPI through the protected OIDC workflow from the exact immutable candidate release, exposes matching wheel and sdist digests plus public provenance, and installs successfully through clean pip, uvx, and pipx paths while npm remained skipped and unpublished.
method: PyPI-name preflight, exact publish.yml dispatch and protected-environment approval, complete workflow observation, PyPI JSON and Integrity API inspection, immutable-asset digest comparison, clean temporary pip/uvx/pipx installation and execution, and npm registry inspection.
command: gh workflow run/watch/view 29487808952; approve pypi pending deployment 18217281990; PyPI JSON and Integrity API requests; clean pip install, uvx, pipx run, and pipx install for solodeveling==0.1.0; npm registry lookup.
result: passed
scope: PyPI project solodeveling version 0.1.0, candidate source commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4, workflow run 29487808952, wheel and sdist, and Windows Python 3.14 smoke environments.
limitations:
- npm was intentionally skipped and the package remains unpublished there.
- Smoke execution covered one local Windows/Python environment; it does not replace the existing cross-platform candidate and CI evidence.
- Native executables remain unsigned by platform-specific code-signing identities.
---

# Evidence

## Authorized publication

- Before dispatch, PyPI returned 404 for solodeveling and publish.yml had no prior
  runs.
- Exactly one workflow run, 29487808952, executed from current protected main while
  naming version 0.1.0 and source revision
  700a9b9dafc877507232b84a94ff3d6eaf7afda4.
- The validation job reverified the exact tag, immutable GitHub Release, complete
  release set, hashes, inventory, and attestations.
- The owner-approved pypi environment deployment published through OIDC. The
  publish-pypi job succeeded and publish-npm was skipped.

## PyPI integrity and provenance

- PyPI exposes solodeveling 0.1.0 with exactly the expected wheel and sdist.
- Wheel digest:
  b6c7c51a3c780925384f4e774e1dd73cf85e13ab6b7d727076354e694791988e.
- Source distribution digest:
  aa9ce8bc7e1b493958f0bc99e53fee3a3a9f503f70e8363a5177d06ce93c12a6.
- Both digests match the immutable GitHub Release assets.
- PyPI Integrity API provenance endpoints returned HTTP 200 for both files.

## Clean installation smoke

- A clean temporary virtual environment installed solodeveling==0.1.0 from PyPI
  without cache and reported solodeveling 0.1.0.
- uvx --no-cache from the exact version reported solodeveling 0.1.0.
- A temporary pipx host successfully exercised both pipx run and pipx install; the
  installed command reported solodeveling 0.1.0.
- The npm registry continued to return 404 for solodeveling.
