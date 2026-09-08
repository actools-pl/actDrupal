# GitHub and change control

This is the human-authorized development workflow for the accepted v1.5.1 rewrite. GitHub stores authoritative source and project records; coding uses ordinary ChatGPT chats outside Work and Projects. Select either the human-Git route or the optional bounded direct-GitHub route according to actual access in that session. Neither route changes review, evidence or merge requirements. No chat's memory, model verdict or screenshot replaces a commit and evidence receipt. This document supplies a workflow, not a configured repository or working CI system.

## 1. New repository and product scope

The canonical repository is `https://github.com/actools-pl/actDrupal`. It starts with independent root history, `main` integration and `task/<ID>` branches. Architecture v1.5.1 supports fresh installations only. There is no inherited base, preservation ref, old source import or existing-site migration gate.

Follow [RB11](runbooks/RB11_NEW_REPOSITORY_STARTUP.md) and [BOOT-000](tasks/BOOT-000.md) for the one-time first commit. Verify live identity/refs and applicable automation before the authorized write. The bootstrap is reviewed before pushing because no integration branch exists yet for a normal PR. Verify the actual root SHA remotely; all subsequent normal tasks use the reviewed branch/PR route.

Use trusted local Git configuration. Do not import `.git`, hooks, executable filters or credential configuration from a coding response. Keep credentials on the trusted workstation and out of chat/source/test hosts. Unexpected existing files or refs require reconciliation, never a reset or forced replacement.

## 2. Setup and operating route

1. Record actual repository identity, access, refs, root-commit scope, available enforcement and relevant automation in RB11's receipt.
2. Review/publish/verify BOOT-000's three seed files. Record its actual parentless root SHA and direct-bootstrap status without inventing a PR/merge result.
3. Establish `main` no-delete/no-force and reviewed-change controls within the setup authority. Do not invent required checks or independent human reviewers. Document actual technical enforcement and the maintainer's manual acceptance duty.
4. Import the documentation through BOOT-001 on its task branch. This task excludes installer source, CI execution setup and server actions.
5. CP-001 introduces the minimal package and new source CI. Add required check contexts after actual names, runs and failure behavior are verified. A documentation-only stage does not depend on unimplemented product tests.
6. Select human Git or the bounded direct route in [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md). Each task records exact base, allowed paths/operations, candidate and merge authority. Existing authorization covers routine corrections within that scope.
7. Before integration, require resolved material findings, maintainer acceptance and applicable checks. If merge was explicitly authorized subject to those conditions, execute it once they are met without repeated permission. Source-write access alone is not production/server authority.

Arrange independent backup of the new project as source accumulates. Backing up another repository is not a prerequisite. No history rewrite, force push, default-branch replacement or infrastructure operation is part of routine startup.

## 3. One task, one reviewable change

Each task starts with a completed `templates/TASK_CARD.md`, an exact base SHA, current source files, a [context packet](templates/CONTEXT_PACKET.md) and a meaningful `templates/TEST_PLAN.md`. Every coding delivery has a [delivery manifest](templates/DELIVERY_MANIFEST.md) identifying the exact input base, outputs, modes and any unexecuted checks. Coder output is a complete patch, or complete changed files with an explicit file manifest. Include deletions, permissions, executable bits, tests, wiring, docs and dependency changes. A loose collection of snippets is insufficient.

Use [RB02](runbooks/RB02_RECEIVE_AND_APPLY_A_PATCH.md) for human-Git receipt or [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) for authorized direct GitHub delivery. Direct delivery still needs a manifest, exact input base, full final file/tree review and actual server-returned candidate identity; a file/blob SHA alone does not identify or lock the branch base. Review the full staged/committed diff, including new files and mode changes. Check generated files against their source. A diff summary is useful navigation but is not a review.

Create a PR targeting the integration branch using `templates/PR_DESCRIPTION.md`. Include purpose, requirement IDs, base/candidate SHAs, tests and limitations, documentation changes and operational impact. Keep credentials, private addresses where inappropriate, user data and raw diagnostic dumps out of the PR. Use synthetic fixtures. Store public-safe receipts in Git; store sensitive/raw evidence outside Git and record only a redacted reference, digest and custody information suitable for the repository's visibility.

Review code and changed CI before allowing privileged devbox tests. Review fixes invalidate findings/evidence according to their actual effect; do not re-run every test without a reason, but do re-run all affected required cases. No change to an assertion merely to hide a defect without a documented requirements correction.

## 4. The four identities that must not be confused

| Identity | Meaning | Required record |
|---|---|---|
| Base commit | Starting source given to the coder | Full SHA in task card and PR |
| Reviewed candidate commit | Exact task code reviewed/tested | Full SHA in review and test receipts |
| Integration/merge commit | Source that actually landed on the integration branch | Full SHA in task ledger and closure |
| Built artifact | The actual archive/package/images installed for qualification | Digest(s), build source SHA, build workflow/run and manifest |

