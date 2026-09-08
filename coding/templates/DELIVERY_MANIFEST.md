# Delivery manifest — <task ID> / <delivery revision>

Template only. Use for each complete coding delivery. Choose one route. The manifest describes the delivery; verify the actual candidate diff and complete changed files through [RB02](../runbooks/RB02_RECEIVE_AND_APPLY_A_PATCH.md) for human-Git delivery or [RB12](../runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) for direct GitHub delivery.

## Delivery identity

| Field | Value |
|---|---|
| Task / task-card revision / authorization reference | <...> |
| Input-packet revision | <...> |
| Delivery revision / previous delivery relationship | <new / replaces unapplied ID / increment on actual candidate SHA> |
| Repository / task branch / exact full base SHA | <actually observed values> |
| Type — choose one | <direct GitHub candidate / unified patch / complete changed files> |
| Delivery method | <verified GitHub operations / downloaded file / complete plain-text code blocks saved by operator> |
| Candidate SHA / parent identity | <actual Git/GitHub observations / UNSET until a commit exists> |
| Observed final task-branch head / observation UTC | <actual values / UNSET> |
| Completion status | <complete / incomplete with exact missing items or unresolved effects> |

Do not invent a checksum, download link, remote write, commit ID or test. `DELIVERY COMPLETE` does not mean accepted, merged or release-qualified.

## Route-specific receipt

### Direct GitHub candidate

- Capability and authorized operation boundary verified in this chat: <record>.
- Expected branch head and concurrency control used: <actual values and operation semantics>.
- Actual returned write/commit identities and candidate parent relationship: <record>.
- Candidate read-back: <complete resulting diff, commit-pinned full changed files and final branch-head observation>.
- PR URL/number and exact base/head, if actually created: <actual values / none>.
- Pending, rejected, partial or uncertain writes and reconciliation outcome: <record / none>.
- Complete reviewer inputs available through: <immutable references verified readable or supplied full files/actual diff>.

A direct candidate needs no fictional patch, sender-computed digest or local source-edit checkout. Use `NOT_APPLICABLE` with that reason for absent export/checkout fields. Any exported artifact or later build/test still needs its actual identity and source/input evidence. Re-read immutable candidate contents; do not treat a successful write response as proof that the intended full change exists. Verify unexpected branch drift before another write. If a result is uncertain, inspect remote state before retrying; preserve real partial commits and record the candidate incomplete until reconciled.

### Human-Git patch or complete files

- File/bundle name and actual saved location: <record>.
- SHA-256 and computation source: <actual value/tool / UNSET: not computed>.
- Each complete-file digest when no bundle is used: <record>.
- Exact-base clean checkout / applicability and staged-diff observations: <record>.
- Candidate identity from Git after committing: <actual SHA / UNSET>.

When the chat cannot compute a digest from actual bytes, leave it `UNSET`; the operator computes the saved patch/bundle or per-file digests before passing the candidate onward. Compare any sender-provided digest. No sender digest is required when unavailable. Hashes identify bytes; they do not establish correctness or approval. Follow [RB10](../runbooks/RB10_PLAIN_CHAT_FILE_HANDOFF.md); do not include Markdown fences in saved source or casually change identified bytes.

## Complete changed-file inventory

| Repository-relative path | Create / modify / delete | Mode or mode change | Purpose | Delivery location or commit-pinned path |
|---|---|---|---|---|
| <...> | <...> | <explicit value / unchanged / verified from base> | <...> | <candidate path / patch / named complete file block> |

List tests, documentation, lockfiles, configuration and workflow changes as well as application code. Renames identify old and new paths. Explain executable modes and link/binary artifacts. If the tool or delivery cannot preserve or expose them for review, use a suitable safe route for that change. No replacement file may contain ellipses or instructions to retain unseen code. A generator/installer script is not a substitute for delivering the actual change.

## Behavior and evidence

- Behavior changed and requirement IDs: <...>.
- Interface or dependency effects: <...>.
- Tests added/changed, proposed commands and target conditions: <...>.
- Tests actually executed with receipts: <... / NOT_RUN with reason>.
- Documentation and changelog included: <paths / specific not-needed reason>.
- Open findings, unsupported conditions and review questions: <...>.

Unavailable chat execution does not erase actual operator/CI test results. Keep each real failed or passed receipt at its actual source/artifact/environment identity.

## Candidate receipt checks

| Check | Actual observation |
|---|---|
| Selected route and authorization match; no unexplained extra effects | <...> |
| Task/base/packet/delivery revisions agree; superseded deliveries marked | <...> |
| Every declared changed file is present/readable at the identified candidate or saved delivery | <...> |
| No truncated content, missing files, guessed continuation or unexplained paths/modes | <...> |
| Full actual diff and changed files inspected; secret checks complete | <... / NOT_RUN> |
| Manual route: exact-base applicability, staged diff and saved-byte identities | <actual results / NOT_RUN / NOT_APPLICABLE with reason> |
| Direct route: expected-head protection, write results, parent/candidate/read-back and final head | <actual results / BLOCKED / NOT_APPLICABLE with reason> |
| Actual candidate is ready for independent review and specified tests | <yes with basis / no and exact blocker> |

End the coding response with `DELIVERY COMPLETE: <task ID> / <delivery revision>` only when the intended delivery and required receipt are complete. Otherwise say `DELIVERY INCOMPLETE` and name the missing items. The marker does not prove correctness. Do not apply an incomplete manual delivery or integrate an incomplete direct candidate. For a truncated patch request a complete bounded replacement at the same base; never join an unanchored continuation. For an interrupted direct operation inspect actual remote state first, refresh the packet at the real candidate and reconcile only the remaining authorized change.
