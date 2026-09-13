# Two actual gradient flows: contraction

SAU ANDI-OPT-gradient-flow-contraction-001; cell ASTIS-SHARED-gradient-flow-contraction.
Source: Chewi2605.07006v1 Definition1.5 / Theorem2.2.
User-directed optimisation continuation; no companion-paper theorem credit.

Reuse StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn.
Subtract actual right ODE derivatives, differentiate squared norm (safe at zero
separation), apply monotonicity, then existing finite-interval right-slope
Gronwall. The squared bound has rate2alpha and the norm bound ratealpha.
Alpha>=0 preserves the source convention; zero is nonexpansive. No attained
minimum, gradient Lipschitzness, nonzero distance or negative-time dynamics.
Complete Hilbert / differentiable / right-time hypotheses are explicit source
generalizations. Curves are supplied; no existence/extension theorem.

Conceptual-mirror audit: none-found. Existing metric-gradient-flow and curvature
growth families cover this mechanism; no new transport or stochastic certificate.
Focused tests derive actual quadratic trajectories for arbitrary initial points,
including coincident points and t0; separate zero-curvature test. Root Tests
import and Analysis import are present; Registry425 agrees with Tests.Basic.
Independent pl_pullback_review checked frozen262ceaf5fd46cb53090042b9f9f84a0ac35197e2.
Fresh contract_blind_81342 reconstructed only an anonymous packet; distinct
contract_source_81342 accepted an explicit domain-mismatch generalization.
All module/test/lesson hashes are unchanged after review; no repair required.

Aggregate candidatee5b46bb4abb6725b2b3ac4f6c47df3ced438da8a passed full gate9216,
including actual Tests.Basic66s and Tests59s, ATLAS inventory and fake closures.
Exact unedited gate JSON is retained in the existing semantic evidence folder;
source_digest3a6e2c4f885283578fe58f52b7deb0d5af0e854b19d8e2b151f6e2032056444a.
Workflow union221 passed. Full harness256 passed with6 Windows-only skips;
earlier localhost/Lean-PATH failures were environmental and were rerun with
localhost permission and explicit elan/Homebrew PATH, keeping tests unchanged.
Six JavaScript syntax checks and generator compileall passed separately.
Publication84, semantic101/6repairs, Frontier109, site685modules4006declarations
and425registered leaves passed. Prior100audits/14optimisationitems and old
ledger byteprefixes remain unchanged.

Root visual inspection: desktop1280x900 and mobile390x844 reader at
chapter-02.html#chewi-opt-v1-gradient-flow-contraction. The statement, displayed
chord/ODE/contraction formula, three proof steps, endpoint assumptions and
accepted domain-mismatch are visible. Both Lean disclosures start closed and
were opened; actual statement434/proof1871code characters present, proof code
viewed. KaTeX errors0; docwidth=scrollWidth1265desktop/375mobile. Mobile formula
has its own horizontal scroller. No layout implementation changed.

Graph focus decl:AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowContraction.norm_sub_le
shows11nodes13edges and4direct relations: module ownership solid; chapter02,
semantic audit and gradient-monotonicity source reference scan dashed. The
actual parent is also named in the lesson. Compiled badge, directions, labels,
reader link and mobile name wrapping checked. Reference scan is incomplete,
not an elaborated Lean dependency certificate; no planned uniqueness consumer
or stochastic/conceptual transport is marked compiled. Temporary tabs21/22
closed, viewport reset and local server stopped.
Next candidate: source Theorem2.4 objective rate, with alpha0 limiting case
handled explicitly, after searching existing convex-flow energy interfaces.

Merged and pushed directly to `main` at `3db5e6829342bd673ec6e2b0f0e70af7607af05d` under standing
user authorization. SAU `MERGED` releases the single stabilization lane. Remote
post-push CI/deployment is separate from passed local evidence.
