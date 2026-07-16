from pathlib import Path


CURRENT_DOCS = (
    Path('README.md'),
    Path('docs/installation.md'),
    Path('docs/runtime-adapters.md'),
    Path('docs/publishing.md'),
    Path('docs/release-readiness.md'),
    Path('docs/cross-agent-evaluation.md'),
    Path('docs/protocol-contract.md'),
    Path('docs/releases/0.1.0.md'),
)


def test_installation_docs_cover_node_and_python_easy_paths() -> None:
    text = Path('docs/installation.md').read_text('utf-8')

    for phrase in (
        'npx solodeveling install',
        'npm install -g solodeveling',
        'uvx solodeveling',
        'uv tool install solodeveling',
        'pipx install solodeveling',
        'preinstall',
        'postinstall',
        'win32-x64',
        'win32-arm64',
        'darwin-x64',
        'darwin-arm64',
        'linux-x64',
        'linux-arm64',
        'Version 0.1.0 is published',
        'https://www.npmjs.com/package/solodeveling',
        'https://pypi.org/project/solodeveling/',
        'immutable GitHub Release',
    ):
        assert phrase in text


def test_readme_positions_solodeveling_without_unmeasured_superiority() -> None:
    text = Path('README.md').read_text('utf-8')

    for phrase in (
        'One agent. The right amount of process.',
        '## How it compares',
        'Superpowers',
        'GSD',
        'GitHub Spec Kit',
        'BMAD Method',
        '## Who it is for',
        'it is not a controlled speed',
        'does not yet claim to complete coding tasks faster',
        'https://www.npmjs.com/package/solodeveling',
        'https://pypi.org/project/solodeveling/',
    ):
        assert phrase in text

    for stale in (
        'The npm and PyPI projects have not been published',
        'After the first reviewed 0.1.0 release is published',
    ):
        assert stale not in text


def test_current_user_docs_do_not_teach_split_command_names() -> None:
    forbidden = (
        'solodeveling-adapt',
        'solodeveling-init',
        'solodeveling-validate',
        'solodeveling-eval',
        'solodeveling-protocol',
    )
    for path in CURRENT_DOCS:
        text = path.read_text('utf-8')
        for phrase in forbidden:
            assert phrase not in text, f'{path}: legacy public name {phrase}'
