from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from slugger import slugify


cases = {"  Hello---World  ": "hello-world", "one  two--three": "one-two-three", "already-clean": "already-clean"}
raise SystemExit(0 if all(slugify(value) == expected for value, expected in cases.items()) else 1)
