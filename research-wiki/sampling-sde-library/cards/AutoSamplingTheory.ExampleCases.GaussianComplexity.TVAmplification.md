# AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification

- File: `AutoSamplingTheory/ExampleCases/GaussianComplexity/TVAmplification.lean`.
- Sole declaration: `actual_averaged_tv_lower_bound`; one canonical compiled node.
- Mathematical source candidate: `ebf76119351b23ef0718fc69aa5081515bab0b52`; its audit was draft. The later independently source-reviewed audit and normal source V have separate exact receipts. No candidate/current audit byte equality is inferred.
- Domain: exactly `3 <= n <= d`, `kappa >= 4`, both actual common-sign conditioned full-Haar priors.
- Actual laws: the independent-block matrix priors pushed through the literal block precision, bound to true inverse-precision Gaussian measures. TV is the supremum over measurable event-probability discrepancies.
- Result: actual measurable-event `TV >= 1 - exp(-floor(d/n)/8 * exp(-10n/sqrt(kappa)))`, with the source probability normalization.
- Analytic adapters: actual law probabilities, RN-density L1/unit mass, finite event integration and the event-supremum comparison are discharged internally. No supplied density, integrability, probability, scalar-affinity or positive-remainder premise is added.
- Proof spine: actual Eq6 probability -> canonical ambient RN densities/event masses -> normalized-density TV/affinity comparison -> actual Ex71 tensorization -> actual Eq25 block estimate -> exact exponential lower bound. Both residual cases remain included.
- Real consumer: `Tests.GaussianComplexityTVAmplification` proves actual `TV >= 1/2` under the explicit threshold `floor(d/n)/8 * exp(-10n/sqrt(kappa)) >= log 2`; the production theorem has no such extra threshold premise.
- Reuse: the same actual Eq6, actual Ex71, actual Eq25 and canonical normalized-density TV comparison nodes, with pinned Mathlib RN integration and exponential-power facts. No duplicate wrapper or new conceptual transport.
- Source: Zhou--Suzuki arXiv2610.20492v1 S2.Ex2, S3.E4-E6, A2.E25/Ex70-Ex72 and the zero-residual omission. This is the selected final Ex72 inequality.
- Authored mathematics: `website/content/declaration_lessons/huanjian-tv-amplification.json`, bound by `website/content/publications/huanjian-tv-amplification.json`.
- Remaining: determinant-sign exact oracle/transcript/TV-precision/deterministic worst-case cap and explicit expected-cost adapters; fixed-spectrum hidden eigenbasis and both main lower bounds. Local root/site/Chrome, remote publication, purification/Exposition Seal and full Goal acceptance remain separate.
