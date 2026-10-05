# Constant-step distance sharpness via an actual quadratic witness

Source: Chewi arXiv:2605.07006v1 Exercises3.2-3.3, Section3.
SAU `ANDI-OPT-gd-sharpness-001`; cell
`ASTIS-SHARED-gradient-descent-sharpness`.
Declaration `Analysis.GradientDescentSharpness.exists_quadratic_worst_case` in
`AutoSamplingTheory/TechnicalLemmas/Analysis/GradientDescentSharpness.lean`.

For 0<α≤β and each real fixed h, choose μ∈{α,β} attaining
M_h=max(|1−hα|,|1−hβ|). The actual f(x)=μx²/2 is C², α-strongly convex,
satisfies the global β upper model using its true gradient, and is minimized at0.
The theorem proves all these certificates. For every natural N, starting at1:

- ‖T_h^N(1)‖=M_h^N≥q^N, where q=(β−α)/(α+β).
- ‖T_(2/(α+β))^N(1)‖=q^N on the same constructed objective.

The witness depends on h, not N. Its α,β are valid class bounds, not both tight
constants: its intrinsic scalar condition number is1. No fixed matrix with both
extremal eigenvalues is constructed. This is a class-level fixed-step distance
obstruction, not a lower bound for adaptive/variable steps, accelerated methods
or all first-order algorithms. Full Section3 sharpness remains uncovered.

## Reuse and proof route

1. Compare endpoint magnitudes to choose μ.
2. Differentiate the actual scalar polynomial. Subtract μ‖x‖²/2 to identify
   μ-strong convexity, then lower its modulus with Mathlib StrongConvexOn.mono.
   The exact quadratic remainder gives the upper model; μ>0 gives the minimizer.
3. Instantiate compiled QuadraticGradientDescent.quadratic_eigenmode with μI
   and initial point1. Its norm gives M_h^N without a supplied recurrence.
4. Apply compiled GradientDescentOptimalStep.optimal_gradient_step to the
   certified objective, obtaining q≤M_h; monotonicity of powers gives q^N≤M_h^N.
5. The balanced endpoint scalars are q and−q; the exact norm formula gives q^N.

Samplinglib's parents supply the two component formulas but not this admissible
witness. Pinned Mathlib db584cd6d46c92f209a44c0f1c829460d327499d supplies
strongConvexOn_iff_convex, StrongConvexOn.mono, HasDerivAt.hasGradientAt and
pow_le_pow_left₀. Optlib5da27c5 has GD interpolation and upper-rate theorems;
CvxLean c62c2f has spectral algebra. The independent bounded search found no
matching parameterized attained lower witness; no external code was copied.
Lean4.33.0. Canonical full source audit is retained in the round-trip folder.

## Verification and integration notes

Focused Tests.Shared.GradientDescentSharpness PASS2871, standard axioms only.
Tests retain a genuine common witness for negative h (growth4^N versus balanced
2^(-N)), zero h (distance1), and α=β=2 (N=0 distance1, positive iterations0).
Independent proof verifier sharp_route_review, blind decoder sharp_blind and
source reviewer sharp_source accepted the scoped packet. Root Tests/Analysis
imports and Registry421 integrated. Canonical full ASTIS gate, reader and graph checks passed.

Conceptual-mirror audit: none-found. This is attainment within the existing
Euclidean quadratic gradient mechanism, not a new cross-domain transport.
No graph-family or companion-paper completion claim follows.

Next boundary after admission: select another precise Exercise3.3 comparison
with its exact source assumptions (for example objective-gap estimates), or a
source polynomial-method consumer, after a fresh dependency/reuse audit. Do not
repeat the exact trajectory or fixed-step distance-witness targets.

Full gate candidate `bce17df72799029d4cb60c18a16c4312bc3bd803` passed at `2026-09-13T03:18:56.228144+00:00`;
source digest `6e390fe3aae1f1a0053199cc060fd35862a169bddec87ca8705a24f6b674bb6e`. Canonical JSON retained in
`runs/semantic-roundtrip/andi-opt-gd-sharpness/canonical-gate-evidence.json`.

- Canonical gate PASS9208 build jobs, including root Tests and Tests.Basic,
  fake-closure scan and ATLAS36469 declarations/26books. Publication PASS80 items;
  semantic PASS97 audits/6 existing repairs; Frontier PASS105 cells. All96 prior
  audits and10 prior optimisation source items remain unchanged as objects.
- Site build/check PASS677 modules,4001 declarations,421 local leaves. Bounded
  graph-check passed. Graph delta adds the new module/declaration, chapter03
  correspondence and accepted semantic audit. The name scanner detects
  optimal_gradient_step and quadratic_eigenmode as references to the new theorem;
  these are dashed scanner edges, not exhaustive elaborated dependency certificates.
  Module ownership is solid. No completion badge or conceptual mirror was authored.
- Reader: libraries/optimisation/chapter-03.html#chewi-opt-v1-exercise-3-3-fixed-step-sharpness.
  Root inspected actual desktop1280/mobile390 statement, formulas, assumptions,
  remaining boundaries and both initially closed Lean disclosures, then opened
  statement and proof. KaTeX errors0; page width=scrollWidth1265 desktop and375
  mobile. Long mobile formulas scroll within their own container.
- Graph focus: lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness.exists_quadratic_worst_case&q=AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentSharpness.exists_quadratic_worst_case.
  Focused branch13 nodes/22 edges/5 highlighted relations was inspected on desktop;
  mobile detail wraps the full name and displays compiled badge, both references
  and reader link. This is root visual evidence, not the independent reviewer's
  own visual inspection. No layout code changed. Preview tabs/server are closed.

Merged and pushed directly to `main` at `d63ab0b916806e84151f627faad15dcc8a71ca17` under standing
user authorization. SAU `MERGED` releases the single stabilization lane. Remote
post-push CI/deployment is separate from passed local evidence.
