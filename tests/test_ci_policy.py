from pathlib import Path
import subprocess
import sys


SCRIPT = Path('scripts/classify_ci_changes.py')


def classify(*paths: str) -> dict[str, str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *paths],
        check=True,
        capture_output=True,
        text=True,
    )
    return dict(line.split('=', 1) for line in result.stdout.splitlines())


def test_only_project_memory_uses_focused_ci() -> None:
    assert classify(
        '.solodeveling/state.md',
        '.solodeveling/work/active/WORK-019.md',
    ) == {'memory_only': 'true', 'docs_only': 'false'}


def test_only_docs_tree_uses_docs_ci() -> None:
    assert classify('docs/installation.md', 'docs/releases/0.1.0.md') == {
        'memory_only': 'false',
        'docs_only': 'true',
    }


def test_empty_or_ambiguous_changes_fail_safe_to_full_ci() -> None:
    assert classify() == {'memory_only': 'false', 'docs_only': 'false'}
    assert classify('.solodeveling\\state.md') == {
        'memory_only': 'false',
        'docs_only': 'false',
    }


def test_product_or_skill_changes_always_use_full_ci() -> None:
    expected = {'memory_only': 'false', 'docs_only': 'false'}

    assert classify('README.md') == expected
    assert classify('CHANGELOG.md') == expected
    assert classify('skills/solodeveling/SKILL.md') == expected
    assert classify('.solodeveling/state.md', 'docs/installation.md') == expected
    assert classify('docs/installation.md', 'src/example.py') == expected
    assert classify('docs\\installation.md') == expected


def test_ci_avoids_duplicate_feature_branch_pushes_and_routes_jobs() -> None:
    workflow = Path('.github/workflows/ci.yml').read_text('utf-8')
    quote = chr(39)

    assert 'push:\n    branches: [main]' in workflow
    assert 'tags:' in workflow
    assert 'v*' in workflow
    assert 'pull_request:' in workflow
    assert 'memory-only:' in workflow
    assert 'docs-only:' in workflow
    assert 'python scripts/classify_ci_changes.py --null' in workflow
    assert 'needs.changes.outputs.memory_only' in workflow
    assert 'needs.changes.outputs.docs_only' in workflow
    assert 'git diff --check $BASE_SHA $GITHUB_SHA' in workflow
    assert 'Run complete Python regression suite' in workflow
    assert f'== {quote}true{quote}' in workflow
    assert f'!= {quote}true{quote}' in workflow
