# Project state

**Record prepared:** 2026-09-09T18:57:00Z (coordinator clarification after independent closeout review; underlying event times remain separately recorded). **Package:** 1.3. **Architecture:** 1.5.1. **State:** BOOT-001 source integration completed and bounded documentation integration checks passed; records-only closeout branch under review/correction; product implementation not started.

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
| Records closeout branch / base | `records/BOOT-001-closeout` / `880f59d86ae936b2c4968378bc6a0b08ba61092f` |
| Reviewed D03 closeout candidate / tree | `10a24fa5a30fe77515800f58fef70c060c938c7b` / `a5e3bb63d0a0b4038e496b361f451e971f74b5bd`; independent review: acceptable within records-only evidence, with CO-01/CO-02 low nonblocking clarity findings |
| Records closeout packet / outputs | `actDrupal_BOOT-001_Closeout_Review_Packet_10a24fa_v1.zip`; `BOOT-001_CLOSEOUT_INDEPENDENT_REVIEW_10a24fa.md`; `BOOT-001_CLOSEOUT_REVIEW_COVERAGE_10a24fa.csv` |
| Records follow-up | Focused D04 clarification changes only `DOCUMENTATION_REGISTER.csv`, `PROJECT_STATE.md` and `SESSION_HANDOFF.md`. Its successor commit is intentionally UNSET until actually created; current closeout bytes are not represented as already integrated |
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

On the next session, first verify the actual current `main`, `records/BOOT-001-closeout` head, records-closeout state and applicable controls. Read at minimum:

- `coding/records/PROJECT_STATE.md`
- `coding/records/TASK_LEDGER.csv`
- `coding/records/REVIEW_LOG.csv`
- `coding/records/TEST_EVIDENCE_INDEX.csv`
- `coding/records/SESSION_HANDOFF.md`
- `coding/records/BOOT-001_REVIEW_FOLLOWUP.md`
- `coding/records/DOCUMENTATION_REGISTER.csv`
- `coding/PACKAGE_CHANGELOG.md`
- `coding/tasks/BOOT-001.md`
- the external D03 closeout review/coverage named above and any later focused D04 review output.

If the records-only closeout has then been reviewed and integrated, activate CP-001 from the actual current integration head under a fresh bounded task packet. Do not replay BOOT-000, D01, D02, publication or PR #1 operations.
