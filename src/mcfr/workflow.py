"""Resume source verification and run approved AI reviews."""

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
from zipfile import BadZipFile

from . import ai_review, research_db as catalog, source_jobs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan")
    scan.add_argument("run_id")
    scan.add_argument("job_id")
    scan.add_argument("--source", required=True, type=Path)
    scan.add_argument("--max-assets", type=catalog.nonnegative_int)
    sub.add_parser("scan-status").add_argument("job_id")

    prepare = sub.add_parser("review-prepare")
    prepare.add_argument("review_id")
    prepare.add_argument("execution_id")
    prepare.add_argument("--model", required=True)
    prepare.add_argument("--max-output-tokens", required=True, type=int)
    prepare.add_argument("--asset", action="append", default=[])
    send = sub.add_parser("review-send")
    send.add_argument("review_id")
    send.add_argument("--approve", required=True)
    send.add_argument("--reuse-identical", action="store_true",
                      help="Reuse an identical approved completed review for the same scope when available")
    sub.add_parser("review-status").add_argument("review_id")

    args = parser.parse_args(argv)
    read_only = args.command in {"scan-status", "review-status"}
    try:
        with closing(catalog.open_db(args.db, "ro" if read_only else "rw")) as db:
            catalog.require_schema(db, minimum=3)
            if args.command == "scan":
                result = source_jobs.scan(db, args.job_id, args.run_id, args.source, args.max_assets)
            elif args.command == "scan-status":
                result = source_jobs.status(db, args.job_id)
            elif args.command == "review-prepare":
                result = ai_review.prepare(
                    db, args.review_id, args.execution_id, args.model, args.max_output_tokens, args.asset,
                )
            elif args.command == "review-send":
                if args.reuse_identical:
                    catalog.require_schema(db, minimum=4)
                result = ai_review.dispatch(db, args.review_id, args.approve, reuse_identical=args.reuse_identical)
            else:
                result = ai_review.review_status(db, args.review_id, include_request=True)
    except (OSError, ValueError, BadZipFile, sqlite3.Error) as exc:
        parser.error(str(exc))
    except KeyboardInterrupt:
        return 130
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result.get("status") == "FAIL" or result.get("state") == "UNCONFIRMED")


if __name__ == "__main__":
    raise SystemExit(main())
