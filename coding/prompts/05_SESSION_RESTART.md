# Session restart prompt

**Active scope:** repository `actools-pl/actDrupal`, architecture v1.5.1, fresh installations only. No existing-site discovery/import/cutover or legacy age reader. Use `main` integration after BOOT-000, then task branches; original v1.5 in `reference/` is historical only. CP-038/039 are cancelled and cannot block active tasks. Own-site backup, restore, disaster recovery and supported updates remain required.


Use in a new role-appropriate conversation after a long interruption, model change or uncertain context. Coordination/coding remain ordinary-chat; reviewer-only Work selection and ordinary fallback follow [CPD-12](../records/REVIEW_ROUTE_DECISION.md). Do not paste secrets or raw server dumps. Read the saved handoff, verify current chat capabilities and obtain fresh repository status first. Direct GitHub operation is optional; human-Git remains the fallback. Use [CONTEXT_PACKET](../templates/CONTEXT_PACKET.md) and [HANDOFF](../templates/HANDOFF.md); no Work, Project or shared-memory feature is needed.

```text
Resume the Actools task using repository-backed records, not conversation memory.

CURRENT INPUTS SUPPLIED OR READ AT IMMUTABLE COMMITS
- Role for this session: coordinator/coder/reviewer/documentation reviewer.
- Actual or operator-reported interface/model/effort; CPD-12 reviewer switch and reason when applicable; prior report, reading boundaries and evidence attribution.
- TASK_CARD and task ID/state.
- PROJECT_STATE, TASK_LEDGER and SESSION_HANDOFF.
- Exact current repository/branch/base/candidate SHA from actual Git/GitHub observations.
- Selected route, capabilities verified in this chat, existing bounded authorization and applicable RB11/RB12 records.
- Actual local checkout clean/dirty state if one is used; otherwise NOT_APPLICABLE with reason for API-only source editing. Actual test/build inputs remain separately identified.
- Full current affected files and required surrounding schemas/interfaces/tests.
- Accepted architecture v1.5.1, relevant ADRs and adopted repository instructions.
- Open review findings, actual redacted test receipts and documentation status.
- Current input-packet and delivery revisions, type and complete/incomplete status.
- Any unapplied patch or complete-file bundle, filename and actual computed digest or UNSET, and its exact base SHA.
- Direct-route returned write/commit/parent identities, observed final head, read-back/PR records, partial candidates and pending or uncertain operations. No patch is required for a direct candidate.
- Whether the latest delivery replaces an unapplied earlier delivery or is an incremental correction on a committed candidate; superseded deliveries.

First state which supplied files/revisions you actually read in full, partly read, could not access or did not need. Ask for specific material missing files or ranges. Then reconcile these inputs. State what is already committed, only proposed, applied but uncommitted, tested, reviewed, blocked and still unknown. Do not apply an old patch to a different base, rewrite concurrent work, re-run a destructive operation or declare a previous test applicable without checking identity/context.

For human-Git delivery the operator uses Git. For direct GitHub delivery a currently capable chat may perform only the repository operations covered by existing bounded authorization, without per-file permission prompts. First follow RB12: inspect head drift and any ambiguous write result before retries; refresh current source at the actual candidate. If capability is unavailable or cannot safely protect the mutation, switch to the human-Git route only after reconciling committed changes. Never overwrite concurrent edits or blindly reapply already committed changes. The human retains integration authority and operates both Hetzner boxes. Repository capability grants no workflow dispatch, provider/server authority, protection bypass or unrelated PR action. Confirm the intended machine and current installed candidate before suggesting tests. Lost connection or missing final output means inspect durable state using the implemented runbook; it does not mean repeat effects.

Return a concise restart assessment, precise missing inputs if any, and the next bounded action permitted by the current task. Use the normal role prompt after reconciliation. If context or required output is too large, ask the coordinator to narrow the coherent task rather than silently drop current source, security checks, tests or docs. Do not restart finished work or rely on an unseen earlier chat's decisions. Dated GitHub handoff observations require current verification. Preserve failed receipts and genuine merge facts; a merged commit does not clear a task blocked by required integration checks.
```
