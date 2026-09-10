#!/usr/bin/env python3
"""Canonical CP-001 source checks used locally and by GitHub Actions."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import subprocess
import sys
import tempfile
import venv
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PYTHON = (3, 14, 7)
EXPECTED_TOOLS = {
    "build": "1.6.0",
    "pip": "26.2.1",
    "pip-audit": "2.10.1",
    "pytest": "9.1.1",
    "setuptools": "84.0.0",
}
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"
LOCK = ROOT / "requirements" / "ci.lock"
WORKFLOW = ROOT / ".github" / "workflows" / "source-ci.yml"


class CheckFailure(RuntimeError):
    """A required source check could not establish its assertion."""


@dataclass(frozen=True)
class ScannerResult:
    status: str
    passing: bool
    detail: str


def _bounded(text: str, limit: int = 4000) -> str:
    if len(text) <= limit:
        return text
    return "...[truncated]...\n" + text[-limit:]


def run(command: list[str], *, cwd: Path = ROOT, check: bool = True, **kwargs) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=120,
        **kwargs,
    )
    if check and proc.returncode != 0:
        raise CheckFailure(
            f"command failed ({proc.returncode}): {' '.join(command)}\n"
            f"stdout:\n{_bounded(proc.stdout)}\nstderr:\n{_bounded(proc.stderr)}"
        )
    return proc


def classify_scanner_result(*, executed: bool, returncode: int | None, payload: str) -> ScannerResult:
    """Fail closed: only a successful, valid, vulnerability-free scan can pass."""
    if not executed:
        return ScannerResult("UNAVAILABLE", False, "scanner did not execute")
    if returncode is None:
        return ScannerResult("ERROR", False, "scanner return code is unknown")
    if returncode != 0:
        return ScannerResult("VULNERABLE" if returncode == 1 else "ERROR", False, f"scanner exit {returncode}")
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        return ScannerResult("ERROR", False, f"invalid scanner JSON: {exc}")
    if not isinstance(parsed, list):
        return ScannerResult("ERROR", False, "scanner JSON must be a dependency list")
    for dependency in parsed:
        if not isinstance(dependency, dict) or not isinstance(dependency.get("vulns", []), list):
            return ScannerResult("ERROR", False, "scanner JSON dependency shape is invalid")
        if dependency.get("vulns"):
            return ScannerResult("VULNERABLE", False, "scanner reported one or more vulnerabilities")
    return ScannerResult("PASS", True, "valid scan reported no known vulnerabilities")


def verify_environment() -> None:
    actual = sys.version_info[:3]
    if actual != EXPECTED_PYTHON:
        raise CheckFailure(f"CPython {EXPECTED_PYTHON!s} required; running {actual!s}")
    mismatches: list[str] = []
    for distribution, expected in EXPECTED_TOOLS.items():
        try:
            actual_version = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            actual_version = "MISSING"
        if actual_version != expected:
            mismatches.append(f"{distribution}={actual_version} (expected {expected})")
    if mismatches:
        raise CheckFailure("tool version mismatch: " + "; ".join(mismatches))


def requirement_records(text: str) -> list[str]:
    logical: list[str] = []
    current = ""
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if current:
            current += " " + stripped
        else:
            current = stripped
        if current.endswith("\\"):
            current = current[:-1].rstrip()
            continue
        logical.append(current)
        current = ""
    if current:
        logical.append(current)
    return logical


def verify_lock() -> None:
    text = LOCK.read_text(encoding="utf-8")
    records = requirement_records(text)
    if not records or records[0] != "--only-binary=:all:":
        raise CheckFailure("CI lock must fail closed to wheel-only artifacts")
    requirements = [record for record in records if not record.startswith("--")]
    if len(requirements) < 10:
        raise CheckFailure("CI lock dependency closure is unexpectedly small")
    for record in requirements:
        if "==" not in record:
            raise CheckFailure(f"un-pinned requirement: {record}")
        hashes = re.findall(r"--hash=sha256:([0-9a-f]{64})(?:\s|$)", record)
        if not hashes:
            raise CheckFailure(f"requirement lacks SHA-256 hash: {record}")

    direct = {
        "build": "1.6.0",
        "pip": "26.2.1",
        "pip-audit": "2.10.1",
        "pytest": "9.1.1",
        "setuptools": "84.0.0",
    }
    for package, version in direct.items():
        prefix = f"{package}=={version} "
        if not any(record.lower().startswith(prefix) for record in requirements):
            raise CheckFailure(f"direct source input is absent or changed in lock: {package}=={version}")

    source_records = requirement_records((ROOT / "requirements" / "ci.in").read_text(encoding="utf-8"))
    source_requirements = {record for record in source_records if not record.startswith("--")}
    expected_source = {f"{package}=={version}" for package, version in direct.items()}
    if source_requirements != expected_source:
        raise CheckFailure("requirements/ci.in does not exactly match the activated direct source-tool contract")


def verify_workflow() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    required = [
        "pull_request:",
        "push:",
        "permissions:\n  contents: read",
        "runs-on: ubuntu-24.04",
        'python-version: "3.14.7"',
        f"actions/checkout@{CHECKOUT_SHA}",
        f"actions/setup-python@{SETUP_PYTHON_SHA}",
        "persist-credentials: false",
        "python -m pip install --require-hashes -r requirements/ci.lock",
        "python tools/check_source.py",
    ]
    missing = [needle for needle in required if needle not in text]
    if missing:
        raise CheckFailure("workflow missing required controls: " + ", ".join(missing))
    forbidden = [
        "pull_request_target",
        "workflow_dispatch",
        "schedule:",
        "self-hosted",
        "secrets.",
        "id-token:",
        "contents: write",
        "actions: write",
        "packages: write",
        "deployments: write",
    ]
    present = [needle for needle in forbidden if needle in text]
    if present:
        raise CheckFailure("workflow contains forbidden authority/trigger: " + ", ".join(present))


def verify_wheel_inventory(wheel: Path) -> None:
    forbidden_fragments = (
        ".git",
        "coding/",
        "tests/",
        "tools/",
        "fixtures/",
        ".env",
        "credential",
        "secret",
        "experiment",
        "seed",
    )
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if not names:
            raise CheckFailure("built wheel is empty")
        for name in names:
            lowered = name.lower()
            blocked_prefixes = (".git/", "coding/", "tests/", "tools/", "fixtures/")
            blocked_names = (".env", "credentials", "credentials.json", "secrets", "secrets.json")
            if lowered.startswith(blocked_prefixes) or Path(lowered).name in blocked_names:
                raise CheckFailure(f"forbidden wheel member: {name}")
            if any(fragment in Path(lowered).name for fragment in ("credential", "secret", "experiment", "seed")):
                raise CheckFailure(f"forbidden wheel member: {name}")
            if not (name.startswith("actools/") or ".dist-info/" in name):
                raise CheckFailure(f"unexpected wheel member: {name}")
        required = {"actools/__init__.py", "actools/cli.py"}
        if not required.issubset(names):
            raise CheckFailure("wheel does not contain the complete minimal actools package")


def verify_negative_fixtures() -> None:
    deliberate = run([sys.executable, "tests/fixtures/deliberate_failure.py"], check=False)
    if deliberate.returncode == 0:
        raise CheckFailure("deliberate failure fixture unexpectedly passed")
    invalid = run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation", "tests/fixtures/invalid_package"],
        check=False,
    )
    if invalid.returncode == 0:
        raise CheckFailure("invalid-package fixture unexpectedly built")


def verify_installed_cli(wheel: Path, directory: Path) -> None:
    env_dir = directory / "installed"
    venv.EnvBuilder(with_pip=True, clear=True).create(env_dir)
    scripts = "Scripts" if os.name == "nt" else "bin"
    python = env_dir / scripts / ("python.exe" if os.name == "nt" else "python")
    run([str(python), "-m", "pip", "install", "--no-deps", str(wheel)], cwd=directory)
    expected = "actools 0.1.0.dev0\n"
    human = run([str(python), "-m", "actools.cli", "version"], cwd=directory)
    if human.stdout != expected or human.stderr:
        raise CheckFailure("installed human version output is not exact/plain")
    machine = run([str(python), "-m", "actools.cli", "version", "--format", "json"], cwd=directory)
    if machine.stdout != '{"program":"actools","version":"0.1.0.dev0"}\n' or machine.stderr:
        raise CheckFailure("installed JSON version output is not exact")
    help_result = run([str(python), "-m", "actools.cli", "--help"], cwd=directory)
    if "version" not in help_result.stdout or "install" in help_result.stdout.lower():
        raise CheckFailure("installed help is missing version or advertises deferred installation")
    unsupported = run([str(python), "-m", "actools.cli", "install"], cwd=directory, check=False, stdin=subprocess.DEVNULL)
    if unsupported.returncode == 0 or "invalid choice" not in unsupported.stderr.lower():
        raise CheckFailure("unsupported invocation did not fail honestly")


def run_audit() -> None:
    with tempfile.TemporaryDirectory(prefix="actools-audit-") as tmp:
        audit_input = Path(tmp) / "requirements.txt"
        lines = [line for line in LOCK.read_text(encoding="utf-8").splitlines() if line.strip() != "--only-binary=:all:"]
        audit_input.write_text("\n".join(lines) + "\n", encoding="utf-8")
        audit = run(
            [
                sys.executable,
                "-m",
                "pip_audit",
                "--strict",
                "--require-hashes",
                "--disable-pip",
                "--progress-spinner=off",
                "--timeout=15",
                "--format=json",
                "-r",
                str(audit_input),
            ],
            check=False,
        )
    result = classify_scanner_result(executed=True, returncode=audit.returncode, payload=audit.stdout)
    if not result.passing:
        raise CheckFailure(
            f"dependency vulnerability check did not pass: {result.status}: {result.detail}\n"
            f"{_bounded(audit.stderr)}"
        )


def main() -> int:
    try:
        verify_environment()
        verify_lock()
        verify_workflow()
        run([sys.executable, "-m", "pytest", "-q"])
        verify_negative_fixtures()
        with tempfile.TemporaryDirectory(prefix="actools-cp001-") as tmp:
            work = Path(tmp)
            out = work / "dist"
            out.mkdir()
            run([sys.executable, "-m", "build", "--wheel", "--no-isolation", "--outdir", str(out), "."])
            wheels = list(out.glob("*.whl"))
            if len(wheels) != 1:
                raise CheckFailure(f"expected one wheel, found {len(wheels)}")
            verify_wheel_inventory(wheels[0])
            verify_installed_cli(wheels[0], work)
        run_audit()
    except (CheckFailure, OSError, subprocess.SubprocessError) as exc:
        print(f"SOURCE-CI: FAIL: {exc}", file=sys.stderr)
        return 1
    print("SOURCE-CI: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
