For every pair \(d,q\in\mathbb N=\{0,1,2,\ldots\}\) satisfying
\[
2q+1<d,
\]
make the following definitions, all of which remain in scope for the entire subsequent proposition. Write
\[
I=\{0,\ldots,d-1\},\qquad J=\{0,\ldots,q\},
\]
with the zero-based indices shown, and set
\[
D=\mathbb R^I,\qquad E=\mathbb R^J,\qquad
\Omega=\{\omega:J\to D\}.
\]
The spaces \(D\) and \(E\) have their Euclidean norms and Borel structures. Let \(\gamma_D\) be the centered Gaussian probability measure on \(D\) with identity covariance, and define the finite product measure
\[
\mu=\bigotimes_{b\in J}\gamma_D
\quad\text{on }\Omega.
\]
Define the real scalars
\[
r=q+1,\qquad L=2r+3\log(1000d),
\]
where the natural numbers in these real expressions are embedded into \(\mathbb R\), and \(\log\) is the natural logarithm. For \(i\in I\) and \(k\in J\), put
\[
\theta_i=\frac{(i+1-\tfrac12)\pi}{d},
\qquad
t_i(k)=
\begin{cases}
1,&k=0,\\
\sqrt{2}\cos(k\theta_i),&k\ne0.
\end{cases}
\]
Here \(\sqrt{2}\) is the nonnegative real square root. For \(i\in I\) and \(\omega\in\Omega\), let
\[
u_i(\omega)=\bigl(\omega(b)(i)\bigr)_{b\in J}\in E,
\qquad
\|u_i(\omega)\|_2^2=\sum_{b\in J}\omega(b)(i)^2.
\]
Let \(\operatorname{Mat}_{J\times J}(\mathbb R)\) denote the real square matrices whose rows and columns are indexed by the ordered pairs in \(J\times J\). Define
\[
Y_i(\omega)=
\begin{cases}
d^{-1}\bigl(u_i(\omega)u_i(\omega)^{\mathsf T}\bigr)
\otimes\bigl(t_i t_i^{\mathsf T}\bigr),
&\|u_i(\omega)\|_2^2\le L,\\
0,&\|u_i(\omega)\|_2^2>L,
\end{cases}
\]
as an element of \(\operatorname{Mat}_{J\times J}(\mathbb R)\). The equality case belongs to the first branch. The outer products use the displayed real coordinates. In the Kronecker product, the row pair is \((b,k)\) and the column pair is \((c,\ell)\); consequently its entry in the first branch is exactly
\[
\bigl(Y_i(\omega)\bigr)_{(b,k),(c,\ell)}
=d^{-1}\,\omega(b)(i)\,\omega(c)(i)\,t_i(k)\,t_i(\ell)
\qquad (b,k,c,\ell\in J).
\]
Next define, for every \(i\in I\),
\[
\operatorname{mean}_i=\int_{\Omega}Y_i(\omega)\,d\mu(\omega),
\qquad
Z_i(\omega)=Y_i(\omega)-\operatorname{mean}_i,
\]
and put
\[
\rho=\frac{2r(L+1)}{d},
\qquad
X_i(\omega)=\rho^{-1}Z_i(\omega).
\]
All scalar inverses and divisions use the real-field convention in which the inverse of zero is zero.

Then, for every real \(s\) satisfying \(0<s\), and then for every \(i\in I\),
\[
\exp\!\left((e^s-s-1)
       \int_{\Omega}X_i(\omega)X_i(\omega)\,d\mu(\omega)\right)
-
\int_{\Omega}\exp\!\bigl(sX_i(\omega)\bigr)\,d\mu(\omega)
\succeq0.
\]

All displayed integrals are Bochner integrals in the indicated finite real matrix space, taken with respect to exactly \(\mu\), with no conditioning; by their definition an integral is zero when its integrand is not integrable. No integrability premise or conclusion is added to this proposition. Matrix products are ordinary matrix products, and scalar multiples are real scalar multiples. For \(M\in\operatorname{Mat}_{J\times J}(\mathbb R)\), the relation \(M\succeq0\) means \(M^{\mathsf T}=M\) and \(v^{\mathsf T}Mv\ge0\) for every \(v\in\mathbb R^{J\times J}\). The matrix exponential is the convergent algebra power series
\[
\exp(M)=\sum_{n=0}^{\infty}\frac{M^n}{n!},
\qquad M^0=I_{J\times J},
\]
using the Euclidean \(L^2\) operator norm and ordinary finite-coordinate topology, while \(e^s\) is the scalar real exponential. The allowed boundary cases are exactly those specified by \(d,q\in\mathbb N\) and \(2q+1<d\); in particular \(q=0\) is allowed, while these conditions make \(I\) and \(J\) nonempty.
