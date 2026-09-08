# Coder Documentation — Start Here

**Actools Coding Package 1.3 — fresh-install revision • 8 September 2026**\
**Product baseline:** Actools Drupal Community architecture 1.5.1\
**Working mode:** ordinary ChatGPT **outside Work and Projects**, using the operator's requested **5.6 sol / Extra High** setting; human-authorized GitHub source control, with direct-chat and human-Git routes; one disposable devbox and one release-test server at Hetzner.

This is the human instruction manual for running the entire coding process. The person following it is called the **operator**. ChatGPT proposes and reviews changes and may perform explicitly authorized GitHub operations through the selected route. The human retains integration authority and controls real-machine execution. No conversation is the authoritative project record.

The package contains documentation, reusable prompts, task records, runbooks and local integrity/workflow checkers. It does not contain an implemented Actools installer. Writing this package has not created GitHub branches, configured either server or passed product acceptance tests.

## 1. How to use this download

Download the complete ZIP and extract it into a new directory. Keep its internal folders together: the relative links in this manual refer to files inside the package. Open Markdown files in a text editor or Markdown viewer. CSV files are ordinary tables; preserve their headers and IDs when editing them.

Begin with this manual, then [the agreed workflow](01_WORKFLOW_AND_DECISIONS.md) and [the roadmap](02_IMPLEMENTATION_ROADMAP.md). Use [the package index](10_PACKAGE_INDEX.md) whenever you need a particular prompt, record or runbook. The copied [v1.5.1 architecture](baseline/Actools_Drupal_Community_Rewrite_Architecture_Implementation_v1.5.1.md) remains the full product specification.

The package can be copied into a reviewed `coding/` directory on a reviewed task branch later. Instructions and links here are relative to the package root; if installed as `coding/`, `records/PROJECT_STATE.md` means `coding/records/PROJECT_STATE.md`. Product source, product `CHANGELOG.md` and installed operator documentation live in their normal repository locations, not inside this package's record folder by accident.

**No remembered fact is sufficient to resume work.** Read the current records and confirm the actual repository state before proceeding.

### The short route through a work session

| Step | Human action | Must be available before continuing |
|---|---|---|
| 1. Prepare | Verify records and Git; activate one bounded task | Actual base, allowed files/effects and acceptance criteria |
| 2. Supply context | Open a normal chat with its role prompt; provide attachments or exact commit-bound readable files | Required files actually read; partial/missing input reported honestly |
| 3. Receive | Save a complete patch/file delivery, or verify the direct GitHub candidate | Delivery manifest, exact base/candidate and complete changed-file content |
| 4. Review | Inspect the actual complete change and start a fresh reviewer chat | Actual candidate and full material review coverage |
| 5. Test | Run selected reviewed commands on the identified test target | Real receipts, protected credentials and known effects |
| 6. Finish | Correct, document, merge and verify; record the handoff | Exact merge result, evidence applicability and next bounded action |

Follow [RB11 — new repository startup](runbooks/RB11_NEW_REPOSITORY_STARTUP.md): verify the new repository, execute the bounded BOOT-000 root-commit step, then import the package through BOOT-001. Use [RB10 — ordinary-chat file handoff](runbooks/RB10_PLAIN_CHAT_FILE_HANDOFF.md) for attachments/files, or [RB12 — direct GitHub operations](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) after current capabilities and operation scope are verified. A failure loops through correction and review; it does not justify skipping a required step.

## 2. What the operator needs

The operator needs access to the agreed GitHub repository, a Git/SSH client, ordinary ChatGPT file attachments, and—when machine tests begin—the registered Hetzner servers and independent console/rescue access. Use a password manager or other protected credential custody outside Git and chat. Start with synthetic data and test credentials.

Basic skills are required: opening/editing a file, uploading an attachment, checking the current folder and running an explicitly identified command. A person unfamiliar with Git or SSH should rehearse the non-destructive repository steps first. A guide cannot make an unidentified destructive command safe.

Shell examples in the runbooks name their shell and execution location. Bash examples belong in a Bash terminal; do not paste them unchanged into PowerShell. Uppercase tokens such as `BASE_COMMIT` or `FILE` are placeholders, not literal values. The task card must replace them with verified values before execution. Never guess the target server, branch, command or missing credential to get past a placeholder.

Ordinary chat is not assumed to have a live checkout, SSH access, background execution, automatic discovery of repository instructions or access to another conversation's attachments. Use fresh normal chats outside Work and Projects. If an ordinary chat offers a useful file-generation or local analysis tool, record what it actually did; the process still works when the model can return only text. The human operates servers. GitHub source operations follow the selected authorized route below; a connection does not itself grant task authority.

