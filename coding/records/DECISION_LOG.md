# Decision log

**Current revision:** 8 September 2026. User instructions govern scope; current product authority is Architecture v1.5.1. Decisions do not constitute executed implementation or repository/server actions.

| ID | Status | Decision | Authority and effect |
|---|---|---|---|
| CPD-01 | Retained | Ordinary ChatGPT outside Work/Projects; requested 5.6 sol / Extra High | Existing accepted operator workflow. Record the actual displayed setting once; reuse supplied session information. |
| CPD-02 | Retained | Disposable Hetzner devbox and separate release-test server | Existing accepted two-box workflow; independent production backup/monitoring still require qualification. |
| CPD-03 | Retained | GitHub stores authoritative source and project records | Exact commits, artifacts and evidence identify work; chat is supplementary. |
| CPD-04 | Retained | Laptop supports administration and controlled independent exercises | No assumed always-on service or selected Google Drive backend. |
| CPD-05 | Superseded in part | Original v1.5 baseline becomes historical provenance; v1.5.1 is active | New user repository and fresh-only scope decisions incorporated; remaining applicable product controls retained. |
| CPD-06 | Retained | Code, review, meaningful tests, documentation and handoff form one outcome | No package-level check establishes product readiness. |
| CPD-07 | Superseded | Earlier existing-repository/legacy-ancestry workflow retired | New repository decision replaces its URL, base, branches and preservation gates. |
| CPD-08 | Retained | Bounded direct GitHub operations where verified; human-Git fallback | Task scope, exact identities and human integration authority remain. |
| CPD-09 | Superseded in part | Earlier mandatory legacy preservation/containment startup retired | RB11 now checks the new repository, first commit and applicable current automation. |
| CPD-10 | Accepted | Independent new repository https://github.com/actools-pl/actDrupal | User's current request; fresh root history, main integration, task branches. No inherited source/history/base. |
| CPD-11 | Accepted | Fresh installations only; no existing-site migration or legacy backup import | User's explicit follow-up. Supersedes C05/D13 migration inclusion, F36 age reader and associated task/case applicability. Own-site lifecycle/recovery remains. |

BOOT-000 is the bounded new root-commit step; BOOT-001 imports this process; CP-001 starts the implementation skeleton. CP-038/039 are cancelled scope identifiers, never reused for unrelated work or treated as completed. No active task may depend on them. S4-RI20/S4-FI40 migration applicability is excluded in v1.5.1, not passing evidence.

Preserve later decision history by appending entries with actual date, authority, requirement IDs, bounded rationale, affected tasks/tests/docs and supersession links. Routine implementation choices inside an authorized task are recorded without repeatedly requesting permission. Actual scope/privilege/destructive changes need their concrete decision.

## Startup execution and BOOT-001 adoption record

Recorded at 2026-09-08T21:58:10Z; underlying operator actions were reported in the 9 September 2026 session, without exact event timestamps.

- Human-Git source route retained. The initial root is `cc4e94135a5b2709dc907ad799b95b9a4c511f73`. Its one-time reviewed non-PR publication is the BOOT-000 exception, not permission for later direct-to-main changes.
- Owner configured sole-maintainer main protection: require a PR and resolved conversations, no administrator bypass, no force pushes/deletion; no second-account approval requirement. PDF supplies individual setting evidence; connected branch summary reports protected=true. Required source-CI checks remain pending until CP-001 introduces and verifies them.
- BOOT-001-D01 imports the validated v1.3 package and updates its execution records plus root README pointer. No product scope, architecture, helper code, original checksum manifest or historical bytes are changed. No further settings/source-publication/server authority is inferred.
- Independent candidate review and human integration remain required. The displayed model/effort is not established by available receipts; the package's requested setting is retained without inventing a matching UI observation.
