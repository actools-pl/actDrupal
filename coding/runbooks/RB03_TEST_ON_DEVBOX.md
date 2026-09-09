# RB03 — Test a candidate on the devbox

**Purpose:** obtain actual target evidence while permitting development debugging. **Where:** laptop control terminal plus the registered devbox. **Inputs:** candidate SHA, initial review record, task test plan, synthetic fixtures, recovery plan. **Authority:** unprivileged by default; only named task steps use required privilege. **Effects:** those explicitly listed in the task, potentially disruptive/destructive on this expendable target.

## Prerequisites

1. Identify the physical/cloud target from the environment register: provider server ID, dev role, hostname/address and current rebuild generation. Verify that your terminal is on that target before every privileged sequence. Similar hostnames and an open SSH tab are insufficient.
2. Confirm this server has no production/customer data, production credentials or irreplaceable unexported evidence. Preserve committed work and required private/redacted artifacts outside it.
3. Read the review record for the exact candidate SHA. Resolve material findings relevant to the proposed privileged effects first. The same model saying “safe” is not permission to skip human target/effect checks.
4. Ensure all task commands are implemented and reviewed, with expected output/exit, test data, cleanup and a finite timeout/stop condition. If a command is absent, mark that case `NOT_RUN`/`BLOCKED`; do not improvise a product command.
5. Before access/firewall/reboot work, verify the independent console/rescue procedure and credentials through the normal provider interface. Establish required alternate/fresh SSH access before closing an existing working session. Do not publish recovery credentials or console screenshots containing them.

Before connecting or transferring artifacts, verify session isolation: SSH agent/X11 forwarding disabled, no sensitive laptop mounts/credential sockets/undeclared reverse tunnels, and no personal GitHub write or provider credentials on the target. Use the separate test identity and approved transfer path in the environment register. See [security rules](../08_SECURITY_AND_SCOPE_RULES.md).

A candidate delivered through [RB12](RB12_DIRECT_GITHUB_OPERATIONS.md) still needs the actual source/CI/build and transfer evidence below. A GitHub commit response is not a local checkout or executed test. The human operates the server under the declared authority; connector access does not authorize SSH, provider actions or test effects.

## Procedure

1. Start a new test receipt. Record UTC time, operator, target/rebuild ID, full candidate SHA, artifact digest for installed tests, OS/image/kernel and relevant versions. Record synthetic fixture identity and previous target state.
2. Fetch/check out the exact reviewed source when the task is a source-level dev test. For installed tests, build/install the specified candidate through the reviewed packaging procedure. Verify source/package identity on the devbox. For qualification source tests/builds, verify the clean checkout and declared build/generated inputs, and capture source state before and after the run. For installed tests, verify the transferred bytes and actual installed artifact. A moving branch name or `HEAD` alone is insufficient. A dirty debugging run must retain its diff/input identity and be labeled exploratory; commit/review the correction and rerun affected checks before acceptance.
3. Execute the task's unprivileged checks first. Attribute prior source-CI evidence to its actual workflow/check/run and tested subject; inherited legacy-CI success does not replace required new Python checks. Record commands and actual exits without masking failures through shell pipelines. If log capture is used, the task must preserve the underlying command exit and redact before export; do not add an unreviewed universal `tee` wrapper.
4. Execute approved privileged steps one at a time, checking the target, current conditions and outcome. Follow the task's exact privilege mechanism; no unrestricted root shell is assumed.
5. Run positive and negative assertions, including declared interruption boundaries. For network controls, operate the external observer from the laptop/declared separate endpoint and record that identity. Pair denied paths with required allowed access.
6. If output delivery fails after an effect, inspect the durable operation state using the implemented, reviewed procedure. Do not repeat a mutation because the terminal lacked a success message.
7. Capture targeted evidence, failed attempts and limitations. A debugging change made directly on the server is an unreviewed new candidate: record it, bring the change into Git, then review and retest affected cases. Never silently promote it as the original SHA.
8. Execute the named cleanup procedure, verify cleanup postconditions and export evidence before reset. Update the receipt and evidence index; leave task state `testing`, `changes_requested` or `blocked` according to the result.

## Expected result

The exact candidate either demonstrates the required assertions in the recorded environment or produces a specific reproducible defect. Receipts distinguish observed failure, missing prerequisite and unexecuted test. Nothing here qualifies a different release package or production profile automatically.

## Stop / recovery

Stop immediately for wrong target, lost alternate recovery, unexplained privilege, exposure of a secret, unexpected outbound delivery, uncontrolled resource use or a step outside the test plan. Preserve available evidence. Use RB05 for access/reset decisions. Fixes return through Git and review; do not disable the failing security control to continue.

If the laptop goes offline during an independent check, mark the affected observation incomplete. If it hosts backup/monitor duties, record the coverage interruption; do not turn an asleep controller into an RPO/monitoring PASS.

**Record:** `templates/TEST_RECEIPT.md`, relevant `templates/REVIEW_RECORD.md` updates, `records/TEST_EVIDENCE_INDEX.csv`, environment generation and the next action in `records/SESSION_HANDOFF.md`.
