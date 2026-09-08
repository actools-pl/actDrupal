# Test receipt — REPLACE_RECEIPT_ID

**Template; no test result is implied.** Use PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE for this development receipt. Do not reuse these as a replacement product result schema.

## Identity

- Task / case IDs / parent WP / architecture references:
- Actual executor (human operator / CI runner) and evidence collector identity:
- Source delivery route and actual candidate/ref readback reference:
- Reviewed candidate full SHA:
- Actually tested full source SHA:
- Source state before/after: clean or explicitly exploratory dirty; retained diff/input identity:
- Declared generated/build inputs and any unexpected local mutation:
- Built/installed artifact filename, digest and build source/run:
- Actual transfer/install verification receipt and observed target drift:
- Dependency/fixture/test versions:
- Relevant configuration/policy/schema versions and non-secret fingerprint:
- Target role, provider identity reference, environment generation and boot identity:
- OS/image/kernel/architecture/relevant tools:
- External observer/controller identity and limitations:
- Session/credential isolation and declared egress verified; exceptions or incomplete checks:
- Started / finished UTC:

## Results

| Case ID | Expected assertion / exit | Actual command or manual steps | Actual exit and observations | Result | Artifact reference / limitation |
|---|---|---|---|---|---|
| REPLACE_CASE | REPLACE_EXPECTED | REPLACE_ACTUAL_OR_NOT_RUN | REPLACE_OBSERVED | NOT_RUN | REPLACE_REFERENCE |

- Underlying operation outcome (if command/report delivery differed):
- Required assertions not evaluated:
- For NOT_APPLICABLE: explicit supported-profile/scope reason:
- For interruption: last observed stage, possible effects, durable operation ID and safe next step:
- Relevant timing/coverage/data-size measurement and units:
- Secret-canary/redaction result where applicable:
- Cleanup attempted, observed result and remaining obligations:
- Final target state / changes made during debugging:

## Evidence and decision

- Raw evidence private custody reference (never secrets):
- Redacted shareable artifacts and digests:
- CI workflow/check names, run/job URL or ID, tested SHA/ref (including merge-test subject where applicable) and actual conclusions:
- Required new source-CI assertions executed; skipped/cancelled/permissive jobs and missing assertions distinguished:
- Chat-local execution, if applicable (NOT_RUN when unavailable); separately retain actual human/CI execution result:
- Evidence expiry/invalidating changes and retained limitations:
- Reviewer check and date:
- Follow-up finding/task:

The receipt names the source/artifact actually tested. Direct GitHub commit delivery does not establish a local checkout, clean build, computed artifact digest or executed test. Leave unavailable facts explicit; do not infer them from repository access. The later Git commit that stores this receipt is recorded by history/index, not self-embedded as the tested subject. Preserve failures and original timestamps; a rerun gets a new receipt or clearly separate attempt.
