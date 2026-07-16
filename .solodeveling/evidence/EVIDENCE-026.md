---
solodeveling_schema: 1
id: EVIDENCE-026
work_item: WORK-026
claim: Exact verified solodeveling@0.1.0 is publicly installable from npm under the intended owner, with later automation restricted to owner-reviewed staged publishing from the protected GitHub workflow.
method: Owner-controlled 2FA bootstrap publication from the immutable GitHub Release tarball; full release-set, asset digest, and strict attestation verification; npm dry-run and registry byte comparison; clean install and npx smoke; GitHub environment inspection; and owner inspection of security-key-protected npm package settings.
command: python scripts/verify_release_set.py; python scripts/prepare_publication.py; gh release verify; gh release verify-asset and gh attestation verify for all 13 assets; npm publish --dry-run; owner-interactive npm publish; npm view; npm install; npx solodeveling version; npm access get status; gh api environment inspection
result: passed
scope: Public npm package solodeveling@0.1.0, exact immutable release tarball, npm ownership and registry integrity, clean Windows launcher journey, GitHub npm environment, stage-only Trusted Publisher claims, token restriction, and unchanged candidate boundary.
limitations:
- Trusted Publisher claims and Require two-factor authentication and disallow tokens were inspected and confirmed by the owner in npm's security-key-protected UI; post-save machine-readable inspection was not retained because npm requires fresh proof-of-presence and no controllable signed-in browser backend was available.
- The owner-controlled bootstrap publication does not carry OIDC-generated npm provenance; later releases are configured to use staged Trusted Publishing before owner approval.
- Native executables remain unsigned; the npm launcher verifies the exact versioned asset SHA-256 and size before execution.
---

# Results

- npm account `ohmiler` was authenticated with `auth-and-writes` 2FA. The unscoped
  package name and version were absent immediately before the one authorized publish.
- Immutable GitHub Release `v0.1.0` and all 13 assets passed release, manifest,
  checksum, inventory, asset-digest, and strict GitHub attestation verification for
  source commit `700a9b9dafc877507232b84a94ff3d6eaf7afda4`.
- The sole npm input was `solodeveling-0.1.0.tgz` with SHA-256
  `d236ad78127e28e860e310ee0557bccee60d0c8e7347216e6662db8d72e2e661`.
  Preparation preserved identical bytes. Dry-run reported exact name/version and only
  `README.md`, `artifacts.json`, `bin/solodeveling.js`, `lib/launcher.js`, and
  `package.json`.
- Owner-interactive publication completed once at `2026-07-16T11:21:09.293Z` without
  an npm automation token. Registry integrity
  `sha512-fw3MSDpolvI1vDkOStqJ7YlMC12FSJ8qk00fN+gtnI9VGMlrZjWQuKIOPUPzMfff9ttDldFPrtO38FKbcEa0ig==`
  and shasum `dd80a2c4edb2e50ab23ab02c5c7ef02b73461de2` matched the local verified bytes;
  maintainer `ohmiler`, repository metadata, and public access also matched.
- Clean `npm install` and clean `npx --package=solodeveling@0.1.0` both downloaded the
  matching Windows native release asset and reported `solodeveling 0.1.0`.
- GitHub environment `npm` retains reviewer `ohmiler`, exact branch policy, no admin
  bypass, and no secret-based publication. The owner configured and inspected npm
  Trusted Publishing for repository `ohmiler/solodeveling`, workflow `publish.yml`,
  environment `npm`, stage-only permission, plus disallowed traditional publishing
  tokens.
- `v0.1.0^{}` remains exact candidate commit
  `700a9b9dafc877507232b84a94ff3d6eaf7afda4`; no artifact, source, tag, GitHub
  Release, PyPI package, or candidate content was replaced.
