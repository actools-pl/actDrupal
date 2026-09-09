# RB05 — Recover access or reset a test box

**Purpose:** preserve control/evidence during a failed test and rebuild an expendable target deliberately. **Where:** laptop and Hetzner console/rescue interface; target only after its identity is established. **Inputs:** environment register, current task/operation ID, last candidate/artifact, tested recovery procedure, exported evidence and synthetic-data disposition. **Authority:** human owner of this test server. **Effects:** recovery or full target rebuild; the latter destroys that target's existing state.

This document intentionally supplies no generic firewall-flush, disk-wipe or force-reset script. Those commands depend on the actual installed platform and failure. Use the implemented task runbook or provider procedure for the exact observed condition.

## A. Access is lost or uncertain

1. Stop issuing repeated installer/apply/restart commands. Note UTC time, the last completed step, possible partial effects and whether a long operation may still be running.
2. Verify the target server ID through the trusted provider interface and compare the register. Check whether another declared management session/path still works. Preserve a working session; do not close it to “test again” before a replacement is verified.
3. Use the separately prepared console/rescue path. If those credentials are unavailable, stop and resolve account recovery through the provider; do not weaken unrelated machines or disclose secrets in chat.
4. Collect only targeted information needed to determine actual operation/network state. Export a redacted summary. Do not paste private keys, full environment dumps or credential-bearing configuration.
5. Follow the task's previously reviewed rollback/reconciliation procedure. If no such procedure fits, mark `blocked` and ask the coordinator/coder for a bounded recovery task against the observed state. Emergency actions must be recorded, not concealed.
6. Verify the recovered access and relevant protection postconditions. A reachable SSH port alone is insufficient if public restrictions were loosened. Record whether protection or data state is still uncertain.

## B. Decide whether to rebuild

Rebuild is appropriate for a clean-install milestone, a deliberately destructive fixture or a damaged expendable target after required evidence has been preserved. It is not a substitute for investigating every failed test; save enough to reproduce the defect first.

Before rebuilding, the human checks each item:

- Exact server ID/role and attached disks/volumes are identified; the other box is not selected.
- No unique source changes remain only there; committed changes and required evidence are available elsewhere.
- Test-data loss is intended, or the required independently stored backup has been verified sufficiently for the intended purpose.
- Any attached storage, snapshots and external resources have a separately documented keep/delete decision; do not assume a server rebuild handles all of them.
- Active operations/schedules and external observers are accounted for. Cleanup does not erase unresolved incident evidence.
- The selected replacement image/platform and post-rebuild access procedure are known.

Confirm this concrete destructive step with the human operator at execution time. The project's use of expendable boxes makes rebuilding part of the workflow; it does not identify which current server or data should be destroyed.

## C. Rebuild and re-register

1. Use the current documented provider rebuild/reinstall procedure for the identified test server. Read the provider's actual operation summary before confirming it.
2. Record the new environment generation and image. Recheck the control device’s effective session isolation; a saved SSH alias must not re-enable agent/X11 forwarding or undeclared tunnels after rebuild. Re-establish a known administrator identity and verify the new host fingerprint through a trusted channel. Do not blindly disable host-key verification or accept an unexpected key on an unchanged server.
3. Restore only the prerequisites the current task/runbook declares. Do not copy private production credentials, developer home directories, unreviewed binaries or old root state.
4. Validate console/SSH recovery access before resuming host security work. Re-run required clean baseline/preflight assertions.
5. Mark previous boot/state-specific evidence historical. Preserve its receipts but do not report them as observations of the rebuilt server.
6. Resume from a newly issued/confirmed task plan for this generation. Old plans bound to prior state or keys must not be blindly replayed.

**Expected:** regained verified control or a documented clean replacement, with preserved failure evidence and explicit data disposition. **Stop:** uncertain target, inaccessible independent evidence/keys, uncontrolled external effects or unreviewed destructive recovery. **Record:** environment generation, incident/receipt references, action authorization, discarded/retained data, access verification, unresolved findings and next task in the handoff.
