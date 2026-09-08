# RB07 — Release candidate installation and rehearsal

Status: process runbook ready for later adoption; product command cells must be supplied from implemented runbooks before execution. No candidate or runtime rehearsal has been executed by this package.

| Field | Value |
|---|---|
| Owner / executor | Integrator / human release-test operator |
| Authority | Repository review/merge authority; separately authorized test-host administration |
| Target | Release-test server, with devbox for fixes and independent endpoint for applicable external tests |
| Applicable baseline | Architecture v1.5.1 §§13–15, §18.5, Annex UX; selected candidate/profile |
| Inputs | Completed task/review records, exact candidate SHA/package digest, trust metadata, qualified test commands and proposed release record |
| Disruption | Test-site outage, reboot, controlled faults and rebuild only as declared in the candidate test plan |
| Last actual rehearsal | Not run |

## 1. Preconditions

The human verifies the server/account identity before any privileged action. Confirm it is the expendable release-test target, has synthetic data and test credentials, and has no unique unexported work. Confirm console/rescue access, intended network identity, preservation of required evidence and backup/key references outside the target. Record the installed predecessor before upgrade tests.

The candidate must have passed its required pre-VM checks and independent code review. Record actual new source-CI workflow/check/run identities and the tested source/merge subject; green legacy jobs or a connector-returned commit are not qualification receipts. Use an actual package produced from identified source, not a source checkout with development tools silently supplying runtime dependencies. The package's trust path must follow the implemented v1.5.1 release design; any development trust root is explicitly test-only. Do not execute an unauthenticated download because its filename looks correct.

Verify that the build receipt names a clean reviewed source tree and all relevant generated/dependency inputs, and that the transferred artifact bytes match its authenticated manifest. Keep SSH agent/X11 forwarding disabled and do not attach sensitive laptop storage or credential sockets to this test host. Provider account tokens stay on the trusted human control device. GitHub write authority stays with the trusted human client or authorized connector credential store and is never copied to the server. The direct-GitHub route grants no provider/server authority.

Prepare a finite list of tests, intended disruptive effects, independent endpoints, required authority, deadlines and cleanup. Existing authorization for this test target carries forward; do not add ritual confirmations between routine approved steps. A target mismatch, missing recovery access or newly unbounded destructive effect is a stop condition.

## 2. Candidate worksheet

Complete before running:

| Item | Actual value required |
|---|---|
| Candidate ID / exact source SHA | Record real identities and completed integration checks; a pending/failed required check blocks qualification |
| Package/image digests and verification receipt | Record actual authenticated artifact identities |
| Host identity / image / OS / architecture | Record from the actual target |
| Profile / capability and contract versions | Match canonical graph and manifest |
| Predecessor for update/import | Exact supported edge, or clean install |
| Runbook versions and executable commands | References to implemented procedures |
| Independent probe/backup/monitor context | Identity/trust scope and known limitations |
| Evidence destinations and redaction | Paths/references excluding secrets |

## 3. Procedure

| Step | Human action | Required observation / evidence | Stop condition |
|---|---|---|---|
| 1 | Record repository/candidate identities and build receipts | Source and artifact identities agree; no unrecorded change | Wrong/missing identity or unreviewed input |
| 2 | Verify target and recoverability; export needed records before approved reset | Confirmed expendable target, independent evidence and recovery access | Unique data, uncertain target or failed rescue access |
| 3 | Create the clean target state required by the test, or the exact qualified upgrade predecessor | OS/image and starting state recorded | Unsupported OS/profile or unexplained residue |
| 4 | Verify and install the package using its implemented operator runbook | Trust and installed-layout checks pass; commands/outputs retained | Verification failure or missing documented step |
| 5 | Follow guided setup, plan review and application steps for the chosen supported profile | Correct target/effects, schema/output parity, no secret disclosure | Changed/stale plan, unexpected effects or unsupported option |
| 6 | Run selected positive and failure cases from the graph/test plan | Real receipts for each case, actual outcomes and cleanup | Unexpected scope, loss of control or violated protection floor |
| 7 | Perform required reboot/access/ingress tests with external observations | Observed behavior throughout relevant transitions | Only local/after-the-fact evidence when external/continuous proof is required |
| 8 | Perform declared backup/restore and independent monitoring exercises when that milestone is ready | Complete-set, recovery and independence evidence; timed boundaries | Missing independent authority, incomplete set or unsafe restored egress |
| 9 | Run the unfamiliar-operator walkthrough in RB08 | Documented steps suffice; deviations recorded | Hidden repair needed or misleading output |
| 10 | Reconcile results, clean declared fixtures, preserve receipts and update release record | No abandoned operations or unexplained changes; limitations explicit | Unresolved material findings or cleanup uncertainty |

For final CP-050 qualification, include accepted Cloudflare on/off evidence from CP-027 and current complete outage-start recovery evidence from CP-047. CP-035’s narrower recovery-path proof does not close intervals it did not measure.

No generic `actools` command sequence is supplied here because implementing this package is still future work. Insert only commands from the real implemented release and verify their options. Proposed tests remain specifications until their harness exists.

## 4. Failure handling

- Stop the affected case; retain redacted commands, timestamps, operation IDs, outputs and actual target state. Do not continue with the success branch.
- If a connection or output stream fails, inspect durable state using the implemented operation/reconciliation runbook. Do not repeat potentially completed effects blindly.
- If the test host is inaccessible, use the independently verified rescue path. Preserve evidence where practical before reset.
- Send a defect task to the coder with exact source/artifact/profile and reproduction. Fix in GitHub; rebuild and retest. Record any diagnostic manual repair as such, then restore the intended starting state before claiming installer success.
- A new package or material configuration change invalidates affected prior receipts. Do not reuse a candidate label to hide changed bytes.

## 5. Recovery, cleanup and acceptance

Restore declared access/maintenance state, remove only owned test resources, revoke temporary test credentials where planned and retain independently required recovery evidence/artifacts. Record incomplete cleanup explicitly. A snapshot reset is not a substitute for the required clean-install or application-restore case.

The integrator reviews the final record under [release acceptance](../07_RELEASE_AND_ACCEPTANCE.md). Passed task tests permit only their stated claim. Production admission remains later, on the real deployment with qualified independent custody/monitoring and current evidence.
