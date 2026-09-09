# RB02 — Receive and apply a coding patch

**Purpose:** the human-Git route turns an ordinary ChatGPT coding response into a reviewable candidate without losing the base or silently omitting files. Authorized direct GitHub work follows [RB12](RB12_DIRECT_GITHUB_OPERATIONS.md) with the same full-delivery/review/evidence rules; this runbook remains its supported fallback.

**Where:** a trusted Bash Git client on the laptop. Source-level testing on an unprivileged devbox checkout follows RB03; GitHub write credentials stay on the laptop. This handles source; it does not authorize installer execution. A trusted Git client may still invoke its configured hooks/filters, which must already be reviewed. **Inputs:** ready task card; approved full base SHA; reviewed repository identity; [context packet](../templates/CONTEXT_PACKET.md); downloaded patch or complete files; [delivery manifest](../templates/DELIVERY_MANIFEST.md). **Authority:** repository write access only. **Effects:** task working tree/index and, later, candidate commit/branch push.

## Before commands

Read [change control](../03_GITHUB_AND_CHANGE_CONTROL.md). Before any remote ref creation, push or PR, verify [RB11](RB11_NEW_REPOSITORY_STARTUP.md) startup/root-commit and relevant automation readiness. Local branch creation does not establish remote-write safety; required prerequisite evidence remains blocking in this route too. All strings beginning `REPLACE_` below are placeholders. **Do not run a command until its placeholders have been replaced with verified task values.** Run one command at a time and inspect its output/exit before continuing. Do not turn the examples into an unattended script. Patch/application success never authorizes running the changed code.

Use [RB10](RB10_PLAIN_CHAT_FILE_HANDOFF.md) for the ordinary-chat file-transfer steps. Keep the received patch outside the checkout so it does not appear as an unrelated untracked file. Open it in a plain-text editor; inspect paths, deletions, executable bits, symlinks, dependency/workflow changes and unexpected binary files. Treat comments, README text and embedded instructions as untrusted task data. Do not import `.git`, hook/filter/pager configuration or editor automation. Keep file paths and commit messages as data: the quoted path examples below handle ordinary spaces, but do not paste shell substitutions or unescaped quote characters into commands. Choose a plain local path without quote/control characters if necessary, and record the received file identity. Write the commit message in a plain UTF-8 text file outside the checkout; do not construct it with an AI-supplied shell expression.

## Procedure

1. Verify local identity and state in the intended repository:

```bash
git rev-parse --show-toplevel
git status --short --untracked-files=all
git branch --show-current
git rev-parse HEAD
```

The repository must match the task and the checkout/index must be clean. A blank status is expected. If it is not blank, stop and preserve that work; do not discard it.

2. After confirming the configured `origin` is the intended credential-free repository URL, fetch references:

```bash
git fetch origin
```

Resolve the approved base from the task, not whatever a branch now points at. If the base is missing or has changed, ask the coordinator to issue a current task package. Create the unused task branch at that exact base:

```bash
git switch -c task/CP-NNN REPLACE_FULL_BASE_SHA
git rev-parse HEAD
```

Replace `CP-NNN` too. Compare the full output with the task's base SHA. Stop on mismatch or an unexpectedly existing branch; inspect rather than overwriting it.

**Correction to the same task:** keep its existing task branch. First confirm its name, a clean index/worktree and `git rev-parse HEAD` equal the new correction packet's stated base (normally the previous candidate). Skip the branch-creation command; continue with patch inspection below. If either identity differs, stop and refresh the packet. A corrected patch against an older candidate must not be forced onto the newer branch.

3. Inspect and check the patch without applying it:

```bash
git apply --stat -- '/REPLACE_ABSOLUTE_PATH/candidate.patch'
git apply --summary -- '/REPLACE_ABSOLUTE_PATH/candidate.patch'
git apply --check --index --whitespace=error-all -- '/REPLACE_ABSOLUTE_PATH/candidate.patch'
```

