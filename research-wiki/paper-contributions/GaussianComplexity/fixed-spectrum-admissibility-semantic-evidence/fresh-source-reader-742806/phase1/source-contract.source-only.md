# Independent source-only contract

Authority: On Complexity of Gaussian Sampling, arXiv:2610.20492v1.
Exact raw HTML SHA-256: 6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915.
The raw paper is preserved under raw-inputs/. Derived excerpts are conveniences.

## Exact family and principal result

For integer d>=2, real kappa>=2, and 1<=i<=d, Eq. (11) defines

    theta_i = ((i - 1/2) pi)/d
    lambda_i = (kappa+1)/2 + ((kappa-1)/2) cos(theta_i)
    Lambda = diag(lambda_1,...,lambda_d).

For every real O satisfying O^T O=I_d, set A=O Lambda O^T.
The short Lemma 4.6 concludes I_d <= A <= kappa I_d in Loewner order.
This covers full O(d), determinant +1 and -1. The hard-family Haar draw and its
independence from algorithm randomness are separate from this universal fact.
Section 2's ambient class d>=1,kappa>=1 does not erase the family's d>=2,kappa>=2.

## Full C.4 content and exact target meaning

The source proof asserts these moves, with no external citation in C.4:

1. The grid has 0<theta_i<pi, hence -1<cos(theta_i)<1, hence 1<lambda_i<kappa.
2. Diagonalization and orthogonality give I_d<=A<=kappa I_d for the actual A.
3. V_A(x)=x^T A x/2 is C-infinity with Hessian A, hence 1-strongly convex and
   kappa-smooth.
4. V_A(0)=0 and V_A(x)>=||x||^2/2>0 for x!=0, so 0 is the unique minimizer.
5. The associated target is the actual Gaussian N(0,A^{-1}); A is precision and
   A^{-1} is covariance.
6. Gaussian integration gives

    Z_A = (2 pi)^(d/2) (det A)^(-1/2)
        = (2 pi)^(d/2) (det Lambda)^(-1/2).

Since Lambda is fixed, Z_A is independent of O and known when the spectrum is
public. In particular det(A)=det(Lambda)>0 for both determinant signs of O.
No orientation-preserving hypothesis is available.

The semantic expansion of the Gaussian law and normalizing integral is

    Z_A = integral_{R^d} exp(-x^T A x/2) dx
    density(pi_A)(x) = Z_A^{-1} exp(-x^T A x/2)
                    = sqrt(det A)/(2 pi)^(d/2) exp(-x^T A x/2).

Here dx is Euclidean Lebesgue volume on the entire space, distinct from Haar
probability on O(d). C.4 writes "Gaussian integration" and its result rather
than explicitly spelling out dx. The display records ordinary Gaussian meaning,
not an extra assumption. Remark 1.3 explicitly uses pi proportional to exp(-V).
The half in the exponent, inverse covariance, exponent d/2, and distinction
between integral Z_A and reciprocal density prefactor must be preserved.

## Source ingredients versus inputs

Inputs are the standing d,kappa ranges, exact grid, real carriers, orthogonality.
Angle, cosine, eigenvalue, quadratic-form, Hessian, unique-minimizer,
integrability and determinant facts are ingredients/consequences. They cannot
be extra public source-facing hypotheses merely because producer lemmas exist.

The source compresses "orthogonal conjugation preserves spectral bounds",
"the quadratic has Hessian A", and "Gaussian integration gives the formula".
This phase records those source moves; it does not certify formal implementation,
source-graph completeness, dependencies or Lean closure.

## Failure and source-scope boundaries

- Restricting to SO(d) loses the stated full-group domain.
- Replacing exact A=O Lambda O^T by an arbitrary already-admissible matrix loses
  the actual fixed-spectrum construction.
- Scalar-grid or diagonal-spectrum bounds are narrower than Lemma 4.6. Matrix
  admissibility alone is narrower than full C.4 regularity/target/normalization.
- Swapping precision and covariance, dropping the inverse, changing exp(-V_A),
  using a Gaussian base law for the integral, or confusing Z_A and Z_A^{-1}
  changes the object.
- Strict eigenvalue bounds use kappa>1 supplied by kappa>=2. At kappa=1 they
  become equalities; any extension requires explicit classification.
- Public spectrum means no dependence of Z_A on unknown O. It does not mean
  independence from d,kappa and does not specify computational cost.
- Lemmas 4.3--4.5 concern Krylov representation, uniform cosine estimates and
  target moments. They are nearby context, not Lemma 4.6 hypotheses/conclusions.
- Theorem 4.1 separately has fixed delta in (0,1), d>=d_0(delta),
  2<=kappa<=d^(1-delta), 0<epsilon<=1/10, and
  Q_G>=(delta/256)sqrt(kappa)log d. C.4 admissibility is not that main lower bound.
- Section 2 exact first-order/matrix-vector oracle equivalence is context.
  Query budgets in the paper are deterministic caps per run, not expected costs.

## Phase-one limit

This is a fresh source-text reconstruction. No candidate Lean statement, code,
tests, proof explanation, publication, exact seals, source graph/topology
outputs, old reviewer verdict contents, anonymous packet or blind reconstruction
has been opened. No candidate status, fidelity, mathematical closure, module or
reader acceptance is asserted. The filename-enumeration caveat is disclosed in
the exposure record. Later comparison must preserve the distinction between a
narrow producer, full C.4 content, and Theorem 4.1.
