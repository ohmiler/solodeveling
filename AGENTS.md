# Agent Instructions

These instructions apply to the entire repository. See `CONTRIBUTING.md` for the
full development and release guidance.

## Working model

- Keep ordinary development correct with one primary agent. Use subagents only when
  the user explicitly requests delegation.
- Preserve user changes and avoid unrelated formatting, generated-file churn, or
  destructive Git operations.
- Use the Solodeveling workflow for project mutations and work that must survive a
  session. Handle bounded read-only questions inline without creating lifecycle
  artifacts.
- Keep reversible, well-understood Quick work ephemeral. Use `.solodeveling/` only
  when work is tracked or a durable decision must be preserved.

## Skill sources and runtime copies

- Treat `skills/` as the canonical, Git-tracked skill suite.
- Treat `.agents/skills/` as a local managed runtime copy. Do not edit or commit it.
- After changing canonical skills, update runtime copies through the installer and
  verify them instead of copying or rewriting files by hand.
- Keep detailed runtime and standards material in references or repository docs
  rather than duplicating it across `SKILL.md` files.

## Verification

Run focused checks for the changed boundary. The main repository checks are:

```console
python -m pytest -q
python scripts/validate_skill_suite.py
python -m solodeveling_protocol.cli .
```

Do not claim work is complete, fixed, passing, secure, or ready without recent,
scoped evidence. Record unavailable checks and narrow the claim accordingly.

## Authority boundaries

- Do not add telemetry, credentials, automatic publication, force-delete behavior,
  or required subagent delegation.
- Do not commit, push, merge, tag, publish, sign, attest, or change repository
  metadata unless the user explicitly authorizes that action.
- Treat release and production-changing actions as separate decisions requiring
  explicit authority.
