# Project state

**Record prepared:** 2026-09-11 after human acceptance, PR #3 integration, passing push-triggered Source CI and independent post-merge review. **Package:** 1.3. **Architecture:** 1.5.1. **State:** BOOT-000/BOOT-001 are complete. CP-001 accepted implementation/source candidate `2aafec4c15a8ea1f05a2a4d97268b8dd1e3fbbec` was merged as `58cfa0d53abb002bd33cd185f56f62c9d830162c` with passing post-merge Source CI and independently accepted integration. PM-R01 records/documentation closeout is locally authorized and pending CPD-12 review before any remote write. CP-002 remains planned/inactive.

| Field | Value |
|---|---|
| Canonical repository / ID | `https://github.com/actools-pl/actDrupal` / `1361769952`; repository observed public |
| Scope | Fresh installations only; no existing-site migration or legacy backup import |
| Active specification | Frozen architecture v1.5.1 |
| Current live `main` at PM-R01 pre-write readback | `58cfa0d53abb002bd33cd185f56f62c9d830162c`; tree `4ca87f34300ba92e37f3e331d8e5ce1805fb41d0`; observed protected |
| BOOT-001 source milestone | Accepted source candidate `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`; PR #1 source merge `880f59d86ae936b2c4968378bc6a0b08ba61092f` |
| BOOT-001 records closeout | Accepted closeout branch head `8e378d88bf663a16c685f788bca0d26bb6483a51`; PR #2 merge `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2` / tree `e189ff949ba8ff79de2302d5e8150ef8838077e3` |
| Retained branches | `task/BOOT-001` at `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`; `records/BOOT-001-closeout` at `8e378d88bf663a16c685f788bca0d26bb6483a51`; `task/CP-001` at `2aafec4c15a8ea1f05a2a4d97268b8dd1e3fbbec`. Remote `records/CP-001-closeout` and `task/CP-002` were absent at the PM-R01 pre-write readback. |
| GitHub controls/automation | `main` observable as protected; detailed protection GET remains 403 to the managed connector; rulesets observed empty. Source CI is merged and runs on PR-to-main/push-main only with `contents: read`; CP-001 did not configure a required check. |
| CP-001 implementation intent | Minimal `actools-drupal` development package, zero runtime dependencies, truthful version/help only, fail-closed source CI and source documentation |
| CP-001 source chronology | Initial `4036274201658873f8324f06224adc8f6985eeff` received CHANGES REQUESTED. Correction `1bdb6b09ddff16220dc5e414254788ba259e1d15` closed F01-F06 source findings with E01 still open. Platform-alignment `a40c61205a06b5ace32f67ae5c405ea7f89318d1` preceded accepted resolver-lock candidate `2aafec4c15a8ea1f05a2a4d97268b8dd1e3fbbec` / tree `4ca87f34300ba92e37f3e331d8e5ce1805fb41d0`. |
| CP-001 independent review chronology | `CP001-IR-40362742-v1` -> CHANGES REQUESTED; `CP001-IR-1bdb6b09-v1` -> F01-F06 source corrections verified/E01 open; `CP001-IR-2aafec4-v1` -> no new source defect/local evidence gaps open; `CP001-IR-2aafec4-local-receipts-v1` -> Local E01 accepted; `CP001-IR-2aafec4-E01H-v1` -> E01-H/overall E01 closed; `CP001-IR-58cfa0d-post-merge-v1` -> post-merge source/integration ACCEPTABLE, PM-R01 records closeout open. |
| CP-001 human acceptance / implementation merge | MP Singh separately accepted exact candidate `2aafec4c15a8ea1f05a2a4d97268b8dd1e3fbbec` and authorized normal protected integration. PR #3 merged as `58cfa0d53abb002bd33cd185f56f62c9d830162c`; parents `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2` + `2aafec4c15a8ea1f05a2a4d97268b8dd1e3fbbec`; merge tree `4ca87f34300ba92e37f3e331d8e5ce1805fb41d0` equals accepted tree. Retained task branch was not deleted. |
| Local E01 evidence | Phase-2 archive SHA-256 `d452112d68a46553cc8b25dd1c9c81deabe9f234907289622d26e801e66e2e52`; retained local wheel `6afa0d7ea5b664bcd4edcd206cefbddb9558ccb704ea4fe777570002b4591abd`; generator/source-integrity supplement SHA-256 `630e558c316bdfba6d0e4f9f756136a55d6e09ddd14f8ebefc8217b6901a463f`; committed lock SHA-256 `6836c3ed72a3667e97b6901f9836f6c0957dd3512911b221986bc7c1b223e7e7`. Exact test rows are in `records/TEST_EVIDENCE_INDEX.csv`. |
| Hosted E01-H / integration evidence | PR Source CI run `34569300056` / job `103167778389` passed on PR merge subject `974712aaf6035c69d72a46821eb36ccb563cc517` with hosted wheel `85da105c2b8baec7983b568187fea377e1a4ef4aefe76af5498508c8ff32ce77`. Post-merge push run `34571622780` / job `103174769272` passed on actual merge `58cfa0d53abb002bd33cd185f56f62c9d830162c` with hosted wheel `a9c57aa62fdbbef84dc1cc6952316de4eb9f892c4ebe5011260061afe5d9c35b`. Both recorded Ubuntu 26.04.1 / CPython 3.14.7 and `SOURCE-CI: PASS`. |
| PM-R01 closeout authority | MP Singh, 2026-09-11: local Human-Git `records/CP-001-closeout` from exact base `58cfa0d53abb002bd33cd185f56f62c9d830162c`; exactly nine records/documentation paths; no closeout push/PR/merge/settings/source/workflow/dependency change or CP-002 activation. Closeout candidate identity is external after commit to avoid self-reference. |
| Product/server qualification | **NOT_RUN / NOT CLAIMED.** CP-001/E01 qualify only the bounded source/package/CI slice. They do not qualify Drupal, host hardening, firewall/SSH, backup/restore, release signing, production behavior or any product-wide G gate. |
| Evidence custody | CP-001 review/evidence artifacts are retained externally with public-safe digests/IDs recorded below and in the review/evidence indexes. Independent source-backup custody remains a separate project concern. |

