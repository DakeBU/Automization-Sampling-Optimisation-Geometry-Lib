# Convex gradient-flow Lyapunov and last-time upper bounds

SAU ANDI-OPT-gradient-flow-last-iterate-001; cell ASTIS-SHARED-gradient-flow-last-iterate.
Source Chewi2605.07006v1 Exercise2.1 upper-bound component; no companion credit.
Reuse ConvexityC2 and StrongConvexFirstOrder, plus Riesz derivative pattern from
GradientDescentOptimalStep. Hessian sign and actual gradient derivative derived;
no supplied Hessian positivity or scalar Lyapunov dissipation premise.
Differentiate L=t²normgrad²+2tgap+distance², cancel terms, use convex support;
right K0 scalar comparison gives antitone L on[0,T]. Drop nonnegative terms
for gradient²<=D0/t²; support+Cauchy+Young gives4tgap<=L<=D0 and gap<=D0/(4t).

C2 Hilbert generalization explicit; minimum and actual flow supplied. Positive
time only for normalized rates, closed Lyapunov includes0 and T0. Nonsmooth
positive-part sharpness witness remains an unbound source obligation; do not
mark full Exercise2.1 complete. No Exercise2.2 or existence claim.
Conceptual-mirror audit none-found: existing metric-gradient-flow family and
convex energy-distance mechanisms already retained. No new transport edge.

Focused PASS2733 actual quadratic exp(-t) trajectory tests antitone energy and
both rates at arbitrary nonnegative horizon; standard axioms only. Independent
pl_pullback_review accepted frozen98b2ee7d2036776eb8b8a142b162484305667dfb;
fresh last_blind_94793 and distinct last_source_94793 source audit accepted.
Verdict implicit-assumption-exposed retains Hilbert generalization, supplied
finite flow/minimum, positive normalized time and incomplete sharpness scope.
Root Analysis/Tests imports and Registry428/Tests.Basic synchronized.
Canonical full gate passed at c82ea86718548c0ee27f88626ee65e569c9ccda5; exact JSON retained.
Current source digest dbd22a55c052e0293d2d59310e30afb027393f904e765ec49089d3ea9be47cfd.
Workflow221/harness256(skips6),6JS syntax checks and generator compileall passed.
Publication87/semantic104audits7repairs/frontier112 checks passed; old103audits,
17items and ledger prefixes preserved. Canonical gate PASS9222 with actual Tests.Basic64s/Tests52s.
Site build/check PASS12chapters428local leaves691modules4009declarations,
77reviewed teaching. Graph-check PASS6direct relations, omitted0.

Root actual CUA visual inspection at desktop1280x900 and mobile390x844:
chapter-02.html#chewi-opt-v1-gradient-flow-last-iterate displays the three-term
Lyapunov and exact coefficients1/t² and1/(4t), supplied minimum/flow,
positive-time rate boundary and five proof steps. Statement/proof opened;
actual Lean code501/4750characters and proof inspected. KaTeX errors0;
documentwidth=scrollWidth1265desktop/375mobile. Long formula/code use their
own horizontal scrollers. No page-wide overflow.

Affected graph has26nodes46edges and6direct relations: owning-module structural
edge; three incomplete source-name references to existing convexity results;
chapter02 source correspondence and independent semantic-audit links.
Structural ownership is solid; reference/source/audit relations are dashed.
Desktop declaration inspector and mobile audit inspector checked. The graph
retains implicit-assumption-exposed (generic fidelity-mismatch colour), with
accepted review state, explicit Hilbert extension and unbound nonsmooth
sharpness. It does not claim source-domain equivalence or whole exercise
completion. Actual Mathlib calls remain in the lesson. Mobile graph document
width=scrollWidth375, KaTeX errors0. Tabs27/28 closed, viewport reset and
preview server stopped. No layout implementation changes.
Previous release Lean34754534011 on487920e and site34754571381 on7f367b1
completed successfully before this work.

Preserve unrelated local files. Next candidate: inspect the Exercise2.1
positive-part sharpness witness with its local smooth-arc/global C2 boundary.

Final independent integration review accepted by pl_pullback_review, with no
pending checks; exact report retained beside canonical gate evidence.
