# Convex gradient-descent gap order sharpness

Source: Chewi arXiv:2605.07006v1 Exercise3.3 testing Theorem3.4, Section3.
SAU `ANDI-OPT-convex-gap-sharpness-001`, cell
`ASTIS-SHARED-convex-gradient-gap-sharpness`.

For beta>0 and each natural N, set D=N+1, mu=beta/(2D), f_N(x)=mu*x²/2.
Prove C2, positive strong convexity mu, global beta upper model and minimizer0.
Actual GD step1/beta from1 has gap beta/(4D)*(1-1/(2D))^(2N)>=beta/(16D).
Bernoulli gives q^N>=1+N(q-1)=(D+1)/(2D)>=1/2, then square and multiply.
For N>=1 the lower bound is at least beta/(32N), matching the source beta/(2N)
upper rate in order. The Lean theorem states the finite N+1 bound.

Quantifiers: forall N construct f_N. Curvature shrinks with N. Beta is a class
upper bound, not the tight smoothness constant. No one fixed strongly convex
quadratic is claimed to have a reciprocal asymptotic tail. The constant1/16 is
an authored convenient bound, not an optimal or source-printed constant. N0
retains actual gap beta/4; no singular1/N upper formula is interpreted.
Only step1/beta, initial distance1; no adaptive or general oracle lower bound,
all-section sharpness, acceleration or companion-paper completion.

## Reuse and diagnosis

Reuse GradientDescentSharpness.exists_quadratic_worst_case at equal endpoints
mu to obtain the exact objective, its certificates and true gradient norm.
Use Mathlib one_add_mul_sub_le_pow, abs_mul_abs_self and pow_mul. Same-witness test
composes GradientDescentValue.gradient_descent_weighted_value_bound; the upper
rate is a test consumer, not a fabricated production dependency.
Independent bounded source/reuse audit in
runs/semantic-roundtrip/andi-opt-convex-gap-sharpness/upstream-review.json.
Mathlib db584cd6d46c92f209a44c0f1c829460d327499d; Lean4.33.0.

Compiler diagnosis: local function abbreviations must be aligned before
nonlinear arithmetic; squaring via explicit multiplication avoids overloaded square normalization.
In the consumer test, clear only the outer scalar denominator rather than
rewriting inside the actual gradient function.
These are representation issues, with no mathematical assumption change.

## Verification and integration notes

Focused compilation PASS2875; same-witness upper/lower sandwich and zero/one
horizon tests, standard axioms only. Independent proof reviewer sharp_route_review accepted frozen commit
001c58d3a38d1e7b7c10d7c56a50b584a9171eae. Fresh decoder convex_blind and
source reviewer convex_source accepted the scoped publication packet, with
equivalent-after-elaboration and no repairs. Root Analysis/Tests first-line
imports and Registry422 integrated. Canonical aggregate gate PASS9210, including root Tests and fake-closure scan;
reader/graph checks passed.
Conceptual-mirror audit: none-found; horizon choice plus elementary scalar
Bernoulli within the existing quadratic GD mechanism, no new transport family.

Next boundary: audit remaining Section3 comparisons or Section5 polynomial
consumer; do not repeat scalar trajectories or this horizon-dependent witness.

Independent integration review preserves all97 prior audits and11 prior
optimisation source items exactly as objects, and the full prior ledger prefix.
Publication PASS81 items; semantic PASS98 audits/6 existing repairs; Frontier
PASS106 cells. Source review initially used field aliases; the independent
reviewer corrected them to the required schema without changing mathematical
content or packet hashes. The current artifact/run hash is the admitted one.

Full gate candidate `1ae34ce4671af921069166f22ed3c7d374e88563` passed at `2026-09-13T04:38:32.041924+00:00`;
source digest `70284874c9dc40f34e43565ccfaa0f919dd2269ace0ab3c8e5db245b80dd11fd`. Exact canonical evidence retained in
`runs/semantic-roundtrip/andi-opt-convex-gap-sharpness/canonical-gate-evidence.json`.

- Site build/check PASS679 modules,4002 declarations,422 local leaves; bounded
  graph-check passed. Graph delta adds production/test modules, one declaration,
  chapter03 correspondence and independent semantic audit. Module ownership is
  solid. The existing name scanner detects exists_quadratic_worst_case as a
  reference to quadratic_gap_lower_bound; this dashed reference is not an
  exhaustive elaborated dependency certificate. The general weighted upper-rate
  theorem is used in the consumer test, not claimed as a production dependency.
- Reader: libraries/optimisation/chapter-03.html#chewi-opt-v1-exercise-3-3-convex-gap-sharpness.
  Root inspected actual desktop1280/mobile390 statement/formulas/assumptions and
  source-boundary display. Both Lean disclosures initially closed (statement503
  code characters, proof2892); opened statement/proof, actual statement code
  visible and proof body present. KaTeX errors0; page width=scrollWidth1265
  desktop,375 mobile. Long mobile formulas scroll within their own container.
- Graph focus: lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.ConvexGradientGapSharpness.quadratic_gap_lower_bound&q=AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexGradientGapSharpness.quadratic_gap_lower_bound.
  Root inspected branch10nodes14edges4highlighted relations, correct parent,
  compiled badge, distinct solid/dashed structure and reader link. Mobile detail
  wraps the full theorem name. Visual evidence is root-attributed, not the
  independent reviewer's own inspection. No layout code or completion badge was
  changed. Temporary preview tabs/server closed and viewport restored.

Merged and pushed directly to `main` at `4ccbce816286249bb3e075999fc78359d583809b` under standing
user authorization. SAU `MERGED` releases the single stabilization lane. Remote
post-push CI/deployment is separate from passed local evidence.
