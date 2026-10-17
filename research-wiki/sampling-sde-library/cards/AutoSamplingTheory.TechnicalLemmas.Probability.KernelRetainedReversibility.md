# AutoSamplingTheory.TechnicalLemmas.Probability.KernelRetainedReversibility

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/KernelRetainedReversibility.lean`
- Layer: canonical shared KERN/MEAS detailed-balance interface.
- Public declaration: `retained_coordinate_isReversible`.
- Independent evidence: [source/compiler verification](../../technical-lemmas/retained-kernel-reversibility-independent-verification.json).
- Authored reader: `website/content/declaration_lessons/shared-retained-kernel-reversibility.json`.

Let A,B be arbitrary measurable spaces and let the joint law be mu compProd R.
If the jointly measurable, s-finite update F(a,b) is reversible under R(a) for
mu-almost every a, its retained-coordinate joint transition is reversible.
The retained measure and the kernels are s-finite, not necessarily probability,
finite or sigma-finite. No topology, nonempty-space, measurable-singleton,
Standard-Borel, finite-flux or signed-integrability premise is added.
Detailed balance alone does not imply invariance without Markovness.

## Proof technology and provenance

For arbitrary measurable joint sets S,T, their fiber sections are measurable
preimages. An indicator followed by nonnegative compProd integration expresses
the joint flux as the integral of its fiber fluxes. The deterministic product
retains a; a.e. fiber detailed balance swaps the inner fluxes. A.e. congruence
then reassembles the joint equality. This works for arbitrary joint sets, not
merely rectangles, and never subtracts infinite fluxes.

This is an ASTIS source-neutral standard derivation from pinned Mathlib
db584cd6, not a numbered PBPS theorem or a claim of new mathematical novelty.
The private `retained_flux` helper is covered by the public theorem's whole-file
review and is not an extra leaf. The two-step reader has exact adjacent folded
Lean and explicitly separates Mathlib calls from ASTIS ownership.

## Actual and planned consumers

No compiled downstream consumer is invented. Planned consumers are the SAME
actual PBPS half-turn under its exact conditional disintegration (A.2/A.9), and
general component-wise Gibbs/heat-bath detailed balance. Each must identify its
actual selected R and joint law. PBPS additionally needs separate coordinate
swap transport and its actual all-L2 realization; invariance alone is not that
adapter. The full PBPS one-step kernel is not assumed reversible.

## Evidence and remaining boundary

Focused producer/test build: PASS1884 jobs; an independent fresh production and
test compilation also passed, with only propext, Classical.choice, Quot.sound.
Blind reconstruction and distinct source review accepted all seven semantic
slots without repair. Normal VERIFIED publication is independently authored.
Registry/root stabilization, merge, deployment and PURIFIED are separate.

No actual-process A.2/A.9 operator, Markov restart/semigroup, hypocoercivity,
quantitative error, stopping/cap, actual-input expected cost, initialization,
composition or complete paper follows from this shared theorem.
