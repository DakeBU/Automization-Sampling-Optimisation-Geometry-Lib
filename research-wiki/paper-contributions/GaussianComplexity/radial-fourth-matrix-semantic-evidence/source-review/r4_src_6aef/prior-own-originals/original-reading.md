# Frozen independent raw-source reading — r4_src_6aef

This reading was reconstructed from the pinned HTML and repository process
instructions before receiving any proposed type/definition packet,
implementation, graph, decoder reconstruction, compiler receipt, exposition,
mapping, prior audit, or prior verdict. It is a mathematical source reading,
not a Lean verification or an acceptance decision about a future candidate.

Source: *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1,
`.astis/huanjian-resume-20261103/2610.20492v1.html`, 951991 UTF-8 bytes,
942139 Unicode code points, SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
The exact raw fragments and their source byte/code-point/line locators are
recorded in `source-manifest.json`; `.txt` files are convenience projections
using each math element's own `alttext`, not replacements for raw HTML.

## 1. Standing objects and conventions

Section 2 defines the norm as Euclidean, the identity as the identity matrix,
and, for symmetric real matrices, A <= B as positive semidefiniteness of B-A.
The order in the present reading is this matrix Loewner order, not an
entrywise order and not an almost-sure comparison of scalar norms.

Section 4.1 supplies integers d >= 2 and the parameter kappa >= 2. For
i = 1,...,d,

    theta_i = (i - 1/2) pi / d,
    lambda_i = (kappa+1)/2 + (kappa-1) cos(theta_i)/2,
    Lambda = diag(lambda_1,...,lambda_d).

Section 4.2 takes a nonnegative integer query budget q with 2q+1 < d and
independent vectors g_1,...,g_(q+1), each with law N(0,I_d). The block Krylov
space is the span of Lambda^j g_a for 1 <= a <= q+1 and 0 <= j <= q. Set
n = 2q+1 and D_n = diag(cos(n theta_i)). The main Lemma 4.4 is a uniform
bound on that space, subject to its stated smallness condition on tau_(d,q).
It is background scope for the present proof paragraph; the local fourth
moment and truncation identities do not assume the smallness condition.

Appendix C.2 sets r = q+1. In particular r >= 1, d >= 2, and 2r <= d. The
coordinates of the deterministic vector t_i are indexed by j = 0,...,q:

    (t_i)_0 = 1,
    (t_i)_j = sqrt(2) cos(j theta_i) for 1 <= j <= q.

The random vector gamma_i is ((g_1)_i,...,(g_r)_i)^T, with coordinates
indexed by a = 1,...,r. The vectors gamma_1,...,gamma_d are independent
N(0,I_r). This follows from all coordinates of the independent standard
Gaussian g_a. No conditional Gaussian law, target covariance, random
eigenbasis, or nonscalar covariance matrix is used in Ex113.

B is a real d by r^2 matrix with row i equal to
d^(-1/2) (gamma_i tensor t_i)^T. Its columns can be indexed by the pair
(a,j), 1 <= a <= r, 0 <= j <= q. A consistent product-index convention is
mathematically sufficient; an implementation must preserve the order of the
tensor factors or provide the corresponding permutation adapter.

The deterministic identities needed below are proved in Fact C.5:

    ||t_i||^2 <= 2r,
    sum_i t_i t_i^T = d I_r,
    sum_i cos(n theta_i) t_i t_i^T = 0.

The first two are ingredients of the p14 PSD chain. They are not extra
hypotheses of the public source Lemma 4.4. The weighted identity is used
elsewhere in the same concentration proof.

## 2. Local literal definitions

Inside the proof of Fact C.6, the source defines

    L = 2r + 3 log(1000d),
    R_i = ||gamma_i||^2 = sum_(a=1)^r (gamma_i)_a^2,
    Y_i = (1/d) (gamma_i gamma_i^T tensor t_i t_i^T)
                  1_{R_i <= L},
    Z_i = Y_i - E[Y_i].

