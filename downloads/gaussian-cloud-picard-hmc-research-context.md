# Picard HMC Part I: Gaussian cloud correction — ASTIS research workspace

Workspace id: `ASTIS-SW-GAUSSIAN-CLOUD-2026`

Recursive implementation route: turn Gaussian-cloud Picard updates into a finite sampler while keeping every adaptive call, cap event and replacement error auditable.

## Evidence boundary

- Source context is pinned by the companion metadata.
- AI explanations and generated Lean are unverified candidates.
- Lean compilation checks only the exact submitted snippet.
- Source fidelity and blue status require independent ASTIS review and admission.

## Primary source

- High-accuracy simulation of Picard HMC, part I: Gaussian cloud correction (2609.38710v1): https://arxiv.org/html/2609.38710v1
- Authors: Fan Chen, Sinho Chewi, Jianfeng Lu, Matthew S. Zhang

## Main high-accuracy sampling guarantee

Source: Theorem 1.1; equations (1.1)–(1.2)

For the paper's sampler and parameter choices, a one-smooth target satisfying the displayed logarithmic Sobolev inequality can be sampled to total-variation error epsilon with the stated expected number of gradient queries, without a warm-start assumption.

```latex
\mathsf{TV}(\widehat\pi,\pi)\le\varepsilon,\qquad \mathbb E Q_{\nabla}=O\!\left(\kappa\{d+\log(\kappa d/\varepsilon)\}^{1/5}\log^{13/2}(\kappa d/\varepsilon)\right)
```

Assumptions:

- d >= 1; V is C2 on R^d and grad V is 1-Lipschitz; pi is the normalized law proportional to exp(-V).
- pi satisfies KL(mu||pi) <= (kappa/2) times the relative Fisher information for every probability measure mu with smooth density, with kappa >= 1.
- A supplied reference point x_ref satisfies ||grad V(x_ref)|| <= sqrt(d/kappa).
- 0 < epsilon <= 1/4; use the source Gaussian-cloud sampler, proximal wrapper and exact parameter schedule rather than an arbitrary Picard discretization.

Proof route:

### 1. Represent dependent Picard evaluations by Gaussian clouds

Source: Sections 3.1 and 4–5

```latex
X_i^{[k]}=\bar X_i^{[k]}+\sqrt{\eta}\,G_i^{[k]}
```

The cloud representation exposes independent Gaussian blocks while preserving the shared dependence needed by Picard iteration. Fluctuation and mean corrections are separate FORS gadgets; independence may not be invented between recursively shared blocks.

Lean status: `open`.

### 2. Assemble a finite adaptive computation

Source: Section 6.1; Lemmas 6.1–6.2

```latex
A_{v+1}=A_v-1+\zeta_{v+1},\qquad T=\inf\{v:A_v=0\}
```

Mandatory predecessor chains are contracted into vertices and optional nested requests become children. Lemmas 6.1 and 6.2 control vertices and attached RGO queries before the deterministic global cap is imposed.

Lean status: `open`.

### 3. Telescope every implementation error

Source: Lemma 6.3

```latex
\mathsf{TV}(\operatorname{Law}(\widehat X),\operatorname{Law}(X))\le\sum_{t=1}^{T_{\max}}\delta_t+\varepsilon_{\rm cap}
```

Dummy filling converts early termination into a common fixed slot space. Hybrids replace one conditional kernel at a time under the ideal history; the cap failure is added only after comparing capped and uncapped ideal algorithms.

Lean status: `open`.

### 4. Insert the Section 6 budgets into the cloud sampler

Source: Theorem 6.4; proof of Theorem 1.1

```latex
\mathbb E Q_{\nabla}\le C\mathfrak L^{11/2}(d+\mathfrak L)^{1/5}
```

Theorem 6.4 fixes h, smoothing levels, Picard depth, phase count, local correction budgets and RGO accuracies. The proximal wrapper then restores general condition number kappa and produces Theorem 1.1.

Lean status: `open`.

Strict boundary:

No local Lean theorem yet proves the sampler, the adaptive forest, or the complexity bound. The big-O hides only universal constants specified by the source parameter choices; it is not a license to omit kappa, dimension, precision, cap or initialization dependencies.

