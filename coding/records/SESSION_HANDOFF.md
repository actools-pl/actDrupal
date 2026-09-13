# Session handoff

**Prepared:** 2026-09-13 for `CP003-ACT-a1efe3b2-v1`. **Subject:** local CP-003 activation only. CP-002 has no pending implementation or closeout work. CP-003 is `ready`; coding waits for acceptance of the activation receipt and exact local activation commit/tree.

## Authoritative repository point

- Repository: `actools-pl/actDrupal`, ID `1361769952`.
- Activation source base / live `main`: `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`.
- Base tree: `f6c8196e8e79a1558d76cbfaa7623708615599a1`.
- Ordered base parents: `0810b890928e61afa8d94f2f8d64e1c867203b29`, then `d2c806c5c8a5bb3529907e1256dbeabe945af821`.
- Required new local branch: `task/CP-003`; it must be absent locally and remotely before the activation packet creates it.
- Retain `task/CP-002` at `f0d2d59e6edb0b7a1ccac8254bd0099788bb2ad1` and `records/CP-002-closeout` at `d2c806c5c8a5bb3529907e1256dbeabe945af821`.
- Current CP-003 source task blob before activation: `6face2dcd35eafe45690c8d97c29329a02f851b1`.

## Dependency closure

- CP-002 source acceptance: `CP002-CPD12-IR1-01-FINAL-f0d2d59e-v1`.
- Implementation merge and post-merge acceptance: `0810b890928e61afa8d94f2f8d64e1c867203b29`; `CP002-CPD12-POST-MERGE-0810b890-v1`.
- Administrative closeout content/publication: `CP002-CPD12-AC01-d2c806c5-v1`; `CP002-CPD12-CLOSEOUT-PUB-HOSTED-d2c806c5-v1`.
- Actual closeout merge: `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`.
- Actual-merge Source CI: run `34731677435`, job `103655487400`, success / `SOURCE-CI: PASS`.
- Final closeout disposition: `CP002-CPD12-CLOSEOUT-POST-MERGE-a1efe3b2-v1`, **ACCEPTED POST-MERGE INTEGRATION**; report SHA-256 `72446d2b5372db8e20d91c88d1c5ed4905cddd345a435ff1f383f3d047d14ebf`.
- Reviewed final closeout receipt SHA-256: `5eebc517bb69fba4f9d5935b8dae9ea70e66d03bbc1030227a1ddd4da802bbf5`.

## Activation authority and route

MP Singh authorized starting CP-003 and this Work / 5.6 Sol max window. The interface/model label is operator-reported; the underlying selector is not independently observable. The human task owner is MP Singh. Implementation review follows CPD-12: Work / ChatGPT 6 Astra while available, ordinary 5.6 sol Extra High fallback.

The selected source route is Human-Git. Trusted checkout: `/home/veritas/actDrupal-cp002-rerun` on host `test`, Ubuntu 26.04.1 LTS x86_64, operator `veritas`. Packet directory: `/home/veritas/cp003-activation-a1efe3b2-v1`. The packet creates the branch and one deterministic local activation commit; no separate branch-creation command is permitted.

The activation commit changes exactly:

1. `coding/tasks/CP-002.md`
2. `coding/tasks/CP-003.md`
3. `coding/records/DOCUMENTATION_REGISTER.csv`
4. `coding/records/PROJECT_STATE.md`
5. `coding/records/REVIEW_LOG.csv`
6. `coding/records/SESSION_HANDOFF.md`
7. `coding/records/TASK_LEDGER.csv`
8. `coding/records/TEST_EVIDENCE_INDEX.csv`

It records dependency closure and freezes the separate 43-path implementation allowlist in `coding/tasks/CP-003.md`. It runs no dependency installation, project/source test, workflow, remote write or product operation. Its only content checks are `git diff --check` and `python3 coding/tools/validate_workflow.py`.

## Frozen implementation boundary

The exact 43-path allowlist, tool/schema versions, 13 fixture paths, two packaged policy fixtures and five test commands are normative in `coding/tasks/CP-003.md`. CP-003 implements initial graph/schema/model/evaluation boundaries only. It excludes privileged execution, effects, collectors, schedules, rendering, draft schemas, new action families, duplicate registries/evaluators and admission authority. No dependency/lock/workflow/CLI handler change is authorized.

Product/server/release qualification remains **NOT_RUN / NOT CLAIMED**. CP-003 source fixtures cannot pass a product-wide G gate.

## Next action and stop point

Verify and execute the sealed Human-Git activation packet exactly once. Return its receipt ZIP and checksum sidecar. Do not code, amend, reset, clean, rerun, push, create a PR, dispatch a workflow, merge or delete a branch after the activation run. The coordinator must first verify and accept the receipt, commit/tree, parent, task-card blob, eight-path diff, clean state and validation result. A failed run is preserved evidence and requires a corrected packet or explicit recovery decision.
