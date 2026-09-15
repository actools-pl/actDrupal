# Session handoff

**Prepared:** 2026-09-14 for `CP003-AC01R1-CLOSEOUT-0193528b-v1`. **Subject:** one in-place recovery attempt for the local CP-003 records-only administrative-closeout commit. CP-003 source/package implementation is merged and independently accepted. CP-004 remains `planned` and unactivated.

## Authoritative repository point

- Repository: `actools-pl/actDrupal`, ID `1361769952`.
- Required parent and live `main`: `0193528b54d803399b0e79e621c21fa9759a2a53`.
- Integrated/parent tree: `4bd079679b5a840b6f31dc20553fc5cf7b9f386a`.
- Ordered merge parents: `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`, then `dddc691ae2102ef3fe5c2d85d97db6c3d245f44e`.
- Accepted candidate and retained task branch: `dddc691ae2102ef3fe5c2d85d97db6c3d245f44e` / `task/CP-003`.
- Required existing local branch/head: `records/CP-003-closeout` at `0193528b54d803399b0e79e621c21fa9759a2a53`; remote branch must remain absent.
- Required blocked worktree: exactly the seven authorized unstaged paths with patch SHA-256 `c600fb4c4227821d00eeb81e06fd4f061e779fde03f23c43af54eb17455f9208`; index and nonignored-untracked set empty.
- PR #7 is merged. No branch deletion is authorized.
- `coding/tasks/CP-004.md` and `coding/records/RELEASE_REGISTER.csv` are unchanged controls.

## Accepted CP-003 evidence chain

- Source review `CP003-CPD12-IR1R2-dddc691a-v1`; report SHA-256 `9238eb7cd2b441a2d82d076ef238411493c248fb9984e83b25b50902642f0b39`; F01–F11 and D01 closed.
- Canonical attempt `CP003-E01-SOURCE-dddc691a-v1`; PASS; evidence ZIP SHA-256 `181f5755db3abbfe1734e7feddae6f9de09787597b664e1ec4236814005b5413`; retained wheel SHA-256 `a8c5a083ae88b29f2d3cf469648ba7c426106eccd06c390017c4e172f162a190`.
- Publication attempt `CP003-PUB01-PUSH-dddc691a-v1`; PASS; evidence ZIP SHA-256 `44b41efdf243aa9c09e7ca1bdd2b0379fc62044bc4aafe3a0300b2c7428cf7f9`.
- PR Source CI run/job `34841884042` / `103968536609`, attempt 1, SUCCESS; hosted wheel SHA-256 `20873db8cb8a99b31c7694e96e75e475a688b34f0b43c59e7928bdc55ff26c4a`.
- Actual normal merge `0193528b54d803399b0e79e621c21fa9759a2a53`; exact ordered parents and candidate-identical tree above.
- Post-merge Source CI run/job `34843725735` / `103974490061`, attempt 1, SUCCESS; hosted wheel SHA-256 `8ff88859ecfa5906799ba6f2ba53ebf6e50428c811d835f04481de9f2066bb10`.
- Final review `CP003-CPD12-POST-MERGE-0193528b-v1`; **ACCEPTED POST-MERGE INTEGRATION**; report SHA-256 `44ac2820a645c51d3d45708359c64fab13644e5533e7dbed4b3c8496c4b260be`.

Product/server/release qualification remains **NOT_RUN / NOT CLAIMED**. The evidence-specific wheel hashes do not establish release reproducibility.

## Accepted blocked attempt

`CP003-AC01-CLOSEOUT-0193528b-v1` passed packet, initial-state, remote-ref, base, payload, branch and seven-path checks. It stopped fail-closed during read-only semantic validation with `CP003-ADR003 file digest differs`. Evidence ZIP SHA-256 is `a890b07b8d936e4e788c4d31300c21f0edaeed766badb9b19618894108c1d538`.

The branch was created at the exact integration commit and the intended seven files were left modified but unstaged. `COMMIT_STARTED=NO`; no remote write occurred. The four registered document hashes described each exact Git blob after adding one extra trailing newline. Their corrected exact-byte SHA-256 values are:

- ADR-0003: `f1d4a58f9252ce548573be6a6522539b224cd3f215d2e73bde79f042e5270979`
- contracts reference: `e629ef892a8b5c9ced79378b1be40cf36662e5f254579f4baed6739099767349`
- status/evidence reference: `d040d320858f8e7de3ab22edef9752a42400c6a732b8cab0ab4c3d6d3a479d87`
- source-CI guide: `274febbb815ea9f4503fe00e05f58bab8cc6616e4a3108d4ba24fef03c3d5f6f`

The original runner's applied-hash loop was also ineffective because its field separator did not split the checksum rows. The recovery uses direct `sha256sum -c` manifests before and after replacement.

## Authorized in-place recovery route

Trusted checkout: `/home/veritas/actDrupal-cp002-rerun` on host `test` as `veritas`. Extract and run the sealed packet `CP003_AC01R1_CLOSEOUT_0193528b_v1_OPERATOR_PACKET.zip`. It verifies the exact accepted failure receipt and retained dirty state before modifying anything. It does not switch, recreate, reset or clean the branch. It replaces the same seven paths with corrected complete files, validates exact hashes/diff/records, creates one deterministic local commit, verifies topology and clean state, seals evidence, and stops.

The candidate changes exactly:

1. `coding/tasks/CP-003.md`
2. `coding/records/DOCUMENTATION_REGISTER.csv`
3. `coding/records/PROJECT_STATE.md`
4. `coding/records/REVIEW_LOG.csv`
5. `coding/records/SESSION_HANDOFF.md`
6. `coding/records/TASK_LEDGER.csv`
7. `coding/records/TEST_EVIDENCE_INDEX.csv`

No source, dependency, lock, workflow, release-register or other-path change is permitted. CP-004's task row remains `planned` with all identity/evidence fields `UNSET`; `coding/tasks/CP-004.md` is not modified.

## Validation and evidence return

The packet requires the exact retained seven-path dirty worktree, an empty index and empty untracked set. It verifies exact `main`, task branch, merge parents/tree, absent remote closeout branch, accepted failure ZIP, blocked-state file hashes and patch, corrected payload hashes, final seven-path worktree/index/commit diffs, exact source-document bytes, unchanged CP-004 task and release register, `git diff --check`, the dedicated closeout validator and `python3 coding/tools/validate_workflow.py`.

On success, return:

- `CP003_AC01R1_CLOSEOUT_0193528b_v1_EVIDENCE.zip`
- `CP003_AC01R1_CLOSEOUT_0193528b_v1_EVIDENCE.zip.sha256`

The receipt supplies the actual deterministic closeout commit/tree, exact parent, changed paths, validations and final clean state. Do not edit or rename the returned files.

## Stop point

Stop after the single recovery attempt, whether PASS or BLOCKED/FAIL. Preserve the evidence and repository state. Do not reset, clean, amend, rerun, switch, recreate/delete a branch, push, create a PR/comment, mark ready, merge, force an operation, dispatch/rerun a workflow, release, deploy, operate a server or activate CP-004. The local closeout candidate and recovery receipt require independent review and new authorization before any remote write.
