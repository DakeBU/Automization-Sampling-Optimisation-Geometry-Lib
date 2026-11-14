For every natural number \(d\) satisfying \(2\le d\), every real number \(\kappa\) satisfying \(2\le\kappa\), every real orthogonal \(d\times d\) matrix \(O\), and every natural number \(n\), including zero, make the following local definitions. There is no determinant-one condition on \(O\), and there is no further bound on \(n\).

For each \(i\in\{0,\ldots,d-1\}\), put
\[
\theta_i=\left(i+\frac12\right)\frac{\pi}{d}.
\]
Define real \(d\times d\) matrices
\[
A=O\,\operatorname{diag}\!\left(\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i\right)_{i=0}^{d-1}O^{\mathsf T},
\qquad
B=\frac{1}{\kappa-1}\left(2A-(\kappa+1)I_d\right).
\]
Then
\[
T_n(B)=O\,\operatorname{diag}\!\left(\cos(n\theta_i)\right)_{i=0}^{d-1}O^{\mathsf T}.
\]
Here \(T_n\) is the real Chebyshev polynomial of the first kind at the integer index obtained by casting the natural number \(n\); on natural indices it satisfies \(T_0=1\), \(T_1=X\), and \(T_{m+2}=2XT_{m+1}-T_m\). The expression \(T_n(B)\) is polynomial evaluation in the real matrix algebra: each real coefficient is mapped to that coefficient times \(I_d\), and polynomial multiplication uses matrix multiplication. The conclusion is an equality of real matrices, not an entrywise application of the scalar polynomial. The factor \(1/(\kappa-1)\) is a real scalar reciprocal. All fractions, \(\pi\), and cosine have their usual real meanings; the occurrences of \(d\), \(i\), and \(n\) in real expressions use the standard real casts.
