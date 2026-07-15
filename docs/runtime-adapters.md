# Runtime adapters

Solodeveling keeps one canonical suite in `skills/`. Built distributions map those
exact bytes into packaged resources. Adapters copy the packaged bytes into a runtime
discovery path and record a hash manifest; they do not rewrite workflow instructions
or add runtime-only lifecycle rules.

## Evidence-based support

Checked 2026-07-15:

| Runtime | Adapter path | Explicit invocation | Current evidence |
| --- | --- | --- | --- |
| Codex | `.agents/skills` | `$solodeveling` | Structural byte conformance and one bounded representative live scenario pass. |
| Claude Code | `.claude/skills` | `/solodeveling` | Structural byte conformance and one bounded representative live scenario pass after response-contract clarification. |
| Cursor | `.cursor/skills` | `/solodeveling` | Structural byte conformance passes. `cursor-agent` was unavailable, so live behavior is unverified. |
| Generic Agent Skills client | `.agents/skills` | Runtime-defined | Format and byte conformance pass; discovery behavior is client-specific. |

The paths and invocation forms follow the current
[Codex skill documentation](https://learn.chatgpt.com/docs/build-skills.md),
[Claude Code skill documentation](https://code.claude.com/docs/en/slash-commands),
[Cursor Agent Skills documentation](https://cursor.com/docs/skills), and
[Agent Skills specification](https://agentskills.io/specification). Recheck primary
documentation when discovery or invocation behavior affects a current decision.

One representative pass is not a Tier 1 behavioral claim. Tier 1 requires the shared
core matrix to pass in actual Codex, Claude Code, and Cursor surfaces.

## Install or update

After installing the Python distribution, preview and install its packaged canonical
suite without a source argument:

    solodeveling install --runtime codex --project-root . --dry-run
    solodeveling install --runtime codex --project-root .
    solodeveling install --runtime claude-code --project-root .
    solodeveling install --runtime cursor --project-root .

Use `--runtime generic` for a compatible client that discovers `.agents/skills`.
Contributors and auditors may override packaged resources explicitly with
`--source ./skills` from a trusted checkout.

Installation validates every canonical `SKILL.md`, rejects source or target symlinks,
preflights all collisions, copies files atomically, and writes
`.solodeveling-manifest.json` inside the runtime skill root. Re-running install updates
only files still matching the prior managed manifest. It refuses modified managed
files and unmanaged collisions.

Installing several native adapters into one project creates separate copies. Some
runtimes may also scan compatibility paths, which can surface duplicate skill names.
Install only the paths needed in that workspace and run check before switching runtime
configuration.

## Check drift

    solodeveling check --runtime codex --project-root .

A successful check proves managed files match their recorded hashes and the packaged
canonical source digest at that moment. Hash equality detects change; it does not prove
publisher identity, authenticity, safety, or behavioral compliance.

## Remove safely

Preview first:

    solodeveling uninstall --runtime codex --project-root . --dry-run

Then remove unchanged managed files:

    solodeveling uninstall --runtime codex --project-root .

Uninstall preflights every manifest path and hash. If any managed file is missing,
modified, replaced by a symlink, or outside the adapter root, it stops before deletion.
Unrelated skills and user files remain. There is intentionally no force-delete option.

Start a fresh agent session after adding a top-level skill directory if the runtime
does not discover it. Treat refresh and co-install behavior as runtime-specific and
unverified until exercised by the live evaluation matrix.
