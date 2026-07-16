---
solodeveling_schema: 1
current_goal: Preserve the completed cross-ecosystem 0.1.0 release and select the next separately authorized improvement.
active_work: []
blockers: []
risks:
- Published npm and PyPI version 0.1.0 plus immutable GitHub Release assets cannot be replaced with different bytes.
- Native executables remain unsigned; launcher integrity checks reduce substitution risk but do not provide platform code signing.
next_action: Choose the next work item separately; later npm releases must use stage-only Trusted Publishing and owner approval.
---
# State

WORK-026 and EVIDENCE-026 record public npm publication from the exact immutable
release tarball, byte-for-byte registry verification, clean npm and npx journeys,
and owner-confirmed stage-only Trusted Publishing with traditional tokens disallowed.
PyPI and npm now both distribute 0.1.0. GitHub Release v0.1.0 remains immutable at
candidate commit 700a9b9dafc877507232b84a94ff3d6eaf7afda4.