Select the requested **5.6 sol / Extra High** setting in the actual interface if available and record the observed selection. Prompt text cannot select a hidden model. If that setting is unavailable, record the mismatch and resolve the choice with the owner; do not silently switch to Work, Projects or another model. No API context limit, fixed attachment count or particular tool availability is assumed. The [audit notes](AUDIT_AND_REVISION_NOTES.md) explain the official-source limits.

| Term | Meaning in this manual |
|---|---|
| Base commit | Exact saved Git revision from which the change starts |
| Candidate commit | Actual new code revision proposed for review and tests |
| Artifact digest | Hash of the actual built/transferred package bytes; distinct from the source commit |
| Merge commit/result | Actual revision integrated into the shared branch; verify its relevant behavior |
| Packet revision | Version of the files, instructions and evidence sent to one chat |
| Environment generation | Recorded identity of a test host after rebuild/reset or other relevant changes |

### Choose and record the GitHub route

| Route | Who performs the source operations | Conditions |
|---|---|---|
| Direct GitHub | ChatGPT uses available connected GitHub operations for the bounded task | Verify actual access and required read/write capabilities in this chat; name the repository, branch, base, file allowlist and permitted operations |
| Human Git | ChatGPT delivers complete patches/files; the operator uses the trusted Git client | Preserve the existing RB02/RB10 checks, actual saved-file identities and clean-base workflow |

Both routes use ordinary chats outside Work and Projects, the same product specification, full review coverage, real test evidence and human integration authority. No connector is required for the fallback route. A GitHub link is not a read receipt; a missing write capability must not be worked around by moving to a different interface or asking for tokens in chat.

Once a bounded task is authorized, routine edits, commits and corrections within its allowed operations can proceed without asking again for every file. A task does not implicitly authorize merge, changing protection, enabling CI with additional authority, creating infrastructure or publishing a release. Use existing explicit authorization where it covers the actual action; otherwise present the completed reviewable candidate and the concrete additional decision needed.

Direct GitHub delivery uses actual repository-returned commit identities and the complete resulting change. It does not require an invented local checkout, downloaded patch or model-computed digest. A server-returned blob identifier identifies a file object, not the branch head or the full candidate. Real builds/tests still need their actual clean inputs and receipts. If access fails or a write outcome is uncertain, preserve the attempted operation and inspect current state before retrying or switching routes.

## 3. The four places and their jobs

| Place | Purpose | What belongs there |
|---|---|---|
| GitHub | Durable project authority | Source, reviewed instructions, accepted decisions, task/review records, redacted evidence references and versioned documentation |
| Devbox | Iteration and destructive tests | Reviewed candidate checkouts, disposable fixtures and explicitly selected test commands |
| Release-test server | Candidate qualification | Verified packages installed through the operator runbook; controlled clean installs, upgrades, reboot and recovery tests |
| Laptop/independent location | Human control and external evidence | Git/chat handoffs, registered external probes, protected backup/recovery material and independently retained test records |

The two servers are development resources. The release-test server contains synthetic data until actual production commissioning is separately authorized. Manually repairing it to make a candidate appear successful creates a defect to fix in source or documentation; it is not a valid installation result.

Do not forward a laptop SSH agent, X11 session or sensitive filesystem to either test server. Keep personal GitHub write tokens, provider credentials and production secrets off both boxes. Use the explicitly reviewed private artifact-transfer or narrowly scoped read-only source-fetch path. A disposable server can still misuse authority exposed to it; see [security rules](08_SECURITY_AND_SCOPE_RULES.md).

Two servers in one provider/account are not proof of independent backup custody. A laptop that is asleep is not an always-on backup or monitor. Development may proceed while unavailable independence/capacity tests remain explicitly unverified. See [test strategy](05_TEST_AND_EVIDENCE_STRATEGY.md).

## 4. The three regular chat roles

| Role | Job | Required output |
|---|---|---|
| Coordinator | Choose a ready task, check dependencies and settle its boundaries | A current, complete task card and context-file list |
| Coder | Implement that one bounded behavior, tests and documentation | One reviewable patch/complete-file set or verified direct GitHub candidate, with full change inventory/content and an honest report |
| Independent reviewer | Challenge the actual candidate against requirements and evidence | Findings tied to files/behavior, missing tests and a disposition for the exact candidate |

