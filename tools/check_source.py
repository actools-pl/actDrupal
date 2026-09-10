#!/usr/bin/env python3
"""Canonical CP-001 source checks used locally and by GitHub Actions."""

from __future__ import annotations

import hashlib
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
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Mapping

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
LOCK_WHEEL_ONLY = "--only-binary :all:"
SOURCE_WHEEL_ONLY = "--only-binary=:all:"
WORKFLOW = ROOT / ".github" / "workflows" / "source-ci.yml"
DIST_INFO = "actools_drupal-0.1.0.dev0.dist-info"
EXPECTED_WHEEL_MEMBERS = {
    "actools/__init__.py",
    "actools/cli.py",
    f"{DIST_INFO}/licenses/LICENSE",
    f"{DIST_INFO}/licenses/NOTICE.md",
    f"{DIST_INFO}/METADATA",
    f"{DIST_INFO}/WHEEL",
    f"{DIST_INFO}/entry_points.txt",
    f"{DIST_INFO}/top_level.txt",
    f"{DIST_INFO}/RECORD",
}
EXPECTED_WORKFLOW = f'''name: Source CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  source:
    name: source
    runs-on: ubuntu-26.04
    timeout-minutes: 15
    steps:
      - name: Checkout
        uses: actions/checkout@{CHECKOUT_SHA} # v7.0.1
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@{SETUP_PYTHON_SHA} # v7.0.0
        with:
          python-version: "3.14.7"

      - name: Install locked source-check tools
        run: python -m pip install --require-hashes -r requirements/ci.lock

      - name: Run canonical source checks
        env:
          PYTHONUTF8: "1"
        run: python tools/check_source.py
'''


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


def _canonical_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


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


def locked_packages() -> dict[str, str]:
    expected: dict[str, str] = {}
    records = requirement_records(LOCK.read_text(encoding="utf-8"))
    for record in records:
        if record.startswith("--"):
            continue
        match = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]+\])?==([^\s]+)(?:\s|$)", record)
        if not match:
            raise CheckFailure(f"cannot parse locked distribution identity: {record}")
        name = _canonical_name(match.group(1))
        version = match.group(2)
        if name in expected:
            raise CheckFailure(f"duplicate distribution in CI lock: {name}")
        expected[name] = version
    if not expected:
        raise CheckFailure("CI lock contains no distributions")
    return expected


def classify_scanner_result(
    *,
    executed: bool,
    returncode: int | None,
    payload: str,
    expected_packages: Mapping[str, str],
) -> ScannerResult:
    """Fail closed unless pinned pip-audit reports complete clean coverage."""
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

    # pip-audit 2.10.1 JsonFormat emits exactly this manifest envelope.
    if not isinstance(parsed, dict) or set(parsed) != {"dependencies", "fixes"}:
        return ScannerResult("ERROR", False, "scanner JSON envelope is invalid")
    dependencies = parsed.get("dependencies")
    fixes = parsed.get("fixes")
    if not isinstance(dependencies, list) or not isinstance(fixes, list) or fixes:
        return ScannerResult("ERROR", False, "scanner JSON manifest fields are invalid")
    if not dependencies:
        return ScannerResult("ERROR", False, "scanner reported empty dependency coverage")

    observed: dict[str, str] = {}
    for dependency in dependencies:
        if not isinstance(dependency, dict):
            return ScannerResult("ERROR", False, "scanner dependency record is not an object")
        if "skip_reason" in dependency:
            return ScannerResult("ERROR", False, "scanner skipped one or more dependencies")
        if set(dependency) != {"name", "version", "vulns"}:
            return ScannerResult("ERROR", False, "scanner dependency record has missing or unexpected fields")
        name = dependency.get("name")
        version = dependency.get("version")
        vulns = dependency.get("vulns")
        if not isinstance(name, str) or not name.strip() or not isinstance(version, str) or not version.strip():
            return ScannerResult("ERROR", False, "scanner dependency identity is invalid")
        if not isinstance(vulns, list):
            return ScannerResult("ERROR", False, "scanner vulnerability field is invalid")
        canonical = _canonical_name(name)
        if canonical in observed:
            return ScannerResult("ERROR", False, f"scanner duplicated dependency: {canonical}")
        observed[canonical] = version
        if vulns:
            return ScannerResult("VULNERABLE", False, f"scanner reported vulnerability for {canonical}")

    expected = {_canonical_name(name): version for name, version in expected_packages.items()}
    if observed != expected:
        missing = sorted(set(expected) - set(observed))
        unexpected = sorted(set(observed) - set(expected))
        mismatched = sorted(name for name in set(expected) & set(observed) if expected[name] != observed[name])
        detail = f"scanner coverage mismatch: missing={missing}; unexpected={unexpected}; version_mismatch={mismatched}"
        return ScannerResult("ERROR", False, detail)

    return ScannerResult("PASS", True, f"complete clean coverage for {len(expected)} locked distributions")


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


