# Complete anonymous theorem reconstruction

This reconstruction is unabridged. Its only mathematical and evidentiary input is the supplied anonymous JSON packet, specifically its anonymous Lean statement and approved definition context. No source text, source identity, declaration identity, audit identity, proof, repository instructions, or other file was consulted. The packet exposes `compiled: true`; this is supplied metadata, not independently verified compilation evidence.

## The theorem, with every defined object

For every pair of natural numbers \(d,q\), where natural numbers include zero, assume the strict inequality
\[
2q+1<d.
\]
There is no additional hypothesis. In particular, \(q=0\) is allowed; the stated inequality implies \(d\ge 2q+2\ge2\). Write \(I=\{0,1,\ldots,q\}=\operatorname{Fin}(q+1)\), \(J=\{0,1,\ldots,d-1\}=\operatorname{Fin}d\), and \(m=q+1\) as auxiliary notation for the finite index sets and their size. Each occurrence of an index inside a real-valued expression means its natural-number value embedded into \(\mathbb R\).

Let \(D=\mathbb R^d\), more precisely \(\operatorname{EuclideanSpace}\,\mathbb R\,(\operatorname{Fin}d)\), with its Euclidean norm and Borel measurable structure. Let \(E=\mathbb R^{q+1}\), more precisely \(\operatorname{EuclideanSpace}\,\mathbb R\,(\operatorname{Fin}(q+1))\), with the same conventions. Let
\[
\Omega=I\to D,
\qquad
\mu=\bigotimes_{b\in I}\operatorname{stdGaussian}(D),
\]
with the product measurable structure. Thus a sample \(\omega\) consists of \(q+1\) vectors \(\omega_b\in\mathbb R^d\); under the probability measure \(\mu\), these vectors are independent centered Gaussian vectors with identity covariance. Equivalently, the real coordinates \(\omega_b(i)\), for \(b\in I\) and \(i\in J\), are independent standard normal variables.

Let the real scalar \(r\) be the real embedding of the natural number \(q+1\), and let
\[
r=q+1,\qquad L=2r+3\log(1000d).
\]
Here \(\log\) is the natural logarithm and \(d\) is embedded into \(\mathbb R\) in the scalar expression. For each \(i\in J\), let
\[
\theta_i=\frac{(i+1-\tfrac12)\pi}{d}
          =\frac{(i+\tfrac12)\pi}{d}.
\]
Let \(t_i:I\to\mathbb R\) be the deterministic coordinate function
\[
t_i(k)=
\begin{cases}
1,&k=0,\\
\sqrt2\cos(k\theta_i),&k\ne0.
\end{cases}
\]
The second branch therefore runs over \(k=1,\ldots,q\), and is empty when \(q=0\). The square root is the nonnegative real square root. For each \(i\in J\), let the random Euclidean vector \(\operatorname{row}_i:\Omega\to E\) have coordinates
\[
\bigl(\operatorname{row}_i(\omega)\bigr)_b=\omega_b(i)
\quad(b\in I).
\]
This is exactly the coordinate function wrapped by `WithLp.toLp 2`; recovering coordinates by `WithLp.ofLp` leaves these coordinates unchanged. In particular,
\[
\|\operatorname{row}_i(\omega)\|_2^2
=\sum_{b\in I}\omega_b(i)^2.
\]

All matrices below are real square matrices with both row and column index set \(I\times I\); their size is \((q+1)^2\) by \((q+1)^2\). Define the random matrix \(Y_i\), for each \(i\in J\), by
\[
Y_i(\omega)=
\begin{cases}
\displaystyle\frac1d\,
\bigl(\operatorname{row}_i(\omega)\operatorname{row}_i(\omega)^{\mathsf T}\bigr)
\otimes\bigl(t_i t_i^{\mathsf T}\bigr),
&\|\operatorname{row}_i(\omega)\|_2^2\le L,\\[2mm]
0,&\|\operatorname{row}_i(\omega)\|_2^2>L.
\end{cases}
\]
The products inside the two factors denote outer products of their coordinate functions. The Kronecker product has the order displayed: the row-vector outer product is the first factor, and the \(t_i\) outer product is the second. The scalar \(1/d\) multiplies the whole Kronecker matrix. The zero in the second branch is the zero matrix. The cutoff includes its equality endpoint: a sample with squared row norm exactly \(L\) uses the first branch. Explicitly, for \(b,k,c,\ell\in I\),
\[
\bigl(Y_i(\omega)\bigr)_{(b,k),(c,\ell)}=
\begin{cases}
\displaystyle\frac1d\,\omega_b(i)\omega_c(i)\,t_i(k)t_i(\ell),
&\displaystyle\sum_{a\in I}\omega_a(i)^2\le L,\\[2mm]
0,&\displaystyle\sum_{a\in I}\omega_a(i)^2>L.
\end{cases}
\]

