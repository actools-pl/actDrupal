# CP-001 source CI and development checks

## Supported check environment

The exact source-CI evidence environment is GitHub-hosted `ubuntu-24.04` x86_64 with CPython **3.14.7**. This is a source-check environment only; it does not change the later Ubuntu production target or qualify a host.

Install the reviewed hash lock and invoke the canonical checker:

```text
python -m pip install --require-hashes -r requirements/ci.lock
python tools/check_source.py
```

The workflow uses exactly the same checker. Its workflow name is `Source CI`; the job name is `source`. Neither name is configured as a branch-protection required check by CP-001.

## Inputs and lock discipline

`requirements/ci.in` pins direct inputs. `requirements/ci.lock` pins the resolved CI closure and SHA-256 wheel identities for the declared Linux/Python target. The build package itself has zero runtime dependencies.

Lock-generation contract: use CPython 3.14.7 and `pip-tools==7.6.1` in a disposable generation environment. Because the coordinator container for the initial candidate had no package-index network path, the candidate lock was assembled from reviewed package-index metadata and **must be regenerated/compared before remote publication**. A difference is a review input, not something to overwrite silently.

## Assertions made by `tools/check_source.py`

1. Exact Python and direct source-tool versions are present.
2. Every locked requirement is exact and has an allowed SHA-256; wheel-only policy is present.
3. The actual workflow has only bounded triggers, read-only repository permission, fixed runner/Python and immutable action pins; no secrets, OIDC, self-hosted runner or deployment/write permission is accepted.
4. Unit tests cover exact human/JSON version output, help, unsupported invocation, closed stdin, a secret canary and a bounded broken pipe.
5. Controlled failure fixtures really fail; the invalid-package fixture cannot build.
6. A wheel is built and its inventory excludes repository history, coding/reference material, tests, tools, fixtures, credentials and experimental seeds.
7. That exact wheel installs into a fresh virtual environment and version/help work from outside the source tree without legacy files.
8. `pip-audit` runs with strict/hash requirements and dependency resolution disabled. Only exit 0 plus valid vulnerability-free JSON is PASS. Unavailable execution, scanner error, malformed output or vulnerability evidence is non-PASS.

## Controlled negative fixtures

```text
python tests/fixtures/deliberate_failure.py
python -m build --wheel --no-isolation tests/fixtures/invalid_package
```

Both commands are expected to return nonzero. Scanner-policy negatives are data-only files under `tests/fixtures/scanner_policy/`; no exploit code is executed.

## Expected outcomes and limits

The canonical checker prints only `SOURCE-CI: PASS` on complete success and exits zero. Any required missing tool, wrong version, build failure, scanner failure or assertion failure exits nonzero and prints `SOURCE-CI: FAIL` with bounded diagnostic context.

A source-CI PASS does **not** establish Drupal installation, privileged execution, server hardening, firewall/SSH behavior, backups/restores, release signing or production admission. It does not mark full G01/G09/G22 or any other product-wide gate PASS.

## Current candidate evidence boundary

The initial coordinator container had Python 3.13.5 and no external package-index resolution. It can exercise source-level unit/static logic, but the exact CPython 3.14.7 build/install/audit path remains pending until run in the declared environment. Preserve that distinction in review and evidence records.
