# Session handoff — <task ID>

| Field | Current fact |
|---|---|
| Written at UTC / writer / next role | <...> |
| Task state / card path | <...> |
| Architecture / ADR / contract versions | <...> |
| Repository / branch / exact base SHA | <...> |
| Candidate SHA / final merge SHA, if real | <...> |
| Operation route / capability in the ending chat | <human-Git / direct GitHub; actual available operations, to reverify next chat> |
| Authorization boundary / task-card revision | <repository, branch, paths, operations and existing user instruction> |
| Worktree status | <clean / dirty with paths / NOT_APPLICABLE: direct source edit without local checkout> |
| Remote task-branch head / last verified UTC | <actual SHA and time / UNSET> |
| Input packet / delivery revision and type | <IDs; direct GitHub candidate / patch / complete changed files; complete / incomplete> |
| Correction relationship / superseded delivery | <new / replaces unapplied delivery / increment on actual candidate; IDs> |
| Input-read or review coverage gaps | <specific missing/partial files and next action / none> |
| Installed candidate by host | <devbox; release-test; package digest/profile or none> |

## Completed facts

<Separate committed code, uncommitted applied changes, unapplied patch, actual tests and accepted review findings. Link exact receipts. Do not write “all done” without identities and limits.>

## Pending delivery and remote operations

<Selected route, exact base SHA, packet/delivery revision, complete changed-file list, modes and whether unapplied/applied-uncommitted/committed. For manual delivery record filename, actual saved-byte digest or UNSET and computation source. For direct delivery record actual returned commits, expected parent, observed current head, read-back and PR identity; no exported patch is required. Describe every uncertain write and required follow-up read before retries. Cover complete-file bundles as well as patches. Mark incomplete and superseded deliveries explicitly. If none, say none. An old delivery must be reconciled against current source before application; never join an unanchored continuation to truncated output. See DELIVERY_MANIFEST.>

## Open findings and blockers

| ID | Status / severity | Exact issue | Next action / owner |
|---|---|---|---|
| <ID> | <...> | <...> | <...> |

## Next bounded action

<Who acts, on which host/repository, prerequisites, expected outcome and stop condition. Distinguish proposed command from an implemented verified command.>

## Files to supply or read in the next chat

<Use [CONTEXT_PACKET](CONTEXT_PACKET.md): current task/instructions/ledger, exact relevant architecture clauses and detailed cases, complete changed source plus necessary unchanged entrypoint/interface/schema/authorization/executor dependencies, actual diff and sanitized receipts. List paths, source revisions and actual digests or UNSET. The new chat verifies its actual available capabilities and returns a read receipt from attachments or commit-pinned repository reads; material partial/unavailable inputs must be supplied before the dependent action. A past connector observation or branch URL is not current access or immutable source. If direct operations are unavailable, reconcile actual remote changes then use the manual route.>

## Environment and cleanup obligations

<Operation IDs needing inspection; temporary resources; quarantines; active maintenance state; intended retained fixtures; independent evidence/key location references without secrets.>

## Documentation/support truth

<Documents changed, walkthrough status, capability graph update permitted by evidence, unqualified tests and release limitations. Preserve failed receipts and unresolved integration checks. A real merge SHA does not clear blocked task status until required integration checks pass.>
