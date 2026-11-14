For every natural number $d\ge 2$, every real number $\kappa\ge 2$, and every real orthogonal $d\times d$ matrix $O$, use coordinates indexed by $i\in\{0,\ldots,d-1\}$ in the ordinary Euclidean space $E=\mathbb R^d$. Orthogonality means $O^{\mathsf T}O=OO^{\mathsf T}=I_d$; there is no determinant-one restriction.

Define, for each such index,
\[
\theta_i=\frac{(i+\tfrac12)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos(\theta_i).
\]
Let $\Lambda=\operatorname{diag}(\lambda_0,\ldots,\lambda_{d-1})$, let $A=O\Lambda O^{\mathsf T}$, and define the map $R_O:E\to E$ by $R_O(z)=Oz$, using the usual matrix-vector product. The conversions between bundled Euclidean vectors and coordinate functions in the statement only implement this ordinary map.

For a positive semidefinite matrix $S$, write $\gamma_{0,S}$ for the Gaussian probability measure obtained by sending the standard covariance-one Euclidean Gaussian through $x\mapsto\sqrt S\,x$; its mean is the zero vector and its covariance matrix is $S$. The matrices $\Lambda$ and $A$ above are positive definite under the stated hypotheses, so their inverses are positive definite and this meaning applies to both measures below.

Then the pushforward equality of probability measures on $E$ is
\[
(R_O)_\#\gamma_{0,\Lambda^{-1}}=\gamma_{0,A^{-1}}.
\]
In particular, for every Borel set $B\subseteq E$,
\[
\gamma_{0,\Lambda^{-1}}\bigl(\{z\in E:Oz\in B\}\bigr)
=\gamma_{0,A^{-1}}(B).
\]
The map $R_O$ is continuous and linear, hence measurable, so this is the usual measure pushforward. Both $\Lambda^{-1}$ and $A^{-1}$ denote square-matrix inverses, while the fractions in the definitions of $\theta_i$ and $\lambda_i$ are real scalar divisions. All definitions are local to each universally chosen triple $(d,\kappa,O)$; no additional parameters or existential constants occur.
