#!/usr/bin/env python3
"""Count a job's weekly volume and blank fields from a CSV export, on this machine only.

Usage:
    python scripts/profile_csv.py <export.csv> --date <column> [--where <column>=<value>]

--date names the column holding each record's date. --where keeps only rows whose
column equals the value (for example --where "type=Quote"), when one export mixes jobs.

Prints JSON: rows counted, the dates they cover, weekly volume (rows x 7 / days
covered), and the share of blank cells in each column. Standard library only.
"""

import csv
import json
import sys
from datetime import datetime


def parse_date(text):
    text = text.strip()
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        pass
    try:
        return datetime.strptime(text.split()[0], "%m/%d/%Y").date()
    except (ValueError, IndexError):
        return None


def profile(path, date_column, where=None):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        if date_column not in columns:
            raise ValueError(f"no column named '{date_column}'; columns are: {', '.join(columns)}")
        if where and where[0] not in columns:
            raise ValueError(f"no column named '{where[0]}'; columns are: {', '.join(columns)}")
        rows = [r for r in reader if not where or (r[where[0]] or "").strip() == where[1]]

    dates = [parse_date(r[date_column] or "") for r in rows]
    known = [d for d in dates if d]
    days = (max(known) - min(known)).days + 1 if known else 0
    return {
        "rows": len(rows),
        "first_date": min(known).isoformat() if known else None,
        "last_date": max(known).isoformat() if known else None,
        "days_covered": days,
        "unreadable_dates": len(dates) - len(known),
        "weekly_volume": round(len(rows) * 7 / days, 1) if days else None,
        "blank_share": {
            c: round(sum(1 for r in rows if not (r[c] or "").strip()) / len(rows), 3) if rows else None
            for c in columns
        },
    }


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help") or "--date" not in args:
        print(__doc__)
        return 0 if args and args[0] in ("-h", "--help") else 2
    try:
        date_column = args[args.index("--date") + 1]
        where = None
        if "--where" in args:
            column, _, value = args[args.index("--where") + 1].partition("=")
            where = (column, value)
        print(json.dumps(profile(args[0], date_column, where), indent=2))
    except (OSError, ValueError, IndexError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
