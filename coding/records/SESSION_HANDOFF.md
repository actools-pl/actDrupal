# Session handoff

**Prepared:** 2026-09-10T08:16:34Z. **Subject:** CP-001 bounded local candidate preparation after completed BOOT-001 closeout.

## Authoritative repository point

- Repository: `actools-pl/actDrupal`, ID `1361769952`.
- Final CP-001 pre-write GitHub readback: `main` = `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2`, tree `e189ff949ba8ff79de2302d5e8150ef8838077e3`, observed protected.
- Remote `task/CP-001` was absent at that readback.
- Retained BOOT branches remained `task/BOOT-001` = `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1` and `records/BOOT-001-closeout` = `8e378d88bf663a16c685f788bca0d26bb6483a51`.
- BOOT-000/BOOT-001 and the records-only closeout are complete. Do not replay them.

## CP-001 authority and state

MP Singh authorized activation and bounded **local** CP-001 implementation from that exact base using the Human Git route and local branch `task/CP-001`. The exact 27-path allowlist is in `coding/tasks/CP-001.md`. The authorization permits isolated local dependency/test work and local candidate commits only.

It does **not** permit push/remote-branch creation, PR creation/update, GitHub Actions publication/dispatch, merge/auto-merge, repository settings/protection/ruleset changes, retained branch deletion, server use, Drupal deployment, production credentials, release publication/signing or allowlist expansion.

CPD-12 remains the independent review route: fresh Work / ChatGPT 6 Astra while available, approved fallback ordinary-chat 5.6 sol under the recorded workflow. Human integration authority remains separate.

## Candidate design boundary

- Development distribution `actools-drupal`, version `0.1.0.dev0`; Python package `actools`; zero runtime dependencies.
- Only `actools version [--format human|json]`, help and honest unsupported-command errors are implemented. No future operation stubs.
- Source CI path `.github/workflows/source-ci.yml`; PR-to-main and push-main only; `contents: read`; GitHub-hosted Ubuntu 24.04; CPython 3.14.7; immutable action SHAs; no release/deployment authority.
- Canonical check: `python tools/check_source.py` after installing `requirements/ci.lock` with hash checking.
- Exact tool and lock-generation contract are recorded in the task card, ADR and development guide.

## Evidence boundary and next action

The coordinator's isolated environment is Python 3.13.5 and currently has no package-index network path. Source-level checks may be executed there and reported as such, but exact CPython 3.14.7 install/build/audit and pip-tools lock regeneration must remain pending until actually executed. A required scanner error/unavailable result cannot be converted into PASS.

Pre-candidate results in that environment:

- `python -m pytest -q`: **22 passed**.
- `python coding/tools/validate_workflow.py`: **OK** (78 workflow-package files, 331 local links, 53 task records).
- Static `verify_lock()` and `verify_workflow()`: **PASS**.
- Exploratory wheel build/inventory with available Python 3.13.5/setuptools 82 and explicit `--ignore-requires-python`: **PASS**; wheel contains only `actools/` plus `.dist-info` metadata/licenses. This is not the exact supported build environment.
- Installed exploratory wheel from outside the source tree: human version and JSON exact; help exposes only `version`; unsupported `install` exits 2.
- Canonical `python tools/check_source.py`: **FAIL as required** at the exact-Python gate (`3.14.7` required; `3.13.5` running).
- Isolated `pip install --require-hashes -r requirements/ci.lock`: **nonzero** because package-index artifacts were unavailable in the container; no dependency/audit PASS is claimed.


The exact delivered local candidate SHA/tree/parent, complete diff/file manifest and actual test receipt are preserved outside the candidate itself to avoid recursive self-reference; send that exact candidate plus surrounding interfaces to the CPD-12 independent reviewer. Do not publish remotely until a later bounded human decision after review and exact live-base/control refresh.
