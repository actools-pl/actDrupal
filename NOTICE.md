# Notices

This repository is the independent **actDrupal** installer project. Actools-authored source is licensed under the root MIT License and retains the Actools 2026 notice.

Drupal, Open Source components installed later, operating-system packages, container images, and other third-party software retain their own licenses and notices. Their presence in a future installation does not relicense those components under this repository's MIT License.

CP-001 contains no imported runtime source from the historical `actoolsDrupal` repository. Any later third-party or inherited source must record its provenance and applicable license before integration.

CP-002 vendors only six compact JSON Canonicalization Scheme conformance input/output pairs from `cyberphone/json-canonicalization` commit `19d51d7fe467d4706a3ff08adf8a748f29fc21e0`. That upstream vector/reference material is Copyright 2018 Anders Rundgren and licensed under the Apache License, Version 2.0. Exact source paths, local byte digests and the applicable Apache-2.0 notice are recorded in `tests/fixtures/jcs/cyberphone/PROVENANCE.md`. No upstream implementation source is vendored by CP-002.
