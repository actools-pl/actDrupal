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
EXPECTED_ERROR = "actools: error: invalid invocation\n"


def cli(*args: str, stdin=None, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, "-S", "-m", "actools.cli", *args],
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


def test_equals_form_is_supported_without_widening_surface() -> None:
    result = cli("version", "--format=json")
    assert result.returncode == 0
    assert result.stdout == EXPECTED_JSON
    assert result.stderr == ""


def test_help_advertises_only_implemented_surface() -> None:
    result = cli("--help")
    assert result.returncode == 0
    assert "version" in result.stdout
    for deferred in ("install", "update", "doctor", "backup", "restore"):
        assert deferred not in result.stdout.lower()
    assert "\x1b" not in result.stdout
    assert len(result.stdout) < 2000
    assert result.stderr == ""


def test_version_help_is_available() -> None:
    result = cli("version", "--help")
    assert result.returncode == 0
    assert "--format" in result.stdout
    assert "\x1b" not in result.stdout
    assert len(result.stdout) < 2000
    assert result.stderr == ""


def test_no_args_is_finite_plain_help() -> None:
    result = cli()
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
    assert "\x1b" not in result.stdout
    assert len(result.stdout) < 2000
    assert result.stderr == ""


@pytest.mark.parametrize(
    "args",
    [
        ("install",),
        ("version", "--unknown"),
        ("version", "--format"),
        ("version", "--format", "xml"),
        ("version", "--format=xml"),
        ("version", "extra"),
    ],
)
def test_invalid_invocation_uses_contract_exit_three(args: tuple[str, ...]) -> None:
    result = cli(*args, stdin=subprocess.DEVNULL)
    assert result.returncode == 3
    assert result.stdout == ""
    assert result.stderr == EXPECTED_ERROR


def test_rejected_values_are_not_reflected_or_terminal_active() -> None:
    secret = "CP001_SYNTHETIC_SECRET_VALUE"
    ansi = "\x1b[31mRED\x1b[0m"
    long_value = "X" * 10_000
    for rejected in (secret, ansi, long_value):
        result = cli("version", "--format", rejected, stdin=subprocess.DEVNULL)
        assert result.returncode == 3
        assert result.stdout == ""
        assert result.stderr == EXPECTED_ERROR
        assert rejected not in result.stderr
        assert "\x1b" not in result.stderr
        assert len(result.stderr) < 128


def test_closed_stdin_cannot_hang_version_or_help() -> None:
    for args in (("version",), ("--help",), ("version", "--help"), ()):
        result = cli(*args, stdin=subprocess.DEVNULL)
        assert result.returncode == 0


def test_environment_secret_canary_is_not_emitted_on_success_or_error() -> None:
    canary = "CP001_SECRET_CANARY_DO_NOT_PRINT"
    for args in (("version",), ("install",)):
        result = cli(*args, env_extra={"CP001_CANARY": canary})
        assert canary not in result.stdout
        assert canary not in result.stderr


def test_broken_pipe_write_and_flush_are_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    from actools import cli as module

    class BrokenWrite(io.StringIO):
        def write(self, text: str) -> int:
            raise BrokenPipeError

    monkeypatch.setattr(module.sys, "stdout", BrokenWrite())
    assert module.main(["version"]) == module.OUTPUT_FAILURE_EXIT

    class BrokenFlush(io.StringIO):
        def flush(self) -> None:
            raise BrokenPipeError

    monkeypatch.setattr(module.sys, "stdout", BrokenFlush())
    assert module.main(["--help"]) == module.OUTPUT_FAILURE_EXIT


def _closed_pipe_result(args: tuple[str, ...], *, unbuffered: bool) -> tuple[int, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    command = [sys.executable, "-S"]
    if unbuffered:
        command.append("-u")
    command.extend(["-m", "actools.cli", *args])
    proc = subprocess.Popen(
        command,
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    assert proc.stdout is not None
    assert proc.stderr is not None
    proc.stdout.close()  # the child now writes to a pipe with no reader
    try:
        returncode = proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=2)
        pytest.fail("CLI hung after its stdout pipe reader closed")
    stderr = proc.stderr.read()
    return returncode, stderr


@pytest.mark.parametrize("unbuffered", [False, True])
@pytest.mark.parametrize(
    "args",
    [
        (),
        ("--help",),
        ("version", "--help"),
        ("version",),
        ("version", "--format", "json"),
    ],
)
def test_real_closed_pipe_never_reports_false_success_or_shutdown_traceback(
    args: tuple[str, ...], unbuffered: bool
) -> None:
    returncode, stderr = _closed_pipe_result(args, unbuffered=unbuffered)
    assert returncode == 3
    assert stderr == ""
