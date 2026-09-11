from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

import pytest

from tools.check_source import (
    CONTRACT_FILES,
    LOCK,
    CheckFailure,
    DIST_INFO,
    EXPECTED_RUNTIME_REQUIREMENTS,
    EXPECTED_WHEEL_MEMBERS,
    EXPECTED_WORKFLOW,
    _create_isolated_installed_env,
    requirement_records,
    verify_wheel_inventory,
    verify_workflow_text,
)

ROOT = Path(__file__).resolve().parents[1]


def test_project_declares_exact_runtime_dependencies() -> None:
    import tomllib

    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert data["project"]["dependencies"] == [
        "PyYAML==6.0.3",
        "jsonschema==4.26.0",
        "rfc8785==0.1.4",
    ]
    assert data["project"]["requires-python"] == ">=3.14,<3.15"
    assert data["project"]["scripts"] == {"actools": "actools.cli:main"}
    assert data["tool"]["setuptools"]["package-data"] == {
        "actools.contracts": ["schemas/*.json"]
    }


def test_source_inputs_include_exact_runtime_and_ci_pins() -> None:
    records = requirement_records(
        (ROOT / "requirements" / "ci.in").read_text(encoding="utf-8")
    )
    assert records[0] == "--only-binary=:all:"
    assert set(records[1:]) == {
        "build==1.6.0",
        "pip==26.2.1",
        "pip-audit==2.10.1",
        "pytest==9.1.1",
        "setuptools==84.0.0",
        "PyYAML==6.0.3",
        "jsonschema==4.26.0",
        "rfc8785==0.1.4",
    }


def test_lock_records_are_pinned_and_hashed() -> None:
    records = requirement_records(
        (ROOT / "requirements" / "ci.lock").read_text(encoding="utf-8")
    )
    assert records[0] == "--only-binary :all:"
    packages = [record for record in records[1:] if not record.startswith("--")]
    assert packages
    assert all("==" in record and "--hash=sha256:" in record for record in packages)


def _valid_members() -> dict[str, bytes | str]:
    schema_dir = ROOT / "src/actools/contracts/schemas"
    metadata = (
        "Metadata-Version: 2.4\n"
        "Name: actools-drupal\n"
        "Version: 0.1.0.dev0\n"
        "License-Expression: MIT\n"
        "Requires-Python: >=3.14,<3.15\n"
        "Requires-Dist: PyYAML==6.0.3\n"
        "Requires-Dist: jsonschema==4.26.0\n"
        "Requires-Dist: rfc8785==0.1.4\n\n"
    )
    members: dict[str, bytes | str] = {
        "actools/__init__.py": "__version__ = '0.1.0.dev0'\n",
        "actools/cli.py": "def main(): return 0\n",
        "actools/contracts/schemas/common-1.0.0.schema.json": (
            schema_dir / "common-1.0.0.schema.json"
        ).read_bytes(),
        "actools/contracts/schemas/configuration-1.0.0.schema.json": (
            schema_dir / "configuration-1.0.0.schema.json"
        ).read_bytes(),
        "actools/contracts/schemas/configuration-defaults-1.0.0.json": (
            schema_dir / "configuration-defaults-1.0.0.json"
        ).read_bytes(),
        f"{DIST_INFO}/licenses/LICENSE": (ROOT / "LICENSE").read_bytes(),
        f"{DIST_INFO}/licenses/NOTICE.md": (ROOT / "NOTICE.md").read_bytes(),
        f"{DIST_INFO}/METADATA": metadata,
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
    for member in CONTRACT_FILES:
        members[member] = (ROOT / "src" / member).read_bytes()
    return members


def _wheel(
    tmp_path: Path,
    members: dict[str, bytes | str],
    *,
    duplicate: str | None = None,
) -> Path:
    path = tmp_path / "synthetic.whl"
    with zipfile.ZipFile(path, "w") as archive:
        for name, value in members.items():
            archive.writestr(name, value)
        if duplicate is not None:
            archive.writestr(duplicate, "duplicate")
    return path


def test_expected_wheel_shape_is_closed_and_contains_contract_resources() -> None:
    assert len(EXPECTED_WHEEL_MEMBERS) == 16
    assert EXPECTED_RUNTIME_REQUIREMENTS == {
        "pyyaml": "6.0.3",
        "jsonschema": "4.26.0",
        "rfc8785": "0.1.4",
    }
    assert {
        "actools/contracts/schemas/common-1.0.0.schema.json",
        "actools/contracts/schemas/configuration-1.0.0.schema.json",
        "actools/contracts/schemas/configuration-defaults-1.0.0.json",
    } <= EXPECTED_WHEEL_MEMBERS


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
        "actools/contracts/schemas/unowned.json",
        "unowned.dist-info/payload.py",
        "../outside",
        "/absolute/path",
    ],
)
def test_wheel_inventory_rejects_any_extra_or_unsafe_member(
    tmp_path: Path, forbidden: str
) -> None:
    members = _valid_members()
    members[forbidden] = "x"
    wheel = _wheel(tmp_path, members)
    with pytest.raises(CheckFailure):
        verify_wheel_inventory(wheel)


