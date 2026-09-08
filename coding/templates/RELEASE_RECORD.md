# Release record — <candidate/version>

Template only. A completed record does not itself publish a release or admit production.

| Field | Value |
|---|---|
| Record ID / recorded UTC / owner | <...> |
| Decision | <candidate under test / withheld / qualified for named profile / released> |
| Exact source commit / final merge check | <actual SHA / receipt; source delivery route does not establish a build> |
| Required new source-CI execution | <workflow/check/run identities, actual tested subject and conclusions; only current applicable checks counted> |
| Build process and immutable inputs | <references; clean source/build receipt and declared generated inputs> |
| Post-merge integration outcome / blockers | <actual merged SHA, checks, failed receipts and corrective tasks; task blocked until required checks pass> |
| Package and image digests | <actual digests and verified transfer/install receipt> |
| Publication identity / immutable reference | <pending, or published artifact identity; distinguish from earlier qualification> |
| Release manifest / contract versions | <references> |
| Trust bootstrap / signatures / TUF metadata | <references; no private material> |
| Signing context | <development-only isolated trust / qualified release trust> |
| Platform/profile / selected capabilities | <finite supported matrix> |
| Supported upgrade/import and reader/writer edges | <explicit edges and evidence> |
| Dependency/license/SBOM records | <references> |

## Required qualification matrix

| Gate/case | Applicability and reason | Exact artifact/profile | Result | Receipt / remaining limitation |
|---|---|---|---|---|
| <ID> | <required / conditional selected / not applicable with reason> | <identity> | <PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE> | <reference> |

Use the evidence labels exactly as shown; `NOT_APPLICABLE` requires the recorded supported-profile/scope reason. Keep these results separate from the release decision and task lifecycle.

Include clean install, upgrade/import if supported, negative/interruption cases, external host checks, ordinary Drupal workflows, applicable UX security/accessibility and independent recovery/monitor evidence. Do not equate planned tests with receipts.

## Recovery and retention

<Measured RPO/RTO boundaries, eligible complete sets, retained readers/artifacts/trust and key references, rehearsal date/profile, independent custody, limitations, cleanup and resource budgets. No key material.>

## Documentation and changelog

<Packaged guide/runbook versions, unfamiliar-operator walkthrough receipts, examples/help validation and release notes.>

## Findings, exceptions and unsupported areas

<Open finding IDs, dispositions, affected claims, scope/expiry/authority of any permitted exception. Required controls are not weakened by this template. List conditional/deferred capabilities truthfully.>

## Decision and handover

<Human/integrator decision, date, approved profile, publication/deployment still pending or actual receipt, operator actions and location of retained redacted evidence. Preserve a failed post-merge check and block affected release claims until corrected. Record final post-merge bookkeeping through a reviewed follow-up records change; its commit is distinct from the tested subject. Production admission is separate and current-context dependent.>
