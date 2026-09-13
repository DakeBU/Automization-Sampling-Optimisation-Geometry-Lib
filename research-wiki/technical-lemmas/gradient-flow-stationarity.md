# Gradient-flow stationarity on a compact time interval

SAU ANDI-OPT-gradient-flow-stationarity-001; cell ASTIS-SHARED-gradient-flow-stationarity.
Source Chewi2605.07006v1 Section2, Lemma2.1 and Corollary2.8.
User-directed optimisation continuation; no companion-paper completion credit.

Reuse compact minimum and scalar K0 right-slope comparison. C1 gives gradient
continuity via fderiv and Riesz inverse. Choose minimum m, derive actual energy
derivative=-normgradient²<=-m², compare endpoints and use supplied minimum.
Divide by T>0 and take sqrt. Exact source coefficient1; no convexity or PL.
Existing PL theorem has unwanted PL/positive-curvature assumptions, hence is
not imported as an unconditional dissipation helper. MVT requires two-sided
interior derivatives; existing right-slope comparison directly fits this API.
The independent route audit considered a terminal-lower-bound generalization;
final theorem retains the source global minimizer instead.

Truth boundary: C2 Euclidean source generalized to C1 Hilbert and right-time
finite interval. Positive time implicit in finite quotient; no t0 convention.
No flow/minimum existence, final-time gradient estimate, infinite-time sequence,
trajectory convergence, discrete algorithm or stochastic transport theorem.
Conceptual-mirror audit none-found: existing metric-gradient-flow family and
prior gradient-descent-stationarity memory already retain energy-budget
averaging. No new cross-space bridge or coercivity implication.

Focused build PASS2470: actual nonstationary quadratic and zero-gap constant
trajectories; standard axioms only. Independent pl_pullback_review accepted
frozen ca8905c3410a983b1d2c6652c0550a9cd4d43afa; fresh source-blind decoder
stationarity_blind_93582 and anti-anchored stationarity_source_93582 accepted.
Source verdict domain-mismatch records explicit Hilbert/C1/finite-interval
generalizations; source minimum is retained, no repair required.
Root Analysis/Tests imports and Registry427/Tests.Basic are synchronized.
Canonical full gate passed at a63c31edc055d17b8bcedb71e6634f1ebe426641; exact JSON retained.
Source digest 3e512cefd4921efd0656b16f35acf645fc480ea7212ca2fef22968c57a337efc.
Workflow union221, full harness256 (6 Windows skips), six JS syntax checks
and generator compileall passed. Publication86, semantic103/7repairs and
Frontier111 checks passed. Old102audits/16items and ledger prefixes preserved.
Canonical gate PASS9220, actual Tests.Basic72s and Tests58s. Site build/check
PASS12chapters427local leaves689modules4008declarations,77reviewed teaching.
Graph-check PASS3direct relations, omitted0. Unrelated local files preserved.

Root actual visual inspection at desktop1280x900 and mobile390x844:
chapter-02.html#chewi-opt-v1-gradient-flow-stationarity displays the exact
sqrt coefficient, attained-minimum quantifier, all hypotheses and four proof
steps. Seven disclosures initially closed; Lean statement/proof opened, actual
code375/2009characters, proof viewed. KaTeX errors0; documentwidth=scrollWidth
1265desktop/375mobile. Long formula uses its own horizontal scroller.

Graph focus decl:AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowStationarity.exists_min_norm_le
has5nodes4edges,3direct relations: owning-module arrow solid; chapter02
correspondence and source-audit links dashed. The actual Mathlib calls are
listed in the lesson; no ASTIS parent or conceptual transport is invented.
Desktop branch and audit inspector checked: domain-mismatch remains visible,
source and reconstruction distinct; no repair or source-equivalence badge.
Mobile inspector compiled badge, exact line23, owning module and reader link
readable; documentwidth=scrollWidth375. Tabs25/26 closed, viewport reset and
preview server stopped. No layout implementation changes.


Previous release CI checked before this work: Lean34750741374 on378303c and
site34750764461 on42be71d succeeded; old cancelled site run superseded.

Next candidate: source Exercise2.1 last-time convex gradient bound, after
retrieval and differentiable-gradient/Hessian interface audit.

Final independent integration accepted by pl_pullback_review. Metadata-refreshed
site/check and graph passed; graph slice matches the inspected version exactly.
Exact review retained in the existing semantic evidence folder.
