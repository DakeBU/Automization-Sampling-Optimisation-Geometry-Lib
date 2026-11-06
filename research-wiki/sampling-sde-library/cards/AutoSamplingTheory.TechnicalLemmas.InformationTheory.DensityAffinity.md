# AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity

- File: `AutoSamplingTheory/TechnicalLemmas/InformationTheory/DensityAffinity.lean`
- Layer: canonical shared mathematical interface; independently verified at `a5d10714ca01eb29c934acec06bb8983413182c2`.
- Declaration: `normalized_density_tv_affinity` in the module namespace.
- Contract: any measurable carrier and common measure; two pointwise nonnegative measurable genuine L1 real densities, each with integral one. No finite/probability/sigma-finite assumption on the reference measure.
- Conclusion: sqrt-product is genuinely L1; its affinity a is in [0,1]; the measurable-event density discrepancy supremum is exactly half the L1 difference and satisfies `1-a ≤ TV ≤ sqrt(1-a²)`.
- Actual consumer: `GaussianComplexity.SingleBlockAffinity.single_block_affinity_bound` internally supplies every density condition from the actual mixed-Gaussian producer and derives Eq25 with B.7.
- Focused verification: disjoint/identical Fin2 endpoint normalization, a.e.-representative preservation of affinity L1/value and every density set-integral, and the actual all-source-domain scalar-power consumer.
- Planned consumer: source B.2.3 Ex72 lower comparison on actual full-product densities after the separate Eq6/coordinate/residual-Gaussian and product-density proofs. No product-law or amplification credit yet.
- Provenance: ASTIS-authored common-measure library statement from standard Cauchy–Schwarz and normalized-density algebra; Zhou–Suzuki arXiv2610.20492v1 Ex69/leading Ex72 motivate the Euclidean instances. It is not attributed as a paper theorem on arbitrary spaces.
- Publication, final root/site/graph acceptance and post-merge purification remain separate lifecycle stages.
