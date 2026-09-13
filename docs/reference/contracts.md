# Contract catalog and operation contracts

CP-003 adds closed `1.0.0` boundaries for the initial requirement, operation,
result, release, evidence, and backup data. These are source-owned data contracts;
they do not implement the future components that will produce or consume them.

## Compatibility matrix

The packaged `contract-catalog-1.0.0.json` is the only registry. The table below
is a readable projection of that resource; the JSON policy remains authoritative.

| Family | Owner | Schema | Packaged policy | Read | Write | Migration edges | Artifact boundary | Mutation authority |
|---|---|---|---|---|---|---:|---|---|
| `configuration` | operator input | `configuration-1.0.0.schema.json` | — | `1.0.0` | `1.0.0` | 0 | operator input | explicit operator output |
| `plan` | planner | `plan-1.0.0.schema.json` | — | `1.0.0` | `1.0.0` | 0 | generated artifact | explicit operator output |
| `operation-journal` | protected engine | `operation-journal-1.0.0.schema.json` | — | `1.0.0` | `1.0.0` | 0 | protected store | protected writer |
| `requirement-graph` | reviewed release source | `requirement-graph-1.0.0.schema.json` | `requirement-graph-1.0.0.json` | `1.0.0` | `1.0.0` | 0 | release resource | release process |
| `release-manifest` | release process | `release-manifest-1.0.0.schema.json` | — | `1.0.0` | `1.0.0` | 0 | release resource | release process |
| `diagnostic-evidence` | collector/evaluator | `diagnostic-evidence-1.0.0.schema.json` | — | `1.0.0` | `1.0.0` | 0 | generated artifact | protected writer |
| `backup-set` | trusted recovery service | `backup-set-1.0.0.schema.json` | — | `1.0.0` | `1.0.0` | 0 | protected store | protected writer |
| `command-result` | command engine | `command-result-1.0.0.schema.json` | — | `1.0.0` | `1.0.0` | 0 | result envelope | none |
| `contract-catalog` | release process | `contract-catalog-1.0.0.schema.json` | `contract-catalog-1.0.0.json` | `1.0.0` | `1.0.0` | 0 | release resource | release process |

There is no implicit compatibility. A document whose `schema_version` is not in
the registered reader set is rejected without mutation. A future version needs a
new schema/resource identity, declared reader and writer behavior, and a real
migration edge before any migration is advertised.

## Python boundary

The public package provides:

```python
from actools.contracts import (
    canonical_contract_bytes,
    canonical_contract_digest,
    canonical_plan_payload_bytes,
    canonical_plan_payload_digest,
    load_contract_catalog,
    load_packaged_contract,
    parse_contract_bytes,
    registration_for,
    validate_contract_document,
)
```

`parse_contract_bytes(family, data)` applies strict UTF-8 JSON parsing, duplicate
key and non-finite rejection, finite data limits, version dispatch, schema
validation, semantic validation, and immutable typed-model construction.
`validate_contract_document()` provides the same boundary for an existing mapping
after copying it. The requirement graph has a larger finite aggregate-node budget
because its fixed 163 records exceed the ordinary 4,096-node contract budget.
Packaged schemas and policies pass through the same byte, depth, Unicode and
aggregate-node checks. Common-schema expansion has an independent finite budget
and rejects missing or cyclic owned references.

`canonical_contract_bytes()` uses RFC 8785. Its SHA-256 helper provides stable
identity only. Neither function authenticates the source, grants authority, or
admits evidence.

`canonical_plan_payload_bytes()` and `canonical_plan_payload_digest()` define the
single noncircular review identity. That projection includes every top-level plan
field except `review`; the excluded object is the receipt that carries the
reviewer identity, reviewed payload digest, review time and expiry. The full
contract helpers still include the receipt when a complete document identity is
needed.

## Plan and review identity

The plan is declarative. It includes:

- exact plan, operation, action, and request identities;
- required authenticated actor/approval authorities;
- protected source and destination IDs plus resolved target;
- state fingerprints and generations;
- collected/expiry times and release/configuration/policy digests;
- required capabilities and ordered described effects;
- expected and maximum disruption;
- preconditions and postconditions;
- checkpoint and rollback requirements;
- one boundary record for every irreversible effect;
- review identity, reviewed plan digest, and review validity.

