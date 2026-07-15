from pathlib import Path


CURRENT_DOCS = (
    Path("README.md"),
    Path("docs/installation.md"),
    Path("docs/runtime-adapters.md"),
    Path("docs/publishing.md"),
    Path("docs/release-readiness.md"),
    Path("docs/cross-agent-evaluation.md"),
    Path("docs/protocol-contract.md"),
    Path("docs/releases/0.1.0.md"),
)


def test_installation_docs_cover_node_and_python_easy_paths() -> None:
    text = Path("docs/installation.md").read_text("utf-8")

    for phrase in (
        "npx solodeveling install",
        "npm install -g solodeveling",
        "uvx solodeveling",
        "uv tool install solodeveling",
        "pipx install solodeveling",
        "preinstall",
        "postinstall",
        "win32-x64",
        "win32-arm64",
        "darwin-x64",
        "darwin-arm64",
        "linux-x64",
        "linux-arm64",
        "not published",
    ):
        assert phrase in text


def test_current_user_docs_do_not_teach_split_command_names() -> None:
    forbidden = (
        "solodeveling-adapt",
        "solodeveling-init",
        "solodeveling-validate",
        "solodeveling-eval",
        "solodeveling-protocol",
    )
    for path in CURRENT_DOCS:
        text = path.read_text("utf-8")
        for phrase in forbidden:
            assert phrase not in text, f"{path}: legacy public name {phrase}"
