from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.check_source import classify_scanner_result, locked_packages

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "scanner_policy"


def _clean_payload(expected: dict[str, str] | None = None) -> str:
    packages = expected or locked_packages()
    return json.dumps(
        {
            "dependencies": [
                {"name": name, "version": version, "vulns": []}
                for name, version in sorted(packages.items())
            ],
            "fixes": [],
        }
    )


def classify(payload: str, *, returncode: int = 0, executed: bool = True):
    return classify_scanner_result(
        executed=executed,
        returncode=returncode,
        payload=payload,
        expected_packages=locked_packages(),
    )


def test_complete_clean_pinned_format_is_the_only_pass() -> None:
    result = classify(_clean_payload())
    assert result.passing is True
    assert result.status == "PASS"
    assert "locked distributions" in result.detail


def test_legacy_list_shape_and_empty_coverage_cannot_pass() -> None:
    for payload in ("[]", '{"dependencies":[],"fixes":[]}'):
        result = classify(payload)
        assert result.passing is False
        assert result.status == "ERROR"


@pytest.mark.parametrize(
    "record",
    [
        {},
        {"name": "pip", "version": "26.2.1"},
        {"name": "pip", "skip_reason": "collection failed"},
        {"name": "", "version": "26.2.1", "vulns": []},
        {"name": "pip", "version": "", "vulns": []},
        {"name": "pip", "version": "26.2.1", "vulns": None},
        {"name": "pip", "version": "26.2.1", "vulns": [], "extra": True},
    ],
)
def test_incomplete_skipped_or_unknown_dependency_shape_cannot_pass(record: dict[str, object]) -> None:
    payload = json.dumps({"dependencies": [record], "fixes": []})
    result = classify(payload)
    assert result.passing is False
    assert result.status == "ERROR"


def test_missing_duplicate_unexpected_and_mismatched_coverage_cannot_pass() -> None:
    expected = locked_packages()
    dependencies = [
        {"name": name, "version": version, "vulns": []}
        for name, version in sorted(expected.items())
    ]

    variants: list[list[dict[str, object]]] = []
    variants.append(dependencies[:-1])
    variants.append(dependencies + [dict(dependencies[0])])
    variants.append(dependencies + [{"name": "unexpected-package", "version": "1", "vulns": []}])
    mismatch = [dict(item) for item in dependencies]
    mismatch[0]["version"] = "999"
    variants.append(mismatch)

    for records in variants:
        result = classify(json.dumps({"dependencies": records, "fixes": []}))
        assert result.passing is False
        assert result.status == "ERROR"


def test_fixes_or_unknown_top_level_fields_cannot_pass() -> None:
    expected = locked_packages()
    base = json.loads(_clean_payload(expected))
    with_fix = dict(base)
    with_fix["fixes"] = [{"name": "x", "old_version": "1", "new_version": "2"}]
    extra = dict(base)
    extra["extra"] = []
    for payload in (json.dumps(with_fix), json.dumps(extra)):
        result = classify(payload)
        assert result.passing is False
        assert result.status == "ERROR"


def test_unavailable_scan_cannot_pass() -> None:
    result = classify_scanner_result(
        executed=False,
        returncode=None,
        payload="",
        expected_packages=locked_packages(),
    )
    assert result.passing is False
    assert result.status == "UNAVAILABLE"


def test_scanner_error_cannot_pass() -> None:
    result = classify((FIXTURES / "error.json").read_text(encoding="utf-8"), returncode=2)
    assert result.passing is False
    assert result.status == "ERROR"


def test_vulnerability_exit_cannot_pass() -> None:
    result = classify((FIXTURES / "vulnerability.json").read_text(encoding="utf-8"), returncode=1)
    assert result.passing is False
    assert result.status == "VULNERABLE"


def test_zero_exit_malformed_output_cannot_pass() -> None:
    result = classify("not-json")
    assert result.passing is False
    assert result.status == "ERROR"


def test_zero_exit_payload_with_vulnerability_still_cannot_pass() -> None:
    expected = locked_packages()
    records = [
        {"name": name, "version": version, "vulns": []}
        for name, version in sorted(expected.items())
    ]
    records[0]["vulns"] = [{"id": "CVE-SYNTHETIC", "fix_versions": ["999"]}]
    result = classify(json.dumps({"dependencies": records, "fixes": []}))
    assert result.passing is False
    assert result.status == "VULNERABLE"
