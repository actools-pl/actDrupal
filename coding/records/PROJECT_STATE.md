# Project state

**Record prepared:** 2026-09-13 for activation `CP003-ACT-a1efe3b2-v1`. **Package:** 1.3. **Architecture:** 1.5.1. **State:** BOOT-000/BOOT-001 and CP-001 remain complete. CP-002 implementation and administrative closeout are merged and independently accepted within their bounded scopes. CP-003 is `ready` on exact base `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`; its local activation receipt/commit/tree must be returned and accepted before coding.

| Field | Value |
|---|---|
| Canonical repository / ID | `https://github.com/actools-pl/actDrupal` / `1361769952`; repository observed public |
| Scope | Fresh installations only; no existing-site migration or legacy backup import |
| Active specification | Frozen architecture v1.5.1 |
| Current live `main` at CP-003 activation | `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`; tree `f6c8196e8e79a1558d76cbfaa7623708615599a1`; normal PR #6 merge with ordered parents `0810b890928e61afa8d94f2f8d64e1c867203b29`, then `d2c806c5c8a5bb3529907e1256dbeabe945af821`; observed protected |
| CP-001 dependency point | CP-001 records closeout is integrated through base `32ecc8978c968e39d72391cde1ee97d931834ef9`; CP-002 activation `CP002-ACT-32ecc89-v1` used that exact base |
| CP-002 implementation subject | Accepted candidate `f0d2d59e6edb0b7a1ccac8254bd0099788bb2ad1` on retained branch `task/CP-002`; PR #5; normal merge `0810b890928e61afa8d94f2f8d64e1c867203b29` with parents `32ecc8978c968e39d72391cde1ee97d931834ef9` + `f0d2d59e6edb0b7a1ccac8254bd0099788bb2ad1`; merge tree `c8c1c4099b66cb1f623c993358f8693ff90227ff` equals the accepted candidate tree |
| CP-002 source review | `CP002-CPD12-IR1-01-FINAL-f0d2d59e-v1` — accepted exact candidate `f0d2d59e6edb0b7a1ccac8254bd0099788bb2ad1`; IR1-01 and IR-04 closed and all earlier CP-002 findings remained closed; source report SHA-256 `07a4c7cd7a71d25342faa1ec237b1194dd6776e8917fc0ef028e7c711bb9dc59` |
| CP-002 post-merge review | `CP002-CPD12-POST-MERGE-0810b890-v1` — **ACCEPTED POST-MERGE INTEGRATION** for `0810b890928e61afa8d94f2f8d64e1c867203b29` and post-merge run/job `34718507884` / `103619931310`; report SHA-256 `86247ead16276ca263e35f7cc554c62469ba3141532d01ccd6bd5d162b746326` |
| CP-002 administrative closeout | Retained branch `records/CP-002-closeout` at accepted head `d2c806c5c8a5bb3529907e1256dbeabe945af821`; content acceptance `CP002-CPD12-AC01-d2c806c5-v1`; publication acceptance `CP002-CPD12-CLOSEOUT-PUB-HOSTED-d2c806c5-v1`; PR #6 actual merge `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3` |
| CP-002 final closeout integration | Push Source CI run `34731677435` / job `103655487400` completed successfully on exact merge `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`; final acceptance `CP002-CPD12-CLOSEOUT-POST-MERGE-a1efe3b2-v1`; report SHA-256 `72446d2b5372db8e20d91c88d1c5ed4905cddd345a435ff1f383f3d047d14ebf`; reviewed receipt SHA-256 `5eebc517bb69fba4f9d5935b8dae9ea70e66d03bbc1030227a1ddd4da802bbf5` |
| CP-002 local evidence | Final Human-Git receipt SHA-256 `2bc84e7d28cf241ba9ae77bfc0f1838f32a939faf6958bf12715a34a0f39e69d`; local canonical wheel `6553d0fb5e2697ea43fb7bca46e113e367fe70d60649718ff0a6f5697c335109`; lock `1ac29d7c89c7c59afabe414429083786d9170c2b363ca61552dbbc0989a77fae`; JCS set `99ec46b9c79cd60a60315a78346a67d760ec59c0f528f053176feefb7957414b` |
| Hosted PR evidence | Source CI run `34718115021` / job `103618885540` passed on PR merge ref `2b347ccae46695e4f60dba25129a4294c006da76` for accepted base/head, with hosted wheel `e344522472c2bee026f8e7509a499219ccd9ed4cefadb095df6715c0ff45dbee` |
| Hosted integration evidence | Push Source CI run `34718507884` / job `103619931310` passed on exact actual merge `0810b890928e61afa8d94f2f8d64e1c867203b29`, with hosted wheel `66dc3cc6efbe94fce993bc10231218a136494fc0dabf5f209056ba9cce484804` and `SOURCE-CI: PASS` |
| Final findings | IR-01, IR-02, IR-03, IR-04, IR-05, IR1-01, DOC-01, DOC-02, CP002-F01 and CP002-F02 are closed. FINAL-DOC-01 was closed by the additive external erratum SHA-256 `59af572748ad112822c5a6680217d0d79f60b2426e946b2421f4518e5e183f0f` without rewriting historical evidence or source. |
| Retained branches | `task/CP-002` remains at `f0d2d59e6edb0b7a1ccac8254bd0099788bb2ad1`; `records/CP-002-closeout` remains at `d2c806c5c8a5bb3529907e1256dbeabe945af821`; no deletion is authorized |
| GitHub controls/automation | `main` is observable as protected. Detailed protection GET was unavailable to the independent reviewer (403); the accessible branch summary did not establish complete historical protection enforcement. Source CI remains the unchanged PR-to-main/push-main workflow with `contents: read`. |
| Product/server/release qualification | **NOT_RUN / NOT CLAIMED.** CP-002 qualifies only its bounded configuration-contract source/integration slice. It does not qualify Drupal installation, host hardening, privileged execution, firewall/SSH, backup/restore, release signing, production admission or any product-wide G gate. |
| CP-003 activation authority | MP Singh, 2026-09-13: start CP-003 in an authorized Work / 5.6 Sol max window. Activation `CP003-ACT-a1efe3b2-v1` creates local branch `task/CP-003` from the exact live-main base and commits exactly eight records/task paths. It authorizes no source implementation before activation receipt acceptance and no push, PR, merge, release, deployment or server operation. |

