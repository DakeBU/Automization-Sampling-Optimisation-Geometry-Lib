# SPHMC stationary phase-reference moments

## Source boundary

Chen–Chewi–Lu–Zhang, *Smoothed Picard Hamiltonian Monte Carlo*,
arXiv:2609.06906v1, Section 3.1 defines

\[
\pi_\eta=\pi*\mathsf N(0,\eta I),\qquad
\Pi_\eta=\pi_\eta\otimes\mathsf N(0,I).
\]

In the proof of Lemma D.4, after equation (D.3), the position and momentum
second moments of this reference law are used to control the realized phase
history. The paper suppresses the elementary product/convolution calculation.

## Frozen packet

For any probability law `mu` with finite second moment about `xstar`, and any
real Gaussian scale `sigma`, prove

\[
\int\|y-x_\star\|^2\,d(\mu*\mathsf N(0,\sigma^2I))(y)
=\int\|x-x_\star\|^2\,d\mu(x)+\sigma^2d.
\]

Then form the actual phase reference

\[
\Pi_\sigma=(\mu*\mathsf N(0,\sigma^2I))\otimes\mathsf N(0,I)
\]

and prove that it is a probability law, both coordinate squares are
integrable, their integrals are the position identity above and `d`, and

\[
\int(\|x-x_\star\|^2+\|p\|^2)\,d\Pi_\sigma
\le M+(\sigma^2+1)d
\]

whenever the original position moment is at most `M`.

## Proof architecture

1. Realize Gaussian smoothing as the pushforward of
   `mu.prod (stdGaussian E)` under `(x,z) ↦ x + sigma • z`.
2. Expand the square around `xstar`.
3. Prove the cross term integrable from the two `L²` moments and show its
   integral is zero using the centered Gaussian first moment.
4. Use the compiled standard-Gaussian identity `E‖Z‖²=d`.
5. Integrate each coordinate over the product phase law and add the bounds.

## Strict remainder

This packet does not prove that Hamiltonian flow or the numerical kernel
preserves `Pi_eta`; it does not prove contraction, (D.3), the repeated history
bound, (D.7), (D.8), or either main theorem. To match the paper variance
parameter, later consumers instantiate `sigma = sqrt eta` with `eta ≥ 0`.