def verify_lock() -> None:
    text = LOCK.read_text(encoding="utf-8")
    records = requirement_records(text)
    options = [record for record in records if record.startswith("--")]
    if options != [LOCK_WHEEL_ONLY]:
        raise CheckFailure("CI lock must contain only the canonical wheel-only artifact directive")
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
    packages = locked_packages()
    for package, version in direct.items():
        if packages.get(package) != version:
            raise CheckFailure(f"direct source input is absent or changed in lock: {package}=={version}")

    source_records = requirement_records((ROOT / "requirements" / "ci.in").read_text(encoding="utf-8"))
    source_options = [record for record in source_records if record.startswith("--")]
    if source_options != [SOURCE_WHEEL_ONLY]:
        raise CheckFailure("requirements/ci.in must contain only the activated wheel-only artifact directive")
    source_requirements = {record for record in source_records if not record.startswith("--")}
    expected_source = {f"{package}=={version}" for package, version in direct.items()}
    if source_requirements != expected_source:
        raise CheckFailure("requirements/ci.in does not exactly match the activated direct source-tool contract")


def verify_workflow_text(text: str) -> None:
    normalised = text.replace("\r\n", "\n")
    if normalised != EXPECTED_WORKFLOW:
        raise CheckFailure("source CI workflow differs from the exact approved CP-001 structure")


def verify_workflow() -> None:
    verify_workflow_text(WORKFLOW.read_text(encoding="utf-8"))


def _safe_wheel_member(name: str) -> None:
    if not name or "\\" in name or name.startswith("/") or name.endswith("/"):
        raise CheckFailure(f"ambiguous wheel member path: {name!r}")
    parts = PurePosixPath(name).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise CheckFailure(f"unsafe wheel member path: {name!r}")


def verify_wheel_inventory(wheel: Path) -> str:
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise CheckFailure("wheel contains duplicate archive member names")
        for name in names:
            _safe_wheel_member(name)
        actual = set(names)
        if actual != EXPECTED_WHEEL_MEMBERS:
            missing = sorted(EXPECTED_WHEEL_MEMBERS - actual)
            unexpected = sorted(actual - EXPECTED_WHEEL_MEMBERS)
            raise CheckFailure(f"wheel inventory mismatch: missing={missing}; unexpected={unexpected}")

        metadata = BytesParser().parsebytes(archive.read(f"{DIST_INFO}/METADATA"))
        if metadata.get("Name") != "actools-drupal" or metadata.get("Version") != "0.1.0.dev0":
            raise CheckFailure("wheel distribution identity/version is incorrect")
        if metadata.get("Requires-Python") not in {">=3.14,<3.15", "<3.15,>=3.14"}:
            raise CheckFailure("wheel Requires-Python metadata is incorrect")
        if metadata.get_all("Requires-Dist"):
            raise CheckFailure("wheel unexpectedly declares runtime dependencies")
        if metadata.get("License-Expression") != "MIT":
            raise CheckFailure("wheel license expression is not MIT")

        entry_points = archive.read(f"{DIST_INFO}/entry_points.txt").decode("utf-8")
        if entry_points != "[console_scripts]\nactools = actools.cli:main\n":
            raise CheckFailure("wheel console-script entry point is not exact")
        if archive.read(f"{DIST_INFO}/top_level.txt").decode("utf-8") != "actools\n":
            raise CheckFailure("wheel top-level package metadata is not exact")

        wheel_meta = BytesParser().parsebytes(archive.read(f"{DIST_INFO}/WHEEL"))
        if wheel_meta.get("Root-Is-Purelib") != "true" or wheel_meta.get("Tag") != "py3-none-any":
            raise CheckFailure("wheel platform/purelib metadata is unexpected")
        if wheel_meta.get("Generator") != "setuptools (84.0.0)":
            raise CheckFailure("wheel was not generated by the activated setuptools version")

        for leaf in ("LICENSE", "NOTICE.md"):
            packaged = archive.read(f"{DIST_INFO}/licenses/{leaf}")
            if packaged != (ROOT / leaf).read_bytes():
                raise CheckFailure(f"wheel packaged {leaf} differs from repository source")

    return hashlib.sha256(wheel.read_bytes()).hexdigest()


