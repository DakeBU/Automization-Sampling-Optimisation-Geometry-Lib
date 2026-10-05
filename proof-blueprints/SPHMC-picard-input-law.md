# SPHMC first Picard innovation law

Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Algorithm 3.1 and the
proof of Lemma D.4.

## Mathematical edge

For an incoming phase-state law `nu`, adjoin independently

\[
Z_0\sim N(0,I_d),\qquad (G_j^{[0]})_{j\in[J]}\sim
\bigotimes_{j\in[J]}N(0,I_d).
\]

Set

\[
P_0=e^{-h/2}P_{\rm init}+\sqrt{1-e^{-h}}Z_0.
\]

The resulting finite product probability law makes `X`, `P0`, and every
coordinate `G j` measurable.  The refreshed state is square-integrable with
budget

\[
B_{\rm refresh}=M+(1-e^{-h})d,
\]

and every Picard innovation satisfies

\[
\mathbb E\|G_j^{[0]}\|^2=d.
\]

## Lean route

1. Reuse `partial_momentum_refresh_second_moment` for the first product.
2. Use `Measure.pi` for the finite independent Gaussian array.
3. Lift refreshed-state integrability through the outer product.
4. Use `integrable_comp_eval` and `integral_comp_eval` for each coordinate.
5. Feed all outputs directly to `picard_center_gradient_moment` in the focused
   integration test.

## Strict boundary

No repeated phase history, run-wide state bound, second Gaussian array,
second refresh, Chebyshev--Lobatto construction, numerical (D.7), total cost
(D.8), or main theorem is asserted.  The incoming state moment remains a
premise; its transport-based derivation is the next separate edge.