## Size and query count of a capped adaptive tree

Source: Section 6.1, Lemma 6.1, equations (6.1)–(6.2)

A breadth-first request queue with conditionally sub-Poisson child counts and mean offspring at most one quarter has expected total size at most four thirds of its root count and a subexponential upper tail. A deterministic local query cap multiplies the vertex bound.

```latex
\mathbb ET\le\frac{4q}{3},\qquad \mathbb P\{T>C(q+mu)\}\le e^{-u}\ (u\ge1),\qquad Q_{\rm ref}\le Q_{\rm loc}T
```

Assumptions:

- q >= 1 roots; A_0=q and, while A_v>0, A_{v+1}=A_v-1+zeta_{v+1} with zeta_{v+1} a nonnegative integer adapted to the exploration filtration.
- Deterministic m >= 1 and lambda >= 0 satisfy E[exp(s zeta_{v+1}) | F_v] <= exp(lambda(exp(ms)-1)) on {A_v>0}, for every 0 <= s <= 1/m.
- m lambda <= 1/4; T is the first v with A_v=0. The local reference-query count per processed vertex is at most Q_loc.

Proof route:

### 1. Differentiate the conditional MGF at zero

Source: Lemma 6.1 proof, expectation estimate

```latex
\mathbb E[\zeta_{v+1}\mid\mathcal F_v]\le m\lambda\le\tfrac14
```

This supplies negative queue drift while the process is alive. Lean must state the conditional-expectation version and the stopped extension after the queue empties.

Lean status: `open`.

### 2. Sum the stopped drift

Source: Lemma 6.1 proof, expected size

```latex
\mathbb E A_{n\wedge T}\le q-\tfrac34\,\mathbb E(n\wedge T)
```

Nonnegativity of the queue yields a uniform bound on the stopped exploration time; monotone convergence then gives the expectation bound for T.

Lean status: `open`.

### 3. Build the exponential supermartingale

Source: Lemma 6.1 proof, tail bound

```latex
\mathbb P\{T>C(q+mu)\}\le e^{-u}
```

The conditional MGF assumption controls the stopped queue and gives the tail with a universal constant C. This step must track the permitted range 0 <= s <= 1/m rather than optimize over an illegal exponent.

Lean status: `open`.

Strict boundary:

This lemma counts a dominating potential request tree. It does not prove that any particular FORS/cloud implementation satisfies the MGF premise, and it does not include RGO-internal query counts except through the separate attachment analysis.

## Adaptive conditional-kernel TV error telescope

Source: Section 6.1, Lemma 6.3

For ideal and implemented adaptive algorithms stopped at the same deterministic number of slots, the output-law error is at most the sum of the mean conditional replacement errors evaluated along the ideal capped histories, plus the probability that the uncapped ideal algorithm exceeds the cap.

```latex
\mathsf{TV}(\operatorname{Law}(\widehat X),\operatorname{Law}(X))\le\sum_{t=1}^{T_{\max}}\delta_t+\varepsilon_{\rm cap}\le T_{\max}\varepsilon+\varepsilon_{\rm cap}
```

Assumptions:

- For each slot 1 <= t <= T_max, K_t(H,.) and Khat_t(H,.) are measurable probability kernels on a common history/output interface.
- Both capped algorithms use the same deterministic T_max and append a measurable dummy symbol after termination.
- The uncapped ideal algorithm exceeds T_max with probability at most epsilon_cap.
- H_{t-1} is the ideal capped history and delta_t is the expectation of TV(K_t(H_{t-1},.), Khat_t(H_{t-1},.)).

Proof route:

### 1. Freeze a common finite history space

Source: Lemma 6.3, setup

```latex
H=(Y_1,\ldots,Y_{T_{\max}}),\qquad Y_t=\dagger\text{ after termination}
```

Dummy filling makes every adaptive run a fixed-length record. This is what permits the t-th conditional rule to be compared without pretending that both algorithms made the same random number of calls.

Lean status: `open`.

### 2. Define adjacent hybrids

