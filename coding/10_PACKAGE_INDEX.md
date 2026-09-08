# Package index — v1.3

Canonical repository: https://github.com/actools-pl/actDrupal. Active Architecture v1.5.1 supports fresh installations only. Start at [00_START_HERE_CODER_DOCUMENTATION.md](00_START_HERE_CODER_DOCUMENTATION.md).

There are 53 recorded task IDs: 51 planned active tasks, including BOOT-000 and BOOT-001, and two cancelled migration identifiers. The roadmap preserves remaining implementation owners and evidence gates. Later active task cards are prepared just in time; cancellation cards cannot be activated.

Sequence: RB11 and BOOT-000 establish the new root; BOOT-001 imports this package; CP-001 starts the minimal Python package/CI; the roadmap then implements the contracts, fresh installer, native lifecycle and qualification.

## Main guides

| File | Purpose |
|---|---|
| [00_START_HERE_CODER_DOCUMENTATION.md](00_START_HERE_CODER_DOCUMENTATION.md) | Coder Documentation — Start Here |
| [01_WORKFLOW_AND_DECISIONS.md](01_WORKFLOW_AND_DECISIONS.md) | Agreed Workflow and Decision Authority |
| [02_IMPLEMENTATION_ROADMAP.md](02_IMPLEMENTATION_ROADMAP.md) | 02 — Implementation roadmap and task activation |
| [03_GITHUB_AND_CHANGE_CONTROL.md](03_GITHUB_AND_CHANGE_CONTROL.md) | GitHub and change control |
| [04_CHAT_CONTEXT_AND_HANDOFF.md](04_CHAT_CONTEXT_AND_HANDOFF.md) | Chat Context, Task Packets and Handoffs |
| [05_TEST_AND_EVIDENCE_STRATEGY.md](05_TEST_AND_EVIDENCE_STRATEGY.md) | Test and evidence strategy |
| [06_DOCUMENTATION_AND_CHANGELOG_WORKFLOW.md](06_DOCUMENTATION_AND_CHANGELOG_WORKFLOW.md) | Documentation and changelog workflow |
| [07_RELEASE_AND_ACCEPTANCE.md](07_RELEASE_AND_ACCEPTANCE.md) | Release and acceptance workflow |
| [08_SECURITY_AND_SCOPE_RULES.md](08_SECURITY_AND_SCOPE_RULES.md) | Security and Scope Rules for Coding Sessions |
| [09_TROUBLESHOOTING_THE_CODING_PROCESS.md](09_TROUBLESHOOTING_THE_CODING_PROCESS.md) | Troubleshooting the Coding Process |
| [10_PACKAGE_INDEX.md](10_PACKAGE_INDEX.md) | Package index |
| [AUDIT_AND_REVISION_NOTES.md](AUDIT_AND_REVISION_NOTES.md) | Audit and revision notes — v1.3 |
| [PACKAGE_CHANGELOG.md](PACKAGE_CHANGELOG.md) | Coding package changelog |
| [PACKAGE_VALIDATION.md](PACKAGE_VALIDATION.md) | Package validation record |
| [README.md](README.md) | Actools Coding Package v1.3 |
| [SHA256SUMS](SHA256SUMS) | Hashes of every other distribution file; excludes itself |

## Active specification

| File | Purpose |
|---|---|
| [Actools_Drupal_Community_Rewrite_Architecture_Implementation_v1.5.1.md](baseline/Actools_Drupal_Community_Rewrite_Architecture_Implementation_v1.5.1.md) | Actools Drupal Community: fresh-install architecture and implementation report |
| [SOURCE_RECORD.md](baseline/SOURCE_RECORD.md) | Active baseline and provenance |

## Chat role prompts

| File | Purpose |
|---|---|
| [01_COORDINATOR.md](prompts/01_COORDINATOR.md) | Coordinator prompt |
| [02_CODER.md](prompts/02_CODER.md) | Coder prompt |
| [03_INDEPENDENT_REVIEWER.md](prompts/03_INDEPENDENT_REVIEWER.md) | Independent reviewer prompt |
| [04_DOCUMENTATION_REVIEWER.md](prompts/04_DOCUMENTATION_REVIEWER.md) | Documentation reviewer prompt |
| [05_SESSION_RESTART.md](prompts/05_SESSION_RESTART.md) | Session restart prompt |

