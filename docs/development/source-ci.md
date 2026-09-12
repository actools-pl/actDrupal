# Source CI and development checks

## Supported check environment

The source-check OS line is **Ubuntu 26.04 LTS x86_64** with CPython **3.14.7**, matching architecture D01. CP-001 local E01 qualification used clean Ubuntu Server **26.04.1 LTS** x86_64. Hosted Source CI remains the unchanged GitHub-hosted `ubuntu-26.04` x64 workflow. CP-002 does not broaden workflow triggers, permissions or runner authority.

Install the reviewed hash lock and invoke the canonical checker:

```text
python -m pip install --require-hashes -r requirements/ci.lock
python tools/check_source.py
```

The workflow name remains `Source CI` and job name `source`.

## Inputs and lock discipline

`requirements/ci.in` now pins eight direct inputs: the five CP-001 source/test tools plus the three CP-002 runtime dependencies:

```text
build==1.6.0
jsonschema==4.26.0
pip==26.2.1
pip-audit==2.10.1
pytest==9.1.1
PyYAML==6.0.3
rfc8785==0.1.4
setuptools==84.0.0
```

The final `requirements/ci.lock` is a resolver result, never a hand-written prediction. Generate it only with CPython 3.14.7, `pip==26.2.1` and `pip-tools==7.6.1` on the accepted Ubuntu Server 26.04.1 x86_64 reference, with pip configuration disabled, explicit PyPI index input, `--allow-unsafe`, `--generate-hashes`, backtracking resolution, no hash reuse and the wheel-only input policy. Record input and generated-lock SHA-256 values from actual bytes.

The accepted normalized generation command is:

```text
pip-compile --no-config --index-url=https://pypi.org/simple --no-emit-index-url --allow-unsafe --generate-hashes --resolver=backtracking --no-reuse-hashes --no-annotate --no-strip-extras --output-file=requirements/ci.lock requirements/ci.in
```

Set `CUSTOM_COMPILE_COMMAND` to that exact one-line command before invoking the same pinned pip-compile option set. This makes pip-tools' generated header record the truthful normalized command rather than reconstructing an incomplete or false command line. The canonical checker rejects any generated header that does not contain that exact command or that claims `--no-index`.

Run generation only from the disposable accepted environment after confirming `python --version`, `python -m pip --version`, and `pip-compile --version`; do not substitute a different platform or tool version merely to obtain a lock. The historical r2 coding delivery intentionally omitted the lock because its sandbox was not the accepted environment. A review candidate must contain the exact-environment generated lock and its local generation/install/test receipts; a source tree that already contains such a lock must not be described as if lock generation were still pending. Hosted Source CI remains unexecuted until publication is separately authorized.

## Canonical checker assertions

`tools/check_source.py` retains the CP-001 fail-closed workflow/scanner/CLI policy and evolves package truth for CP-002:

1. exact CPython 3.14.7 and all eight direct installed versions;
2. a hash-locked resolver closure whose direct pins exactly match `requirements/ci.in`, whose generated header records the exact normalized `CUSTOM_COMPILE_COMMAND` without `--no-index`, whose frozen dependency/hash body remains unchanged, plus a successful `python -m pip check`;
3. byte-for-byte unchanged Source CI workflow shape, including only PR/push to `main`, `contents: read`, immutable action pins, `persist-credentials: false`, Ubuntu 26.04 and Python 3.14.7;
4. the complete test suite, including strict parser/default/origin/JCS adversarial tests and all unchanged CP-001 CLI tests;
5. the two CP-001 controlled negative build fixtures, still reason-bound;
6. one closed **16-member** wheel: `actools/__init__.py`, `actools/cli.py`, four `actools.contracts` Python modules, three declared schema/default JSON resources, and the same seven distribution metadata/license members;
7. exact wheel metadata runtime requirements: `PyYAML==6.0.3`, `jsonschema==4.26.0`, `rfc8785==0.1.4`;
8. byte equality for packaged contract/schema resources and root license/notices;
9. an actual installed `actools` launcher in a fresh isolated virtual environment outside the source tree: that verifier environment first hash-installs the complete actual `requirements/ci.lock` and passes `pip check`, then installs only the already-built Actools wheel with `--no-index --no-deps`; the installed probe preserves CP-001 version/help/error behavior, proves the Draft 2020-12 schema resource is loadable, checks the exact three runtime versions, and requires each runtime distribution/module path to resolve inside that fresh verifier environment rather than from an outer/system site-packages location;
10. strict `pip-audit==2.10.1` complete, duplicate-free, unskipped package/version coverage exactly equal to the generated lock. Any scanner vulnerability, skip, malformed output, incomplete coverage or unavailability is non-PASS.

## Targeted CP-002 test command

After the real lock has been generated and installed in the accepted environment:

```text
python -m pytest -q \
  tests/test_configuration_contract.py \
  tests/test_jcs_conformance.py \
  tests/test_package_contents.py
```

Then run:

```text
python tools/check_source.py
```

A command printed in documentation is not evidence that it ran. Record actual environment, candidate identity, start/end time, exit and bounded output as PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE.

## JCS provenance receipt

The six compact vector pairs are pinned to `cyberphone/json-canonicalization@19d51d7fe467d4706a3ff08adf8a748f29fc21e0`. `tests/fixtures/jcs/cyberphone/PROVENANCE.md` records source paths, coder-stage local-byte SHA-256 values and Apache-2.0 notice. The Human-Git operator must independently recompute/confirm every file digest and the set digest before the final candidate is independently reviewed.

## Evidence boundary

Source-CI success does not establish Drupal installation, privileged execution, host hardening, firewall/SSH behavior, backup/restore, release signing or production admission. CP-002 is a pure data-contract slice and does not mark G03/G09 or any product-wide gate PASS by itself.
