#!/usr/bin/env python3
"""Read-only lint for this coding package and its edited workflow records.

Standard library only; no shell, network, subprocess, imports from the package,
or file writes. This is not a Markdown renderer, evidence verifier, signature
checker, hostile-filesystem sandbox, or Actools product acceptance test.
Run on a stable operator-owned package directory. See PACKAGE_VALIDATION.md.
"""

import argparse
import csv
import hashlib
import io
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import unquote, urlsplit


BASELINE = "baseline/Actools_Drupal_Community_Rewrite_Architecture_Implementation_v1.5.1.md"
BASELINE_SHA256 = "b131f36e316593f93aa9ec41e86c1b918a7b32dec87300188e4fdf0d487dde87"
ORIGINAL = "reference/Architecture_v1.5_ORIGINAL_REFERENCE_ONLY.md"
ORIGINAL_SHA256 = "3b5873db1c30687b63c51f1f8078d80f3ca2381698ec305444533222ba3a5100"
STATES = {
    "planned", "ready", "coding", "review", "testing", "changes_requested",
    "blocked", "accepted", "merged", "deferred", "cancelled",
}
TASK_COLUMNS = [
    "task_id", "parent_wp", "milestone", "title", "depends_on", "status",
    "base_commit", "candidate_commit", "merged_commit", "task_card",
    "review_ref", "evidence_ref", "docs_ref",
]


def regular_inventory(root):
    if root.is_symlink() or not root.is_dir():
        raise ValueError("root must be a real directory")
    root = root.resolve()
    files = {}
    total = 0
    for folder, directories, names in os.walk(root, followlinks=False):
        for name in directories + names:
            path = Path(folder) / name
            entry = path.lstat()
            relative = path.relative_to(root).as_posix()
            if stat.S_ISLNK(entry.st_mode):
                raise ValueError("symlink is not allowed: " + repr(relative))
            if stat.S_ISREG(entry.st_mode):
                files[relative] = path
                total += entry.st_size
            elif not stat.S_ISDIR(entry.st_mode):
                raise ValueError("special file is not allowed: " + repr(relative))
            if len(files) > 2000 or total > 32 * 1024 * 1024:
                raise ValueError("workflow lint inventory exceeds its 2000-file/32-MiB bounds")
    return root, files


def markdown_prose(text, label, errors):
    """Remove fenced code; flag unclosed fences. No claim of full GFM parsing."""
    lines = []
    fence = None
    for line in text.splitlines():
        mark = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if fence is None and mark:
            fence = (mark[1][0], len(mark[1]))
            continue
        if fence is not None:
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= fence[1] and not mark[2].strip():
                fence = None
            continue
        lines.append(line)
    if fence is not None:
        errors.append(label + ": unclosed Markdown fence")
    return "\n".join(lines)


def local_target(root, parent, target):
    decoded = unquote(target)
    if "\\" in decoded or any(ord(c) < 32 for c in decoded):
        raise ValueError("unsupported path characters")
    result = (parent / decoded).resolve()
    result.relative_to(root)
    return result


