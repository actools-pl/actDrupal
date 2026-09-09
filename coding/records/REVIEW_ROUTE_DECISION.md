# CPD-12 — Practical reviewer route and usage fallback

**Status:** accepted workflow decision by MP Singh in the coordinator conversation on 9 September 2026; incorporation into the BOOT-001 correction is prepared, not yet applied or integrated. **Recorded:** 2026-09-09T07:16:46Z (preparer clock, not an invented user-action timestamp). **Scope:** independent-review and documentation-review roles only. **Supersedes:** CPD-01 only where it required these reviewer roles to use ordinary chat.

## Owner decision

The owner reports using Work / **ChatGPT 6 Astra** for review while usage is available, and chooses ordinary, non-Work chat / **5.6 sol** as the fallback when that usage is exhausted or the selected Work reviewer is unavailable. These are the owner's interface/model labels, not an independently verified product catalogue, account entitlement, quota or underlying model identity. The existing **Extra High** preference accompanies the 5.6 sol fallback when available; Astra's effort selection was not supplied. Record the actual displayed selection when observable, or `operator-reported` / `not observable` as appropriate. Do not ask again merely to switch between these two approved review routes. A different fallback needs a recorded owner choice.

Coordinator and coder sessions, human-Git source handling and server-operation boundaries remain as previously agreed. The decision does not change implementation scope, introduce runtime AI, an API key, an API workflow, a ChatGPT Project dependency or any new service. Work is permitted for review, not required for completion.

## Review and authority requirements remain unchanged

Use a fresh reviewer conversation separate from the candidate's coding conversation, with neutral requirements and the exact candidate's complete files, final diff, task, decisions and evidence. The selected review mode grants no repository editing, commit, push, PR/comment publication, merge, CI dispatch, credentials or server authority. Any such effect needs the applicable separate scope; merely having tools does not supply it. Reading supplied files and producing an external report/coverage file are the review deliverables. Only explicitly selected, source-inspected, bounded local checks may run; do not execute setup hooks, old apply/commit scripts, dependency installation or project tests merely because the Work environment exposes them.

If the Work surface would require additional setup/execution authority that this review does not have, use supplied files without that setup, or the approved ordinary-chat fallback. Do not broaden permissions, connect a private filesystem, enable a runner or transfer credentials to make a reviewer work.

An AI review is not approval by a second human. Human acceptance, protected-branch integration, meaningful testing and evidence gates remain separate. Review-only use of Work is not itself a defect under this decision; it is not evidence that the ordinary-chat interface or an installed operator walkthrough was rehearsed.

## Switching partway through a review

Preserve the current report and coverage as partial when unfinished. Carry the same exact base/candidate/tree, packet revision, full source/diff, open findings, precise read/unread boundaries, checked commands/results and evidence limitations into the replacement review conversation. Reverify file access and supplied identities there. Record the switch, reason, actual new interface/model/effort and whether the report extends or supersedes a prior one. Attribute earlier reading/tests to their original reviewer; never relabel them as fresh reading/execution. Re-read changed material and necessary dependencies, and resolve material missing coverage before an acceptance recommendation. An incomplete prior review is not discarded or converted into a PASS because usage ran out.

## Existing BOOT-001 review and document precedence

The received report self-describes Codex Work Mode; the owner now confirms their review selection as Work / ChatGPT 6 Astra. Preserve both statements with their provenance. This decision authorizes the route and future fallback; it does not fabricate a screenshot, change the old report, establish its exact past effort setting or erase F01, F02, G01 or E01–E04.

For reviewer-role selection, this owner decision and the updated operative prompts take precedence over generic ordinary-chat-only wording in frozen distribution copies, the older review kickoff, and earlier preparation snapshots. This is not permission to ignore any product, security, reading or test requirement. The active architecture v1.5.1 and historical v1.5 bytes stay frozen; coding still uses its agreed ordinary-chat route. No whole-architecture audit or product qualification follows from this process amendment.

See [decision log](DECISION_LOG.md), [review follow-up](BOOT-001_REVIEW_FOLLOWUP.md), [independent reviewer prompt](../prompts/03_INDEPENDENT_REVIEWER.md) and [handoff procedure](../04_CHAT_CONTEXT_AND_HANDOFF.md).
