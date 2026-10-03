# Proximal BPS: high accuracy from a warm start — ASTIS research workspace

Workspace id: `ASTIS-SW-PBPS-2026`

Consumer: a Renyi-warm input becomes a high-accuracy position law through an augmented-state discrete chain.

## Evidence boundary

- Source context is pinned by the companion metadata.
- AI explanations and generated Lean are unverified candidates.
- Lean compilation checks only the exact submitted snippet.
- Source fidelity and blue status require independent ASTIS review and admission.

## Primary source

- Accelerated High-Accuracy Sampling from a Warm Start via the Proximal Bouncy Particle Sampler (2609.06905v1): https://arxiv.org/html/2609.06905v1
- Authors: Fan Chen, Sinho Chewi, Jianfeng Lu, Matthew S. Zhang

## Optimized expected gradient complexity

Source: PBPS Corollary 4.4, (4.19)–(4.20); Theorem 4.3, (4.8)–(4.9)

With universal positive tuning constants, run the implementable algorithm with the source parameter choices. Its output is epsilon-close to the target in TV and has the following expected gradient-query bound. No fixed worst-case running-time claim is made.

```latex
\begin{gathered}L=\Delta+\log\frac{K_{\rm opt}d\kappa}{\varepsilon},\quad\eta=\frac{c_{\rm opt}}{\beta(\sqrt{dL}+L)},\quad\operatorname{TV}(\mathcal L(\widehat X),\pi)\le\varepsilon,\\\mathbb E Q_\nabla\le K_{\rm opt}\sqrt\kappa(d+L)^{1/4}L^{3/4}\left(\Delta+\log\frac4\varepsilon\right)\log(\kappa L).\end{gathered}
```

Assumptions:

- The common setting; an input probability law mu_0 with R_2(mu_0||pi) <= Delta, where Delta >= 1.
- 0 < epsilon < 1/4; query access to grad V and a sample from mu_0.
- Choose L and eta below and the iteration, resampling, error and solver budgets in source (4.8)–(4.9). The constants c_opt and K_opt are universal, not arbitrary user choices.

Proof route:

### 1. Augment, then reflect the auxiliary variable

Source: Proposition 2.1; (3.11); Proposition 3.4

```latex
\pi_\eta(dx,dy)=\pi(dx)\mathcal N(x,\eta I)(dy),\qquad (x,y)\mapsto(x,2x-y)
```

Gaussian symmetry preserves the augmented law under this reflection. It differs from velocity reflection at a bounce. A conditional half-turn and occasional RGO resampling form the ideal transition; they are not independent ordinary Gibbs redraws at every step.

Lean status: `open`.

### 2. Use discrete hypocoercivity, not a reversible gap shortcut

Source: Theorem 3.5; Appendices B–C

```latex
f=\mathbb E[f\mid Y]+(f-\mathbb E[f\mid Y]),\qquad\chi^2(\nu_0\mathcal K^{JN}\Vert\pi_\eta)\le e^{-J}\chi^2(\nu_0\Vert\pi_\eta)
```

The source chooses eta, rho and a block length N as in Theorem 3.5. Conditional resampling damps the fluctuation; reflection couples it to the conditional mean. A modified L2 energy and half-turn operator bounds are essential. The local unrefreshed process alone need not mix.

Lean status: `open`.

### 3. Keep implementation mismatch separate from ideal mixing

Source: Theorem 4.3, (4.14)–(4.18)

```latex
\mathbb P(\widehat X\ne X_T^{\rm id})\le3Ta=\varepsilon/2,\qquad\operatorname{TV}(\mathcal L(\widehat X),\pi)\le\varepsilon/2+\varepsilon/2
```

Solver failure, approximate RGO draws and capped bounce rates each consume an error budget a. Lifted Renyi control bounds bad events along the ideal chain; a coupling union bound transfers its convergence to the implemented output.

Lean status: `open`.

### 4. Balance localization against block length

Source: Corollary 4.4, (4.21)–(4.23)

```latex
(\alpha\eta)^{-1/2}=\sqrt{\kappa/c_{\rm opt}}(\sqrt{dL}+L)^{1/2}
```

Substitute the chosen eta into the iteration bound and charge proximal solves, RGO calls and candidate bounce queries. Retaining L prevents a hidden warmness or precision dependence from disappearing into the dimension exponent.

Lean status: `open`.

Strict boundary:

This is the discrete augmented Proximal BPS algorithm with curved conditional flights. It is not vanilla continuous-time BPS, and its acceleration does not follow just from invariance or an algebraic reflection identity.

## Suggested agent instruction

Use the pinned source statement and explicit assumptions above. Work on one selected proof step at a time. Separate ASTIS-owned compiled declarations from Mathlib or external facts. Treat every generated explanation and Lean fragment as unverified until the exact snippet compiles and an independent source-fidelity review accepts the correspondence. Never infer whole-paper completion from a reusable support lemma.
