# Separate dependency repair 1

This immutable revision corrects one dependency in the pending Appendix C.4 normalizer branch. Frozen phase one and phase two remain intact.

The challenged node states both `det(OΛOᵀ)=det Λ` and the resulting formula `Z_A=(2π)^(d/2)(det Λ)^(−1/2)`. Rereading the pinned raw source at `A3.SS4.p3.1` and `A3.Ex160` confirms that the full claim needs the preceding Gaussian-integral equality `Z_A=(2π)^(d/2)(det A)^(−1/2)`. Determinant invariance alone does not identify `Z_A`.

The repair therefore adds the existing `sg:fs-admiss:normalizer-integral` prerequisite to `edge:fs-admiss:determinant`. This is the only mathematical graph change. The graph remains acyclic. All 34 node claims, the other edge fields, the full `Z_A` assertion, the known-normalizer branch, and every coverage disposition remain preserved. The source normalization gap remains unproved and becomes an explicit ancestor of the full claim.

The selected producer and its exact seal/signature are unchanged: seal SHA-256 `ab68d72daa52e4607be3acf310b93cb0ad20c3638cd8062078805e3a33eccab0`, signature SHA-256 `186231307d4c41acba15a1098c56518120394295cf048f504fed6f8ea50018d5`. The repair adds no public premise and makes no proof, counterexample, source-verification, or completion claim.

`exact-diff.json` gives the before/after hashes and the single edge-parent patch. Full unified graph and matching diffs are included. `coverage.json` is a byte-identical copy of frozen phase-two coverage. `matching.json` records the separate revision without changing any semantic slot, source-node binding, or pending branch. Exposure is limited to the authorized challenger concern, the pinned raw C.4 source, the existing frozen graph/matching, and seal-hash verification. No implementation or API was opened.

This revision stops at its freeze for review by the distinct challenger.
