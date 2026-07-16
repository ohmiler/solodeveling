from __future__ import annotations

import argparse

from .store import BookmarkStore


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    add = subparsers.add_parser("add")
    add.add_argument("store")
    add.add_argument("title")
    add.add_argument("url")
    listing = subparsers.add_parser("list")
    listing.add_argument("store")
    args = parser.parse_args()
    store = BookmarkStore(args.store)
    if args.command == "add":
        bookmark = store.add(args.title, args.url)
        print(bookmark["id"])
    else:
        for bookmark in store.list():
            print(f'{bookmark["id"]}\t{bookmark["title"]}\t{bookmark["url"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
