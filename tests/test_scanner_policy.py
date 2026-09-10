from __future__ import annotations

from pathlib import Path

import pytest

from tools.check_source import classify_scanner_result

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "scanner_policy"


def test_clean_valid_scan_is_the_only_pass() -> None:
    result = classify_scanner_result(executed=True, returncode=0, payload="[]")
    assert result.passing is True
    assert result.status == "PASS"


def test_unavailable_scan_cannot_pass() -> None:
    result = classify_scanner_result(executed=False, returncode=None, payload="")
    assert result.passing is False
    assert result.status == "UNAVAILABLE"


def test_scanner_error_cannot_pass() -> None:
    result = classify_scanner_result(
        executed=True,
        returncode=2,
        payload=(FIXTURES / "error.json").read_text(encoding="utf-8"),
    )
    assert result.passing is False
    assert result.status == "ERROR"


def test_vulnerability_result_cannot_pass() -> None:
    result = classify_scanner_result(
        executed=True,
        returncode=1,
        payload=(FIXTURES / "vulnerability.json").read_text(encoding="utf-8"),
    )
    assert result.passing is False
    assert result.status == "VULNERABLE"


def test_zero_exit_malformed_output_cannot_pass() -> None:
    result = classify_scanner_result(executed=True, returncode=0, payload="not-json")
    assert result.passing is False
    assert result.status == "ERROR"


def test_zero_exit_payload_with_vulnerability_still_cannot_pass() -> None:
    payload = (FIXTURES / "vulnerability.json").read_text(encoding="utf-8")
    result = classify_scanner_result(executed=True, returncode=0, payload=payload)
    assert result.passing is False
    assert result.status == "VULNERABLE"
