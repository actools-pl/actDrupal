# RB10 — Files in and out of an ordinary chat

**Purpose:** give a fresh coding or review conversation the right files, then receive a complete result without depending on Work, Projects, connectors or chat memory. This runbook is the **human-Git route** and supplements [context rules](../04_CHAT_CONTEXT_AND_HANDOFF.md) and [safe patch receipt](RB02_RECEIVE_AND_APPLY_A_PATCH.md). When current chat access and bounded authorization support direct GitHub operations, use [RB12](RB12_DIRECT_GITHUB_OPERATIONS.md) for those operations and candidate receipt; a manual patch/download is not mandatory. Both routes retain the same source-read, complete-file review and evidence requirements.

**Location and authority:** the operator's trusted laptop, local Git client and ordinary ChatGPT browser window. Preparing files does not authorize executing received code or changing a remote server. Use a text editor for code; Word and rich-text editors can alter characters and formatting.

Before remote actions, follow [RB11](RB11_NEW_REPOSITORY_STARTUP.md) for current new-repository identity/ref/automation checks and the bounded BOOT-000 root step. BOOT-001 follows the verified root. Reuse actual completed startup receipts and current bounded authority; a route change does not establish missing evidence. No old-repository backup, ancestry or preservation sequence is a prerequisite. Direct edits need no fictional local worktree; human patch application still requires its real clean-base checks.

## 1. Prepare one coherent packet

1. Follow RB01 to select one ready task and verify its actual full base commit and clean checkout. Administrative packet records may live in a controlled directory outside that checkout until their reviewed record change. Never fabricate a self-referential commit hash.
2. Create a new task/packet-revision directory outside the checkout, using only non-secret identifiers. Keep inputs, received outputs and test receipts distinguishable. This is a human file arrangement, not a new application state store.
3. Fill [CONTEXT_PACKET](../templates/CONTEXT_PACKET.md): task and packet revision, intended role, architecture/decision references, actual base or candidate, full required files and evidence. Attach the relevant repository instructions explicitly; ordinary chat is not assumed to discover them.
4. Export the exact required committed source files from the identified checkout. A trusted local Git client can show an individual file at a full commit; the operator must select the actual path and revision. A GitHub permalink containing the commit can help identify it, but a link is not proof that this chat can read it. Supply the file contents when needed.
5. Include complete affected files and relevant existing consumers, entrypoints, schemas and authority helpers. Include precise architecture excerpts with section IDs and enough surrounding requirements. Keep the full unchanged baseline available. Do not attach the entire evolving repository merely because a ZIP is convenient.
6. Remove secrets and irrelevant data before upload. An allowlisted source selection is preferable to deleting a few known secrets from a broad archive. Exclude `.git`, credential stores, environment secrets, private keys, real site content, unrestricted logs, downloaded dependencies and unrelated local configuration. Names, excerpts and screenshots can disclose sensitive data too.

Use the packet's file inventory to identify missing or conflicting revisions. If checksums are used, compute them from the actual saved bytes on the trusted laptop; a model must leave an uncomputed digest unresolved. A checksum supplied beside the same files detects accidental mismatches, not publisher authenticity.

## 2. Start a normal chat and verify access

Open an ordinary ChatGPT chat outside Work and Projects. Select the user's requested model/reasoning setting if actually available in that interface, and record the observed selection. Prompt text does not change the account's model picker. Do not silently switch interface or model to get around an unavailable option.

Attach the packet files and paste the appropriate complete role prompt. Ask the model to report which files it actually read, which were partial/unavailable, and which required dependencies are missing. A filename displayed in chat is not sufficient evidence of readable content.

If an archive cannot be opened, supply the required individual files or split a large packet into named batches under the same packet revision. Each batch has an explicit inventory; the model waits for the complete declared input set before proposing a complete implementation or review disposition. If the session cannot retain the necessary full context, reduce the coherent task or restart; do not rely on a guessed token limit or an unverified summary.

