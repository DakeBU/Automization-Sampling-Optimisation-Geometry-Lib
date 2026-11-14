# Reconstructed proposition

For every finite-dimensional real inner product space \(E\), equipped with its inner-product norm and Borel \(\sigma\)-algebra, let \(n=\dim_{\mathbb R}E\) and let \(\gamma_E\) be the standard Gaussian probability measure on \(E\). Then the function
\[
f_E:E\longrightarrow\mathbb R,\qquad
f_E(x)=\exp\!\left(\frac{\|x\|^2}{3}\right)
\]
is integrable with respect to \(\gamma_E\), and its real Bochner integral satisfies
\[
\int_E \exp\!\left(\frac{\|x\|^2}{3}\right)\,d\gamma_E(x)
=3^{n/2}.
\]

The dimension \(n\) may be zero. In that case \(\gamma_E=\delta_0\), \(f_E(0)=1\), and both sides of the integral identity equal \(1\).

## Scope and dependencies

- The universal quantifier ranges over \(E\) and the specified structures on \(E\). The hypotheses require a normed additive commutative group, a real inner product space structure, finite real dimension, and a measurable structure equal to the Borel \(\sigma\)-algebra.
- The standard Gaussian is fixed by \(E\). It is the pushforward of \(n\) independent centered real Gaussian coordinates of variance one by an orthonormal basis map into \(E\). Its dimension-zero specialization is unit mass at \(0\).
- The point \(x\) is bound in the function and in the integral, and ranges over all of \(E\). Integrability means almost-everywhere strong measurability and finite integral of \(\lvert f_E\rvert\) with respect to \(\gamma_E\). The integrability assertion and the integral equality are conjuncts of the conclusion.
- The norm is squared before division by the fixed real constant \(3\) inside the exponential. The right-hand side has fixed real base \(3\) and exponent \((n:\mathbb R)/2\), with dimension cast to \(\mathbb R\) before division. Equivalently, it is \(\exp((n/2)\log 3)\).