These are literal finite-dimensional real objects. R_i is squared norm,
not norm. The event is inclusive at L; its complement is R_i > L. The
normalization in Y_i is 1/d and the normalization in its square is 1/d^2.
The source L is deterministic and positive in the standing domain, and
log is the natural logarithm. The selected scalar a in the earlier radial
truncation argument is also defined literally by

    a = (1/r) E[R_i 1_{R_i <= L}].

Its formula is well defined because r >= 1. There is no off-source default
case, selected witness, quotient representative, or conditional choice in
these definitions. Ex113 itself does not concern the truncated law or a.

## 3. Exact core claims

For every i = 1,...,d, Ex113 asserts the matrix expectation

    E[R_i gamma_i gamma_i^T] = (r+2) I_r.

Its entrywise statement is

    E[(sum_c gamma_c^2) gamma_a gamma_b]
       = (r+2) if a=b, and 0 otherwise.

The source proves the off-diagonal entries by sign symmetry. A reflection
of coordinate a preserves the standard Gaussian law and R_i while changing
the sign of R_i gamma_a gamma_b when a != b. On the diagonal, independence
of distinct standard Gaussian coordinates and their scalar second/fourth
moments give

    E[R_i gamma_a^2]
      = E[gamma_a^4] + sum_(c != a) E[gamma_c^2 gamma_a^2]
      = 3 + (r-1) = r+2.

This explains the exact constant r+2. It is not a free constant, an
asymptotic estimate, a conditional expectation, or an additional premise.
For this identity alone the law of gamma_i suffices; independence between
different i is not mathematically needed.

Ex114 asserts, pointwise in the Gaussian realization,

    Y_i^2 = (R_i ||t_i||^2 / d^2)
              (gamma_i gamma_i^T tensor t_i t_i^T) 1_{R_i <= L}.

Here square means matrix multiplication. Its proof uses
(gamma gamma^T)^2 = ||gamma||^2 gamma gamma^T,
(t t^T)^2 = ||t||^2 t t^T, multiplication of Kronecker products,
and idempotence of an indicator. Gaussianity and independence play no role
in this algebraic identity. There is no claim that E[Y_i^2] equals
(E[Y_i])^2.

The p14 truncation step is the following chain of matrix inequalities:

    sum_i E[Y_i^2]
      <= ((r+2)/d^2) sum_i ||t_i||^2 (I_r tensor t_i t_i^T)
      <= (2r(r+2)/d^2) (I_r tensor sum_i t_i t_i^T)
       = (2r(r+2)/d) I_(r^2).

To obtain the first inequality, remove 1_{R_i <= L} from Ex114. The
untruncated expression is PSD: its scalar coefficient is nonnegative and
gamma gamma^T tensor t t^T is the outer product of gamma tensor t.
Consequently the difference produced by removing the indicator is PSD
pointwise. Expectation preserves this order, and Ex113 computes the
untruncated expectation. Pulling t_i outside the expectation is legitimate
because t_i is deterministic. This is not entrywise monotonicity of a
possibly signed entry and does not require the entries themselves to be
nonnegative.

The second inequality uses ||t_i||^2 <= 2r against the PSD matrix
I_r tensor t_i t_i^T. The final equality uses sum_i t_i t_i^T = d I_r.
All sums here are over i=1,...,d, and every matrix in the chain is real
r^2 by r^2. The denominator d is positive by the standing source domain.

The remainder of p14 derives

    E[Z_i^2] = E[Y_i^2] - (E[Y_i])^2 <= E[Y_i^2],
    v_* = 2r(r+2)/d,
    E[(cos(n theta_i) Z_i)^2]
      = cos^2(n theta_i) E[Z_i^2] <= E[Z_i^2].

