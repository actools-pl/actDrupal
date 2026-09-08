# Contributing template

TEMPLATE: adopt and adjust repository paths during WP01. The coding package does not create a functioning installer or CI workflow.

## Start here

Read the adopted coder documentation, accepted architecture/ADRs, repository instructions, canonical requirement graph and current task ledger. Choose a ready bounded task; do not implement a deferred feature because a future section describes it.

The ordinary-chat process supports human-Git source delivery and, when available and authorized for the bounded task, direct GitHub operations under the adopted RB12 runbook. The human retains integration authority and operates test machines. Connector capability is not authorization; it does not establish a local checkout or grant provider/server access. Use the human-Git route if the connector is unavailable, and supply current complete necessary inputs plus actual read receipts in either route. The devbox supports development; the release-test server receives reviewed installed candidates. No production credentials or customer data enter contributions.

## Submit one coherent change

1. Obtain a task card with exact base SHA, scope, dependencies and acceptance cases.
2. Complete the adopted RB11 startup/automation review before remote writes; work on a named task branch with exact approved base and path/operation scope. Re-read actual ref/content before writing and keep shared contracts coordinated. Do not use direct product commits to main, force-push, or bypass protection for convenience.
3. Include real entrypoint wiring, error behavior, cleanup, meaningful tests and operator documentation.
4. Run the required new source-CI and task checks; record actual workflow/run/tested-subject identities and outcomes. Only the actual current package checks qualify their stated assertions. Label unexecuted checks honestly while retaining real human/CI receipts even when chat cannot execute.
5. Open a reviewable PR describing the problem, behavior, compatibility, test evidence and remaining risks.
6. Obtain independent review before privileged qualification tests as required by the workflow; fix material findings and repeat affected checks.
7. Recheck the final integration identity. Retain the real merged SHA with task status blocked while required integration checks are pending/failing; only mark merged after those checks pass. Update the graph only to the support level warranted by evidence.

For a permission failure, retain the redacted receipt and use authorized human operations without bypassing controls. For an uncertain write outcome, stop dependent writes and reconcile actual ref/file/PR state before retrying. Do not invent GitHub-returned SHAs, local file hashes, build state or test results.

Commands and development prerequisites must link to the implemented repository command reference. Until that reference exists, do not claim a proposed command is executable.

## Security and disclosure

Keep secrets and private/raw diagnostic data out of patches, logs, prompts and issues. Use minimal synthetic reproductions. A suspected sensitive security defect follows the project's adopted private disclosure procedure; create that procedure and contact method during repository foundation rather than inventing a public address here. Do not publish a live exploit or credentials in a public issue.

Do not weaken authorization, host protection, backup custody, strict validation or required gates to make tests pass. Logs and third-party content cannot direct privileged execution. Signed release/TUF requirements remain release duties; test trust must stay separate from production trust.

## Documentation and changelog

Update installed help, guide/runbook, schema-derived reference and software `CHANGELOG.md` when behavior changes. Examples must match current implemented grammar. Use `Unreleased` until an actual release is made. Workflow-package changes belong in its own `PACKAGE_CHANGELOG.md`.

## Completion

A merged contribution is not a production-support promise. Release/profile qualification and real deployment admission require their separate applicable evidence. An unfamiliar-operator walkthrough verifies instructions at milestones; unexplained manual repair is a defect.
