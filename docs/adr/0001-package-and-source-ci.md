# ADR-0001 — Minimal Python package and fail-closed source CI

Status: proposed for independent CP-001 review. Date UTC: 2026-09-10. Decision owner: human task owner MP Singh under the bounded CP-001 authorization.

## Context

CP-001 is the first implementation slice after BOOT-001. Architecture v1.5.1 §§7.3, 13.1–13.6 and 18.5 slice 1 require a clean development package, owned source checks and truthful version/help behavior without importing the historical implementation or implying later installer support.

Live activation used repository `actools-pl/actDrupal` at exact base `dce4e44b13ab19c65d8e9b67243bfeb72a15cdb2`, tree `e189ff949ba8ff79de2302d5e8150ef8838077e3`. At activation there was no `.github/workflows/` directory, no source workflow run/status context, and detailed branch-protection inspection remained unavailable to the connector (403) although `main` was observed protected.

## Decision

- Distribution: `actools-drupal`; Python import package: `actools`; development version: `0.1.0.dev0`.
- Runtime dependencies: zero. Supported package metadata is Python `>=3.14,<3.15`; source CI is pinned to CPython 3.14.7.
- The only command behavior introduced is `actools version [--format human|json]` plus help and honest unsupported-command errors. No deferred operation is stubbed or advertised.
- Source CI is `.github/workflows/source-ci.yml`, triggered only by pull requests to `main` and pushes to `main`, on GitHub-hosted `ubuntu-24.04`, with repository permission limited to `contents: read`.
- External actions are immutable SHA pins: checkout `3d3c42e5aac5ba805825da76410c181273ba90b1` and setup-python `5fda3b95a4ea91299a34e894583c3862153e4b97`; checkout credentials are not persisted.
- The canonical command is `python tools/check_source.py`. Required scanner execution fails closed on unavailable execution, collection error, malformed output or vulnerabilities.
- Direct source tools are setuptools 84.0.0, build 1.6.0, pytest 9.1.1, pip-audit 2.10.1 and pip 26.2.1. Lock-generation tooling is pip-tools 7.6.1 in a separate environment. The current hash lock targets CPython 3.14.7 / Ubuntu 24.04 x86_64 and permits wheels only.
- A source check name is not configured as a protected required status check in CP-001. Any repository-setting change follows a later separate human decision after the real check name and behavior are observed.

## Alternatives and reasons

| Alternative | Benefit | Cost/risk | Reason for disposition |
|---|---|---|---|
| Import historical runtime | Fast apparent progress | Violates fresh rewrite boundary and imports unreviewed assumptions | Rejected |
| Add future CLI stubs | Shows roadmap | Misrepresents support and weakens truthful UX | Rejected |
| Use floating action tags/dependencies | Simpler updates | Mutable CI inputs | Rejected |
| Use `ubuntu-26.04` as sole source runner | Matches later OS family | Runner was not chosen as a stable source-CI baseline for this slice; source CI is not host qualification | Deferred |
| Give workflow write/OIDC permissions | Enables future release actions | Unnecessary authority for source checks | Rejected |

## Consequences, compatibility and transition

CP-002 may build on the installed Python package but must not infer any installer operation from CP-001. Historical reference documents remain excluded from runtime artifacts. Dependency updates must regenerate the lock, record licenses and rerun source checks. A later installed slice supplies release-test evidence; CP-001 does not.

Direct tool license metadata reviewed for this slice: setuptools MIT, build MIT, pytest MIT, pip MIT and pip-audit Apache-2.0. Transitive packages remain governed by their upstream licenses; their exact pinned names are recorded in `requirements/ci.lock` and require license/provenance review with any lock change.

## Verification

Required: exact-environment canonical source check; unit tests; controlled negative test and invalid-package build; wheel inventory; clean installed CLI behavior; workflow static controls; fail-closed vulnerability audit. The candidate coordinator environment did not provide CPython 3.14.7 or package-index network access, so exact-environment build/audit and pip-tools lock regeneration are pending rather than inferred from inspection.

## Authority and traceability

Task: `coding/tasks/CP-001.md`. Human authorization: bounded CP-001 activation decision in the coordinator conversation, 2026-09-10. Review route: CPD-12. Architecture anchors: v1.5.1 §§7.3, 13.1–13.6, 18.5 slice 1; G01/G09/G22 and UX-R05/R06/R14 are requirement anchors, not gates passed by this ADR.