Source: Lemma 6.3 proof

```latex
\mathcal A^{(t)}=(K_1,\ldots,K_t,\widehat K_{t+1},\ldots,\widehat K_{T_{\max}})
```

Consecutive hybrids share the ideal history distribution through slot t-1. Therefore the only new discrepancy is the conditional kernel at slot t, averaged under precisely that ideal history.

Lean status: `open`.

### 3. Use data processing for the adaptive suffix

Source: Lemma 6.3 proof

```latex
\mathsf{TV}(\operatorname{Law}(\mathcal A^{(t)}),\operatorname{Law}(\mathcal A^{(t-1)}))\le\delta_t
```

All later calls may depend on the replaced output, but they form one common measurable downstream kernel for this adjacent pair. Data processing absorbs that adaptive continuation.

Lean status: `compiled-support-only`.

Compiled reusable support:

- `AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope.abs_real_comp_sub_le_integral_eventBound`
- `AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope.abs_real_comp_commonSuffix_sub_le_integral_eventBound`

### 4. Telescope the capped adjacent hybrids

Source: Lemma 6.3 proof

```latex
\mathsf{TV}(P_{T_{\max}},P_0)\le\sum_{t=1}^{T_{\max}}\delta_t
```

Apply the triangle inequality to the fixed finite list of hybrid event probabilities. Every slot budget is charged once with unit coefficient.

Lean status: `compiled-support-only`.

Compiled reusable support:

- `AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope.abs_sub_zero_le_sum_range_of_adjacent`

### 5. Add cap failure once

Source: Lemma 6.3 proof

```latex
\mathsf{TV}(\widehat P,P)\le\mathsf{TV}(\widehat P,P_{\rm capped})+\varepsilon_{\rm cap}
```

A final coupling or event comparison handles ideal capped versus ideal uncapped output. This is a separate proof edge, so the cap term is not repeated at every slot.

Lean status: `open`.

Strict boundary:

The mean conditional-event integral, common-suffix contraction and finite real telescope now compile as reusable Lean edges. The exact dummy-filled history kernel, source-specific delta_t identification and measurability, and capped/uncapped comparison remain separate red obligations; therefore Lemma 6.3 itself is not yet formalized. Uniform epsilon is only a corollary after those adapters.

## Section 6 recursive-call and accumulated-error ledger

The paper's adaptive sampler is easiest to audit as two coupled ledgers. The call ledger counts a breadth-first request forest. The error ledger compares ideal and implemented conditional kernels one slot at a time. They meet at the deterministic cap T_max; they must not be collapsed into one informal union bound.

- **Potential request schedule** — Input: FORS attempts and nested cloud/RGO requests Output: A dominating adaptive forest Charge: No accuracy error; this is a counting enlargement.
- **Local and global caps** — Input: Tree-size and per-vertex query tails Output: A finite record of at most T_max slots Charge: Only the ideal global-cap failure contributes epsilon_cap in Lemma 6.3.
- **Slot t replacement** — Input: Same ideal history H_{t-1} Output: Replace K_t by Khat_t Charge: delta_t; later adaptive behavior is handled by data processing.
- **Hybrid telescope** — Input: T_max adjacent algorithm pairs Output: Implemented capped law versus ideal capped law Charge: Sum from t=1 to T_max of delta_t.
- **Final cap comparison** — Input: Ideal capped and ideal uncapped outputs Output: Actual target algorithm comparison Charge: Add epsilon_cap, giving sum delta_t + epsilon_cap.

Ledger boundary:

This ledger does not prove the conditional-kernel bounds, the adaptive-tree moment estimate, measurability of histories, or the paper's final parameter substitution. Each remains a separate theorem obligation. Dummy filling is part of the mathematical interface, not presentation-only padding.

## Suggested agent instruction

Use the pinned source statement and explicit assumptions above. Work on one selected proof step at a time. Separate ASTIS-owned compiled declarations from Mathlib or external facts. Treat every generated explanation and Lean fragment as unverified until the exact snippet compiles and an independent source-fidelity review accepts the correspondence. Never infer whole-paper completion from a reusable support lemma.
