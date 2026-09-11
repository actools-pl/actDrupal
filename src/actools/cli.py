"""Truthful, deliberately small command-line surface for CP-001."""

from __future__ import annotations

import json
import os
import sys
from collections.abc import Sequence
from typing import TextIO

from . import __version__

PROGRAM = "actools"
INVOCATION_ERROR_EXIT = 3
OUTPUT_FAILURE_EXIT = 3
ERROR_TEXT = "actools: error: invalid invocation\n"
ROOT_HELP = """usage: actools [-h] {version} ...

actDrupal development CLI. Only version/help is implemented in CP-001.

commands:
  version     show the development package version

options:
  -h, --help  show this help message and exit
"""
VERSION_HELP = """usage: actools version [-h] [--format {human,json}]

show the development package version

options:
  -h, --help            show this help message and exit
  --format {human,json} output format (default: human)
"""


def _silence_stream(name: str) -> None:
    try:
        fd = os.open(os.devnull, os.O_WRONLY)
        stream = os.fdopen(fd, "w", encoding="utf-8", closefd=True)
        setattr(sys, name, stream)
    except OSError:
        pass


def _write(stream: TextIO, stream_name: str, text: str) -> int:
    try:
        stream.write(text)
        stream.flush()
    except (BrokenPipeError, OSError):
        # Avoid a second pipe diagnostic during interpreter shutdown. Output
        # delivery failure is an invocation/report failure under §18.5.
        _silence_stream(stream_name)
        return OUTPUT_FAILURE_EXIT
    return 0


def _write_stdout(text: str) -> int:
    return _write(sys.stdout, "stdout", text)


def _write_stderr(text: str) -> int:
    return _write(sys.stderr, "stderr", text)


def _version_text(fmt: str) -> str:
    if fmt == "json":
        return json.dumps(
            {"program": PROGRAM, "version": __version__},
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n"
    return f"{PROGRAM} {__version__}\n"


def _invocation_error() -> int:
    # Never echo rejected arguments. This keeps diagnostics bounded and avoids
    # reflecting terminal controls, secret-looking values, or very long input.
    _write_stderr(ERROR_TEXT)
    return INVOCATION_ERROR_EXIT


def _parse_version(args: list[str]) -> tuple[str, str | None]:
    if not args:
        return "version", "human"
    if args in (["-h"], ["--help"]):
        return "help", None
    if len(args) == 2 and args[0] == "--format" and args[1] in {"human", "json"}:
        return "version", args[1]
    if len(args) == 1 and args[0].startswith("--format="):
        value = args[0].partition("=")[2]
        if value in {"human", "json"}:
            return "version", value
    return "error", None


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args in (["-h"], ["--help"]):
        return _write_stdout(ROOT_HELP)

    if args[0] != "version":
        return _invocation_error()

    action, fmt = _parse_version(args[1:])
    if action == "help":
        return _write_stdout(VERSION_HELP)
    if action == "version" and fmt is not None:
        return _write_stdout(_version_text(fmt))
    return _invocation_error()


if __name__ == "__main__":  # pragma: no cover - exercised via subprocess tests
    raise SystemExit(main())
