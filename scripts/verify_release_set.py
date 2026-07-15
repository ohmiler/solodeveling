from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts.assemble_release_set import ReleaseSetError, verify_release_set
except ModuleNotFoundError as error:
    if error.name != "scripts":
        raise
    from assemble_release_set import ReleaseSetError, verify_release_set


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a complete Solodeveling release set without publishing."
    )
    parser.add_argument("release_set", type=Path)
    parser.add_argument("--source-revision", required=True)
    arguments = parser.parse_args()
    try:
        manifest = verify_release_set(
            arguments.release_set, source_revision=arguments.source_revision
        )
    except (OSError, ValueError, KeyError, ReleaseSetError) as error:
        print(f"release-set-verification-error: {error}")
        return 1
    print(
        f"Solodeveling {manifest['version']} release set is internally consistent "
        "and not published"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
