Let \(d,q\in\mathbb N\) be arbitrary natural numbers satisfying \(2q+1<d\). Use zero-based indices \(i=0,\ldots,d-1\) and \(k=0,\ldots,q\), and define
\[
\theta_i=\frac{(i+\tfrac12)\pi}{d}.
\]
Let \(t\) be the real \(d\times(q+1)\) matrix with entries
\[
t_{ik}=\begin{cases}
1,&k=0,\\
\sqrt{2}\cos(k\theta_i),&k\ne0,
\end{cases}
\]
where \(\sqrt{2}\) is the nonnegative real square root of \(2\). Let \(D\) be the real \(d\times d\) diagonal matrix whose \(i\)-th diagonal entry is
\[
D_{ii}=\cos\bigl((2q+1)\theta_i\bigr).
\]
All off-diagonal entries of \(D\) are zero.

Then all three of the following hold:

1. \(t^{\mathsf T}t=dI_{q+1}\).
2. \(t^{\mathsf T}Dt=0_{(q+1)\times(q+1)}\).
3. For every \(i=0,\ldots,d-1\),
   \[
   \sum_{k=0}^{q}t_{ik}^{\,2}\le 2(q+1).
   \]

Here transposition and matrix multiplication are over the reals, \(I_{q+1}\) is the identity matrix, and the sum in the third conclusion is the squared Euclidean norm of row \(i\). The definitions of \(\theta,t,D\) apply throughout all three conclusions. The only hypothesis on \(d,q\) is the displayed strict inequality, in addition to their being natural numbers; there are no existentially chosen constants. The bound is exactly \(2(q+1)\).
