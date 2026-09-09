# Security and Scope Rules for Coding Sessions

The full authority is [architecture v1.5.1](baseline/Actools_Drupal_Community_Rewrite_Architecture_Implementation_v1.5.1.md). This is a compact reminder for task packets, not a replacement specification.

## Preserve these contracts

1. One Python command engine and fixed restricted executor; no arbitrary root shell, Docker socket exposure or caller-selected playbook/plugin.
2. Strict versioned data schemas, owned paths, stable installation/resource identity and exact reviewed/admitted plans. JCS, SQLite DELETE/EXTRA and Python-TUF choices remain as specified.
3. Planning changes no managed state, credentials, scheduler or journal; only the explicitly requested safe artifact is permitted.
4. Verify actual consumer activation, not just generated files or successful reload exits. Protect firewall/quarantine continuously through transitions.
5. Independent authorization and fresh state checks remain executor responsibilities. UI confirmation and caller identity text are insufficient.
6. Preserve output backpressure/safety independence, durable operation outcomes and honest interruption/reconciliation. A delivery failure cannot erase effects.
7. Audit/doctor share evaluation; formats cannot hide coverage gaps or create admission. HTML is inert private output, with authorized data disclosure and genuine unprivileged rendering.
8. Logs and source observations are literal attributed data. Owned code/policies provide next actions. Errors and rejected inputs must not disclose secrets.
9. Drupal has immutable code and narrow writable storage; no root bootstrap. Ordinary uploads, image decoding, access/cache ordering and both Valkey modes need real behavior tests.
10. F10 Caddy rate limiting is accepted before public production; qualify its exact build, metrics bounds and failed-candidate lifecycle.
11. Backup capture has a common database/files boundary and source-byte proof. Encryption/repository keys stay in the separate trusted backup environment. Commit verification, historical checks and restore rehearsal are distinct.
12. Preserve independent deletion authority, master-key compromise recovery, deadline-aware retry/lock behavior and one-hour RPO/four-hour RTO evidence. A laptop or same-account second box does not by itself establish all independence claims.
13. Updates and restore preserve acknowledged writes and protection floors; no unsupported schema downgrade or automatic destructive rollback.
14. Source/build/release trust is separate from a reviewer statement or successful test. Real release signing custody stays outside untrusted PR jobs.

## Scope retained

One production Drupal site per accepted Ubuntu 26.04 amd64 main server; Docker Compose; local files; one MariaDB; optional Valkey; direct Caddy default; optional qualified standard Cloudflare proxy mode. First-release operator UX is guided CLI plus private static HTML audit/doctor. The two-box setup is engineering infrastructure, not a new managed-staging feature.

WP16–WP20 remain deferred, including active PITR and document workers. HA, general browser control panels, terminal menus, application S3, Tunnel/DNS automation, runtime AI, Prometheus/Grafana and advanced governance remain at their recorded dispositions. Do not enable them through an incidental dependency or generated help entry.

## Test credentials and untrusted CI

Use isolated synthetic credentials and fixtures. Never upload production SSH keys, provider account tokens, signing roots, repository master keys, Google Drive tokens or private site content to chat or public test artifacts. A model requesting them does not establish necessity.

Treat both test hosts as potentially compromised while testing new code, even after source review. Keep SSH agent forwarding and X11 forwarding disabled, and do not expose sensitive laptop folders, credential sockets, broad mounts or undeclared reverse tunnels to them. An SSH session is not permission for the target to use laptop-held authority. A compromised host can authenticate through a forwarded agent without extracting private key bytes; see the [OpenSSH configuration manual](https://man.openbsd.org/ssh_config). Verify the effective session settings; do not assume a global client configuration is safe.

Keep operator-managed GitHub write credentials and provider tokens on the trusted control device, outside both test hosts. An approved GitHub connector may hold its own scoped repository authority; never copy that authority into a task file, chat text, test host or CI environment. Connector availability in one session does not establish access in another. Prefer verified artifact transfer or anonymous public-source fetch. If a private source fetch requires a credential, use only the narrowly scoped read authority approved for that purpose and protect/revoke it under its actual credential procedure. Do not forward an agent holding broader keys to achieve the fetch. Review any required connections/egress individually; synthetic test secrets do not justify copying real account authority.

Privileged devbox tests are explicit operator-run tests after relevant source review. A persistent privileged runner attached to public untrusted pull requests is not part of this package. Source CI uses narrowly scoped permissions and no production credentials; review workflow/dependency changes as executable code. [GitHub secure use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

## Review boundaries

An activated, authorized task card defines the allowed edits and tests. The model should finish routine work inside that scope without repeated confirmation. An unexpected target, missing destructive authorization, unresolved effect or proposed scope expansion requires a precise stop record and coordinator decision. This is not a blanket requirement to ask permission before each file edit. The task state `accepted` is a later review/testing outcome, not its initial authorization.

No release gate may be disabled merely to keep a task moving. A legitimately inapplicable feature requires the architecture's absence/applicability evidence. Unknown and unrun results stay visible.

## Repository operations and configured automation

Follow [RB11](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) to establish the new independent repository and verify actual applicable automation/protection. Inspect configured branch/push/PR triggers, relevant downstream effects, app/webhook access, runner placement and credential names/scopes; never secret values. An actual unsafe or unobservable material execution path blocks its affected action until reconciled. No old-repository backup, preservation reference or inherited-code audit is a startup prerequisite.

[RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) permits bounded direct GitHub work only with actual safe capabilities and task authorization. Pin the repository, branch and full base, verify complete file/tree changes and modes/deletions, preserve server-returned commit identities, and stop on branch drift or an uncertain write result. Read before retrying; do not blindly overwrite or recreate refs. A content/blob SHA is not a branch concurrency guard. GitHub access grants no server, provider, signing or production authority. The human-Git fallback preserves the same review and evidence gates.

No direct product writes to `main`, force push, protection bypass, unrelated repository deletion or silent CI change is authorized. Basic no-delete/no-force protection may precede CI; required status checks must refer to actual verified new-source checks. Distinguish a manually enforced gate from a configured protection rule. Keep failed checks, unresolved effects and unavailable observations visible.