## Operator process runbooks

| File | Purpose |
|---|---|
| [RB01_START_OR_RESUME_A_SESSION.md](runbooks/RB01_START_OR_RESUME_A_SESSION.md) | RB01 — Start or Resume a Coding Session |
| [RB02_RECEIVE_AND_APPLY_A_PATCH.md](runbooks/RB02_RECEIVE_AND_APPLY_A_PATCH.md) | RB02 — Receive and apply a coding patch |
| [RB03_TEST_ON_DEVBOX.md](runbooks/RB03_TEST_ON_DEVBOX.md) | RB03 — Test a candidate on the devbox |
| [RB04_QUALIFY_ON_RELEASE_TEST.md](runbooks/RB04_QUALIFY_ON_RELEASE_TEST.md) | RB04 — Qualify a candidate on the release-test server |
| [RB05_RECOVER_ACCESS_OR_RESET_TEST_BOX.md](runbooks/RB05_RECOVER_ACCESS_OR_RESET_TEST_BOX.md) | RB05 — Recover access or reset a test box |
| [RB06_CLOSE_TASK_AND_HANDOFF.md](runbooks/RB06_CLOSE_TASK_AND_HANDOFF.md) | RB06 — Close a task and hand off without relying on memory |
| [RB07_RELEASE_CANDIDATE_AND_REHEARSAL.md](runbooks/RB07_RELEASE_CANDIDATE_AND_REHEARSAL.md) | RB07 — Release candidate installation and rehearsal |
| [RB08_DOCUMENTATION_WALKTHROUGH.md](runbooks/RB08_DOCUMENTATION_WALKTHROUGH.md) | RB08 — Operator documentation walkthrough |
| [RB09_HANDLE_SECRETS_OR_UNTRUSTED_OUTPUT.md](runbooks/RB09_HANDLE_SECRETS_OR_UNTRUSTED_OUTPUT.md) | RB09 — Handle Secrets or Untrusted Output |
| [RB10_PLAIN_CHAT_FILE_HANDOFF.md](runbooks/RB10_PLAIN_CHAT_FILE_HANDOFF.md) | RB10 — Files in and out of an ordinary chat |
| [RB11_NEW_REPOSITORY_STARTUP.md](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) | RB11 — Start the new actDrupal repository |
| [RB12_DIRECT_GITHUB_OPERATIONS.md](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) | RB12 — Bounded direct GitHub operations from an ordinary chat |

## Prepared task cards

| File | Purpose |
|---|---|
| [BOOT-000.md](tasks/BOOT-000.md) | BOOT-000 — Establish the independent root commit |
| [BOOT-001.md](tasks/BOOT-001.md) | BOOT-001 — Import the coding workflow into actDrupal |
| [CP-001.md](tasks/CP-001.md) | CP-001 — Package skeleton and source CI |
| [CP-002.md](tasks/CP-002.md) | CP-002 — Strict configuration parser and canonical default resolution |
| [CP-003.md](tasks/CP-003.md) | CP-003 — Canonical requirement graph and operation/result contracts |
| [CP-004.md](tasks/CP-004.md) | CP-004 — Owned filesystem primitives and honest publication |
| [CP-005.md](tasks/CP-005.md) | CP-005 — Fixed subprocess context and secret-safe process handoff |
| [CP-006.md](tasks/CP-006.md) | CP-006 — Protected operation journal and crash-state fixtures |
| [CP-038.md](tasks/CP-038.md) | CP-038 — Cancelled scope record |
| [CP-039.md](tasks/CP-039.md) | CP-039 — Cancelled scope record |

## Project records

