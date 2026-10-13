# AutoSamplingTheory.TechnicalLemmas.Probability.ConditionalResampling

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/ConditionalResampling.lean`
- Layer: shared KERN/MEAS adapter
- Purpose: recover a joint finite measure from its first marginal and conditional second-coordinate law.
- Contract/status: [canonical Frontier Cell](../../frontier-cells/ASTIS-SHARED-conditional-resampling-law.json).

The retained coordinate is an arbitrary measurable space; the resampled
coordinate is nonempty and Standard Borel. Mathlib's disintegration theorem
applied to the two projections gives the identity after simplifying the
identity pushforward. The zero finite measure is allowed.

This is an adapter to an existing disintegration theorem, not a new proof of
disintegration. Conditional versions are only specified marginal-almost-
everywhere; no null-fiber support property is asserted. Constructing the
state-to-state heat-bath kernel and proving its invariance are real downstream
obligations, not consequences silently included in this statement.
Focused test: `Tests/ConditionalResampling.lean`.

## Imports

- `Mathlib.Probability.Kernel.CondDistrib`

## Representative Declarations And Exports

- `fst_compProd_condDistrib_snd_eq_self`

## Curated Formalized Memory Entries

- no curated formalized memory entries for this module

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
