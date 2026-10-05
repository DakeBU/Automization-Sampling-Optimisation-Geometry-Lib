# Convex gradient-flow objective rate

SAU ANDI-OPT-gradient-flow-value-001; cell ASTIS-SHARED-gradient-flow-value.
Source: Chewi2605.07006v1 Theorem2.4. User-directed optimisation continuation;
no companion-paper theorem credit. Reuse shared first-order convex support.

Actual chain rule derives objective decrease using scalar right-slope Gronwall
on every subinterval with K=epsilon0. Differentiate squared distance to the
supplied minimizer, then use first-order support and objective decrease to
freeze the terminal gap in constant negative forcing. Scalar (not norm) Gronwall
permits that negative forcing. K0 gives D0/(2t); K=-alpha gives
alpha*D0/[2(exp(alpha*t)-1)]. No scalar comparison or generic integral reproof.

Source endpoint: printed t>=0 is singular at0 for both coefficient branches.
Keep original source wording; formal theorem uses positive observation time.
Quadratic exp(-t) actual flow at0 gives gap1/2, while Lean total quotient is0.
A separate exact-proposal review accepted the positive-time domain
clarification. No analytic alpha-to-zero limit theorem is claimed. Hilbert/
differentiability/right-time generalizations and supplied minimum remain clear.

Conceptual-mirror audit none-found: existing metric-gradient-flow/curvature-growth
families already retain distance-energy scalar comparison; no new transport.
Proof/test/lesson frozen at e15a55bf9f73450143cbc0ff9131a7e9068932f3 and
independently checked by pl_pullback_review. Fresh anonymous decoder,
value_source_92471 anti-anchored source review and distinct value_repair_92471
exact-proposal review accepted; source verdict remains domain-mismatch.
Root Tests and Analysis imports are present; Registry426 matches Tests.Basic.
Nonstationary quadratic tests cover both curvature branches plus the endpoint
counterexample; focused build PASS2480, standard axioms only.

Aggregate candidate00d937ea54cde89521f6d852fa727a7feb903a47 passed full gate9218,
including actual Tests.Basic81s, Tests74s, ATLAS36469 declarations/26books and
fake-closure scan. Exact unedited canonical-gate-evidence.json retained;
source_digest d6aee1cc33d1d60c49aca3d4723ac775062e94e9b8701cd1ee5ee71e9ccbf909.
Workflow union221 and full harness256 passed (6 Windows-only skips), as did
six JavaScript syntax checks and Python generator compileall. Publication85,
semantic102/7repairs, Frontier110 and site687modules4007declarations426leaves
passed. Prior101audits/15optimisationitems and ledger byteprefixes preserved.

Root visual inspection: desktop1280x900 and mobile390x844 reader at
chapter-02.html#chewi-opt-v1-gradient-flow-value. Both curvature coefficients,
positive-time assumptions, four proof steps and separately accepted source
repair are visible. Actual Lean statement452/proof4240 code characters opened
and proof viewed. Disclosures initially closed. KaTeX errors0;
documentwidth=scrollWidth1265desktop/375mobile, formula has its own scroller.
Original source t>=0, actual Lean t>0 and accepted exact repair remain separate.

Graph focus decl:AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowValue.value_le
shows17nodes23edges,4direct relations: module ownership solid; first-order
support reference scan, chapter02 correspondence and semantic audit dashed.
Audit-to-repair association dashed; repair is a proposal, not a Lean theorem.
Desktop and mobile inspector show compiled badge, line22, prerequisite and
reader/evidence link; mobile width=scrollWidth375. Source scan is incomplete,
not an elaborated implication certificate. No new conceptual transport or
planned accuracy-time consumer is marked compiled. Temporary tabs23/24 closed,
viewport reset and local server stopped. Existing unrelated files excluded.

Next candidate after this packet: inspect Chewi Corollary2.8 gradient-norm
consequence and existing actual-flow dissipation/integral interfaces before
choosing another reachable theorem edge.

Final independent integration review accepted by pl_pullback_review; report
retained in the existing semantic evidence folder. Rebuilt the contribution
graph after lifecycle metadata refresh; final site/graph checks pass.

Merged and pushed directly to `main` at `378303c9ee474067f7d418390fb8ebb637a010cf` under standing
user authorization. SAU `MERGED` releases the single stabilization lane. Remote
post-push CI/deployment is separate from passed local evidence.
