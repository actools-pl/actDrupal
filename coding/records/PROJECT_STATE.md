# Project state

**Record prepared:** 2026-09-09T17:42:09Z (coordinator record; underlying GitHub/operator event times are recorded separately). **Package:** 1.3. **Architecture:** 1.5.1. **State:** BOOT-001 source integration completed and bounded documentation integration checks passed; records-only closeout; product implementation not started.

| Field | Value |
|---|---|
| Canonical repository / ID | https://github.com/actools-pl/actDrupal / 1361769952; repository remained public during BOOT-001 |
| Scope | Fresh installations only; no existing-site migration or legacy backup import |
| Active specification / historical reference | Frozen v1.5.1 / non-operative unchanged v1.5 |
| BOOT-000 root | `cc4e94135a5b2709dc907ad799b95b9a4c511f73` |
| BOOT-001 accepted candidate / tree | `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1` / `27ced31b2b6d0e2d5ea80d1fd4679981d611b38d` |
| BOOT-001 PR / tested merge | PR #1 / `880f59d86ae936b2c4968378bc6a0b08ba61092f` |
| Merge relationship | Normal merge commit with parents `cc4e94135a5b2709dc907ad799b95b9a4c511f73` and `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`; integrated tree equals the accepted tree |
| Review | BOOT-001-IR-7c5289b: ACCEPTABLE WITHIN THE STATED BOOT-001 TASK EVIDENCE; F01/F02 closed; material G01 reading resolved |
| Human acceptance / integration authority | MP Singh accepted the exact candidate and later authorized the normal protected merge; source integration is complete |
| Integration checks | PASS within bounded documentation scope; see `records/TEST_EVIDENCE_INDEX.csv` and PR chronology comment |
| GitHub controls | `main` observed protected. Detailed branch-protection GET returns 403 because the managed connector lacks Administration read access; individual saved-rule/app/automation checks retain owner-observation provenance |
| Task branch | `task/BOOT-001` retained at `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`; no branch deletion requested |
| Records follow-up | This file is the records-only BOOT-001 closeout subject. Its own bookkeeping commit/PR is intentionally not self-referenced; verify current `main` before the next task |
| Product source / source CI / server qualification | Not implemented / NOT_RUN / NOT_RUN |
| CP-001 | Planned and **not activated by this closeout record** |
| CP-038 / CP-039 | Cancelled; all other CP tasks remain planned |
| Evidence custody | Review/acceptance evidence is attached to PR #1; integration chronology is recorded in the later PR comment. Independent source-backup custody remains unverified |

## BOOT-001 evidence anchors

- Final independent re-review SHA-256: `dc031405dea1c92fbf33f3f72846916d0be201a985bce1cb0855b0f5a419d7de`.
- Final review coverage SHA-256: `0e128a51d9f4491929cf5d84c9bf830f89cd2653e01b050fcd6df3a130ec9b92`.
- Review/acceptance evidence ZIP SHA-256: `7a62ed457367f8995d032437afac5e2beee7730cae5ce49a8a9d81dd8a6d95e9`; attachment: https://github.com/actools-pl/actDrupal/pull/1#issuecomment-5604276344.
- Integration evidence ZIP SHA-256: `702402f875d384e6d7afa70a98c3ffb460b7cb1ccd56df8cc330a282f73978eb`.
- Integration results JSON SHA-256: `1065292430eb0577b42e1626bf1ce12d4a59d0087839833bd58cec9570aeaea0`.
- Merge/integration chronology: https://github.com/actools-pl/actDrupal/pull/1#issuecomment-5604636531.

## Retained limits and next action

The BOOT-001 checks qualify only the documentation/workflow import. No installer, CI, devbox, release-test, backup-recovery or production behavior is thereby qualified. No workflow/check runs were returned for the merged SHA; absence is not a green CI result. The detailed protection endpoint remains unavailable to the connector and independent source-backup custody remains unverified.

On the next session, first verify the actual current `main`, records-closeout state and applicable controls. If this closeout has been reviewed and integrated, activate CP-001 from that actual current integration head under a fresh bounded task packet. Do not replay BOOT-000, D01, D02, publication or PR #1 operations.