def verify_negative_fixtures() -> None:
    deliberate = run([sys.executable, "tests/fixtures/deliberate_failure.py"], check=False)
    marker = "CP-001 intentional negative-test fixture"
    if deliberate.returncode != 1 or marker not in deliberate.stderr:
        raise CheckFailure("deliberate failure fixture did not fail for its intended marker")

    invalid = run(
        [sys.executable, "-m", "build", "--wheel", "--no-isolation", "tests/fixtures/invalid_package"],
        check=False,
    )
    backend_marker = "cp001_intentionally_missing_backend"
    combined = invalid.stdout + "\n" + invalid.stderr
    if invalid.returncode == 0 or backend_marker not in combined:
        raise CheckFailure("invalid-package fixture did not fail for the intentionally missing backend")


def _clean_subprocess_env() -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV"}}
    env["PYTHONNOUSERSITE"] = "1"
    return env


def verify_installed_cli(wheel: Path, directory: Path, wheel_sha256: str) -> None:
    env_dir = directory / "installed"
    venv.EnvBuilder(with_pip=True, clear=True).create(env_dir)
    scripts = "Scripts" if os.name == "nt" else "bin"
    python = env_dir / scripts / ("python.exe" if os.name == "nt" else "python")
    launcher = env_dir / scripts / ("actools.exe" if os.name == "nt" else "actools")
    env = _clean_subprocess_env()

    run([str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)], cwd=directory, env=env)
    if not launcher.is_file():
        raise CheckFailure("installed actools console launcher is missing")

    expected = "actools 0.1.0.dev0\n"
    human = run([str(launcher), "version"], cwd=directory, env=env)
    if human.stdout != expected or human.stderr:
        raise CheckFailure("installed launcher human version output is not exact/plain")
    machine = run([str(launcher), "version", "--format", "json"], cwd=directory, env=env)
    if machine.stdout != '{"program":"actools","version":"0.1.0.dev0"}\n' or machine.stderr:
        raise CheckFailure("installed launcher JSON version output is not exact")
    root_help = run([str(launcher), "--help"], cwd=directory, env=env)
    version_help = run([str(launcher), "version", "--help"], cwd=directory, env=env)
    if "version" not in root_help.stdout or "install" in root_help.stdout.lower() or "--format" not in version_help.stdout:
        raise CheckFailure("installed launcher help surface is incorrect")
    unsupported = run([str(launcher), "install"], cwd=directory, check=False, stdin=subprocess.DEVNULL, env=env)
    if unsupported.returncode != 3 or unsupported.stderr != "actools: error: invalid invocation\n":
        raise CheckFailure("installed launcher unsupported invocation contract is incorrect")

    probe_code = (
        "import actools, importlib.metadata, json, pathlib; "
        "m=importlib.metadata.metadata('actools-drupal'); "
        "print(json.dumps({'module':str(pathlib.Path(actools.__file__).resolve()),"
        "'version':importlib.metadata.version('actools-drupal'),"
        "'requires':m.get_all('Requires-Dist') or []}, sort_keys=True))"
    )
    probe = run([str(python), "-I", "-c", probe_code], cwd=directory, env=env)
    info = json.loads(probe.stdout)
    module_path = Path(info["module"]).resolve()
    if not module_path.is_relative_to(env_dir.resolve()) or module_path.is_relative_to(ROOT.resolve()):
        raise CheckFailure("installed import did not originate from the fresh virtual environment")
    if info["version"] != "0.1.0.dev0" or info["requires"] != []:
        raise CheckFailure("installed distribution identity/version/runtime dependency metadata is incorrect")
    if hashlib.sha256(wheel.read_bytes()).hexdigest() != wheel_sha256:
        raise CheckFailure("wheel changed between inventory and installed-launcher checks")


def run_audit() -> None:
    expected = locked_packages()
    with tempfile.TemporaryDirectory(prefix="actools-audit-") as tmp:
        audit_input = Path(tmp) / "requirements.txt"
        lines = [line for line in LOCK.read_text(encoding="utf-8").splitlines() if line.strip() != LOCK_WHEEL_ONLY]
        audit_input.write_text("\n".join(lines) + "\n", encoding="utf-8")
        audit = run(
            [
                sys.executable,
                "-m",
                "pip_audit",
                "--strict",
                "--require-hashes",
                "--no-deps",
                "--disable-pip",
                "--progress-spinner=off",
                "--timeout=15",
                "--format=json",
                "-r",
                str(audit_input),
            ],
            check=False,
        )
    result = classify_scanner_result(
        executed=True,
        returncode=audit.returncode,
        payload=audit.stdout,
        expected_packages=expected,
    )
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
            wheel_sha256 = verify_wheel_inventory(wheels[0])
            verify_installed_cli(wheels[0], work, wheel_sha256)
        run_audit()
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print(f"SOURCE-CI: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"SOURCE-CI: WHEEL-SHA256 {wheel_sha256}")
    print("SOURCE-CI: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
