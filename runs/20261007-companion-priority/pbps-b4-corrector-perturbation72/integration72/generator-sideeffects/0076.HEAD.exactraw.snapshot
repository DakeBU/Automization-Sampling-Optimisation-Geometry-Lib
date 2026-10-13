# AutoSamplingTheory.TechnicalLemmas.Probability.KernelReversibility

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/KernelReversibility.lean`.
- Layer: shared KERN/MEAS countable integration.
- Canonical packet: [random-scan reversibility cell](../../frontier-cells/ASTIS-SHARED-random-scan-reversibility.json).
- Actual consumer: `RandomScanHeatBath.randomScan_isReversible`.
- Focused tests: `Tests/RandomScanHeatBathReversibility.lean`.

## Statement

On a countable measurable space with measurable singletons, let `mu` be any
measure and `K` any kernel. If the singleton flux is symmetric,

\[
 \mu(\{x\})K(x,\{y\})=\mu(\{y\})K(y,\{x\})\quad\text{for all }x,y,
\]

then for any measurable sets `A,B`,

\[
 \int_A K(x,B)\,\mu(dx)=\int_B K(y,A)\,\mu(dy).
\]

The public conclusion is Mathlib's existing `Kernel.IsReversible K mu`. The
module does not create a second reversibility definition. Markovness, finite
target mass and finite output mass are not hypotheses of this bridge.

## Why the passage from points to sets is valid

Every set is countable, and singleton measurability lets Mathlib express its
mass as the sum of its point masses. Expand the outer set integral and each
kernel's mass on the other set. Interchange the two nonnegative countable sums
and apply the supplied pointwise flux equality term by term. This is Tonelli
arithmetic in extended nonnegative reals, not an exchange of signed integrals.
No integrability or finite-mass estimate is hidden in the argument.

`isReversible_of_singleton_balance` uses the pinned `lintegral_countable`,
`ENNReal.tsum_mul_right` and `ENNReal.tsum_comm` APIs. Its two public imports are
Mathlib's kernel invariance and countable Lebesgue-integration modules. It does
not depend on the finite Boolean heat-bath construction that consumes it.

## Scope and pitfalls

Countability is a real scope restriction: singleton masses alone do not
determine an atomless measure. This is not a general-state detailed-balance
criterion obtained for free from point probabilities. Zero or infinite atomic
masses are allowed in this nonnegative identity.

Mathlib's `IsReversible.invariant` additionally requires a **Markov** kernel;
the unrestricted bridge alone does not justify that stationary-law conclusion.
Neither this bridge nor its Markov consequence proves irreducibility, mixing,
an estimator guarantee, or computational cost.

This is an ASTIS-owned integration of existing Mathlib countable-measure facts,
not a new claim of an exact textbook theorem. Compilation, independent review
and Registry integration follow the canonical cell, not this prose.