A documentation reviewer joins at milestones or when a runbook changes substantially. One human can operate all chats. Use a fresh review conversation with neutral requirements and the actual code; do not treat the coder's confidence as evidence. The same model in separate chats is a useful second pass, not a guarantee of independent security expertise.

Use the [coordinator](prompts/01_COORDINATOR.md), [coder](prompts/02_CODER.md), [reviewer](prompts/03_INDEPENDENT_REVIEWER.md) and [documentation reviewer](prompts/04_DOCUMENTATION_REVIEWER.md) prompts. A role name is an instruction you supply; ordinary chat does not automatically maintain that role or read an `AGENTS.md` file.

## 5. One-time preparation

1. Read [workflow decisions](01_WORKFLOW_AND_DECISIONS.md) and active architecture v1.5.1. The destination is `https://github.com/actools-pl/actDrupal`; scope is fresh installations only.
2. Follow [RB11](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) to verify current identity/refs, permissions and applicable automation. An empty default-branch setting is not an actual base commit.
3. Activate [BOOT-000](tasks/BOOT-000.md). Review the three seed files, establish a new root commit in a fresh checkout and publish/verify it within the recorded startup authority. No existing codebase or history is imported. Record the exact root and actual protection/automation state.
4. Use `main` for integration and `task/BOOT-001` from that verified root. Activate [BOOT-001](tasks/BOOT-001.md), import the package at `coding/`, deliberately add the root README pointer and review the complete change.
5. After BOOT review, merge and applicable checks, activate CP-001 from the actual integration SHA. It introduces the minimal Python package, license/notices and new source CI. Required check names are configured only after the real checks exist and their behavior is verified.
6. Use the existing ordinary-chat model/effort and human-Git/direct route choices. Do not ask the operator repeatedly for settings or authority already supplied for this session/task.
7. Establish the environment register and independent new-project backup practice as real work requires them. Test servers, production endpoints and credentials are not needed just to author the initial schemas.

The architecture retains new-site backup/restore, supported updates and full security/UX qualification. Existing-site migration and legacy backup import are excluded. The original v1.5 report in `reference/` is historical evidence only; current coders use v1.5.1. CP-038/039 remain cancelled identifiers, with no active dependents.

## 6. The daily start procedure

Follow [RB01 — start or resume](runbooks/RB01_START_OR_RESUME_A_SESSION.md):

1. Open the current [project state](records/PROJECT_STATE.md), [task ledger](records/TASK_LEDGER.csv) and [last handoff](records/SESSION_HANDOFF.md).
2. Compare their branch/commit references with the actual remote and, for the human-Git route, the checkout. Record discrepancies; do not resolve them by guessing which chat was latest.
3. Check whether there is an unfinished mutation or unresolved review. Resume that bounded work before opening a conflicting task.
4. Select one dependency-ready task and fill its actual base commit, scope, input files, tests and documentation duties.
5. Build the context packet described in [context and handoff](04_CHAT_CONTEXT_AND_HANDOFF.md), using [CONTEXT_PACKET](templates/CONTEXT_PACKET.md). Include full relevant files and precise baseline sections by safe attachments or verified commit-bound reads; record actual coverage and inspect material before exposing it to chat.
6. Start the appropriate normal chat with the matching prompt and identified inputs; recheck any required connector access in that chat. Require a short read receipt identifying full, partial, unavailable and missing material. Record a conversation reference, but keep all decisions and outputs in repository-backed records.

Size the task so that the relevant complete files, tests, documentation and reviewable change can be handled reliably in one bounded context. Attach an architecture index and exact applicable excerpts with access to the full baseline; asking the model to repeat the entire specification is unnecessary. A partial interface or missing security helper is not a safe substitute for context. Split a large parent task into coherent recorded slices without marking the parent complete early.

Use one active writer for a shared component. Other chats may review or work on explicitly independent files; they must not each reinvent the same schema or command interface.

In the human-Git route, keep administrative record edits from making the code checkout ambiguous. Commit agreed preparation records before capturing the final coding base, or keep the pending task packet in a controlled directory outside that checkout and reconcile it in a later record commit. The packet may name the just-recorded base without requiring a tracked file to contain the hash of its own commit. Before receiving a patch, the code checkout must be clean at its stated base. Never discard records merely to achieve a clean status. In the direct route, bind the input to the actual remote base and inspect the complete returned candidate/tree; local checkout fields may be explicitly not applicable for source editing, but actual test/build working-state evidence remains required.

## 7. The complete task cycle

