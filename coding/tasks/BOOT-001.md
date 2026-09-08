# BOOT-001 — Import the coding workflow into actDrupal

**State:** coding; documentation import prepared for local application, not yet committed, reviewed independently or merged. **Owner:** WP01. **Milestone:** P01. **Depends on:** BOOT-000 accepted with a verified published root. **Architecture:** v1.5.1 §§1.5/7.3/13.1/18.5/18.6.

Use [Start Here](../00_START_HERE_CODER_DOCUMENTATION.md), [change control](../03_GITHUB_AND_CHANGE_CONTROL.md) and [RB11](../runbooks/RB11_NEW_REPOSITORY_STARTUP.md). Select human Git or the currently supported bounded direct route under RB12. No server action is authorized by this card.

## Activation record

| Field | Initial value |
|---|---|
| Canonical repository / integration / task branch | https://github.com/actools-pl/actDrupal / main / task/BOOT-001 |
| Current identity, route and capabilities | MP Singh; human Git on Windows; Git 2.55.0.windows.5 reported. Assistant supplies complete files/patch and performs isolated checks plus connected read-only GitHub inspection. No assistant GitHub write is authorized by this delivery. |
| BOOT-000 root/publication/review and RB11 readiness receipts | Accepted bounded bootstrap; see [BOOT-000 receipt](BOOT-000.md) and [current state](../records/PROJECT_STATE.md). Individual protection settings use owner PDF evidence; protected flag uses connected branch readback. |
| Exact verified main base SHA | `cc4e94135a5b2709dc907ad799b95b9a4c511f73` |
| Local clean-tree evidence or direct exact-tree read receipt | Operator reported task/BOOT-001 created at `cc4e94135a5b2709dc907ad799b95b9a4c511f73`, clean status, no new commit or push. Connected read returns only protected main at that base. Recheck before applying. |
| Exact file allowlist, source operations and merge authority | All 76 validated distribution paths prefixed coding/ plus root README.md; 77 changed paths total, regular mode 100644. Current step allows local patch application/staging and inspection only. No commit, push, PR, merge, settings change or server action in the apply helper. Later operations remain separate. |
| Package destination | coding/ |
| Human owner / independent reviewer | MP Singh / fresh ordinary-chat Independent Reviewer role operated by MP Singh; reviewer conversation not yet opened, independent disposition pending. The preparing assistant is not that independent reviewer. |
| Candidate / merge / review / evidence | Candidate commit UNSET; merge UNSET; independent review NOT_RUN; operator import NOT_RUN at preparation. Sender checks identify delivered bytes in the external DELIVERY_MANIFEST.md and CHECK_RESULTS.json, not a fabricated commit. |

Fill real prerequisite fields before acting; outcome fields stay UNSET until produced. An existing authorization is reused for routine work within its boundaries. No old repository base, branch or evidence is transferable to this new task.

## Complete deliverable and allowed changes

Import the whole reviewed Coding Package v1.3 into `coding/`, including the active v1.5.1 architecture, records, prompts, templates, checksum manifest, read-only helpers and clearly labelled historical reference. Deliberately update root `README.md` to link to `coding/00_START_HERE_CODER_DOCUMENTATION.md` and state implementation is pending.

The exact delivery allowlist is the validated package inventory with `coding/` prefixed, plus root `README.md`. Task-specific public-safe record edits are part of that allowlist and must be manifested. The package includes two Python process helpers; review them as code before execution. Historical reference content is non-operative, byte-exact and excluded from product artifacts; never treat it as current instructions or implementation evidence.

No installer source, installed dependency, CI workflow, privileged handler, credential or server mutation is included. The root seed `.gitattributes` preserves the historical reference bytes with `-text -diff`; its checksum and open-file review establish its identity while authored documentation follows normal text checks.

## Procedure

