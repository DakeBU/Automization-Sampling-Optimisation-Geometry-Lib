# SPHMC first partial momentum refresh

Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Algorithm 3.1
lines 282--300 and the use of the run-wide state estimate in Lemma D.4,
lines 2177--2180.

## Frozen edge

Let `nu` be the incoming law of `(X,P_init)` and adjoin a fresh
`Z ~ stdGaussian E` by the product law. For `h >= 0`, set

\[
  P_0=e^{-h/2}P_{\rm init}+\sqrt{1-e^{-h}}Z.
\]

Prove measurability and combined-square integrability, then the exact identity

\[
\mathbb E(\|X-x_*\|^2+\|P_0\|^2)
=\mathbb E(\|X-x_*\|^2+e^{-h}\|P_{\rm init}\|^2)
 +(1-e^{-h})\dim E.
\]

Consequently an incoming bound `M` yields the explicit refreshed budget
`M + (1-exp(-h))*dim E`. The old `M` is not silently reused.

## Reuse

The shared parent
`StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian` packages
Mathlib's standard-Gaussian L2/covariance APIs and finite Parseval. This avoids
a third route-private copy of the same Gaussian norm-square argument.

## Proof route

1. Extract position- and momentum-square integrability from the nonnegative
   combined incoming energy.
2. Upgrade the incoming momentum to L1 and use the shared Gaussian L2/L1 facts.
3. Prove integrability of the product-space mixed inner product.
4. Use Fubini and the actual zero Gaussian mean to make the mixed expectation
   vanish; no centering of `P_init` is assumed.
5. Expand the Hilbert norm, use `a^2=exp(-h)` and
   `sigma^2=1-exp(-h)`, and integrate term by term.
6. Apply `exp(-h)<=1` to obtain the consumer budget.

## Actual consumer

`Tests.SmoothedPicardHMCPartialMomentumRefresh` supplies the refreshed product
law and corrected budget to
`PicardCenterMoment.picard_center_gradient_moment`. This is a typed composition
test, not a claim that the full history or D.7 has been constructed.

## Strict boundary

The repeated Algorithm 3.1 kernel/history, the D.3 plus Lemma 4.16 run-wide
state estimate, initialization, the second refresh, the joint Picard Gaussian
array, Chebyshev--Lobatto node/weight instantiation, absorption into
`C*kappa*d*L_q^18`, D.8 and Theorem 5.1 remain red and independent.