### Step A — Make the task ready

Start from [TASK_CARD](templates/TASK_CARD.md) or one of the initial cards. Complete every activation field. Include the relevant architecture section and requirement/test IDs, current full files, dependencies and the intended observable result.

The task must say what is allowed to change and which environment may be used. It must identify meaningful failure cases and the exact documentation to update. If a necessary dependency is outside scope, revise the card with the coordinator before implementing it. Routine implementation choices within the already authorized card do not require repeated permission requests.

Change task state from `planned` to `ready` only when those facts are available. A missing provider value, unsupported version or unqualified backend is a concrete blocker, not a default to invent.

### Step B — Ask for the implementation

Supply the task packet to a coding chat and use [the coder prompt](prompts/02_CODER.md). Ask it to inspect the identified current files first. It should deliver one coherent change including tests and documentation, an explanation of behavior and actual verification. The manual route returns a complete patch/file set; the direct route follows RB12 and returns the real candidate, complete changed-file inventory and reviewable content.

Require a [DELIVERY_MANIFEST](templates/DELIVERY_MANIFEST.md) with the actual task/packet/base, complete changed-file set, selected delivery route and final completion statement. A direct delivery is complete only after verifying the actual repository result; read-only planning or an uncertain write cannot be reported as committed code. In the file-handoff route, if downloads are unavailable, use complete plain-text patch/file bodies saved by the human through RB10. Do not apply a truncated result, omitted functions or a guessed continuation. Request a complete bounded replacement at the same base, or revise the task split. Model-uncomputed hashes remain `UNSET` with a reason; the operator computes checksums for actual saved/downloaded bytes. Direct source delivery uses its verified commit/tree and read-back identity without inventing a local archive.

If the chat cannot run a test, its output must say so. A proposed test command is not a passed test. Commands that invoke unimplemented Actools features must remain identified as future examples until the corresponding entrypoint exists.

### Step C — Receive and inspect the change

For the human-Git route, follow [RB02 — receive/apply a patch](runbooks/RB02_RECEIVE_AND_APPLY_A_PATCH.md): confirm the exact base, clean working tree and allowlist; validate applicability and inspect the complete staged change. For the direct route, follow [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md): verify the exact repository/branch base, complete planned file set, actual returned commit and resulting full diff/tree, including deletions and modes. Never use a blind overwrite to resolve concurrent changes.

Both routes require workflow/trigger inspection before writes, because source pushes or PRs may execute CI. Applying/committing a change does not authorize a new installer/test execution outside the task's approved effects. Record only a candidate actually created and read back from Git/GitHub; retain the delivery observation and actual result separately when they differ.

### Step D — Review before privileged testing

Give the independent reviewer the task, relevant complete files, exact diff and available basic-check evidence. Resolve material privilege, destructive-operation, credential or unexpected-command findings before running privileged tests on the devbox.

The reviewer records which full changed files and necessary unchanged entrypoints, schemas, consumers and authority helpers were actually inspected. Material unread/partial inputs keep the review incomplete. The reviewer reports concrete defects and coverage gaps. “Looks good” without identifying the reviewed version and limitations is not sufficient. Record findings in [REVIEW_LOG](records/REVIEW_LOG.csv) and detailed records based on [REVIEW_RECORD](templates/REVIEW_RECORD.md).

### Step E — Execute the selected tests

Follow [RB03 — devbox testing](runbooks/RB03_TEST_ON_DEVBOX.md) and the task's completed [TEST_PLAN](templates/TEST_PLAN.md). Verify the actual target identity, source checkout or installed artifact as applicable, and safety conditions before effects. Run the commands individually as specified; stop on an unexpected result or wrong target.

Capture command, exit status, source commit, package digest where relevant, environment generation, timestamps, observed assertions and cleanup. Source/build runs record clean input identity and relevant pre/post-run worktree state. Installed qualification may have no checkout on the target; it instead retains actual build-source, transfer and installed-artifact identities and the applicable target-state receipt. Dirty-source experiments may help diagnosis but cannot be presented as qualification of the recorded clean commit. Preserve stdout and stderr separately where their contract matters. Use [TEST_RECEIPT](templates/TEST_RECEIPT.md); index redacted receipts in [TEST_EVIDENCE_INDEX](records/TEST_EVIDENCE_INDEX.csv).

Logs may contain untrusted text and secrets. Review/redact them before sending them to a chat or storing public artifacts. Screenshots can supplement a receipt but cannot replace commands, exit codes and exact version identity.

