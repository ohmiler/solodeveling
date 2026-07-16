---
solodeveling_schema: 1
id: EVIDENCE-036
work_item: WORK-036
claim: Public PyPI and npm 0.1.2 match the immutable candidate and pass clean pip and npx installation.
method: Release preflight, protected OIDC publication, npm staged review, public downloads, provenance checks, and isolated smoke tests.
command: gh release and run 29524805137; npm stage view/download/approve; PyPI Simple and Integrity APIs; pip install; npm view/pack; clean version/install/check.
result: passed
scope: Version 0.1.2, candidate SHA 00efc22a01daad1cddb544b4d97ffb6a45b283fc, candidate run 29521649767, publish run 29524805137, npm stage e02400e1-a1c1-41b2-b325-ec609d88d36d, and Windows fresh-install environments.
limitations:
- Native executables remain unsigned.
- Fresh functional checks ran on Windows; candidate CI covers other platforms.
- A cached pip index briefly lagged at 0.1.1; no-cache queries exposed 0.1.2.
---
# Evidence

- Run 29524805137 validated all 13 immutable assets, published PyPI through OIDC,
  and staged npm through trusted automation.
- Before approval, the 4,319-byte staged npm tarball matched candidate SHA-256
  8808631a727ec955caabcab24ef665b282d04363c48c1aa148212551cca14216 and
  SHA-1 ccf1ffee51384f9237de472f82ad579f4ed5e0c9.
- npm latest is 0.1.2, its staged list is empty, and the public tarball retains
  those exact digests.
- PyPI wheel SHA-256 is
  1c2b40c4168441c95679235e47aafbb5d561826f48a092138af2035b7039a92c.
- PyPI sdist SHA-256 is
  24f72fecaf28df85f5fb53004f957e607d7247f698a836fa0df57c1f7364b457.
  Both match the release and both provenance endpoints returned HTTP 200.
- A new Python 3.14 venv and a new npm cache each reported 0.1.2 in an empty
  project, installed 31 managed Codex files, and passed the conformant check.
