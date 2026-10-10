# AutoSamplingTheory.TechnicalLemmas.Probability.KernelInvariance

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/KernelInvariance.lean`
- Layer: shared KERN interface
- Purpose: propagate a supplied invariant measure through finite kernel powers.
- Contract/status: [canonical Frontier Cell](../../frontier-cells/ASTIS-SHARED-kernel-invariant-powers.json).

For an arbitrary measurable state space, kernel and measure, one-step
invariance implies invariance for every natural power. Induction uses the
identity kernel at zero and Mathlib's invariant-composition theorem at a
successor. Neither finiteness nor Markov normalization is assumed here.
`bind_pow_eq` only changes notation; it is not a second mathematical leaf.

The real downstream use is iterating a verified heat-bath/MCMC transition.
Starting from another law, ergodicity and mixing bounds are separate results.
The reversibility test explicitly supplies the Markov assumption required by
Mathlib's reversibility-to-invariance implication. See `Tests/KernelInvariance.lean`.

## Imports

- `Mathlib.Probability.Kernel.Invariance`
- `Mathlib.Probability.Kernel.Composition.Comp`

## Representative Declarations And Exports

- `invariant_pow`
- `bind_pow_eq`

## Curated Formalized Memory Entries

- `probability.kernel.invariant-powers` -> `invariant_pow` (Mathlib.Probability.Kernel.Invariance; Mathlib.Probability.Kernel.Composition.Comp)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
