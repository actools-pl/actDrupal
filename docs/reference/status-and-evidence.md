# Status, coverage, gates, and evidence

CP-003 preserves operational facts as separate axes. A renderer may explain these
facts but must not merge, upgrade, or re-evaluate them.

## Finding status and severity

| Finding status | Meaning |
|---|---|
| `PASS` | Fresh valid proof establishes that the control is satisfied. |
| `FAIL` | Valid proof establishes a violation. |
| `WARN` | Valid proof establishes a policy-defined weakness or approaching threshold. |
| `UNKNOWN` | Proof is missing, stale, inaccessible, malformed, unsupported, or inconclusive. |
| `SKIPPED` | The assessment was deliberately omitted and no evaluated equivalent proof exists. |
| `NOT_APPLICABLE` | Registry and deployment proof establishes that the control does not apply. |

Severity is independent: `critical`, `high`, `medium`, `low`, `info`, or `none`.
PASS and NOT_APPLICABLE use severity `none`. A FAIL can be nonblocking, and an
exception does not rewrite FAIL to PASS.

Evidence state is also independent: `valid`, `missing`, `stale`, `inaccessible`,
`malformed`, `unsupported`, `inconclusive`, `skipped`, or
`not-applicable-proven`. Valid evidence needs an observed identity and an evidence
reference. Missing or incomplete proof cannot carry a factual PASS/FAIL/WARN.
NOT_APPLICABLE requires its own applicability proof.

## Run state, gate state, and impact

Run state is `complete`, `partial`, or `error`. Any UNKNOWN or SKIPPED result makes
the pure evaluator's run partial; an engine error makes it error.

Each evaluated policy has a separate gate state:

- `pass`: the evaluated policy has no blockers or full-required coverage gaps;
- `blocked`: blockers or required coverage gaps remain;
- `not_evaluated`: this policy gate was not requested or could not be evaluated.

Each finding separately records `blocks`, `does-not-block`, or `not-evaluated`.
A healthy doctor policy does not imply a production-admission evaluation.

## Two coverage denominators

For applicable findings only:

\[
\text{selected coverage} =
\frac{\#(\mathrm{PASS,FAIL,WARN}\ \text{among selected controls})}
{\#(\text{selected controls})}
\]

\[
\text{full required-policy coverage} =
\frac{\#(\mathrm{PASS,FAIL,WARN}\ \text{among required controls})}
{\#(\text{required controls})}
\]

UNKNOWN and SKIPPED controls remain denominator members and are named in
`gap_ids`. Proven NOT_APPLICABLE controls are excluded. A narrow selection cannot
reduce the full required-policy denominator. Optional selected gaps remain visible
and can make a run partial, but alone do not force exit 2 when full
required-policy coverage is complete.

## Audit and doctor exit precedence

| Exit | Meaning |
|---:|---|
| 0 | Required applicable controls were assessed and the selected policy permits the outcome. |
| 1 | Required coverage is complete, but assessed findings block the selected policy. |
| 2 | Required evidence/coverage is incomplete, including a run that also contains known failures. |
| 3 | Invocation, context, engine, or report-production error prevents a valid result. |

Precedence is `3 > 2 > 1 > 0`.

For example, one valid blocking firewall FAIL plus one required missing backup
observation produces:

| Axis | Value |
|---|---|
| Firewall finding | `FAIL`, preserved |
| Backup finding | `UNKNOWN` |
| Selected coverage | `1 / 2`, gap is backup |
| Full required-policy coverage | `1 / 2`, gap is backup |
| Gate | `blocked`, with both blocker and gap |
| Run state | `partial` |
| Exit | `2`, because incomplete coverage outranks blocking findings |

This is not converted to generic failure and the known firewall violation is not
discarded.

## Time and provenance ownership

| Field | Owner and meaning |
|---|---|
| `captured_at` | Collector: when the observation snapshot was obtained |
| `evaluated_at` | Evaluator: when policy meaning was assigned |
| `valid_until` | Evidence policy: the latest validity boundary for this context |
| `rendered_at` | Presentation adapter: when a view was produced |

Rendering never changes capture/evaluation time or renews validity. A static HTML
file is a historical view, not live state.

Evidence provenance separately records source kind/reference, authentication
reference, integrity algorithm/digest/verification, context match, freshness, and
whether a value is presentation-only. A hash proves identity only. Admission
requires an independently authenticated source plus exact source and digest,
context, integrity, and freshness verification. A caller-edited, caller-rehashed,
or presentation-only document cannot create or renew admission.

`AdmissionVerification` represents facts that a future trusted evidence reader
would establish. Constructing that data class is not itself authentication or
authority; CP-003 implements only the pure comparison predicate and no admission
reader.

## Effects, attempts, and artifacts

Collection attempts remain separate from evaluated findings so a failed/skipped
attempt is retained even when acceptable substitute evidence supplies a result.
Diagnostic effects and cleanup receipts are explicit data and cannot be inferred
from a deep flag or presentation request.

Artifact references name media type, digest, and owned source. HTML is enumerated
for audit/doctor only and remains a presentation artifact with
`admission_authority=none`, `creates_evidence=false`, and
`collects_evidence=false`.

## Evidence boundary

The schemas and deterministic fixtures test data meaning only. They do not execute
collectors, perform privileged probes, render HTML, authenticate evidence stores,
restore a backup, or evaluate production readiness. Runtime and product gate
statuses remain not evaluated unless a later qualified component produces
accepted evidence.
