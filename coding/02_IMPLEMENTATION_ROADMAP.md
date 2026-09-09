# 02 — Implementation roadmap and task activation

**Package version:** 1.3. **Baseline:** active revised Actools Drupal Community architecture v1.5.1; provenance is in `baseline/SOURCE_RECORD.md`. **State:** planning only; no code, branches, tests or releases have been produced by this package.

Start with [coder documentation](00_START_HERE_CODER_DOCUMENTATION.md). Follow [GitHub/change control](03_GITHUB_AND_CHANGE_CONTROL.md) for every candidate and [test/evidence strategy](05_TEST_AND_EVIDENCE_STRATEGY.md) for every claim. The task schedule is [TASK_LEDGER.csv](records/TASK_LEDGER.csv).

## 1. Authority and sequencing

This is the human execution breakdown of v1.5.1, not a replacement feature registry. Architecture §18.5 fixes dependency order; §§14–15 fix WP/gate ownership; Annex UX adds first-release UX requirements and security refinements. Once implemented, the canonical requirement graph owns capabilities and applicability. The ledger tracks task progress and links to that graph; it must not independently redefine support.

P01–P12 below are **coding-package milestone labels** organizing the accepted architecture for human execution. They do not rename architecture M0–M9. Work-package numbers identify owners and are not a linear implementation order. CP task numbers identify reviewable work, not a command interface.

Ordinary ChatGPT with the user's selected 5.6 sol Extra High setting supplies proposed code and documentation; reviewer-only selection and fallback follow [CPD-12](records/REVIEW_ROUTE_DECISION.md). The human retains GitHub integration authority and operates test hosts; bounded GitHub source operations may use the verified direct-chat route or the human-Git route. The mutable devbox is for development/destructive experiments; the separate release-test box receives reviewed candidate packages through the runbook. No assistant response is evidence that a command ran.

## 2. Start and readiness

Follow [RB11 new repository startup](runbooks/RB11_NEW_REPOSITORY_STARTUP.md). BOOT-000 establishes and verifies the independent root commit; BOOT-001 imports this package through its reviewed task branch; CP-001 begins the implementation skeleton and new source CI. There is no old-repository backup or ancestry prerequisite. Keep actual scope, operator and receipts in the startup record. BOOT-000/001 and CP-001–CP-006 have prepared cards. Later active cards are created just in time from `templates/TASK_CARD.md`; the ledger says UNSET until they exist. CP-038/039 have cancellation cards, not executable implementation instructions.

Active rows begin `planned`; CP-038/039 are `cancelled` by accepted scope. Unproduced commit/review/evidence fields remain `UNSET`. BOOT-000 has the explicit empty-base/direct-bootstrap exception described in its card. Before activating a task, the coordinator and human fill its exact base commit, affected-file inventory, executable interface versions, allowed changes, meaningful acceptance cases, test environment and documentation targets. Recheck dependency outcomes and the actual remote base; verify the working tree when using a local checkout. Direct source editing without a checkout uses the RB12 commit/tree receipt; actual build/test inputs still require their clean-state evidence. A milestone title or an accepted architecture decision is not an implementation result.

An `UNSET` **activation-critical** field blocks that task from coding/testing until it is supplied from repository/host evidence. It does not require repeated permission for work already authorized: ordinary code/contract choices can be resolved within scope and recorded. Ask the human only when an actual scope/authority decision or unavailable material input is required. Host IDs, live endpoints, secrets, branch base and test results must never be guessed.

Prepared task cards describe the smallest useful first slices. If a slice proves too large, split it into suffixed child tasks before coding, preserve the parent ID and dependencies, and update ledger/card/graph references in one change. Keep the 53 recorded parent identifiers (51 active planned tasks, two cancelled scope records): a parent closes only after its applicable child outcomes and their integration evidence are accepted. A child should have one bounded observable outcome whose required input files, complete changes and meaningful review fit the actual ordinary-chat file/context limits. Split at a tested contract boundary; do not omit surrounding code, failure paths or documentation merely to fit a chat. Do not quietly redefine completed acceptance outcomes or attach several unrelated task completions to one review.

