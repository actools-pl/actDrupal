# Package validation — v1.3

**Subject:** documentation/specification package for actDrupal, fresh installations only. The checks below were executed during preparation on 8 September 2026. No product, server, GitHub write or runtime qualification is claimed.

## Run the supplied checks

From the extracted package root, with trusted Python 3:

```bash
python tools/verify_package.py
python tools/validate_workflow.py
```

Review both standard-library-only helpers before execution. They read files and have no network, subprocess, installation, privilege-change or write behavior. Use a stable operator-owned directory; these are not hostile-filesystem sandboxes. The distribution checksum checker expects an unedited extraction. Working record edits are tracked through Git and naturally differ from the distribution checksum list; do not regenerate the original list to conceal them.

The workflow linter checks regular-file inventory bounds, active/original baseline hashes, Markdown fence/local-path structure, CSV shape, unique tasks, dependencies/cycles, documentation-register targets and selected fresh-scope guards. External links, Markdown anchor rendering, real authority/commits, model/effort availability, host state, test authenticity, full semantic completeness and product security are outside its claim. The historical original is checked by hash and intentionally excluded from operative Markdown/scope parsing.

The bootstrap .gitattributes uses LF for authored text. Its narrowly named historical-reference rule preserves original bytes with -text -diff. The original is reviewed through its recorded digest/open-file inspection; product code and active documents retain normal diff and whitespace checks.

## Executed package checks

| Check | Actual result and boundary |
|---|---|
| Input identity | All 67 input manifest entries matched; supplied architecture equalled the original bundled v1.5 bytes. |
| Final structure | 76 regular package files; 65 operative Markdown documents, one exact historical Markdown reference, five CSV files, two Python helpers, two other bootstrap text templates and SHA256SUMS. |
| Workflow linter | PASS: 303 local file links resolved; CSV shape and 53 unique task IDs validated; dependencies are present and acyclic. 51 tasks planned, two cancelled; no active-to-cancelled dependency. |
| Scope | Active architecture has no old repository URL/ref/base or migration command/action vocabulary. C05/D13/F36/WP24 applicability revised; FRESH-T01–T04 present. Existing feature, WP, G, UX and S4 identifiers retained. |
| Historical evidence | Original v1.5 byte identity preserved; operative baseline has its own SHA in SOURCE_RECORD and the linter. Historical text has no task authority. |
| Isolated bootstrap/staging | PASS against a disposable local bare Git remote: reviewed seed root has no parent, pushed/read-back root matches, task branch starts at that root, all 79 seed/package files have mode 100644, authored diff check passes, staged original reference bytes remain exact. This was Linux/Bash validation of the documented Git operations, not a Windows/GitHub or human walkthrough. |
| Negative guard cases | PASS: workflow linter rejected an active CP-040 dependency on cancelled CP-039 and rejected an altered original reference in disposable copies. |
| Distribution integrity | Final SHA256SUMS covers the other 75 files; verified on the completed distribution and extracted final ZIP before delivery. |
| Standalone copies | Start Here and active Architecture downloads match their respective ZIP entries byte-for-byte. |

## Material limits

No external GitHub branch/settings/PR/workflow mutation, server provisioning, installer build, runtime test, product-security qualification, upstream-version refresh or unfamiliar-operator walkthrough was performed. The local bootstrap test used disposable local fixtures and a synthetic test identity. Its commits are not project commits or startup evidence for the operator's repository. Runtime task/evidence records therefore remain unproduced.

Excluded existing-site migration cases are NOT_APPLICABLE under the accepted scope; they are never passing product evidence. Own-site backup, full DR, supported updates, first-release security/UX and capacity/recovery objectives still need their actual implementation and qualification.
