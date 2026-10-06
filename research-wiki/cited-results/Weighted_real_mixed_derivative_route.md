# Real mixed weak derivatives after actual compact Sobolev

2026-10-06. Root raw interface proposal, not compiled or independently admitted.
PBPS2609.06905v1 AppendixC.1 and SPHMC2609.06906v1 Section4.1 motivate the
remaining local regularity/weighted core dependency. The current compact
Schwartz/Sobolev candidate is still EXPLORING under independent review.

Retain actual v=chi*u and Gchi=chi*G+u*gradient chi from the same originalD/u,
actual global volume L2/supports and the ordinary all-C1 weak gradient. The
candidate derives actual AE-linked complex L2 TD T_v and MemSobolev2; a final
first-distribution-derivative or real Hessian certificate must not be supplied.

Proposed route in six steps:
1. Extend the actual first weak-gradient identity to all complex Schwartz tests
   using the same strict outer plateau and real-linear Re/Im Frechet calculus.
   With g_a=inner(Gchi,a), derive partial_a T_v=LpTD(ofReal(g_a)), using true
   global volume L2 of g_a, explicit AE classes, legal bilinear L1 and the
   negative sign in TemperedDistribution.lineDerivOp_apply_apply.
2. Apply pinned MemSobolev.lineDerivOp twice, order2 -> order1 -> order0,
   and memSobolev_zero_iff to construct an actual complex L2 class H_ab for
   partial_b(partial_a T_v). Sobolev.lean:316 is exactly the p=2 interface.
3. For a genuine real smooth compact test psi, embed its actual Schwartz map
   into complex Schwartz via the real-linear ofRealCLM. Evaluate that same
   mixed distribution at the test; the derived first TD identity gives the
   ordinary negative-gradient-test integral, with every L1 product justified.
4. Take real parts only after integral_re is legal. Re(H_ab)'s standard
   representative has volume MemLp2 via continuous real-linear projection,
   and should satisfy integral psi*Re(H_ab)=-integral g_a*Dpsi[b]. One need
   not first assert H_ab is a pointwise real class or map TD to a nonexistent
   complex-vector-space structure on real codomain. Actual real representative
   and weak identity still require compiled proof.
5. Retain AE representative identities. Any symmetry, finite-basis Hessian
   assembly or restriction to where chi=1 needs its own actual proof; do not
   assert support of a chosen quotient representative from raw support of v.
6. Only after these real weak derivatives are produced, pursue actual compact
   mollifier convergence and original weighted generator graph/core extension.

Pinned original APIs inspected: TemperedDistribution.lineDerivOp_apply_apply
(TemperedDistribution.lean:367), SchwartzMap.lineDerivOp_apply_eq_fderiv
(SchwartzSpace/Deriv.lean:104), HasCompactSupport.toSchwartzMap (Basic.lean:555),
MemSobolev.lineDerivOp/memSobolev_zero_iff, actual MemLp.toLp/coeFn_toLp and
integral_re. Complex TD pairing stays bilinear, with no conjugation.

Failure boundary: the actual first TD equation, projected real tested
derivatives/representatives, realness/domain/cast handling and Hessian/chi=1
adapter are unproved. Dimension0 and zero directions stay included. This note
does not assert localized weighted D membership, weighted H2/core/Bochner,
BL/Poincare, epsilon0, measurable fiber choice, source main or composition.
The Fourier factor (2pi)^-2 is the Bessel adapter normalization; it is not a
new physical PDE or Bochner coefficient. Reflected/RGO scales remain distinct.
Same space/volume/operator: proposed exact interface, not conceptual mirror.
