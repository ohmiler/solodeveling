import unittest

from wordcounter import count_words


class WordCounterTests(unittest.TestCase):
    def test_counts_words(self) -> None:
        self.assertEqual(count_words("red blue red"), [("blue", 1), ("red", 2)])

    def test_ignore_case(self) -> None:
        self.assertEqual(count_words("Red red", ignore_case=True), [("red", 2)])


if __name__ == "__main__":
    unittest.main()
