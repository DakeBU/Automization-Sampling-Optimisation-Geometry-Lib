# SPHMC canonical-score representative obstruction

## Source-facing issue

SPHMC Lemma 4.17 invokes the restricted-Gaussian contraction, while the cited
Lee--Shen--Tian Lemma 2, equation (11), evaluates the gradient of an explicit
pointwise smooth log-density-ratio representative. Mathlib's `llr` is a
specific Radon--Nikodym-based function, but the available identification with
that explicit representative is only almost everywhere. An adapter to the
canonical score therefore cannot use almost-everywhere equality alone.

## Typed counterexample

For `μ = δ₀`, let `f(x)=0` and `g(x)=x`. Then `f=g` `μ`-almost everywhere,
but

\[
\nabla f(0)=0 \ne 1=\nabla g(0).
\]

Hence no theorem can transport classical gradients across arbitrary
almost-everywhere equality.

## Possible sufficient repair routes

Examples of stronger interfaces that could justify the paper's score step are:

1. choose the explicit smooth representative as the score-bearing object;
2. prove equality on a neighbourhood at almost every relevant point; or
3. formulate Fisher information using Sobolev weak gradients, whose
   equivalence classes are compatible with almost-everywhere equality.

The typed obstruction does not select among these repairs and does not prove
the restricted-Gaussian LSI, Talagrand T2, or Wasserstein contraction.
It also does not show that Mathlib's particular `llr` has an incorrect gradient,
exclude a theorem for full-support absolutely continuous measures under added
regularity, or exclude an RGO-specific pointwise/local-equality adapter.
