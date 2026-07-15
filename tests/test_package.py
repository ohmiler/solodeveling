from solodeveling_protocol import SCHEMA_VERSION, __version__


def test_package_exports_protocol_and_package_versions() -> None:
    assert SCHEMA_VERSION == 1
    assert __version__ == "0.1.0"