def test_wheel_inventory_rejects_duplicate_member(tmp_path: Path) -> None:
    wheel = _wheel(tmp_path, _valid_members(), duplicate="actools/cli.py")
    with pytest.raises(CheckFailure):
        verify_wheel_inventory(wheel)


def test_wheel_inventory_rejects_unowned_runtime_dependency(tmp_path: Path) -> None:
    members = _valid_members()
    members[f"{DIST_INFO}/METADATA"] = (
        "Metadata-Version: 2.4\n"
        "Name: actools-drupal\n"
        "Version: 0.1.0.dev0\n"
        "License-Expression: MIT\n"
        "Requires-Python: >=3.14,<3.15\n"
        "Requires-Dist: PyYAML==6.0.3\n"
        "Requires-Dist: jsonschema==4.26.0\n"
        "Requires-Dist: rfc8785==0.1.4\n"
        "Requires-Dist: requests==2.34.2\n\n"
    )
    with pytest.raises(CheckFailure):
        verify_wheel_inventory(_wheel(tmp_path, members))


def test_exact_approved_workflow_passes() -> None:
    verify_workflow_text(EXPECTED_WORKFLOW)


@pytest.mark.parametrize(
    "mutated",
    [
        EXPECTED_WORKFLOW.replace(
            "    name: source\n",
            "    name: source\n    permissions: write-all\n",
            1,
        ),
        EXPECTED_WORKFLOW.replace(
            "    runs-on: ubuntu-26.04\n",
            "    continue-on-error: true\n    runs-on: ubuntu-26.04\n",
            1,
        ),
        EXPECTED_WORKFLOW.replace(
            "    branches: [main]\n\npermissions:",
            '    branches: [main]\n    tags: ["*"]\n\npermissions:',
            1,
        ),
        EXPECTED_WORKFLOW.replace("runs-on: ubuntu-26.04", "runs-on: self-hosted"),
        EXPECTED_WORKFLOW.replace("persist-credentials: false", "persist-credentials: true"),
        EXPECTED_WORKFLOW.replace(
            "actions/checkout@",
            "actions/checkout@0000000000000000000000000000000000000000 # replaced\n        # original ",
        ),
        EXPECTED_WORKFLOW.replace(
            "python tools/check_source.py", "python tools/check_source.py || true"
        ),
        EXPECTED_WORKFLOW + "\n# unexpected extra content\n",
    ],
)
def test_workflow_rejects_any_effective_or_unexpected_change(mutated: str) -> None:
    with pytest.raises(CheckFailure):
        verify_workflow_text(mutated)


def test_contract_runtime_import_surface_is_declared() -> None:
    import ast
    import sys

    external: set[str] = set()
    for relative in (
        "src/actools/contracts/__init__.py",
        "src/actools/contracts/canonical.py",
        "src/actools/contracts/configuration.py",
        "src/actools/contracts/errors.py",
    ):
        tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in sys.stdlib_module_names:
                        external.add(top)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                top = node.module.split(".")[0]
                if top not in sys.stdlib_module_names:
                    external.add(top)
    assert external == {"yaml", "jsonschema", "rfc8785"}


def test_installed_verifier_uses_fresh_hash_locked_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Regression for CP002-F01: never inherit dependency copies from system site."""
    import tools.check_source as source_check

    builder_kwargs: dict[str, object] = {}
    commands: list[list[str]] = []

    class RecordingBuilder:
        def __init__(self, **kwargs: object) -> None:
            builder_kwargs.update(kwargs)

        def create(self, target: Path) -> None:
            scripts = target / ("Scripts" if source_check.os.name == "nt" else "bin")
            scripts.mkdir(parents=True)

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(source_check.venv, "EnvBuilder", RecordingBuilder)
    monkeypatch.setattr(source_check, "run", fake_run)

    env_dir, python, launcher, env = _create_isolated_installed_env(tmp_path)

    assert builder_kwargs == {"with_pip": True, "clear": True}
    assert "system_site_packages" not in builder_kwargs
    assert env_dir == tmp_path / "installed"
    assert launcher.parent == python.parent
    assert commands == [
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--require-hashes",
            "-r",
            str(LOCK),
        ],
        [str(python), "-m", "pip", "check"],
    ]
    assert env["PYTHONNOUSERSITE"] == "1"
    assert "PYTHONPATH" not in env
    assert "PYTHONHOME" not in env
    assert "VIRTUAL_ENV" not in env