For each \(i\in J\), let the deterministic matrix \(\operatorname{mean}_i\) be its exact expectation under the just-defined product Gaussian law, and let \(Z_i\) be the variable centered by that expectation:
\[
\operatorname{mean}_i=\int_\Omega Y_i(\omega)\,d\mu(\omega),
\qquad
Z_i(\omega)=Y_i(\omega)-\operatorname{mean}_i.
\]
The mean is this integral over the entire sample space, not a free matrix, a conditional expectation on the cutoff event, or an untruncated outer-product mean. The cutoff event has already been incorporated into \(Y_i\). The finite-dimensional, measurable truncated matrix variable \(Y_i\) is bounded for each fixed \(d,q,i\), so its Bochner integral is its ordinary finite expectation. No separately displayed integrability assertion for \(Y_i\) is an additional conjunct of the supplied statement.

Finally, define the deterministic real weights and the real scalar bound
\[
w_i=\cos\bigl((2q+1)\theta_i\bigr)
\quad(i\in J),
\qquad
C=\frac{2r(r+2)}d
 =\frac{2(q+1)(q+3)}d.
\]
The frequency is exactly \(2q+1\). The scalars \(r,L,\theta_i,t_i,w_i,C\) are fixed by the definitions, not existential choices.

## The four asserted outputs

With all the preceding definitions in scope, the theorem asserts the conjunction of the following four claims:

1. For every \(i\in J\), the matrix-valued function
   \[
   \omega\longmapsto Z_i(\omega)Z_i(\omega)
   \]
   is Bochner integrable with respect to \(\mu\).

2. For every \(i\in J\), the matrix-valued function
   \[
   \omega\longmapsto
   \bigl(w_i Z_i(\omega)\bigr)\bigl(w_i Z_i(\omega)\bigr)
   \]
   is Bochner integrable with respect to \(\mu\). Here each \(w_i Z_i(\omega)\) is scalar multiplication of the entire matrix by the fixed real number \(w_i\).

3. The operator norm of the sum of the unweighted second-moment matrices satisfies
   \[
   \left\|\sum_{i\in J}
      \int_\Omega Z_i(\omega)Z_i(\omega)\,d\mu(\omega)
   \right\|_{\mathrm{op}}
   \le \frac{2r(r+2)}d.
   \]

4. The operator norm of the sum of the weighted second-moment matrices satisfies the same bound:
   \[
   \left\|\sum_{i\in J}
      \int_\Omega
      \bigl(w_i Z_i(\omega)\bigr)\bigl(w_i Z_i(\omega)\bigr)
      \,d\mu(\omega)
   \right\|_{\mathrm{op}}
   \le \frac{2r(r+2)}d.
   \]

Each product \(Z_i(\omega)Z_i(\omega)\) is the ordinary matrix square. In coordinates, its \(((b,k),(c,\ell))\) entry is
\[
\sum_{(a,h)\in I\times I}
  \bigl(Z_i(\omega)\bigr)_{(b,k),(a,h)}
  \bigl(Z_i(\omega)\bigr)_{(a,h),(c,\ell)}.
\]
It is not entrywise squaring. The weighted integrand is exactly \(w_i^2 Z_i(\omega)^2\) by ordinary scalar multiplication and matrix multiplication. This is an elementary equivalent way to write the displayed weighted product, with no change to its integrability assertion or to its norm bound.

The norm is the complete Euclidean operator norm of a matrix acting on \(\mathbb R^{I\times I}\) with its Euclidean norm:
\[
\|A\|_{\mathrm{op}}
=\sup_{\|x\|_2=1}\|Ax\|_2.
\]
All matrix integrals are Bochner integrals in this finite-dimensional matrix space with that norm; their entries are the integrals of the corresponding real entries. The integrability outputs mean almost-everywhere strong measurability together with finiteness of the extended integral of the matrix norm. They apply separately to every \(i\) and to each of the two displayed square-valued functions. The approved context defines a nonintegrable Bochner integral to be zero; the theorem's explicit integrability outputs establish that these second-moment integrals have their usual expectation meaning. Thus the last two assertions can equivalently be written
\[
\left\|\sum_{i=0}^{d-1}\mathbb E_\mu[Z_i^2]\right\|_{\mathrm{op}}\le C,
\qquad
\left\|\sum_{i=0}^{d-1}\mathbb E_\mu[w_i^2Z_i^2]\right\|_{\mathrm{op}}\le C.
\]
The sum is inside each norm. Both conclusions concern sums of actual matrix expectations, not a sum of norms or a bound asserted pointwise in \(\omega\). The only universally quantified parameters of the theorem are the natural numbers \(d,q\) satisfying \(2q+1<d\); each per-index integrability assertion quantifies over all \(i\in\operatorname{Fin}d\). All four conclusions hold together for the same defined objects.

## Seven semantic slots

