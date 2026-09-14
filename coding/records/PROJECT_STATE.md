# Project state

**Record prepared:** 2026-09-14 for recovery `CP003-AC01R1-CLOSEOUT-0193528b-v1`. **Package:** 1.3. **Architecture:** 1.5.1. **State:** BOOT-000/BOOT-001, CP-001, CP-002 and the bounded CP-003 source/package implementation are complete. CP-003 is `merged` at exact merge `0193528b54d803399b0e79e621c21fa9759a2a53` and independently accepted. The first records-closeout attempt stopped before staging or commit; this corrected seven-path recovery remains local and requires its own receipt and independent review before any remote write. CP-004 remains `planned` and unactivated.

| Field | Value |
|---|---|
| Canonical repository / ID | `https://github.com/actools-pl/actDrupal` / `1361769952`; repository observed public |
| Scope | Fresh installations only; no existing-site migration or legacy backup import |
| Active specification | Frozen architecture v1.5.1 |
| Current live `main` at closeout authorization | `0193528b54d803399b0e79e621c21fa9759a2a53`; tree `4bd079679b5a840b6f31dc20553fc5cf7b9f386a`; PR #7 normal merge with ordered parents `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`, then `dddc691ae2102ef3fe5c2d85d97db6c3d245f44e` |
| CP-002 dependency closure | CP-002 implementation and administrative closeout remain merged and independently accepted through `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3`; CP-003 used that exact base |
| CP-003 activation | `CP003-ACT-a1efe3b2-v1`; records/task activation commit `3a2633f8c73bba438a28ddb7385d23f255458321`; implementation branch `task/CP-003` |
| CP-003 accepted source subject | Candidate `dddc691ae2102ef3fe5c2d85d97db6c3d245f44e`; tree `4bd079679b5a840b6f31dc20553fc5cf7b9f386a`; four commits and exactly 51 PR paths comprising the accepted eight-path activation plus 43-path implementation sets |
| CP-003 source review | `CP003-CPD12-IR1R2-dddc691a-v1` accepted the exact candidate; F01–F11 and D01 closed; report SHA-256 `9238eb7cd2b441a2d82d076ef238411493c248fb9984e83b25b50902642f0b39` |
| CP-003 canonical source evidence | `CP003-E01-SOURCE-dddc691a-v1`, PASS; evidence ZIP SHA-256 `181f5755db3abbfe1734e7feddae6f9de09787597b664e1ec4236814005b5413`; retained wheel SHA-256 `a8c5a083ae88b29f2d3cf469648ba7c426106eccd06c390017c4e172f162a190`; lock SHA-256 `1ac29d7c89c7c59afabe414429083786d9170c2b363ca61552dbbc0989a77fae` |
| CP-003 publication evidence | `CP003-PUB01-PUSH-dddc691a-v1`, PASS; one ordinary non-force push created retained `task/CP-003` at the exact candidate; evidence ZIP SHA-256 `44b41efdf243aa9c09e7ca1bdd2b0379fc62044bc4aafe3a0300b2c7428cf7f9` |
| Hosted PR evidence | PR #7 Source CI run `34841884042`, job `103968536609`, attempt 1, success on the accepted subject; hosted wheel SHA-256 `20873db8cb8a99b31c7694e96e75e475a688b34f0b43c59e7928bdc55ff26c4a`; public evidence comment `5663878636` supersedes only the PR body's pre-run `NOT_RUN` entry |
| CP-003 integration | PR #7 merged normally at `0193528b54d803399b0e79e621c21fa9759a2a53` on 2026-09-14T12:29:41Z; ordered parents are exact base then exact accepted candidate; merge tree equals the accepted candidate tree |
| Hosted post-merge evidence | Push Source CI run `34843725735`, job `103974490061`, attempt 1, success on exact merge `0193528b54d803399b0e79e621c21fa9759a2a53`; hosted wheel SHA-256 `8ff88859ecfa5906799ba6f2ba53ebf6e50428c811d835f04481de9f2066bb10` |
| CP-003 final integration review | `CP003-CPD12-POST-MERGE-0193528b-v1` — **ACCEPTED POST-MERGE INTEGRATION**; no source, scope, topology, evidence-binding or post-merge CI mismatch; report SHA-256 `44ac2820a645c51d3d45708359c64fab13644e5533e7dbed4b3c8496c4b260be`; live-observation cutoff `2026-09-14T13:36:44Z` |
| Retained branch | `task/CP-003` remains at `dddc691ae2102ef3fe5c2d85d97db6c3d245f44e`; no deletion is authorized |
| GitHub controls/automation | `main` is observable as protected. Source CI remains the ordinary PR-to-main/push-main workflow. No settings change or workflow dispatch/rerun is part of this closeout. |
| Product/server/release qualification | **NOT_RUN / NOT CLAIMED.** CP-003 qualifies only its bounded requirement-graph and contract source/package slice. It does not qualify Drupal installation, hosts, networks, privileged execution, backups/restores, deployment, releases or any product-wide G gate. |
| First records-closeout attempt | `CP003-AC01-CLOSEOUT-0193528b-v1` stopped fail-closed during semantic validation because four documentation digests described the exact Git bytes plus an added extra trailing newline. Accepted failure evidence ZIP SHA-256 `a890b07b8d936e4e788c4d31300c21f0edaeed766badb9b19618894108c1d538`; exact seven-path worktree patch SHA-256 `c600fb4c4227821d00eeb81e06fd4f061e779fde03f23c43af54eb17455f9208`; branch created at the exact parent; index and untracked set empty; commit not started; no remote write. |
| Records-only recovery authority | `CP003-AC01R1-CLOSEOUT-0193528b-v1` may operate in place only on the verified blocked branch `records/CP-003-closeout`, correct the four exact-byte document digests and recovery chronology within the same seven authorized paths, run validations and create one deterministic local commit. It may not switch, recreate, reset or clean the branch and authorizes no remote write. |
| CP-004 state | `planned`, base/candidate/merge/review/evidence all `UNSET`; `coding/tasks/CP-004.md` is an unchanged control and CP-004 is not activated |

