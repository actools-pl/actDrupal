# Changelog

## Unreleased

### Added

- CP-001 development package skeleton for the fresh-install rewrite and truthful `actools version`/help/error behavior.
- CP-001 narrow `Source CI` workflow and canonical fail-closed source checker with immutable action pins, locked tooling, complete scanner-coverage policy, closed wheel shape and installed-launcher checks.
- CP-002 configuration contract `1.0.0` for the `single-site-production` profile, with Draft 2020-12 schemas, strict UTF-8 JSON and restricted Actools YAML parsing, finite resource limits, explicit semantic checks and non-reflective errors.
- CP-002 omission-only canonical defaults with deterministic JSON-Pointer origin records using only `operator` and `release_default`.
- CP-002 RFC 8785 canonical bytes for resolved configuration and resolution envelopes, with six pinned Apache-2.0 JCS conformance-vector pairs and recorded provenance.

### Changed

- The Python distribution now declares exactly three runtime dependencies: `PyYAML==6.0.3`, `jsonschema==4.26.0`, and `rfc8785==0.1.4`.
- Source/package checks now expect the `actools.contracts` subpackage and its three packaged JSON contract resources, and installed-wheel verification uses a fresh isolated venv whose dependency closure is hash-installed from the actual generated `requirements/ci.lock` before the candidate wheel is installed with dependency resolution disabled; the exact CP-001 CLI and unchanged Source CI workflow authority are preserved.

### Known limits

- This remains a development package, not a working Drupal installer or production-qualified release.
- CP-002 introduces no CLI configuration command, wizard, filesystem publication, host discovery, journal, plan/apply operation, privileged execution, secret loading/generation or network/server effect.
- The CP-002 `requirements/ci.lock` must be resolver-generated and verified by the Human-Git operator under the accepted Ubuntu Server 26.04.1 / CPython 3.14.7 / pip 26.2.1 / pip-tools 7.6.1 contract. A coding environment that cannot reproduce that environment must not fabricate the lock.
- JCS vector SHA-256 values in provenance require independent Human-Git receipt recomputation before the final candidate review.
- No CP-002 result by itself qualifies servers, Drupal behavior, restore, signing, release support or any product-wide gate.
