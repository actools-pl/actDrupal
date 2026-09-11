# Configuration contract 1.0.0

CP-002 defines a **data-only** configuration contract. A document that passes this contract is structurally and semantically valid for later Actools consumers; it is not proof that installation, a selected capability, a host or production is ready.

## Identity and supported profile

- Contract: `1.0.0`
- Schema dialect: JSON Schema Draft 2020-12
- Profile: `single-site-production` only
- Inputs: UTF-8 JSON or the restricted Actools YAML subset
- Canonical bytes: RFC 8785 JCS

The resolved object has these closed groups: `schema_version`, `profile`, `installation`, `site`, `environment`, `platform`, `capabilities`, `host`, `drupal`, `recovery`, `monitoring`, `secrets`, and `references`. Unknown fields fail.

The only selectable capability identifiers represented by this contract version are `valkey-cache` and `cloudflare-standard-proxy`. They describe requested configuration relationships only; later owners must independently implement and qualify them.

## Strict JSON

JSON parsing is bytes-first. The parser enforces the 1 MiB cap before decode, requires strict UTF-8 and one JSON document, detects duplicate object keys before dictionary collapse, rejects `NaN`/`Infinity` and overflow to non-finite values, rejects lone/invalid Unicode surrogates, and restricts native integers to `-9007199254740991..9007199254740991`. Fields declared as integer require the native integer model; integral floats such as `60.0` are not accepted as integer configuration values. Comments, trailing data and extensions are not accepted.

## Restricted Actools YAML

YAML is a convenience syntax for the same JSON-compatible model, not a general YAML configuration language. PyYAML 6.0.3 supplies scanning/parsing only; Actools owns scalar meaning.

Accepted plain non-string forms are exactly lowercase `null`, `true`, `false`, and JSON-number lexical forms. Quoted scalars stay strings. Ordinary safe unquoted text stays string.

Rejected forms include anchors/aliases, tags, merge keys, directives, multiple documents, duplicate/non-string keys, `~`, implicit empty nulls, `yes/no/on/off` variants, date/timestamp/time implicit forms, hexadecimal/octal/binary/sexagesimal/underscore numbers, `.nan`/`.inf`, leading-zero numeric forms, leading-plus/trailing-dot/dot-leading numeric extensions, and block scalar styles.

## Resource limits

| Limit | Value / convention |
|---|---:|
| Input bytes | 1,048,576 |
| Container nesting | 32; root mapping/sequence is level 1 |
| Mapping entries | 256 per mapping |
| Sequence elements | 256 per sequence |
| Aggregate nodes | 4,096 |
| Ordinary string | 16,384 Unicode scalar values |
| Native integer | I-JSON safe range above |

Aggregate-node accounting counts every container/scalar value and every mapping-key scalar.

## Owned formats and semantic checks

Draft 2020-12 format assertions are active. The finite checker set contains only:

- `actools-domain`: lowercase DNS-style multi-label domain;
- `actools-endpoint`: DNS/IPv4 `host:port` or bracketed IPv6 `[address]:port`;
- `actools-filesystem-authority-id`: `fs-auth:<identifier>`;
- `actools-secret-reference`: `secret://<scope>/<name>`.

A schema format not in that registry fails schema-quality tests.

Cross-field validation requires:

- `drupal.cache.mode=valkey` exactly when `valkey-cache` is selected;
- `drupal.ingress.mode=cloudflare-standard` exactly when `cloudflare-standard-proxy` is selected;
- enabled email/Telegram notification channels to carry a secret reference;
- disabled notification channels to carry `null`, not a retained credential reference.

Secret values themselves are out of contract. `secrets.database_credentials` and notification credentials are references only. Rejected values are never echoed in error text.

## Defaults

Defaults are data in `configuration-defaults-1.0.0.json`, not JSON Schema mutation. They apply only to omitted fields. Explicit `null`, `false`, `0`, empty string or empty container is never replaced by a default; if that explicit value violates the schema it fails later validation.

Version 1.0.0 release defaults include the accepted Ubuntu/Docker Compose platform references, database cache, direct Caddy ingress, local Drupal public/private storage, empty capability selection, production environment type, accepted access-policy identifiers, RPO 60 minutes, RTO 240 minutes, health/security/deep-diagnostic cadences 5 minutes/24 hours/7 days, and disabled/null email and Telegram notification channels.

## Origin map

Resolution returns a detached resolved configuration plus a deterministic JSON-Pointer-keyed origin map. Entries exist for every scalar leaf and every empty mapping/sequence leaf in the resolved configuration; non-empty containers do not receive their own entry.

Operator-present values use:

```json
{"origin":"operator"}
```

A release-default value uses:

```json
{
  "origin":"release_default",
  "default_set":"configuration-defaults-1.0.0",
  "default_set_version":"1.0.0"
}
```

No `policy_default` exists in this contract version.

## Canonical bytes

`ResolvedConfiguration.canonical_configuration_bytes()` returns RFC 8785 bytes for the resolved configuration. `canonical_resolution_bytes()` canonicalizes the envelope containing the resolved configuration and origin map. Canonicalization is pure data processing and performs no publication, journal, secret, environment, subprocess or network operation.

## Bounded errors

`ConfigurationError` reports an owned JSON-pointer-like path and a reason code only. Raw parser failures fall back to `/` if reaching an unowned input key, and wrapped parser/canonicalizer failures suppress reflective exception chains. Rejected values are not interpolated, preventing secret-canary and terminal-control reflection.
