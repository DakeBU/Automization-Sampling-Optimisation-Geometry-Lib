# Reconstructed proposition

For every pair of natural numbers d and q such that 2q + 1 < d, set n = q + 1 and let r be the real number obtained by embedding n into the reals. Use Fin m = {0, ..., m - 1} as each coordinate index set. Define D = R^d and E = R^n with their Euclidean norms and Borel structures, Omega = (Fin n -> D) with its product measurable structure, and mu = the finite product, over b in Fin n, of the centered identity-covariance Gaussian probability law on D.

Define L = 2r + 3 log(1000d), where log is the natural logarithm and d in this expression is embedded into R. For i in Fin d, define
  theta_i = (i + 1 - 1/2) pi / d,
and, for k in Fin n, define the real coordinate function
  t_i(k) = 1                              if k = 0,
           sqrt(2) cos(k theta_i)         otherwise.
Here i and k appearing in real arithmetic denote their natural-number values embedded into R, and sqrt denotes the nonnegative square root.

For i in Fin d and omega in Omega, let x_i(omega) be the vector in E with coordinate x_i(omega)_b = omega(b)_i for every b in Fin n. Let I = Fin n x Fin n. Define a real matrix Y_i(omega) with row and column index set I by
  Y_i(omega) = d^(-1) [(x_i(omega) x_i(omega)^T) tensor (t_i t_i^T)]
                    if ||x_i(omega)||_2^2 <= L,
              0     otherwise.
The first branch includes equality. The outer products have their ordinary coordinate meaning, and tensor denotes the Kronecker product: for a,b,c,e in Fin n, the entry with row (a,b) and column (c,e) in the first branch is d^(-1) omega(a)_i omega(c)_i t_i(b) t_i(e).

The following conjunction holds:
  (1) For every i in Fin d and every omega in Omega,
        ||Y_i(omega)||_op <= 2rL/d.
  (2) For every i in Fin d,
        || integral_Omega Y_i(omega) dmu(omega) ||_op <= 2r/d.
Every displayed matrix norm is the real operator norm induced by the Euclidean norm on R^I. The row-vector norm in the truncation condition is the Euclidean norm on E. The integral is the totalized Bochner integral: it is assigned the zero matrix if the integrand is not integrable. No integrability premise or integrability conclusion is part of this assertion.

## Objects

Natural-number dimensions d and q; n := q + 1; real r := n; Euclidean spaces D := R^d and E := R^n; outcome space Omega := Fin n -> D; product Gaussian measure mu; real cutoff L := 2r + 3 log(1000d); real angles theta_i := (i + 1 - 1/2) pi/d; deterministic coordinate functions t_i on Fin n; row vectors x_i(omega) := (omega(b)_i) indexed by b in Fin n; paired matrix index I := Fin n x Fin n; and matrices Y_i(omega) defined by the displayed truncated, scaled Kronecker product. WithLp.toLp 2 and WithLp.ofLp only package and recover the same row coordinates.

## Domains

d,q belong to N. i belongs to Fin d. b,k,a,c,e belong to Fin(q+1), with a,b,c,e used for paired matrix indices. omega belongs to Omega = (Fin(q+1) -> EuclideanSpace R (Fin d)). Each omega(b) is a vector in D and omega(b)_i is real. Each row x_i(omega) belongs to E. theta_i, t_i(k), r and L are real. Each Y_i(omega) and its integral belong to Matrix I I R, a real (q+1)^2 by (q+1)^2 matrix space equipped here with the Euclidean operator norm. mu is the finite product of the specified standard Gaussian probability measures on D, using the product measurable structure.

## Quantifiers

Universally quantify over implicit natural-number parameters d and q, then over a proof hq of 2*q+1 < d. All let-defined objects are within this scope. The conclusion is a conjunction. Its first conjunct is forall i in Fin d, forall omega in Omega, the stated pointwise norm bound. Its second conjunct is forall i in Fin d, the stated norm bound on the integral over omega with respect to mu. The integral binds omega only inside that integral. No existential, almost-everywhere, positive-probability, or high-probability quantifier appears.

## Assumptions

The explicit hypothesis is only 2*q+1 < d for natural numbers d and q. The packet fixes the meanings of Euclidean space, standard Gaussian measure, product measure, matrix products, matrix operator norm, and totalized Bochner integral. These are the approved semantic context. There is no additional integrability, measurability, event, norm, independence, moment, or tail premise. The Gaussian product law is defined, rather than an unspecified distribution subject to further assumptions. The inequalities imply d >= 2 and q+1 >= 1; these are consequences of the stated hypothesis, not added premises. q = 0 is allowed.

## Conclusion

The exact conclusion is the conjunction of (forall i, forall omega, ||Y_i(omega)||_op <= 2*r*L/d) and (forall i, ||integral Y_i dmu||_op <= 2*r/d). Both are non-strict upper bounds. The first applies to every outcome, including cutoff-boundary outcomes. The second is about the norm of the totalized matrix integral. It does not itself assert integrability, and if the integrand were nonintegrable the integral would be the zero matrix by the approved semantics. No bound on a sum, a centered matrix, a square, an integral of a norm, a concentration probability, or any further conclusion is asserted.

## Scopes

The dimension hypothesis precedes and governs every definition and both conjuncts. D, E, Omega, mu, r, L, theta, t, row and Y are local let-definitions, not independently quantified choices. theta and t are deterministic. Y depends on the same dimension pair, cutoff and Gaussian coordinate construction in both conjuncts. Its cutoff uses <=, and the zero branch applies when that relation fails, equivalently when the squared row norm is > L. The first conjunct is genuinely pointwise in omega; there is no exceptional null set. The second universal quantifier over i is outside the integral; omega is integrated out. The conclusion does not equate Y with an untruncated matrix outside the cutoff or supply an expectation formula. Since d > 0 follows from the hypothesis, the displayed inverse of the real embedding of d agrees with ordinary 1/d.

## Constant dependencies

All numerical constants are fixed as written: 1 in q+1 and 2q+1; 2 multiplying q and r and in both upper bounds; 3 multiplying log; 1000 inside log; the half-step 1/2 and pi in theta; and sqrt(2) in the nonzero-frequency coordinates of t. There is no unspecified absolute constant, confidence parameter, or independently variable cutoff. r depends only on q. L depends on d and q. theta_i depends on d and i. t_i(k) depends on d,i,k, with q determining its coordinate domain. D depends on d; E on q; Omega and mu on both dimensions. x_i depends on d,q,i,omega, and Y_i depends on these and on the defined cutoff and t_i. The first upper bound is exactly 2rL/d, and the second is exactly 2r/d; both depend only on d,q. Although L does not appear in the second upper bound, its definition still enters the integrated Y_i.
