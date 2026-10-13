# AutoSamplingTheory.TechnicalLemmas.Probability.KernelTransport

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/KernelTransport.lean`
- Layer: shared KERN/MEAS transport interface.
- Contract/status: [canonical Frontier Cell](../../frontier-cells/ASTIS-SHARED-kernel-invariant-transport.json).
- Focused consumers: `Tests/KernelTransport.lean`.

## Mathematical interface

Let `e : α ≃ᵐ β` be a measurable equivalence. If a kernel `κ : Kernel α α`
preserves a measure `μ`, transporting both its input and its output by `e`
gives a kernel preserving `μ.map e`. At state `y`, first return to `e.symm y`,
apply `κ`, and push the resulting law forward by `e`.

The theorem `invariant_map_comap` uses arbitrary measurable spaces, kernels and
measures. It does not need Markovness, finiteness, s-finiteness, topology,
Standard-Borel structure or nonempty spaces. It transports a law, not a density
relative to an unchanged reference measure; a density/Jacobian formula is a
different statement.

## Why this statement has this form

`Kernel.comap` changes the input coordinate and `Kernel.map` changes the output
law. They cannot be interchanged without checking the types and direction.
Measurability of both directions of `e` makes the pushforward cancellation
legitimate. In particular the proof uses the genuine measurable branch of
`Kernel.map`, not its nonmeasurable zero fallback.

The proof architecture is measure-level kernel composition: move the final
pushforward outside composition, replace input comap by deterministic
composition, cancel inverse pushforwards, and reuse the given invariance.
Mathlib supplies the measure/kernel algebra. No ASTIS heat-bath or mixture
theorem is a proof prerequisite of this transport result.

## Actual consumer and remaining obligations

Tests split a dependent finite-coordinate product using existing
`MeasurableEquiv.piFinSuccAbove`, followed by `prodComm`. This puts the selected
coordinate second, matching `heatBathSnd`. Transport pulls that update back to
the original coordinate space; fixed-mixture and finite-power interfaces can
then be reused.

The coordinate consumer needs a finite joint measure and a nonempty
Standard-Borel resampled coordinate. Retained coordinates need only
measurability. A finite number of coordinates does not imply finite state space.
Conditional representatives remain specified only marginal-almost-everywhere.

The private test constructions do not export a complete coordinate-update
algorithm. Retained-coordinate behavior, source-facing update correspondence,
concrete Gibbs support/normalization, reversibility and mixing remain separate
obligations. This source-neutral prerequisite is not numbered source-theorem
assimilation or a certified categorical functor.