The centered-square equality follows by expanding Y_i-E[Y_i] and taking
expectations; its subtracted square is PSD because E[Y_i] is symmetric.
Also E[Z_i^2] is PSD. Thus the same variance-parameter bound holds for the
weighted centered sequence. No assumption E[Z_i^2] <= E[Y_i^2], variance
bound, centering identity, or weighted bound is licensed as an added
source-facing premise: these are derived proof ingredients.

## 4. Integrability and implicit analytical content

The source writes all expectations without separate measurability or
integrability hypotheses. In this setting those properties are consequences
of the law and literal formulas, not additional source assumptions.

All coordinates are measurable standard Gaussian variables. Their
polynomials are measurable, the radial cutoff event is measurable, and
finite matrices can be integrated entrywise (equivalently, as finite-
dimensional Bochner integrals). The untruncated entries in Ex113 and the
untruncated Ex114 upper bound have degree four in gamma_i. Gaussian fourth
moments imply absolute integrability, permitting finite sum interchange,
sign-symmetry arguments, multiplication by deterministic entries, and the
matrix order passage through expectation. For example,
|R gamma_a gamma_b| <= R^2, and

    E[R^2] = 3r + r(r-1) = r(r+2) < infinity.

The truncated Y_i and Y_i^2 are integrable as well. In the standing source
domain they are bounded using R_i <= L on their support; Gaussian polynomial
domination also supplies a direct route. The centered matrices have finite
second moments. No extra tail-integrability, boundedness, covariance,
independence-across-i, or moment-bundle hypothesis should be added to Ex113
or to the public Lemma 4.4 merely to facilitate one proof.

The source invokes Gaussian scalar second/fourth moments, coordinate
independence, sign symmetry, the algebra of rank-one and Kronecker products,
and expectation preserving PSD order without independently named lemmas or
citations at p14. These are source-implicit mathematical justifications.
The identities and PSD chain themselves are printed source assertions.
There is no substantive local mathematical gap detected in these assertions.

## 5. Boundary and constant checks

At q=0, r=1, n=1, and d>=2. Then t_i=(1), gamma_i is scalar standard
normal, and R_i=gamma_i^2. Ex113 becomes E[gamma_i^4]=3. Ex114 becomes

    Y_i^2 = d^(-2) gamma_i^4 1_{gamma_i^2 <= L}.

The first PSD bound is 3/d in this scalar case. The displayed final source
bound is 6/d because ||t_i||^2=1 was loosened to <=2r=2. That looseness is
valid; it is not an endpoint exception. A proof that requires r>=2 or
q>0 would miss the source boundary. The dimension r=0 is outside this
source slice; a vacuous zero-dimensional library generalization is not the
source's q=0 case.

There is no kappa dependence in Ex113, Ex114, or v_*. The source precision
parameter kappa>=2 is used for the spectral family and the invertible
cosine/power change of basis; it supplies no extra local Gaussian moment
factor. The local fixed coefficients are exactly r+2 and 2r(r+2)/d.
The absolute sufficiently large constant C belongs to Fact C.6 and
tau_(d,q), not to these exact moment/algebra statements.

Fact C.6 proves probability at least 0.995 for both operator bounds.
Lemma 4.4 then uses tau_(d,q)<=1/2 and obtains the simultaneous Krylov
quadratic-form bound with probability at least 0.99. Those concentration
and smallness boundaries must not be conflated with the pointwise or
expectational content of p14.

## 6. Review boundary retained for the next phase

This is the original independent source reconstruction. It does not approve
any named declaration, definition, proof route, source mapping, graph,
decoder, exposition, or publication item. A later selective type/definition
audit must compare its exact inputs with the meanings above, recursively
expand project-owned assumptions and definitions, preserve q=0, and keep
every derived moment/PSD/integrability conclusion inside proof dependencies.
Any new candidate-specific conclusion must be recorded in a later artifact;
this frozen reading must remain intact.

Only this review directory was written. No ATLAS/API/proof search, production
Lean reading, compiler invocation, normal verification ledger, queue/frontier
mutation, commit, push, integration, or process permission grant was used.