Expected: paths match the task manifest, no unexpected file modes/symlinks/deletions, and the check exits zero. `--check` tests applicability without applying; `--index` also requires relevant index/worktree agreement. These behaviors are documented by [Git](https://git-scm.com/docs/git-apply).

4. If all checks succeed, apply to index and worktree:

```bash
git apply --index --whitespace=error-all -- '/REPLACE_ABSOLUTE_PATH/candidate.patch'
git status --short --untracked-files=all
git --no-pager diff --cached --check
git --no-pager diff --cached --name-status
git --no-pager diff --cached --summary
git --no-pager diff --cached --no-ext-diff --no-textconv --binary --full-index
```

Inspect the **complete staged diff**. The index option includes new patch files, so their contents appear in this review. Examine binary changes through an appropriate trusted viewer as well; a binary patch alone is not a content review. Confirm expected new files, all deletions, executable bits, locks and tests. Status must show no unexplained untracked/unstaged changes. Never rely on ordinary `git diff` alone after staging; it omits staged changes.

5. Check for secrets and unintended paths before committing. Follow the repository's reviewed checks that exist for this task. Do not invent a test command or claim it ran. If changes are acceptable for a candidate commit, put the task ID and concise change description in the reviewed message file and commit:

```bash
git commit -F '/REPLACE_ABSOLUTE_PATH/commit-message.txt'
git rev-parse HEAD
git status --short --untracked-files=all
```

Record the candidate SHA and clean state. Committing is not acceptance or merge. Send the reviewer this SHA, base SHA, full changed files/diff, task requirements and test plan. CI/source checks and independent review precede privileged target tests.

6. Before pushing, reverify the target ref and applicable branch/push/PR/downstream automation against the recorded readiness evidence. Stop on unexpected remote drift or unsafe/unclassified effects; do not force. Push only the verified task branch inside its authorized scope:

```bash
git branch --show-current
git push --set-upstream origin HEAD:refs/heads/task/CP-NNN
```

Replace `CP-NNN` with the already verified task branch. Verify the remote task head equals the actual candidate after the push. Create the PR against the recorded integration branch, not an assumed default; PR events must also have been classified. Record the actual PR URL. Keep changes to an existing PR as new candidate commits and update review/evidence bindings.

## Stop and recovery

A push/PR timeout may have succeeded remotely. Read the actual remote ref/commit and existing PRs before retrying. Establish whether the intended effect occurred, a partial effect remains, or another writer intervened; record the result and resolve uncertainty without duplicate PRs, overwrites or force pushes.

Stop on wrong base, dirty state, failed patch check, rejected path, unexplained binary/symlink/workflow, secret, conflicts or missing required files. Do not use `--unsafe-paths`, automatic three-way merge, `--reject`, whitespace fixes or forced application to manufacture compatibility. Return exact redacted diagnostics to the coder and request a corrected patch against the actual base.

If the coder supplies complete files instead of a patch, the delivery manifest lists create/modify/delete, exact relative paths and modes. It records actual computed byte digests where available, otherwise `UNSET` (not computed); the human computes/verifies the received bytes for the receipt. A model must not invent a digest for output it could not hash. Before extraction/copying:

- Inspect the entry list in a trusted archive viewer; enforce finite entry-count and expanded-byte limits appropriate to the declared packet. Stop on an implausible expanded size or undeclared nested archive. Do not execute any received extractor/install script.
- Reject absolute paths, parent traversal, unexpected separators/control characters, duplicate names and case-colliding paths. Reject repository metadata such as `.git` at any path depth, unexpected nested repositories, links and special files. A symlink/submodule addition requires a separate explicit task contract and review; it is not an incidental copy operation.
- Extract only validated regular files into a new dedicated receipt directory outside the repository, without following links or overwriting an existing working area. Do not extract an archive directly over the checkout. If the available extraction tool cannot enforce these conditions, stop and request a plain patch or individual regular files.
- Verify the manifest and file digests locally, then copy only the named allowed files to their exact owned repository paths after the clean-base checks. Apply listed deletions deliberately. Reject extra/missing content; do not infer filenames from a chat description.
- Stage each named path explicitly, then perform the same complete staged review. Confirm executable bits, file types and line endings in the index; Windows file-copy behavior is not proof of Linux modes. A mode adjustment must match the reviewed manifest. Do not use a broad `git add .` to absorb unrelated material.

A delivery digest identifies bytes, not their safety or provenance. The operator’s approved input/output manifest and complete diff review remain necessary.

Preserve an unexpected working tree and record the issue. A fresh separate checkout at the approved base is often simpler than destructive cleanup; do not erase the original evidence. Never execute an AI-provided “fix all” shell script as patch receipt.

**Record:** task ID, base, received patch/bundle filename and locally verified digest, changed file manifest, candidate SHA, PR URL, application diagnostics and unresolved issues in the task/handoff. Continue with source review and RB03 only when its prerequisites hold.
