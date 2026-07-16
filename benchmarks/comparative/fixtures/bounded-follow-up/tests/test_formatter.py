import unittest

from formatter import format_title


class FormatterTests(unittest.TestCase):
    def test_formats_title(self) -> None:
        self.assertEqual(format_title('  hello world  '), 'Hello World')


if __name__ == '__main__':
    unittest.main()