## 3. Work that grows from the beginning

Every relevant task includes its real collector/result fixture, actionable errors, help and operator/runbook changes. CP-003 starts canonical evidence/coverage semantics; CP-011 adds actual host observations. P11 completes and reconciles these—it does not introduce the audit engine for the first time. Packaging starts at CP-001, and the first installed slice at CP-010 uses the actual intended installation layout. A local development artifact does not claim trusted public distribution.

Activated pre-release tasks, including CP-001/CP-010 and the CP-011–CP-016 installed host qualification, may use a reviewed development build from human-controlled exact source, transferred directly to the registered test target with source and artifact identities retained. Each task still requires its declared review, target/recovery checks, authority and effect boundaries; this does not authorize arbitrary privileged experiments or publication. This is a private development fixture, not a published installer, update channel or release candidate. It does not establish release authenticity or TUF qualification. Before **publishing any installable artifact**, even with test-only trust, complete the v1.5.1 release-engineering ADR and required bootstrap/verification path; see [release workflow](07_RELEASE_AND_ACCEPTANCE.md). Later CP-017/CP-037 extend and qualify release/runtime/update trust. This distinction prevents an early fixture test from either skipping publication controls or depending on the whole later release lifecycle.

Each card imports exact relevant controls and tests from the architecture. The summaries below name anchor IDs and sections; ranges such as “S2 controls” require selecting exact applicable IDs when the card is activated. This avoids making every host task responsible for every architecture test. Tests attributed to multiple tasks can reuse the same identified fixture and evidence when its validity conditions still hold. Passing a unit fixture never declares an entire G gate passed.

Documentation targets in the tables are required subjects, not claims that future documents exist. On activation, choose their exact repository paths and record those in the card and ledger. The documentation owner verifies commands against implemented help and supported handlers; no example may advertise an unsupported command.

## 4. Sequenced backlog

### P01 — Repository foundation

**Architecture mapping:** M0; WP01/WP25. Establish independent root history, import the workflow, then build the minimal development package and source checks.

**[BOOT-000](tasks/BOOT-000.md):** review and publish the new root seed under RB11, then verify its exact SHA. **[BOOT-001](tasks/BOOT-001.md):** import the complete package at `coding/` on `task/BOOT-001` from that root and merge into `main` after review/applicable checks. Neither task implements product code or changes a server.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| [CP-001](tasks/CP-001.md) — Repository/package skeleton and source CI | WP01 / WP25 · BOOT-001 | Build and install a development package from a clean checkout; version/help truthfully expose only implemented support. | G01/G09/G22; §18.5 slice 1; UX-R05/R06/R14; UX-0 | Contributor setup and first clean-checkout verification |

### P02 — Contracts and CLI skeleton

**Architecture mapping:** M0; WP02. Freeze the first executable contracts and support truth before handlers consume them.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| [CP-002](tasks/CP-002.md) — Strict configuration parser and canonical defaults | WP02 · CP-001 | Reject duplicate/unknown/ambiguous or oversized inputs; equivalent inputs resolve the same versioned defaults and canonical bytes. | G03/G09; §18.5 contract ownership; UX-T01/T02; UXS-C14 | Configuration format, validation failures and default provenance |
| [CP-003](tasks/CP-003.md) — Requirement graph and operation/result contract skeleton | WP02 / WP22 · CP-002 | Graph separates accepted scope from implementation; plan/result/evidence/release/journal/backup contracts have explicit owners and initial compatibility fixtures. | G03/G04/G09/G19; §7.8/§18.5; UX-R01/R03/R07; UXS-C04/C12 | Contract catalog, command output semantics and coverage interpretation |

### P03 — Safe implementation primitives

