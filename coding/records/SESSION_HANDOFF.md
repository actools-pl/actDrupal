# Session handoff

**Prepared:** 2026-09-10 after CPD-12 re-review and D01 platform reconciliation. **Subject:** CP-001 Ubuntu-26.04 source-CI alignment and bounded E01 preparation after `CP001-IR-1bdb6b09-v1`.

## Authoritative repository point

- Repository: `actools-pl/actDrupal`, ID `1361769952`.
- Final CP-001 pre-write GitHub readback: `main` = `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2`, tree `e189ff949ba8ff79de2302d5e8150ef8838077e3`, observed protected.
- Remote `task/CP-001` was absent at that readback.
- Retained BOOT branches remained `task/BOOT-001` = `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1` and `records/BOOT-001-closeout` = `8e378d88bf663a16c685f788bca0d26bb6483a51`.
- BOOT-000/BOOT-001 and the records-only closeout are complete. Do not replay them.

## CP-001 authority and state

MP Singh authorized activation and bounded **local** CP-001 implementation from that exact base using the Human Git route and local branch `task/CP-001`. The exact 27-path allowlist is in `coding/tasks/CP-001.md`. On 2026-09-10 he additionally authorized the intended E01 sequence on a disposable Ubuntu 26.04.1 test server: put the exact candidate there, regenerate/compare the lock, perform the hash-locked install and run the complete canonical checker/pip-audit evidence.

This bounded server authority is test-only. It does **not** permit push/remote-branch creation, PR creation/update, GitHub Actions publication/dispatch, merge/auto-merge, repository settings/protection/ruleset changes, retained branch deletion, Drupal deployment, production credentials, release publication/signing or allowlist expansion.

CPD-12 remains the independent review route: fresh Work / ChatGPT 6 Astra while available, approved fallback ordinary-chat 5.6 sol under the recorded workflow. Human integration authority remains separate.

Independent review `CP001-IR-40362742-v1` returned **CHANGES REQUESTED**. Correction candidate `1bdb6b09ddff16220dc5e414254788ba259e1d15` / tree `13e07bcc266d76adf218e2314853d67771b67b9d` then received `CP001-IR-1bdb6b09-v1`: F01-F06 source corrections verified, no new blocking code finding, E01 still open. The re-review inherited the candidate's Ubuntu-24.04 source-CI declaration; architecture D01 actually requires Ubuntu 26.04 LTS / current 26.04.1 media, so that declaration is now being aligned and must receive focused review.

## Candidate design boundary

- Development distribution `actools-drupal`, version `0.1.0.dev0`; Python package `actools`; zero runtime dependencies.
- Only `actools version [--format human|json]`, help and honest unsupported-command errors are implemented. No future operation stubs.
- Source CI path `.github/workflows/source-ci.yml`; PR-to-main and push-main only; `contents: read`; GitHub-hosted Ubuntu 26.04 x64 (public preview at correction time); CPython 3.14.7; immutable action SHAs; no release/deployment authority.
- Canonical check: `python tools/check_source.py` after installing `requirements/ci.lock` with hash checking.
- Exact tool and lock-generation contract are recorded in the task card, ADR and development guide.

## Evidence boundary and next action

The coordinator's isolated environment is Python 3.13.5 and currently has no package-index network path. The operator has prepared a disposable Ubuntu Server 26.04.1 LTS x86_64 host with uv-managed CPython 3.14.7 for the authorized E01 run. Until those commands are actually executed and captured, lock regeneration/install/build/audit remain pending. A required scanner error/unavailable result cannot be converted into PASS.

Pre-candidate results in that environment:

- `python -m pytest -q`: **22 passed**.
- `python coding/tools/validate_workflow.py`: **OK** (78 workflow-package files, 331 local links, 53 task records).
- Static `verify_lock()` and `verify_workflow()`: **PASS**.
- Exploratory wheel build/inventory with available Python 3.13.5/setuptools 82 and explicit `--ignore-requires-python`: **PASS**; wheel contains only `actools/` plus `.dist-info` metadata/licenses. This is not the exact supported build environment.
- Initial exploratory installed-wheel evidence from candidate 40362742 is invalidated for F02/F03/F05 and retained only as history. Corrected local source tests now require invalid invocation exit 3, non-reflective bounded diagnostics, real closed-pipe handling and installed console-launcher/import-origin checks.
- Canonical `python tools/check_source.py`: **FAIL as required** at the exact-Python gate (`3.14.7` required; `3.13.5` running).
- Isolated `pip install --require-hashes -r requirements/ci.lock`: **nonzero** because package-index artifacts were unavailable in the container; no dependency/audit PASS is claimed.


The exact delivered local candidate SHA/tree/parent, complete diff/file manifest and actual test receipt are preserved outside the candidate itself to avoid recursive self-reference; send that exact candidate plus surrounding interfaces to the CPD-12 independent reviewer. Do not publish remotely until a later bounded human decision after review and exact live-base/control refresh.

## Correction status after CP001-IR-40362742-v1

- Corrections remain within the original 27-path allowlist; `REVIEW_LOG.csv` and `TEST_EVIDENCE_INDEX.csv` are intentionally untouched.
- Focused corrected tests on the available Python 3.13.5: **66 passed** (26 CLI; 40 scanner/package/workflow). These are not E01 qualification.
- Corrected exploratory wheel build succeeded with `--ignore-requires-python` and produced only the nine approved members. The strengthened inventory check then correctly refused qualification because the available setuptools is not 84.0.0.
- Corrected exploratory wheel installation used the actual `actools` console launcher outside the source tree; version/JSON/help and exit-3 invalid invocation behaved as intended, and an isolated import probe resolved `actools` inside the fresh venv even when a source-tree `PYTHONPATH` was supplied. This remains Python-3.13 exploratory evidence.
- Exact CPython 3.14.7 + pip-tools 7.6.1 lock regeneration/compare, hash-locked install, exact tool versions, complete `python tools/check_source.py` and real pip-audit 2.10.1 output are authorized on the disposable Ubuntu 26.04.1 E01 host but remain pending actual execution. GitHub-hosted `ubuntu-26.04` source CI remains later and requires separate publication/PR authority; the hosted runner label is public preview at this correction point.
- Produce a new local correction candidate, cumulative diff/manifest, finding-by-finding disposition and retest receipt; then use CPD-12 focused re-review. CP-002 stays planned/inactive.
