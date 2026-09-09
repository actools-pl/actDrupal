# BOOT-001 — Review receipt and correction follow-up

**Prepared:** 2026-09-09T07:16:46Z. **Review:** BOOT-001-IR-153d937. **Subject:** operator-reported commit `153d937d56a08000e4cdf41312fbd5cf11567019`, reconstructed tree `8690def93e4ef3c7dc71706452622a0128d15807`, original task base `cc4e94135a5b2709dc907ad799b95b9a4c511f73`. **Disposition received:** CHANGES REQUESTED. This record summarizes supplied evidence; it is not an independent review of the correction and does not close findings.

## Original evidence custody and provenance

Retain the unchanged original files in the controlled external packet. They are supplied again in D02 under `evidence/`, not copied into product/runtime paths.

| Evidence | SHA-256 |
|---|---|
| `BOOT-001_INDEPENDENT_REVIEW_153d937(1).md` (D02 copy: `evidence/BOOT-001_INDEPENDENT_REVIEW_153d937.md`) | `b21d45bf9a0e405aa0ef5586851f3d12ca0b45e7df1cba2659b0100ea074e923` |
| `BOOT-001_REVIEW_COVERAGE_153d937(1).csv` (D02 copy: `evidence/BOOT-001_REVIEW_COVERAGE_153d937.csv`) | `8c737a9a6e015f12e942e47af4c685f55fcf042a18e678f2f7358151ac3f08f2` |

The operator supplied these files; their hashes bind received bytes, not an authenticated reviewer identity. The old review declares Codex Work Mode; the owner now reports Work / ChatGPT 6 Astra and approves [CPD-12](REVIEW_ROUTE_DECISION.md). Its past exact effort remains unobserved here. Original findings and evidence limits are not edited retrospectively.

## Findings and remaining coverage

| ID | Classification / current state | Correction response and closure requirement |
|---|---|---|
| F01 | medium, task-blocking, OPEN | P02 proposes RB01 step 2 separating pre-write checks, actual BOOT-000 result recording, independent new-project backup and safe resume. Re-review complete RB01 and its RB11/change-control/Start Here/handoff dependencies against empty-start and existing-candidate scenarios. Unsafe triggers must still block their affected write. |
| F02 | low, nonblocking, OPEN | P02 aligns the roadmap with 53 parent IDs including BOOT-000/001 and cancelled CP-038/039, and changes the final heading to 8. Compare ledger and headings; do not change CP task IDs/dependencies/states. |
| G01 | disclosed partial semantic coverage, unresolved | Initial review covered task-cited active architecture clauses but not the complete active/historical additions. P02 does not waive that original final-diff reading obligation or treat hashes as semantic review. Resolve material remaining reading before recommending acceptance; preserve precise boundaries and justification. |

Original G01 remaining ranges: active v1.5.1 lines 137–447, 480–1047, 1125–1296, 1335–1584, 1760–1828, 1859–3012; historical v1.5 lines 21–3003. These range identities refer to the frozen files in the original report, not other documents. The historical text stays non-operative even when read. Read complete changed correction files and necessary unchanged dependencies as well as assessing the original final base-to-result additions; no whole-product implementation audit is claimed.

E01: original commit identity/association was operator-reported, while supplied file/tree bytes were independently reconstructed. E02: Windows apply/commit receipts are operator chat output; old Linux rehearsal harness coverage was limited. E03: controls/refs evidence is historical and must be refreshed as applicable before future remote writes; a settings edit PDF alone is not proof of persisted/current detailed enforcement. E04: CPD-12 resolves the interface-choice decision but does not prove the exact prior UI label/effort or ordinary-chat UX. None is automatically an observed product failure. Do not rerun old mutations to manufacture historical evidence.

## Current correction scope and checks

P02/D02 is incremental on `153d937d56a08000e4cdf41312fbd5cf11567019`, not a replacement import on the root. Complete changed files, incremental and final root-to-result diffs, inventories, original reviewer files, owner-decision text and new preparer checks are in the external correction delivery. No new correction commit or operator application is asserted in this preparation snapshot. Its eventual SHA and receipts must be recorded outside the clean checkout before a later reviewed record update.

The original distribution SHA256SUMS, both architectures, both Python helpers, all root files and CP rows are preserved. The fresh-distribution integrity check must pass; the adopted-copy verifier must still fail with exactly the explicitly manifested edits/additions. Do not regenerate its manifest. Workflow lint, F01 tabletop scenarios and F02 count/order checks concern this bounded documentation correction only; the new check receipt names actual commands, environment, outputs and limits. Preparer checks are not independent acceptance, Windows execution or UX-T20.

Findings stay open until a reviewer checks the actual corrected candidate and records closure. Owner approval of the route/correction scope is not task acceptance or merge authority. BOOT-000 is not repeated. CP-001 remains planned until reviewed BOOT integration and required checks.