## CP-001 retained evidence anchors

- Initial review `CP001-IR-40362742-v1` report SHA-256: `092a442a075f48539c72a8b984b0eca2edd7f6ca7e19260603fb5bb8dd1649d0`.
- Correction re-review `CP001-IR-1bdb6b09-v1` report SHA-256: `23c3a1ce221aa567ae3ad8a71ab0e7a17c707c1d9d283bceefc19cd4a0ea420f`.
- Focused candidate review `CP001-IR-2aafec4-v1` report SHA-256: `3ed2c60c2a22467144dba358686d0c7e0f3582f19eb7c2d05e35fc5cfdea2cd3`.
- Local receipt review `CP001-IR-2aafec4-local-receipts-v1` report SHA-256: `c77b39df3548b058ee9565ecfd2b5049da7655c42c0f3407abaae2dbe996d008`.
- E01-H review `CP001-IR-2aafec4-E01H-v1` report SHA-256: `66af42084583733828c7dc1096a2665a73ccedc724c8778ae023e651ada2abb1`.
- Post-merge review `CP001-IR-58cfa0d-post-merge-v1` report SHA-256: `e50d7d370165c8459d3bb070e057864bfcde4036b8974c82615a5dc98ddef451`; coordinator post-merge packet SHA-256 `43a313ddc261af1dbb1f5f24499c487eb429374b7dc201ae2cab3dcb02d85b30`.
- Phase-2 archive SHA-256 `d452112d68a46553cc8b25dd1c9c81deabe9f234907289622d26e801e66e2e52`; local receipt supplement `630e558c316bdfba6d0e4f9f756136a55d6e09ddd14f8ebefc8217b6901a463f`; original Phase-1C archive `f8926d0963b0a4996942b5e923a93925e6f78aa9eba7e20d9d8410c5e065d10e`.
- GitHub run IDs: PR E01-H `34569300056`; post-merge push integration `34571622780`.

## Current task boundary

PM-R01 is the only active CP-001 follow-up. Exactly these nine existing paths may change in the locally authorized closeout candidate: `coding/tasks/CP-001.md`, `coding/records/TASK_LEDGER.csv`, `coding/records/PROJECT_STATE.md`, `coding/records/SESSION_HANDOFF.md`, `docs/adr/0001-package-and-source-ci.md`, `docs/development/source-ci.md`, `coding/records/DOCUMENTATION_REGISTER.csv`, `coding/records/REVIEW_LOG.csv`, `coding/records/TEST_EVIDENCE_INDEX.csv`. The accepted implementation/source/workflow/lock/tests remain unchanged. CP-002 is still planned and inactive; do not create a task branch or populate its activation record until PM-R01 is reviewed/integrated and separately activated.
