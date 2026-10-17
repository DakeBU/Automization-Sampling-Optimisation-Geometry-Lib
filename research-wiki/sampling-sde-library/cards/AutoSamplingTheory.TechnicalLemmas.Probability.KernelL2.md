# AutoSamplingTheory.TechnicalLemmas.Probability.KernelL2

- File: `AutoSamplingTheory/TechnicalLemmas/Probability/KernelL2.lean`
- Layer: canonical shared KERN/L2 interface.
- Public declaration: `invariant_kernel_l2_operator`.
- Evidence: [independent source/compiler verification](../../technical-lemmas/invariant-kernel-l2-independent-verification.json).
- Reader: `website/content/declaration_lessons/shared-invariant-kernel-l2.json`.

For an arbitrary measurable space, finite target and invariant Markov kernel,
construct one real L2 contraction. It realizes raw kernel integration for EVERY
MemLp representative, with genuine almost-everywhere fiber integrability.
It preserves the nonnegative cone, one and genuine means. Only a reversible
kernel additionally gives a self-adjoint operator. No topology, nonempty,
Standard-Borel, nonzero mass or supplied integrability premise is required.
Order positivity is not Hilbert positive semidefiniteness.

## Proof technology and provenance

The finite joint law has both marginals equal to the target. Coordinate
pullbacks give isometries B,C; P=B* C has norm at most one. Integrable indicator
pairings identify its representative with the raw conditional integral.
Invariance transports null sets, and reversible rectangle flux gives joint
swap symmetry and self-adjointness. This is a standard ASTIS derivation using
pinned Mathlib APIs, not a numbered PBPS theorem or its author proof topology.
Private proof technology from ActualL2Expectation is adapted rather than copied
into a second actual-process witness bundle; there are no ASTIS proof imports.
The private Prop and pair_operator helper are implementation, not extra leaves.

## Actual and planned consumers

No compiled downstream consumer is invented. The planned actual PBPS adapters
are the retained-coordinate half-turn on L2(J), A.2/A.9, and the actual one-step
observable operator B.1. Each must PRODUCE invariance from the actual law, and
the half-turn adapter must produce reversibility. The full one-step kernel is
not assumed reversible.

## Remaining boundary

The source-neutral generic interface does not complete either actual adapter,
process restart/semigroup, density evolution, hypocoercivity, quantitative
convergence, implementation/cap/error/cost, warm-start composition or any paper.
Independent verification, root integration, merge and PURIFIED remain distinct.
