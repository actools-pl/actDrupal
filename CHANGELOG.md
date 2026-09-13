# Changelog

## Unreleased

### Added

- CP-001 development package skeleton for the fresh-install rewrite and truthful `actools version`/help/error behavior.
- CP-001 narrow `Source CI` workflow and canonical fail-closed source checker with immutable action pins, locked tooling, complete scanner-coverage policy, closed wheel shape and installed-launcher checks.
- CP-002 configuration contract `1.0.0` for the `single-site-production` profile, with Draft 2020-12 schemas, strict UTF-8 JSON and restricted Actools YAML parsing, finite resource limits, explicit semantic checks and non-reflective errors.
- CP-002 omission-only canonical defaults with deterministic JSON-Pointer origin records using only `operator` and `release_default`.
- CP-002 RFC 8785 canonical bytes for resolved configuration and resolution envelopes, with six pinned Apache-2.0 JCS conformance-vector pairs and recorded provenance.
- CP-003 closed contract catalog and immutable typed `1.0.0` models for plans, operation journals, release manifests, diagnostic evidence, backup sets and command results.
- CP-003 canonical 163-node architecture requirement graph, with decision, implementation, advertised-support, mapping and runtime-evidence states kept separate and all support claims initially false.
- CP-003 deterministic diagnostic evaluator with separate selected/full-required coverage, explicit gate/run states and fixed `3 > 2 > 1 > 0` audit/doctor exit precedence.

### Changed

- The Python distribution now declares exactly three runtime dependencies: `PyYAML==6.0.3`, `jsonschema==4.26.0`, and `rfc8785==0.1.4`.
- Source/package checks now expect the `actools.contracts` subpackage and its three packaged JSON contract resources, and installed-wheel verification uses a fresh isolated venv whose dependency closure is hash-installed from the actual generated `requirements/ci.lock` before the candidate wheel is installed with dependency resolution disabled; lock verification also fails closed unless the generated header records the exact accepted normalized compile command without `--no-index` and the frozen dependency/hash body is unchanged. The exact CP-001 CLI and unchanged Source CI workflow authority are preserved.
- CP-002 strict validation now rejects scoped/control-bearing endpoints, requires true end-of-input for owned identifiers/references, keeps endpoint port parsing total under extreme input, closes the reviewed YAML implicit-type lexical gaps, and enforces direct-mapping depth limits before recursive copying.
- Contract packaging now closes over 30 wheel members: eight contract modules, eleven schema/default resources, two policy resources, the existing CLI/package modules, and seven distribution metadata/license members. Runtime dependencies and the Source CI workflow remain unchanged.

### Known limits

- This remains a development package, not a working Drupal installer or production-qualified release.
- CP-002 introduces no CLI configuration command, wizard, filesystem publication, host discovery, journal, plan/apply operation, privileged execution, secret loading/generation or network/server effect.
- The historical r2 coding delivery omitted `requirements/ci.lock` by design. Every CP-002 review candidate must instead contain a resolver-generated lock and retained Human-Git receipts from the accepted Ubuntu Server 26.04.1 / CPython 3.14.7 / pip 26.2.1 / pip-tools 7.6.1 contract. A correction coding environment that cannot reproduce that environment must leave lock regeneration to Human-Git rather than fabricate or hand-edit it.
- JCS vector SHA-256 values in provenance require independent Human-Git receipt recomputation before the final candidate review.
- No CP-002 result by itself qualifies servers, Drupal behavior, restore, signing, release support or any product-wide gate.
- CP-003 provides no executor, collector, renderer, scheduler, release signer, admission reader or server effect. HTML is an enumerated audit/doctor artifact contract only; graph and unit results advertise no capability support and establish no runtime or product-wide gate.