A branch name, tag name or “latest” is not an immutable identity. Squash/rebase/merge can produce a different commit. Record it and run applicable integration checks on the resulting source. For first-release qualification, build the release candidate from the recorded integration source and qualify that artifact on the release-test server. Do not copy a manually repaired devbox directory and call it the release package.

`git rev-parse HEAD` alone does not establish the contents of the working tree. For acceptance/qualification builds and source tests, start from a clean identified checkout with declared generated inputs and locked dependencies; record pre/post-run state. Ignored caches or generated files that influence a build belong in its declared input closure. Exploratory tests with local edits may be useful, but must be labeled with the dirty state and retained diff/input identities; they do not qualify the clean commit. Bring relevant edits into a reviewed candidate and repeat affected checks before acceptance. Do not perform a destructive cleanup to manufacture clean state.

A source match alone does not establish identical dependency resolution or build output. Record dependency locks, build tools and resulting digests. A digest establishes byte identity, not authenticity; the architecture's maintained verification and trust bootstrap remain required for installable releases. This package does not replace them with a checksum.

If a merge produces only an identity change and demonstrably identical relevant source/dependency closure, the reviewer may document reuse of narrowly applicable earlier evidence. It must still identify the original tested object and the equivalence basis. The final installed artifact still needs its own required qualification.

## 5. CI is an execution boundary

CP-001 implements small documented source CI entrypoints and pins reviewed tool versions. Checks cover clean build/install, package inventory, truthful version/help and meaningful negative fixtures. Define the scanner's failure policy, including scan errors/unavailable execution; reporting findings with exit zero is not a passing vulnerability gate. A safe controlled negative fixture demonstrates the policy. Record real commands and run/check identities only after execution. Broader runtime and release qualification remains in the later named tasks.

Use ephemeral GitHub-hosted runners for source CI, with minimum permissions (normally repository contents read for checks), no production credentials, no Hetzner API token, no laptop credentials and no automatic privileged deployment to either server. Dependency installation and test execution still execute code, so review workflow/build changes and use the platform's untrusted-contribution controls. Do not attach a persistent self-hosted runner on the devbox or release-test server to untrusted public PRs.

Do not use `pull_request_target` to check out and execute untrusted contributor code with privileged context. Pin third-party actions to reviewed immutable revisions, inspect permissions and avoid inserting untrusted issue/branch text into shell commands. Release signing/publishing is a separate tightly authorized workflow; never give its credentials to routine PR checks. These controls follow GitHub's [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

CI artifacts/logs can contain secrets despite masking. Minimize collected data and review exports before sharing. Record a workflow run URL/ID, tested SHA, runner image/tool versions where relevant, actual check conclusions and retained artifact references in the test receipt. Export necessary redacted evidence before CI retention expires. Account for runner availability, quota and retention as setup inputs; do not assume unlimited resources.

## 6. Status and merge rules

Use exactly these task states: `planned`, `ready`, `coding`, `review`, `testing`, `changes_requested`, `blocked`, `accepted`, `merged`, `deferred`, `cancelled`.

The normal path is planned → ready → coding → review → testing → accepted → merged. Findings lead to changes_requested; unresolved prerequisites lead to blocked. Record the reason and return path. Accepted means the task's required review/evidence is complete; merged means the approved result is on the recorded integration commit and required integration checks have passed. Neither means a product release or production admission.

Final merge SHA and post-merge observations cannot be committed inside the earlier candidate that precedes that merge. Record them through a small reviewed follow-up records PR or an explicitly approved equivalent protected workflow. This bookkeeping commit has its own identity and does not replace the tested subject SHA.

If integration checks fail after the change actually merged, preserve the merge SHA and fact, record a blocking corrective task and block affected dependents/candidate qualification. Always retain the actual `merged_commit` even while the task status is `blocked`. Set task status `merged` only after required integration checks pass; a recorded merge SHA alone does not release dependents or establish product readiness. Do not erase the merge fact or reuse stale evidence.

Update `records/TASK_LEDGER.csv`, `records/REVIEW_LOG.csv`, `records/TEST_EVIDENCE_INDEX.csv` and `records/SESSION_HANDOFF.md` during closure. Capability implementation and qualification remain governed by the architecture's canonical requirement graph; the human task ledger does not become a competing capability source.

Use `runbooks/RB06_CLOSE_TASK_AND_HANDOFF.md` to finish. Do not merge a failing or incomplete required gate by reclassifying it as optional. A genuinely inapplicable test needs the supported-profile/capability reason and reviewer agreement. Deferred work needs an explicit scope decision and remains visible.

## 7. Undo and conflicts

For an unmerged incorrect patch, preserve evidence and ask the coder for a correction against the exact current state. For accepted source already merged, prefer a new reviewed corrective/revert commit. Git reversion does not reverse a database migration, firewall change or published credential: the affected product runbook controls live recovery.

Do not give a beginner a generic `reset --hard`, `clean -fd`, forced checkout, force push or firewall flush as routine recovery. If a task has merge conflicts, record both SHAs and resolve deliberately in a new candidate, then review and run affected tests again.
