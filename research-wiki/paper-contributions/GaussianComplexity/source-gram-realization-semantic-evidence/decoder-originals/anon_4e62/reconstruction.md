For every pair of natural numbers \(d,q\) and every hypothesis
\[
2q+1<d,
\]
make the following local definitions. All finite indices below are zero based: \(i\in\operatorname{Fin}(d)\) has values \(0,\ldots,d-1\), and \(b,c,k,\ell\in\operatorname{Fin}(q+1)\) have values \(0,\ldots,q\). Natural numbers occurring in real expressions are embedded in \(\mathbb R\).

Let
\[
D=\mathbb R^d,\qquad E=\mathbb R^{q+1},\qquad
\Omega=\{\omega:\operatorname{Fin}(q+1)\to D\},
\]
where \(D\) and \(E\) are Euclidean spaces, and let the measure on \(\Omega\) be
\[
\mu=\bigotimes_{b\in\operatorname{Fin}(q+1)}\operatorname{stdGaussian}(D).
\]
Here \(\operatorname{stdGaussian}\) is the centered Gaussian probability law with identity covariance. Define the real numbers
\[
r=(q+1)\in\mathbb R,\qquad
L=2r+3\log(1000d),
\]
where \(\log\) denotes the natural logarithm. For \(i\in\operatorname{Fin}(d)\), define
\[
\theta_i=\frac{(i+1-\tfrac12)\pi}{d},\qquad
t_{i,k}=\begin{cases}
1,&k=0,\\
\sqrt2\cos(k\theta_i),&k\ne0,
\end{cases}
\quad k\in\operatorname{Fin}(q+1).
\]
For \(i\in\operatorname{Fin}(d)\) and \(\omega\in\Omega\), let
\[
\operatorname{row}_i(\omega)=(\omega_b(i))_{b\in\operatorname{Fin}(q+1)}\in E.
\]
The norm of this row, and of every vector of \(E\) below, is its Euclidean norm.

Let \(I=\operatorname{Fin}(q+1)\times\operatorname{Fin}(q+1)\). Define an \(I\)-by-\(I\) real matrix \(Y_i(\omega)\) by
\[
Y_i(\omega)=
\begin{cases}
d^{-1}\bigl(\operatorname{row}_i(\omega)\operatorname{row}_i(\omega)^{\mathsf T}\bigr)
\otimes(t_i t_i^{\mathsf T}),&\|\operatorname{row}_i(\omega)\|^2\le L,\\
0,&\text{otherwise}.
\end{cases}
\]
The index order in this Kronecker product is the following: for row index \((b,k)\in I\) and column index \((c,\ell)\in I\),
\[
\bigl(Y_i(\omega)\bigr)_{(b,k),(c,\ell)}=
\begin{cases}
d^{-1}\omega_b(i)\omega_c(i)t_{i,k}t_{i,\ell},&\|\operatorname{row}_i(\omega)\|^2\le L,\\
0,&\text{otherwise}.
\end{cases}
\]
Set
\[
\operatorname{mean}_i=\int_\Omega Y_i(\omega)\,d\mu(\omega),\qquad
Z_i(\omega)=Y_i(\omega)-\operatorname{mean}_i.
\]
Define the real number
\[
a=\frac1r\int_E
\mathbf 1_{\{y\in E:\|y\|^2\le L\}}(x)\,\|x\|^2\,
 d\operatorname{stdGaussian}(E)(x),
\]
where the integrand is \(\|x\|^2\) on the displayed set and zero off that set. All displayed integrals are Bochner integrals in the displayed spaces, with value zero when their integrands are not integrable.

Define
\[
w_i=\cos\bigl((2q+1)\theta_i\bigr),
\]
where \(2q+1\) is first formed as a natural number and then embedded in \(\mathbb R\). For each \(\omega\in\Omega\), define the real matrix \(B(\omega)\), with row index in \(\operatorname{Fin}(d)\) and column index in \(I\), by
\[
B(\omega)_{i,(b,k)}=(\sqrt d)^{-1}\,
\bigl(\operatorname{row}_i(\omega)\bigr)_b\,t_{i,k}.
\]
Here each square root is the nonnegative square root. Finally define the condition
\[
G(\omega)\quad\Longleftrightarrow\quad
\forall i\in\operatorname{Fin}(d),\quad
\|\operatorname{row}_i(\omega)\|^2\le L.
\]

Then, for every \(\omega\in\Omega\), the condition \(G(\omega)\) implies the conjunction of the following two equalities of \(I\)-by-\(I\) real matrices:
\[
\sum_{i\in\operatorname{Fin}(d)}Z_i(\omega)
=B(\omega)^{\mathsf T}B(\omega)-a\,\mathrm{Id}_I
\]
and
\[
\sum_{i\in\operatorname{Fin}(d)}w_i Z_i(\omega)
=B(\omega)^{\mathsf T}\operatorname{diag}(w)B(\omega).
\]
Here \(\mathrm{Id}_I\) is the identity matrix on the ordered-pair index set \(I\), and \(\operatorname{diag}(w)\) is the \(\operatorname{Fin}(d)\)-by-\(\operatorname{Fin}(d)\) diagonal matrix with entries \(w_i\). Matrix products, finite sums, scalar multiplication, and subtraction have their ordinary real matrix meanings. Both equalities lie within the implication from \(G(\omega)\).
