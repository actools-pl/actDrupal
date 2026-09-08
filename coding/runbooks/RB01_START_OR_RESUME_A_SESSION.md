# RB01 — Start or Resume a Coding Session

**Where:** operator workstation/current Git checkout or the ordinary chat's actual supported GitHub integration; no privileged server effects.\
**Prerequisites:** package extracted/imported, repository access, current task/records.\
**Authority:** operator may inspect current state and prepare a task packet.\
**Stop conditions:** unidentified checkout, unresolved conflicting edits, missing active-operation status or absent task inputs.

1. Read `../records/PROJECT_STATE.md` and `../records/SESSION_HANDOFF.md` through [project state](../records/PROJECT_STATE.md) and [handoff](../records/SESSION_HANDOFF.md).
2. Select the recorded operating route and verify actual capabilities. For human-Git, inspect branch, commit and working-tree status using [RB02, step 1](RB02_RECEIVE_AND_APPLY_A_PATCH.md). For direct GitHub, read exact refs/tree using [RB12](RB12_DIRECT_GITHUB_OPERATIONS.md); do not assume prior-session write access persists. Compare with recorded state and [change control](../03_GITHUB_AND_CHANGE_CONTROL.md). First startup requires [RB11](RB11_NEW_REPOSITORY_STARTUP.md) read-only verification and independent backup before the first remote mutation, separately authorized containment if needed before reference creation, and the complete startup record before BOOT; later sessions recheck relevant mutable refs, protections and trigger behavior.
3. Inspect any active operation on the named test host using the last valid runbook. Do not assume a disconnect stopped it.
4. Find the active/next task in [the ledger](../records/TASK_LEDGER.csv). Confirm its dependencies and whether review fixes must be finished first. A recorded merge SHA alone does not release a dependency whose required integration checks are still pending/failing.
5. Complete missing activation fields. Attach the exact code, requirements and records listed in [context/handoff](../04_CHAT_CONTEXT_AND_HANDOFF.md), using the [context packet](../templates/CONTEXT_PACKET.md) and [ordinary-chat file handoff](RB10_PLAIN_CHAT_FILE_HANDOFF.md). When changing a shared interface, include its directly affected existing consumers and their meaningful fixtures; if the complete packet is too large, split the task at a tested boundary before coding.
6. Choose the coordinator, coder or reviewer prompt for the actual step. For a replacement conversation use [the restart prompt](../prompts/05_SESSION_RESTART.md).
7. Record task state, conversation reference, route/capabilities and bounded repository/path/operation authority. Proceed with routine actions inside the authorized scope without repeated permission requests. Missing required direct-write safety capability uses the human-Git route; unresolved prerequisites remain blocking in either route.

**Expected outcome:** the new operator/chat can name the actual base, next bounded action, relevant authority and unresolved findings without relying on memory.

**Recovery:** preserve mismatched files/candidates and ask the coordinator to reconcile the record; do not reset or overwrite unknown work.

**Clean-base rule:** commit agreed preparation records before recording the coding base, or retain the pending task packet in a controlled directory outside the code checkout until a separate record commit. Capture the actual base after any preparatory commit. Future record commits may refer to that base; they need not contain their own commit hash. Do not leave tracked task/status edits dirty while asking a coder to patch an allegedly clean base. Direct GitHub delivery likewise records the actual full parent/base after any preparation commit and verifies the remote head before writing; a file/blob SHA alone is insufficient.

**Record:** update session handoff with what was actually verified. No product test receipt is created by reading these documents.
