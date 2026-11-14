# Anonymous mathematical reconstruction

For every natural number \(d\ge 2\), every real number \(\kappa\ge 2\), and every natural number \(n\) satisfying \(1\le n<d\), make the following definitions. Coordinates are indexed by \(i\in\{0,1,\ldots,d-1\}\), and all sums below run over precisely that index set.

Define
\[
\theta_i=\frac{(i+\tfrac12)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,
\qquad
\Lambda=\operatorname{diag}(\lambda_0,\ldots,\lambda_{d-1}).
\]
Let \(\mu\) be the centered multivariate Gaussian measure on the usual real Euclidean space \(\mathbb R^d\) with covariance matrix \(\Lambda^{-1}\). In terms of the supplied definition, this is the image of the standard Gaussian under
\[
z\longmapsto (\Lambda^{-1})^{1/2}z.
\]
The supplied matrix square root is the functional-calculus square root on the positive semidefinite domain and is zero outside that domain. Matrix and scalar inverses use their standard totalized conventions.

For \(x=(x_0,\ldots,x_{d-1})\in\mathbb R^d\), set
\[
S(x)=\|x\|^2=\sum_{i=0}^{d-1}x_i^2,
\qquad
Q(x)=\sum_{i=0}^{d-1}\cos(n\theta_i)x_i^2,
\qquad
M=\int_{\mathbb R^d}S(x)\,d\mu(x).
\]
The norm here is the usual Euclidean norm, and the displayed integral is the real Bochner integral.

Then all of the following statements hold simultaneously:

1. \(S\in L^2(\mu)\), including almost-everywhere strong measurability.
2. \(Q\in L^2(\mu)\), including almost-everywhere strong measurability.
3. \(\displaystyle \operatorname{Var}_{\mu}(S)=2\sum_{i=0}^{d-1}\frac{1}{\lambda_i^2}\).
4. \(\displaystyle \operatorname{Var}_{\mu}(Q)=2\sum_{i=0}^{d-1}\frac{\cos^2(n\theta_i)}{\lambda_i^2}\).
5. \(\operatorname{Var}_{\mu}(S)\le 2M\).
6. \(\operatorname{Var}_{\mu}(Q)\le 2M\).
7. \(\displaystyle 2M\le \frac{2d}{\sqrt{\kappa}}\).

Here \(\operatorname{Var}_{\mu}(f)\) has the supplied precise convention: take the extended nonnegative integral of the squared norm of \(f-\int f\,d\mu\), then apply \(\mathrm{ENNReal.toReal}\), which sends infinity to zero. The two explicit \(L^2\) assertions are part of the conclusion and establish finite variance for the observables at issue.

The quantifiers cover every admissible triple \((d,\kappa,n)\); there are no existential parameters or additional hypotheses. The definitions are local to each such triple, and every displayed assertion uses those same definitions and the same measure. The angles depend on \(d\); the eigenvalues, matrix, measure, and \(M\) depend on \((d,\kappa)\); \(S\) depends on its dimension; and \(Q\) depends on \((d,n)\). The sole numerical factor in the variance formulas and bounds is the explicit constant \(2\), independent of all parameters. No assertion about an original source's identity, wording, or correspondence is made.
