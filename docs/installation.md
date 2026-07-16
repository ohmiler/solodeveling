# Installation

Solodeveling uses one package name and one public executable name in every ecosystem:
`solodeveling`. The internal Python import namespace
`solodeveling_protocol` is not a second product or command.

## Choose an installation path

Node.js 20 or newer:

~~~console
npx solodeveling install
~~~

`npx` is the shortest path and does not require a global package install. For a
persistent command:

~~~console
npm install -g solodeveling
solodeveling install
~~~

Python 3.10 or newer:

~~~console
uvx solodeveling install
uv tool install solodeveling
pipx install solodeveling
~~~

`uvx` runs the tool ephemerally. `uv tool install` and `pipx install` keep an isolated
installation and place `solodeveling` on the user PATH.

Version 0.1.0 is published on
[npm](https://www.npmjs.com/package/solodeveling) and
[PyPI](https://pypi.org/project/solodeveling/). The npm launcher retrieves only the
matching native asset from the
[immutable GitHub Release](https://github.com/ohmiler/solodeveling/releases/tag/v0.1.0).
For development against an unreleased checkout, install the local Python project:

~~~console
python -m pip install .
solodeveling install
~~~

## Supported release targets

The npm launcher maps only these exact targets:

| Operating system | x64 | arm64 |
| --- | --- | --- |
| Windows | `win32-x64` | `win32-arm64` |
| macOS | `darwin-x64` | `darwin-arm64` |
| Linux | `linux-x64` | `linux-arm64` |

A target is release-supported only when its native artifact was built and smoke-tested
by CI for that version. Other operating systems and CPU architectures fail without
running downloaded code and suggest `uv tool install solodeveling` or
`pipx install solodeveling`.

## What npm does

The npm package is a small dependency-free launcher. It has no
`preinstall`, `install`, or `postinstall` script, so
installing the package does not download or execute the native binary.

On the first explicit `solodeveling` command for a version, the launcher:

1. maps the local OS and architecture to a fixed supported key;
2. reads the exact filename, byte size, and SHA-256 from the manifest bundled in that
   npm package version;
3. downloads the matching asset from the immutable version path under
   `ohmiler/solodeveling`;
4. rejects redirects to non-HTTPS URLs, excessive redirects, wrong sizes, wrong
   hashes, unsafe names, and unsupported targets;
5. atomically caches the verified file and executes it without a shell.

Every cached invocation verifies the file again before execution. The source-tree
manifest is intentionally empty; the release workflow fills it only after all six
version-matched native artifacts pass.

## Install into a project

Run from the project root:

~~~console
solodeveling install
~~~

Solodeveling reuses valid managed manifests first. For a new installation it detects
fixed project-local markers for Codex/Agent Skills, Claude Code, and Cursor, installs
each distinct detected target, and defaults to `.agents/skills` when no marker exists.
It does not inspect global programs, environment-provided paths, or agent account
settings.

## Upgrade, check, and remove

For npm:

~~~console
npm install -g solodeveling@latest
solodeveling install
~~~

For uv or pipx:

~~~console
uv tool upgrade solodeveling
pipx upgrade solodeveling
solodeveling install
~~~

Verify or safely remove every managed project installation without remembering its
runtime:

~~~console
solodeveling check
solodeveling uninstall
~~~

Package removal removes the command, not managed skills already copied into projects.
Uninstall refuses to delete managed files whose bytes changed.

### Advanced overrides

Use these only for automation, a non-current project, or deliberate single-runtime
control:

~~~console
solodeveling install --runtime claude-code
solodeveling check --runtime cursor --project-root PATH
solodeveling uninstall --runtime codex --dry-run
~~~

`--dry-run` previews an operation but is never required for install or uninstall.

## Publication trust

Release 0.1.0 binds the Python distributions, npm tarball, six native executables,
manifest, checksums, SBOM, source commit, and attestations in one immutable release
set. The public npm and PyPI bytes were verified against that set after publication.

Later registry releases use OIDC trusted publishing with protected GitHub
environments rather than long-lived write tokens. npm automation is restricted to
staged publication so an owner must review and approve it before it becomes public.
Publication remains a separate authorized action; ordinary CI only builds and tests
local artifacts.
