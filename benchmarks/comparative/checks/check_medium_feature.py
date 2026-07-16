from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
from bookmarks import BookmarkStore


with tempfile.TemporaryDirectory() as temporary:
    path = Path(temporary) / "items.json"
    store = BookmarkStore(path)
    first = store.add("First", "https://one.example")
    second = store.add("Second", "https://two.example")
    removed = store.remove(first["id"])
    ok = removed == first and BookmarkStore(path).list() == [second]
    try:
        store.remove(999)
    except KeyError:
        pass
    else:
        ok = False
    process = subprocess.run([sys.executable, "-m", "bookmarks", "remove", str(path), str(second["id"])], cwd=root, capture_output=True, text=True)
    ok = ok and process.returncode == 0 and process.stdout.strip() == "Second"
    missing = subprocess.run([sys.executable, "-m", "bookmarks", "remove", str(path), "999"], cwd=root, capture_output=True, text=True)
    ok = ok and missing.returncode == 2 and bool(missing.stderr.strip())
raise SystemExit(0 if ok else 1)
