# AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw

- File: `AutoSamplingTheory/ExampleCases/GaussianComplexity/AveragedBlockLaw.lean`.
- Sole declaration: `actual_averaged_block_product`; one canonical compiled node.
- Independent source/module verification: candidate `98cc6c8953d38dd54bc4e4ef7a547fd68a381ac8`, audit `ASTIS-RT-20261106-HuanjianAveragedBlockLaw`.
- Domain: exactly `3 <= n <= d`, `kappa >= 4`, and one fixed common sign `b = +1` or `b = -1`.
- Actual prior: twice-restricted full orthogonal Haar, independent product across blocks, then the literal block-precision matrix pushforward. The averaged target is its genuine Gaussian bind.
- Result: the actual coordinate pushforward is the product of actual single-block bind-mixtures and the standard residual Gaussian. Actual prior/target/block probabilities and almost-everywhere positive-definite support are proved; zero residual is retained as the probability unit factor.
- Real consumer: for every allowed parameter and either fixed common sign, actual averaged block-mixture and residual Gaussian marginals in `Tests.GaussianComplexityAveragedBlockLaw`.
- Reuse: same canonical Haar/component probabilities, block regularity, generic positive-definite Gaussian precision density, actual mixture laws and exact fixed-tuple Gaussian product theorem. No covariance/measurability/independence/mixture identity is supplied as an assumption.
- Source: Zhou--Suzuki arXiv2610.20492v1 Section3.1 Eq6, with Section2 conditioned prior/actual target, explicit contiguous coordinates and the zero-tail convention. The source omits the measurable-family/transport/averaging details completed here.
- Authored mathematics: `website/content/declaration_lessons/huanjian-averaged-block-law.json`, bound through `website/content/publications/huanjian-averaged-block-law.json` as the actual Eq6 proof edge.
- Direct production consumer: the same canonical declaration is actually called by `ProductDensity.actual_product_density`, the independently source-reviewed Ex70 density/coordinate-volume adapter. This does not change the scope of Eq6 itself.
- Remaining route: Ex71 tensorization, Ex72 amplified TV, source oracle/precision/deterministic-query-cap/expected-cost adapters, hidden-eigenbasis and both main lower bounds. Actual remote delivery and purification are separate acceptance stages.
