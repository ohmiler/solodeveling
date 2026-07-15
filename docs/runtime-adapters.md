# Runtime adapters

Solodeveling keeps one canonical suite in skills/. Adapters copy those bytes into a
runtime discovery path and record a hash manifest; they do not rewrite workflow
instructions or add runtime-only lifecycle rules.

## Evidence-based support

Checked 2026-07-15:

| Runtime | Adapter path | Explicit invocation | Current evidence |
| --- | --- | --- | --- |
| Codex | .agents/skills | $solodeveling | Structural adapter and canonical byte conformance pass. Live evaluation is pending. |
| Claude Code | .claude/skills | /solodeveling | Structural adapter and canonical byte conformance pass. Live evaluation is pending. |
| Cursor | .cursor/skills | /solodeveling | Structural adapter and canonical byte conformance pass. cursor-agent was unavailable in the verification environment, so live behavior is unverified. |
| Generic Agent Skills client | .agents/skills | Runtime-defined | Format and byte conformance pass; discovery behavior is client-specific. |

The paths and invocation forms follow the current
[Codex skill documentation](https://learn.chatgpt.com/docs/build-skills.md),
[Claude Code skill documentation](https://code.claude.com/docs/en/slash-commands),
[Cursor Agent Skills documentation](https://cursor.com/docs/skills), and
[Agent Skills specification](https://agentskills.io/specification). Recheck primary
documentation when discovery or invocation behavior affects a current decision.

Adapter conformance is not a Tier 1 behavioral claim. Tier 1 requires shared scenarios
to run successfully in the actual Codex, Claude Code, and Cursor agent surfaces.

## Install or update

Run from a checkout or distribution containing the canonical skills/ directory:

    solodeveling-adapt install --runtime codex --source ./skills --project-root .
    solodeveling-adapt install --runtime claude-code --source ./skills --project-root .
    solodeveling-adapt install --runtime cursor --source ./skills --project-root .

Use --runtime generic for a compatible client that discovers .agents/skills.
Preview without writes by adding --dry-run.

Installation validates every canonical SKILL.md, rejects source or target symlinks,
preflights all collisions, copies files atomically, and writes
.solodeveling-adapter.json inside the runtime skill root. Re-running install updates
only files still matching the prior managed manifest. It refuses modified managed
files and unmanaged collisions.

Installing several native adapters into one project creates separate copies. Some
runtimes may also scan compatibility paths, which can surface duplicate skill names.
Until live co-install evaluation is complete, install only the adapter paths actually
needed in that workspace and use check before switching runtime configuration.

## Check drift

    solodeveling-adapt check --runtime codex --source ./skills --project-root .

A successful check proves that managed files match their recorded hashes and the
canonical source digest at that moment. It reports missing, modified, unexpected, and
source-drifted content. Hash equality detects change; it does not prove publisher
identity, authenticity, safety, or behavioral compliance.

## Remove safely

Preview first:

    solodeveling-adapt uninstall --runtime codex --project-root . --dry-run

Then remove unchanged managed files:

    solodeveling-adapt uninstall --runtime codex --project-root .

Uninstall preflights every manifest path and hash. If any managed file is missing,
modified, replaced by a symlink, or outside the adapter root, it stops before deletion.
Unrelated skills and user files remain. Review modified files and recover or relocate
them explicitly; there is intentionally no force-delete option.

After adding a top-level skill directory, start a fresh agent session if the runtime
does not discover it. Claude Code documents live detection for existing skill roots
but requires restart when the top-level skills directory was absent at session start;
Codex also recommends restart when an update does not appear. Treat Cursor refresh
behavior as unverified until the live evaluation suite runs.