def validate(root):
    root, files = regular_inventory(root)
    errors = []
    markdown_count = 0
    link_count = 0
    csv_count = 0
    parsed = {}
    for relative, path in sorted(files.items()):
        if path.suffix not in {".md", ".csv"}:
            continue
        if relative == ORIGINAL:
            if hashlib.sha256(path.read_bytes()).hexdigest() != ORIGINAL_SHA256:
                errors.append("historical original differs from its recorded identity")
            continue
        if relative == BASELINE and hashlib.sha256(path.read_bytes()).hexdigest() != BASELINE_SHA256:
            errors.append("active v1.5.1 baseline differs from its distribution identity")
        text = path.read_text(encoding="utf-8")
        if re.search(r"actools-pl/actoolsDrupal|rewrite/community-v1\.|pre-rewrite-", text):
            errors.append(relative + ": superseded repository/ref in active content")
        if not text.endswith("\n"):
            errors.append(relative + ": missing final newline")
        if path.suffix == ".md":
            markdown_count += 1
            prose = markdown_prose(text, relative, errors)
            # Package links use simple inline Markdown destinations. Anchors and
            # external URLs are intentionally not fetched/validated.
            for destination in re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", prose):
                url = urlsplit(destination)
                if url.scheme or url.netloc or not url.path:
                    continue
                link_count += 1
                try:
                    target = local_target(root, path.parent, url.path)
                except ValueError:
                    errors.append(relative + ": link outside package or unsupported path " + repr(destination))
                    continue
                if not target.exists():
                    errors.append(relative + ": missing linked path " + repr(destination))
        else:
            csv_count += 1
            rows = list(csv.reader(io.StringIO(text), strict=True))
            if not rows or not rows[0] or len(set(rows[0])) != len(rows[0]):
                errors.append(relative + ": absent/duplicate CSV header")
                continue
            for line, row in enumerate(rows[1:], 2):
                if len(row) != len(rows[0]):
                    errors.append(relative + ": inconsistent CSV width at row " + str(line))
            parsed[relative] = rows
    if BASELINE not in files:
        errors.append("immutable v1.5.1 baseline missing")
    if ORIGINAL not in files:
        errors.append("historical original reference missing")
    if BASELINE in files:
        spec = files[BASELINE].read_text(encoding="utf-8")
        if "actools migration discover" in spec or re.search(r"`migration\.(?:import|cutover)`", spec):
            errors.append("excluded migration command/action in active specification")
        for token in ("FRESH-T01", "FRESH-T02", "FRESH-T03", "FRESH-T04"):
            if token not in spec:
                errors.append("missing fresh-install scope case " + token)
    ledger = parsed.get("records/TASK_LEDGER.csv")
    tasks = {}
    if not ledger or ledger[0] != TASK_COLUMNS:
        errors.append("task ledger missing or columns differ from this package contract")
    else:
        for row in ledger[1:]:
            if len(row) != len(TASK_COLUMNS):
                continue
            item = dict(zip(TASK_COLUMNS, row))
            task = item["task_id"]
            if not re.fullmatch(r"(?:BOOT|CP)-\d{3}(?:-[A-Za-z0-9]+)?", task):
                errors.append("invalid task ID " + repr(task))
            if task in tasks:
                errors.append("duplicate task ID " + repr(task))
            tasks[task] = item
            if item["status"] not in STATES:
                errors.append(task + ": invalid task lifecycle state " + repr(item["status"]))
            card = item["task_card"]
            if card not in {"", "UNSET"}:
                try:
                    if not local_target(root, root, card).is_file():
                        errors.append(task + ": task card missing")
                except ValueError:
                    errors.append(task + ": unsafe task-card path")
        graph = {}
        for task, item in tasks.items():
            refs = item["depends_on"].split(";") if item["depends_on"] != "NONE" else []
            graph[task] = refs
            if len(refs) != len(set(refs)):
                errors.append(task + ": duplicate dependency")
            for dep in refs:
                if dep not in tasks:
                    errors.append(task + ": unknown dependency " + repr(dep))
                elif item["status"] not in {"cancelled", "deferred"} and tasks[dep]["status"] == "cancelled":
                    errors.append(task + ": active task depends on cancelled " + dep)
        for task in ("CP-038", "CP-039"):
            if task not in tasks or tasks[task]["status"] != "cancelled":
                errors.append(task + ": excluded migration task must remain cancelled")
        if "BOOT-000" not in tasks or tasks.get("BOOT-001", {}).get("depends_on") != "BOOT-000":
            errors.append("new-root bootstrap dependency is missing")
        # Iterative traversal avoids recursion depth depending on ledger input.
        remaining = {task: set(refs) & tasks.keys() for task, refs in graph.items()}
        while remaining:
            ready = {task for task, refs in remaining.items() if not refs}
            if not ready:
                errors.append("task dependencies contain a cycle: " + repr(sorted(remaining)))
                break
            remaining = {task: refs - ready for task, refs in remaining.items() if task not in ready}
    docs = parsed.get("records/DOCUMENTATION_REGISTER.csv")
    if docs:
        if "document_id" not in docs[0] or "relative_path" not in docs[0]:
            errors.append("documentation register lacks required path/identity columns")
        else:
            seen = set()
            for row in docs[1:]:
                if len(row) != len(docs[0]):
                    continue
                item = dict(zip(docs[0], row))
                identifier = item["document_id"]
                if identifier in seen:
                    errors.append("duplicate document ID " + repr(identifier))
                seen.add(identifier)
                if identifier.startswith("PKG-"):
                    try:
                        if not local_target(root, root, item["relative_path"]).is_file():
                            errors.append(identifier + ": package document missing")
                    except ValueError:
                        errors.append(identifier + ": unsafe document path")
    else:
        errors.append("documentation register missing")
    return {"files": len(files), "markdown": markdown_count, "links": link_count,
            "csv": csv_count, "tasks": len(tasks)}, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path,
                        default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    try:
        counts, errors = validate(args.root)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print("LINT ERROR: " + ascii(str(exc)), file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("LINT FINDING: " + ascii(error), file=sys.stderr)
        return 1
    print("OK: workflow structure checked: " + str(counts))
    print("This does not verify evidence, Git/host state, semantic completeness or product readiness.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
