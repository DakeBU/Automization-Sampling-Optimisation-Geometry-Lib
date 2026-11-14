# AutoSamplingTheory.ExampleCases.GaussianComplexity.AffinityTensorization

- File: `AutoSamplingTheory/ExampleCases/GaussianComplexity/AffinityTensorization.lean`.
- Sole declaration: `actual_affinity_tensorization`; one canonical compiled node.
- Mathematical source candidate: `4014feb9c6dff0b4e0dcb9fb49ae1b961cf3cf0b`; its audit was draft. The later independently source-reviewed audit and normal source V have separate exact receipts. No candidate/current audit byte equality is inferred.
- Domain: exactly `3 <= n <= d`, `kappa >= 4`, both actual common-sign conditioned full-Haar priors.
- Actual laws: the independent-block priors pushed through the literal precision, bound to true inverse-precision Gaussian measures.
- Result: both laws are AC to ambient volume; the square root of the product of their RN derivative real values is genuinely L1, and its integral equals the actual block-density affinity to exact power `d / n`.
- Representative audit: actual Ex70 withDensity gives finite a.e. RN identification; toReal recovers nonnegative actual finite densities. No constructor/integral/infinity fallback supplies the source meaning.
- Proof spine: actual product density -> RN density a.e. -> normalized product-affinity L1 and actual volume change -> finite-product Fubini with common residual unit mass. The source omitted zero-dimensional residual is included, without an added positive-remainder premise.
- Real consumer: all-source-parameter actual ambient RN-affinity exponential-decay bound in `Tests.GaussianComplexityAffinityTensorization`; the prior Eq25 scalar estimate alone did not establish this quantity. Eq25 is not a parent of the tensorization proof.
- Reuse: the same actual Ex70, actual mixture density and canonical normalized-density affinity nodes; pinned Mathlib RN, sqrt-product and real product-integral facts. No duplicate wrapper or new conceptual transport.
- Source: Zhou--Suzuki arXiv2610.20492v1 S3.E4-E6, actual density definitions, A2.Ex68/70/71 and the zero-residual omission. Ex72 is the next source consumer.
- Authored mathematics: `website/content/declaration_lessons/huanjian-affinity-tensorization.json`, bound by `website/content/publications/huanjian-affinity-tensorization.json`.
- Direct production consumer: the same canonical actual RN-affinity tensorization is genuinely called by `TVAmplification.actual_averaged_tv_lower_bound`, the independently source-reviewed Ex72 measurable-event TV bound for the actual Gaussian-prior binds. This does not enlarge the scope of Ex71 itself.
- Remaining route: determinant-sign exact oracle/transcript/TV-precision/deterministic worst-case cap and explicit expected-cost adapters; fixed-spectrum hidden eigenbasis and both main lower bounds. Remote publication, purification/Exposition Seal and full Goal acceptance remain separate.
