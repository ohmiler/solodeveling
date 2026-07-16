from __future__ import annotations

from pathlib import Path

import pytest

from scripts.build_native import NativeBuildError, build_native, native_target


@pytest.mark.parametrize(
    ("system", "machine", "expected"),
    [
        ("win32", "AMD64", ("win32-x64", "solodeveling-0.1.1-windows-x64.exe")),
        ("win32", "ARM64", ("win32-arm64", "solodeveling-0.1.1-windows-arm64.exe")),
        ("darwin", "x86_64", ("darwin-x64", "solodeveling-0.1.1-macos-x64")),
        ("darwin", "arm64", ("darwin-arm64", "solodeveling-0.1.1-macos-arm64")),
        ("linux", "x86_64", ("linux-x64", "solodeveling-0.1.1-linux-x64")),
        ("linux", "aarch64", ("linux-arm64", "solodeveling-0.1.1-linux-arm64")),
    ],
)
def test_native_target_is_exact(
    system: str, machine: str, expected: tuple[str, str]
) -> None:
    assert native_target(system, machine) == expected


def test_native_target_rejects_unsupported_platform() -> None:
    with pytest.raises(NativeBuildError, match="unsupported"):
        native_target("freebsd", "x86_64")


def test_native_builder_includes_canonical_resources(
    tmp_path: Path,
) -> None:
    output = tmp_path / "native"
    calls: list[tuple[tuple[str, ...], Path]] = []

    def runner(argv, cwd):
        arguments = tuple(argv)
        calls.append((arguments, cwd))
        dist = Path(arguments[arguments.index("--distpath") + 1])
        dist.mkdir(parents=True)
        (dist / "solodeveling.exe").write_bytes(b"native")
        return 0

    built = build_native(
        Path("."),
        output,
        system="win32",
        machine="AMD64",
        runner=runner,
    )

    assert built.name == "solodeveling-0.1.1-windows-x64.exe"
    assert built.read_bytes() == b"native"
    arguments, cwd = calls[0]
    assert cwd == Path(".").resolve()
    assert "--onefile" in arguments
    assert "--noupx" in arguments
    assert "--add-data" in arguments
    assert "--collect-data" in arguments
    assert "rfc3987_syntax" in arguments
    joined = " ".join(arguments)
    assert "solodeveling_protocol/resources/skills" in joined
    assert "solodeveling_protocol/resources/evals" in joined
    assert "solodeveling_protocol/templates" in joined
    assert "solodeveling_protocol/schemas" in joined


def test_native_builder_refuses_existing_output_before_runner(
    tmp_path: Path,
) -> None:
    output = tmp_path / "native"
    output.mkdir()
    destination = output / "solodeveling-0.1.1-linux-x64"
    destination.write_bytes(b"existing")
    called = False

    def runner(argv, cwd):
        nonlocal called
        called = True
        return 0

    with pytest.raises(NativeBuildError, match="already exists"):
        build_native(
            Path("."),
            output,
            system="linux",
            machine="x86_64",
            runner=runner,
        )
    assert called is False
