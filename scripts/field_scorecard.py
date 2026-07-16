from __future__ import annotations

import argparse
import json
from pathlib import Path

from solodeveling_protocol.field_scorecard import (
    ScorecardError,
    load_scorecard,
    summarize_scorecard,
)


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate or summarize a local field scorecard')
    parser.add_argument('command', choices=('validate', 'summary'))
    parser.add_argument('scorecard', type=Path)
    args = parser.parse_args()
    try:
        document = load_scorecard(args.scorecard)
    except ScorecardError as error:
        parser.error(str(error))
    if args.command == 'validate':
        result = {'valid': True, 'observations': len(document['observations'])}
    else:
        result = summarize_scorecard(document)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