**Architecture mapping:** M0/M2; WP03. Make owned filesystem access, fixed execution and secret-safe output reusable and reviewable.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| [CP-004](tasks/CP-004.md) — Owned filesystem and honest atomic publication | WP03 · CP-003 | Traversal/links/special files/ownership races fail safely; pre-commit preservation and post-replacement uncertainty are distinguished. | G03/G07/G08; §7.7/§7.10; UX-T02/T13/T22; UXS-C10 | Owned paths, output destinations and publication-failure recovery |
| [CP-005](tasks/CP-005.md) — Fixed subprocess context and secret-safe handoff | WP03 · CP-004 | Untrusted values remain data; bounded child execution, redacted errors and authorized data-only handoff cannot inherit privileged authority. | G03/G07/G08; §7.1/§7.7; UX-T10/T14; UXS-C01/C02/C05/C06/C07 | Secret references, bounded commands and safe evidence collection |

### P04 — First complete installed operation

**Architecture mapping:** M0/M2; WP04 and bounded WP09. Prove a fixture operation from the final installation layout before any host-changing handler.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| [CP-006](tasks/CP-006.md) — Protected operation journal and crash-state fixtures | WP04 · CP-005 | SQLite DELETE/EXTRA and one protected writer verified; intent/state transitions survive qualified failures; read-only consumers cannot recover by writing. | G02/G04/G07; §7.4/§7.9/§18.5; UX-R04; UXS-02 | Operation states, journal troubleshooting and uncertainty |
| CP-007 — Resource locks and finite process/output deadlines | WP04 / WP09 · CP-006 | Conflicting operations serialize; expired ownership reconciles; stalled output cannot stop required durable bookkeeping or safety deadlines. | G02/G07/G18; §7.9; UX-T06/T07/T14; UXS-C03 | Lock contention, client disconnect and output-delivery failure |
| CP-008 — Read-only planner and guided init parity | WP09 / WP02 · CP-007 | Init writes only a requested valid non-secret artifact; plan writes no managed state/secrets/locks; exact review/expiry identity is retained. | G03/G04/G08; §18.5; UX-T01–04/T07/T19/T21; UXS-C04/C14 | Answer-file and interactive setup; reading a plan |
| CP-009 — Restricted executor for one owned reversible fixture | WP09 / WP04 · CP-008 | One fixed test handler validates authority and exact plan; interruption/reconcile cannot duplicate effects or silently rewrite plans. | G02/G04/G07/G18; §18.5 slice 4; UX-T03–06/T14; UXS-C04/C15 | Fixture apply, operation inspection and safe reconciliation |
| CP-010 — First installed vertical slice and independent review | WP09 / WP25 / WP22 · CP-009 | Final-layout development install completes plan/apply/interruption/reconcile/report fixture with actual package provenance. | G01/G02/G03/G04/G07/G09/G19; §13.6/§18.5; UX-1/UX-2 | First installed-slice runbook and evidence return |

### P05 — Linux foundation

**Architecture mapping:** M1/M2; WP05–WP09. Qualify access, firewall, update and confinement effects on real expendable targets.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-011 — Ubuntu read-only discovery and preflight collectors | WP05 / WP22 · CP-010 | Observe actual OS/image/kernel/repositories/users/listeners; unsupported inputs block host apply without probing by mutation. | G01/G04/G09/G19; §6/§18.5 slice 5; S2 host cases; UX-2 | Host prerequisites and interpreting preflight |
| CP-012 — SSH administrator transition and recovery access | WP06 / WP09 · CP-011 | Verified separate recovery path and fresh-session tests precede committing access changes; failure deliberately rolls back safely. | G05/G07/G08; §6.2/§18.5 slice 6; S2 access cases | SSH transition, lockout prevention and console recovery |
| CP-013 — WireGuard management lifecycle and revocation | WP06 / WP09 · CP-012 | Qualified peers, routing, revocation and VPN loss preserve declared management and rescue boundaries. | G05/G06/G07/G08; O01 required WireGuard; §6/§14.2 | VPN enrollment, removal and lost-client recovery |
| CP-014 — Continuous host and Docker firewall protection | WP07 / WP09 · CP-013 | External IPv4/IPv6 probes corroborate policy before exposure during reload/reboot/daemon startup; authorized recovery stays usable. | G05/G06/G07; RV13-02; RV13-T03/T04; §6.3/§6.5 | Firewall change/reboot test and recovery runbook |
| CP-015 — Packages updates confinement and filesystem baseline | WP08 / WP09 · CP-014 | Effective repository/patch/reboot ownership and denied-access controls match policy; exclusions produce patch debt. | G01/G05/G07/G08/G09/G19; §6.2/§6.5/§18.4; S2 controls | Maintenance windows, patch triage and confinement diagnosis |
| CP-016 — Single restart owner and complete host-handler qualification | WP04 / WP08 / WP09 · CP-015 | Restart ADR selects one owner with durable exhaustion/stop intent; actual host handlers pass access/reboot/interruption installed tests. | G02/G05/G06/G07/G18/G19; RV13-04; S5-BHT27/BHT28; UX-2 | Service recovery budgets, operator stop and host acceptance |

