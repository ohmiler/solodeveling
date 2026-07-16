from __future__ import annotations

import json
from pathlib import Path


class BookmarkStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _read(self) -> list[dict[str, object]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, bookmarks: list[dict[str, object]]) -> None:
        self.path.write_text(json.dumps(bookmarks, indent=2) + "\n", encoding="utf-8")

    def add(self, title: str, url: str) -> dict[str, object]:
        bookmarks = self._read()
        bookmark = {"id": max((int(item["id"]) for item in bookmarks), default=0) + 1, "title": title, "url": url}
        bookmarks.append(bookmark)
        self._write(bookmarks)
        return bookmark

    def list(self) -> list[dict[str, object]]:
        return self._read()
