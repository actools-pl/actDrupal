# Context packet — <task ID> / <packet revision>

Template only. The operator or an authorized chat records actually observed identities before use. This packet transfers context into one role-appropriate conversation under [CPD-12](../records/REVIEW_ROUTE_DECISION.md); it grants no repository access, server access or authority beyond the current task.

## Identity and purpose

| Field | Observed value |
|---|---|
| Task / task-card revision / current state | <...> |
| Packet revision / prepared at UTC / operator | <...> |
| Role and bounded outcome | <coordinator / coder / reviewer / documentation reviewer> |
| Interface / model / effort / provenance | <actual observed value, operator-reported value, or not observable; apply CPD-12 for reviewer-only choice> |
| Reviewer switch / prior coverage | <reason, prior report and exact read/unread boundaries, or not applicable> |
| Repository / branch / exact full base SHA | <verified values; UNSET if not yet observed> |
| Route / capability verification in this chat | <human-Git / direct GitHub; available operations and UTC observation> |
| Task authorization reference / actor / allowed operations | <existing user authorization and exact boundary; no secrets> |
| Branch head observation / intended expected-head precondition | <actual SHA, UTC and operation capability; NOT_APPLICABLE for read-only work> |
| Local checkout state and observation time | <clean / dirty with paths; NOT_APPLICABLE: direct source editing without local checkout> |
| Startup automation/root-commit verification | <RB11 record and applicable freshness; unresolved risks block remote writes> |
| Candidate SHA for review/correction | <actual SHA / none yet> |
| Architecture / adopted ADR and instruction revisions | <...> |
| Previous packet / delivery being replaced or continued | <IDs and reason / none> |
| Actual chat capabilities | <attachment reading, commit-pinned GitHub reads/writes, text response, file generation or execution actually available; otherwise unavailable/unknown> |

An implementation task cannot be ready with an unknown base or necessary missing source. Direct writes additionally require a bounded repository, branch, file allowlist and authorized operation set; available credentials alone grant no task authority. Do not repeat authorization requests for routine work already covered. `NOT_APPLICABLE` for an API source-edit checkout does not waive clean identified inputs for later builds/tests. A coordinator can still identify exact missing inputs. Never invent a hash to complete this table or require a tracked file to contain its own future commit hash.

## Allowlisted input inventory

| Attachment / packet path or actual remote read | Repository path or external source | Source commit/revision | SHA-256 and computation source, or UNSET | Complete file or named baseline section | Purpose |
|---|---|---|---|---|---|
| <...> | <...> | <...> | <actual digest + tool / UNSET: not computed> | <...> | <...> |

Include the task, relevant instructions/ADRs, exact baseline clauses and detailed acceptance cases, complete files to change, needed surrounding source/tests/schema/configuration, current records, open findings and sanitized receipts. Label working task records outside the code commit. Do not substitute an old excerpt for current source. Direct reads must all use the identified immutable source commit and expose truncation/pagination limits; links alone do not establish reading. Dated GitHub observations in handoffs must be reverified before relying on mutable state. Inspect each allowlisted input for secrets, private data, unsafe links and irrelevant bulk before sharing. See [context rules](../04_CHAT_CONTEXT_AND_HANDOFF.md).

## Chat input receipt — filled after inspection

| Input path / revision | Read in full / partly read / unavailable / not needed | Exact missing portion or reason | Does this block the task or verdict? |
|---|---|---|---|
| <...> | <...> | <...> | <yes with reason / no with reason> |

The chat must report its actual access. A visible filename, inferred content, checksum or remembered summary is not a read receipt. Request exact missing files; if an archive is unreadable, the operator supplies the necessary extracted plain-text files. Do not propose overwriting an unseen file or issue an acceptance recommendation without material required context.

## Current facts and unresolved work

- Observed current behavior and required change: <...>.
- Open review finding IDs and status: <...>.
- Actual failed/passed attempt receipts and applicability: <...>.
- Active remote effects or ambiguous operations needing inspection: <...>.
- Documentation and changelog obligations: <...>.
- Proposed commands versus implemented commands: <...>.
- Scope/interface decisions needing resolution: <... or none>.

## Delivery agreement

- One selected type: <direct GitHub candidate / unified patch / complete changed files / review report / task card>.
- Expected delivery revision and exact base: <...>.
- Correction relationship: <new task / replacement of unapplied delivery ID / incremental correction on candidate SHA>.
- Requested tests/docs and their expected files: <...>.
- Can complete required context and delivery fit this task? <yes with bounded scope / no; coordinator must revise>.
- Actual returned candidate identity / parent / observed final task-branch head: <fill after Git/GitHub verification; UNSET beforehand>.
- Human-route file/digest identity: <fill from actual saved bytes; NOT_APPLICABLE for a direct candidate without an exported bundle>.
- Pending/uncertain repository operations: <operation and observed state / none>.
- PR creation/update and merge authority: <separately identify covered operations; no implicit dispatch/server authority>.

For manual delivery the operator follows [RB10](../runbooks/RB10_PLAIN_CHAT_FILE_HANDOFF.md); direct operations follow [RB12](../runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md). In both routes inspect the [delivery manifest](DELIVERY_MANIFEST.md) and check the actual Git result. No incomplete output or unanchored continuation may be applied. Missing execution capability means tests are `NOT_RUN` unless separate real receipts are supplied.
