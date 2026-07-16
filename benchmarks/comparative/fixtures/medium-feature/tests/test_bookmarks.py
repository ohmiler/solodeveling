import tempfile
import unittest
from pathlib import Path

from bookmarks import BookmarkStore


class BookmarkStoreTests(unittest.TestCase):
    def test_add_and_list(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            store = BookmarkStore(Path(temporary) / "bookmarks.json")
            created = store.add("Example", "https://example.com")
            self.assertEqual(created["id"], 1)
            self.assertEqual(store.list(), [created])


if __name__ == "__main__":
    unittest.main()
