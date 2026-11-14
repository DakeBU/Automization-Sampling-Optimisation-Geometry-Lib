For every \(d,q\in\mathbb N\), every \(\kappa\in\mathbb R\) with \(\kappa\ge 2\) and \(2q+1<d\), and every real Euclidean coordinate array
\[
x\in\mathbb R^{I\times A},\qquad I=\{0,\ldots,d-1\},\qquad A=\{0,\ldots,q\},
\]
make the following definitions. Regard \(x_{i,a}\) as its unchanged real coordinate at the ordered pair \((i,a)\), and put
\[
\theta_i=\frac{(i+\tfrac12)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,\qquad
\Lambda=\operatorname{diag}(\lambda_i)_{i\in I},\qquad
g_a(i)=x_{i,a}.
\]
Define a real \(d\)-by-\((q+1)\) matrix \(t\), and a real \(d\)-by-\((q+1)^2\) matrix \(B\) whose column indices are ordered pairs in \(A\times A\), by
\[
t_{i,k}=
\begin{cases}
1,&k=0,\\
\sqrt{2}\cos(k\theta_i),&1\le k\le q,
\end{cases}
\qquad
B_{i,(a,k)}=\frac{1}{\sqrt d}\,g_a(i)t_{i,k}.
\]
Here square roots are the nonnegative real roots. Define the subspace
\[
K=\operatorname{span}_{\mathbb R}
\left\{\Lambda^k g_a:\ a\in A,\ k\in A\right\}
\subseteq\mathbb R^I,
\]
where \(\Lambda^k\) is the ordinary matrix power and its product with \(g_a\) is ordinary matrix-vector multiplication; in particular \(\Lambda^0\) is the identity. Then the actual image of \(B\) equals this entire subspace:
\[
\left\{Bc:\ c\in\mathbb R^{A\times A}\right\}=K.
\]
Explicitly, \(c\) ranges over all real coefficient arrays indexed by \((a,k)\), and \((Bc)_i=\sum_{(a,k)\in A\times A}B_{i,(a,k)}c_{a,k}\). Thus the left side is the set of all linear combinations of the columns of \(B\); it is not merely the set of those columns. The right side is the real linear span of the displayed vectors, not merely their set of values.

The assumptions imply \(d\ge 2q+2\ge 2\), so the denominator \(\sqrt d\) is positive. The case \(q=0\) is included: \(A=\{0\}\), \(t_{i,0}=1\), the only column of \(B\) is \(g_0/\sqrt d\), and \(K=\operatorname{span}_{\mathbb R}\{g_0\}\). If every coordinate of \(x\) is zero, both sets are \(\{0\}\); zero vectors or linear dependence among the \(g_a\) are also allowed. The case \(\kappa=2\) and the smallest admissible dimension \(d=2q+2\) are included. Neither \(d=0\) nor \(d=1\) is admissible. The first and last angular nodes are \(\theta_0=\pi/(2d)\) and \(\theta_{d-1}=\pi-\pi/(2d)\); the angles \(0\) and \(\pi\) are not sampled. No distribution, independence, nonzero-coordinate, rank, or invertibility assumption is placed on \(x\), the \(g_a\), or \(B\).
