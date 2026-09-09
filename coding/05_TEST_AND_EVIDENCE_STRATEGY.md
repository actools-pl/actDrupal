# Test and evidence strategy

## 1. What this strategy proves

The package defines how to obtain evidence; no installer test has passed merely because this document exists. Architecture v1.5.1 §§13.5–13.6, 15 and 18.5, the integrated S2–S5/RV13 cases and Annex UX control the required behavior. Task plans select applicable cases and retain their original IDs. New regression fixtures can receive task-local IDs without renaming architecture requirements.

A code review checks reasoning and implementation. A unit test checks a bounded component. An installed test checks the actual packaged entrypoint and environment. An external test checks a boundary from outside it. A recovery rehearsal checks whether data and service can actually be recovered. These forms support different claims and cannot substitute for one another.

## 2. Test environments

| Environment | Main use | Cannot establish alone |
|---|---|---|
| Ephemeral source CI | Unit, schema/contract, static checks, deterministic fixtures, packaging and documentation checks | The actual supported VM's host security, external firewall behavior or complete recovery |
| Mutable Hetzner devbox | Implementation debugging, installed development slices, real Ubuntu services, controlled failure injection | Clean release installation if development tools/manual changes supplied missing prerequisites |
| Hetzner release-test server | Reviewed immutable candidates, fresh installation, upgrades, reboot/interruption and documented operator journeys | Independence from the same provider/account or untested production capacity |
| Laptop / separately controlled endpoint | External probes, controller/key custody and initially attended backup/recovery exercises | Continuous monitoring or one-hour recovery coverage while asleep/offline |

The two Hetzner boxes are distinct targets, not an HA pair, replica pair or managed staging feature. Never assume nested VMs are available. Run one target-destructive test at a time; preserve the other machine only where the test plan explicitly assigns it a role. If the laptop is the backup controller, identify sleep/connectivity restrictions in every relevant receipt. Same-account/provider redundancy is not independent provider/account-loss evidence.

Later complete production qualification needs the architecture's independently controlled, reliably available backup/monitor arrangement. A simulated backend in the devbox or a temporarily awake laptop can test protocol behavior; it cannot pass the absent independence/availability obligation. Record that gate as unverified/blocked with a named dependency.

## 2.1. Source delivery and source CI

Either the human-Git route or the bounded direct-GitHub route in [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) may deliver a reviewed source candidate. A connector-returned commit SHA identifies a repository change; it does not prove a local checkout exists, that a build ran, that the build inputs were clean or that a server was tested. Verify the candidate's complete resulting tree/diff and obtain actual execution receipts from the relevant CI runner or human-operated environment. Never fill absent checkout, digest or result fields with a model inference.

Before repository writes, verify applicable current automation under [RB11](runbooks/RB11_NEW_REPOSITORY_STARTUP.md). BOOT-000's seed and BOOT-001's documentation have their own review/structural checks, with no invented source-CI prerequisite. CP-001 establishes source CI for the new Python package. Retain workflow/check/run identities, actual tested source or merge subject and conclusions. Skipped, cancelled, unavailable or permissively non-failing jobs do not establish PASS. Meaningful negative fixtures prove failure behavior; ordinary source CI has no provider/production credentials or provisioning effects. Configure only real verified required checks within the recorded authority.

## 3. Plan each task before running it

Use `templates/TEST_PLAN.md`. Record:

- Exact requirement, risk and externally observable assertion.
- Supported profile, enabled capabilities and excluded/deferred capabilities with reason.
- Required source SHA/artifact, fixtures and test implementation version.
- Location, target identity, authority, expected effects and cleanup.
- Actual commands only after implemented and reviewed; prerequisites and expected exits/output.
- Failure injection, positive behavior, stop condition and recovery path.
- Evidence required, data classification, redaction and what would invalidate the result.

A low-risk documentation typo does not require unrelated VM tests. A change to privileged paths, state durability, secrets, firewall, backup consistency or interface semantics needs tests of the concrete changed risks. Tests should detect a deliberately seeded relevant defect or independently observe the invariant; copying the implementation's calculation into an assertion is weak evidence.

## 4. The first installed slice

Before host mutation, implement and qualify WP01–WP04 plus the bounded WP09 slice: the installed package validates a strict configuration, emits a genuinely read-only plan, executes one owned reversible fixture effect under the fixed executor, journals it, rejects stale/tampered inputs, survives a declared interruption and reports reconciliation truthfully.

This fixture is an isolated owned test resource, not permission to alter SSH or firewalls. Prove applicable G04 read-only behavior and installed-layout handling before starting the actual host preparation handlers. Add diagnostics, help, documentation and packaging with each slice; do not defer them to the end.

## 5. Host and runtime qualification

Before tests, verify session isolation: no forwarded SSH agent or X11 session, sensitive laptop mounts, personal GitHub write credentials, provider API tokens or production authority on either test host. Use separate test credentials and only the declared external connections. Access from the laptop does not require granting the remote host access to the laptop’s agents or files; see [security rules](08_SECURITY_AND_SCOPE_RULES.md).

For host changes, capture exact Ubuntu image/release, kernel, architecture, relevant package versions, boot identity, target role and network topology. Use a fresh server for clean-install evidence at defined milestones. A reset to a prepared snapshot is a useful known-state test but is not automatically a clean vendor-image installation.

For SSH/WireGuard/firewall tests, check alternate recovery first and keep a second working session where the task requires it. External positive/negative IPv4 and IPv6 probes, including during transitions, need an external observer and ordering evidence. A local listener listing or a successful SSH session cannot prove every prohibited ingress path is denied. Lack of IPv6 connectivity from the observer is an evidence limitation, not an IPv6 PASS.