### P06 — Runtime foundation

**Architecture mapping:** M3; WP10/WP11. Generate pinned runtime generations with stable identities and real consumer activation.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-017 — Pinned release images templates and build trust | WP10 / WP25 · CP-016 | Trusted inputs, immutable identities and template/image manifests agree; build jobs have no production signing secrets. | G09/G22; §11/§18.6; UX-R14 | Build provenance, version matrix and release trust setup |
| CP-018 — Stable Compose resources and generation activation | WP10 / WP03 · CP-017 | Stable project/daemon/resource identity preserves data across paths/releases; consumers acknowledge actual activated bytes. | G02/G07/G08/G09/G18; RV13-01/RV13-03; RV13-T01/T02/T05/T06 | Container resource mapping, activation and failed reload |
| CP-019 — MariaDB lifecycle and scoped application privileges | WP11 · CP-018 | Pinned DB boots; app identity lacks administration powers; phase credentials and restoration/event inventory are explicit. | G07/G08/G09/G14/G15; §7.6/§8.2/§10.5 | Database roles, bootstrap and credential ownership |
| CP-020 — Optional Valkey roles memory and outage qualification | WP11 / WP22 · CP-019 | On/off profiles pass; only accepted cache bins use Valkey; generation metadata, eviction/timeouts and failure semantics qualify. | G08/G09/G10/G19/G20; §8.3; S3 cache controls | Cache enable/disable, pressure and outage diagnosis |
| CP-021 — Credential rotation and runtime consumer acknowledgement | WP11 / WP10 · CP-020 | Rotation verifies successor consumption before applicable predecessor revocation; interruption preserves known state and redaction. | G02/G07/G08/G18; RV13-01; §7.6/§7.10/§7.11 | Rotation, failed activation and application-secret recovery |

### P07 — Secure Drupal

**Architecture mapping:** M3; WP12/WP13. Qualify ordinary Drupal, protected administrative access, storage and accepted ingress controls.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-022 — Immutable Drupal settings services and FPM bundle | WP12 / WP10 · CP-021 | Pinned Drupal install boots with complete configuration; code/config/private paths and application identities remain protected. | G07/G08/G09/G10; §8.1/§8.2; S3 Drupal controls | Drupal installation, settings ownership and operational commands |
| CP-023 — Local public/private storage and authorized probes | WP13 / WP12 · CP-022 | Owned local writes/cleanup and public/private delivery pass; no application-object support claim appears. | G03/G07/G10/G14; §8.4/§8.5; C01 local-storage scope | Local file permissions, private downloads and storage probes |
| CP-024 — Drupal privileged VPN MFA and cache-order enforcement | WP12 / WP22 · CP-023 | Privileged workflows require VPN plus MFA including warm-cache/session/reset/API cases; editors and ordinary users keep permitted access. | G08/G10/G15/G18/G19; §8.6; RV13 cache-order refinement | Administrator/editor workflows, MFA recovery and access diagnosis |
| CP-025 — Ordinary image and cold-derivative resource bounds | WP12 / WP22 · CP-024 | Small-byte/high-pixel/malformed images fail within budgets while supported legitimate uploads and derivatives work. | G10/G19/G20; RV13-11; RV13-T21/T22; §8.5 | Supported image limits and rejected-upload troubleshooting |
| CP-026 — Direct Caddy ingress and accepted F10 limiter qualification | WP10 / WP12 / WP22 · CP-025 | TLS/ACME and real pre-PHP limits pass trust/aggregate/key-memory/metrics/reload tests with legitimate traffic positives. | G06/G09/G10/G20/G22; F10; §8.7/§18.8; RV13-13; RV13-T25/T26 | Direct ingress, certificate renewal and rate-limit operations |
| CP-027 — Optional standard Cloudflare profile qualification | WP10 / WP12 / WP22 · CP-026 | Implement and qualify the accepted optional standard profile and its disabled path; prove origin identity level, TLS/header/trust/rotation and authorized VPN paths. | G06/G09/G10/G21; RV13-12; RV13-T23/T24; §8.7/§18.6 | Optional proxy setup, identity claims and safe disable |

