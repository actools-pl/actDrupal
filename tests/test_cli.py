from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXPECTED_HUMAN = "actools 0.1.0.dev0\n"
EXPECTED_JSON = '{"program":"actools","version":"0.1.0.dev0"}\n'


def cli(*args: str, stdin=None, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, "-m", "actools.cli", *args],
        cwd=ROOT,
        stdin=stdin,
        text=True,
        capture_output=True,
        timeout=5,
        env=env,
    )


def test_human_version_is_exact_plain_and_finite() -> None:
    result = cli("version")
    assert result.returncode == 0
    assert result.stdout == EXPECTED_HUMAN
    assert result.stderr == ""
    assert "\x1b" not in result.stdout
    assert len(result.stdout) < 80


def test_json_version_is_exact_and_valid() -> None:
    result = cli("version", "--format", "json")
    assert result.returncode == 0
    assert result.stdout == EXPECTED_JSON
    assert result.stderr == ""
    assert json.loads(result.stdout) == {"program": "actools", "version": "0.1.0.dev0"}


def test_help_advertises_only_implemented_surface() -> None:
    result = cli("--help")
    assert result.returncode == 0
    assert "version" in result.stdout
    for deferred in ("install", "update", "doctor", "backup", "restore"):
        assert deferred not in result.stdout.lower()
    assert result.stderr == ""


def test_version_help_is_available() -> None:
    result = cli("version", "--help")
    assert result.returncode == 0
    assert "--format" in result.stdout
    assert result.stderr == ""


def test_no_args_is_finite_plain_help() -> None:
    result = cli()
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
    assert "\x1b" not in result.stdout
    assert len(result.stdout) < 2000
    assert result.stderr == ""


def test_unsupported_command_is_honest_nonzero_error() -> None:
    result = cli("install", stdin=subprocess.DEVNULL)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "invalid choice" in result.stderr.lower()
    assert len(result.stderr) < 2000


def test_closed_stdin_cannot_hang_version_or_help() -> None:
    version = cli("version", stdin=subprocess.DEVNULL)
    help_result = cli("--help", stdin=subprocess.DEVNULL)
    assert version.returncode == 0
    assert help_result.returncode == 0


def test_environment_secret_canary_is_not_emitted() -> None:
    canary = "CP001_SECRET_CANARY_DO_NOT_PRINT"
    result = cli("version", env_extra={"CP001_CANARY": canary})
    assert canary not in result.stdout
    assert canary not in result.stderr


def test_broken_pipe_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    from actools import cli as module

    class Broken(io.StringIO):
        def write(self, text: str) -> int:
            raise BrokenPipeError

    monkeypatch.setattr(module.sys, "stdout", Broken())
    assert module.main(["version"]) == module.BROKEN_PIPE_EXIT
