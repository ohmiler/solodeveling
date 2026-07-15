from __future__ import annotations

import argparse
from pathlib import Path

from solodeveling_protocol.release import ReleaseError, build_release_bundle


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build verified Solodeveling release artifacts without publishing."
    )
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    arguments = parser.parse_args()
    try:
        manifest = build_release_bundle(
            arguments.project_root,
            arguments.output,
        )
    except ReleaseError as error:
        print(f"release-error: {error}")
        return 1
    print(f"built release bundle for {manifest['version']}: {arguments.output}")
    for artifact in manifest["artifacts"]:
        print(f"{artifact['sha256']}  {artifact['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
