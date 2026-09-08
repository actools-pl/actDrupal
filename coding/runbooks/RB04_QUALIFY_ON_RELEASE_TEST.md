# RB04 — Qualify a candidate on the release-test server

**Purpose:** prove the packaged installer and operator instructions work independently of the developer's repaired environment. **Where:** registered release-test server, laptop/external observer, GitHub evidence. **Inputs:** reviewed source/integration SHA; built artifact and manifest/digests; documented installation/update procedure; test plan; known test data; independent recovery material. **Authority/effects:** declared installation, upgrade, reboot or restore steps on this expendable test target only.

## Prerequisites

1. Confirm the task is ready for this milestone. Record the exact candidate artifact and its build source, dependency locks, build process/run and verification method. Candidate review/devbox evidence must refer to this source or document precise equivalence and remaining tests.
2. Record server identity and whether the test starts from a clean qualified Ubuntu image, a specific installed predecessor or another explicitly defined state. Rebuild when a clean-install case requires it; a prior developer-prepared snapshot is not that proof.
3. Verify provider console/rescue access and the data/export/reset plan. Use only synthetic/test secrets. Check network restrictions for copied environments before restore can trigger email, webhooks, scheduled jobs or database events.
4. Confirm required independent observation/backup endpoint availability. Same-provider/account separation and a laptop controller have the limits in `05_TEST_AND_EVIDENCE_STRATEGY.md`.
5. Verify effective SSH session isolation and transfer credentials under the security rules: no agent/X11 forwarding, broad mounts, credential sockets, personal GitHub write or provider tokens on this host. Verify the transferred artifact and ensure its build receipt records a clean source checkout plus declared build inputs.
6. Have an operator follow packaged instructions. Prefer someone unfamiliar with the implementation; if the same human must act, record that limitation and avoid relying on undocumented memory.

Direct GitHub delivery is source delivery only. Readback of a candidate SHA under [RB12](RB12_DIRECT_GITHUB_OPERATIONS.md) cannot replace actual new source-CI, clean-build, authenticated artifact or installed-test receipts. Keep the human-operated server procedure and its authority unchanged regardless of the Git delivery route.

## Procedure

1. Begin a receipt and record target generation, image/kernel/platform, selected profile/capabilities, UTC start, artifact digest and installed predecessor if applicable.
2. Install/upgrade using only the candidate's documented supported bootstrap and operator runbook. Record every command and meaningful outcome. Product verification/trust requirements remain mandatory; a locally computed digest is not a substitute for authenticated release verification.
3. Do not install compilers, development dependencies, source trees or ad hoc packages merely to make the product work. If the official architecture/profile deliberately requires a dependency, its installer/runbook must own and verify it. An undocumented manual prerequisite is a defect.
4. Run the milestone's functional/security/UX cases from the approved test plan. Include legitimate workflows, failure/interruption behavior, reboot where relevant and installed help/runbook checks. Record terminal/session and underlying operation outcomes separately.
5. For upgrades, preserve the exact predecessor artifact/config/data fixture and exercise only a supported edge. For recovery, use independently retained keys/readers and measure the architecture-defined scope. A successful fresh install does not prove upgrade or restore. An early CP-035 recovery-path exercise records its limited timing scope; the complete detection/delivery-inclusive outage-start RTO is measured in CP-047 and reassessed for CP-050’s exact candidate, as specified in the roadmap.
6. For longer-running tests, start the declared workload and measurement period only after recording its baseline and criteria. Preserve failed attempts, missed schedules and notification-channel outcomes separately. Do not extrapolate a short run to unmeasured availability.
7. Any manual repair stops qualification of that unchanged candidate. Record the missing instruction/defect, fix in Git, review it, build a new identified artifact and rerun affected cases. Leave the old receipt intact.
8. Finish with cleanup, actual final state, exported redacted evidence and a milestone qualification decision. Keep the server available for the next planned test or rebuild under RB05. Record retained data and pending cleanup explicitly.

## Expected result

A named candidate is qualified only for the implemented cases, supported profile and measured conditions in its receipts. “Installed successfully” is narrower than “first release qualified.” Repository merge, successful CI and attractive diagnostic reports cannot grant production admission.

## Stop / recovery

Stop for wrong artifact/target, unexpected live credentials/data, missing alternate access, uncontrolled external effects, absent required recovery material, missing runbook step or insufficient measurement inputs. Preserve evidence and use the task's recovery procedure/RB05. Do not fetch a newer mutable “latest” build during a running qualification sequence.

The release-test server does not become live production by relabeling it. Before real deployment, use the approved clean deployment procedure and production credentials/data workflow. No purchase, live deployment or public admission is authorized by this runbook.

**Record:** test receipts and index, `templates/RELEASE_RECORD.md`, `records/RELEASE_REGISTER.csv`, review findings, runbook defects and next handoff.
