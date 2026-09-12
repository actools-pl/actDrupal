# Actools Drupal Community

Secure Drupal installation and operations toolkit being developed from the beginning in https://github.com/actools-pl/actDrupal.

**Status:** pre-alpha development. CP-001 established the minimal Python package, truthful `actools version`/help behavior, and fail-closed source CI. The current unreleased CP-002 source adds a strict data-only configuration contract library; it does **not** add an installation command, wizard, host mutation, or production-ready release.

The current product scope is fresh installations only. Existing-site migration and legacy backup imports are excluded. Backup, restore, disaster recovery and supported updates for sites created by the new installer remain planned requirements.

CP-002 configuration contract `1.0.0` supports only profile `single-site-production`. It parses strict UTF-8 JSON or the restricted Actools YAML subset, applies omission-only release defaults with explicit origins, validates the closed schema and semantic relationships, and exposes RFC 8785 canonical bytes. Contract-valid configuration is not installation or production readiness. See `docs/reference/configuration.md` and ADR-0002.

Coding Package v1.3 and the active Architecture v1.5.1 are included under `coding/`. Start with the [coder documentation](coding/00_START_HERE_CODER_DOCUMENTATION.md), the current task card, and the exact task base before changing source.
