# Scaled residual: orthogonal graph route (proposal only)

2026-10-06. Root mathematical/API discovery, not compiled, independently
reviewed or admitted Lean truth. Current weighted-C1 packet inputs stay frozen.
PBPS2609.06905v1 Section2.2/AppC1 actual original-gradient Poincare and separate
SPHMC2609.06906v1 Section4.1 RGO covariance-upper background are the consumers.

For a genuinely closed partial-linear D:H->K on real Hilbert spaces, actual
positive-epsilon variational solutions satisfy
epsilon*norm(u)^2+norm(Du)^2=<f,u>. Let r=epsilon*u in the SAME domain.
Then norm(r)^2+epsilon*norm(Du)^2=<f,r>, hence norm(r)<=norm(f) and
norm(Dr)^2<=epsilon*norm(f)^2. These are proposed algebraic consequences,
not supplied limit certificates. No uniform norm(u) bound/Poincare is used.

An actual weak cluster v of r_n, epsilon_n->0, together with Dr_n->0,
can be shown to satisfy (v,0) in the SAME closed graph by testing against
its genuine Hilbert orthogonal complement: for every q=(a,b) in graph(D)^perp,
<r_n,a>+<Dr_n,b>=0. Real weak/strong inner limits give <v,a>=0; genuine
double-orthogonal=closed-graph then gives graph membership. This avoids a
WeakSpace/WeakDual product homeomorphism or an unbounded-adjoint certificate.

If f is truly orthogonal to EVERY kernel element, then <f,v>=0. Passing the
actual energy inequality norm(r_n)^2<=<f,r_n> along that weak subsequence
forces strong r_n->0. A subsequence contradiction can yield the whole
sequence. Thus residual centering itself is unnecessary for this step:
the actual zero-gradient-implies-constant direction and genuinely centered f
already supply kernel orthogonality in the actual probability space. Actual
constant-domain membership still supplies centered test/domain subtraction
and real noncompact score consumers; no earlier packet is bypassed or erased.

Pinned Mathlib db584cd6d46c92f209a44c0f1c829460d327499d was searched:
Analysis/Normed/Module/WeakDual.lean has WeakDual.isSeqCompact_closedBall370,
requiring genuine separability of H. Riesz InnerProductSpace.toDual maps the
bounded r_n to bounded functionals; a weak-star limit is pulled back by the
actual inverse Riesz isometry, with all evaluations checked.
Topology/Algebra/Module/Spaces/WeakDual.lean283 has the genuine eval-tendsto
criterion. InnerProductSpace/Projection/Submodule gives actual
Submodule.orthogonal_orthogonal_eq_closure/orthogonal_orthogonal; exact APIs,
real product-inner conventions and completeness must be elaborated first.
The ordinary product H x K has the max norm, not the Hilbert product norm.
Use the actual WithLp2 product: comap the SAME D.graph by
WithLp.linearEquiv2, and obtain its true closedness from
WithLp.prod_continuous_ofLp. Then WithLp.prod_inner_apply gives the real sum
of the two inner products. An ignored weak-plus-strong graph-interface
prototype passed standard3 at attempt3 after two field/simp API corrections;
it is not production, independently reviewed, an SAU or a residual-zero proof.
MeasureTheory/Measure/SeparableMeasure.lean382 gives IsSeparable for actual
countably-generated/SFinite measure, and427 gives actual Lp second-countable.
Finite real Hilbert/Borel E and true finite conditional probability should
supply those instances; this adapter remains UNPROVED, not inferred from
finite-dimensional underlying E to finite-dimensional L2.

Proposed route, at most seven steps:
1. Prove actual scaled-domain/energy/boundedness/Dr->0 from variational data.
2. Establish real L2 separability from the actual measure/topological APIs.
3. Extract actual weak-star Riesz subsequences for every bounded subsequence.
4. Prove weak-plus-strong graph admission by the actual orthogonal complement.
5. Use actual kernel orthogonality and energy to force strong residual-zero.
6. Prove whole-sequence convergence by actual subsequence contradiction.
7. Combine the accepted actual global m*normDu^2<=normf^2 and variational
   test at a centered original-domain z to derive m*normz^2<=normDz^2.

Step7 is a separate later integration node: no epsilon0 solution/range or
uniform unscaled u is needed before Poincare. Exact reflected quarter constant
and later unreflected RGO scale must remain distinct. Actual scalar mean/AE
constant L2 pairing, original domain subtraction and variance/energy quotient
representatives still require concrete adapters; future linear observables
still need actual Gibbs L2 moment evidence. No source theorem, spectral gap,
core/adjoint, covariance upper, main result, measurable fiber selector or
actual input precision/expected-cost composition is completed by this note.

Failure policy: verify exact double-orthogonal/closed-domain and separability
instances before proof search. Do not replace weak sequential compactness by
an assumption of finite-dimensional L2, graph weak closure by a supplied
certificate, or centeredforcing by an unexplained normalization. Retire an
API route after repeated unchanged failures; preserve the strict residual.
