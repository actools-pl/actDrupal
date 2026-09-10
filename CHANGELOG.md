# Changelog

## Unreleased

### Added

- CP-001 development package skeleton for the fresh-install rewrite, with no runtime dependencies.
- Truthful `actools version [--format human|json]` and bounded help/error behavior; no installer or future command stubs are exposed.
- Narrow `Source CI` workflow and canonical source checker with pinned action identities, hash-locked tooling input, package-inventory checks and controlled negative fixtures.
- Root license/notices, contributor/agent/security guidance and the initial package/source-CI ADR.

### Known limits

- This is a development skeleton, not a working Drupal installer or release.
- Source CI is configured by this candidate but has not run on GitHub before publication.
- The CP-001 lock must be regenerated/compared with the declared pip-tools/Python environment before remote publication because the coordinator build environment could not reach the package index.
- No CP-001 result qualifies servers, Drupal behavior, restore, signing, release or product-wide security gates.
