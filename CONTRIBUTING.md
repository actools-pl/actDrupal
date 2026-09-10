# Contributing to actDrupal

This project is built as small, reviewed slices. Start with `AGENTS.md`, `coding/00_START_HERE_CODER_DOCUMENTATION.md`, the active architecture and the current task card. Use synthetic data only; do not place credentials or private diagnostics in source, issues, logs or prompts.

## CP-001 development environment

The reproducible source-CI target is **CPython 3.14.7 on Ubuntu 26.04 LTS x86_64**. Local E01 qualification uses Ubuntu Server 26.04.1 LTS; hosted source CI uses GitHub's `ubuntu-26.04` x64 runner label. This aligns source checks with architecture D01, but source CI alone does not qualify the installed host or full product stack.

Create an isolated environment with CPython 3.14.7, then install the hash-locked source tools:

```text
python -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements/ci.lock
python tools/check_source.py
```

On Windows, activate the environment using its `Scripts` directory; the current CI lock is deliberately bound to the Ubuntu x86_64 runner, so use an equivalent Ubuntu/WSL environment for exact source-CI reproduction rather than weakening hashes.

Direct source inputs are in `requirements/ci.in`. The committed lock was generated from those exact bytes with CPython 3.14.7, pip 26.2.1 and `pip-tools==7.6.1` on the Ubuntu 26.04.1 x86_64 E01 host. Regenerate and compare under that contract before changing any pinned dependency. The lock header records the truthful generation command; the external E01 receipt binds the OS/interpreter/tool versions, input/output digests and semantic comparison.

## What the canonical check establishes

It verifies exact Python/tool versions and hash-closed inputs; the complete fixed source-workflow shape; unit and reason-bound controlled negative fixtures; a closed wheel inventory and metadata; the actual installed `actools` launcher plus import origin; truthful version/help and fixed non-reflective exit-3 invocation errors; real-pipe output failure; and exact complete `pip-audit==2.10.1` dependency coverage. Required execution that is unavailable, incomplete or errors remains a failed check.

A passing source check is not a release, server, Drupal, backup/restore or production qualification. Do not mark G01/G09/G22 or other product-wide gates PASS from CP-001 source fixtures.

## Review and integration

Submit one coherent task candidate with its exact base, complete diff/tree, commands actually run and results. Independent review follows CPD-12. Fix material findings and rerun invalidated evidence. Publication, pull-request creation, merge and repository-setting changes require their own bounded human authority.
