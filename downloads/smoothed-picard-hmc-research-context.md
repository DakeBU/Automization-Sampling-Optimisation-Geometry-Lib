# Smoothed Picard HMC and the proxy warm start — ASTIS research workspace

Workspace id: `ASTIS-SW-SPHMC-2026`

Producer: low-accuracy transport control, then an implementable proxy warm start.

## Evidence boundary

- Source context is pinned by the companion metadata.
- AI explanations and generated Lean are unverified candidates.
- Lean compilation checks only the exact submitted snippet.
- Source fidelity and blue status require independent ASTIS review and admission.

## Primary source

- Smoothed Picard Hamiltonian Monte Carlo (2609.06906v1): https://arxiv.org/html/2609.06906v1
- Authors: Fan Chen, Sinho Chewi, Jianfeng Lu, Matthew S. Zhang

## Low-accuracy W2 guarantee

Source: SPHMC Theorem 1.1; Algorithm 3.2; Section 4.5; Appendix D

Given a reference point with small gradient, the source algorithm outputs a probability law satisfying the displayed normalized Wasserstein error. This theorem counts gradient and proximal queries; gradient-only implementation is a separate reduction.

```latex
\sqrt\alpha W_2(\widehat\pi,\pi)\le\varepsilon,\qquad \mathbb E Q_{\nabla,\mathrm{prox}}=O\!\left[\left(\kappa^2+\kappa^{7/6}d^{1/6}\varepsilon^{-1/3}\right)\log^4\frac{e\kappa d}{\varepsilon}\right]
```

Assumptions:

- The common C2 strong-convexity/smoothness setting.
- 0 < epsilon <= 1; a supplied x_ref satisfies ||grad V(x_ref)|| <= sqrt(alpha d).
- Use the source algorithm and its parameter choices, not an arbitrary Picard or HMC discretization.

Proof route:

### 1. Smooth the density

Source: Section 3.1, (3.1)–(3.2); Section 4.1

```latex
e^{-V_\eta}=e^{-V}*\mathcal N(0,\eta I),\qquad \nabla V_\eta(y)=\mathbb E[\nabla V(X)\mid X+\sqrt\eta G=y]
```

This is not the Gaussian average of V. Differentiation under the integral and a specified conditional-law version justify the score identity. The implementable score estimator has bias as well as variance; it is not assumed exactly unbiased.

Lean status: `open`.

### 2. Integrate the smoothed Hamiltonian equation

Source: Sections 3.2, 4.2–4.4; Appendix B

```latex
X_t=X_0+tP_0-\int_0^t(t-s)\nabla V_\eta(X_s)\,ds
```

Picard iteration approximates the trajectory, while Chebyshev–Lobatto quadrature approximates its integrals. Smoothing regularity, quadrature remainder and stochastic score error are separate inputs to the local-error estimate.

Lean status: `open`.

### 3. Budget all three errors

Source: Section 4.5; Appendix C.3

```latex
W_2(\widehat\pi,\pi)\le W_2(\widehat\pi,\pi_\eta)+W_2(\pi_\eta,\pi)
```

The first term includes iteration and numerical errors; the second is the smoothing bias. Finite second moments and the exact-kernel contraction must be supplied before using this triangle inequality.

Lean status: `open`.

Strict boundary:

No Wq, Renyi warmness, exact stationarity of a discretization, or cost-free proximal oracle follows from this W2 statement.

## An implementable law near a Renyi-warm proxy

Source: SPHMC Theorem 1.2; Theorem 7.1(ii); Sections 5–6

For every allowed delta the algorithm produces the actual law below. A second, existential comparison law is close in TV and has bounded order-2 Renyi divergence. The comparison law need not be directly sampled.

```latex
\exists\widehat\pi_\delta^\dagger:\quad \operatorname{TV}(\widehat\pi_\delta,\widehat\pi_\delta^\dagger)\le\delta,\quad R_2(\widehat\pi_\delta^\dagger\Vert\pi)\le1,\qquad \mathbb E Q_\nabla=O\!\left(\kappa^{7/6}d^{1/6}\log^9\frac{e\kappa d}{\delta}\right)
```

Assumptions:

- The common setting and the same reference-point bound as Theorem 1.1.
- 0 < delta < 1/2.
- The recursive generator uses higher-moment smoothed sampling and terminal RGO implementation; this is not a general W2-to-Renyi implication.

Proof route:

### 1. Turn a moment bound into a nearby bounded-displacement coupling

Source: Lemma 6.2

```latex
W_p(P,Q)\le r\quad\Longrightarrow\quad\exists P^\dagger:\ \operatorname{TV}(P,P^\dagger)\le\delta,\quad W_\infty(P^\dagger,Q)\le r\delta^{-1/p}
```

For p >= 2 and finite p-moments, replace a coupled sample by its partner on the event where displacement exceeds r delta^(-1/p). Markov's inequality bounds that event; measurability and coupling attainment must be justified.

Lean status: `open`.

### 2. Regularize both laws before measuring divergence

Source: Lemma 6.3(ii); Theorems 6.1 and 6.5

```latex
R_q(P^\dagger*\gamma_\tau\Vert Q*\gamma_\tau)\le\frac{qW_p(P,Q)^2}{2\tau\delta^{2/p}},\qquad q>1,\quad\tau>0
```

A Gaussian reverse-transport bound applies after convolution. Recursive conditional/RGO updates then recover the desired unsmoothed target; deleting that recursion would change the theorem.

Lean status: `open`.

### 3. Track the moving conditional target and oracle bill

Source: Lemma 6.4; Sections 6.3–6.4 and 7.1

```latex
(A^+)^{-1}=A^{-1}+a^{-1},\qquad u^+=A^+(u/A+y/a)
```

Completing the square closes the RGO family under another RGO. The recursive stages and outer proximal sampler improve conditioning; the kappa-squared setup term from Theorem 1.1 is not silently discarded.

Lean status: `open`.

Strict boundary:

Only the proxy has the displayed Renyi certificate. Genuine Renyi warmness of the actual output requires the stronger W_psi2 input in the separate source theorem.

## Suggested agent instruction

Use the pinned source statement and explicit assumptions above. Work on one selected proof step at a time. Separate ASTIS-owned compiled declarations from Mathlib or external facts. Treat every generated explanation and Lean fragment as unverified until the exact snippet compiles and an independent source-fidelity review accepts the correspondence. Never infer whole-paper completion from a reusable support lemma.
