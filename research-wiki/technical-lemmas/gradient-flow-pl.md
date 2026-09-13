# Actual gradient-flow dissipation and PL decay

SAU ANDI-OPT-gradient-flow-pl-001; cell ASTIS-SHARED-gradient-flow-pl.
Source Chewi2605.07006v1 Section2 Lemma2.1 and Corollary2.6.

For a supplied continuous curve on[0,T] with its actual right gradient ODE
beforeT, derive d(f composed X)/dt=-norm gradient squared by the Frechet
chain rule and Riesz identity. PL gives e prime<=-2alpha e; reuse pinned
Mathlib finite-interval right-slope Gronwall to get0<=e(t)<=e(0)exp(-2alpha t).
The ASTIS SemigroupDecay interface requires all-real derivatives, so do not
force this forward flow into a negative-time existence hypothesis. No scalar
Gronwall reproof, artificial flow construction or supplied energy identity.

Source generalization: complete real Hilbert space, differentiability rather
than C2, and right derivative rather than two-sided. Terminal continuity is
retained. AtT0 the derivative clause is empty and the bound equality. Positive
alpha and supplied attained minimum retain source conventions. No pointwise
trajectory convergence, convexity, discretization, stochastic process or paper
completion. Mathematical scheduling remains the user's optimisation task.

Reuse audit: runs/semantic-roundtrip/andi-opt-gradient-flow-pl/upstream-review.json.
Conceptual-mirror audit none-found: existing metric-gradient-flow/gap-gradient
families already retain this exact dissipation/PL/Gronwall mechanism. No new
cross-domain hypothesis map or transport certificate was discovered.

Compiler diagnosis: use the explicit Riesz continuous-linear derivative and
simp only to avoid the simplifier replacing it with opaque fderiv; unfold slope
for the existing one-sided comparison. No hypothesis change. The nonstationary
quadratic test proves its real gradient/minimum/PL and actual exp(-t) trajectory;
rate exp(-2t) is exact, includingt0.

Focused compile PASS2470. Frozen72b56d03335823f040b7c01dbf1479a979db71f2,
independent pl_pullback_review production/proof audit. Fresh source-blind
gf_decode_67183 and anti-anchored gf_source_67183 review accepted the source
specialization, with domain-mismatch explicitly retained. A provisional globally
equivalent label was rejected by the gate; the independent reviewer corrected
it without relabeling genuinely wider domains or weaker assumptions. No repairs.

Aggregate candidate5855e2ccd8b828c0a91e73f09befe463996107b8: PASS9214 including
actual Tests/Tests.Basic and fake-closure scan. Source digest
8288f61517132e3428fedf6f4a4a5e227289266c79b1a7506e3a0be4eb7d402a.
Exact source-bound gate JSON retained unedited in the existing evidence folder.
Root Analysis/Tests imports and Registry424/Tests.Basic agree. Website209 and
formalization84 workflow suites pass; harness256 passes with6 Windows-only
skips, six JavaScript syntax checks and generator compilation pass. Publication83,
semantic100/6repairs, Frontier108, site683modules/4005declarations/424leaves pass.

Root actual visual checks (not independent reviewer's screenshots):
- Reader chapter02#chewi-opt-v1-gradient-flow-pl: desktop1280x900 and mobile390x844,
  authored statement, formulas, three proof steps, accepted domain-mismatch and
  explicit endpoint/regularity boundaries checked. Both Lean disclosures initially
  closed, then opened; statement528/proof1642code characters. Actual proof code
  viewed. KaTeX errors0; document width=scrollWidth1265desktop/375mobile.
  Long mobile formula has its own horizontal scroller.
- Graph focus decl:AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowPL.dissipation_and_decay:
  5nodes4edges,3direct highlighted relations: owning module declares solid,
  source chapter02 and semantic audit dashed. Actual arrows/labels and compiled
  badge checked; mobile long-name wrapping and reader link present, width375.
  Mathlib calls are listed in the lesson, not invented ASTIS parent nodes.
  Planned nonlinear-pullback consumer is not a compiled dependency.
- Temporary tabs19/20 closed, viewport reset and localhost server stopped.

Next bounded candidate: source/reuse audit of Chewi Theorem2.2 actual two-flow
contraction from the existing strong-convex gradient-monotonicity interface.
Keep flow existence and gradient-distance decay separate from this PL value rate.
Do not count the scalar Gronwall helper or a wrapper as another mathematical SAU.
