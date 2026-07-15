# Installation

Solodeveling uses one package name and one public executable name in every ecosystem:
`solodeveling`. The internal Python import namespace
`solodeveling_protocol` is not a second product or command.

## Choose an installation path

Node.js 20 or newer:

~~~console
npx solodeveling install --runtime codex --dry-run
npx solodeveling install --runtime codex
~~~

`npx` is the shortest path and does not require a global package install.
For a persistent command:

~~~console
npm install -g solodeveling
solodeveling version
~~~

Python 3.10 or newer:

~~~console
uvx solodeveling version
uv tool install solodeveling
pipx install solodeveling
~~~

`uvx` runs the tool ephemerally. `uv tool install` and
`pipx install` keep an isolated installation and place
`solodeveling` on the user PATH.

The npm and PyPI projects are not published at the current source revision. Registry
commands above describe the reviewed-release UX and will work only after publication.
For development or pre-release verification, use a trusted checkout:

~~~console
python -m pip install .
solodeveling version
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

The project root defaults to the current directory:

~~~console
solodeveling install --runtime codex --dry-run
solodeveling install --runtime codex
solodeveling check --runtime codex
~~~

Use `--project-root PATH` when the target is elsewhere. Valid runtime
values are `codex`, `claude-code`, `cursor`, and
`generic`.

## Upgrade and remove

For npm:

~~~console
npm install -g solodeveling@latest
solodeveling install --runtime codex --dry-run
solodeveling install --runtime codex
npm uninstall -g solodeveling
~~~

For uv or pipx:

~~~console
uv tool upgrade solodeveling
pipx upgrade solodeveling
~~~

Package removal removes the command, not managed skills already copied into projects.
Remove project skills separately and preview first:

~~~console
solodeveling uninstall --runtime codex --dry-run
solodeveling uninstall --runtime codex
~~~

Uninstall refuses to delete managed files whose bytes changed.

## Publication trust

A future release must bind the Python distributions, npm tarball, six native
executables, manifest, checksums, SBOM, source commit, and provenance before either
registry is published. npm and PyPI publication use OIDC trusted publishing with
protected GitHub environments rather than long-lived write tokens. Publication is a
separate authorized action; ordinary CI only builds and tests local artifacts.
