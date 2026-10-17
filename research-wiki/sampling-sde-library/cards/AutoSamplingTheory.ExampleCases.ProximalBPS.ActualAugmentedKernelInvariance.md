# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAugmentedKernelInvariance

- File: `AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAugmentedKernelInvariance.lean`
- Layer: route-local actual-law integration node
- Purpose: Construct the literal reflected conditional-mixture PBPS transition and prove its normalized Gibbs augmentation invariant.
- Status: Independently source/compiler VERIFIED; aggregate integration and purification remain distinct.
- Evidence: [source, seal, focused tests and state](../../paper-contributions/PBPS/actual-augmented-kernel-invariance-verification.json).
- Reader: source-ordered formula proof and initially folded exact Lean in `website/content/declaration_lessons/pbps-actual-augmented-kernel-invariance.json`.

## Public declaration

`actual_augmented_kernel_invariant` closes Proposition3.4/eq3.11 for the SAME
literal process and half-turn H. Its original six analytic hypotheses and source
fixed rho in(0,1) do not include probability or invariance premises. The explicit
conditional R is pointwise q_y and disintegrates the actual augmented J.swap.

## Proof and reuse

Normalize Gibbs/augmentation using the owned producer, identify the chosen
conditional via nested tilts, use actual half-turn reversibility, and combine the
shared finite-mixture and coordinate-transport APIs. A private measurable-section
Tonelli lift proves joint preservation, and the existing Gaussian reflection is
applied before the mixture. The exact transition law is part of the conclusion.

Private `retained_invariant`, `reflected_conditional_mixture` and the complete
sealed Prop are implementation, not three extra mathematical leaves. Mathlib
supplies nonnegative kernel integration, disintegration and composition algebra.
The source uses Euclidean coordinates; finite Hilbert/rank-zero extension and
exceptional-clock representatives are explicitly audited. No null event uniform
in all parameters is inferred.

## Consumer and red boundary

Actual K is the planned input to PBPS Theorem3.5; no downstream compiled
convergence theorem is invented. Invariance alone proves no quantitative rate,
process restart/semigroup, augmented all-L2 realization, capped implementation
error, actual expected cost, warm-start composition or full-paper completion.
