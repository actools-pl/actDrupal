# BOOT-000 — Establish the independent root commit

**State:** accepted for the bounded direct bootstrap; publication and initial controls evidenced. **Owner:** WP01. **Milestone:** P01. **Depends on:** none. **Product baseline:** v1.5.1 §§1.5/7.3/18.6. Follow [RB11](../runbooks/RB11_NEW_REPOSITORY_STARTUP.md).

## Activate before execution

Record repository `https://github.com/actools-pl/actDrupal`, current verified empty-ref state, actual route/capabilities, operator path, root-commit/push authority, reviewer and applicable automation/protections. Record actual model/effort once per session; reuse the operator's supplied setting. Unexpected existing work is reconciled, never overwritten.

**Exact seed allowlist:** root `README.md`, `.gitignore`, `.gitattributes`, from the three named bootstrap templates in RB11. No product source, package import, CI workflow, credential, server change, license authorship invention or inherited `.git` directory. All files use regular Git mode 100644.

## Outcome and acceptance

1. Review the exact seed contents and staged diff; run the whitespace check.
2. Create a new root commit locally. Its base is `NOT_APPLICABLE_EMPTY_REPOSITORY`; it has no parent.
3. Within the recorded authority, push that exact root to previously absent `main`, verify the returned remote SHA and root-parent relationship, and record applicable controls.
4. Retain the receipt and review outside the checkout for BOOT-001 to import. Set status `accepted` only after actual verified publication. Record candidate_commit as the root SHA; merged_commit is `NOT_APPLICABLE_DIRECT_BOOTSTRAP`. This one-time non-PR bootstrap is explicit; normal later tasks use reviewed task branches/PRs.

**Next:** BOOT-001 from the verified root. No runtime gate has executed. A missing remote, unsafe trigger, concurrent ref or ambiguous write blocks only the affected action; do all authorized preparation and reconcile the concrete issue.

## Execution receipt imported by BOOT-001

This receipt records the operator's completed bootstrap, not a new execution. Operator: MP Singh; source route: human Git on the trusted Windows laptop. The assistant performed preparation and connected read-only verification. Exact terminal event timestamps were not retained; the session date reported by the operator is 9 September 2026. Root commit metadata provides its own timestamp, not a timestamp for subsequent publication.

| Field | Recorded fact |
|---|---|
| Repository / ID | actools-pl/actDrupal / 1361769952; public |
| Initial base | NOT_APPLICABLE_EMPTY_REPOSITORY |
| Candidate / published root | `cc4e94135a5b2709dc907ad799b95b9a4c511f73` |
| Complete root tree | `a6f1fe6fbf660c61608c559718ea879d5cfb7f5a` |
| Parent relationship | No parent; confirmed in operator output and earlier connected readback |
| Merge field | NOT_APPLICABLE_DIRECT_BOOTSTRAP; no PR was created for the initial root |
| Seed contents | Only README.md, .gitignore and .gitattributes, all mode 100644 |
| Review | Complete staged seed diff checked in the startup conversation before commit; this is not a separate independent-review conversation |
| Checks | Operator reported all three seed SHA-256 checks OK, empty whitespace findings, exact committed blob IDs, clean working tree and remote SHA readback equal to the root |
| Final root state | Published on main; no bypass, rejection or force push reported |
| Current controls | Owner's PDF displays main-only PR requirement, conversation resolution and no administrator bypass; approvals and required CI checks off; force pushes and deletion not allowed |
| Control evidence limit | Connected branch summary reports protected=true; detailed branch-protection read returned HTTP 403; individual checkbox states rely on the owner-supplied PDF, not an administration readback or destructive enforcement test |
| Runtime / release | NOT_RUN; no installer implementation or deployment |

Root file objects: `.gitattributes` = `e5b811c28b89c35ad7731b5fe3c3e1f1f5287d51`; `.gitignore` = `aba24130fd13cea5a7db6c7d3ec41c89e3eb7798`; `README.md` = `e50dae8305a57a3ef9b3dd2635bc4ceb73619de2`.

External evidence, retained outside this public repository: `actDrupal_BOOT-000_Published_Root_Receipt_2026-09-09.md` (SHA-256 `20a5fe1c9396438694cb7105738388dc4288b4f60b56c50f5f7b435a76249ef3`); `actDrupal_BOOT-000_Protection_Verified_BOOT-001_Handoff_2026-09-09.md` (SHA-256 `903d6becbdcf7f10f6b0b46c18a092690425d43ded8119faa98ee0c18b1e7c0d`); the owner-supplied branch-protection PDF (SHA-256 `97b8d7202c7e622dd84fe99388877cbb15ed88387d14be0c70322bfa36a532d2`). The filenames and hashes are evidence references, not claims that these external files are stored in coding/ or independently backed up.

Earlier setup reports: Actions allowed; workflow token limited to repository contents/packages read; Actions creating/approving PRs disabled; no self-hosted runners or webhooks reported; ChatGPT Codex Connector listed. These are dated owner reports, not a new account-wide automation audit. The three-file root has no workflow. The approved BOOT-001 import likewise adds no `.github/workflows` paths.
