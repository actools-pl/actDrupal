# TASK-____ — <one bounded outcome>

Template only. Complete every required input/activation field before declaring the task ready. Future completion fields (candidate, review, test, merge and handoff outcomes) remain `UNSET` until actual evidence exists; do not invent them to activate a task. Keep this card in the adopted repository task location and link it from the ledger.

| Field | Value |
|---|---|
| State | planned |
| Parent WP / milestone / UX slice | <IDs and applicability> |
| Base branch / exact base SHA | <branch> / <full SHA> |
| Task branch | <branch> |
| Delivery route / actual chat capabilities | <human-Git / direct GitHub; verified operations and UTC> |
| Existing authorization / permitted operations | <reference, repository, branch, paths, effects; PR and merge authority explicit where applicable> |
| Local source-edit checkout / path and state | <actual path and clean/dirty state / NOT_APPLICABLE: API editing without local checkout> |
| Expected remote head / concurrency precondition | <observed SHA and supported mechanism / NOT_APPLICABLE for no direct mutation> |
| Startup verification / root-commit record | <RB11 reference; unresolved automation risk blocks remote writes> |
| Owner / reviewer / human test operator | <identities or roles> |
| Architecture / ADR versions | <v1.5.1 and relevant accepted ADRs> |
| Requirement, control and gate IDs | <canonical IDs; conditional cases labelled> |
| Dependencies | <accepted prerequisite tasks and interface versions> |
| Parent/child completion boundary | <parent task; this child outcome if split; remaining integration obligation> |
| Target environments | <CI/devbox/release-test/laptop/independent endpoint> |

## Outcome and scope

<Observable behavior needed, why it matters and exact boundary. Include entrypoint, error paths and cleanup. State what is deferred or not part of this task only where confusion is plausible.>

## Required current input files

| Path / source | Full-file revision or digest | Why needed |
|---|---|---|
| <current file/schema/test/ADR> | <identity> | <dependency> |

## Allowed changes and dependencies

| Path/component | Intended change | Interface consumers affected |
|---|---|---|
| <owned path> | <behavior> | <consumers or none> |

<Record a card revision for necessary additional files/interfaces; explain dependency impact. Escalate actual scope decisions, not routine choices within the authorized task. Direct GitHub capability does not expand the allowlist or authorize dispatch, infrastructure access or protection bypass. The same bounded scope applies to either route.>

For a shared schema, result contract or security-helper change, list directly affected existing consumers and the specific consumer compatibility/integration cases to run. Include their current interface code and meaningful fixtures in the input packet. If no consumer exists yet, record that explicitly and assign its integration obligation to the first consuming task; do not invent a passing consumer test. Changing additional consumers requires a recorded allowlist/card revision. Producer-only tests cannot establish compatibility of existing consumers.

## Contracts and security

- Input/output owners and exact schema versions: <...>
- Actor/authority and disclosure boundary: <...>
- Protected target identity, resources and effects: <...>
- Preconditions/postconditions: <...>
- Interruption, reconciliation, rollback and irreversible boundary: <...>
- Secrets, logging/redaction and retained evidence: <...>
- Finite time/size/resource budgets and origin of values: <...>
- Relevant UX-R/UX-T/UXS-C requirements: <... or justified not applicable>

## Acceptance cases

| Case ID | Requirement | Fixture and failure/success condition | Independent observable outcome | Environment |
|---|---|---|---|---|
| <ID> | <ID> | <case> | <assertion beyond helper return> | <target> |

## Test command plan — not an execution receipt

| Command/specification | Availability | Working directory / host | Authority and disruption | Expected outcome / evidence |
|---|---|---|---|---|
| <exact command or proposed test specification> | <implemented at named revision / created by this patch / proposed only / blocked> | <location> | <privilege, inputs, changes, cleanup> | <result and receipt fields> |

Source-only API editing does not require an invented local checkout; actual build/install/test steps do require their own identified clean inputs and execution environment. Do not mark a test passed in this table. Record actual outcomes in the test evidence system with source SHA, artifact digest, profile, command, timestamps, result and cleanup.

## Documentation and changelog

- Guide/help/reference/runbook IDs and paths: <...>
- Operator journey, error or compatibility changes: <...>
- Software changelog entry required: <yes and category / reason not needed>
- Installed walkthrough needed and reviewer: <...>

## Completion and handoff

- Candidate SHA / parent / full diff / artifact identity: <fill when real>
- Delivery receipt and operation reconciliation: <actual Git/GitHub results, full file inventory, pending/uncertain effects / none>
- Review receipt and open findings: <...>
- Test receipts and unexecuted limitations: <...>
- Direct-consumer integration receipts or named future integration obligation: <...>
- Document verification receipt: <...>
- Final merge SHA and required recheck: <fill after merge; task remains blocked until required integration checks pass>
- Capability/support effect supported by evidence: <none yet / exact graph update>

## Revisions

| Date UTC | Change | Reason / dependency impact | Recorded by |
|---|---|---|---|
| <date> | <revision> | <reason> | <identity> |
