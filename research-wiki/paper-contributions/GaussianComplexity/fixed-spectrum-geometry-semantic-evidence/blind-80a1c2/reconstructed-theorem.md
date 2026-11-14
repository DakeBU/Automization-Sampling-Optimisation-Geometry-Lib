# Reconstructed mathematical proposition

For every natural number \(d\) with \(d\ge 2\), every real number \(\kappa\) with \(\kappa\ge 2\), and every real orthogonal \(d\times d\) matrix \(O\), use the index set \(I=\{0,1,\ldots,d-1\}\) and define
\[
\theta_i=\frac{(i+\tfrac12)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos(\theta_i)
\quad(i\in I),
\]
\[
A=O\,\operatorname{diag}(\lambda_i)_{i\in I}\,O^{\mathsf T},
\qquad
f:\mathbb R^d\longrightarrow\mathbb R,\qquad
f(x)=\frac{x^{\mathsf T}Ax}{2}.
\]
Here \(\mathbb R^d\) has its standard real Euclidean inner product and norm, and orthogonality means \(O^{\mathsf T}O=OO^{\mathsf T}=I_d\), with either determinant sign allowed. All of the following conclusions hold together for these definitions:

1. The function \(f\) is globally \(C^\infty\): it has continuous derivatives of every finite order.
2. At every \(x\in\mathbb R^d\), the gradient map \(\nabla f:\mathbb R^d\to\mathbb R^d\) has a genuine real Fréchet derivative equal to the linear map represented by \(A\). Explicitly, for every such \(x\),
   \[
   D(\nabla f)(x)[h]=Ah\qquad\text{for every }h\in\mathbb R^d.
   \]
3. The function \(f\) is strongly convex on all of \(\mathbb R^d\) with modulus \(1\). Explicitly, for every \(x,y\in\mathbb R^d\) and every \(a,b\in\mathbb R\) satisfying \(a\ge0\), \(b\ge0\), and \(a+b=1\),
   \[
   f(ax+by)\le a f(x)+b f(y)-\frac{ab}{2}\lVert x-y\rVert^2.
   \]
4. The gradient is globally Lipschitz with the stated bound \(\kappa\): for every \(x,y\in\mathbb R^d\),
   \[
   \lVert\nabla f(x)-\nabla f(y)\rVert\le\kappa\lVert x-y\rVert.
   \]
5. \(f(0)=0\).
6. For every \(x\in\mathbb R^d\),
   \[
   \bigl(\text{for every }y\in\mathbb R^d,\ f(x)\le f(y)\bigr)
   \quad\Longleftrightarrow\quad x=0.
   \]
   Thus the global minimum is attained uniquely at the zero vector, and its value is zero.

The formulas for \(\theta_i\), \(\lambda_i\), \(A\), and \(f\) are definitions inside the universal quantifiers, not additional hypotheses. The gradient uses the real Euclidean Riesz identification of the Fréchet derivative with a vector. Although the formal gradient operator is totalized, conclusion 1 supplies differentiability of \(f\), and conclusion 2 asserts actual derivative existence for the gradient at every point; a default value at a nondifferentiable point is not being used as evidence of differentiability. Smoothness here means every finite derivative order, without an analyticity assertion. The constants \(1\) and \(\kappa\) are the stated bounds; no assertion of their sharpness is included.
