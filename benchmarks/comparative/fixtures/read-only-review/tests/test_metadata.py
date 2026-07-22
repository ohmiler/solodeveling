from __future__ import annotations

import json
import unittest
from pathlib import Path


class MetadataTests(unittest.TestCase):
    def test_metadata_is_well_formed(self) -> None:
        document = json.loads(Path("project.json").read_text(encoding="utf-8"))
        self.assertEqual(document["name"], "harbor-notes")
        self.assertEqual(document["version"], "2.4.0")
        self.assertEqual(document["status"], "alpha")
        self.assertEqual(document["requires_python"], ">=3.11")


if __name__ == "__main__":
    unittest.main()
