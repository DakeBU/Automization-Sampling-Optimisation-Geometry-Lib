# Ordinary volume weak resolvent: independent source/API pre-read

Date: 2026-10-06. Independent source actor: `phase_source_reviewer_20261005`.
Read-only baseline: `3dd0f26066b68263deb9db1f37c66f3a5f874b17`.
Lean: `leanprover/lean4:v4.33.0`; pinned Mathlib:
`db584cd6d46c92f209a44c0f1c829460d327499d`.

This is a dependency-route capsule before a future candidate review. No new
candidate Lean, ignored `.astis` prototype, anonymous reconstruction or new
math verdict was read. No compilation, SAU, source acceptance, VERIFIED or
mathematical progress is established. The existing C1 public interfaces are
inputs, not a verdict about the proposed ordinary-resolvent implementation.
The older `Weighted_ordinary_resolvent_dependency_audit.md` was read as a
public API/route inventory; its review conclusions are not used as evidence.
Prior exposure remains explicit: an earlier BL keyword/signature search
exposed covariance helper matching lines; later legitimately issued covariance
review read those modules. Complete repository-wide candidate blindness is
not claimed. Root's ignored C1 and ordinary-Laplacian prototypes were not read.

## Primary contract and omitted detail

Fresh primary reads:

- [PBPS arXiv:2609.06905v1 Section 2.2](https://arxiv.org/html/2609.06905v1#S2.SS2),
  HTML168–211, equations2.6–2.14: actual Gibbs/Gaussian augmentation and
  reflection. The conditional law is a normalized actual density.
- [PBPS v1 Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1),
  HTML1197–1237, with Lemma C.1 HTML1276–1310 independently read in the
  preceding source/API capsule: smooth compact tests and a further weighted-H1
  extension; conditional Poincare/density are separate ingredients.
- [SPHMC arXiv:2609.06906v1 Section 4.1](https://arxiv.org/html/2609.06906v1#S4.SS1),
  HTML403–430: actual RGO score/covariance identities and BL/CR bounds.

The ordinary distributional PDE below is not a quoted numbered theorem in
these anchors. It is a source-backed analytic prerequisite for an intended
elliptic route toward BL. The source's omitted functional-analytic detail
must not be replaced by an assumed Poisson solution or final PDE certificate.
No claim is made that this particular implementation route is the source's
only necessary proof route.

The two fiber potentials are different:

\[
 W_y^{\rm RGO}(x)=V(x)+\frac{\|x-y\|^2}{2\eta},\qquad
 W_y^{\rm ref}(z)=V((y+z)/2)+\frac{\|z-y\|^2}{8\eta}.
\]

Under `z=2x-y`, the inverse is `x=(y+z)/2`, `dx=2^{-d} dz`,
`Z_ref=2^d Z_RGO`, and the reflected Hessian is
`(Hess V((y+z)/2)+eta^{-1}I)/4`. Gradient pullback has factor2;
Dirichlet energy has factor4. Transport of operator domains and epsilon
parameters requires a true adapter. Equality of the original-coordinate laws,
operators, or constants must not be inferred from pushforward alone.

## Exact seven-slot prerequisite

| Slot | Contract to retain |
|---|---|
| Objects | Same actual positive-epsilon weighted solution u, actual G=D.closure u, actual forcing f, true gradient of W, and ordinary distributional Laplacian. |
| Domains | Finite-dimensional real Hilbert/Borel full space, including dimension0; actual L2(mu) quotients with mu=volume.tilted(-W); all ordinary distributions/local norms use volume. |
| Quantifiers | One exact closable compact-smooth gradient D before epsilon/input; for every epsilon>0 and f in L2(mu), one u/G serves all tests and all compact restrictions. In the source consumer, common R/S before y and one D_y before epsilon/f. |
| Assumptions | Shared W only C1, genuine volume integrability of exp(-W), actual exact D graph/closability. Source consumer retains genuine V C2 with all-point/all-vector 0<alpha<=beta Hessian bounds, eta>0 and beta eta<=1. No local-L2/PDE/final-domain certificate supplied. |
| Conclusion | Preserve prior weak equations; derive u,G,f,k in L2(volume.restrict K) for every compact K, locally integrable squared norms, and the genuine volume distribution identity with k=epsilon u+inner(grad W,G)-f. |
| Scope | Analytic prerequisite; no classical second derivative of arbitrary L2 representative u, local H2, global core/Bochner, Poincare/BL, noncompact constant/linear test, zero-epsilon limit, macro H1, sampler/main/composition/cost claim. |
| Constants | Exact positive epsilon and unit Laplacian/drift coefficients; no curvature constant needed for the shared C1 identity. Reflected source factors8eta/one-quarter remain explicit. Local gradient bound M_K depends on compact K, not a global constant. |

The target is precisely

\[
 k=\varepsilon u+\langle\nabla W,G\rangle-f,\quad
 \forall\phi\in C_c^2(E),\quad
 \int u\Delta\phi\,dx=\int k\phi\,dx.
\]

Integrability of both displayed products and every individual term used in
splitting/rearrangement must be proved. C-infinity source tests specialize
C2 tests. Applying Lean's total `laplacian` to u itself would not establish
this distributional conclusion.

## Actual interfaces and smallest missing join

Fresh current public-interface reads:

- `FunctionalInequalities.WeightedResolventC1.weak_resolvent_c1`: same D/u/G,
  all-domain variational identity, ordinary C1 compact directional weak
  gradient, local volume integrability, and all three weighted C1 test L1
  products and exact equation. Neither a new D nor a new weak solution is
  needed.
- `FunctionalInequalities.WeightedLocalL2.lp_locallyMemLp_volume`: for each
  actual scalar/vector L2(mu) class under continuous W and genuine weight
  integrability, produces locally integrable squared norm and every compact
  volume-restriction L2. Its actual proof transfers a.e. measurability via
  `absolutelyContinuous_tilted`, then cancels continuous positive weights.
- `Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one` and
  `fderiv_apply_eq_inner_gradient_of_differentiableAt`: actual C1 continuity
  and directional/Riesz bridge, not an IBP or Hessian certificate.
- `Analysis.Calculus.Laplacian.laplacian_eq_sum_stdOrthonormalBasis` and
  `continuous_laplacian_of_contDiff_two`: actual test-function Laplacian
  coordinate/continuity bridges, not weak elliptic regularity.
- `ProximalBPS.ConditionalC1Resolvent.conditional_c1_resolvent`: actual
  common R/S disintegration/reflection, normalized reflected law, positive
  integrable partition and original dense closable D_y, retained before
  epsilon/input. This supplies the source-specific consumer without inventing
  the RGO/reflected adapter.

The smallest missing analytic join is:

1. Set `psi=exp(W)*phi` for C2 compact phi. W C1 suffices; this inverseweight
   test remains compact and C1. It need not be C-infinity or globally bounded.
2. Prove the actual product-rule gradient
   `grad psi=exp(W)*(grad phi+phi*grad W)` via Frechet/Riesz calculus. Cancel
   `exp(-W)*exp(W)=1` inside the justified weighted equation.
3. Obtain u/G/f compact-volume L2 separately. On compact K, continuous
   grad W is bounded by M_K, so `abs(inner(grad W,G))<=M_K*norm(G)`.
   Prove target volume a.e. strong measurability and the restricted a.e.
   bound before invoking `MemLp.of_le_mul`; sums give k compact L2.
   This also proves each unweighted compact-test product L1 before algebra.
4. For each standard orthonormal basis b_i, use C1 compact
   `chi_i(x)=fderiv phi x b_i` in the existing ordinary weak-gradient
   identity. Actual C2 and derivative-support facts give this test class.
5. Sum the genuine identities and use the finite-basis Laplacian/gradient
   bridges to obtain `integral u*Delta(phi)=-integral inner G grad(phi)`.
   Combining with step2 gives the displayed sign for k.
6. Convert all compact-restriction L2 results to local integrability of
   squared norms; retain every earlier weak-solution conjunct.

No global drift-product L2 is inferred from boundedness on each compact K.
The solution and its forcing may be noncompact. Only the tests and the
products supported by them are compact; no tail hypothesis is needed for
these particular products. Noncompact tests and global domain estimates
would require further cutoff/tail arguments.

Pinned Mathlib contracts actually inspected:

- `MeasureTheory/Function/LpSeminorm/Monotonicity.lean:188`,
  `MemLp.of_le_mul`: target a.e. strong measurability and a.e. norm bound
  are explicit inputs; compact-pointwise bounds need `ae_restrict_mem`.
- `MeasureTheory/Function/LocallyIntegrable.lean:312,332`, compact
  integrability and `locallyIntegrable_iff`; finite-dimensional full space
  supplies local compactness/metrizability.
- `Analysis/Calculus/ContDiff/Comp.lean:750`, `ContDiff.fderiv_right`:
  C2 gives C1 derivative, subsequently evaluate on a fixed direction.
- `Analysis/Calculus/FDeriv/Const.lean:388,392`, actual derivative-support
  and `HasCompactSupport.fderiv_apply`, requiring no supplied compact Hessian.
- `Analysis/Calculus/ContDiff/FTaylorSeries.lean:948`,
  `iteratedFDeriv_two_apply`; and the existing ASTIS finite-basis bridge.
  These are derivative identities, not a weak-H2 producer.

Dimension0 uses an empty orthonormal-basis sum and zero gradients/Laplacian;
canonical volume is nonzero, so actual Gibbs normalization still holds. The
scalar equation reduces to epsilon*u=f a.e. No unit vector or `[Nontrivial E]`
cutoff premise belongs in the proposed generic target. No separate 0D compile
was run in this preread.

## Source omissions and review policy

PBPS's compact-smooth-to-H1 passage additionally uses covariance continuity
and conditional Poincare. Its noncompact constant IBP needs real cutoffs;
neither follows merely from the local ordinary equation. SPHMC's BL covariance
upper bound needs a genuine analytic producer on the original unreflected
RGO law. Local L2 RHS is not local H2 or a global weighted Hessian estimate;
local H2 would itself not certify a global generator core or Bochner argument.
Fiberwise existence for every y is not a joint measurable choice of u_y.

Classification: `local-lemma` / `internal-paper-step` analytic prerequisite
with an explicitly omitted source-detail boundary. Available parent producers
and pinned calculus/L2 contracts are real; the distributional join and all
required integrability remain new proof obligations before implementation.
A later review must reject any convenient replacement u/G/D, assumed final
Poisson identity, changed sign, hidden C-infinity W, law/scale conflation, or
paper-completion claim. This preread assigns no acceptance verdict.