**objects.** The natural parameters are \(d,q\) with the strict inequality witness \(2q+1<d\). The defined carriers are \(D=\mathbb R^d\), \(E=\mathbb R^{q+1}\), and \(\Omega=\operatorname{Fin}(q+1)\to D\). The defined law is the product of \(q+1\) standard Gaussian laws on \(D\). The real scalar \(r=q+1\), cutoff \(L=2r+3\log(1000d)\), angles \(\theta_i=(i+1/2)\pi/d\), coordinate functions \(t_i(0)=1\) and \(t_i(k)=\sqrt2\cos(k\theta_i)\) for nonzero \(k\), and vectors \(\operatorname{row}_i(\omega)_b=\omega_b(i)\) specify the random matrix \(Y_i\). This matrix is \(d^{-1}(\operatorname{row}_i\operatorname{row}_i^{\mathsf T})\otimes(t_it_i^{\mathsf T})\) on the inclusive cutoff and zero outside it. Its expectation defines \(\operatorname{mean}_i\), and \(Z_i=Y_i-\operatorname{mean}_i\). The remaining objects are \(w_i=\cos((2q+1)\theta_i)\) and \(C=2r(r+2)/d\). The complete explicit definitions and matrix entries appear above.

**domains.** The parameters \(d,q\) are natural numbers including zero; all stated scalar formulas take values in \(\mathbb R\). Spatial indices \(i\) range over \(\operatorname{Fin}d\), and vector indices \(b,k,c,\ell\) range over \(\operatorname{Fin}(q+1)\). The sample space has the finite product Borel structure and probability law \(\mu\) specified above. Each \(Y_i,Z_i\) is a function from \(\Omega\) to real matrices indexed on both sides by \(\operatorname{Fin}(q+1)\times\operatorname{Fin}(q+1)\). Each \(\operatorname{mean}_i\) is in that same matrix space. Integrals are Bochner integrals there, and norms are induced Euclidean operator norms, not entrywise norms.

**quantifiers.** For all natural \(d,q\) satisfying \(2q+1<d\), define the entire displayed collection of carriers, law, scalars, coordinate functions, vectors, and matrices; then assert the conjunction of two universal integrability statements and two scalar norm inequalities. Each integrability statement separately quantifies over every \(i\in\operatorname{Fin}d\). The norm statements sum over every such \(i\) and integrate over all \(\omega\in\Omega\) with respect to the single law \(\mu\). The variables \(\omega\) and matrix-coordinate indices are bound in the corresponding functions, integrals, and coordinate descriptions. There is no existential constant, random sample hypothesis, or additional external parameter.

**assumptions.** The only mathematical hypothesis beyond the types of \(d,q\) is the strict integer inequality \(2q+1<d\). In particular \(d\) is positive and \(q=0\) remains permitted. The Gaussian law, cutoff, weights, centering, and constant are definitions rather than extra assumptions or arbitrary inputs. Integrability of each of the two square-valued matrix functions is asserted as an output, not assumed. Equality at the truncation threshold belongs to the nonzero formula branch.

**conclusion.** For every spatial index, the ordinary matrix square of \(Z_i\) and the ordinary matrix square of its scalar multiple \(w_i Z_i\) are Bochner integrable. The operator norm of the finite sum of the expectations of the first squares is at most \(C=2(q+1)(q+3)/d\), and the operator norm of the finite sum of the expectations of the weighted squares is also at most the same \(C\). Each \(Z_i\) is centered by the actual expectation of the already truncated matrix \(Y_i\). In the weighted conclusion the scalar is squared inside the expectation: \((w_i Z_i)^2=w_i^2Z_i^2\). Both bounds are on the norm after summing the expected matrices.

**scopes.** All let-defined objects and all four conjuncts are inside the universal scope of the same \(d,q\) and the hypothesis \(2q+1<d\). The per-index quantifier of the first integrability conjunct applies to its unweighted integrand only, and the independent per-index quantifier of the second applies to its weighted integrand only. The matrix expectation defining \(\operatorname{mean}_i\) is over the full product law with \(i\) fixed. Each subsequent second-moment expectation fixes \(i\) before the outer finite sum. The cutoff comparison applies to \(\|\operatorname{row}_i(\omega)\|_2^2\) before forming \(Y_i\), and centering is performed after that truncation. The weights are deterministic and do not depend on \(\omega\). The norm encloses the complete finite sum of integrals in each of the last two conjuncts.

**constant_dependencies.** The real \(r\) is fixed as \(q+1\); the bound is fixed exactly as \(C=2r(r+2)/d=2(q+1)(q+3)/d\), with no unspecified multiplicative constant or additional dependency. The cutoff is fixed as \(L=2(q+1)+3\log(1000d)\), with exactly the coefficients \(2,3,1000\). The scalar normalization of \(Y_i\) is exactly \(d^{-1}\). The angles depend on \(d,i\), the coordinate functions on \(d,i,k\), and the weights on \(d,q,i\), with frequency exactly \(2q+1\). The same \(C\) applies to both norm bounds; there is no confidence level, tolerance, exceptional event, or unspecified distribution parameter.
