# solodeveling

The npm launcher for Solodeveling. It provides the same solodeveling command as the
Python distribution without requiring Python on the user's machine.

    npx solodeveling install

The launcher has no install script and no runtime npm dependencies. On explicit
invocation it downloads the exact-version native executable from the Solodeveling
GitHub Release, verifies its bundled SHA-256 and size, caches it, and then runs it.
Unsupported platforms fail closed and show the Python installation fallback.

This source-tree package is not publication-ready until the release workflow replaces
the empty artifact manifest with hashes from reviewed, version-matched native builds.