**Applicability:** F10 rate limiting is accepted in v1.5.1 and must qualify before public production. It is not a deferred UI feature. Cloudflare is optional for a deployment; v1.5.1 §18.3 C01 nevertheless includes implementation and qualification of exactly one initial standard proxy-to-Caddy mode, together with the disabled/direct mode. CP-027 therefore remains a first-release prerequisite. Qualify the enabled mode on an explicitly selected controlled test profile; do not enable it on unrelated deployments merely to finish a row. Unavailable test inputs leave that qualification blocked while other work continues. Removing this accepted mode from release scope requires a recorded user-authorized architecture scope revision; a task applicability label cannot make that decision. Direct Caddy remains the complete default.

### P08 — Backup capture

**Architecture mapping:** M4; WP14. Produce independent, complete, byte-consistent recovery sets with honest coverage and retention.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-028 — Staged database/files capture with byte proof | WP14 / WP04 · CP-026 | Fence every declared writer; same-size/mtime-preserved changes, renames and deletes produce one immutable boundary within measured budgets. | G02/G14/G19/G20; RV13-05; §10.2/§18.6 | Capture workflow, writer inventory and pause-budget failures |
| CP-029 — Independent repository custody and key-incident paths | WP14 / WP11 · CP-028 | Independent backup identity encrypts/commits; production lacks historical keys/deletion authority; master-key compromise uses new key domain. | G07/G08/G14/G15/G16; RV13-06; §10.8/§18.6 | Repository setup, recovery-key custody and compromise runbook |
| CP-030 — Complete-set catalog commit and recovery presentation | WP14 / WP02 / WP22 · CP-029 | Missing constituents, invalid identities or failed mandatory checks cannot commit; capture/commit/eligibility/restore proof stay distinct. | G14/G15/G19; §10.5; UX-T15; UXS-C13 | Backup listing, usable points and failed commit diagnosis |
| CP-031 — Cadence retention and deadline-driven retry | WP14 / WP23 · CP-030 | 30-minute attempts and configured retention preserve eligible history; failures trigger bounded retry before one-hour coverage loss. | G14/G16/G19/G20; RV13-09; §10.9/§18.4 | Schedules, coverage breaches, retention and retry escalation |
| CP-032 — Repository locks maintenance and historical verification | WP14 / WP23 · CP-031 | Pinned operation/lock matrix and finite verification horizon cover old-only data without hiding coverage loss or bypassing locks. | G14/G16/G19/G20; RV13-07/RV13-08; §10.9 | Check/prune authority, lock failures and historical-data sweep |

### P09 — Restore and recovery

