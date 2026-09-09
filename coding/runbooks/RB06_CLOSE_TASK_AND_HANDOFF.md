# RB06 — Close a task and hand off without relying on memory

**Purpose:** leave enough repository-backed context for another human and fresh ChatGPT window to continue correctly. **Where:** GitHub and trusted local Git client, or the actually available bounded direct GitHub route under [RB12](RB12_DIRECT_GITHUB_OPERATIONS.md). **Inputs:** current task card, candidate SHA/PR, review record, test receipts, documentation changes and known blockers. **Authority:** human maintainer/integrator; an assistant may perform mechanical operations already included in the recorded authorization, subject to every same gate. Edit/PR authority alone does not imply merge authority. **Effects:** record updates and, if accepted, a normal reviewed merge.

## Procedure

1. Check the exact current candidate SHA and compare it with review/test receipts. List any commits made after review or tests. Ask the reviewer to classify which evidence remains valid and which must rerun; do not attach old green checks to changed code without explanation.
2. Reconcile every required acceptance case: passed with evidence, failed, blocked, not run, or explicitly inapplicable with reason. A required missing case prevents task acceptance. Preserve all material findings, including those fixed, with verification evidence.
3. Check the implementation is wired through the actual supported entrypoint and complete for its bounded scope. Placeholder handlers, mock success, missing installed files or undocumented setup do not satisfy “done.”
4. Check operator/maintainer documentation, runbook updates, examples, help and changelog entry. Documentation may describe future work only when explicitly labeled. Commands must match the candidate and identify where they run and required authority.
5. Complete `templates/REVIEW_RECORD.md`, the task's acceptance checklist and `templates/PR_DESCRIPTION.md`. The human maintainer records acceptance. Update state to `accepted` only now; that means this task, not production admission.
6. Re-read the actual PR head/base, protections and required check/review bindings. Merge by the repository's selected normal method after required checks and within recorded merge authority. Bind any direct merge to the exact accepted head using the supported precondition; if the interface cannot safely do that, use the human protected merge route. Honor existing conditional merge authorization without repeated permission once its conditions are met. Record the resulting full integration SHA, actual merge method and PR. Do not force push or move historical tags. If conflicts are resolved or source changes at merge, treat the result as a new candidate requiring affected review/checks.
7. Run/inspect applicable checks on the integrated source. Record the distinction between tested candidate and merge SHA; release-test qualification later uses the actual identified built artifact. If integration fails after a real merge, retain that SHA/fact and the failed receipt, open a blocking corrective task, and block affected dependents/candidate qualification. Do not rewrite history or treat the merge as evidence of passing integration.
8. Record the actual merge SHA/date in `merged_commit` immediately when known. While required integration checks are pending or failing, keep task status `blocked`, retain the actual merge fact and record the blocker/corrective task. Set status `merged` only after those checks pass. If no merge occurred and acceptance is incomplete, leave `changes_requested` or `blocked` with the exact reason/owner/next step. Update the task/review/evidence indexes and current project state. Use `deferred`/`cancelled` only for an explicit recorded disposition.
9. Fill `templates/HANDOFF.md` and publish the active handoff to `records/SESSION_HANDOFF.md`. Link the final relevant files, current branch/SHA, environment generations, open risks and next ready task. Record any server state or unfinished cleanup that the next person must know.
10. Put final merge/receipt/handoff bookkeeping that can exist only after merge into a small reviewed follow-up records PR or the repository’s explicitly approved equivalent protected workflow. Its commit records the earlier tested subject; no self-referential SHA is required. Do not bypass branch rules with a direct integration-branch push. Ensure code and public-safe evidence are committed/pushed to the intended repository; keep private evidence/keys in their approved custody. Verify the new handoff can be understood without opening the old chat. Start a fresh session with the current task package and required source files when needed.

## Minimum handoff contents

- Task ID/status, architecture/WP/requirement references and decision changes, if any.
- Base, candidate and integration SHA; PR; installed artifact identities if tested.
- Operating route/capabilities, bounded authorization, actual remote writes and any ambiguous outcome/concurrent-ref issue; current startup/root-commit references.
- What changed and why; actual tests and limitations; review outcomes.
- Documentation/runbook/changelog paths and any unresolved operator confusion.
- Both boxes' roles/current generations; installed candidate; pending operations/cleanup.
- Next task, dependencies, exact files to supply and authority still needed.
- Precise blockers and owner, with no secrets or claim of an unexecuted gate passing.

## Expected / stop / recovery

Expected: another person can identify authoritative source, safely inspect current state and begin the next ready task. Stop closure on mismatched SHAs, missing required evidence, unresolved material findings, undocumented manual fixes or an uncertain target. Preserve current records and issue a concrete correction; do not erase failed evidence or rewrite history.

**Records:** `records/PROJECT_STATE.md`, `records/TASK_LEDGER.csv`, `records/REVIEW_LOG.csv`, `records/TEST_EVIDENCE_INDEX.csv`, `records/SESSION_HANDOFF.md`. Update `records/RELEASE_REGISTER.csv` only when the work actually changes a candidate/release record.
