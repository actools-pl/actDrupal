# Troubleshooting the Coding Process

| Situation | What to do | What to record |
|---|---|---|
| Chat remembers another architecture version | Attach the current baseline/decision record; identify the exact contradictory instruction | Active baseline and affected task |
| Chat cannot read an attachment/archive | Supply the exact missing individual files and update the read receipt; do not infer content from filenames | Packet revision and actual full/partial/unavailable coverage |
| Output ends mid-file or download is unavailable | Preserve incomplete output separately; use RB10 to obtain a complete bounded replacement or plain-text delivery | Manifest, base, delivery status and actual saved files |
| Direct GitHub connector is absent or lacks a required operation | Use the existing human-Git route within the same task scope; refresh the packet from actual state | Capability gap, route change and exact base/candidate |
| GitHub reports a permission or protection failure | Retain the redacted failure; use authorized human operations or resolve the genuine permission requirement | Operation, branch, returned result and blocker; no token disclosure or ruleset bypass |
| GitHub write times out or its outcome is uncertain | Stop dependent writes; read the current ref/files/PR/checks and reconcile possible completion under RB12 before any retry | Intended effect, known pre-state, response, observed post-state and unresolved effects |
| GitHub branch changed unexpectedly | Preserve both candidate identities; re-read full changed content and coordinate a new base/review | Expected/actual SHAs, competing changes and accepted correction lineage |
| A configured workflow can provision infrastructure or exposes unexpected authority | Stop repository writes and use RB11 for containment planning before proceeding | Workflow/ref/trigger, relevant authority, current runs and scoped next action |
| A CI badge is green but required Python assertions are missing or skipped | Keep new-source qualification blocked; inspect the intended check definitions and actual assertions | Workflow/check/run IDs, tested SHA, conclusions and missing coverage |
| Coder lacks a file/interface | Export the exact relevant committed file; revise packet inventory | Packet revision and unchanged/changed base |
| Patch fails applicability | Stop; inspect actual base and dirty files; request a refreshed patch or reviewed conflict resolution | Expected/actual commit and failure output |
| New files are absent from a diff | Inspect status and explicit new-file inventory; include them in review and commit | Full changed-path list and modes |
| AI says tests passed without real evidence | Classify as proposed/unverified; run the task-owned checks in the correct environment | Actual receipt or NOT_RUN reason |
| Tests pass but required behavior is absent | Review assertions and entrypoint wiring; add an independent failure fixture | Requirement gap and regression test |
| Review recommends disabling a failing security check | Determine whether the check is wrong using source/requirement evidence; do not weaken a valid requirement | Decision and independent justification |
| Devbox works but clean release-test fails | Preserve both environments; identify hidden dependency or manual change; fix source/runbook | Exact package, environment delta and retest |
| Operation output disappears | Inspect the recorded operation and actual state before retry | Known/unknown effects, ID and reconciliation direction |
| Remote access is lost | Use the previously verified independent console/rescue procedure | Host identity, last change and recovery steps |
| Only one external probe family is available | Record missing IPv4/IPv6 coverage; obtain the missing vantage before its claim | Actual source/target protocol and limitation |
| Laptop backup/monitor was offline | Record the gap; do not claim continuous protection | Missed interval and next qualified test |
| Conflicting chats edit the same component | Stop competing writers, preserve candidates and let the integrator choose a base | Candidate identities and resolution |
| Candidate merged under a different commit | Record the real merge identity and recheck integration; task stays blocked while required checks are pending/failing | Candidate→merge mapping, actual merged SHA, check receipts and any corrective task |
| Documentation names a nonexistent command | Correct docs to installed grammar or finish the declared command task; no ad hoc alias | Example/version and verified replacement |
| A secret appears in output or Git | Stop sharing; follow RB09 and credential-specific incident procedure | Redacted incident ID, exposure scope and remediation |
| A user asks for broader functionality mid-task | Preserve current state; let coordinator define revised task/dependencies | Explicit revised scope and consequences |

Related repository procedures: [RB11 new repository startup](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) and [RB12 direct GitHub operations](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md). Connector availability does not create authorization; a fallback route does not expand the allowed operation. No GitHub permission grants test-host or provider authority.

## When a test command fails

Send the exact command, exit status and bounded redacted output along with its candidate/environment identity. Do not send only “it did not work.” Ask for diagnosis against the accepted requirement, then a minimal coherent patch and regression case. A workaround that changes the host manually must be recorded and cannot replace a reproducible release-test pass.

## When no safe next step is known

Use task state `blocked`. Identify the missing fact, the authority/effect at risk, who can resolve it and the smallest read-only observation that could help. Do not guess destructive cleanup or use a general shell offered by a generated error message.

## When a chat is too long

Save the patch, evidence, records and handoff. Start a new chat with [SESSION_RESTART](prompts/05_SESSION_RESTART.md). The new chat verifies actual state before changing files. A summary is a navigation aid; the current committed files remain authoritative. Refresh the packet and read receipt. Never join unanchored continuation fragments or old full-file replacements into a new candidate; use the explicit delivery/base protocol in [RB10](runbooks/RB10_PLAIN_CHAT_FILE_HANDOFF.md).
