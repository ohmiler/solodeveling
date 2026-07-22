from __future__ import annotations

import unittest
from pathlib import Path


class MigrationDocumentTests(unittest.TestCase):
    def test_proposal_identifies_the_production_command(self) -> None:
        document = Path("MIGRATION.md").read_text(encoding="utf-8")
        self.assertIn("python migrate.py --production", document)
        self.assertIn("Drop the legacy", document)


if __name__ == "__main__":
    unittest.main()
