# Release and acceptance workflow

Package version: 1.3. Authority: architecture v1.5.1 §§13–15, §18.5 and Annex UX. This document describes work to perform later. No installer build or release is qualified by this package.

## 1. Four different decisions

| Decision | Meaning | What it does not establish |
|---|---|---|
| Task accepted | Bounded task meets its card; material review issues resolved; required evidence present | Whole-system support |
| Task merged | Accepted change integrated at an identified commit and required integration checks passed; a real merge with pending/failed checks retains its SHA but task status is `blocked` | Full release or production admission |
| Candidate qualified | Identified package passes the applicable release/profile matrix | Every optional capability or every deployment |
| Production admitted | Real deployment satisfies its current protection, recovery and operational gates | Permanent health after later changes |

Keep task states in the task ledger: `planned`, `ready`, `coding`, `review`, `testing`, `changes_requested`, `blocked`, `accepted`, `merged`, `deferred`, `cancelled`. Release/capability states are recorded separately. A test may be planned, passed, failed, blocked or not run without changing the meaning of those task states.

The delivery route does not change these decisions. Direct GitHub writes under [RB12](runbooks/RB12_DIRECT_GITHUB_OPERATIONS.md) can produce a source candidate and collect check observations within the authorized task; they do not grant release publication, signing, deployment, server or ruleset authority. The human/integrator retains the agreed acceptance and integration authority.

## 2. Readiness to build a candidate

**Early local development exception to this release workflow:** Activated pre-release development tasks may build controlled fixtures from an exact reviewed, clean checkout for direct human-operated installation on the registered expendable targets. This includes CP-001/CP-010 and the installed host-development work in CP-011–CP-016 before the later release-trust qualification is complete. The task must identify the required fixture, allowed effects and reviewed build/install procedure. Keep its source, dependency/build inputs, artifact digest and verified private transfer record. This permission is for controlled development evidence only, not a distribution channel. These fixtures are not published artifacts, update targets or release candidates and cannot satisfy release-trust qualification. Do not post an unsigned installer to GitHub Releases or a download endpoint under this label. Architecture §18.6 still requires the release-engineering ADR (roles, thresholds, expiry and bootstrap/rotation) before publishing **any** installable artifact, including test-trust distributions. Published candidates must also exercise the required verifier; later update qualification is not a waiver.

The integrator checks that:

1. Candidate scope is explicit: active work, selected optional features, platform/profile, supported reader/writer versions and supported upgrade/recovery edges.
2. The canonical requirement graph supplies support and gate applicability. Preserve the 20 active work packages WP01–WP15 and WP21–WP25. WP16–WP20 remain deferred; a reserved interface does not implement them.
3. Candidate changes are merged and reviewed; unresolved findings have a severity, owner, disposition and honest effect on release eligibility. Required security controls cannot be waived by a chat convenience decision.
4. Final integrated source identity is exact, the actual build checkout is clean with declared generated/build inputs, and the required new source-CI checks executed and passed for that identified subject. Record workflow/check/run identities and distinguish an actual PR merge-test subject from the candidate head. A connector commit or incomplete CI badge supplies none of the missing build/qualification evidence. Candidate evidence from an earlier branch is reassessed after rebasing, conflict resolution or merging.
5. Packaging, dependency and license/SBOM inputs are recorded. The candidate is installed from the final package/layout rather than run only from the source checkout.
6. Trust bootstrap, signatures and the Python-TUF release process required by v1.5.1 are implemented before distributing installable artifacts. Development-only signing keys and trust roots are conspicuously segregated and cannot establish production trust. A hash alone does not authenticate a release.
7. Installation/update/recovery runbooks and support views match the candidate. Changelog entries describe implemented behavior only.

No universal assertion of a reproducible build is made here. Record the implemented build process, immutable input identities and actual artifact digests; claim stronger reproducibility only after it is demonstrated.

## 3. Qualify on the release-test server

Use [RB07](runbooks/RB07_RELEASE_CANDIDATE_AND_REHEARSAL.md). The release-test server receives reviewed candidates through the documented installer workflow. Keep synthetic data and test-only credentials there. Do not repair it with unrecorded hand edits and still call the installer successful.

The finite candidate matrix includes relevant clean install, supported upgrade/import, service reboot, failure/interruption and recovery paths. Run the applicable G gates and S2–S5/RV13/UX refinements from the graph. Use risk-based combinations without omitting mandatory high-risk interactions. First-release UX includes UX-R01–UX-R15 and UX-T01–UX-T22 plus applicable UXS-C expansions; conditional UX-R16–18/UX-T23–24 do not silently enter the release.

