# Project state

**Record prepared:** 2026-09-10 after CPD-12 re-review and D01 platform reconciliation. **Package:** 1.3. **Architecture:** 1.5.1. **State:** BOOT-000/BOOT-001 including records-only closeout are complete; CP-001 remains blocked on E01 after `CP001-IR-1bdb6b09-v1`, with F01-F06 source corrections verified. MP Singh has authorized the bounded E01 sequence on a disposable Ubuntu 26.04.1 test server. No CP-001 remote branch, PR, hosted workflow run or merge is authorized or recorded.

| Field | Value |
|---|---|
| Canonical repository / ID | `https://github.com/actools-pl/actDrupal` / `1361769952`; repository observed public at CP-001 activation |
| Scope | Fresh installations only; no existing-site migration or legacy backup import |
| Active specification | Frozen architecture v1.5.1 |
| Current live `main` at final pre-write readback | `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2`; tree `e189ff949ba8ff79de2302d5e8150ef8838077e3`; observed protected |
| BOOT-001 source milestone | Accepted source candidate `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`; PR #1 source merge `880f59d86ae936b2c4968378bc6a0b08ba61092f` |
| BOOT-001 records closeout | Accepted closeout branch head `8e378d88bf663a16c685f788bca0d26bb6483a51`; PR #2 merge/current base `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2`; integrated tree `e189ff949ba8ff79de2302d5e8150ef8838077e3` |
| Retained branches at activation | `task/BOOT-001` at `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`; `records/BOOT-001-closeout` at `8e378d88bf663a16c685f788bca0d26bb6483a51` |
| GitHub controls/automation | `main` observable as protected; detailed protection GET remains 403 to managed connector; rulesets observed empty; no existing source workflow/status context at base; absence is not green CI |
| CP-001 authorization | MP Singh, 2026-09-10: local branch/candidate work within the exact 27-path allowlist plus the later explicitly authorized bounded E01 execution on a disposable Ubuntu 26.04.1 test server; no remote publication/PR/Actions/merge/settings/deployment/production authority |
| CP-001 local branch / route | `task/CP-001` / Human Git. Remote branch was absent at final pre-write readback. |
| CP-001 implemented intent | Minimal `actools-drupal` development package, zero runtime dependencies, truthful version/help only, bounded source CI and source documentation |
| CP-001 candidate / review / merge | Candidate `4036274201658873f8324f06224adc8f6985eeff` = CHANGES REQUESTED. Correction candidate `1bdb6b09ddff16220dc5e414254788ba259e1d15` / tree `13e07bcc266d76adf218e2314853d67771b67b9d`; `CP001-IR-1bdb6b09-v1` verifies F01-F06 source corrections and leaves E01 open. Ubuntu-26.04 platform-alignment candidate `a40c61205a06b5ace32f67ae5c405ea7f89318d1` / tree `283db1551a6fdbbde2165e245cb85cc4cac25a85`; resolver-lock incorporation candidate pending external post-commit binding; merge UNSET |
| Exact source-CI target | Architecture-aligned Ubuntu 26.04 LTS x86_64 / CPython 3.14.7. Local E01 reference host: Ubuntu Server 26.04.1 LTS. Hosted CI: GitHub `ubuntu-26.04` x64, public preview at correction time; workflow not yet published or run |
| Coordinator execution limitation | Coordinator container remains Python 3.13.5 without package-index resolution. Operator-provided disposable E01 host is Ubuntu 26.04.1 LTS x86_64 with uv-managed CPython 3.14.7. Resolver-backed lock generation/comparison has been executed there; hash-locked installation, complete build/install/audit and hosted CI remain pending, not inferred |
| Local evidence chronology | Initial 40362742 receipt: 22 tests and exploratory checks, later invalidated in the affected F01-F06 assurance areas by independent review. Correction work on available Python 3.13.5: focused CLI/scanner/package/workflow tests = 66 passed; exploratory corrected wheel/install checks remain explicitly Python-3.13 evidence. E01 Phase 1C on Ubuntu 26.04.1 x86_64 / CPython 3.14.7 generated a 34-distribution lock from unchanged `ci.in` with pip 26.2.1 + pip-tools 7.6.1 and explicit PyPI resolution; generated lock SHA-256 `6836c3ed72a3667e97b6901f9836f6c0957dd3512911b221986bc7c1b223e7e7`. Hash-locked install/build/audit remains open. |
| Product/server qualification | NOT_RUN. The authorized disposable Ubuntu 26.04.1 E01 host is only a source/dependency test environment; CP-001 does not qualify Drupal, host hardening, restore, release signing or production behavior |
| Evidence custody | BOOT final evidence supplied in the next-window handoff; independent source-backup custody remains unverified |

## BOOT-001 retained evidence anchors

- Final independent source re-review SHA-256: `dc031405dea1c92fbf33f3f72846916d0be201a985bce1cb0855b0f5a419d7de`.
- Final source-review coverage SHA-256: `0e128a51d9f4491929cf5d84c9bf830f89cd2653e01b050fcd6df3a130ec9b92`.
- Review/acceptance evidence ZIP SHA-256: `7a62ed457367f8995d032437afac5e2beee7730cae5ce49a8a9d81dd8a6d95e9`; attachment: `https://github.com/actools-pl/actDrupal/pull/1#issuecomment-5604276344`.
- PR #1 integration evidence ZIP SHA-256: `702402f875d384e6d7afa70a98c3ffb460b7cb1ccd56df8cc330a282f73978eb`; integration results JSON SHA-256: `1065292430eb0577b42e1626bf1ce12d4a59d0087839833bd58cec9570aeaea0`.
- PR #1 merge/integration chronology: `https://github.com/actools-pl/actDrupal/pull/1#issuecomment-5604636531`.
- Final next-window evidence additionally contains the focused D04 closeout review/coverage and PR #2 integration receipt/results that establish current base `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2`.

## Current task boundary

Only paths explicitly listed in `coding/tasks/CP-001.md` may change. The root `README.md` remains unchanged. Review/evidence indexes are not pre-populated with results that have not occurred. Candidate identity, complete diff/tree and actual local execution results are recorded externally after the local candidate is produced and are supplied to the CPD-12 reviewer.

Any live `main` drift, remote appearance of `task/CP-001`, required allowlist expansion, or material architecture/interface change stops dependent work for reconciliation. BOOT operations are not replayed.
