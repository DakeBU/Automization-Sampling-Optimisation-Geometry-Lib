# Reconstructed mathematical statement

For every pair of natural numbers d and q such that 2q + 1 < d, make the following definitions. All coordinate indices are zero-based. Write J = {0,...,d−1} and I = {0,...,q}, let D = R^d and E = R^(q+1) with their Euclidean norms and Borel structures, and let Ω = I → D. Give Ω the product probability measure μ consisting of one standard Gaussian law on D for each b in I. Thus a sample ω assigns a vector ω(b) in R^d to each b in I; these vectors are independent centered Gaussian vectors with identity covariance.

Let r be the real number q+1, and define the real numbers

    L = 2r + 3 log(1000d),
    C = 2r(r+2)/d,

where log is the natural logarithm and natural-number parameters are embedded in R in scalar formulas. For each i in J, set

    θ_i = (i + 1 − 1/2)π/d = (i + 1/2)π/d,
    t_i(0) = 1,
    t_i(k) = sqrt(2) cos(kθ_i)  for k = 1,...,q.

Here sqrt(2) is the nonnegative square root; when q = 0, only the coordinate t_i(0) occurs. For ω in Ω, define the row vector x_i(ω) in E by

    x_i(ω)_b = ω(b)_i  for b in I.

Define the real matrix Y_i(ω), with both its rows and columns indexed by I × I, by

    Y_i(ω) = (1/d) (x_i(ω)x_i(ω)^T) ⊗ (t_i t_i^T)
                 if ||x_i(ω)||_2^2 ≤ L,
             0   if ||x_i(ω)||_2^2 > L.

The outer products and Kronecker product here mean exactly that, on the first branch, the entry in row (b,k) and column (c,l) is

    (1/d) x_i(ω)_b x_i(ω)_c t_i(k)t_i(l),

for every b,c,k,l in I. On the second branch, every entry is zero. Equality at the truncation threshold is included in the first branch.

Then both of the following assertions hold:

1. For every i in J, the matrix-valued function ω ↦ Y_i(ω)Y_i(ω) is Bochner integrable with respect to μ. More explicitly, it is almost everywhere strongly measurable and its operator norm has finite integral. The product is ordinary matrix multiplication, so this is the integrability of the matrix square, not of the entrywise square.
2. With Id denoting the identity matrix on the paired index set I × I, the matrix

       C Id − Σ_{i=0}^{d−1} ∫_Ω Y_i(ω)Y_i(ω) dμ(ω)

   is symmetric positive semidefinite. Equivalently,

       Σ_{i=0}^{d−1} ∫_Ω Y_i(ω)^2 dμ(ω) ≼ [2(q+1)(q+3)/d] Id,

   where ≼ is the positive-semidefinite order on real matrices: the difference on the right minus the left is symmetric and has nonnegative quadratic form on every vector in R^(I × I). All matrix integrals in these assertions are Bochner integrals in the complete Euclidean operator norm.

# Seven-slot analysis

## 1. objects

The fixed objects are D = R^d, E = R^(q+1), the sample space Ω = {0,...,q} → D, the finite product standard Gaussian measure μ, the real scalar r = q+1, the real scalars L and C, angles θ_i, deterministic cosine vectors t_i, coordinate-row random vectors x_i, and random real matrices Y_i indexed in both directions by {0,...,q} × {0,...,q}. The vector x_i is precisely the Euclidean vector with coordinates ω(b)_i; the WithLp wrappers do not change those coordinates. The outer products and Kronecker product have the paired-index ordering stated in the reconstructed theorem.

## 2. domains

The parameters d and q are natural numbers, including zero before the hypothesis is imposed. The hypothesis forces d ≥ 2q+2; q = 0 is allowed. Coordinate indices i range from 0 through d−1. Indices b,c,k,l range from 0 through q, including both endpoints. Samples ω belong to Ω. The vectors x_i and t_i lie in E; Y_i has (q+1)^2 rows and columns and real entries. All scalar formulas use the usual embedding of natural numbers into R. Euclidean norms are used for vectors, and the complete Euclidean operator norm is used for matrix Bochner integrability.

## 3. quantifiers

For every pair of natural numbers d and q satisfying 2q+1 < d, form all displayed objects by their fixed definitions. The first conclusion holds for every i in {0,...,d−1}. The second conclusion concerns the finite sum over that same entire index set. Positive semidefiniteness includes symmetry and the nonnegative quadratic-form condition for every real vector indexed by {0,...,q} × {0,...,q}. No constant, truncation level, angle, or vector is existentially chosen.

## 4. assumptions

The sole mathematical hypothesis on the parameters is the strict inequality 2q+1 < d. The Gaussian law, product sample measure, cosine vectors, truncation level, and matrices are definitions, not additional hypotheses. Integrability is an asserted output. The condition ||x_i(ω)||_2^2 ≤ L is the branch condition defining Y_i at each sample, including equality; it is not an assumption that samples satisfy that condition.

## 5. conclusion

For each i, the matrix-valued function ω ↦ Y_i(ω)Y_i(ω), with ordinary matrix multiplication, is Bochner integrable against μ: it is almost everywhere strongly measurable and the integral of its operator norm is finite. In addition, C times the identity matrix minus the sum over all i of the Bochner integrals of Y_i(ω)Y_i(ω) is a real symmetric positive semidefinite matrix. Equivalently, the sum of these matrix second moments is at most C times the identity in the positive-semidefinite order. This is a deterministic order statement about integrated matrix squares, not a pointwise or probability bound. The explicit integrability assertion ensures these are integrable Bochner integrals rather than reliance on totalized nonintegrable integrals.

## 6. scopes

The universal parameter quantifiers and their strict dimension hypothesis enclose every local definition and both conjuncts of the conclusion. One common Ω and μ is used for all i. The angles and cosine vectors are deterministic; x_i and Y_i depend on ω. The truncation branch applies separately to each i and ω, using the squared norm of that row, with the zero matrix on the complementary event ||x_i(ω)||_2^2 > L. In the second conclusion, each product Y_i(ω)Y_i(ω) is integrated before the finite sum is taken. The identity has the paired index set {0,...,q} × {0,...,q}. No almost-sure qualifier weakens the resulting deterministic matrix order assertion.

## 7. constant_dependencies

The scalar r = q+1 depends only on q. The truncation level is exactly L = 2r + 3 log(1000d), with natural logarithm, and depends only on d and q. The bound is exactly C = 2r(r+2)/d, depending only on d and q. The numbers 2, 3, and 1000, the factor sqrt(2), the half-grid shift 1/2, and π are fixed constants. The angles θ_i depend only on i and d; the cosine coordinate t_i(k) is fixed by i,k,d, with k ranging through 0,...,q. No scalar constant depends on ω or is left unspecified.
