# Audit and revision notes — v1.3

**Date:** 8 September 2026. **Authority:** user's new-repository request and explicit fresh-install-only/no-migrations decision. **Result:** documentation revision; no GitHub mutation, product implementation, server action or runtime qualification.

## Inputs and review coverage

The input ZIP contained 68 files; its 67 SHA256SUMS entries matched. The separate uploaded architecture matched the bundled v1.5 exactly. Source and ZIP digests are in [SOURCE_RECORD](baseline/SOURCE_RECORD.md). This revision inspected package inventory, references, startup/authority procedures, relevant architecture clauses, task dependencies, prompts, records and process helper code. It is not a fresh technical-security audit of every historical claim or a revalidation of all upstream product versions.

## Changes and consequences

| Subject | Change |
|---|---|
| Repository/startup | New actDrupal root; main integration; BOOT-000 explicit initial-commit exception before the normal PR cycle. Replace legacy preservation/ancestry gates with current identity/ref/automation checks. |
| Architecture authority | Active v1.5.1 with new hash; original v1.5 retained byte-for-byte under reference/ with no operative authority. Historical source citations are not falsely retargeted. |
| Product scope | Existing-site migration, discovery/import/cutover and legacy age import excluded; own-site recovery and supported updates retained. No live source-site inventory needed. |
| Contracts and requirements | Remove migration command/action vocabulary; revise C05/D13/F36/WP24. Preserve S4-RI20/FI40 IDs as excluded, never PASS. Add FRESH-T01–T04 scope cases with existing owners/gates. |
| Dependency graph | CP-038/039 cancelled without reuse. CP-040 depends on CP-037; CP-050 depends on CP-049/027. BOOT-001 depends on the accepted verified BOOT-000 root. |
| Records and prompts | Reset execution outcomes to unproduced; record current scope everywhere. No previous repo commit, receipt or authorization is asserted to be new-repo progress. Existing valid bounded task authorization is reused in actual execution. |
| Bootstrap/operator help | Three reviewed seed templates, Git Bash location guidance, actual SHA recording, first-root review/readback and current-control staging. No guessed required CI check names. |
| Integrity | Update baseline identities, read-only linter, documentation register, index and final manifest; scope/dependency/link/CSV checks and a local isolated bootstrap check are reported in PACKAGE_VALIDATION. |

## Retained responsibilities

Ordinary-chat human operation, two test boxes, complete deliveries, reviewer coverage, source/installed artifact identity, real evidence, complete outage-start recovery targets, effective security controls, source CI permissions, TUF/signing qualification, incremental docs and unfamiliar-operator acceptance remain. Source/record edits do not authorize servers, deployment or public installer publication. The new repository name does not rename the actools CLI or change the Python/Ansible/Compose/PHP architecture.

The user removed migration scope, not native restoration, internal schema evolution or trusted backup re-encryption after key compromise. The representative 80 GB qualification profile remains a controlled test requirement; a fresh production installation is not populated by importing a live site.

## Historical package lineage

V1.0 established the workflow; v1.1 refined ordinary-chat complete-file/evidence handling; v1.2 added bounded connected GitHub operations and an existing-repository startup model. V1.3 replaces the latter model and the migration inclusion while retaining the applicable workflow refinements. The supplied originals remain the evidence for historical details; this current audit record does not claim those earlier runs were repeated.
