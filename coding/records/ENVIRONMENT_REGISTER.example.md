# Environment register — example to complete privately

**Example only. No servers, credentials or test results are registered by this file.** Copy to a controlled working record when the environments are actually created. Keep the public repository copy limited to aliases/non-sensitive metadata; keep addresses, account details and recovery custody references private when required. Never record secret values.

## Environment rows

| Field | DEV-01 | RELEASE-TEST-01 | LAPTOP-CONTROLLER |
|---|---|---|---|
| Role | Mutable development / destructive tests | Reviewed candidate qualification | Administration / initial attended external tests and backup control |
| Provider / account boundary | Hetzner; actual account to record | Hetzner; record whether same account | Operator controlled; actual device to record |
| Provider server ID / private inventory reference | UNSET | UNSET | Not a cloud server |
| Hostname / address reference | UNSET | UNSET | UNSET |
| OS / image / CPU architecture | Verify against v1.5.1 profile | Verify against v1.5.1 profile | Record actual OS; Bash Git environment if used |
| Image/rebuild generation and UTC date | UNSET | UNSET | UNSET |
| Current boot identity when relevant | UNSET | UNSET | UNSET |
| Installed candidate / artifact digest | NONE | NONE | Tool versions only when configured |
| Current Git checkout / SHA | NONE | No development checkout required | UNSET; direct GitHub use alone creates no local checkout |
| GitHub source delivery route / operation-record reference | Human transfers or narrowly scoped read only | Verified artifact transfer only | UNSET; human-Git or authorized connector route, with actual capability and repository/ref recorded |
| Source/build cleanliness and retained diagnostic edits | UNSET | Qualified artifact build receipt required | UNSET |
| Effective SSH agent/X11 forwarding | Disabled; verify session | Disabled; verify session | Verify each test-host connection |
| Sensitive mounts / credential sockets / undeclared tunnels | Prohibited | Prohibited | No exposure to test hosts |
| Source/artifact transfer and restricted credential reference | UNSET; no personal write token | UNSET; no personal write token | Trusted transfer identity; no secret values |
| Permitted external egress / observer paths | Task-specific | Task-specific | Record declared test endpoints |
| Test data profile / size / synthetic? | UNSET | UNSET | UNSET |
| Current task / active operation | NONE | NONE | NONE |
| Recovery console verified date / procedure reference | NOT VERIFIED | NOT VERIFIED | Device recovery reference |
| SSH host fingerprint / trusted verification reference | UNSET | UNSET | Client key custody reference only |
| Backup/controller role and independent key custody | No historical repository keys by default | No historical repository keys by default | Initial attended controller; qualify actual setup |
| Independent external observer | UNSET | UNSET | Record IPv4/IPv6 availability |
| Reset permission / retained data | Per concrete human-reviewed reset | Per concrete human-reviewed reset | Not disposable by this plan |
| Cleanup / outstanding risk | UNSET | UNSET | Sleep/connectivity restrictions to record |

## Shared limitations and change record

- Two servers under one provider/account do not establish provider/account-loss independence.
- A laptop controller is attended development infrastructure until its actual availability is qualified. Offline periods do not satisfy production recovery or monitoring objectives.
- Record relevant firewall topology, attached storage, snapshot use and external endpoints in the private inventory. A target rebuild does not automatically remove attached/external resources.
- After rebuild, rotate/re-provision appropriate test credentials, verify host identity and invalidate old boot/state-specific receipts. Preserve historical evidence.
- Provider tokens remain under the human control-device custody procedure. GitHub write authority is held by the trusted human client or the authorized connector credential store; do not export connector tokens or copy personal write credentials to either test host. A test-only read credential, if actually necessary, has narrow authority and an explicit revoke/custody procedure; do not use a forwarded broader agent. GitHub capability grants no provider or server authority.
- Production/customer credentials and real customer content are prohibited in these development environments unless a later separately documented authorized handling plan changes that boundary.

| UTC date | Environment / old → new generation | Reason / authorized human | Source/artifact | Exported evidence / data disposition | Outstanding checks |
|---|---|---|---|---|---|
| UNSET | UNSET | Example only | NONE | NONE | Registration required |