| File | Purpose |
|---|---|
| [DECISION_LOG.md](records/DECISION_LOG.md) | Decision log |
| [DOCUMENTATION_REGISTER.csv](records/DOCUMENTATION_REGISTER.csv) | Structured project record; retain headers and identifiers |
| [ENVIRONMENT_REGISTER.example.md](records/ENVIRONMENT_REGISTER.example.md) | Environment register — example to complete privately |
| [PROJECT_STATE.md](records/PROJECT_STATE.md) | Project state |
| [RELEASE_REGISTER.csv](records/RELEASE_REGISTER.csv) | Structured project record; retain headers and identifiers |
| [REVIEW_LOG.csv](records/REVIEW_LOG.csv) | Structured project record; retain headers and identifiers |
| [SESSION_HANDOFF.md](records/SESSION_HANDOFF.md) | Session handoff |
| [TASK_LEDGER.csv](records/TASK_LEDGER.csv) | Structured project record; retain headers and identifiers |
| [TEST_EVIDENCE_INDEX.csv](records/TEST_EVIDENCE_INDEX.csv) | Structured project record; retain headers and identifiers |

## Reusable record templates

| File | Purpose |
|---|---|
| [ADR.md](templates/ADR.md) | ADR-____ — <one material decision> |
| [CHANGELOG_ENTRY.md](templates/CHANGELOG_ENTRY.md) | Software changelog entry template |
| [CONTEXT_PACKET.md](templates/CONTEXT_PACKET.md) | Context packet — <task ID> / <packet revision> |
| [DELIVERY_MANIFEST.md](templates/DELIVERY_MANIFEST.md) | Delivery manifest — <task ID> / <delivery revision> |
| [HANDOFF.md](templates/HANDOFF.md) | Session handoff — <task ID> |
| [PR_DESCRIPTION.md](templates/PR_DESCRIPTION.md) | <Task ID>: <concrete change> |
| [RELEASE_RECORD.md](templates/RELEASE_RECORD.md) | Release record — <candidate/version> |
| [REVIEW_RECORD.md](templates/REVIEW_RECORD.md) | Review record — REPLACE_REVIEW_ID |
| [RUNBOOK.md](templates/RUNBOOK.md) | RB-____ — <one operational outcome> |
| [TASK_CARD.md](templates/TASK_CARD.md) | TASK-____ — <one bounded outcome> |
| [TEST_PLAN.md](templates/TEST_PLAN.md) | Test plan — REPLACE_TASK_ID |
| [TEST_RECEIPT.md](templates/TEST_RECEIPT.md) | Test receipt — REPLACE_RECEIPT_ID |

## Repository adoption and bootstrap templates

| File | Purpose |
|---|---|
| [AGENTS.template.md](repository_templates/AGENTS.template.md) | Repository instructions template for Actools |
| [CHANGELOG.template.md](repository_templates/CHANGELOG.template.md) | Changelog |
| [CONTRIBUTING.template.md](repository_templates/CONTRIBUTING.template.md) | Contributing template |
| [README.bootstrap.md](repository_templates/README.bootstrap.md) | Actools Drupal Community |
| [gitattributes.bootstrap](repository_templates/gitattributes.bootstrap) | Reviewed seed template; map to exact root destination in RB11 |
| [gitignore.bootstrap](repository_templates/gitignore.bootstrap) | Reviewed seed template; map to exact root destination in RB11 |

## Read-only process helpers

| File | Purpose |
|---|---|
| [validate_workflow.py](tools/validate_workflow.py) | Standard-library read-only process check; no runtime/product qualification |
| [verify_package.py](tools/verify_package.py) | Standard-library read-only process check; no runtime/product qualification |

## Historical provenance only

| File | Purpose |
|---|---|
| [Architecture_v1.5_ORIGINAL_REFERENCE_ONLY.md](reference/Architecture_v1.5_ORIGINAL_REFERENCE_ONLY.md) | Exact original v1.5; historical, non-operative; not a coding dependency |
| [README.md](reference/README.md) | Historical reference — not implementation authority |

The complete SHA256SUMS inventory defines distribution contents. Only the two process helpers are executable source in this package; their Git mode is 100644. The archived original is preserved byte-for-byte and excluded from product artifacts. Current documentation and tests never treat its old repository or migration instructions as operative.
