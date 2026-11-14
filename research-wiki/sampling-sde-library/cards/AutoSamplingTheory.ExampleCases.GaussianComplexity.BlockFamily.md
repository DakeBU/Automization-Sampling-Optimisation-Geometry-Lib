# AutoSamplingTheory.ExampleCases.GaussianComplexity.BlockFamily

- Existing module: `AutoSamplingTheory/ExampleCases/GaussianComplexity/BlockFamily.lean`; this card adds a retrieval/consumer description, not a new theorem or Registry credit.
- Canonical definitions and results remain those of the existing `ASTIS-SW-GAUSSIAN-COMPLEXITY-block-precision` Frontier Cell: literal `blockPrecision` in contiguous block coordinates, `blockPrecision_regular` and `blockPrecision_unique_minimizer`. Their existing source/Lean evidence and status remain authoritative.
- Source domain of the regularity theorem: `3 <= n <= d`, `kappa >= 4`, arbitrary actual orthogonal tuple. The full matrix is the block diagonal of `singleBlockPrecision` matrices and the residual identity, with the zero residual case included.
- Actual production consumer: `FirstOrderQuery.actual_first_order_query` consumes this same `blockPrecision` and the symmetry projection of `blockPrecision_regular` to prove the genuine gradient of the actual centered quadratic and reconstruct its actual first-order observation from primitive replies.
- The query theorem does not assume symmetry or a gradient identity as a new public premise, and does not duplicate this regularity result. It does not consume spectral inequalities as a calculus hypothesis.
- This newly authored card does not retroactively insert a missing parent Registry entry or grant fresh independent review to old module bytes. Existing Gaussian-law and other consumers remain unchanged.
- Remaining route boundaries: finite-horizon operational query caps, adaptive posterior/transcript/output laws, TV precision, expected-cost adapters, fixed-spectrum route, both main lower bounds, remote publication and postmerge purification/Exposition Seal.
