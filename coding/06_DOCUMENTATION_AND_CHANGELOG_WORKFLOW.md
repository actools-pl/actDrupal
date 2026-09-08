# Documentation and changelog workflow

Package version: 1.3. This workflow implements the documentation duties in architecture v1.5.1 §§13.2–13.6, §18.5 and Annex UX. It does not claim that the software or its commands already exist.

## 1. What must exist

Maintain these document families in the software repository. Use one canonical home for each fact and link to it elsewhere.

| Family | Audience and contents | Source of truth |
|---|---|---|
| Accepted architecture and ADRs | Contributors: scope, trust boundaries, alternatives and recorded decisions | Accepted architecture; subsequent explicit ADRs |
| Contributor/coder guide | Human operating ordinary ChatGPT: bounded human-Git or direct-GitHub source delivery, review, test and handoff process | This package after repository adoption |
| Installed operator guide | Person installing or maintaining an identified supported release | Implemented grammar, generated support views and qualified runbooks |
| Runbooks | Person performing one operation, including failure handling | Tested installed operation and its receipts |
| Troubleshooting | Symptoms, safe observations, causes and bounded next actions | Real error contracts and reproduced failure cases |
| Release notes/changelog | Upgrader: user-visible changes, compatibility, security and schema-update impact | Accepted changes and exact release record |
| Capability/support views | What is implemented, qualified, deferred or unsupported | Canonical requirement/capability graph, with evidence links |
| Evidence index | Reviewer/operator: what ran, where, against which bytes and with what outcome | Actual sanitized receipts; never chat assurance |

The package's `PACKAGE_CHANGELOG.md` records changes to this workflow package. The software repository's `CHANGELOG.md` records installer changes. Do not put planned installer features under a released software version because this package describes them.

## 2. Documentation is part of a coding task

Every [task card](templates/TASK_CARD.md) names affected operator journeys and document IDs, or gives a concrete reason why none change. The coder includes those documentation changes in the same reviewable task change as the implementation, whether delivered by patch or the authorized direct-GitHub route. A separate documentation pass verifies the result; it is not a substitute for writing the documentation initially.

For each task:

1. Identify new or changed behavior, configuration, permissions, error outcomes and compatibility.
2. Update the corresponding guide, help source, schema-derived reference and runbook. Reuse shared defaults and vocabulary instead of copying them into many pages.
3. Mark example commands as **specified—not implemented**, **implemented—not verified for this release/profile**, or **verified for the identified release/profile**, as appropriate. These are documentation labels, not extra task states.
4. Add meaningful documentation checks: referenced command exists, supported flags match, examples parse under the schema, links resolve, and documented exit handling matches runtime. A passing help-text comparison alone does not qualify an operation.
5. Complete the independent code review and the relevant installed tests.
6. Run a documentation walkthrough at the appropriate milestone. Record the operator, exact package/source identity, environment, deviations and outcome.
7. Update `records/DOCUMENTATION_REGISTER.csv`, the task/evidence records and the software changelog entry. Do not fabricate a release date or runtime verification date.

## 3. Writing rules

- Begin with the outcome, prerequisites and disruption. Explain what an operator should observe before showing the next action.
- Separate normal procedure, stop conditions and recovery branches. A failed command is not permission to proceed through the next numbered step.
- State the required identity and privileges; distinguish laptop, devbox, release-test server and independent backup/monitor environment.
- Use placeholders that are unmistakably placeholders. Never include real credentials, private keys, tokens, signed access URLs, personal data or live customer data.
- Do not invent convenience commands or flags. Architecture v1.5.1 §18.5 owns the accepted grammar; real help/handlers and compatibility tests establish implementation. Earlier illustrative commands do not override it.
- Do not turn arbitrary logs, remote error text or user-controlled URLs into trusted next actions. Guidance comes from reviewed owned mappings, with source text visibly attributed.
- Describe expected output semantically. Avoid brittle whole-screen screenshots as the only proof. Show how to find the operation ID and inspect an interrupted operation using the qualified interface.
- Distinguish observed success, stale/unknown evidence, report-production failure and actual operation failure. Failure to display an operation result must not instruct a blind retry of a completed effect.
- Preserve audit/doctor status, severity, coverage and policy decisions across explanations. Do not explain every nonzero exit as the same error.
- Document secret *references and handling*, never secret values. Diagnostic material must be bounded and redacted before sharing with chat or GitHub.
- Include accessible plain-text/Markdown alternatives. First-release static HTML is private, inert, unprivileged output; a persistent dashboard, terminal menu system and browser action buttons remain deferred.
- Do not claim production support for conditional capabilities on the basis of a task merge. Labels derive from the canonical graph and evidence.

