# AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/KernelMixture.lean`
- Layer: shared KERN/MEAS fixed-mixture interface.
- Contract/status: [canonical Frontier Cell](../../frontier-cells/ASTIS-SHARED-finite-kernel-mixture.json).
- Focused consumers/tests: `Tests/KernelMixture.lean`.

## Mathematical interface

For a finite index type, let `w : ι → ℝ≥0` be fixed weights with sum one.
If every component kernel preserves the same measure `μ`, the weighted mixture
preserves `μ`. Markov components give a Markov mixture. The target measure is
arbitrary: it need not be finite, s-finite, positive or normalized.

`finiteMixture` is a finite sum of kernels with constant densities.
`finiteMixture_apply` identifies the resulting measure as the weighted sum.
The s-finite component assumption belongs to the pinned `Kernel.withDensity`
API; Markov kernels automatically satisfy it. Constant-density measurability
ensures this is the genuine branch, not the totalized zero fallback.

## Proof architecture

1. Evaluate the mixture on a measurable set using `Measure.bind_apply`.
2. Interchange a finite sum of nonnegative functions with the lower integral.
3. Pull out each fixed nonnegative weight and use component invariance.
4. Factor out `μ s` and use normalization of the weights.

No Bochner integrability or dominated-convergence assumption is needed for
this nonnegative finite-sum argument. Mathlib supplies all proof dependencies.
ASTIS heat-bath and finite-power declarations are inputs to the concrete test
consumer, **not** prerequisites of the mixture theorem itself.

## Consumers and boundaries

Tests construct an identity/heat-bath mixture and reuse `invariant_pow` for its
finite iteration. Zero weights are allowed. Thus the identity weight may be
zero; the test name does not certify positive holding probability or
aperiodicity. The empty-index definition is the zero kernel, but normalization
is impossible on that index type.

State-dependent selection weights, reversibility, mixing rates, coordinate
transport, concrete Gibbs normalization and computational implementation are
separate obligations. This source-neutral interface is motivated by the MCMC
and Discrete Sampling anchors in the cell; it does not assimilate a numbered
source theorem. `finiteMixture_apply` is an evaluation interface, not an
additional random-scan convergence result.
