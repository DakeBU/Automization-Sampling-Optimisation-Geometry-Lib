# AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery

- File: `AutoSamplingTheory/ExampleCases/GaussianComplexity/FirstOrderQuery.lean`.
- Sole declaration: `actual_first_order_query`; one canonical compiled node.
- Mathematical candidate: `515f9401d4c324680bb2a1c010274cafa47efc02` carried a draft semantic audit. Later independent source/whole-module review and normal source V are pinned separately; no candidate/current audit-byte equality is inferred.
- Domain: exactly `3 <= n <= d`, `kappa >= 4`, arbitrary actual orthogonal blocks; no probability or determinant-sign premise.
- Actual objects: canonical `blockPrecision`, centered `f(x)=x^T A x/2` with zero additive constant, and the exact forward/inverse block responses `O_j v`/`O_j^T v` tagged false/true. Inverse means the orthogonal block inverse, not the precision inverse.
- Result: internally produced genuine `HasGradientAt f (g x) x` and `(f x, gradient f x)=(inner x (g x)/2,g x)` for every actual point. The vector g combines the actual affine block reply formula and the residual identity action.
- Proof spine: canonical actual-family symmetry -> actual quadratic Frechet derivative and Riesz identification -> actual block action from primitive replies -> literal contiguous block/residual assembly -> actual potential/gradient observation. The zero residual case is retained without a positive-remainder premise.
- Real consumer: `Tests.GaussianComplexityFirstOrderQuery` compares two actual hidden block tuples at the same point; equal actual primitive replies imply equal actual potential/gradient observations. This does not assume the desired gradient equality.
- Reuse: the same `blockPrecision`, `singleBlockPrecision` and `blockPrecision_regular` nodes, plus pinned Mathlib matrix action, inner-product differentiation and gradient uniqueness facts. Generated definition proof constants receive no separate paper-lemma credit.
- Source: Zhou--Suzuki arXiv2610.20492v1 S2, S3.E4-E5, Appendix B.1 oracle reduction Ex33-Ex35.
- Authored mathematics: `website/content/declaration_lessons/huanjian-first-order-query.json`, bound by `website/content/publications/huanjian-first-order-query.json`.
- Typed conceptual correspondence: `transport:gaussian-quadratic-oracle-factorization` compares exact algebraic reply reconstruction with Remark4.2, only as a separately source-reviewed mechanism. It is not a Lean implication, sample-law/TV transport or certified functor.
- Remaining: finite-horizon adaptive simulation and deterministic worst-case per-block2T/total2Tk caps; strict2T<n downstream transcript/output indistinguishability, independent seed and Borel laws, sampling TV precision, expected-cost adapters, fixed-spectrum hidden eigenbasis and both complete main lower bounds. Canonical root/site/Chrome, remote publication, purification/Exposition Seal and full Goal acceptance are separate.
