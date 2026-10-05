# Implemented two-layer Picard phase kernel

Pinned source: Chen, Chewi, Lu and Zhang, arXiv:2609.06906v1,
Algorithm 3.1 steps 1--4 (HTML lines 282--306), Appendix D.1 (D.1),
Algorithm D.2 and Lemma D.3 (HTML lines 2138--2164).
Primary source rechecked 2026-10-05.

One sole writer: root-samplinglib-writer. Freeze the normalized C2 Hessian
bounds, 0 < eta <= c < 1 and eps > 0. Retain the actual residual-stopped
gradient program from ApproximateProximalExecution, including its final query.

For supplied finite deterministic nodes t and weights omega, positionWeight
and momentumWeight, construct the independent law

\[
\gamma=(\gamma_E\otimes\gamma_E)\otimes
  (\gamma_E^{\otimes\iota}\otimes\gamma_E^{\otimes\iota}).
\]

Its coordinates are zeta0, zeta1, G0 and G1. Construct both Picard layers,
the final position/momentum and the second OU half-refresh exactly in source
order, replacing exact prox by the parent's measurable actual stopped q.
Prove every intermediate jointly measurable, then define

\[
K(s,\cdot)=\gamma\circ\Phi(s,\cdot)^{-1}.
\]

Use Mathlib Kernel.id, Kernel.const, product and map; no new kernel axioms.
The phase parameter satisfies h >= 0, proving a nonnegative refresh variance;
the positive source schedule remains a consumer obligation. The finite supplied
coefficients are not certified Chebyshev--Lobatto coefficients.

Actual consumer: future iterated Algorithm 3.1 history law and D.4 realized
center/cost law. Focused test must use positive dimension and both Gaussian
arrays; it must retain the interpreter certificate and kernel output law.
Quadrature construction, repeated-law moments, contraction, invariant law,
Wp/proxy warmness, complete D.7/D.8 and both main theorems remain separate.

Proof route: (1) obtain actual stopped program, (2) gradient measurability,
(3) measurable first refresh/centers, (4) measurable first and second arrays,
(5) measurable final refresh, (6) canonical product Markov kernel, (7) exact
Gaussian pushforward law. After repeated same-shape errors diagnose the API
or statement; never weaken the algorithm to close the proof.
