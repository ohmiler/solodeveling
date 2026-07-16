from __future__ import annotations

import argparse
from collections import Counter


def count_words(text: str, *, ignore_case: bool = False) -> list[tuple[str, int]]:
    words = text.split()
    if ignore_case:
        words = [word.lower() for word in words]
    return sorted(Counter(words).items())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--ignore-case", action="store_true")
    args = parser.parse_args()
    for word, count in count_words(args.text, ignore_case=args.ignore_case):
        print(f"{word} {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
