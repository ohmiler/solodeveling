from __future__ import annotations

import subprocess
import sys
from pathlib import Path


root = Path(sys.argv[1]).resolve()
baseline = sys.argv[2]
committed = subprocess.run(["git", "diff", "--name-only", baseline, "HEAD"], cwd=root, capture_output=True, text=True, check=True).stdout.splitlines()
status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, capture_output=True, text=True, check=True).stdout.splitlines()
changed = sorted(set(committed) | {line[3:] for line in status if len(line) > 3})
readme = (root / "README.md").read_text(encoding="utf-8")
passed = changed == ["README.md"] and "--ignore-case" in readme and "hello 2" in readme and "world 1" in readme
raise SystemExit(0 if passed else 1)