The model may perform useful analysis of available material, but a material unread file prevents a complete coding/review claim. Re-upload the specific missing item; do not ask it to guess the absent code from an older conversation.

## 3. Receive a complete delivery

The agreed output is one bounded patch, or a manifest-defined set of complete changed files when that is more reliable. Use [DELIVERY_MANIFEST](../templates/DELIVERY_MANIFEST.md). It identifies the task, packet revision, exact base, delivery type, each changed/deleted/renamed path and relevant modes, and what was actually checked.

When downloadable artifacts are unavailable, the model can return a complete plain-text patch or complete named file bodies in code fences. Save only the intended bytes using a plain-text editor. Preserve indentation, Unicode, file endings and the declared final newline. Save patch files with their intended `.patch` extension, not an editor-added `.txt`; never include surrounding commentary or Markdown fences in them.

“The rest is unchanged,” ellipses, omitted functions, invented download links or an interrupted code block are not a complete file. Do not apply output until every manifest item and the explicit completion statement are present. A completion statement is a consistency signal, not a substitute for inspecting the saved files.

If delivery is truncated, label it incomplete and preserve it separately. Request a complete replacement for the affected bounded patch/file at the same exact base. Do not assemble code from an unanchored “continue” or mix a fresh full-file replacement with fragments from an older candidate. If complete delivery does not fit reliably, return to the coordinator for coherent smaller tasks or explicitly bounded complete-file deliveries before any application.

## 4. Inspect and apply on the laptop

Follow RB02 before touching the checkout. Inspect archive member names, types, duplicates and size before extraction into a fresh quarantine directory; never extract a generated ZIP over the repository. Copy only declared reviewed paths, handle deletions explicitly, and inspect the resulting staged diff including new files and modes. Reject repository metadata, surprise executable client configuration and undeclared files.

Use the actual quoted path to the saved patch in the RB02 commands. Do not paste placeholder values into a command. Git applicability checks and the staged diff must agree with the intended base and delivery manifest. Whitespace conversion, missing executable bits or case-colliding filenames are defects to resolve, not reasons to skip review.

Once committed, obtain the real candidate commit from Git. The candidate becomes the subject of independent review and selected tests. Applying or committing code is not permission to execute a privileged test script.

## 5. Review, failures and corrections

Start a fresh reviewer chat with neutral requirements, the actual candidate diff, full changed files and necessary unchanged dependencies. Include the read-coverage record and real test receipts. The coder's explanation is useful context but does not replace inspection. Material omissions leave the review incomplete.

For corrections, state whether the previous delivery was never applied or whether the fix builds on an actual candidate commit. Refresh the packet revision, source files, outstanding finding IDs and failed-attempt receipts. A patch against candidate B must not be applied to original base A merely because both belong to the same task.

Send failed tests with the actual command, source/artifact identity, environment generation, exit status, bounded redacted output and observed effects. Record chat-local execution as `NOT_RUN` when unavailable; preserve the actual operator-run outcome and receipt separately. An unexecuted proposed test remains `NOT_RUN`. Use the existing testing and reconciliation runbooks before any repeat of an operation with uncertain effects.

## 6. Finish the handoff

Preserve the final delivery, actual Git identities, read/review coverage, test attempts and documentation changes. Update the current records and follow RB06 for the reviewed merge and post-merge record change. Before closing the chat, identify any unresolved remote operation and the next bounded task.

If changing from the direct route to this fallback, first inspect the actual remote task head and any uncertain write/PR result; refresh the packet at the real candidate. Do not reapply a patch over changes already committed remotely or treat a missing chat response as a failed write. Reverify capability in each new chat; no connector is required for this manual route.

**Successful completion:** another operator can locate the exact input packet, received changes, actual candidate, review and evidence without opening the old conversation. This runbook creates no automatic background task or cross-chat memory dependency.
