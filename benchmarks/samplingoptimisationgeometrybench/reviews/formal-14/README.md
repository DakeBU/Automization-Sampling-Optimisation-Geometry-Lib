# Formal round 14: fixed kernel mixtures and common invariance

`sogb-038` is an original public-dev L3 natural-language / Lean pair. It
shares the random-scan family because uniform coordinate sampling uses the
same fixed mixture construction. The exact Lean target permits an arbitrary
target measure and assumes s-finite component kernels, not Markov components.

- [Anonymous target](packets/anonymous-input.json), [blind decode](decoder.json), and [independent source review](source-review.json).
- [Exact rubric repair](packets/repair-input.json) and [independent acceptance](repair-review.json). Equivalent measure-level proofs and omission of zero-weight terms earn credit; the Lean statement, proof and points are unchanged.
- [Trusted Lean 4.33.0 receipt](trusted-reference-receipt.json). The earlier pointwise evaluation proof is reproduced only in the trusted reference, not the learner task or verifier baseline.
- [Selected compiled local edges](compiled-proof-occurrences.json) and [PBPS consumer path](compiled-consumer-path.json). Markovness and invariance both use the pointwise formula, and the PBPS invariant-kernel proof reaches the latter via its conditional mixture proof. These are selected proof-body occurrences, not mathematical necessity or new graph tasks.

The formal answer proves the fixed-weight invariant-measure equality. The
two-state counterexample with positive state-dependent weights is a prose
extension, not a Lean conclusion. This round does not prove convergence,
formally complete PBPS, or report model performance.
