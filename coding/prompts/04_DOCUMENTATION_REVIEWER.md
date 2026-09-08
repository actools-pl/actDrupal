# Documentation reviewer prompt

**Active scope:** repository `actools-pl/actDrupal`, architecture v1.5.1, fresh installations only. No existing-site discovery/import/cutover or legacy age reader. Use `main` integration after BOOT-000, then task branches; original v1.5 in `reference/` is historical only. CP-038/039 are cancelled and cannot block active tasks. Own-site backup, restore, disaster recovery and supported updates remain required.


Use a fresh ordinary chat at milestones and for meaningful operator-facing changes. Attach [CONTEXT_PACKET](../templates/CONTEXT_PACKET.md), current implemented grammar/help, relevant handlers, complete changed documents, document diff, runbook, release/profile identity and walkthrough receipts. Work, Projects and tool access are not required. Verified commit-pinned read access is optional; use supplied complete files when unavailable. Do not assume capability or source visibility from another chat.

```text
Review the attached Actools operator documentation as someone who must operate the system without remembered chat context. Do not implement software or assume commands work because they appear in the architecture. Remain read-only unless a distinct documentation correction/publication action is already authorized; an AI review through the author's connected account is not independent human approval.

Confirm document version, packet revision, task/release/profile, exact source/package identity, selected human-Git/direct route and supported capability set. For direct candidates inspect complete documents and actual diff at immutable commits, including required handlers; no downloaded patch or local source-edit checkout is required. Unresolved API truncation or missing files prevents a complete verdict. Return a short input receipt identifying each file/revision actually read, partly read, unavailable or not needed. Request material missing sections or handlers before a verdict; do not infer content from filenames or remembered examples. Compare each executable example against current implemented command grammar, handler behavior and test evidence. Distinguish specified-but-unimplemented commands, implemented-but-unverified examples and verified release/profile procedures. Never invent a convenience flag or missing recovery command.

For each runbook verify: purpose; correct machine/environment; release/profile; required identity/authority; prerequisites and independent recovery access; inputs/secret references; disruption; ordered exact steps; expected observations and exit handling; stop conditions; recovery/reconciliation branches; cleanup; evidence; escalation; and last verified identity/date.

Trace the likely human journey: discover task, choose supported path, review target/effects, execute, interpret progress/result, stop on ambiguity, recover safely and retain evidence. Ensure loss of a display connection cannot prompt a blind retry. For repository actions require inspection of remote state after uncertain writes, preservation of concurrent edits and truthful partially committed state. Verify route-specific fields allow justified NOT_APPLICABLE for API-only source edits while retaining actual clean build/test input requirements. Confirm PR creation/update and branch/tag writes account for applicable configured automation; repository access grants no server authority. Confirm administration/recovery remains usable while Drupal is unavailable. Check terminology and accessibility without relying on colour or screenshots.

Check private report sharing, redaction and local HTML safety statements. Reports must not promise fresh evidence, authenticated admission or backup recoverability they do not possess. Do not expose production secrets in examples or diagnostic collection.

Evaluate actual walkthrough receipts. Did an operator need an undocumented command or explanation? Record that as a specific defect. A simulated reading or model review alone is not an installed walkthrough. If the implementer performed the walkthrough, state the independence limit: this is a preliminary rehearsal and cannot close first-release UX-T20, which requires a reviewer who did not implement the tested flow and has the expected Linux administration background.

RETURN
1. Blocking ambiguities or unsafe instructions, with exact location and consequence.
2. Missing/mismatched commands, prerequisites, failure branches and support labels.
3. Minimal proposed corrections preserving scope.
4. Focused walkthrough/retest steps and required evidence.
5. Document-register updates and explicit remaining unverified items.
```
