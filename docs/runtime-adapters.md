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

After installing the distribution, run one command from the project root:

    solodeveling install

Solodeveling prefers valid managed manifests, then detects fixed project-local
`.codex`/`.agents`, `.claude`, and `.cursor` markers. It installs every distinct
detected adapter and defaults to `.agents/skills` when none exists. Codex and generic
share that target and are never written twice.

Some clients also scan compatibility paths and may show duplicate skill names when
several native adapters coexist. Use an explicit advanced runtime override only when
a workspace needs deliberate single-target control.

Installation validates every canonical `SKILL.md`, rejects source or target symlinks,
preflights all detected targets before writing, copies files atomically, and writes
`.solodeveling-manifest.json` inside each runtime skill root. Re-running install
updates only files still matching the prior managed manifest. The preflight rejects modified managed files and unmanaged collisions before
ordinary writes begin.

## Check drift

    solodeveling check

A successful check proves every discovered managed file matches its recorded hash and
the packaged canonical source digest at that moment. Hash equality detects change; it
does not prove publisher identity, authenticity, safety, or behavioral compliance.

## Remove safely

    solodeveling uninstall

Uninstall discovers only validated Solodeveling manifests and preflights every
managed path and hash. If any managed file is missing, modified, replaced by a
symlink, or outside the adapter root, it stops before deletion. Unrelated skills and
user files remain. There is intentionally no force-delete option.

### Advanced overrides

Explicit options remain for automation and unusual workspaces:

    solodeveling install --runtime claude-code --project-root PATH
    solodeveling install --runtime cursor --dry-run
    solodeveling uninstall --runtime codex --dry-run

`--source` is available to contributors and auditors using a trusted checkout.
`--dry-run` is an optional preview and is not part of ordinary installation.
Start a fresh agent session after adding a top-level skill directory if the runtime
does not discover it. Treat refresh and co-install behavior as runtime-specific and
unverified until exercised by the live evaluation matrix.
