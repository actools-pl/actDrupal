from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from tools.check_source import (
    CheckFailure,
    DIST_INFO,
    EXPECTED_WORKFLOW,
    requirement_records,
    verify_wheel_inventory,
    verify_workflow_text,
)

ROOT = Path(__file__).resolve().parents[1]


def test_project_declares_zero_runtime_dependencies() -> None:
    import tomllib

    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["dependencies"] == []
    assert data["project"]["requires-python"] == ">=3.14,<3.15"
    assert data["project"]["scripts"] == {"actools": "actools.cli:main"}


def test_lock_records_are_pinned_and_hashed() -> None:
    records = requirement_records((ROOT / "requirements" / "ci.lock").read_text(encoding="utf-8"))
    assert records[0] == "--only-binary=:all:"
    packages = [record for record in records[1:] if not record.startswith("--")]
    assert packages
    assert all("==" in record and "--hash=sha256:" in record for record in packages)


def _valid_members() -> dict[str, bytes | str]:
    return {
        "actools/__init__.py": "__version__ = '0.1.0.dev0'\n",
        "actools/cli.py": "def main(): return 0\n",
        f"{DIST_INFO}/licenses/LICENSE": (ROOT / "LICENSE").read_bytes(),
        f"{DIST_INFO}/licenses/NOTICE.md": (ROOT / "NOTICE.md").read_bytes(),
        f"{DIST_INFO}/METADATA": (
            "Metadata-Version: 2.4\n"
            "Name: actools-drupal\n"
            "Version: 0.1.0.dev0\n"
            "License-Expression: MIT\n"
            "Requires-Python: >=3.14,<3.15\n\n"
        ),
        f"{DIST_INFO}/WHEEL": (
            "Wheel-Version: 1.0\n"
            "Generator: setuptools (84.0.0)\n"
            "Root-Is-Purelib: true\n"
            "Tag: py3-none-any\n\n"
        ),
        f"{DIST_INFO}/entry_points.txt": "[console_scripts]\nactools = actools.cli:main\n",
        f"{DIST_INFO}/top_level.txt": "actools\n",
        f"{DIST_INFO}/RECORD": "placeholder\n",
    }


def _wheel(tmp_path: Path, members: dict[str, bytes | str], *, duplicate: str | None = None) -> Path:
    path = tmp_path / "synthetic.whl"
    with zipfile.ZipFile(path, "w") as archive:
        for name, value in members.items():
            archive.writestr(name, value)
        if duplicate is not None:
            archive.writestr(duplicate, "duplicate")
    return path


def test_wheel_inventory_accepts_only_complete_owned_shape(tmp_path: Path) -> None:
    wheel = _wheel(tmp_path, _valid_members())
    digest = verify_wheel_inventory(wheel)
    assert len(digest) == 64


@pytest.mark.parametrize(
    "forbidden",
    [
        "tests/test_cli.py",
        "coding/README.md",
        ".git/config",
        "tools/check_source.py",
        "actools/.git/config",
        "actools/tests/fixture.py",
        "actools/credentials/key.pem",
        "unowned.dist-info/payload.py",
        "../outside",
        "/absolute/path",
    ],
)
def test_wheel_inventory_rejects_any_extra_or_unsafe_member(tmp_path: Path, forbidden: str) -> None:
    members = _valid_members()
    members[forbidden] = "x"
    wheel = _wheel(tmp_path, members)
    with pytest.raises(CheckFailure):
        verify_wheel_inventory(wheel)


def test_wheel_inventory_rejects_duplicate_member(tmp_path: Path) -> None:
    members = _valid_members()
    wheel = _wheel(tmp_path, members, duplicate="actools/cli.py")
    with pytest.raises(CheckFailure):
        verify_wheel_inventory(wheel)


def test_wheel_inventory_rejects_unowned_metadata_or_runtime_dependency(tmp_path: Path) -> None:
    members = _valid_members()
    members[f"{DIST_INFO}/METADATA"] = (
        "Metadata-Version: 2.4\n"
        "Name: actools-drupal\n"
        "Version: 0.1.0.dev0\n"
        "License-Expression: MIT\n"
        "Requires-Python: >=3.14,<3.15\n"
        "Requires-Dist: requests\n\n"
    )
    wheel = _wheel(tmp_path, members)
    with pytest.raises(CheckFailure):
        verify_wheel_inventory(wheel)


def test_exact_approved_workflow_passes() -> None:
    verify_workflow_text(EXPECTED_WORKFLOW)


@pytest.mark.parametrize(
    "mutated",
    [
        EXPECTED_WORKFLOW.replace("    name: source\n", "    name: source\n    permissions: write-all\n", 1),
        EXPECTED_WORKFLOW.replace("    runs-on: ubuntu-26.04\n", "    continue-on-error: true\n    runs-on: ubuntu-26.04\n", 1),
        EXPECTED_WORKFLOW.replace("    branches: [main]\n\npermissions:", '    branches: [main]\n    tags: ["*"]\n\npermissions:', 1),
        EXPECTED_WORKFLOW.replace("runs-on: ubuntu-26.04", "runs-on: self-hosted"),
        EXPECTED_WORKFLOW.replace("persist-credentials: false", "persist-credentials: true"),
        EXPECTED_WORKFLOW.replace("actions/checkout@", "actions/checkout@0000000000000000000000000000000000000000 # replaced\n        # original "),
        EXPECTED_WORKFLOW.replace("python tools/check_source.py", "python tools/check_source.py || true"),
        EXPECTED_WORKFLOW + "\n# unexpected extra content\n",
    ],
)
def test_workflow_rejects_any_effective_or_unexpected_change(mutated: str) -> None:
    with pytest.raises(CheckFailure):
        verify_workflow_text(mutated)
