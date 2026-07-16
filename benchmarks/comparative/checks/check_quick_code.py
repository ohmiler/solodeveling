from __future__ import annotations

import subprocess
import sys
from pathlib import Path


root = Path(sys.argv[1]).resolve()
baseline = sys.argv[2]
sys.path.insert(0, str(root))
from labels import normalize_label

status = subprocess.run(
    ['git', 'status', '--porcelain', '--untracked-files=all'],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
committed = subprocess.run(
    ['git', 'diff', '--name-only', baseline, 'HEAD'],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
changed = {path.replace(chr(92), '/') for path in committed}
changed.update(line[3:].replace(chr(92), '/') for line in status if len(line) > 3)
allowed = {'labels.py', 'tests/test_labels.py'}
cases = {
    '  Hello   WORLD  ': 'hello world',
    '\tAlready\nclean\t': 'already clean',
    'one': 'one',
}
passed = changed <= allowed and all(
    normalize_label(value) == expected for value, expected in cases.items()
)
raise SystemExit(0 if passed else 1)
