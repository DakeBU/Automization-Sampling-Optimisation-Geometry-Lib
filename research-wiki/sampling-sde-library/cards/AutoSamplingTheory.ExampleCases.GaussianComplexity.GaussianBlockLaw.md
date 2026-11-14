# AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw

- File: `AutoSamplingTheory/ExampleCases/GaussianComplexity/GaussianBlockLaw.lean`.
- Declaration: `actual_conditional_block_product`; one canonical compiled node.
- Independent source/module verification: `83bb8c9361d0dba4077db5994f682a1f4b45d85a`, audit `ASTIS-RT-20261106-HuanjianConditionalBlockLaw`.
- Domain: exactly source `3 <= n <= d`, `kappa >= 4`, and any fixed tuple in the full orthogonal group. No sign prior, covariance validity or independence hypothesis.
- Result: the literal contiguous coordinate split of the actual inverse-block-precision Gaussian is the genuine finite product of its actual block Gaussians and standard residual Gaussian. Zero residual is included.
- Actual consumers: every block and residual Gaussian marginal, contiguous coordinate/inverse checks and zero-dimensional probability point mass; the same canonical production node is now genuinely called by `AveragedBlockLaw.actual_averaged_block_product` for actual common-sign prior averaging.
- Reuse: unchanged canonical single-block and ambient regularity, actual Mathlib Gaussian and finite-product characteristic functions and measure uniqueness. Positivity, inverse and map-domain facts are internal proof components.
- Source scope: ASTIS completes the implicit fixed-tuple conditional producer for Zhou–Suzuki arXiv2610.20492v1 Eq5–Eq6. This declaration remains the conditional prerequisite; actual prior averaging is now separately proved by the canonical `AveragedBlockLaw.actual_averaged_block_product`. Product densities, tensorization, amplification and both main lower bounds remain open.
- Source of authored mathematics: `website/content/declaration_lessons/huanjian-conditional-block-law.json`; publication binding is prerequisite for full Eq6.
- Root/Registry, rendered delivery, actual merge and postmerge purification are separate acceptance stages.
