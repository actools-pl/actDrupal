# BOOT-001 — final review, integration and closeout record

**Prepared:** 2026-09-09T17:42:09Z. **Task:** BOOT-001. **Original base:** `cc4e94135a5b2709dc907ad799b95b9a4c511f73`. **Initial candidate:** `153d937d56a08000e4cdf41312fbd5cf11567019`. **Accepted corrected candidate:** `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1` / tree `27ced31b2b6d0e2d5ea80d1fd4679981d611b38d`. **Tested merge:** `880f59d86ae936b2c4968378bc6a0b08ba61092f`.

This file preserves the original changes-requested history and records the later corrected review, human acceptance, protected integration and bounded merged-result checks. It is a records-only chronology update, not a new review of product implementation and not activation of CP-001.

## Review chronology

### Initial independent review — BOOT-001-IR-153d937

The initial review requested changes for F01 (startup prerequisite ordering) and F02 (roadmap count/numbering), and disclosed material G01 reading limits. Its immutable evidence remains part of the PR #1 review archive.

- Original review SHA-256: `b21d45bf9a0e405aa0ef5586851f3d12ca0b45e7df1cba2659b0100ea074e923`.
- Original coverage SHA-256: `8c737a9a6e015f12e942e47af4c685f55fcf042a18e678f2f7358151ac3f08f2`.

### Corrected independent re-review — BOOT-001-IR-7c5289b

The corrected candidate `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1` was re-reviewed against BOOT-001-P02 / RP02-v1.

**Disposition:** ACCEPTABLE WITHIN THE STATED BOOT-001 TASK EVIDENCE.

- F01: CLOSED.
- F02: CLOSED.
- Material G01 reading: RESOLVED with explicit direct/prior/mapped coverage.
- CPD-12 reviewer route: consistent; no new material source defect or task-blocking regression found.
- E01/E02 narrowed; E03 retained; E04 reviewer-route choice resolved with observation limits retained.
- Final review SHA-256: `dc031405dea1c92fbf33f3f72846916d0be201a985bce1cb0855b0f5a419d7de`.
- Final coverage SHA-256: `0e128a51d9f4491929cf5d84c9bf830f89cd2653e01b050fcd6df3a130ec9b92`.

Review/acceptance evidence ZIP SHA-256: `7a62ed457367f8995d032437afac5e2beee7730cae5ce49a8a9d81dd8a6d95e9`; attached at https://github.com/actools-pl/actDrupal/pull/1#issuecomment-5604276344.

## Human acceptance, publication and merge

MP Singh separately accepted the exact corrected candidate and later authorized marking PR #1 ready and merging it with a normal protected merge commit. Those decisions did not authorize settings changes, source alteration, branch deletion or CP-001 activation.

Actual integration result:

- PR: https://github.com/actools-pl/actDrupal/pull/1
- Merge SHA: `880f59d86ae936b2c4968378bc6a0b08ba61092f`.
- Merge parents: `cc4e94135a5b2709dc907ad799b95b9a4c511f73` and `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`.
- Integrated tree: `27ced31b2b6d0e2d5ea80d1fd4679981d611b38d`, identical to the accepted candidate tree.
- `task/BOOT-001` retained at `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1`.
- No source conflict resolution, protection bypass, branch deletion or server/dependency operation was recorded.

## Bounded merged-result checks

Fresh bounded documentation integration checks ran against supplied bytes whose complete 81-file graph matched the GitHub-returned merged tree.

| Check | Result |
|---|---|
| Complete source inventory | PASS: all 81 files/hashes/regular modes unchanged |
| Base-to-integrated inventory | PASS: 79 changed paths; 78 `coding/` additions plus root README modification |
| Authored whitespace | PASS: `git diff --check` exit 0 |
| Integrated workflow lint | PASS: 78 package files, 67 Markdown, 338 local links, 5 CSV, 53 tasks |
| Fresh distribution integrity / lint | PASS / PASS: 75 manifest entries; 76 package files, 303 links, 53 tasks |
| Adopted-copy integrity diagnostic | Expected exit 1 with exactly 22 changed and two unlisted paths; no extra discrepancy |
| README/frozen files/ledger/headings | PASS; architectures/helpers/original manifest intact, all 51 CP rows unchanged, sections 1–8, CP-001 planned |
| Supplied pre-merge graph consistency | `git fsck --full --no-reflogs` exit 0; not a signature/authenticity claim |

Integration chronology: https://github.com/actools-pl/actDrupal/pull/1#issuecomment-5604636531.

Integration evidence ZIP SHA-256: `702402f875d384e6d7afa70a98c3ffb460b7cb1ccd56df8cc330a282f73978eb`.
Integration results JSON SHA-256: `1065292430eb0577b42e1626bf1ce12d4a59d0087839833bd58cec9570aeaea0`.

## Retained qualifications

The detailed branch-protection endpoint returns 403 to the managed connector because Administration read permission is unavailable. `main` is observable as protected, but individual saved-rule/admin/app settings retain owner-observation provenance; no independent destructive enforcement test is claimed. No workflow/check runs were returned for the merged SHA, and their absence is not a green CI result. Independent source-backup custody remains unverified.

These are evidence limits, not observed product failures. No installer, CI, devbox, release-test or production qualification is claimed by BOOT-001.

## Closeout disposition

BOOT-001 source integration and its required bounded documentation checks are complete. The task ledger may record BOOT-001 as `merged` with candidate `7c5289bd0c7cfc6b0ac08bbdfad73e4b1b349ff1` and tested merge `880f59d86ae936b2c4968378bc6a0b08ba61092f`. F01/F02 are closed and material G01 coverage is resolved.

This records-only follow-up deliberately does not embed its own eventual merge SHA. After this closeout is reviewed and integrated, read current `main` and activate CP-001 from that actual integration head. CP-001 remains planned until then.