The CP-050 matrix includes the accepted Cloudflare on/off qualification from CP-027 and complete recovery evidence from CP-047. CP-035’s earlier recovery-path exercise remains a prerequisite for destructive lifecycle work but cannot replace the complete outage-start RTO proof. Reassess all evidence against the final candidate, enabled/disabled modes and actual context; a dependency entry alone is not a PASS.

Record each result against source SHA, package digest, OS/profile, selected capabilities, fixture and test version. Preserve negative observations and actual elapsed times. Unit tests do not establish firewall reachability; a backup upload does not establish recovery.

## 4. Two-box limits

The devbox and release-test server separate development from installation qualification. Sharing a provider or administrative account still creates shared risks. Containers on either host do not prove independent backup custody or detection of that host/account's loss.

For controlled exercises the laptop can provide an independent test endpoint when available. Continuous availability and independently controlled backup/monitor authority must be qualified before production admission under v1.5. If the necessary independent environment is absent, record the affected tests as blocked/not run and the support claim as unqualified. Do not substitute “two servers exist” for the required trust separation.

The reference 80 GB total site size is planning input. Unknown split, daily change rate, bandwidth, pause allowance and repository growth remain measured qualification inputs. RPO ≤1 hour and RTO ≤4 hours are verified over the complete agreed boundaries; a timed restore command alone does not establish the four-hour outage-to-recovery objective.

## 5. Merge and candidate identity

Recheck the actual final merge commit. If a merge changes code, dependency locks, schemas, generated assets or build inputs, rerun affected checks and regenerate affected artifacts. When the final tree is identical to a reviewed candidate tree, record the comparison and still complete required integration/branch checks. Never relabel a receipt from another SHA without showing the relationship and its limits.

A pending or failed required integration check after an actual merge preserves the real `merged_commit` and keeps the task `blocked`; a failure also opens a corrective task. Mark the task `merged` only when its required integration checks pass. Do not release affected dependent work or transfer acceptance to the failing result. Final merge/qualification records enter Git through a reviewed follow-up records change when they could not exist before the merge, with their record commit distinct from the tested subject.

If a candidate artifact changes, its digest changes and affected qualification must follow the new artifact. A new version label does not transfer evidence. Retain the candidate's provenance and failed results even after a corrected candidate passes.

## 6. Release decision record

Create [RELEASE_RECORD](templates/RELEASE_RECORD.md) and update `records/RELEASE_REGISTER.csv`. Include exact source and package identities, required evidence, unresolved issues, documentation receipts, trust metadata, support profile, operator actions, retained recovery dependencies and the decision maker. Reference evidence locations rather than placing secrets or large raw dumps into GitHub.

A release can be withheld or limited to an explicitly qualified development profile. Such a label must not imply production support. Do not publish a qualified-release claim while mandatory profile gates are unexecuted. Creating a release record does not itself publish code or deploy a server; those are distinct later operations under the project workflow.

## 7. Production transition later

Before real production use, rebuild the chosen host cleanly, install the qualified release through independently bootstrapped trust, provision distinct production credentials and data, and pass real deployment admission. Retain independent recovery keys and current rehearsal evidence. Do not promote the experimental server by changing its label or reuse test signing material.

The two-box arrangement is a development practice. It does not add a managed staging feature, deployment webhook, browser control panel or new product topology.

Related: [test strategy](05_TEST_AND_EVIDENCE_STRATEGY.md), [documentation workflow](06_DOCUMENTATION_AND_CHANGELOG_WORKFLOW.md), [security rules](08_SECURITY_AND_SCOPE_RULES.md).


## Fresh-install scope applicability

The released product supports new installations and qualified lifecycle/recovery of its own sites. Do not require a real legacy site, existing-site importer, migration cutover rehearsal or age-reader test for release. CP-038/039 are cancelled; S4-RI20/S4-FI40 are NOT_APPLICABLE by the user's v1.5.1 decision, never PASS. Require FRESH-T01–T04 and all other applicable security/UX/recovery/update cases. Native recovery-set identity/authenticity checks and post-restore writer/revocation protection remain mandatory. The 80 GB representative profile and full one-hour RPO/four-hour RTO qualification still apply with controlled fixtures. No production upgrade edge is advertised before a real source release and qualified target exist.
