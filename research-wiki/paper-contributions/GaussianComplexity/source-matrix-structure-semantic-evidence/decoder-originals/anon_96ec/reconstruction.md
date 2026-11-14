For every pair of natural numbers d and q and every hypothesis hq that
2q + 1 < d, make the following local choices and definitions. The variables d
and q are implicit parameters in the displayed Lean universal quantifier. In
particular q may be zero; equivalently, the stated natural-number bound is
d >= 2q + 2, so every allowed d is positive.

Give the real matrix space with both its row and column index set equal to
Fin(q + 1) x Fin(q + 1) the Borel sigma algebra of its ordinary finite
coordinate topology. The matrix norm convention is the operator norm of the
matrix acting between the corresponding real Euclidean spaces; this norm
preserves that topology.

Let D = R^d and E = R^(q + 1), each with its Euclidean norm and Borel sigma
algebra. Let Omega = (Fin(q + 1) -> D). Equip Omega with the finite product
sigma algebra and the measure

    mu = product over b in Fin(q + 1) of stdGaussian(D),

where stdGaussian(D) is the centered Gaussian probability measure on D with
identity covariance. Thus an element omega of Omega assigns a vector
omega(b) in D to each b in Fin(q + 1).

Define the real numbers

    r = q + 1,
    L = 2r + 3 log(1000d),

where the natural numbers are embedded in R and log is the natural
logarithm. For each i in Fin d, whose natural-number value is denoted i,
put

    theta_i = (i + 1 - 1/2) pi / d = (i + 1/2) pi / d.

Define the coordinate function t_i : Fin(q + 1) -> R by

    t_i(k) = 1                         if the value of k is 0,
             sqrt(2) cos(k theta_i)    otherwise.

Here k in the second line is the real embedding of its natural-number
value, and sqrt is the nonnegative square root. For each i in Fin d and
each omega in Omega, define the Euclidean vector row_i(omega) in E by

    row_i(omega)_b = omega(b)_i,    b in Fin(q + 1).

This is the Euclidean-space wrapping WithLp.toLp 2 of the displayed
coordinate function; WithLp.ofLp recovers these same coordinates.

Write M for the real matrices whose row and column indices both range over
Fin(q + 1) x Fin(q + 1). For each i in Fin d define Y_i : Omega -> M by

    Y_i(omega) = (1/d) [row_i(omega) row_i(omega)^T]
                            tensor [t_i t_i^T]
                    if ||row_i(omega)||_2^2 <= L,
                 0  otherwise.

The tensor here is the matrix Kronecker product: at row (a,b) and column
(c,e), its entry before multiplication by 1/d is
row_i(omega)_a row_i(omega)_c t_i(b) t_i(e). Each outer product uses the
coordinate functions, as in Matrix.vecMulVec. The cutoff includes equality,
and the zero in the other branch is the zero matrix in M.

For every i in Fin d, define

    mean_i = integral over Omega of Y_i(omega) dmu(omega),
    Z_i(omega) = Y_i(omega) - mean_i,
    w_i = cos((2q + 1) theta_i),
    X_i(omega) = w_i Z_i(omega).

The number 2q + 1 in the definition of w_i is formed as a natural number
and then embedded in R. All displayed matrix integrals are Bochner
integrals in M with the matrix norm convention above. The integral notation
is totalized to zero for nonintegrable functions; the definitions alone do
not add an asserted integrability hypothesis or conclusion for Y_i.

Then all five of the following assertions hold together:

1. For every i in Fin d, X_i is measurable from Omega with its displayed
   product sigma algebra to M with the locally fixed Borel sigma algebra.
2. The entire indexed family (X_i)_(i in Fin d) is jointly independent under
   mu (the assertion iIndepFun X mu).
3. For every i in Fin d, X_i is Bochner integrable with respect to mu. This
   includes almost-everywhere strong measurability and a finite integral of
   its matrix norm.
4. For every i in Fin d,

       integral over Omega of X_i(omega) dmu(omega) = 0 in M.

5. For every i in Fin d and every omega in Omega, X_i(omega) is Hermitian.
   Since the entries are real, this means exactly that X_i(omega) equals
   its transpose. This last quantifier is over every omega, rather than
   only mu-almost every omega.

For q = 0, Fin(q + 1) has its single coordinate k = 0, so the piecewise
definition of t_i uses only its value 1. This case is included whenever
d >= 2; no separate assertion is made for parameters outside 2q + 1 < d.

Ambiguity: none remains given the supplied approved definition context.
