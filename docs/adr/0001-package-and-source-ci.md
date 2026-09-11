# ADR-0001 — Minimal Python package and fail-closed source CI

Status: **accepted and integrated for the bounded CP-001 source slice; F01-F06 and E01 are closed, post-merge Source CI passed, and `CP001-IR-58cfa0d-post-merge-v1` accepts the integration. PM-R01 is a records/documentation chronology closeout pending focused review.** Date UTC: 2026-09-11. Decision owner: human task owner MP Singh under the bounded CP-001 authorization.

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
- Direct source tools remain setuptools 84.0.0, build 1.6.0, pytest 9.1.1, pip-audit 2.10.1 and pip 26.2.1. Lock generation uses pip-tools 7.6.1 under CPython 3.14.7 on Ubuntu 26.04.1 x86_64. E01 Phase 1C generated the committed 34-distribution lock from the unchanged direct-input file with clean pip configuration and explicit PyPI resolution; the generated lock SHA-256 is `6836c3ed72a3667e97b6901f9836f6c0957dd3512911b221986bc7c1b223e7e7`. A branch-protection required-check change is not part of CP-001.

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

The provisional JSON version payload is not the later full §18.5 result envelope; downstream compatibility transition belongs to the first consuming schema task.

The exact local E01 sequence completed on Ubuntu Server 26.04.1 LTS x86_64 / CPython 3.14.7: resolver-backed lock reproduction, hash-enforced installation, exact tool/dependency checks, genuine pip-audit coverage, real wheel/launcher/import checks, negative fixtures and the canonical checker. `CP001-IR-2aafec4-local-receipts-v1` accepted Local E01. The GitHub-hosted PR run `34569300056` then passed on the reviewed PR subject and `CP001-IR-2aafec4-E01H-v1` closed E01-H/overall E01. MP Singh separately accepted candidate `2aafec4c15a8ea1f05a2a4d97268b8dd1e3fbbec`; PR #3 integrated it as normal merge `58cfa0d53abb002bd33cd185f56f62c9d830162c` with identical tree `4ca87f34300ba92e37f3e331d8e5ce1805fb41d0`. The push-triggered Source CI run `34571622780` passed on that actual merge, and `CP001-IR-58cfa0d-post-merge-v1` accepted the bounded integration result.

PM-R01 changes chronology/index records only; it does not modify this technical decision. CP-002 remains planned/inactive until the records-only closeout is independently reviewed/integrated and activation is separately authorized. Task: `coding/tasks/CP-001.md`. Review route: CPD-12. G01/G09/G22 and UX anchors remain requirement references, not passed product gates.
