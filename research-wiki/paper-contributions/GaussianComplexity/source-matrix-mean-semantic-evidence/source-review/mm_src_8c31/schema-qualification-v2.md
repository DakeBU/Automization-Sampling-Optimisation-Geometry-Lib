# Schema qualification v2 — original mathematical review unchanged

The original v1 report, overlay, portable manifest and all 66 manifested portable copies remain unchanged. This qualification corrects only the metadata-schema claim's practical boundary; it does not rewrite or reseal the original report.

The v1 check was the independent **minimum** vocabulary/key-shape validation described in that report. It was not an invocation of the actual canonical core validator. The coordinator's subsequent read-only actual-core check reported one error: `reviewed audit needs source_review.evidence`. The original overlay used `review_evidence`; the core requires a nonempty field named `evidence`.

I inspected the separately authorized core lines 616–642, then reconstructed exactly one own audit in memory from my original fresh reviewer packet, anonymous decoder input and original v1/v2 overlays. The minimum registry/protocol wrapper field placement was supplied separately as format-only schema information. No real registry or other audit was read or written. An initially incomplete synthetic wrapper produced format errors; that exact harness and its errors are retained in `synthetic-incomplete-wrapper-v2.json` and are not mathematical failures.

With the correctly formed one-audit wrapper, the actual `validate_registry` function reproduces **exactly the original v1 evidence-key error**. Substituting v2 produces **an empty error list**. Both the canonical anonymous decoder packet hash and the canonical fresh reviewer packet hash remain exactly equal to their original pinned values. The complete v1/v2 wrapper inputs and results are retained in `canonical-core-single-audit-v2.json`; no source/semantic conclusion was changed to satisfy the validator.

`canonical-overlay-v2.json` adds `source_review.evidence` with the exact existing `review_evidence` string and an optional `run_artifact` pointing to the original portable report. All original overlay fields remain equal. In particular the seven slots, `equivalent-after-elaboration` verdict, empty deltas/repairs and review states are unchanged. `source_review.review_run_sha256` still points to the complete original report's external raw SHA-256:

`89550a6307ff2d651fc906d342d6690f1bf37c0559623f10966268f2a257b2dd`.

The mathematical candidate remains `5fb1440f771bdae77ad31f27b2275447fe3e89e5`; neither P/T nor prose, source, definitions or reconstruction changed. v2 is a metadata schema correction, not a source repair, new mathematical audit, normal VERIFIED transition, compiler/browser claim, permission grant or integration authorization.

`portable-manifest-v2.json` preserves every v1 input and exposure artifact, the original v1 overlay and manifest, and adds these v2 schema artifacts under new names. Existing destinations are only byte-checked. `v1-preservation-v2.json` records the unchanged v1 identities. No v1 file is overwritten, even with equivalent reserialization.
