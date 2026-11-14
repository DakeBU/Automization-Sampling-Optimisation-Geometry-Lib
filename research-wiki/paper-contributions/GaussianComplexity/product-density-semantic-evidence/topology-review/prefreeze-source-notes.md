# Independent raw-source prefreeze for Ex70–72

This record was frozen before receiving the Statement Seal or proposed Source Proof Graph. It contains independent expectations only. It does not certify source fidelity, graph coverage, or Lean correctness.

The source is `.astis/huanjian-resume-20261103/2610.20492v1.html`, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. The exact seven slots, source proof-step inventory and residual guards are in `prefreeze-source-expectations.json`; raw source text and math alttext are in `raw-source-excerpt.txt`.

The key source boundary is actual-law identification. Appendix B.2 names `p_O` as the density of `N(0,A_O^-1)` and `p_b` as the density of the conditioned-Haar Gaussian mixture `P_b`. Section 3.1 defines `A_O`, its independently sampled block construction and the averaged target, and Eq6 identifies the actual full law with the independent block product. Ex70 consumes that identity to give the density on the actual full-dimensional coordinate space. It does not merely assert an algebraic product of unrelated normalized functions.

Ex71 applies Tonelli to the nonnegative affinity integrand and uses residual Gaussian mass one. When `kn=d`, the source explicitly omits the residual Gaussian factor and asserts the same affinity equality. The two dimension cases form exhaustive alternatives. Ex72 then uses the common-volume normalized-density TV overlap identity, `min(u,v) <= sqrt(uv)`, the affinity equality, and Eq25's bound with the exact constants.

The source suppresses the coordinate-volume bookkeeping between a tuple of blocks and `R^d`. A faithful formal route must keep that bridge visible and prove the required volume transport. A coordinate equivalence with a default Pi/product maximum norm must not be called a Euclidean isometry without an appropriate norm choice and proof. Volume preservation, rather than an unsupported metric claim, is the relevant property for Ex70–71.

After the seal and graph arrive, the review will compare their exact claims to raw source, examine every in-scope proof region or explicit exclusion, trace full root closure, check consumer-use edge directions, test OR routes against false ANDs, and inspect conditional discharge and actual-density definitions. No implementation Lean or extractor private rationale has been read. Shared ledgers and frontiers are outside this review's write scope.