## CP-002 retained evidence anchors

- Final source review `CP002-CPD12-IR1-01-FINAL-f0d2d59e-v1` report SHA-256 `07a4c7cd7a71d25342faa1ec237b1194dd6776e8917fc0ef028e7c711bb9dc59`.
- Final independent post-merge review `CP002-CPD12-POST-MERGE-0810b890-v1` report SHA-256 `86247ead16276ca263e35f7cc554c62469ba3141532d01ccd6bd5d162b746326`.
- Local final Human-Git receipt SHA-256 `2bc84e7d28cf241ba9ae77bfc0f1838f32a939faf6958bf12715a34a0f39e69d`.
- Local lock SHA-256 `1ac29d7c89c7c59afabe414429083786d9170c2b363ca61552dbbc0989a77fae`; JCS set SHA-256 `99ec46b9c79cd60a60315a78346a67d760ec59c0f528f053176feefb7957414b`.
- Hosted PR Source CI `34718115021` / `103618885540`; hosted wheel `e344522472c2bee026f8e7509a499219ccd9ed4cefadb095df6715c0ff45dbee`.
- Actual integration merge `0810b890928e61afa8d94f2f8d64e1c867203b29`; post-merge push Source CI `34718507884` / `103619931310`; hosted wheel `66dc3cc6efbe94fce993bc10231218a136494fc0dabf5f209056ba9cce484804`.
- FINAL-DOC-01 external erratum SHA-256 `59af572748ad112822c5a6680217d0d79f60b2426e946b2421f4518e5e183f0f`.
- Administrative closeout merge `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`; final push Source CI `34731677435` / `103655487400`; final closeout review `CP002-CPD12-CLOSEOUT-POST-MERGE-a1efe3b2-v1`, report SHA-256 `72446d2b5372db8e20d91c88d1c5ed4905cddd345a435ff1f383f3d047d14ebf`.

## Current task boundary

CP-002 has no pending implementation or closeout work. CP-003 activation is bounded by `coding/tasks/CP-003.md`: exact base/tree, 43-path implementation allowlist, frozen versions, fixtures, commands, documentation and exclusions. The Human-Git activation packet changes exactly eight records/task paths, creates the local task branch and stops. Coding begins only after its returned receipt and exact activation commit/tree are accepted. Implementation may then change only the 43 activated paths. Publication, PR, merge, branch deletion, workflow dispatch, product/release qualification, deployment and server operations remain separately authorized stages.
