# Solodeveling

Solodeveling is a single-agent-first software delivery protocol for solo developers.
It keeps a single primary agent oriented across discovery, planning, implementation,
verification, security, release, and maintenance without requiring subagents. The
same canonical skill suite can be materialized for Codex, Claude Code, Cursor, or a
generic Agent Skills client.

Status: alpha. Codex and Claude Code each passed one bounded representative live
scenario. Cursor has structural adapter evidence only because `cursor-agent` was not
available in the verification environment. Tier 1 remains unverified until the full
core scenario matrix passes on all three runtimes.

## Requirements

- Python 3.10 or newer
- A supported coding-agent runtime
- A project directory under version control, with current work committed or backed up
  before installing any automation

## Install the package

Until the first reviewed release is published, install from a trusted checkout:

```console
git clone https://github.com/ohmiler/solodeveling.git
cd solodeveling
python -m pip install .
```

This installs the canonical skills and four local commands. It does not modify a
project until `solodeveling-adapt install` is run explicitly.

## Install skills into a project

Run exactly one native adapter unless the project intentionally supports several
agent discovery roots. Preview first:

```console
solodeveling-adapt install --runtime codex --project-root . --dry-run
solodeveling-adapt install --runtime codex --project-root .
```

Choose the runtime mapping you need:

```console
solodeveling-adapt install --runtime codex --project-root .
solodeveling-adapt install --runtime claude-code --project-root .
solodeveling-adapt install --runtime cursor --project-root .
solodeveling-adapt install --runtime generic --project-root .
```

The mappings are `.agents/skills`, `.claude/skills`, `.cursor/skills`, and
`.agents/skills` respectively. Installation validates the suite, rejects symlink and
path traversal, refuses unmanaged collisions, copies files atomically, and records a
managed hash manifest. It never changes runtime settings or grants tools.

Start a fresh agent session after first installation. Invoke `$solodeveling` in Codex,
`/solodeveling` in Claude Code or Cursor, and use the client-defined invocation in a
generic Agent Skills runtime.

## Verify, upgrade, and recover

Check installed bytes against the packaged canonical suite:

```console
solodeveling-adapt check --runtime codex --project-root .
```

Upgrade the Python package from a reviewed source, preview the adapter update, then
run install again. Managed files modified by a user are never overwritten.

Preview removal before applying it:

```console
solodeveling-adapt uninstall --runtime codex --project-root . --dry-run
solodeveling-adapt uninstall --runtime codex --project-root .
```

Uninstall removes only unchanged managed files. If anything drifted, it stops and
preserves the files for manual recovery; there is no force-delete mode.

## Project memory and evaluation

Create validated project memory with `solodeveling-init`, then check it with
`solodeveling-validate`. Contributors can inspect the bounded cross-agent harness
without making an agent call:

```console
solodeveling-eval probe
solodeveling-eval run --runtime codex --smoke --dry-run
```

Live evaluation uses external model services and may consume plan usage or API
credits. Review `docs/cross-agent-evaluation.md` before authorizing a live call.

## Security and support boundaries

Solodeveling applies risk-scaled verification and Secure SDLC guidance, but installing
it does not make a project secure or compliant. Hashes detect drift; they do not prove
publisher identity. Current support claims and known limitations are documented in
`docs/runtime-adapters.md`, `docs/cross-agent-evaluation.md`, and the committed
evidence records.

No telemetry is collected. No publishing credentials are included. Release builds are
local and non-publishing until a reviewed tag or registry action is separately
authorized.

## License

Apache-2.0. See `LICENSE`.
