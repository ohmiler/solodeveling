from __future__ import annotations

import argparse
from pathlib import Path

from cyclonedx.schema import SchemaVersion
from cyclonedx.validation.json import JsonStrictValidator

from solodeveling_protocol import __version__
from solodeveling_protocol.release import ReleaseError, verify_candidate_bundle

from verify_release import VerificationError, verify_bundle


def verify_candidate(project_root: Path, bundle: Path, source_revision: str) -> None:
    verify_bundle(project_root, bundle)
    verify_candidate_bundle(bundle, source_revision=source_revision)
    sbom = bundle / f"solodeveling-protocol-{__version__}.cdx.json"
    validation_error = JsonStrictValidator(SchemaVersion.V1_6).validate_str(
        sbom.read_text("utf-8")
    )
    if validation_error is not None:
        raise VerificationError(
            f"CycloneDX strict validation failed: {validation_error}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a source-bound Solodeveling candidate bundle."
    )
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument(
        "--project-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    arguments = parser.parse_args()
    try:
        verify_candidate(
            arguments.project_root.resolve(),
            arguments.bundle.resolve(),
            arguments.source_revision,
        )
    except (OSError, ValueError, KeyError, ReleaseError, VerificationError) as error:
        print(f"candidate-verification-error: {error}")
        return 1
    print("Solodeveling release candidate is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())