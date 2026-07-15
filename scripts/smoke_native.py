from __future__ import annotations

import argparse
from pathlib import Path

from smoke_installed import SmokeError, installed_smoke


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke-test one current-platform native artifact."
    )
    parser.add_argument("native_root", type=Path)
    parser.add_argument("workspace", type=Path)
    arguments = parser.parse_args()
    artifacts = tuple(
        path
        for path in arguments.native_root.iterdir()
        if path.is_file() and path.name.startswith("solodeveling-")
    )
    if len(artifacts) != 1:
        print(f"native-smoke-error: expected one artifact, found {len(artifacts)}")
        return 1
    try:
        installed_smoke(arguments.workspace, str(artifacts[0].resolve()))
    except (OSError, SmokeError) as error:
        print(f"native-smoke-error: {error}")
        return 1
    print(f"Native Solodeveling smoke test passed: {artifacts[0].name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
