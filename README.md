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

After the first reviewed 0.1.0 release is published, Node.js users need one command:

~~~console
npx solodeveling install
~~~

For a permanent command:

~~~console
npm install -g solodeveling
solodeveling install
~~~

Python users can run it without a permanent install or install it as a tool:

~~~console
uvx solodeveling install
uv tool install solodeveling
pipx install solodeveling
~~~

The npm and PyPI projects have not been published yet. Until the reviewed release,
install from this trusted checkout:

~~~console
git clone https://github.com/ohmiler/solodeveling.git
cd solodeveling
python -m pip install .
solodeveling install
~~~

All channels expose only one public command: `solodeveling`. See
[Installation](docs/installation.md) for prerequisites, platform support, upgrades,
integrity controls, and current publication status.

## Automatic project installation

The ordinary workflow has no required options:

~~~console
solodeveling install
solodeveling check
solodeveling uninstall
~~~

Solodeveling first reuses any installation it already manages. Otherwise it detects
project-local Codex/Agent Skills, Claude Code, and Cursor directories. It installs
every distinct runtime found, and defaults to the standard `.agents/skills` path when
the project has no runtime marker. It never searches global executables or writes
outside the current project.

Installation validates the skill suite, preflights every detected target, rejects
symlinks and path traversal, refuses unmanaged collisions, copies files atomically,
and records managed hashes. Check detects missing, changed, or unexpected managed
files. Uninstall removes only unchanged managed files and has no force-delete mode.

Start a fresh agent session after first installation, then invoke `$solodeveling` in
Codex, `/solodeveling` in Claude Code or Cursor, or the client-defined invocation in
another Agent Skills runtime.

### Advanced overrides

Automation and unusual workspaces may still select an exact runtime or another
project. `--dry-run` remains available as an optional preview, not a required step:

~~~console
solodeveling install --runtime claude-code --project-root PATH
solodeveling install --runtime cursor --dry-run
~~~

## Other commands

The install flow stays short; project memory and evaluation remain explicit:

~~~console
solodeveling init
solodeveling validate .
solodeveling eval probe
solodeveling version
~~~

Live evaluation can consume model-service usage or API credits, so review
[Cross-agent evaluation](docs/cross-agent-evaluation.md) before authorizing a live
run.

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
