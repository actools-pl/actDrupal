# Chat Context, Task Packets and Handoffs

## Purpose and working mode

A fresh ordinary ChatGPT conversation receives or reads the relevant current files and produces one bounded result. Choose and record one route for the task: **human-Git delivery**, where the operator saves and applies a patch or complete files, or **direct GitHub delivery**, where a currently available integration performs already authorized repository operations on the named task branch. The human retains integration authority and operates the test machines. The user's preferred model setting is **5.6 sol / Extra High**, if available. No Work window, ChatGPT Project, shared project memory, connector, background job, automatic repository inspection or SSH capability is required.

Use the five reusable role prompts in [the package index](10_PACKAGE_INDEX.md). Supply current repository instructions explicitly; ordinary chat does not automatically discover AGENTS.md or another chat's attachments. Record actual capabilities and use [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) for authorized connected source work. [RB11](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) establishes the new repository via BOOT-000 before BOOT-001. Reuse valid startup receipts; recheck current identity/refs and applicable automation. A branch or PR may trigger configured automation, and source access does not grant infrastructure, workflow-dispatch, ruleset or merge authority outside the task. Existing bounded task authorization persists without repeated requests for routine edits.

## Build a coding packet

Use [CONTEXT_PACKET](templates/CONTEXT_PACKET.md). The packet has one task ID, revision, intended role and exact base commit. It contains an explicitly selected set:

1. Completed task card, dependency status, selected route and observed repository/branch/base. Record local checkout cleanliness when one is used; use `NOT_APPLICABLE: direct API source editing; no local checkout` when true. Tests/builds later require their own actual source/input observations.
2. Current adopted repository instructions and relevant accepted ADRs.
3. Relevant v1.5.1 sections, including associated detailed acceptance cases and shared constraints. The full architecture can accompany them; an excerpt must name its source revision and section.
4. Complete current files to edit, plus the existing entrypoints, schemas, interfaces, tests and configuration needed to understand the change.
5. Current ledger row, handoff and unresolved findings affecting the task.
6. An inventory mapping each attachment or packet path to its repository path, source commit and purpose. Record a checksum only if an identified tool actually computed it from those bytes; otherwise use `UNSET` with reason `not computed`.

Use committed source at the recorded base. Direct reads must identify full commit-pinned paths, inspect pagination/truncation and record the actual revision returned; a mutable branch URL or tool success message is not sufficient. Do not fetch half the source from one head and half from a later head. Working records kept outside that commit must be explicitly labelled with their packet revision; never disguise them as committed code. Do not recursively zip a working directory: it can contain `.env`, credentials, untracked data, old logs or unrelated work. Git-tracked files can also contain secrets. Inspect the allowlisted files before sharing. Treat links and binary artifacts explicitly; do not follow symlinks into private directories.

The operator can assemble the packet manually from exact-commit GitHub views and a local checkout. A capable chat may instead read the allowlisted files at the same immutable commit and return the identical inventory/read receipt. This does not require every package file in every task or a local checkout for an API-only source edit. If the chat cannot inspect an archive, extract it locally and attach the named plain-text files. Do not use a new auto-upload script, encode a private directory or paste an environment dump to work around unavailable attachments.

## Confirm what the chat could actually read

Before implementation or a review verdict, the chat returns a short input receipt using the inventory: **read in full**, **partly read**, **unavailable** or **not needed**, with the actual revision and any missing sections. A visible attachment name, successful upload or summary is not proof of readable full content. Material needed source that is partial or unavailable blocks the dependent change or verdict; the chat asks for the specific missing file or range and can continue unrelated read-only analysis.

The human checks that this receipt matches the intended packet. No model statement alone proves exhaustive reading; later code review, tests and the actual resulting diff remain necessary. If a filename exists in several revisions, identify which one applies before coding. Never reconstruct absent source from a previous conversation, architecture examples or a remembered signature.

## Keep the task small enough to finish

Choose one coherent outcome whose necessary current files, requirements, complete change, tests and documentation can be inspected and delivered together. Do not use a guessed token allowance or a promised model context size as the gate. If the chat cannot inspect the required context or finish the delivery, the coordinator narrows the task while retaining meaningful acceptance criteria and explicit interface dependencies.

The architecture is large. Use its full baseline as a reference and provide the exact relevant sections and detailed cases; do not spend each session repeating its entire narrative. A shorter task must not omit authorization, errors, cleanup, wiring or required failure tests. A handoff summary helps navigation and does not replace current source.

## What the coder returns

Use [DELIVERY_MANIFEST](templates/DELIVERY_MANIFEST.md). Each delivery names one task, input-packet revision, exact base, delivery revision and type:

- **Direct GitHub candidate:** actual returned candidate commit, verified parent/base relationship, complete changed-file inventory and immutable diff/file references. Read back the resulting candidate and reconcile all declared changes. Provide required file contents to a reviewer who cannot access the references; a downloadable patch is optional for this route.
- **Unified patch:** one complete patch including additions, deletions and file modes.
- **Complete changed files:** complete named file bodies, with an explicit create/modify/delete/mode inventory. No replacement file may say “the rest is unchanged.”

The report states changed behavior, interface effects, meaningful tests and actual results, documentation/changelog changes, remaining findings and handoff details. The model must not invent hashes, commit IDs, execution or a saved-file link. A base SHA must be actually observed from Git/GitHub. A candidate SHA exists only after an actual commit, created by the operator or returned by a verified authorized GitHub operation. For direct GitHub delivery record operation results, observed final branch head and any incomplete or uncertain effect; do not present a proposed SHA as a commit.

