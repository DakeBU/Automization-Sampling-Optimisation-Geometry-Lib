# Next source route: compact-test Poincare from compact-test LSI

Planning only; not a Statement Seal, implemented theorem or admitted Bench task.
This continues the existing independently reviewed source-topology-v2 plan.
Do not reset the Exercise1.7, paper, cycle or wider form-domain frontiers.

## Target and dependency order

For a Borel probability measure on a finite-dimensional real Hilbert space,
assume one fixed source constant `C > 0` and

\[
  \operatorname{Ent}_\mu(v^2)\le 2C\int\|\nabla v\|^2\,d\mu
  \qquad(v\in C_c^\infty).
\]

The next source consumer should derive, for every compact smooth `g`,

\[
  \int\left(g-\int g\,d\mu\right)^2d\mu
  \le C\int\|\nabla g\|^2\,d\mu.
\]

Its final public inputs must not include centering, finite-energy certificates,
square-root LSI admissibility, an entropy expansion or the desired comparison.
Produce those inside the proof. First finish the current independent review of
`LogSobolevCutoff`; this plan does not promote its PROVED_LOCAL state to VERIFIED.
Freeze the exact elaborated interface and definition semantics before starting
the next proof. A centered analytic helper is useful only if actually consumed
by this uncentered target, not as a replacement for it.

## Reuse, then close the remaining joins

1. Set `f = g - integral g`. Derive smoothness, global boundedness, zero mean,
   and compact support of the derivative from the actual compact smooth `g`.
   Centering generally destroys compact support of the function. Prove the
   unchanged-gradient and variance identities, rather than assuming them.
2. Reuse
   `CompactGradientSqrtPerturbation.eventually_contDiff_and_integrable_sqrt_perturbation`.
   It constructs the actual smooth `u_e = sqrt(1+e*f)`, L2 and entropy inputs,
   the eventual global lower bound, and both finite derivative energies.
   The Riesz norm/measurability handoff in `Tests/Shared/LogSobolevCutoff.lean`
   demonstrates the existing interface; do not copy another cutoff proof.
3. Apply `LogSobolevCutoff.logSobolev_of_compact_test` to that actual `u_e`.
   Probability mass and centering give `integral (1+e*f)=1`; positivity gives
   `u_e^2=1+e*f`. Expand Mathlib's literal `klFun` and justify integral algebra
   using the produced integrability, obtaining
   \[
   \operatorname{Ent}_\mu(u_e^2)
      =\int\operatorname{klFun}(1+ef)\,d\mu.
   \]
   The existing `BoundedPerturbationLaw` identifies the actual probability KL
   separately if needed for the literal hint. Do not infer differentiability
   of an RN representative or invent a canonical Fisher identity.
4. For `e != 0`, divide the valid inequality by the positive number `e^2`.
   Reuse `BoundedDensityPerturbation.tendsto_integral_klFun_one_add_mul_div_sq`
   and `BoundedPerturbationEnergy.eventually_integrable_and_tendsto_sqrt_perturbation_energy`:
   \[
   \frac{\operatorname{Ent}_\mu(u_e^2)}{e^2}
      \longrightarrow\frac12\int f^2\,d\mu,\qquad
   \frac{\int\|\nabla u_e\|^2\,d\mu}{e^2}
      \longrightarrow\frac14\int\|\nabla f\|^2\,d\mu.
   \]
   Derive the Frechet/gradient norm identities. Keep the punctured-neighborhood
   filter and coefficient `2C` explicit; no division at zero is valid.
5. Pass closed real order to the limits. Cancel the factor one half and use
   the identities from step1. This proves compact Euclidean PI with the same
   admissible constant, not equality of optimal constants.

## Source and remaining boundary

Chewi, *Log-Concave Sampling*, August20 2026, pinned PDF SHA256
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`:
Exercise1.7 / (1.E.1), printed43/PDF55; compact function LSI and density discussion,
printed48-49/PDF60-61. This is original ASTIS planning, not reproduced prose.

The full Chapter1 form-domain/core extension, abstract reversible-energy
statement, optimal-constant passage and complete numbered-exercise/QA admission
remain separate. The existing source-only topology is not a progress ledger:
its SOURCE_GAP labels may be closed only with actual reviewed proof evidence.
No new QA, leaf, chapter/paper completion, empirical difficulty or model score
is awarded by this plan. The shared stabilization lease remains foreign-owned.
