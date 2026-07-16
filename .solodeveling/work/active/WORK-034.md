---
solodeveling_schema: 1
id: WORK-034
title: Prepare verified release candidate 0.1.2
status: active
level: critical
type: release
goal: Produce and independently verify an exact non-publishing 0.1.2 release candidate
  from protected main.
scope: Version metadata, release notes, version-bound regressions, protected source
  delivery, complete 13-file release set, checksums, SBOM, and GitHub attestations.
out_of_scope: Tag creation, GitHub Release, PyPI publication, npm staging or publication,
  Pilot-4, and unrelated product changes.
acceptance:
- Python, npm, native filenames, manifests, SBOM, and release notes consistently identify
  0.1.2.
- Release notes accurately describe the compatible low-ceremony workflow changes and
  known limitations.
- Complete local, pull-request, and protected-main verification passes.
- The candidate workflow builds exactly 13 expected files from one exact protected-main
  SHA.
- Independent checksum, inventory, source identity, release-set, and attestation verification
  passes.
- No tag, GitHub Release, registry staging, or publication action occurs.
risks:
- Version drift could make the npm launcher request nonexistent native assets.
- Candidate artifacts could be confused with published or immutable release bytes.
- Native executables remain unsigned despite checksum and provenance verification.
decisions:
- Use 0.1.2 as a compatible patch because public commands and schema remain backward
  compatible.
- Keep 0.1.0 and 0.1.1 immutable and treat the candidate as disposable non-publishing
  input.
- Preserve historical 0.1.1 release notes, evidence, and benchmark pins unchanged.
verification:
- Run focused version, release, packaging, protocol, and documentation regressions.
- Run the complete Python and Node suites, validators, compilation, dependency, package,
  and native smoke gates.
- Merge through protected CI, dispatch release-candidate.yml for the exact main SHA,
  download all 13 files, and verify every attestation.
security_considerations:
- Bind candidate bytes, checksums, manifest, SBOM, attestations, workflow identity,
  and source revision exactly.
- Treat downloaded artifacts and attestations as untrusted until independently verified.
- Do not request or expose registry credentials, OTP values, or recovery codes.
recovery:
- Stop on any source, version, inventory, hash, SBOM, attestation, or workflow mismatch.
- Discard only disposable candidate output and rebuild the entire set from a newly
  reviewed exact main commit.
- Never repair a generated manifest or replace one candidate file after hashing.
next_action: Deliver the source boundary through protected CI, then dispatch the exact main candidate.
evidence:
- EVIDENCE-034
---
# Release boundary

This work authorizes source preparation and one non-publishing candidate workflow
from the exact protected-main commit produced by this work. Tag creation, GitHub
Release creation, PyPI, npm staging, and npm publication require separate explicit
authorization naming the exact candidate source and run.
