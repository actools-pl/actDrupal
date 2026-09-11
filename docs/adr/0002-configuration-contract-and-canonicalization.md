# ADR-0002 — Strict configuration contract and RFC 8785 canonicalization

Status: **candidate for independent CP-002 review; not accepted, merged or published by this coding delivery.**

## Context

CP-002 is the first WP02 configuration-contract slice after the accepted CP-001 package/source-CI baseline. Architecture v1.5.1 requires one canonical data model, strict schema ownership, omission/null/false fidelity, explicit default origins and identical data for later preview/authorization/apply consumers. This slice must remain a pure library: it adds no CLI command, wizard, host discovery, filesystem publication, journal, plan/apply operation, privileged execution, secret loading/generation or network/server effect.

The activation `CP002-ACT-32ecc89-v1` fixes configuration contract `1.0.0`, Draft 2020-12, profile `single-site-production`, RFC 8785 and runtime dependencies `PyYAML==6.0.3`, `jsonschema==4.26.0`, `rfc8785==0.1.4`.
The reviewed `rfc8785` tag `v0.1.4` resolves to upstream commit `4d9b161f6054301d98d0566e813d020fb019ee10`; the dependency is consumed as a pinned package, not vendored source.

## Decision

### One bounded configuration shape

The contract uses these closed groups:

- `schema_version`, `profile`;
- `installation.id`;
- `site.id`, `site.domain`;
- `environment.id`, `environment.type`;
- `platform.os_profile`, `platform.runtime_backend`;
- `capabilities.selected_ids` with only `valkey-cache` and `cloudflare-standard-proxy` in this version;
- `host.management_endpoint`, `host.filesystem_authority_id`, and the three accepted access-policy identifiers;
- `drupal.storage`, `drupal.cache.mode`, `drupal.ingress.mode`;
- `recovery.rpo_minutes`, `recovery.rto_minutes`;
- `monitoring` cadence plus `email`/`telegram` notification enable/reference records;
- `secrets.database_credentials` as a reference only;
- `references.policy`, `references.release`.

Every object is closed with `additionalProperties: false`. The schema expresses structure; `configuration.py` owns the finite cross-field checks: Valkey mode and capability must agree, standard Cloudflare ingress and capability must agree, an enabled notification requires a secret reference, and a disabled notification cannot retain one. These relationships assert configuration consistency only; they do not claim the capability is implemented or production-qualified.

### Strict parser boundary

JSON is bytes-first strict UTF-8 with duplicate-key detection before dictionary collapse, non-finite rejection, safe-integer bounds and a Unicode-scalar walk. Restricted YAML uses PyYAML only for syntax/tokens/events. Actools constructs the data model itself and rejects anchors, aliases, tags, merges, directives, multiple documents, duplicate/non-string keys, implicit empty nulls, YAML 1.1 boolean variants, dates/timestamps, non-finite values and YAML-only numeric forms. Quoted YAML remains string; only lowercase `null`/`true`/`false` and JSON-number lexical forms receive non-string types.

Resource limits are fixed at 1 MiB input, 32 container levels (root container is level 1), 256 entries/elements per mapping/sequence, 4,096 aggregate nodes, 16,384 Unicode scalar values per ordinary string and the I-JSON safe native integer range ±9,007,199,254,740,991. Schema `integer` fields use a strict native-integer type checker, so integral floats are not silently accepted as integers. Aggregate nodes count each container/scalar and every mapping-key scalar.

Errors expose only an owned JSON-pointer path plus a bounded reason code; raw parser failures fall back to `/` when an unowned key would otherwise be reflected, and wrapped parser/canonicalizer failures suppress underlying exception chains. Rejected values are never echoed.

### Format assertion

Draft 2020-12 validation uses an explicit `FormatChecker` whose registry is reduced to four Actools-owned formats: domain, endpoint, filesystem-authority ID and secret reference. Schema-quality validation fails if any other format name appears.

### Defaults and origins

JSON Schema `default` is not used for mutation. `configuration-defaults-1.0.0.json` is the sole release-default source. Defaults apply only where a field is omitted; explicit null/false/zero/empty values are preserved and may then fail the schema if invalid. The operator input is never modified in place.

Origins are a deterministic JSON-Pointer map for every resolved scalar leaf and every empty mapping/sequence leaf. Operator-present values receive `{"origin":"operator"}`. Release-default values additionally identify `configuration-defaults-1.0.0` and default-set version `1.0.0`. No `policy_default` source is invented.

### Canonical bytes and vectors

Canonical output is `rfc8785.dumps()` bytes for parser/validator-bounded I-JSON-compatible data, for both the resolved configuration and `{configuration, origins}` resolution envelope. Ordinary `json.dumps(sort_keys=True)` is not treated as canonicalization.

Six byte-for-byte published vectors are vendored from `cyberphone/json-canonicalization@19d51d7fe467d4706a3ff08adf8a748f29fc21e0`: arrays, french, structures, unicode, values and weird. Their Apache-2.0 provenance and byte receipts are recorded beside the fixtures. The upstream 100-million-number corpus is not vendored.

### Package/source-CI transition

The distribution still has version `0.1.0.dev0` and the CP-001 CLI remains untouched. The wheel grows from nine members to a closed sixteen-member shape: the two CP-001 Python files, four contract Python modules, three schema/default JSON resources and the same seven distribution metadata/license members. Runtime metadata must contain exactly the three accepted runtime pins. `.github/workflows/source-ci.yml` remains byte-for-byte the CP-001 workflow; the checker and lock inputs evolve underneath that unchanged authority.

## Consequences and evidence boundary

Configuration validity is not installation/production readiness. No host, Drupal, backup, restore, release-signing or product-wide gate is established by this ADR.

The final CP-002 review subject must contain a real resolver-generated `requirements/ci.lock` produced under the accepted Ubuntu Server 26.04.1 x86_64 / CPython 3.14.7 / pip 26.2.1 / pip-tools 7.6.1 contract. This coder environment did not provide that accepted generation environment, so the lock remains an operator-generated final-candidate item rather than a hand-written artifact.

The vector receipt values are present for deterministic source testing, but the packet-required Human-Git independent digest recomputation is still an evidence obligation before final review.