## CP-003 retained evidence anchors

- Accepted source review: `CP003-CPD12-IR1R2-dddc691a-v1`; report SHA-256 `9238eb7cd2b441a2d82d076ef238411493c248fb9984e83b25b50902642f0b39`.
- Canonical source/package/scanner attempt: `CP003-E01-SOURCE-dddc691a-v1`; evidence ZIP SHA-256 `181f5755db3abbfe1734e7feddae6f9de09787597b664e1ec4236814005b5413`; PASS.
- Publication attempt: `CP003-PUB01-PUSH-dddc691a-v1`; evidence ZIP SHA-256 `44b41efdf243aa9c09e7ca1bdd2b0379fc62044bc4aafe3a0300b2c7428cf7f9`; PASS.
- PR #7 Source CI: run/job `34841884042` / `103968536609`, attempt 1, SUCCESS; hosted wheel SHA-256 `20873db8cb8a99b31c7694e96e75e475a688b34f0b43c59e7928bdc55ff26c4a`.
- Actual integration: merge `0193528b54d803399b0e79e621c21fa9759a2a53`; ordered parents `a1efe3b27f3905d5ccf06aafcf31062e4b02aac3` then `dddc691ae2102ef3fe5c2d85d97db6c3d245f44e`; tree `4bd079679b5a840b6f31dc20553fc5cf7b9f386a`.
- Post-merge Source CI: run/job `34843725735` / `103974490061`, attempt 1, SUCCESS; hosted wheel SHA-256 `8ff88859ecfa5906799ba6f2ba53ebf6e50428c811d835f04481de9f2066bb10`.
- Final independent review: `CP003-CPD12-POST-MERGE-0193528b-v1`; report SHA-256 `44ac2820a645c51d3d45708359c64fab13644e5533e7dbed4b3c8496c4b260be`; accepted.
- Accepted fail-closed closeout receipt: `CP003-AC01-CLOSEOUT-0193528b-v1`; evidence ZIP SHA-256 `a890b07b8d936e4e788c4d31300c21f0edaeed766badb9b19618894108c1d538`; no staging, commit or remote write; retained worktree patch SHA-256 `c600fb4c4227821d00eeb81e06fd4f061e779fde03f23c43af54eb17455f9208`.

The three wheel hashes in local canonical, PR and post-merge evidence differ. The final review accepted this as non-blocking for source integration and explicitly forbids interpreting these hashes as byte-reproducible release evidence.

## Current task boundary

CP-003 has no pending source implementation or integration work. Attempt `CP003-AC01-CLOSEOUT-0193528b-v1` created the local records branch and applied the intended seven-path payload, then stopped before staging or commit on the documentation-digest defect. The only authorized next operation is the sealed one-shot in-place recovery: verify branch `records/CP-003-closeout` at exact HEAD `0193528b54d803399b0e79e621c21fa9759a2a53`, exact blocked patch `c600fb4c4227821d00eeb81e06fd4f061e779fde03f23c43af54eb17455f9208`, empty index/untracked set and exact remote refs; apply the corrected complete seven-file payload; validate; make one deterministic local commit; seal the recovery receipt and stop. No switch, branch creation, reset or clean is permitted.

The closeout candidate itself must receive independent review and separate authorization before any push, PR or merge. No source, dependency, lock, workflow, release-register or other path may change. No publication, workflow action, release, deployment, server operation, branch deletion or CP-004 activation is authorized.
