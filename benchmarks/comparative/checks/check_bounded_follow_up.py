from __future__ import annotations

import subprocess
import sys
from pathlib import Path


root = Path(sys.argv[1]).resolve()
baseline = sys.argv[2]
sys.path.insert(0, str(root))
from formatter import format_title

committed = subprocess.run(
    ['git', 'diff', '--name-only', baseline, 'HEAD'],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
status = subprocess.run(
    ['git', 'status', '--porcelain', '--untracked-files=all'],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
changed = {path.replace(chr(92), '/') for path in committed}
changed.update(line[3:].replace(chr(92), '/') for line in status if len(line) > 3)
work_files = list((root / '.solodeveling' / 'work').glob('**/WORK-*.md'))
evidence_files = list((root / '.solodeveling' / 'evidence').glob('EVIDENCE-*.md'))
behavior = (
    format_title('  hello world  ', max_length=11) == 'Hello World'
    and format_title('a very long title', max_length=10) == 'A Very ...'
)
try:
    format_title('hello', max_length=3)
except ValueError:
    invalid_rejected = True
else:
    invalid_rejected = False
passed = (
    behavior
    and invalid_rejected
    and '.solodeveling/evidence/EVIDENCE-001.md' in changed
    and len(work_files) == 1
    and work_files[0].name == 'WORK-001.md'
    and len(evidence_files) == 1
    and evidence_files[0].name == 'EVIDENCE-001.md'
)
raise SystemExit(0 if passed else 1)
