# RB11 — Start the new actDrupal repository

**Purpose:** initialize independent source history in `https://github.com/actools-pl/actDrupal`, then establish a reviewed coding workflow for fresh installations only. **Where:** trusted operator workstation and GitHub. **State:** procedure authored; execution NOT_RUN. This runbook grants no server, workflow-dispatch, release-publishing or production authority.

There is no legacy source commit, old-repository backup, preservation tag, fork or ancestry prerequisite. Do not reuse another project's working checkout or `.git` directory. An unexpected existing branch or file is inspected and reconciled; it is never reset or replaced to simulate an empty repository.

## 1. Verify the destination and record the startup scope

Read the live repository through the selected authorized route. Record time, owner/name, repository ID, visibility, default-branch setting, actual refs and permissions. An empty repository may report `main` as its default even though no `main` ref or commit exists. Record this as `EMPTY_REPOSITORY`, not as a fabricated SHA.

The preparation discussion observed public `actools-pl/actDrupal`, repository ID `1361769952`, default setting `main`, and no returned branches on 8 September 2026. These are dated observations, not evidence that startup has executed or that the repository is still empty.

Verify applicable repository/account rules, app/webhook access, Actions policy, runner access and any automation that could act on a push or PR. In a verified empty repository, record repository workflow files as absent; do not require an inventory of historical workflows from another project. Broader account policy/integration effects still depend on actual settings. Inspect credential names/scopes only, never values. If an applicable setting is unavailable, identify the concrete owner check required. Resolve a material unsafe trigger before the affected write; do not introduce a generic legacy-containment gate.

Activate [BOOT-000](../tasks/BOOT-000.md) with its exact destination, seed paths, initial-commit/push authority and reviewed contents. Authorization already covering those operations remains valid; do not request it again per file. Source authority does not itself include unrelated settings or infrastructure changes.

## 2. Make the first commit on a fresh local checkout

Use the human-Git route for this one-time bootstrap unless an available connected operation explicitly supports root commits and complete result verification. Do not pass a missing/zero/old SHA to an API that requires a parent commit.

The operator chooses a new local folder, records its actual path and uses trusted Git configuration. These commands are **Git Bash on the Windows laptop, or Bash on the trusted workstation**, not PowerShell. Keep credentials in the approved credential manager; do not paste tokens into URLs/chat. Review configured hooks/filters before committing.

```bash
git clone https://github.com/actools-pl/actDrupal.git actDrupal
cd actDrupal
git remote get-url origin
git status --short --branch
git ls-remote --heads --tags origin
```

The parent directory must be the operator's chosen work directory and `actDrupal` must not already exist. A clone warning about an empty repository is expected only when the verified remote is empty. Stop on an unexpected remote, files or refs. Git LFS, submodules, large binary source imports and old source archives are not bootstrap inputs.

With no local HEAD and no remote refs, establish the intended unborn branch:

```bash
git symbolic-ref HEAD refs/heads/main
```

Prepare only these three reviewed seed files from `repository_templates/`: `README.bootstrap.md` becomes root `README.md`; `gitignore.bootstrap` becomes root `.gitignore`; `gitattributes.bootstrap` becomes root `.gitattributes`. Do not copy the whole template directory to the root. Read each final file before staging. The README truthfully says implementation is pending. License/notices publication is implemented in CP-001 under the architecture's existing policy; a public empty repository is not a software release.

```bash
git add -- README.md .gitignore .gitattributes
git diff --cached --stat
git diff --cached --check
git diff --cached -- README.md .gitignore .gitattributes
git commit -m "chore: initialize actDrupal fresh-install project"
git rev-parse --verify HEAD
git status --short
git ls-remote --heads --tags origin
```

Review/record the complete seed candidate and actual root commit. Recheck the remote remains empty before the explicitly scoped first push. There can be no normal same-repository PR to an integration branch that does not exist yet; this single root commit has pre-push review and post-push verification. Do not invent a PR or merge SHA for it.

```bash
git push --set-upstream origin main
git ls-remote origin refs/heads/main
git rev-list --parents -n 1 HEAD
```

The remote SHA must equal the recorded local candidate. The root commit has no parent. An unexpected rejection or ref is inspected; do not force the push or amend history to disguise it. Retain public-safe scope/review/commands/results outside the checkout until BOOT-001 imports their references.

## 3. Establish the normal integration controls

Keep `main` as integration/default branch and use `task/<ID>` branches. Apply available no-delete/no-force and reviewed-PR controls within the recorded setup authority. Record enforcement and any manual limitations accurately. For a sole maintainer, do not require a second GitHub identity that does not exist; independent AI review is not an authenticated human approval. Maintainer acceptance and evidence remain required.

Required CI check names are added after CP-001 creates and runs the actual checks. Do not require nonexistent historical check names or leave BOOT waiting for product tests it cannot yet run. No source workflow is included in the three seed files or BOOT-001. Review CP-001's minimal source CI before its first trigger; exclude provider, production and signing credentials and persistent privileged host runners.

Start protection after the root commit can be addressed, before normal development advances. If a governing rule already requires PR-only creation and prevents bootstrap, use its owner-approved supported bootstrap route; record the concrete issue rather than bypassing a rule silently.

## 4. Import the package and begin the skeleton

Complete BOOT-000's actual publication/review receipt and mark it `accepted`. Its base is `NOT_APPLICABLE_EMPTY_REPOSITORY`; candidate is the real root SHA; `merged_commit` is `NOT_APPLICABLE_DIRECT_BOOTSTRAP`. The accepted verified root, not the word `accepted` alone, releases BOOT-001.

Create `task/BOOT-001` from the exact verified `main` SHA and import the reviewed package at `coding/` through [BOOT-001](../tasks/BOOT-001.md). Keep its existing root README: update it deliberately to point at `coding/00_START_HERE_CODER_DOCUMENTATION.md`. Merge through the recorded route after review and applicable documentation checks. CP-001 then starts from the verified BOOT integration result.

Once source exists, arrange the new repository's ordinary independent backup and recovery practice under owner custody. A laptop copy can support development recovery, but it is not an always-on independent production backup/monitor. Record the real coverage; do not label a plan as a verified backup. No task requires copying another project's history to begin.

## Receipt and recovery

Record exact repository ID/URL, actual timestamp, route, local path if used, initial/root SHA, permitted operations, seed-file review, remote readback, root-parent result, current protections/automation, public-safe backup plan, BOOT branch/base, gaps and next action in PROJECT_STATE and SESSION_HANDOFF. No secret values belong there.

On ref drift, unexpected files, failed checks, ambiguous writes or unavailable required authority, preserve the candidate and inspect current state. Correct or resume against the actual state. Do not reset/clean/force-push as routine recovery. No installer or server command is part of this runbook.

References: [GitHub repository quickstart](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories), [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [Git symbolic-ref](https://git-scm.com/docs/git-symbolic-ref).
