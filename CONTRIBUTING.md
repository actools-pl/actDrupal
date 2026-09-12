# Contributing to actDrupal

This project is built as small, reviewed slices. Start with `AGENTS.md`, `coding/00_START_HERE_CODER_DOCUMENTATION.md`, the active architecture and the current task card. Use synthetic data only; do not place credentials or private diagnostics in source, issues, logs or prompts.

## Source-CI development environment

The reproducible source-CI target is **CPython 3.14.7 on Ubuntu 26.04 LTS x86_64**. The accepted local reference environment is Ubuntu Server 26.04.1 LTS; hosted source CI uses GitHub's `ubuntu-26.04` x64 runner label. This aligns source checks with architecture D01, but source CI alone does not qualify the installed host or full product stack.

Create an isolated environment with CPython 3.14.7, then install the reviewed hash lock:

```text
python -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements/ci.lock
python tools/check_source.py
```

On Windows, activate the environment using its `Scripts` directory; the final CI lock must be generated and qualified for the Ubuntu x86_64 source-test target, so use an equivalent Ubuntu/WSL environment for exact source-CI reproduction rather than weakening hashes.

Direct source inputs are in `requirements/ci.in`. CP-002 retains the five CP-001 source/test pins and adds exactly three runtime pins: `PyYAML==6.0.3`, `jsonschema==4.26.0`, and `rfc8785==0.1.4`. Generate `requirements/ci.lock` from those exact bytes only under the documented CPython 3.14.7 / Ubuntu Server 26.04.1 x86_64 contract with `pip==26.2.1` and `pip-tools==7.6.1`; do not hand-edit resolver hashes or reuse the CP-001 lock after changing direct inputs. See `docs/development/source-ci.md`.

## What the canonical check establishes

It verifies exact Python/tool/runtime versions, `pip check`, and hash-closed inputs; the complete fixed source-workflow shape; strict configuration/parser/default/JCS tests; unit and reason-bound controlled negative fixtures; the closed wheel inventory and exact runtime metadata; the actual installed `actools` launcher plus import origin and packaged schema resource; truthful version/help and fixed non-reflective exit-3 invocation errors; real-pipe output failure; and exact complete `pip-audit==2.10.1` dependency coverage. Required execution that is unavailable, incomplete or errors remains a failed check.

A passing source check is not a release, server, Drupal, backup/restore or production qualification. CP-002 contract validity also does not mark G03/G09 or any other product-wide gate PASS.

## Review and integration

Submit one coherent task candidate with its exact base, complete diff/tree, commands actually run and results. Independent review follows CPD-12. Fix material findings and rerun invalidated evidence. Publication, pull-request creation, merge and repository-setting changes require their own bounded human authority.
