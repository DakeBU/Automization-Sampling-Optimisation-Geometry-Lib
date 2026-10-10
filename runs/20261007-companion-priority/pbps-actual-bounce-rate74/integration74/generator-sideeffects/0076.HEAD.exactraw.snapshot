# AutoSamplingTheory.TechnicalLemmas.Probability.HeatBath

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/HeatBath.lean`
- Layer: shared KERN/MEAS integration node.
- Contract/status: [canonical Frontier Cell](../../frontier-cells/ASTIS-SHARED-heat-bath-snd-invariance.json).
- Focused consumer/tests: `Tests/HeatBath.lean`.

## Mathematical interface

`heatBathSnd μ` keeps the first coordinate and resamples the second using the
selected regular conditional distribution of a finite joint measure `μ`.
The retained space is merely measurable. The resampled space is nonempty and
Standard Borel. The construction is a noncomputable Markov-law interface, not
an executable implementation or a sampling-cost theorem.

`heatBathSnd_isMarkovKernel` proves mass one at every input, and
`heatBathSnd_apply` identifies the resulting measure as a Dirac first-coordinate
factor times the selected conditional law. These support the single substantive
correctness edge `heatBathSnd_invariant`: the update preserves `μ`.

## Proof architecture

1. Compose the deterministic first projection with the product of the identity
   kernel and the conditional-distribution kernel.
2. Reassociate its action on `μ` and identify the first marginal pushforward.
3. Rewrite the identity-kernel product action as a measure composition-product.
4. Reuse `ConditionalResampling.fst_compProd_condDistrib_snd_eq_self`.

The focused test uses `KernelInvariance.invariant_pow` directly for finite
heat-bath iteration. No duplicate iteration theorem is introduced.

## Boundaries

Zero finite measures and an empty retained space are allowed. Conditional-law
characterization is only marginal-almost-everywhere; the everywhere-Markov
property says nothing about conditional support on null fibers. Reversibility,
state-dependent scan, mixing rates, concrete Gibbs-density normalization and
continuous-time Langevin/Gibbs invariance are separate obligations.

The external motivation is MCMC §2.1.1 and Discrete Sampling §1.3, precisely
pinned in the cell. This source-neutral integration node does not assimilate
either textbook's full Gibbs-sampling analysis.
