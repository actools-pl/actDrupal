# Repository instructions for coding agents

Read `coding/00_START_HERE_CODER_DOCUMENTATION.md`, the active v1.5.1 architecture, the current task card and records before changing source. The repository is a fresh-install rewrite; do not import the historical implementation or add migration behavior.

## Current implemented surface

CP-001 implements only a development package skeleton and truthful `actools version` / help behavior. Do not advertise or stub installation, update, doctor, backup, restore, server, Drupal or provider operations until their bounded tasks are accepted.

## Change control

- Work from the exact task base on a named task branch and stay inside its affected-file allowlist.
- Human integration authority is separate from coding and review. Connector capability is not authorization.
- Never force-update protected history, bypass controls, publish secrets, or use project servers under a source-only task.
- Keep CPD-12 independent review: fresh Work / ChatGPT 6 Astra while available, with the approved ordinary-chat 5.6-sol fallback.

## Source checks

The canonical CP-001 check is `python tools/check_source.py` in the pinned environment documented in `docs/development/source-ci.md`. A missing scanner, dependency-resolution failure, invalid scan result or unavailable required execution is not a pass. Never rewrite expected results to make a failure green.

No CP-001 source check qualifies a production host, Drupal installation, backup/restore behavior, release signature or product-wide G gate.
