from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from tools.check_source import CheckFailure, requirement_records, verify_wheel_inventory

ROOT = Path(__file__).resolve().parents[1]


def test_project_declares_zero_runtime_dependencies() -> None:
    import tomllib

    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["dependencies"] == []
    assert data["project"]["requires-python"] == ">=3.14,<3.15"


def test_lock_records_are_pinned_and_hashed() -> None:
    records = requirement_records((ROOT / "requirements" / "ci.lock").read_text(encoding="utf-8"))
    assert records[0] == "--only-binary=:all:"
    packages = [record for record in records[1:] if not record.startswith("--")]
    assert packages
    assert all("==" in record and "--hash=sha256:" in record for record in packages)


def _wheel(tmp_path: Path, names: list[str]) -> Path:
    path = tmp_path / "synthetic.whl"
    with zipfile.ZipFile(path, "w") as archive:
        for name in names:
            archive.writestr(name, "x")
    return path


def test_wheel_inventory_accepts_minimal_owned_shape(tmp_path: Path) -> None:
    wheel = _wheel(
        tmp_path,
        [
            "actools/__init__.py",
            "actools/cli.py",
            "actools_drupal-0.1.0.dev0.dist-info/METADATA",
            "actools_drupal-0.1.0.dev0.dist-info/RECORD",
        ],
    )
    verify_wheel_inventory(wheel)


@pytest.mark.parametrize("forbidden", ["tests/test_cli.py", "coding/README.md", ".git/config", "tools/check_source.py"])
def test_wheel_inventory_rejects_nonruntime_material(tmp_path: Path, forbidden: str) -> None:
    wheel = _wheel(
        tmp_path,
        [
            "actools/__init__.py",
            "actools/cli.py",
            "actools_drupal-0.1.0.dev0.dist-info/METADATA",
            forbidden,
        ],
    )
    with pytest.raises(CheckFailure):
        verify_wheel_inventory(wheel)
