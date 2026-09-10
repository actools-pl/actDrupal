# ADR-0001 — Minimal Python package and fail-closed source CI

Status: **changes requested; corrected local candidate requires focused CPD-12 re-review and E01 evidence closure**. Date UTC: 2026-09-10. Decision owner: human task owner MP Singh under the bounded CP-001 authorization.

## Context

CP-001 is the first implementation slice after BOOT-001. Architecture v1.5.1 §§7.3, 13.1–13.6 and 18.5 slice 1 require a clean development package, owned source checks and truthful version/help behavior without importing the historical implementation or implying later installer support.

Live activation used repository `actools-pl/actDrupal` at exact base `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2`, tree `e189ff949ba8ff79de2302d5e8150ef8838077e3`. At activation there was no `.github/workflows/` directory, no source workflow run/status context, and detailed branch-protection inspection remained unavailable to the connector (403) although `main` was observed protected.

The first independent review, `CP001-IR-40362742-v1`, reviewed candidate `4036274201658873f8324f06224adc8f6985eeff` and requested six corrections: scanner coverage/format binding, CLI error contract/safety, explicit-help broken-pipe handling, closed wheel inventory, installed launcher/import-origin verification and effective workflow verification. E01 also requires the declared Python/tool/lock/build/audit evidence before acceptance.

## Decision

- Distribution: `actools-drupal`; Python import package: `actools`; development version: `0.1.0.dev0`; runtime dependencies: zero; Python `>=3.14,<3.15`.
- Only `actools version [--format human|json]`, root/version help and fixed safe invalid-invocation diagnostics exist. Invalid invocation and output/report delivery failure use architecture §18.5 exit **3**. Rejected argument bytes are not reflected.
- All help/version output uses one controlled write+flush boundary so a closed pipe cannot produce false success or an interpreter-shutdown traceback.
- Source CI is the single exact workflow `.github/workflows/source-ci.yml`, limited to pull requests to `main` and pushes to `main`, `contents: read`, GitHub-hosted `ubuntu-26.04` x64, Python 3.14.7, immutable action pins and non-persisted checkout credentials. The `ubuntu-26.04` hosted label was public preview at this correction point; retain that as a CI evidence limitation rather than falling back to a different product OS. The checker accepts the complete approved shape, not substring presence.
- The package wheel is a closed owned shape: exactly `actools/__init__.py`, `actools/cli.py` and the expected distribution metadata/license files. Wheel metadata confirms distribution/version/Python range, zero runtime requirements, MIT license, exact console entry point, pure wheel tag and source-equivalent license bytes.
- Installed acceptance runs the actual absolute `actools` launcher in a fresh venv outside the source tree with Python import overrides removed, verifies import origin and installed metadata, and binds checks to the exact wheel digest.
- `pip-audit==2.10.1` JSON is bound to its pinned `v2.10.1` formatter envelope (`dependencies` and `fixes`). PASS requires exact complete package/version coverage of the lock, no skips/duplicates/extras/mismatches and explicit empty vulnerability lists. Any incomplete/unknown/unavailable/vulnerable state fails closed.
- Direct source tools remain setuptools 84.0.0, build 1.6.0, pytest 9.1.1, pip-audit 2.10.1 and pip 26.2.1. Lock generation remains pip-tools 7.6.1 under CPython 3.14.7. A branch-protection required-check change is not part of CP-001.

## Alternatives and reasons

| Alternative | Benefit | Cost/risk | Disposition |
|---|---|---|---|
| Import historical runtime | Faster apparent progress | Violates fresh rewrite boundary | Rejected |
| Use default argparse error behavior | Less code | Exit 2 conflicts with accepted contract and reflects attacker-controlled text | Rejected after review |
| Accept scanner exit 0 without coverage equality | Simple | Clean result could mean skipped/incomplete collection | Rejected after review |
| Permit any `actools/` or `.dist-info/` wheel member | Flexible | Cannot substantiate package-exclusion claims | Rejected after review |
| Validate workflow by required/forbidden substrings | Small checker | Misses effective permissions, triggers and failure suppression | Rejected after review |
| Test `python -m actools.cli` only | Simple | Can miss broken console entry point/source import substitution | Rejected after review |
| Floating action/dependency versions | Simple updates | Mutable CI input | Rejected |

## Consequences and evidence boundary

CP-002 remains blocked until CP-001 acceptance. The provisional JSON version payload is not the later full §18.5 result envelope; downstream compatibility transition belongs to the first consuming schema task.

The coordinator environment can run focused source tests on Python 3.13.5, but that is not E01. Before acceptance/publication, regenerate/compare the lock under CPython 3.14.7 + pip-tools 7.6.1, install it with hashes, confirm exact tool versions and consistency, run the corrected canonical checker including real pip-audit output and wheel/launcher checks, and preserve exact digests. The real GitHub-hosted workflow run requires a later separately authorised publication/PR step and is not implied here.

Task: `coding/tasks/CP-001.md`. Review route: CPD-12. G01/G09/G22 and UX anchors remain requirement references, not passed product gates.
