# Anonymous theorem reconstruction

For every natural number \(d\) with \(d\ge 2\), every real number \(\kappa\) with \(\kappa\ge 2\), and every natural number \(n\) with \(1\le n<d\), make the following definitions. Index the coordinates by \(i=0,\ldots,d-1\), and set
\[
\theta_i=\frac{(i+\tfrac12)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,\qquad
\Lambda=\operatorname{diag}(\lambda_0,\ldots,\lambda_{d-1}).
\]
Let \(\mu\) be the multivariate Gaussian measure on \(\mathbb R^d\), equipped with its usual Euclidean norm, with mean zero and covariance matrix \(\Lambda^{-1}\). Define the real quadratic function
\[
Q(x)=\sum_{i=0}^{d-1}\cos(n\theta_i)x_i^2.
\]
Then both \(x\mapsto\|x\|_2^2\) and \(Q\) are integrable with respect to \(\mu\), and
\[
\int_{\mathbb R^d}\|x\|_2^2\,d\mu(x)
=\sum_{i=0}^{d-1}\lambda_i^{-1},
\qquad
\int_{\mathbb R^d}Q(x)\,d\mu(x)
=\sum_{i=0}^{d-1}\frac{\cos(n\theta_i)}{\lambda_i}.
\]

## Objects and domains

The parameters are a finite dimension \(d\in\mathbb N\), a real scalar \(\kappa\), and a natural-number mode \(n\). The coordinate index type is exactly \(\operatorname{Fin}(d)\), with values zero through \(d-1\). The angles and diagonal entries are real numbers. The matrix \(\Lambda\) is a real \(d\times d\) diagonal matrix. The integration variable belongs to the real Euclidean space \(\mathbb R^d\). The measure \(\mu\) and the functions appearing in the conclusion are determined by the displayed definitions; they are not additional universally quantified choices.

## Quantifiers and assumptions

The Lean quantifier order is: \(d\), a proof of \(2\le d\), \(\kappa\), a proof of \(2\le\kappa\), \(n\), a proof of \(1\le n\), and a proof of \(n<d\). The braces on \(d\) and \(\kappa\) make those arguments implicit in Lean; they remain universally quantified mathematical parameters. The subsequent `let` bindings are local definitions within all these quantifiers. There are no additional hypotheses of integrability, matrix invertibility, or covariance positivity.

## Integrability and covariance convention

Both integrability assertions are conclusions, conjoined with the two integral identities. `Integrable` means actual real Bochner integrability. In particular, the assertion for the signed function \(Q\) includes finiteness of \(\int |Q|\,d\mu\). The equalities are identities of finite, genuinely integrable expectations, rather than assertions relying only on a totalized integral value.

In the approved definition context, the second argument of `multivariateGaussian` is covariance on its positive semidefinite domain: the Gaussian is the image of the standard Gaussian under the square root of that argument, followed by the mean shift. Here that argument is \(\Lambda^{-1}\), not \(\Lambda\). Thus the coordinate covariance entries are \(\lambda_i^{-1}\) on the diagonal and zero off the diagonal, with no extra factor of two. The mean is zero. Under the displayed parameter assumptions all \(\lambda_i\) are positive (indeed \(1<\lambda_i<\kappa\)), so the totalized inverse and square-root definitions are used in their ordinary nonsingular positive-definite setting.

## Scope and constants

All sums run over every coordinate. The first expectation concerns the squared Euclidean norm; the second concerns exactly the stated cosine-weighted sum of coordinate squares, which need not be nonnegative. The dimension and \(\kappa\) determine \(\theta\), \(\lambda\), \(\Lambda\), and \(\mu\); \(n\) additionally determines \(Q\) and the cosine weights on the second right-hand side. The constants \(1/2\) and \(\pi\) have exactly their displayed values. There are no unspecified constants, asymptotic limits, estimates, or extra ranges of \(n\) in the assertion.

This reconstruction records only the mathematical meaning of the anonymous statement and approved definition context. It does not identify a source or assess source fidelity, compilation, or a proof.
