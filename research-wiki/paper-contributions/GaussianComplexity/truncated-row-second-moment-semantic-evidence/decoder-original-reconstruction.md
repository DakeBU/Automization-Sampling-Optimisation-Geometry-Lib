# Independent reconstruction from the supplied Lean statement

For every pair of natural numbers \(d,q\in\mathbb N\) such that
\[
2q+1<d,
\]
put \(n=q+1\) and let \(r=n\), regarded as a real number. Thus \(n\geq1\), so division by \(r\) is well defined. Let
\[
E=\mathbb R^{n},\qquad \mu=N(0,I_n)
\]
be Euclidean space with its Euclidean norm and Borel measurable structure, equipped with the centered standard Gaussian probability measure whose orthonormal coordinates are independent with variance one. Define
\[
R(x)=\|x\|_2^2=\sum_{i=0}^{q}x_i^2,
\qquad
L=2r+3\log(1000d),
\qquad
A=\{x\in E:R(x)\leq L\},
\]
where \(d\) is cast to a real number inside the logarithm and \(\log\) is the natural logarithm. The stated hypothesis implies \(d\geq2q+2>0\), so its logarithm argument is positive. Define the real scalar
\[
a=\frac1r\int_E \mathbf1_A(x)R(x)\,d\mu(x).
\]
For each \(x\in E\), form the \(n\times n\) real matrices
\[
G(x)=xx^{\mathsf T},\qquad
K(x)=\mathbf1_A(x)G(x).
\]
Their row and column indices are \(i,j\in\{0,\ldots,q\}\), and explicitly
\[
G(x)_{ij}=x_i x_j,\qquad
K(x)_{ij}=
\begin{cases}
x_i x_j,&\|x\|_2^2\leq L,\\
0,&\|x\|_2^2>L.
\end{cases}
\]

The theorem asserts both of the following:

1. The matrix-valued function \(K\) is integrable with respect to \(\mu\): it is almost everywhere strongly measurable and
   \[
   \int_E\|K(x)\|_{\mathrm{op}}\,d\mu(x)<\infty,
   \]
   where \(\|\cdot\|_{\mathrm{op}}\) is the Euclidean \(L^2\) operator norm on these finite matrices.
2. Its matrix Bochner integral is the scalar multiple of the identity
   \[
   \boxed{\displaystyle
   \int_E \mathbf1_{\{\|x\|_2^2\leq L\}}(x)\,xx^{\mathsf T}\,d\mu(x)
   =\left(\frac1{q+1}\int_E
      \mathbf1_{\{\|x\|_2^2\leq L\}}(x)\,\|x\|_2^2\,d\mu(x)\right)I_{q+1}.}
   \]
   Equivalently, for every \(i,j\in\{0,\ldots,q\}\),
   \[
   \int_E\mathbf1_A(x)x_i x_j\,d\mu(x)
   =\begin{cases}a,&i=j,\\0,&i\ne j.\end{cases}
   \]

Every integral is taken with respect to the original Gaussian measure over all of \(E\). The indicator sets the integrand to zero outside \(A\); it includes points with \(R(x)=L\). The scalar normalization is division by the real dimension \(r=q+1\), and there is no division by \(\mu(A)\). The real scalar integral is a real Bochner integral, and the matrix integral is a Bochner integral in the finite-dimensional real matrix space. The identity matrix has diagonal entries one and off-diagonal entries zero; scalar multiplication multiplies all entries.

The only quantified parameters are \(d\) and \(q\), and the only additional assumption is \(2q+1<d\). All displayed objects \(E,\mu,r,R,L,a,G,K,A,n\) are determined by those parameters and the definitions above. In particular, \(d\) enters through the numerical hypothesis and the cutoff \(L\); the coordinate dimension is \(q+1\). The assertions of integrability and the integral identity hold for every such pair of parameters, with no further assumptions.
