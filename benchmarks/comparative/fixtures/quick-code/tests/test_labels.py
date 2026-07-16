import unittest

from labels import normalize_label


class LabelTests(unittest.TestCase):
    def test_strips_surrounding_whitespace(self) -> None:
        self.assertEqual(normalize_label('  Example  '), 'Example')


if __name__ == '__main__':
    unittest.main()
