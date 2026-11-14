# Reconstructed statement

For every pair of natural numbers \(d,q\), and every hypothesis \(h_q:2q+1<d\), make the following local definitions. All indices below are zero-based: \(\operatorname{Fin}(n)=\{0,\ldots,n-1\}\).

Let
\[
D=\operatorname{EuclideanSpace}_{\mathbb R}(\operatorname{Fin}(d)),\qquad
E=\operatorname{EuclideanSpace}_{\mathbb R}(\operatorname{Fin}(q+1)),\qquad
\Omega=\operatorname{Fin}(q+1)\to D.
\]
Thus \(D\) and \(E\) are real Euclidean spaces of dimensions \(d\) and \(q+1\), respectively. Write \(\gamma_D=\mathrm{stdGaussian}(D)\) and \(\gamma_E=\mathrm{stdGaussian}(E)\) for the centered Gaussian probability measures with identity covariance on those spaces. Define the measure on \(\Omega\) by
\[
\mu=\bigotimes_{b\in\operatorname{Fin}(q+1)}\gamma_D.
\]
Let the real numbers \(r,L\) be
\[
r=(q+1)\in\mathbb R,\qquad L=2r+3\log(1000d),
\]
where the natural numbers in real expressions are embedded into \(\mathbb R\), and \(\log\) is the natural logarithm. For \(i\in\operatorname{Fin}(d)\), define
\[
\theta_i=\frac{(i+1-\tfrac12)\pi}{d}.
\]
Define \(t:\operatorname{Fin}(d)\to\operatorname{Fin}(q+1)\to\mathbb R\) by
\[
t_{i,k}=\begin{cases}
1,&k=0,\\
\sqrt{2}\cos(k\theta_i),&k\ne0.
\end{cases}
\]
For each \(i\in\operatorname{Fin}(d)\) and \(\omega\in\Omega\), let
\[
\operatorname{row}_i(\omega)
=\bigl(\omega(b)_i\bigr)_{b\in\operatorname{Fin}(q+1)}\in E.
\]
This is precisely the Euclidean vector obtained by applying \(\mathrm{WithLp.toLp}\,2\) to the displayed coordinate function; \(\mathrm{WithLp.ofLp}\) recovers those same coordinates.

Define \(Y_i(\omega)\) to be a real square matrix with both its row and column index sets equal to
\(\operatorname{Fin}(q+1)\times\operatorname{Fin}(q+1)\), hence with dimension \((q+1)^2\) by \((q+1)^2\), as follows:
\[
Y_i(\omega)=
\begin{cases}
 d^{-1}\bigl[\operatorname{row}_i(\omega)\operatorname{row}_i(\omega)^{\mathsf T}\bigr]
 \otimes\bigl[t_i t_i^{\mathsf T}\bigr],
 &\|\operatorname{row}_i(\omega)\|_2^2\le L,\\
 0,&\|\operatorname{row}_i(\omega)\|_2^2>L.
\end{cases}
\]
Here the first outer product uses the coordinates recovered by \(\mathrm{WithLp.ofLp}\), the second uses the coordinate function \(t_i\), and \(\otimes\) is the matrix Kronecker product in this order. Explicitly, at row \((b,k)\) and column \((c,\ell)\), the entry in the first branch is
\[
 d^{-1}\,\omega(b)_i\,\omega(c)_i\,t_{i,k}\,t_{i,\ell}.
\]
The cutoff includes equality. Let
\[
\operatorname{mean}_i=\int_{\Omega}Y_i(\omega)\,d\mu(\omega),\qquad
Z_i(\omega)=Y_i(\omega)-\operatorname{mean}_i,
\]
with both matrices having that same pair index set. Define the real number
\[
a=\frac{1}{r}\int_E
 \mathbf 1_{\{y\in E:\|y\|_2^2\le L\}}(x)\,\|x\|_2^2\,d\gamma_E(x).
\]
The indicator is zero outside the displayed set and includes its boundary. Define \(w:\operatorname{Fin}(d)\to\mathbb R\) by
\[
w_i=\cos\bigl((2q+1)\theta_i\bigr).
\]
For each \(\omega\in\Omega\), define the real matrix \(B(\omega)\), with row index set \(\operatorname{Fin}(d)\) and column index set \(\operatorname{Fin}(q+1)\times\operatorname{Fin}(q+1)\), by
\[
 B(\omega)_{i,(b,k)}=(\sqrt d)^{-1}\,
 \bigl(\operatorname{row}_i(\omega)\bigr)_b\,t_{i,k}.
\]
Square roots are nonnegative square roots. Define the condition
\[
G(\omega)\quad\Longleftrightarrow\quad
 \text{for every }i\in\operatorname{Fin}(d),\quad
 \|\operatorname{row}_i(\omega)\|_2^2\le L.
\]

Then, for every real number \(\Delta\) and every \(\omega\in\Omega\), if \(G(\omega)\) holds, the following implication holds:
\[
\left(
 \left\|\sum_{i\in\operatorname{Fin}(d)}Z_i(\omega)\right\|_{\mathrm{op}}\le\Delta
 \quad\text{and}\quad
 \left\|\sum_{i\in\operatorname{Fin}(d)}w_i Z_i(\omega)\right\|_{\mathrm{op}}\le\Delta
\right)
\quad\Longrightarrow\quad
\left(
 \left\|B(\omega)^{\mathsf T}B(\omega)-I\right\|_{\mathrm{op}}
 \le\Delta+(1-a)
 \quad\text{and}\quad
 \left\|B(\omega)^{\mathsf T}\operatorname{diag}(w)B(\omega)\right\|_{\mathrm{op}}
 \le\Delta
\right).
\]
In the conclusion, \(I\) is the identity matrix on
\(\operatorname{Fin}(q+1)\times\operatorname{Fin}(q+1)\), and \(\operatorname{diag}(w)\) is the \(d\)-by-\(d\) matrix whose diagonal entries are \(w_i\) and whose other entries are zero. Matrix products are ordinary matrix products; \(w_i Z_i(\omega)\) is real scalar multiplication. Every matrix norm displayed is the operator norm for the action between the corresponding Euclidean coordinate spaces. Every row-vector norm is the Euclidean norm.

Both integrals are Bochner integrals in their displayed spaces and are interpreted as zero if the integrand is not integrable; no integrability hypothesis or conclusion is imposed. The two norm inequalities in the antecedent must hold together, and the two norm inequalities in the conclusion are both under the hypotheses \(G(\omega)\) and that conjunction. No nonnegativity assumption is placed on \(\Delta\). The natural-number case \(q=0\) is included whenever \(1<d\).