**Architecture mapping:** M4; WP15/WP24. Restore privately and measure the whole recovery chain before destructive lifecycle acceptance.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-033 — Private restore and internal-writer suppression | WP15 / WP11 · CP-032 | Wrong key/site/corrupt data fails before promotion; isolated identity/egress and database-event suppression hold through import. | G07/G08/G15/G16; RV13-10; §7.11/§10.5/§10.7 | Private restore, event inventory and validation |
| CP-034 — Verified recovery promotion and revocation | WP15 / WP09 · CP-033 | Only verified target promotes; credentials/sessions/authority reconcile without repository keys entering production. | G02/G08/G15/G16/G18; §10.7/§10.8; S5-BHT19 | Promotion, fencing, revocation and failed handover |
| CP-035 — Measured fresh-host recovery-path exercise | WP15 / WP24 · CP-034 | Independent exercise proves complete fresh-host restore and measures acknowledged-change loss, operator/rebuild/validation time and the representative 80 GB profile; detection/delivery-inclusive G16 remains open until CP-047/050. | G14/G15/G16/G19/G20; §10.4/§10.10/§18.4; UX-T15/T20 | Disaster recovery, timeline, retained readers and rehearsal receipt |

**Recovery sequencing:** CP-035 is the required measured recovery-path proof before CP-036 destructive update/rollback acceptance. Record its actual timing origin, simulated detection/notification assumptions and all unmeasured intervals. It does not close the whole outage-start four-hour RTO while CP-045/046 monitoring and delivery are absent; a restore duration below four hours alone is insufficient. After those components exist, CP-047 measures the complete outage, detection, channel delivery, operator response, fresh-host bootstrap and verified application/files recovery chain. CP-050 verifies that proof applies to the exact release candidate/profile and repeats invalidated portions or the full exercise as required. Both the one-hour acknowledged-change-loss limit and four-hour outage-start limit remain unchanged; failure blocks their release claims rather than relaxing the targets.

**Environment limit:** two Hetzner boxes in one account do not prove independent backup custody/account-loss recovery. A laptop can develop and run controlled independent exercises while available. Production-grade independent monitoring/backup needs its separately qualified placement and authority. If unavailable, preserve the gap and finish other authorized work; do not simulate independence using containers on the target. The 80 GB combined profile, one-hour RPO and four-hour RTO are accepted requirements, not measured results.

### P10 — Supported updates

**Architecture mapping:** M6; WP21/WP24. Implement supported product/application updates over proven checkpoints. Existing-site migration is excluded.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-036 — Deployment updates and acknowledged-write-safe rollback | WP21 / WP10 · CP-035 | Verified recovery checkpoint precedes lifecycle tests; failed build/schema/readiness cannot erase writes or security lineage. | G02/G09/G18/G22; §11.2; S5-BHT20/BHT21; UX-3 | Update planning, rollback limits and failed update recovery |
| CP-037 — TUF management update and retained-reader compatibility | WP21 / WP25 · CP-036 | Pinned maintained verifier enforces trust/expiry/rollback and exact release identity; only qualified readers/upgrade edges advertised. | G09/G18/G22; §11.1/§11.3/§18.6 | Management update, offline recovery and support retirement |
| [CP-038](tasks/CP-038.md) — Cancelled: existing-site discovery | WP24 / WP22 · no dependency | Excluded by user in v1.5.1; no implementation or release prerequisite. | C05/D13 superseded; S4-RI20 excluded | Scope/cancellation record only |
| [CP-039](tasks/CP-039.md) — Cancelled: existing-site import/cutover | WP24 / WP15 / WP21 · no dependency | Excluded by user in v1.5.1; no implementation or release prerequisite. | C05/D13 superseded; S4-FI40 excluded | Scope/cancellation record only |

**First-release support:** lifecycle failure fixtures are still required, but do not advertise an upgrade from a nonexistent prior production release. The first public release supports fresh installation and qualified recovery of sites created by this installer. It has no existing-site importer or legacy age reader. Later releases advertise only actual tested source-to-target edges.

### P11 — Complete operational UX

