"""Truthful, deliberately small command-line surface for CP-001."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence

from . import __version__

PROGRAM = "actools"
BROKEN_PIPE_EXIT = 3


def _parser() -> argparse.ArgumentParser:
    kwargs: dict[str, object] = {}
    if sys.version_info >= (3, 14):
        kwargs["color"] = False
    parser = argparse.ArgumentParser(
        prog=PROGRAM,
        description="actDrupal development CLI. Only version/help is implemented in CP-001.",
        **kwargs,
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    version = subparsers.add_parser("version", help="show the development package version")
    version.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="output format (default: human)",
    )
    return parser


def _write_stdout(text: str) -> int:
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except BrokenPipeError:
        # Prevent a second BrokenPipeError from interpreter shutdown and return a
        # stable, documented non-success exit without a traceback.
        try:
            fd = os.open(os.devnull, os.O_WRONLY)
            sys.stdout = os.fdopen(fd, "w", encoding="utf-8", closefd=True)
        except OSError:
            pass
        return BROKEN_PIPE_EXIT
    return 0


def _version_text(fmt: str) -> str:
    if fmt == "json":
        return json.dumps(
            {"program": PROGRAM, "version": __version__},
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n"
    return f"{PROGRAM} {__version__}\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)

    if args.command is None:
        return _write_stdout(parser.format_help())
    if args.command == "version":
        return _write_stdout(_version_text(args.format))

    # argparse owns command validation, so this is defensive rather than a
    # hidden implementation path.
    parser.error("unsupported command")
    return 2


if __name__ == "__main__":  # pragma: no cover - exercised via subprocess tests
    raise SystemExit(main())
