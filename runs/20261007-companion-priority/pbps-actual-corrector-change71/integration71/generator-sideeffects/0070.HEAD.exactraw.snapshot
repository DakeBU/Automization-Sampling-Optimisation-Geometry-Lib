# AutoSamplingTheory.TechnicalLemmas.Probability.CoordinateHeatBath

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/CoordinateHeatBath.lean`.
- Layer: shared KERN/MEAS operational integration.
- Contract and current evidence: [canonical Frontier Cell](../../frontier-cells/ASTIS-SHARED-coordinate-heat-bath.json).
- Actual consumers: `Tests/CoordinateHeatBath.lean`.

## Mathematical interface

A state has finitely many possibly different coordinate types. To update site
`i`, the existing measurable equivalence splits the state as `(r, s)`, with
retained coordinates `r` first and selected coordinate `s` second. For the
pushed-forward joint measure, select the regular conditional law `κ(r)` of
the second component given the first. The transition law at `x` is

\[
  K_i(x)=(e_i^{-1})_\#\bigl(\delta_{r(x)}\otimes\kappa(r(x))\bigr).
\]

`heatBath` is the single public construction. `heatBath_isMarkovKernel` and
`heatBath_invariant` reuse the existing one-block construction and generic
measurable-equivalence transport. They are adapters within one integration
packet, not separately counted new mathematical leaves.

The substantive operational statement `heatBath_ae_apply_eq` says that, for
an unselected site `j`, `y j = x j` almost everywhere under `K_i(x)`. This
distinguishes a coordinate update from an arbitrary target-invariant kernel,
which could resample the whole state instead.

## Assumptions and their roles

- Each coordinate has a measurable space. The target is a finite measure,
  including zero; no probability normalization or density is imposed here.
- Only the selected coordinate must be nonempty and Standard Borel, as
  required to select the conditional distribution in this construction.
- Literal retention at `j` requires `MeasurableSingletonClass (X j)`. It does
  not require singleton measurability of every other coordinate or of the
  whole retained product. These assumptions are absent from the invariant
  law and Markovness interfaces.
- The public indexing uses `Fin (n+1)`: a selected site exists. Finite coordinate
  count is not finite state space. Arbitrary finite-index reindexing already
  has Mathlib equivalence APIs and is not duplicated as a new splitting leaf.

## Why the omitted step is valid

The conditional law is a probability measure, so the first marginal of its
product with the retained Dirac measure is that Dirac measure. Measurable
evaluation at the retained site gives an almost-everywhere equality under
the Dirac measure; pull this equality back through the first projection and
then push the product law through the inverse split. `j != i` identifies `j`
as one of the retained `succAbove` coordinates. Every map uses its genuine
measurability proof.

This uses native marginal-product and almost-everywhere map facts. There is
no public duplicate of Mathlib's coordinate split or first-marginal theorem.
Equality of laws on a coarse sigma-algebra must not be mistaken for equality
of sampled coordinate values: the measurable-singleton condition is visible
exactly at that step.

## Tests and dependency roles

The tests check the actual public kernel on a three-site Boolean product with
a middle-site update, simultaneous retention by finite intersections, and a
zero target. A retained coordinate with an indiscrete sigma-algebra exercises
the weaker marginal-law/invariance contract without asserting literal retention.

The fixed-mixture and finite-power tests join this public kernel with existing
`KernelMixture` and `KernelInvariance`. Those modules are consumer-test inputs,
not proof parents of coordinate retention or single-site invariance.

## Strict source boundary

This is a noncomputable law interface, not an executable conditional sampler.
The chosen conditional version is characterized only almost everywhere under
the retained marginal. Retention of the other coordinates holds independently
of any feasible-support claim for that version on marginal-null fibers.

MCMC section 2.1.1 and Discrete Sampling section 1.3 motivate the integration;
the exact page/byte audit is in
`runs/20260908-samplewiki-resume/source-coordinate-update-audit.md`.
The Discrete Sampling copy-index repair still needs independent source review.
This card does not assimilate a numbered source theorem, certify the repair,
establish concrete Gibbs support or normalization, or assert reversibility,
ergodicity, mixing time, continuous-time domains or sampling cost.
