# <Task ID>: <concrete change>

## Why

<Problem, affected operator behavior and consequence.>

## What changes

<Behavior, entrypoint, failure handling, docs and scope. Explain relevant trust/interface changes.>

## Traceability

- Task/card: <ID/path>
- Requirements/gates: <IDs and applicability>
- Base SHA / candidate SHA: <exact identities>
- Operation route / task authorization: <human-Git or direct GitHub; bounded task reference>
- Received context/delivery manifest: <references and verified receipt identity>
- Direct-route candidate parent/read-back and head drift reconciliation: <actual record / NOT_APPLICABLE for manual route>
- Source-edit checkout and actual build/test inputs: <local clean/dirty state or NOT_APPLICABLE for API-only source edits; separately record actual clean build inputs, generated inputs and exploratory-test limits>
- Architecture/ADR/contracts: <versions>
- Changed dependencies or support profile: <details or none>

## Validation

| Check | Actual status | Source/artifact/environment | Receipt / limitation |
|---|---|---|---|
| <test/review/walkthrough> | <PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE> | <identity/profile> | <reference> |

`NOT_APPLICABLE` requires the supported-profile/scope reason. A model-suggested result is not operator/test-run evidence.

Commands proposed but not executed: <list separately>. Do not mark checkboxes passed because code contains a test.

## Operator documentation and compatibility

<Guide/runbook/help/changelog changes; config/upgrade consequences; documentation verification.>

## Risks and recovery

<Concrete remaining risks, irreversible boundary, rollback/reconciliation limitations and cleanup.>

## Review and merge conditions

<Independent reviewer/receipt; open findings; exact targeted rechecks after changes or merge; no unresolved material blocker for acceptance. Record applicable human integration authorization. An AI review via the author's connected account is not independent human approval. Preserve actual merge SHA, but keep task blocked if required integration checks are pending or fail. Task merge does not confer release qualification.>

Opening/updating this PR may trigger automation; its applicable triggers, credentials and effects must already be covered by startup/task verification. Repository authorization is not authority to dispatch workflows or operate servers.
