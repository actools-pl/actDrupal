# ADR-0003 — Canonical requirement graph and contract boundaries

Status: **CP-003 implementation candidate; not yet independently reviewed, merged, or product-qualified.**

## Context

Architecture v1.5.1 requires one source-owned requirement graph and independently
versioned contracts before execution handlers are built. Decision acceptance,
implementation, advertised support, and runtime evidence are different facts. A
schema, task card, or passing source test must not turn an unimplemented capability
into supported product behavior.

The same boundary is needed for operational data. Plans are declarative review
artifacts, journals are protected durable state, evidence records observations and
evaluation, command results report both the underlying outcome and delivery, and a
backup commit is not a restore rehearsal.

CP-003 is still a source-only slice. It introduces no executor, collector, renderer,
release signer, scheduler, server effect, or admission authority.

## Decision

### One catalog owns versions and vocabulary

`contract-catalog-1.0.0.json` is the only reader/writer and policy-resource
registry. It owns nine families, the 22 accepted action identifiers, the four
diagnostic formats, and eight safe next-action identifiers. Every current reader
and writer version is `1.0.0`; there are no migration edges. Unknown future
versions fail before schema construction and the caller's input is never mutated.

Each schema is JSON Schema Draft 2020-12, closes every owned object with
`additionalProperties: false`, and is evaluated through the existing strict type
and format boundary. RFC 8785 canonical bytes supply identity, not authenticity.
Schema defaults do not populate contract values.

### The graph is release source, not runtime evidence

The packaged graph contains the complete architecture inventory:

| Kind | Count |
|---|---:|
| Feature (`F01`–`F75`) | 75 |
| Work package (`WP01`–`WP25`) | 25 |
| Gate (`G01`–`G22`) | 22 |
| UX requirement (`UX-R01`–`UX-R18`) | 18 |
| UX security refinement (`UXS-01`–`UXS-08`) | 8 |
| UX security case (`UXS-C01`–`UXS-C15`) | 15 |
| **Total** | **163** |

The canonical graph is bound to architecture version `1.5.1` and its exact
SHA-256. Every node has source, ownership, parent/dependency/relationship mapping
state, decision and implementation status, applicability, tests, contract mapping,
and runtime evidence. Unresolved mappings remain explicit. No node advertises
support in this slice, and every runtime-evidence status is `not-evaluated`.

Graph validation rejects duplicate IDs, unknown references, dependency cycles,
unowned nodes, wrong ID/kind relationships, falsely implemented deferred scope,
evidence-free PASS, and support claims that are not implemented, evidenced,
fully mapped, and profile-qualified.

The canonical graph additionally binds worker gates G11–G13 and PITR gate G17 to
their conditional `future-decision` feature scope. It keeps the current backup and
restore gates G14–G16 unconditionally applicable. A deferred feature therefore
cannot become a current-profile obligation merely because its gate exists.

The graph and the coding ledger have different authority:

- the graph owns product requirement/capability meaning and support truth;
- the task ledger owns work sequencing, workflow state, candidate/review/evidence
  references, and administrative closeout;
- neither is allowed to silently overwrite or infer the other.

### Contracts preserve ownership boundaries

- A plan contains exact request/action identity, actor requirements, protected
  resources, target, fingerprints and generations, validity times, context
  digests, effects, disruption, checks, recovery, irreversible boundaries, and
  review identity. It contains no command text or executable payload. Its review
  binds the RFC 8785 digest of every plan field except the review receipt itself,
  eliminating a circular self-hash while retaining every significant target,
  authority, effect and state field.
- An operation journal is written by the future protected engine and records
  intent, actor, locks, generations, attempts, deadlines, handler,
  postconditions, evidence, error, reconciliation, and cleanup. Succeeded required
  postconditions resolve to unique journal evidence records; a success label alone
  is insufficient.
- A diagnostic-evidence document separates collection attempts, factual finding
  observation/status, severity, run state, selected coverage, full required-policy
  coverage, gate disposition, effects/cleanup, and provenance. Dependency
  resolution can make the final status UNKNOWN without deleting valid raw
  observation facts.
- A backup set separates constituent/commit checks from the later restore proof.
  `committed` requires the complete owned single-site constituent inventory,
  digest-verified receipts and successful records for all four commit checks. The
  selected transport is the independently hosted authenticated-TLS Restic REST
  boundary; this representation is not backend qualification.
  `restore_proof.status=not-run` remains valid and does not become PASS.
- A command result contains one structured result, one JSON stdout-document count,
  durable operation outcome, independent delivery status, redacted errors,
  evidence references, catalog-owned next actions, and presentation metadata.
  Delivery failure cannot rewrite a verified durable operation outcome.
- A release manifest records immutable release inputs and compatibility claims but
  cannot bootstrap its own trust. Advertised profiles require a qualification
  receipt; signature/trust-root verification remains external.

### Evaluation is pure; admission remains external

`evaluate_diagnostics()` consumes already-collected immutable inputs and performs
no discovery or effects. It calculates both denominators independently, sorts
findings deterministically, preserves known failures, and assigns audit/doctor
exit precedence `3 > 2 > 1 > 0`. Missing or otherwise incomplete proof cannot
produce PASS. Optional unknowns can make a run partial without making full
required-policy coverage incomplete.

The same evaluator semantics validate serialized results. Required blockers
survive a narrower selection, selected optional blockers are explicit, every gate
is tied to actual policy evaluation, empty required inventories cannot pass, and
engine errors force the gate to `not_evaluated`. Prerequisite identifiers form a
validated acyclic graph; an unsatisfied prerequisite makes its dependent UNKNOWN
without suppressing independent findings.

Presentation is never an admission source. The admission helper is only a pure
prerequisite predicate over provenance plus facts established by a future trusted
evidence reader; it does not authenticate those facts. Exact source and digest,
authenticated origin, context, integrity, and freshness must all match outside
the presentation path.

`html` is registered only for `audit` and `doctor`. A successful HTML delivery
must carry the same owned `text/html` artifact reference in delivery and
presentation metadata. An undelivered result cannot claim a published artifact.
No renderer or publication helper is implemented here.

Packaged schema and policy resources pass through the strict byte, depth, Unicode
and aggregate-node limits before use. Common-reference expansion has a separate
finite budget and rejects cycles. The larger reviewed graph keeps its explicit
32,768-node allowance.

## Consequences

Later handlers have closed, typed inputs instead of permissive dictionaries.
Compatibility changes require a catalog/schema version and an explicit migration
edge before a reader or writer claims them. Consumers can distinguish operation
success from output failure, historical backup commitment from restore proof, and
factual findings from coverage or policy decisions.

The cost is deliberate verbosity: fields that are not known are represented as
unknown, not evaluated, partial, or unresolved rather than omitted or inferred.
This is required to prevent false support and false evidence.

Source tests establish parser/model/schema behavior only. They do not establish
an installed Drupal system, executor safety, diagnostic collection, HTML
rendering, backup restoration, release authenticity, or any product-wide gate.