**Architecture mapping:** M7; WP22/WP23. Close coverage, reporting, history and monitoring over the engine and collectors already built.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-040 — Audit graph and full applicability closure | WP22 / WP02 · CP-037 | Close full F/control/test mapping and both coverage denominators over existing incremental engine; no deferred item becomes implemented by appearance. | G09/G19/G21; §7.8/§12.1; UX-T08/T09/T19; UXS-C12/C15 | Audit scope, evidence gaps and capability support |
| CP-041 — Remaining audit/doctor collectors and explicit probe integration | WP22 · CP-040 | Close required AUD/DOC inventory with bounded effective observations; mutating/synthetic probes remain typed authorized actions. | G03/G04/G07/G19/G21; §12.1/Appendix C; UX-T21 | Doctor checks, explicit probes, offline and deep modes |
| CP-042 — Cross-format evaluator exit and delivery closure | WP22 / WP02 · CP-041 | Human/JSON/Markdown preserve failures, unknowns, severity, policy and exit precedence; report failures preserve actual operation truth. | G03/G08/G19; UX-T07/T08/T09/T12/T14; UXS-C05/C06/C07/C12/C15 | Command formats, automation exits and safe next actions |
| CP-043 — Private static HTML and accessibility qualification | WP22 / WP03 / WP25 · CP-042 | Unprivileged inert single-file rendering proves disclosure, browser/network, publication, bounded size, print/accessibility and stale-state behavior. | G03/G07/G08/G09/G19/G20; UX-T10–13/T17/T18/T22; UXS-C01/C02/C08–C12 | Private report export, limits, retention and accessibility |
| CP-044 — Core history drift and evidence lifecycle closure | WP23 / WP22 · CP-043 | History retains declared samples/receipts with honest gaps and invalidation; recovery dependencies outlive ordinary report cleanup. | G08/G14/G19/G20; §12.2/§18.4; UX-T12/T22 | History, drift, expiring evidence and cleanup |
| CP-045 — Independent HTTPS and authenticated heartbeat monitor | WP23 · CP-044 | External identity checks HTTPS/liveness with replay controls and checker-health limitations; production loss cannot suppress detection. | G16/G19/G21; C02; §18.4; UX-R10 | Monitor enrollment, missed heartbeat, maintenance and checker loss |
| CP-046 — Independent email and Telegram delivery qualification | WP23 / WP22 · CP-045 | Both destinations receive qualification messages; partial failures, throttling, expiry and retries remain independent and redacted. | G08/G16/G19/G21; §12.2/§18.4; UX-T16/T21 | Routing, notification probe, delivery failure and credential rotation |
| CP-047 — Integrated capacity and longer-running operational tests | WP22 / WP23 / WP24 · CP-046, CP-035 | Declared profile survives sustained legitimate/abuse load plus capture/maintenance; measure complete outage-start recovery, including CP-045/046 detection/delivery and operator response, against the one-hour RPO/four-hour RTO; record actual budgets and breaches. | G09/G14/G16/G19/G20/G21; §10.10/§15/§18.7; RV13 refinements | Capacity profile, test limitations and routine operations |

### P12 — Release qualification

**Architecture mapping:** M9; WP24/WP25. Prove the packaged candidate through clean installation and operator documentation, then prepare release readiness.

| Task | Owner / depends on | Acceptance outcome | Source/gate anchors | Documentation to update |
|---|---|---|---|---|
| CP-048 — Release artifact and finite support matrix closure | WP25 · CP-047, CP-037 | Signed/rebuildable artifacts bind manifest, notices, exact profile/versions/readers and qualified support; remaining gaps are explicit. | G01/G09/G22; §11.3/§18.6; UX-R14 | Release notes, SBOM/notices, support and upgrade matrix |
| CP-049 — Unfamiliar-operator walkthrough and documentation closure | WP25 / WP24 · CP-048 | Another operator follows packaged setup/failure/private-recovery guidance while Drupal is unavailable; undocumented steps become defects. | G01/G15/G16/G18/G19; UX-T20; S4-FI37; UX-5 | Complete operator guide, runbooks and troubleshooting acceptance |
| CP-050 — Clean release-test install upgrade and full acceptance matrix | WP24 / WP25 · CP-049, CP-027 | Reviewed candidate passes applicable profile gates on clean supported target, including accepted Cloudflare on/off qualification and current complete outage-start recovery proof; independent boundaries use real evidence or remain unqualified. | All applicable G01–G22; G11–G13/G17 deferred; UX-T01–22; §15 | Candidate qualification report and remaining limitations |
| CP-051 — Release readiness record and community handover | WP25 · CP-050 | Human-readable release decision cites reviewed commit, evidence, docs, limitations and custodians; publishing/deployment is a later explicit action. | G01/G09/G19/G22; §13.5/§18.7; UX-5 | Release changelog, maintainer handover and post-release workflow |

