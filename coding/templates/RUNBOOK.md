# RB-____ — <one operational outcome>

Status: <specified-not-implemented / implemented-not-qualified / verified-for-named-release-profile / needs-reverification>.

## Identity and applicability

| Field | Value |
|---|---|
| Runbook version / owner | <...> |
| Installer release/source/package digest | <exact tested identity, or not implemented> |
| Supported profile and capability/handler IDs | <...> |
| Authority and required actor | <...> |
| Target machine/environment | <laptop/devbox/release-test/production/independent backup environment> |
| Requirement/gate/task IDs | <...> |
| Last walkthrough / reviewer / receipt | <actual identity/date or not run> |

## Outcome and prerequisites

<Purpose, entry criteria, required current evidence, target validation, tool versions, independent recovery access, inputs and secret-reference locations. Never include secret values.>

## Disruption and boundaries

<Expected effects, service/write pause, finite deadlines, irreversible boundary and impact on concurrent operations. State what cannot safely be retried blindly.>

## Procedure

| Step | Exact implemented command or named manual action | Where / authority | Expected observation | Stop if |
|---|---|---|---|---|
| 1 | <command/action> | <context> | <observable postcondition> | <condition> |

Each command must be verified against current help/handler source before being labelled executable. Keep proposed future commands in a separate specification section, not mixed into the runnable procedure. Do not leave unresolved placeholders in an operationally qualified runbook.

## Stop and reconciliation

<How to preserve evidence, identify durable operation state, avoid duplicate effects, keep protection floors and select the qualified next action. Loss of stdout/SSH is not proof of failure or rollback.>

## Recovery branches

| Condition | Safe observation | Authorized recovery action | Success / escalation condition |
|---|---|---|---|
| <failure> | <bounded observation> | <implemented action> | <observable result> |

## Cleanup and evidence

<Temporary resources, retained diagnostic data, cleanup receipts, restored maintenance/access state and safe evidence destination. Record exact source/package/profile, commands, timestamps, operator, expected/observed result, operation IDs and redaction. For timed recovery, record the actual clock origin and each measured detection, delivery, response, bootstrap and recovery interval. Distinguish a partial recovery-path rehearsal from complete outage-start RPO/RTO qualification; identify simulated or unmeasured intervals.>

## Escalation and document maintenance

<Named project role/contact mechanism without secrets; material defect recording; dependent guides; changes requiring re-verification.>
