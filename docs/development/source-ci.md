# CP-001 source CI and development checks

## Supported check environment

The source-check OS line is **Ubuntu 26.04 LTS x86_64** with CPython **3.14.7**, matching architecture D01. Local E01 qualification uses a clean Ubuntu Server **26.04.1 LTS** x86_64 host. Hosted source CI uses GitHub-hosted `ubuntu-26.04` x64; that hosted label is public preview at this correction point, so capture its actual runner image/version in the later CI evidence. Source-CI success does not by itself qualify host hardening or the complete installed product.

Install the reviewed hash lock and invoke the canonical checker:

```text
python -m pip install --require-hashes -r requirements/ci.lock
python tools/check_source.py
```

The workflow uses exactly the same checker. Its workflow name is `Source CI`; the job name is `source`. Neither name is configured as a branch-protection required check by CP-001.

## Inputs and lock discipline

`requirements/ci.in` pins direct inputs. `requirements/ci.lock` pins the resolved CI closure and SHA-256 wheel identities for the declared Linux/Python target. The build package itself has zero runtime dependencies.

Lock-generation contract: use CPython 3.14.7 and `pip-tools==7.6.1` in a disposable generation environment. The initial lock was assembled from reviewed package-index metadata because the coordinator container had no package-index network path. It therefore **must be regenerated and compared in the declared environment before remote publication**. Preserve the command, input/output digests and explanation of every semantic difference; do not silently overwrite the reviewed input.

## Assertions made by `tools/check_source.py`

1. Exact Python and direct source-tool versions are present.
2. Every locked requirement is exact and hashed, the direct input set is unchanged, and wheel-only policy is present.
3. The source workflow matches the complete approved CP-001 workflow shape: only pull requests to `main` and pushes to `main`, repository `contents: read`, GitHub-hosted `ubuntu-26.04`, CPython 3.14.7, immutable checkout/setup-python pins, non-persisted checkout credentials, the exact locked-install step and the canonical check step. Extra triggers, job-level authority, ignored failures, runner changes or extra execution are rejected.
4. Unit tests cover exact human/JSON version output and help, architecture exit code **3** for invalid invocation/report failures, bounded non-reflective error text, closed stdin, secret canaries, write/flush failures and real closed pipes in buffered and unbuffered Python.
5. Controlled failure fixtures must fail for their intended reason: the deliberate marker and the intentionally missing build backend are checked, so a missing test tool cannot masquerade as a successful negative test.
6. A wheel is built and must have the closed nine-member CP-001 inventory: the two owned runtime Python files plus only the expected `actools_drupal-0.1.0.dev0.dist-info` metadata/license files. Duplicate, malformed, traversal, nested test/Git/credential material and unrelated metadata roots are rejected. Distribution identity, Python range, zero runtime requirements, MIT license, console entry point, pure-wheel metadata and packaged license bytes are checked.
7. That exact wheel digest is bound to installed acceptance checks. The fresh environment is invoked through its absolute `actools` console launcher from outside the source tree with `PYTHONPATH`/`PYTHONHOME` overrides removed; an isolated import probe must resolve `actools` inside that environment and confirm distribution/version/zero-runtime-requirement metadata.
8. `pip-audit==2.10.1` runs with strict/hash requirements, `--no-deps` and `--disable-pip`. Its pinned JSON formatter contract is the object envelope `{"dependencies": [...], "fixes": [...]}`. PASS requires complete, duplicate-free, unskipped package/version coverage exactly matching every locked distribution, explicit empty vulnerability lists and no fixes. Empty/incomplete coverage, skipped or malformed records, mismatched versions, scanner error/unavailability or any vulnerability is non-PASS. The exact 2.10.1 formatter contract is bound to `pypa/pip-audit` tag `v2.10.1`, `pip_audit/_format/json.py`; real scanner output remains part of the E01 execution gate.

## Controlled negative fixtures

```text
python tests/fixtures/deliberate_failure.py
python -m build --wheel --no-isolation tests/fixtures/invalid_package
```

Both commands are expected to return nonzero **for the intended fixture reason**. Scanner-policy negatives are data-only files under `tests/fixtures/scanner_policy/`; no exploit code is executed.

## Expected outcomes and limits

On complete success the checker prints the exact built wheel SHA-256 followed by `SOURCE-CI: PASS` and exits zero. Any required missing/wrong tool, lock or workflow mismatch, build/install/inventory failure, scanner failure or assertion failure exits nonzero and prints `SOURCE-CI: FAIL` with bounded diagnostic context.

A source-CI PASS does **not** establish Drupal installation, privileged execution, server hardening, firewall/SSH behavior, backups/restores, release signing or production admission. It does not mark full G01/G09/G22 or any other product-wide gate PASS.

## Current correction evidence boundary

Independent review `CP001-IR-40362742-v1` returned **CHANGES REQUESTED** with F01-F06 and evidence gate E01 open. The corrections address scanner completeness/format binding, exit/error safety, help delivery failure, wheel shape, installed launcher/import isolation and exact workflow assurance. Focused correction tests may run on the available Python 3.13.5 and remain explicitly non-qualifying. CPython 3.14.7 lock regeneration/install, complete canonical build/install/audit, and the later separately authorised GitHub-hosted workflow run remain pending until actually executed.