Pin installed artifact and template/image digests. Verify effective behavior inside consumers; a rendered configuration file or accepted reload command alone does not prove activation. Include legitimate Drupal workflows alongside denial tests. Test synthetic canaries rather than real credentials/content.

## 6. Recovery and longer-running qualification

Backup eligibility, committed complete coverage, repository data verification, independent key custody, historical verification, restore success and RPO/RTO are separate assertions. Record observed timestamps and source boundaries. A successful command, directory upload or backup repository connection does not prove these obligations.

Measure the representative accepted 80 GB profile and actual change rate when available. The 80 GB input is neither a storage allocation nor an automatic performance guarantee. Do not extrapolate a small fixture into full-site recovery acceptance. Retain all failed captures and breached intervals in evidence.

The one-hour RPO and four-hour RTO remain architecture requirements. An exercise can pass “the tool reports a missed objective honestly” while failing the recovery objective itself. Mark both results explicitly. Include operator response and replacement-host work in the architecture-defined outage-start RTO. Controlled tests use synthetic data and private outbound restrictions; copied environments must not email users or run inherited jobs.

CP-035 provides measured fresh-host recovery-path evidence before destructive update/cutover work; record any simulated detection/delivery assumptions and unmeasured intervals. It cannot close the complete outage-start RTO while CP-045/046 monitoring and notification delivery are absent. CP-047 measures the complete outage/detection/delivery/operator/bootstrap/recovery chain, and CP-050 verifies that evidence applies to its exact candidate/profile, repeating invalidated portions or the full exercise as required. The one-hour RPO and four-hour RTO targets remain unchanged.

Use release-test for repeated backup cycles, upgrade paths, reboot and bounded soak tests as the implementation reaches those milestones. Every soak test declares a duration, workload, capacity profile, budgets, interruption handling and acceptance thresholds before execution. Do not invent throughput or uptime promises in the documentation package.

## 7. UX and documentation are testable

Select relevant UX-T01–UX-T22 and expanded UXS cases. Include closed stdin/non-TTY, structured stdout, bounded stderr, interrupted output, same-plan review binding, secret/error redaction, inert report content, genuine unprivileged rendering, safe destinations and truthful freshness/admission state.

Run the installed CLI/help and packaged runbooks. Test HTML using the declared browser/environment, keyboard, zoom/reflow, print and appropriate assistive checks; automated lint alone cannot assert accessibility compliance. An unfamiliar operator should complete representative setup, failed-operation diagnosis and private recovery without the coder supplying missing commands. Record every undocumented intervention as a defect.

## 8. Results and evidence receipts

Use `templates/TEST_RECEIPT.md` for each coherent test run. Result labels for this development record are `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN` and `NOT_APPLICABLE`; these are evidence bookkeeping labels, not replacements for the product's result/exit contracts. `NOT_APPLICABLE` requires the explicit profile/scope reason. An interrupted run is not a pass and records its observed outcome and incomplete assertions.

For source tests/builds, record source cleanliness and relevant local/generated inputs before and after execution. A commit SHA is not proof that local bytes matched it. Acceptance evidence uses the reviewed clean subject; dirty debugging runs retain their actual diff/input identity and remain exploratory until the correction is committed, reviewed and affected checks rerun. Installed evidence names the actual verified transferred/installed artifact and any observed target drift.

If ChatGPT cannot execute a test, its own execution status is `NOT_RUN`; preserve a human-run or CI-run test's actual outcome and receipt separately. Observing a check through a connector is evidence collection, not model-local execution. A capability to read or write GitHub grants no Hetzner or test-host authority; the human continues the approved server procedures.

Bind every receipt to the full tested source SHA, artifact digest where installed, test fixture version, target/environment, operator, UTC timestamps, commands/exits, expected/actual observations, limitations and cleanup. Attach a redacted summary and link/digest of suitable retained artifacts. Retain the original failed observation alongside later corrected evidence.

Separate the tested subject SHA from the later commit that records the receipt. A receipt cannot include the hash of the same commit that contains itself. Record source/artifact identities as observed; the evidence index/history records where the receipt subsequently landed.

Inspect logs before sharing. Do not collect `env`, unrestricted container inspect, private settings, credentials, live tokens, database dumps or broad home-directory archives as convenient context. Prefer targeted redacted observations. Keep sensitive/raw evidence privately controlled; public Git records contain only appropriate metadata and redacted extracts. A hash does not make confidential content safe to publish or authenticate its origin.

## 9. Retesting and closure

Changing a relevant source file, dependency lock, build image, selected capability, configuration, security policy or target state may invalidate a receipt. The reviewer records affected tests and explains any reuse. Reboot invalidates boot-specific observations. Rendering an old report does not refresh its evidence.

Before privileged tests: source review must find no unresolved material concern for those effects, the human verifies the target, authority, prerequisites and recovery. Before task acceptance: required tests and documentation checks are complete. Before release: the combined packaged candidate is qualified independently and all applicable release/profile gates are assessed. No single “all tests passed” badge replaces the gate matrix.

Use `runbooks/RB03_TEST_ON_DEVBOX.md`, `runbooks/RB04_QUALIFY_ON_RELEASE_TEST.md` and `runbooks/RB06_CLOSE_TASK_AND_HANDOFF.md`. Store indexes in `records/TEST_EVIDENCE_INDEX.csv`; milestone/release status remains explicit in `records/RELEASE_REGISTER.csv` and `templates/RELEASE_RECORD.md`.
