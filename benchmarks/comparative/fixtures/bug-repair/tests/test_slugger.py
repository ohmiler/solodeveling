import unittest

from slugger import slugify


class SluggerTests(unittest.TestCase):
    def test_lowercases_words(self) -> None:
        self.assertEqual(slugify("Hello World"), "hello-world")


if __name__ == "__main__":
    unittest.main()