The top-level action must equal the request action. Calendar-valid UTC timestamps
retain up to nanosecond precision. Plan expiry must follow collection without
exceeding the accepted fifteen-minute start-validity window; review time and
review expiry must stay inside that plan interval. The receipt's digest must equal
the canonical plan-payload digest. Maximum disruption cannot be shorter than
expected disruption, a required checkpoint needs an identity, and irreversible
effects must exactly match their boundary records. Closed schemas reject command
text, `argv`, shell fragments, unknown fields, omitted required groups, and type
coercion.

A digest is not proof of review or authority. The future executor must load the
canonical plan through its protected path, match the exact reviewed digest,
target, effects, expiry, state fingerprints, and authenticated actor/approval.
CP-003 does not implement that executor or admission step.

## Journal, result, and delivery

The operation journal owns durable mutation truth. A successful stage has no error
and every required postcondition is satisfied with a non-null evidence identity
that resolves exactly once in the journal's evidence records. Historical failed
attempts remain valid when a later attempt and independently referenced proof
establish completion. Generations cannot regress, attempt IDs and evidence
identities are unique, and reconciliation classification and its `required` flag
agree.

The command-result envelope owns reporting truth:

- `result` is exactly one typed payload;
- JSON delivery declares exactly one stdout document;
- an operation payload and its durable outcome must agree on journal, state, and
  reconciliation identity;
- command outcome follows durable state, while delivery has an independent state;
- a failed delivery names a corresponding error record;
- next actions match an exact catalog-owned action/source/documentation tuple;
- presentation metadata has `admission_authority=none`,
  `creates_evidence=false`, and `collects_evidence=false`.

Thus a successful recorded operation can coexist with failed report delivery. The
safe response is to inspect the journal or retry the delivery as registered; a
delivery error does not authorize replaying effects.

HTML is an enumerated future artifact format for `audit` and `doctor` only.
Successful delivery requires matching `text/html` artifact references. CP-003
does not provide rendering, filesystem publication, a browser, or a service.

## Backup commitment and restore proof

A backup set names its protected source, capture boundary, release/configuration,
required constituents, repository snapshot, independent encryption-key identity,
file-history/PITR applicability, constituent receipts, verification results,
retention, commit, and restore proof. For the initial single-site profile, a
committed set owns exactly one required database, public-files, private-files,
configuration, release-identity and application-secrets constituent. Each must
have a complete digest-verified receipt. The four mandatory commit flags also
resolve to distinct successful verification records.

The selected repository transport identity is `restic-rest`, representing the
independent authenticated-TLS Restic REST arrangement with append-only
`rest-server` as the accepted reference. This data value does not qualify a
backend. Any alternative transport requires its own future contract registration,
adapter and conformance evidence before it can be accepted.

Commitment and restoration answer different questions:

| State | Establishes | Does not establish |
|---|---|---|
| `commit.status=committed` | Required constituents have complete digest-verified receipts and all commit checks passed | The backup restores correctly |
| `restore_proof.status=pass` | A separately identified restore verification exists | Current freshness or future restorability |
| `restore_proof.status=not-run` | No restore proof is claimed | Failure of the already committed set |

Repository/catalog integrity and an uploaded filename do not replace a restoration
receipt.

## Requirement graph versus task ledger

The requirement graph is the release-owned product truth for F/WP/G/UX/UXS IDs,
decisions, implementation, mappings, support, and runtime evidence. The task
ledger is workflow truth for assignment, dependency sequencing, commits, reviews,
tests, and closeout. A task may be administratively complete while its product
capability remains partial or unsupported; a graph decision may be accepted while
implementation and evidence remain absent.

The CP-003 graph intentionally advertises no support and claims no runtime PASS.
Unresolved parent, dependency, relationship, test, or contract mappings stay
visible for their owning future tasks. Worker gates G11–G13 and PITR gate G17 are
conditional `future-decision` scope tied to their deferred feature families;
current backup and restore gates G14–G16 remain always applicable.

## Closed vocabularies

The action vocabulary is:

`host.initialize`, `host.prepare`, `deployment.install`,
`configuration.publish`, `credentials.rotate`, `service.restart`,
`caddy.reload`, `maintenance.transition`, `application.operator`,
`storage.probe`, `notification.probe`, `backup.capture`, `backup.verify`,
`backup.maintain`, `recovery.rehearse`, `recovery.restore`,
`recovery.promote`, `deployment.update`, `deployment.rollback`,
`management.update`, `diagnostics.probe`, and `operation.reconcile`.

The only safe next-action IDs are `collect.evidence`, `consult.runbook`,
`inspect.operation`, `reconcile.operation`, `request.authority`,
`resolve.coverage`, `retry.delivery`, and `review.plan`. They are identifiers and
documentation mappings, never executable source text.