## 4. When a document needs re-verification

| Change | Required reconsideration |
|---|---|
| Command, schema, defaults or exit contract | Examples, help, automation examples, error handling and compatibility fixtures, including directly affected existing consumers |
| Privilege, paths, ownership or secrets | Prerequisites, identity, disclosure rules, stop/cleanup procedure |
| Plan/action/effect or interruption semantics | Plan review, operation inspection, retry/reconciliation and recovery branches |
| Image, package, installation layout or dependencies | Clean installed walkthrough and supported profile references |
| Backup, storage, credentials or retained readers | Recovery-set and restore runbooks; invalidate affected recovery proof |
| Output/rendering | Terminal and HTML behavior, accessibility, privacy, output budgets and publication errors |
| Security-sensitive dependency patch | Affected behavior and compatibility; no blanket assumption that a small version change is harmless |
| Repository route, connector capabilities, automation triggers or required checks | Startup/read-before-write instructions, authorization bounds, actual check identities, failed/uncertain operation handling and human-Git fallback; do not claim old observations remain current |
| Editorial correction only | Focused documentation review; repeat runtime steps only if their meaning changed |

Record a document as needing re-verification rather than leaving an old successful receipt attached without qualification. The unchanged portions can retain their traceable evidence. When a shared contract/helper changes, the task and documentation record name its affected existing consumers and their meaningful compatibility/integration checks. A producer schema test or matching help text cannot establish that those consumers still work. If a consumer has not yet been implemented, carry its explicit integration obligation into its first task and keep its documentation labelled accordingly.

Recovery documentation distinguishes the early CP-035 fresh-host recovery-path rehearsal from CP-047/050 qualification of the complete outage-start detection, delivery, response and restore timeline. Retain actual timing origins and unmeasured intervals; never label restore-only duration as the complete four-hour RTO. Likewise, describe Cloudflare as optional to enable while preserving its accepted first-release implementation/qualification obligation unless the user authorizes a scope revision.

## 5. Human walkthrough

Use [RB08](runbooks/RB08_DOCUMENTATION_WALKTHROUGH.md). First-release UX-T20 qualification requires at least one reviewer who did not implement the tested flow and has the expected Linux administration background. If the same person performs an earlier rehearsal, record that limitation, start from the written procedure alone and obtain a fresh review of the observed deviations. That preliminary rehearsal does not close the required independent walkthrough.

Every necessary off-document command, assumption or repair is recorded. Decide whether it is an installer defect, documentation defect, unsupported environment or test mistake. Correct the owner and repeat the affected branch. Do not teach the tester a hidden workaround and then record the original runbook as passed.

## 6. Changelog procedure

Use [CHANGELOG_ENTRY](templates/CHANGELOG_ENTRY.md). During development, collect entries under `Unreleased`, each tied to a task/PR and source change. At release preparation, consolidate them into clear user-facing notes:

- Added, changed, fixed and removed behavior.
- Security-relevant behavior with disclosure appropriate to the release process; sensitive exploit detail belongs in a restricted issue until handled.
- Configuration, schema, reader/writer and upgrade implications.
- Known limitations and genuinely unsupported/deferred capabilities.
- Operator action, if needed, with a link to the qualified runbook.

Avoid advertising implementation intentions as completed features. Avoid “various improvements,” unsupported performance claims and “production ready” without a support profile and release evidence. Record unreleased work separately from released behavior. Coding-package and installer versions are separate identities.

For new-repository startup and connected GitHub work, maintain one current observation/operation record linked from the handoff. Record actual bootstrap and subsequent task identities; historical reference observations are not live startup evidence. Use [RB11](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) and [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md). A connector commit is source delivery, and a CI result belongs to its real tested subject/runner; neither is an installed walkthrough receipt.

## 7. Adoption checklist

Before the first installed slice: assign document owners, seed the register, create an operator-guide skeleton, link every executable test command to its actual source, and close documentation review for that slice. Continue incrementally through every active work package. WP25 closes the release documentation; it does not postpone writing until the end.

Related: [coder start guide](00_START_HERE_CODER_DOCUMENTATION.md), [release acceptance](07_RELEASE_AND_ACCEPTANCE.md), [documentation-review prompt](prompts/04_DOCUMENTATION_REVIEWER.md).
