# Contributing

Solodeveling is single-agent-first: ordinary development must remain correct with one
primary coding agent and cannot require subagents. Contributions should preserve one
canonical skill suite across runtimes and keep support claims bounded by recorded
evidence.

## Development setup

```console
git clone https://github.com/ohmiler/solodeveling.git
cd solodeveling
python -m pip install ".[dev]"
python -m pytest -q
python scripts/validate_skill_suite.py
python -m solodeveling_protocol.cli .
```

Run the official `quick_validate.py` from the current skill-creator tool against all
ten skill directories when that tool is available. Do not download and execute a
validator from an unreviewed source merely to satisfy a check.

## Change discipline

- Start from a shaped work item with explicit scope, risk, verification, security, and
  recovery fields.
- Preserve user changes and avoid unrelated formatting or generated-file churn.
- Add failing tests before behavior changes and include adversarial cases for unsafe
  paths, secrets, authority, recovery, and completion claims.
- Keep detailed runtime or standards material in references or repository docs rather
  than duplicating it across `SKILL.md` files.
- Do not add telemetry, credentials, automatic publication, force-delete behavior, or
  required subagent delegation.
- Record live-agent cost limits, versions, failures, and unavailable coverage without
  weakening rubrics to manufacture a pass.

## Package and release checks

Build into a new output directory and verify it without publishing:

```console
python scripts/build_release.py ./local-release
python scripts/verify_release.py ./local-release
```

Install the wheel in a fresh virtual environment and run
`scripts/smoke_installed.py` outside the checkout. A release, tag, merge, signature,
attestation, registry upload, or repository metadata change requires separate review
and authority.