For manual delivery, if downloadable-file creation is unavailable, return a complete plain-text diff in one code block, or complete named files in separate code blocks, with the same manifest. The operator saves the contents in a plain-text editor, excluding Markdown fences and surrounding commentary, and follows [RB10 — plain-chat file handoff](runbooks/RB10_PLAIN_CHAT_FILE_HANDOFF.md) and [RB02](runbooks/RB02_RECEIVE_AND_APPLY_A_PATCH.md). A download link or plain-text response must describe the same complete delivery. Do not return a shell script that generates or installs the change as a delivery substitute.

For direct work, re-read the expected task-branch head before writes and use the available concurrency precondition required by RB12. A per-file blob SHA alone does not prove that an entire branch stayed at the expected base. If the available tool cannot prevent a conflicting overwrite or provide a safely reconcilable operation, fall back to the human-Git route for that mutation. Unexpected head drift requires refreshed source and scope/review impact assessment; do not force or overwrite concurrent changes. If a write times out or returns an ambiguous result, inspect the remote file/commit/branch/PR state before retrying; track unknown outcome as blocked. A multi-file operation partly committed is a real incomplete candidate to reconcile, not an unapplied patch to recreate blindly.

End the response with `DELIVERY COMPLETE: <task ID> / <delivery revision>` only if every listed item was delivered; otherwise use `DELIVERY INCOMPLETE` with the missing items. This helps spot interruption; it does not replace manifest and complete candidate inspection. The manual route also requires Git applicability/staged-diff checks; the direct route requires verified read-back and remote-state reconciliation. An incomplete response, absent file, visibly cut-off block or mismatched manifest is **not ready to apply or integrate**. For direct delivery, preserve observed remote commits and resume by reconciliation at the actual head; the display being interrupted does not mean writes failed. For a manual delivery, preserve it as incomplete and request a complete replacement of the bounded patch or affected whole-file delivery from the same base. Do not concatenate an unanchored “continue,” apply an arbitrary prefix or guess missing code. If size caused the interruption, revise the task boundaries before another delivery.

## Review packet and full-file coverage

Start a fresh reviewer conversation with neutral requirements and the actual candidate: task contract, base/candidate SHAs, complete actual diff, complete changed files and necessary unchanged entrypoint/schema/authorization/executor dependencies, plus relevant tests and available sanitized receipts. Include dependencies that determine the changed behavior; this does not require reviewing the entire repository for every bounded task. The coder's explanation can provide context but is not the review checklist or proof of correctness.

Use the coverage table in [REVIEW_RECORD](templates/REVIEW_RECORD.md) to distinguish read-in-full files, deliberately bounded unchanged context and missing material. Trace the public or CLI entrypoint through validation, authority and effect to the result. Code and tests may share an incorrect assumption; reviewers need independent failure examples and observable outcomes. Missing material files or incomplete delivery prevent a reliable acceptance recommendation. Fresh chats using the same model are useful separate reviews, not a guarantee of independent security expertise. Reviewers may use verified read access, but do not edit or publish reviews/comments without applicable authorization. Corrections belong to an authorized coding task. An AI review made through the same connected account is not independent human approval and must not be represented as satisfying a separate-human approval rule.

## Corrections and a changed base

After a candidate has been committed, a correction normally uses that candidate as its new exact base. Refresh the packet with current complete affected files, unresolved finding IDs, failed attempt receipts and delivery history. State whether a new delivery replaces an **unapplied** earlier delivery at the same base or is an **incremental correction** on an actual candidate. Mark the old delivery superseded; do not apply both by accident.

If integration changes the base, record both identities and have the coordinator assess dependency and review impact. Reissue current source and a corrected task packet. Do not replay an old full-file bundle, force an old patch onto new code or silently resolve concurrent edits. Use RB02 for local clean-base/patch corrections and RB12 for direct branch/candidate reconciliation. Change of route must be recorded; reconcile any remote candidate before applying a manual replacement. Review the corrected full files and final actual diff, close findings with evidence, and rerun affected tests; old review conclusions do not automatically transfer to new bytes.

## Evidence-return packet

Use an attempt ID for every run. Include commit, artifact digest, target role/generation, OS/tool versions, exact commands, start/end times, exit status, observed assertions, cleanup and test limitations. Preserve failures and link subsequent corrections. A proposed command is not a test receipt.

Redact before upload, including paths, environment dumps, headers, exception text and tokens in URLs. Keep a controlled original only when permitted and necessary; the index points to the redacted copy used for review. A checksum binds bytes but does not prove a trustworthy independent observer produced them.

## Session restart and close

Before a new conversation or interruption, save the actual delivery/evidence and complete [HANDOFF](templates/HANDOFF.md). Update [PROJECT_STATE](records/PROJECT_STATE.md) and [SESSION_HANDOFF](records/SESSION_HANDOFF.md) through the normal record workflow. Record unapplied, applied-uncommitted and committed changes separately, including packet/delivery revision, selected route, exact remote candidates and outstanding/uncertain write operations. Preserve genuine failed test receipts; a later success does not erase them. An observed merge SHA may coexist with task status `blocked` until required integration checks pass.

Use [the restart prompt](prompts/05_SESSION_RESTART.md) with current records, active task, current code and outstanding review/evidence. The new chat reconciles the facts before proposing changes. If branch or files differ from the handoff, preserve both states and stop competing edits. Do not resolve context drift using force-push, hard reset, unchecked overwrite or silent cherry-picking. An interrupted display is not permission to repeat remote effects; inspect the operation through its implemented runbook first.
