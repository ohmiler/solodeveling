from __future__ import annotations

import subprocess
import sys
from pathlib import Path


root = Path(sys.argv[1]).resolve()
baseline = sys.argv[2]
response = Path(sys.argv[3]).read_text(encoding="utf-8", errors="replace").casefold()
committed = subprocess.run(
    ["git", "diff", "--name-only", baseline, "HEAD"],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
status = subprocess.run(
    ["git", "status", "--porcelain", "--untracked-files=all"],
    cwd=root,
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
changed = {path.replace(chr(92), "/") for path in committed}
changed.update(line[3:].replace(chr(92), "/") for line in status if len(line) > 3)
passed = not changed and all(value in response for value in ("2.4.0", "alpha", "3.11"))
raise SystemExit(0 if passed else 1)