### Step F — Correct and recheck

Return failures as evidence, not as a request to make the tests green by any means. The coder must explain the cause and implement a bounded fix. If the implementation changes, refresh the packet revision with the actual parent candidate, full current files, open review findings and failed receipts; record the new candidate and rerun affected tests. Distinguish a replacement for an unapplied patch from a correction based on an already committed candidate. A reviewer determines whether unaffected evidence can be reused under the same configuration and artifact context.

Never erase a failed test record after a successful retry. Link the new result and resolution. If a valid requirement is infeasible, record a design issue; do not quietly weaken it.

### Step G — Check documentation against runtime

Follow [documentation workflow](06_DOCUMENTATION_AND_CHANGELOG_WORKFLOW.md). Update operator steps, failure guidance, examples and changelog for the actual behavior. Mark a documentation change unnecessary only with a specific reason in the task/PR.

At the relevant milestone, follow [RB08 — documentation walkthrough](runbooks/RB08_DOCUMENTATION_WALKTHROUGH.md). A reviewer must be able to operate the installed candidate using the written instructions. A rescue command supplied only in chat is a documentation defect.

The final UX-T20 walkthrough needs a reviewer with the expected Linux administration background who did not implement the tested flow. Your own rehearsals and fresh AI reviews help prepare it; they cannot close that particular release gate.

### Step H — Accept, merge and verify the merge result

Follow [RB06 — close and hand off](runbooks/RB06_CLOSE_TASK_AND_HANDOFF.md). The human integrator checks the exact candidate's review, tests and docs and controls the merge decision. The human or, when explicitly authorized, ChatGPT performs the allowed GitHub merge through the recorded route. Record the resulting merge commit separately. Revalidate the merged result as required; a conflict resolution or changed build is a new relevant candidate, not automatically covered by an old receipt.

Record the actual merge SHA even if an integration check fails. In that case preserve the failure and actual `merged_commit`, keep the task status `blocked` until required integration checks pass, and open the corrective task; stop affected dependents and qualification. Update later merge/evidence/handoff records through a small reviewed follow-up change, keeping the tested subject commit distinct from the record commit. Do not bypass branch protection to complete bookkeeping.

Update the ledger, project state and handoff. Task merge does not grant production readiness. The capability and release gates require their own complete, applicable evidence.

## 8. What a completed task must contain

| Item | Required record |
|---|---|
| Scope | Current task card, requirements, dependencies and allowed effects |
| Code | Actual candidate diff and repository commit |
| Tests | All required task assertions pass with real receipts; justified `NOT_APPLICABLE` cases and actual limitations remain explicit |
| Review | Findings, fixes and disposition for the exact candidate |
| Documentation | Operator/runbook/reference changes, or a justified no-change decision |
| Changelog | User-visible change and operational/migration consequence where relevant |
| Integration | Actual merged commit and required merged-result verification |
| Continuity | Updated task state and next-session handoff |

A scaffolding task may be merged without full application qualification when its own bounded criteria pass and it advertises no unsupported capability. A task that claims a security/recovery behavior cannot substitute missing required evidence with a general disclaimer.

## 9. Understanding the records

| Record | Who updates it | When |
|---|---|---|
| [PROJECT_STATE](records/PROJECT_STATE.md) | Human integrator | Integration head, active task or global blocker changes |
| [TASK_LEDGER](records/TASK_LEDGER.csv) | Coordinator proposes; integrator records | Each actual state transition |
| [DECISION_LOG](records/DECISION_LOG.md) | Integrator | A scope/workflow decision is actually made |
| [REVIEW_LOG](records/REVIEW_LOG.csv) | Reviewer proposes; integrator records | Findings opened, corrected or dispositioned |
| [TEST_EVIDENCE_INDEX](records/TEST_EVIDENCE_INDEX.csv) | Test operator | Every retained test attempt |
| [DOCUMENTATION_REGISTER](records/DOCUMENTATION_REGISTER.csv) | Documentation owner | A document changes or is rehearsed |
| [RELEASE_REGISTER](records/RELEASE_REGISTER.csv) | Release operator | Candidate built, qualified, rejected or released |
| [SESSION_HANDOFF](records/SESSION_HANDOFF.md) | Current operator | At every pause or transfer to another person/chat |

Dates use UTC ISO 8601 in records; local display may include a named timezone. Do not overwrite real evidence with example values. `UNSET`, empty commit cells and `NOT_RUN` mean unresolved facts, not permission to continue a dependent action.

## 10. Working with the release-test server

