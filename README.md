# Solodeveling

Solodeveling is a single-agent-first software delivery protocol for solo developers.
It keeps a single primary agent oriented across discovery, planning, implementation,
verification, security, release, and maintenance without requiring subagents. The
same canonical skill suite works with Codex, Claude Code, Cursor, and generic Agent
Skills clients.

Status: alpha. Codex and Claude Code each passed one bounded representative live
scenario. Cursor has structural adapter evidence only because `cursor-agent`
was unavailable. Tier 1 remains unverified until the full core scenario matrix passes.

## Quick start

After the first reviewed 0.1.0 release is published, Node.js users can preview and
install into the current project without installing Python:

~~~console
npx solodeveling install --runtime codex --dry-run
npx solodeveling install --runtime codex
~~~

Install the same command globally if you prefer:

~~~console
npm install -g solodeveling
solodeveling install --runtime codex --dry-run
solodeveling install --runtime codex
~~~

Python users can run it without a permanent install or install it as a tool:

~~~console
uvx solodeveling install --runtime codex --dry-run
uv tool install solodeveling
pipx install solodeveling
~~~

The npm and PyPI projects have not been published yet. Until the reviewed release,
install from this trusted checkout:

~~~console
git clone https://github.com/ohmiler/solodeveling.git
cd solodeveling
python -m pip install .
solodeveling install --runtime codex --dry-run
~~~

All channels expose only one public command: `solodeveling`. See
[Installation](docs/installation.md) for prerequisites, platform support, upgrades,
integrity controls, and current publication status.

## Runtime installation

Choose the runtime whose native skill-discovery directory should be managed:

~~~console
solodeveling install --runtime codex
solodeveling install --runtime claude-code
solodeveling install --runtime cursor
solodeveling install --runtime generic
~~~

The default project root is the current directory. Use `--project-root PATH`
for another project. The mappings are `.agents/skills`,
`.claude/skills`, `.cursor/skills`, and
`.agents/skills` respectively.

Installation validates the skill suite, rejects symlinks and path traversal, refuses
unmanaged collisions, copies files atomically, and records managed hashes. It does
not change coding-agent settings or grant tools. Start a fresh agent session after
first installation, then invoke `$solodeveling` in Codex,
`/solodeveling` in Claude Code or Cursor, or the client-defined invocation
in another Agent Skills runtime.

## One command, complete lifecycle

~~~console
solodeveling check --runtime codex
solodeveling uninstall --runtime codex --dry-run
solodeveling uninstall --runtime codex
solodeveling init --help
solodeveling validate .
solodeveling eval probe
solodeveling version
~~~

Check detects missing, changed, or unexpected managed files. Uninstall removes only
unchanged managed files and preserves drift for manual recovery; there is no
force-delete mode. Live evaluation can consume model-service usage or API credits,
so review [Cross-agent evaluation](docs/cross-agent-evaluation.md) before authorizing
a live run.

## Security and support boundaries

The npm launcher has no runtime dependencies and no install lifecycle script. On an
explicit invocation it selects an exact-version native artifact, downloads only from
the versioned GitHub Release, verifies its bundled size and SHA-256, caches it, and
executes it without a shell. Windows, macOS, and Linux on x64 and arm64 are release
targets only after their CI builds and native smoke tests pass. Unsupported targets
fail closed and show the Python-tool fallback.

Solodeveling applies risk-scaled verification and Secure SDLC guidance, but installing
it does not make a project categorically secure or compliant. Hashes detect byte
changes; they do not by themselves prove publisher identity. No telemetry is
collected and no publishing credentials are included.

No tag, GitHub Release, npm package, or PyPI package is created by ordinary CI.
External publication requires a reviewed source revision and separate explicit
authorization.

## License

Apache-2.0. See [LICENSE](LICENSE).
