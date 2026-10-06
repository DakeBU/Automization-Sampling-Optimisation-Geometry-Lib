# Actual Gibbs gradient mean

Canonical declaration: `AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean.integrable_gradient_and_integral_eq_zero` in `AutoSamplingTheory/TechnicalLemmas/Analysis/GibbsGradientMean.lean`.

The mathematical statement and formula proof are authored once in `website/content/declaration_lessons/gibbs-gradient-mean.json`. The exact preproof statement, independent topology/statement admission, focused build and independent whole-proof evidence are in `runs/20261007-companion-priority/smoothed-score-posterior/`. Source and exact-commit admission remain separate from those checks.

This is ASTIS-authored sufficient background for the actual posterior score identity in SPHMC Section 3.1 and unnumbered `S4.Ex9`. It is not a separately numbered theorem printed by the paper. Its direct paper consumer is `SmoothedScorePosterior.smoothed_score_posterior`; static MCMC reuse is planned only.

The minimal import is `GibbsGradientMoment`. Search and reuse retain its actual gradient second moment, canonical strong-convex Gibbs integrability, and pinned Mathlib full-space directional integration by parts. The old second-moment producer has an ordering binder; the new producer satisfies it internally by widening the upper bound to `max alpha beta`. The new public signature has no ordering binder and includes dimension zero.

Hidden regularity contracts are produced internally: actual Gibbs probability, vector gradient square-integrability and first integrability, ordinary-volume exponential weight integrability, weighted vector gradient integrability and all three products required by the global integration-by-parts theorem. No separately supplied boundary-decay, minimizer, partition, mean identity or analytic-domain certificate is used.

The proof route has four steps, indexed in the canonical lesson: actual Gibbs domains; ordinary weighted domains; constant-test directional integration by parts; normalized Hilbert mean cancellation. The production proof and translated quadratic/zero-dimensional tests compile under Lean 4.33.0 and Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`.

Failure policy: retain failed compiler evidence, type the exact mathematical/API obstruction after repeated unchanged failures, and preserve the sealed signature. Instance elaboration and metadata dependency qualification do not justify changing the mathematical statement. No Gaussian LSI, Talagrand transport, quantitative posterior bias, paper main theorem or query-cost claim follows from this leaf alone.