Promote only an identified candidate, following [RB04](runbooks/RB04_QUALIFY_ON_RELEASE_TEST.md). Record the source commit and built artifact digest. Use the installed runbook, not a development checkout with extra dependencies that accidentally mask packaging defects.

Test clean installation, repeat application, supported update edges, failure and recovery behavior as the relevant features become available. The accepted optional Cloudflare mode still requires implementation and on/off qualification; opting out on one deployment does not remove that release obligation. Early CP-035 recovery-path proof supports lifecycle development, while complete outage-start RTO including detection, delivery and response closes later at the integrated rehearsal after monitoring/alerts exist. Rebuild the target for clean-state milestones. Retain independent records before destructive resets. A provider snapshot is a convenience reset point, not proof of a clean install or a complete application backup.

When a candidate fails, preserve the result, fix the repository and build a new candidate. Do not apply undocumented permanent fixes directly to the release-test host. Debugging may occur, but the final claim needs a repeat from the specified known state.

See [release and acceptance](07_RELEASE_AND_ACCEPTANCE.md) for test signing versus real release trust, missing independence evidence and final production commissioning.

## 11. How to stop for the day or hand over to another person

Complete the [handoff template](templates/HANDOFF.md) and update [SESSION_HANDOFF](records/SESSION_HANDOFF.md). Include:

- Selected GitHub route, actual branch/base/candidate/merge references, any uncommitted files where a checkout exists, and attempted writes with uncertain outcomes.
- Active task and its current state.
- Tests attempted, outcomes, evidence locations and unresolved findings.
- Whether any remote operation may still be running or have ambiguous effects.
- Current devbox/release-test generations and the last known safe state.
- Documentation/changelog status and the next bounded action.
- Protected secret locations by reference only; no secret values.

The next operator reads the handoff and confirms reality. They do not assume a closed terminal means a remote operation stopped. For ambiguity, inspect the recorded operation and follow its supported reconciliation path.

## 12. Where to go when something goes wrong

| Problem | Next document |
|---|---|
| New chat or lost conversational context | [Context/handoff](04_CHAT_CONTEXT_AND_HANDOFF.md) and [restart prompt](prompts/05_SESSION_RESTART.md) |
| Patch does not apply, branch differs or files are dirty | [RB02](runbooks/RB02_RECEIVE_AND_APPLY_A_PATCH.md) |
| New repository startup, automation or protection is unresolved | [RB11](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) |
| GitHub access unavailable, remote head changed or a write result is uncertain | [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) |
| Attachment unreadable, download missing or code truncated | [RB10](runbooks/RB10_PLAIN_CHAT_FILE_HANDOFF.md) and the delivery manifest |
| Test failed or evidence is missing | [Test strategy](05_TEST_AND_EVIDENCE_STRATEGY.md) and [coding-process troubleshooting](09_TROUBLESHOOTING_THE_CODING_PROCESS.md) |
| SSH/VPN access lost or target needs reset | [RB05](runbooks/RB05_RECOVER_ACCESS_OR_RESET_TEST_BOX.md) |
| Secret or hostile content appeared in output | [RB09](runbooks/RB09_HANDLE_SECRETS_OR_UNTRUSTED_OUTPUT.md) |
| Operator steps do not work | [RB08](runbooks/RB08_DOCUMENTATION_WALKTHROUGH.md) |
| Unclear whether a candidate may be called ready | [Release/acceptance](07_RELEASE_AND_ACCEPTANCE.md) |

## 13. The first real action

After implementation is explicitly started, follow RB11 and BOOT-000 to establish the new root, then BOOT-001 for the documentation import. CP-001 follows its accepted integration. Begin with the package/contracts foundation before host-changing handlers; later phases implement the fresh installer and its own lifecycle/recovery. All product implementation and runtime qualification remain pending in this delivered package.

The first technical milestone is an installed narrow operation that validates input, creates a true read-only plan, performs one owned reversible fixture effect, records verified state, survives interruption and explains reconciliation. It establishes the engine and the human workflow before host changes become consequential.

## 14. Evidence status of this package

The v1.3 revision and input identities are recorded in [AUDIT_AND_REVISION_NOTES](AUDIT_AND_REVISION_NOTES.md). [PACKAGE_VALIDATION](PACKAGE_VALIDATION.md) records package checks and their limits. The standalone Start Here file matches this guide inside the ZIP. Distribution checksums detect changed bytes; they are not signatures or product qualification. Current tasks have fresh records; earlier repository results are not copied into them.
