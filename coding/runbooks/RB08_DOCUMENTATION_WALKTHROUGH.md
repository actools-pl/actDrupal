# RB08 — Operator documentation walkthrough

Status: process runbook ready for later adoption; installed product walkthrough not run.

| Field | Value |
|---|---|
| Owner | Documentation reviewer with integrator |
| Executor | For first-release UX-T20 qualification, a reviewer who did not implement the tested flow and has the expected Linux administration background |
| Target | Identified release-test candidate; laptop/independent endpoint where the procedure requires it |
| Authority | The exact authority required by the selected product runbook; reading docs grants none |
| Inputs | Packaged guide/runbook/help, exact source/package/profile, selected journey and evidence form |
| Disruption | Inherits the selected approved operation; reading-only review has no host effect |
| Acceptance basis | v1.5.1 §13.5–13.6 and Annex UX; UX-T20, plus UX-T21 only where an authorized scheduling journey is tested |
| Last actual walkthrough | Not run |

## 1. Prepare

Choose one bounded journey: clean setup, plan/apply, audit/doctor interpretation, update failure, backup interpretation, private restoration or another implemented operation. Confirm prerequisites, target identity, test data, rescue path and permitted effects before execution. Use the packaged documentation for the exact candidate, not an unpublished explanation from its author.

The reviewer prepares an observation record containing candidate/source digest, document versions, profile, tester identity, start/end UTC, prior familiarity, command availability and limitations. If the implementer is the only available tester, label the walkthrough as a preliminary rehearsal and retain a fresh documentation review separately. It cannot close the first-release independent UX-T20 requirement; a fresh model review alone does not replace the required installed operator exercise.

For a coder-workflow rehearsal, exercise the selected human-Git or direct-GitHub route separately and record actual connector capabilities, read receipts, write reconciliation and fallback behavior. A static documentation review can check these instructions without making repository changes; label it accordingly. Use [RB11](RB11_NEW_REPOSITORY_STARTUP.md) and [RB12](RB12_DIRECT_GITHUB_OPERATIONS.md) for the operational steps. A coder-process rehearsal does not replace installed product UX-T20 qualification or confer server/provider authority.

## 2. Walk through without hidden help

1. Find the appropriate procedure using the guide/index and installed help. Note misleading navigation or unsupported advertised options.
2. Establish the target, authority, inputs, prerequisites and disruption using the document alone.
3. Execute only implemented commands from the approved procedure. Record actual commands with secrets redacted; never copy raw private configuration into chat.
4. Compare expected observations, output/exit meaning and next steps with reality. Check plain output/non-TTY behavior where required by the journey.
5. Follow an applicable deliberately prepared failure branch when the test plan authorizes it. Confirm stop/reconciliation instructions do not cause blind retries or security weakening.
6. Complete cleanup and evidence preservation. State whether the intended outcome was achieved without off-document assistance.

If a necessary instruction is missing, pause the affected step and record the precise question. An author may explain it for diagnosis, but that assisted run does not qualify the original procedure. Correct the document or implementation and repeat the affected segment from a valid starting state.

## 3. What to record

| Observation | Required detail |
|---|---|
| Navigation difficulty | Page/heading, expected location and actual route |
| Ambiguous authority or target | Exact wording and plausible wrong action |
| Command mismatch | Documented command, implemented help/handler identity and actual result |
| Unexpected output | Redacted evidence, exit/status and missing explanation |
| Missing stop/recovery branch | Situation, safe state and consequence of continuing |
| Accessibility obstacle | Actual terminal/browser/assistive context and blocked task |
| Required manual repair | Every off-document step and whether it exposes code or documentation defect |
| Support misstatement | Claimed capability versus graph and actual evidence |

For static HTML, assess actual supported local browser behavior and printable/Markdown alternatives; an accessibility linter alone does not prove a person can use it. Never treat a pretty report as fresh health, authenticated admission or successful recovery. For recovery guidance, verify that the clock origin and every measured or assumed interval are visible: an early CP-035 recovery-path exercise cannot be labelled complete outage-start RTO qualification. CP-047/050 must cover detection and independent delivery as well as operator response, rebuild and verified recovery.

## 4. Stop, recover and clean up

Stop on ambiguous target, missing authority, unsupported command, unexpected destructive effect, exposed secret or missing recovery path. Preserve redacted evidence and use the already qualified target recovery procedure. Do not create an improvised root command to bridge a documentation gap.

Return the fixture/host to the planned state through implemented cleanup actions. Record any unresolved operation, maintenance latch or retained test object. Raise specific defects, assign owners and retain the original failed receipt alongside the corrected result.

## 5. Close the review

The documentation reviewer records: passed for named candidate/profile, changes required, blocked, or not run. Update the documentation register with actual receipt and invalidation conditions. This is a document/walkthrough outcome, not a new task state or a production-support decision.

Use the [documentation reviewer prompt](../prompts/04_DOCUMENTATION_REVIEWER.md) for a fresh review and [documentation workflow](../06_DOCUMENTATION_AND_CHANGELOG_WORKFLOW.md) for the required updates.
