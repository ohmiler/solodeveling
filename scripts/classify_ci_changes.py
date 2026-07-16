from __future__ import annotations

import argparse
import sys


MEMORY_PREFIX = '.solodeveling/'
DOCS_PREFIX = 'docs/'


def is_only(paths: list[str], prefix: str) -> bool:
    if not paths:
        return False
    return all(
        path.startswith(prefix)
        and '\\' not in path
        and not path.startswith('/')
        and '//' not in path
        and '/./' not in path
        and '/../' not in path
        for path in paths
    )


def parse_paths(argv: list[str]) -> list[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--null', action='store_true')
    parser.add_argument('paths', nargs='*')
    args = parser.parse_args(argv)
    if not args.null:
        return args.paths
    try:
        return [
            value.decode('utf-8')
            for value in sys.stdin.buffer.read().split(b'\0')
            if value
        ]
    except UnicodeDecodeError:
        return []


def main(argv: list[str] | None = None) -> int:
    paths = parse_paths(sys.argv[1:] if argv is None else argv)
    memory = 'true' if is_only(paths, MEMORY_PREFIX) else 'false'
    docs = 'true' if is_only(paths, DOCS_PREFIX) else 'false'
    print(f'memory_only={memory}')
    print(f'docs_only={docs}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
