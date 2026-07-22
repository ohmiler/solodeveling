# Release readiness

This document defines the current non-publishing candidate and public-release gates
for Solodeveling. Ordinary CI verifies source, packages, six native targets, and npm
packaging; it does not publish, tag, create a GitHub Release, or mutate a registry.

## Local candidate gate

1. Run the full Python suite, skill-suite validation, protocol validation,
   compilation, dependency checks, Node launcher tests, and diff review.
2. Build the current-platform executable into a new path:

       python scripts/build_native.py C:/tmp/solodeveling-native-0.3.0

3. Exercise embedded templates, schemas, skills, evaluations, and unified commands:

       python scripts/smoke_native.py C:/tmp/solodeveling-native-0.3.0 C:/tmp/native-smoke-0.3.0

4. Build the Python candidate from a clean exact commit and verify its checksums,
   contents, SBOM, release notes, and manifest.
5. Verify that installed wheel and native resources include every canonical skill,
   including `solodeveling-brainstorming`, and run the representative routing
   scenarios against the exact candidate bytes.
6. Review manifests and SHA-256 values. Integrity hashes are not signatures,
   attestations, or proof of publisher identity.

Builders refuse unsafe or existing destinations, require exact inventories, use
temporary staging, and never upload to a registry.

Python 3.10 and 3.14 remain the supported CI bounds. Candidate invocation, tag
creation, GitHub Release creation, environment changes, PyPI publication, npm
staging, and npm publication are each a separate external action and authorization
checkpoint.

## 0.3.0 preparation status — 2026-07-22

- The next feature release is isolated locally on `release/0.3.0`. Commit `26f0ac5`
  contains the pinned no-skill benchmark harness; commit `0429dba` contains the
  frontend and backend workflow-feedback implementation.
- Clear non-Critical Standard work now has one combined delivery workflow. Backend
  work has fail-closed Quick routing, one shared boundary record, effect-specific
  gates, capability-aware triage, and an additive migration template.
- The 30-call Solodeveling 0.2.0-versus-no-skill pilot is preregistered and passed
  offline fixture checks. It has not run, is not a 0.3.0 release gate, and provides
  no comparative result or public performance claim.
- Exact source revision d0e9bcbaef88b301561fe4f6a530e0897378b2c9 passed
  281 Python tests, skill/protocol validation, npm tests, compilation, dependency
  checks, diff review, fresh-wheel installed smoke, and candidate verification.
- Tenant policy denied the three-call live routing pilot before execution even after
  informed owner approval. On 2026-07-22 the owner accepted the missing live evidence
  only for local candidate construction; the gap remains unverified.
- Python, npm, artifact, native-output, current-version tests, and release notes are
  being advanced together to 0.3.0 under that bounded local-candidate acceptance.
- The verified Python candidate contains wheel SHA-256
  e8898b324edf33978e01905396702d1841f892cc21c1b281f509ddacd4b41f67
  and sdist SHA-256
  8bc9ae2cec4e9e7e0dedaa7be21f466e3484ee76a89a3242cb3cc824db060c0e.
  The Windows x64 native smoke passed for SHA-256
  cab76a3c49af00beef50fcbfa2e5549aebfdcb46bcae51295a807ad765e4957f.
- No push, pull request, tag, GitHub Release, registry action, live-agent call, or
  production mutation is authorized by this preparation.

Tier 1 remains unverified because the complete behavioral matrix has not passed on
Codex, Claude Code, and Cursor. Native executables remain unsigned.

## Remaining 0.3.0 gates

- Resolve the missing live routing evidence in an approved environment or obtain a
  new explicit release-level risk acceptance before tag or publication. The current
  acceptance expires when local candidate inspection ends.
- Complete the cross-platform CI candidate so all six native executables can be bound
  into the npm tarball and complete release set.
- Continue dogfooding representative tasks while recording tool calls, memory writes,
  broad-gate runs, reopen/archive counts, elapsed verification time, and escaped
  regressions. Any Critical under-classification blocks release.
- Reconcile source behavior, release notes, package inventories, checksums, SBOM,
  scenario results, and known limitations.
- Confirm the protected PyPI and npm environments and trusted-publisher identities
  still match `publish.yml` before any registry action.
- With separate explicit authority, create tag `v0.3.0` at the verified source
  revision and create the immutable GitHub Release from that exact candidate.
- With another explicit authority checkpoint, publish PyPI and stage or publish npm.
  Complete clean-environment post-publication smoke checks before announcing the
  release.

## Complete release-set gate

After all upstream checks pass, assemble the coordinated non-publishing input from
one exact source revision:

    python scripts/assemble_release_set.py <candidate> <native> <npm-tarball> <release-set> --source-revision <sha>
    python scripts/verify_release_set.py <release-set> --source-revision <sha>

`release-set-manifest.json` must describe exactly two Python distributions, six
native executables, one npm tarball, one CycloneDX SBOM, and release notes. The
verifier recomputes size and SHA-256, checks the flat inventory, validates the npm
archive without extraction, and requires its platform manifest to match all six
native bytes. This gate provides bounded integrity and provenance input; it is not
publication, platform signing, or Tier 1 behavior proof.

Recovery before publication is to discard only disposable output and rebuild the
entire set from the reviewed commit. Do not edit a generated manifest or replace an
individual artifact. Candidate invocation, tag creation, GitHub Release creation,
PyPI publication, npm staging, and npm publication remain separate authorization
checkpoints.
