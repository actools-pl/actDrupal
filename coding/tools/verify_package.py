#!/usr/bin/env python3
"""Read-only integrity check for a fresh extracted coding package.

Standard library only. No network, shell commands, privilege changes or writes.
The adjacent SHA256SUMS is not authenticated; this is not a signature verifier.
Edited working copies are expected to fail the distributed-copy check.
"""

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys


def inventory(root):
    files = set()
    for folder, directories, names in os.walk(root, followlinks=False):
        for name in directories + names:
            path = Path(folder) / name
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISLNK(mode):
                raise ValueError("symlink is not allowed: " + relative)
            if stat.S_ISREG(mode):
                files.add(relative)
            elif not stat.S_ISDIR(mode):
                raise ValueError("special file is not allowed: " + relative)
    return files


def verify(root):
    if root.is_symlink() or not root.is_dir():
        raise ValueError("package root must be a real directory")
    root = root.resolve()
    actual = inventory(root)
    if "SHA256SUMS" not in actual:
        raise ValueError("SHA256SUMS is missing")
    expected = {}
    for number, line in enumerate((root / "SHA256SUMS").read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
        if match is None:
            raise ValueError("invalid manifest line " + str(number))
        digest, relative = match.groups()
        path = PurePosixPath(relative)
        if (path.is_absolute() or ".." in path.parts or "\\" in relative
                or ":" in relative or path.as_posix() != relative
                or relative in {".", "SHA256SUMS"}):
            raise ValueError("unsafe/noncanonical manifest path: " + relative)
        if relative in expected:
            raise ValueError("duplicate manifest path: " + relative)
        expected[relative] = digest
    if not expected:
        raise ValueError("manifest is empty")
    errors = []
    for relative in sorted(set(expected) - actual):
        errors.append("missing: " + relative)
    for relative in sorted(actual - set(expected) - {"SHA256SUMS"}):
        errors.append("unlisted: " + relative)
    for relative in sorted(set(expected) & actual):
        digest = hashlib.sha256()
        with (root / relative).open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != expected[relative]:
            errors.append("changed: " + relative)
    return len(expected), errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path,
                        default=Path(__file__).resolve().parent.parent,
                        help="fresh extracted package directory (default: this script's package)")
    args = parser.parse_args()
    try:
        count, errors = verify(args.root)
    except (OSError, UnicodeError, ValueError) as exc:
        print("CHECK ERROR: " + str(exc), file=sys.stderr)
        return 2
    if errors:
        print("INTEGRITY MISMATCH\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print("OK: " + str(count) + " files match the distributed checksum manifest.")
    print("This does not authenticate the package or qualify the Actools product.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