1. Verify BOOT-000 and RB11 receipts, actual repository ID/URL, current main SHA, automation and controls. Create/verify `task/BOOT-001` at that SHA; reconcile any unexpected ref or dirty tree.
2. On the fresh extracted distribution, review and run `tools/verify_package.py`; verify the active architecture and reference identities. Integrity is byte comparison, not authenticity or product acceptance.
3. Copy the complete package at `coding/` and make the reviewed README pointer change. Do not overwrite existing files silently; unexpected content requires a current diff and explicit reconciliation.
4. Record the real startup/base/route fields; keep all future implementation tasks planned, CP-038/039 cancelled, and runtime evidence NOT_RUN. Copy public-safe BOOT-000 receipt references into the records.
5. Run the reviewed `tools/validate_workflow.py` on the working package, inspect the full diff/inventory/modes, authored-file whitespace and applicable documentation checks. The original distribution SHA256SUMS remains the distribution identity; expected record changes are tracked through Git and do not justify silently regenerating it.
6. Produce the complete delivery manifest/candidate using RB02 or RB12. Review the exact base-to-candidate change, resolve findings with identifiable correction commits and verify all paths/content.
7. Merge only under the actual recorded authority after review and applicable checks. Record the real integration SHA and required post-merge outcomes through the normal follow-up record procedure; failed checks block CP-001.

## Acceptance and next step

The root and package belong to actDrupal; relative links resolve; all delivered bytes/types/modes are accounted for; the active architecture is v1.5.1; historical content is labelled non-operative; no migration task is an active dependency. No product/CI/server action is claimed. CP-001 starts from the verified accepted BOOT integration result.

## BOOT-001-P01 activation and handoff

Packet and delivery: BOOT-001-P01 / BOOT-001-D01. Source distribution: `Actools_Coding_Package_v1.3(1).zip`, SHA-256 `948beb79e1507b529388b8664db7b2184d6bd6868d78fb2a42620fa52cd2adf0`. Its original `SHA256SUMS`, both process helpers, active baseline and historical reference remain byte-exact. The eight package files changed for startup/task bookkeeping are PACKAGE_CHANGELOG.md, records/DECISION_LOG.md, records/DOCUMENTATION_REGISTER.csv, records/PROJECT_STATE.md, records/SESSION_HANDOFF.md, records/TASK_LEDGER.csv, tasks/BOOT-000.md and this task card. No ninth package-file edit is authorized in this delivery. Root README.md receives the deliberate working-documentation pointer. The external manifest names and hashes every delivered file.

Current mode remains ordinary chat and human Git; no move to Work, Projects or an API is made. The package requests 5.6 sol / Extra High. The actual displayed model/effort is not available in the supplied execution evidence; do not invent a match or silently select another setting. This limitation does not change the mechanical import; retain the owner-selected interface setting and resolve any real mismatch before a later implementation session.

### Bounded test plan

Review both complete process helpers before running them. On the fresh distribution, run `python3 tools/verify_package.py` and `python3 tools/validate_workflow.py` from its package root. On the adopted working package, run its unchanged `tools/validate_workflow.py`; the original distribution verifier is expected to identify the eight explicitly manifested bookkeeping edits and is not a whole-working-copy acceptance check. Do not regenerate SHA256SUMS.

For the delivered patch, check exact base and clean state; run `git apply --check --index --whitespace=error-all` before `git apply --index --whitespace=error-all`; then verify the complete staged index, worktree SHA-256 inventory, unchanged root seeds, expected tree, README link and `git diff --cached --check`. The provided apply helper uses no product Python, installs nothing and creates no commit. Sender rehearsal is isolated Linux evidence; it is not an execution receipt for the Windows laptop.

Meaningful stop cases: wrong branch/base/remote; pre-existing coding/ or other untracked material; dirty/staged input; modified patch or manifest; unexpected remote task branch or main drift; failed patch applicability; unexpected output paths/modes/bytes. Preserve actual partial state on error. No reset, clean, force, three-way conflict resolution or silent overwrite is permitted.

After application, retain the operator output outside the checkout. Then create/verify an actual candidate through the selected human-Git workflow and submit the complete exact candidate, manifest and evidence to a fresh reviewer conversation. Candidate creation, any later publication/PR and integration require their respective scope and current checks. CP-001 remains planned until reviewed BOOT integration and required integration checks pass.
