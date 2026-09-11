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

`requirements/ci.in` pins the five direct inputs. `requirements/ci.lock` is now the resolver-generated CI closure: 34 distributions with SHA-256 hashes emitted by `pip-compile` under CPython 3.14.7 on Ubuntu Server 26.04.1 LTS x86_64. The lock may carry hashes for published wheel candidates across platforms; the later hash-enforced installation receipt records which compatible artifacts are actually selected on the declared target. The build package itself has zero runtime dependencies.

Lock-generation contract: use CPython 3.14.7, `pip==26.2.1` and `pip-tools==7.6.1` in a disposable generation environment with pip configuration disabled, explicit PyPI index input, `--allow-unsafe`, `--generate-hashes`, backtracking resolver, no hash reuse, and wheel-only input policy. E01 Phase 1C generated the committed lock from unchanged `requirements/ci.in` (SHA-256 `615a1f8c33300e7b47c366916c89738bd572b37b8124e98064efe1fca27f86f8`). Generated lock SHA-256 is `6836c3ed72a3667e97b6901f9836f6c0957dd3512911b221986bc7c1b223e7e7`. Relative to the prior handwritten 35-distribution lock, the resolver produced 34 distributions: `typing-extensions` is absent, `boolean.py` is canonically emitted as `boolean-py`, and transitive pins move to `cachecontrol==0.14.4`, `msgpack==1.2.2` and `pip-api==0.0.35`. Phase 1B and 1C dependency bodies were byte-identical; Phase 1C corrected only pip-tools' displayed command header. Hash-enforced installation and full canonical execution remain separate E01 evidence and must run on the exact candidate containing this lock.

## Assertions made by `tools/check_source.py`

1. Exact Python and direct source-tool versions are present.
2. Every locked requirement is exact and hashed, the direct input set is unchanged, and the lock contains exactly pip-tools' canonical `--only-binary :all:` directive while the source input retains its equivalent `--only-binary=:all:` form.
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

Independent review `CP001-IR-40362742-v1` returned **CHANGES REQUESTED** with F01-F06 and evidence gate E01 open. The corrections address scanner completeness/format binding, exit/error safety, help delivery failure, wheel shape, installed launcher/import isolation and exact workflow assurance. Focused correction tests may run on the available Python 3.13.5 and remain explicitly non-qualifying. CPython 3.14.7 resolver-backed lock generation is now evidenced by E01 Phase 1C; hash-locked installation, complete canonical build/install/audit, and the later separately authorised GitHub-hosted workflow run remain pending until actually executed.