## 5. Milestone exit and review

A milestone closes when its activated applicable cards have accepted code review, meaningful test evidence for the actual candidate, updated operator/developer documentation, and no unresolved blocker for its claimed outcome. The human records remaining limitations. A dependency can advance using an exact accepted and integrated smaller slice whose required integration checks passed only when the dependent card identifies exactly which proven contract it relies on; it cannot assume all of the parent's WP is complete.

Use one active writer for shared interfaces. A schema, result contract or shared security-helper change identifies its directly affected existing consumers and exercises meaningful consumer-level compatibility or integration fixtures; producer-only tests cannot close that change. When a consumer does not yet exist, record that fact and carry its integration obligation into its first implementation card. After a relevant change, determine which evidence is invalidated and rerun only the affected checks plus required gates. The release-test server receives the reviewed package; changing it by manual workaround creates an installer/runbook defect to repair in source. Read-only investigation is allowed and recorded. Rebuild it at clean-install milestones instead of letting accumulated fixes become hidden prerequisites.

At P04 prove the complete fixture before host mutation. At P05 qualify rescue and ingress behavior before exposing real runtime services. At P09 prove recovery before destructive update acceptance. At P12 accept only named supported profiles with traceable evidence. No final release checklist can retrospectively excuse a missing early safety boundary.

## 6. Traceability and completion record

Every activated card records: exact WP owner; applicable F/control/UX-R/UX-T/UXS-C and G IDs; exact source sections; input contract versions; effects and authority; owned files; meaningful failure and positive cases; test environment; documentation targets; reviewer findings; exact reviewed candidate; evidence and merged commit.

The initial ledger contains 53 parent identifiers: BOOT-000, BOOT-001 and CP-001 through CP-051, including the two cancelled CP scope records. It is a starting work breakdown, not an estimate of 53 chat turns. Larger tasks can need multiple bounded review/fix cycles; one complex adapter may need extra child cards after its interfaces are known. No calendar or monetary estimate is implied.

The task ledger records acceptance; `CHANGELOG.md` explains user-facing changes; release notes describe supported behavior and known limits. A changed commit does not silently inherit an earlier PASS. A merged patch is not automatically a released artifact, and a released artifact is not automatically production-qualified for every machine/profile.

## 7. Deferred work stays outside this backlog

WP16 PITR and WP17–WP20 active document queues/workers/converters/scaling remain deferred. Reserve only the generic future contract boundary already required by v1.5. Application object storage, managed previews/staging, general monitoring dashboards, runtime AI, tenancy and HA remain outside first-release implementation unless a later explicit architecture revision selects them.

Annex UX Phase 2A terminal menus, Phase 2B private dashboard and Phase 2C browser actions remain deferred. The first release implements guided CLI, exact-plan review, truthful diagnostics and private inert static HTML reports; it has no persistent UI service or browser action API. UX-R16–R18/UX-T23–T24 are not first-release acceptance requirements. UXS-C labels expand existing UX tests, not a second coverage denominator.

The two-box development workflow is external engineering infrastructure. It does not add managed staging or multi-host application orchestration to Actools.


## 8. Fresh-install scope qualification

Architecture §18.11 adds FRESH-T01–T04 within existing owners/gates: reject conflicting populated targets and bind genuine resume to its journal; expose no migration/discovery/legacy-reader entrypoint; reject foreign recovery inputs before effects; qualify native own-site recovery including replacement-host operation and complete RPO/RTO. CP-002/CP-005/CP-010 own the early contract/dispatch slices; CP-022/CP-033/CP-035/CP-050 close installed cases as applicable. CP-040's graph marks excluded migration requirements NOT_APPLICABLE with their decision reference, never PASS. The removal does not delete WP24's DR responsibilities or its other applicable gates.
