# Log-Concave Sampling Lean Organization

Generated: `2026-08-02 02:28:31`

Primary source: `https://chewisinho.github.io/main.pdf`

Local source: `/home/nitanda_sub/mark/repos/outer_papers/sampling_theory_sde/Chewi-Log-Concave-Sampling/main.pdf`

The repository is a faithful reconstruction of the textbook mathematics.  A
textbook sentence is not stored as one monolithic Lean theorem: it is decomposed
into reusable leaves, and the cited or implicit background steps are made
explicit when Lean needs them.

## How To Read The Library

- Blue nodes in the status tree are compiled local Lean leaves or modules.
- Red nodes are missing mathematical infrastructure with a named target file.
- Shared roots (`MEAS`, `KERN`, `DENS`, `GAUSS`, `CONV`, `FI`, `SDE`, `PATH`,
  `DISC`, `REG`) are reused across chapters so the library does not duplicate
  the same measure-theory, convexity, Gaussian, or SDE lemmas for each sampler.
- Algorithm chapters should be consumers.  They should call the shared roots
  after those roots compile locally.

Main visual ledger:
`research-wiki/lemma-dags/log_concave_sampling_foundation.md`

Rendered status tree:
`docs/assets/log_concave_sampling_status.svg`

## Visual Index

```mermaid
flowchart LR
  PDF[textbook statement]:::source
  Hidden[cited or implicit<br/>background fact]:::source
  Root[shared root<br/>MEAS DENS CONV CALC SDE]:::root
  Leaf[small Lean leaf<br/>blue/red]:::leaf
  Module[owning Lean module]:::module
  Chapter[chapter theorem<br/>consumer]:::consumer

  PDF --> Hidden --> Root --> Leaf --> Module --> Chapter

  classDef source fill:#f8fafc,stroke:#64748b,color:#0f172a,stroke-width:1.5px;
  classDef root fill:#e0f2fe,stroke:#0284c7,color:#0f172a,stroke-width:2px;
  classDef leaf fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef module fill:#fef3c7,stroke:#d97706,color:#422006,stroke-width:2px;
  classDef consumer fill:#dcfce7,stroke:#16a34a,color:#052e16,stroke-width:2px;
```

## Chapter-By-Chapter Map

| Part | Chapter | Summary | Lean organization plan | Shared roots | Status |
| --- | --- | --- | --- | --- | --- |
| Part I | 1. Langevin diffusion in continuous time | The continuous-time backbone: stochastic calculus, Markov semigroups, optimal-transport geometry, Langevin dynamics, and convergence viewpoints. | Generator integrability, Gibbs tails, whole-space weighted IBP, the `C_c^2` core, normalized core annihilation, conditional core invariance, and radial `O(R^-2)` second-derivative/Laplacian cutoff scaling compile locally. The concrete Langevin semigroup/domain extension is external-blocked. | MEAS, GAUSS, DENS, FI, SDE, REG | partial-local-compiled |
| Part I | 2. Functional inequalities | The inequality toolkit that turns geometry of the target into convergence rates: PI, LSI, transport, concentration, isoperimetry, and preservation operations. | Separate definitions and bookkeeping from preservation theorems; reuse log-concavity, Prekopa-Leindler/Brunn-Minkowski, and LSI/KL/FI leaves. | CONV, DENS, FI, REG | partial-local-compiled |
| Part I | 3. Stochastic analysis topics | Path-space tools used repeatedly later: quadratic variation, Girsanov change of measure, Doob transforms, Follmer drift, and Schrodinger bridges. | Keep finite-dimensional Gaussian change of measure as the compiled base; only then lift to Brownian/path-space RN derivatives and bridge transforms. | GAUSS, PATH, DENS, SDE, REG | finite-girsanov-rn-cylinder-compiled |
| Part II | 4. Analysis of Langevin Monte Carlo | The first algorithmic convergence chapter, presenting coupling, interpolation, convex-optimization, and Girsanov proof routes for LMC. | Treat LMC as a consumer of law-map, conditional-kernel, weak-FP, KL/FI, Girsanov, and Gaussian-transition geometry leaves. | MEAS, KERN, SDE, DENS, PATH, DISC, REG | partial-local-compiled |
| Part II | 5. Faster low-accuracy samplers | Randomized midpoint, Hamiltonian Monte Carlo, and underdamped Langevin methods, organized around better discretizations and dynamics. | Delay algorithm theorems until transition kernels, Hamiltonian/underdamped generators, and Gaussian-noise update contracts are local. | GAUSS, SDE, DISC, REG | planned |
| Part II | 6. Convergence in Renyi divergence | Stronger divergence control for LMC and underdamped methods, using interpolation and Girsanov routes. | Extend compiled Renyi integrand algebra toward full divergence, log-normalizer, and path-derivative contracts. | DENS, FI, SDE, PATH, REG | first algebra leaves compiled |
| Part II | 7. High-accuracy samplers | Rejection sampling, Metropolis-Hastings filters, discrete-time Markov chains, and MALA cold/warm start analyses. | Formalize proposal kernels, acceptance probabilities, reversibility/detailed balance, and warm-start density comparisons after kernel infrastructure is stable. | KERN, DENS, GAUSS, DISC, REG | planned |
| Part II | 8. Proximal sampler | Restricted Gaussian oracles and proximal transitions, with convergence under strong log-concavity, log-concavity, and functional inequalities. | Use two-point Gaussian/proximal kernel log-concavity as the compiled start; add restricted Gaussian conditional laws and time-reversal flow interfaces. | CONV, GAUSS, KERN, FI, DISC, REG | kernel-geometry-compiled |
| Part II | 9. Lower bounds for sampling | Oracle/query lower bounds in one dimension, constant dimension, and Gaussian families. | Treat as a consumer of oracle models, information lower bounds, Gaussian comparison, and dimension-specific construction lemmas. | MEAS, GAUSS, DENS, DISC, REG | deferred-consumer |
| Part II | 10. Structured sampling | Sampling with stochastic gradients, coordinate methods, and mirror Langevin geometry. | Introduce oracle/noisy-gradient and coordinate-update interfaces only after base kernels and mirror-geometry assumptions are explicit. | MEAS, CONV, SDE, DISC, REG | deferred-consumer |
| Part II | 11. Non-log-concave sampling | Approximate stationarity and nonconvex behavior controlled through Fisher information bounds and applications. | Reuse FI, KL, weak-FP, and score/Fisher algebra; do not assume convexity roots unless the theorem explicitly requires them. | DENS, FI, SDE, DISC, REG | deferred-consumer |
| Part II | 12. Diffusion generative models | Score matching and discretization analysis for diffusion generative modeling. | Use path-space change of measure, score-drift regularity, weak-FP, and discretization leaves after the SDE/PATH foundation is mature. | MEAS, DENS, SDE, PATH, DISC, REG | deferred-consumer |

## Current Ch.1 Ladder

```mermaid
flowchart TD
  A[generator display<br/>Lf = Delta f - gradV dot gradf]:::blue
  B[weighted display<br/>exp(-V)Lf]:::blue
  C[coordinate divergence<br/>and trace bridge]:::blue
  D[global C1/C2 regularity<br/>gradient, Laplacian, Pi fderiv]:::blue
  E[finite-box trace<br/>IntegrableOn]:::blue
  F[finite-box face terms]:::blue
  G[local and exact-support<br/>smooth cutoffs]:::blue
  H[compact-in-open and Pi-box<br/>plateau = 1]:::blue
  I[radial cutoff family<br/>compact support + tends to 1]:::blue
  J1[scale-uniform cutoff fderiv<br/>O(R^-1)]:::blue
  J1S[closed outer region<br/>totalized fderiv = 0]:::blue
  JP[PiLp cutoff derivative<br/>chain-rule bridge]:::blue
  JT[smulRight basis trace<br/>equals derivative on field]:::blue
  J2[Hessian/Laplacian cutoff<br/>O(R^-2)]:::blue
  K[generic L1 cutoff-gradient limit<br/>from Integrable field]:::blue
  KS[Gibbs source-field<br/>integrability]:::blue
  KM[generic main-term<br/>dominated convergence]:::blue
  KMI[concrete generator-display<br/>integrability for C_c^2 tests]:::blue
  KGT[Gibbs-tail passage]:::blue
  L[weighted whole-space IBP<br/>integral Lf d pi = 0]:::blue
  M[generator and semigroup<br/>domain contract]:::red
  N[invariant Gibbs law]:::red
  O[reversibility<br/>KL/FI dissipation]:::red

  A --> B --> C --> E --> F --> L --> N --> O
  D --> B
  D --> E
  G --> F
  G --> H
  I --> J1 --> JP --> JT --> K --> L
  KS --> L
  KM --> KMI --> L
  KGT --> L
  I --> J1S
  I --> J2
  M --> N

  classDef blue fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef red fill:#fee2e2,stroke:#dc2626,color:#450a0a,stroke-width:2px;
```

| Layer | Current blue result | Remaining red edge |
| --- | --- | --- |
| display algebra | pointwise generator, weighted display, coordinate sum conventions | none for finite-dimensional pointwise algebra |
| regularity | global `C¹/C²` gives gradient continuity, Laplacian continuity, scalar `ContinuousOn`, and Pi-field `HasFDerivAt` with Mathlib `fderiv` | closed-box/local regularity variants if later needed |
| finite boxes | trace `IntegrableOn`, a.e. trace bridge, trace-to-coordinate transfer, signed face-term wrapper | none for the compact-support whole-space route |
| cutoffs | local/exact support, compact-in-open and Pi-box plateaus, radial compact support, pointwise exhaustion, `O(R⁻¹)` first-derivative control, and `O(R⁻²)` second-derivative/Laplacian control | no cutoff estimate is a semigroup-domain theorem |
| whole-space passage | compact-support whole-space divergence and Gibbs-weighted `integral exp(-V) Lf = 0` for `C_c^2` tests, plus generic cutoff/tail infrastructure | stronger noncompact test classes when a consumer requires them |
| operator bridge | C_c^2 core/domain agreement, normalized-Gibbs core annihilation, and abstract semigroup/domain-to-invariance theorem compile | instantiate the contract for the Langevin evolution and extend mean-zero to its stable domain |
| invariant law | abstract implication is compiled | concrete Langevin semigroup contract or an equivalent uniqueness theorem |

## Current Compiled Foundation

- Positive log-concavity, products, powers, pullbacks, superlevel geometry,
  absolute-linear Laplace geometry, and negative-log potential convexity live in
  `AutoSamplingTheory/TechnicalLemmas/Geometry/LogConcavity.lean`.
- Gibbs density, the ENNReal-to-real log-concavity bridge for finite nonzero
  normalizers, finite-measure lower-bound envelopes, exact finite-dimensional
  quadratic normalizers, exact one-dimensional Laplace normalizers, and
  normalized withDensity probability bridges under those explicit envelope
  hypotheses live in `AutoSamplingTheory/TechnicalLemmas/Measure/Gibbs.lean` and
  `AutoSamplingTheory/TechnicalLemmas/Analysis/Integrability.lean`.
- Product Gaussian linear forms, moment-generating normalizers, Esscher shifts,
  finite-dimensional change of measure, and Euclidean `stdGaussian` bridges
  live in `AutoSamplingTheory/TechnicalLemmas/ProbabilityDistributions/Gaussian.lean`.
- KL/DV/Renyi algebra, LSI bookkeeping, weak generator, weak-FP algebra, and
  finite-dimensional Girsanov cylinders are compiled as reusable support.
- `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean` contains
  the reusable smooth unit cutoff, positive-scale radial family, closed-ball
  support and topological-support bounds, compact support, pointwise convergence
  to one, a general compact-in-open smooth plateau theorem, a bounded unit-cutoff
  derivative, the totalized `fderiv` bound for `x -> ||x|| / R`, a single
  constant controlling every radial first derivative by `C / R`, and zero
  totalized derivative throughout the closed outer region `2R <= ||x||`, and
  a single constant controlling every radial second iterated derivative by
  `C / R^2`.  The finite-dimensional Laplacian trace bound is compiled in
  `Analysis/Calculus/Laplacian.lean`.
- `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Divergence.lean`
  contains the finite coordinate-divergence convention, Euclidean/Pi `WithLp`
  trace bridge, the radial-cutoff `toLp` derivative producer, the standard-basis
  `smulRight` trace identity, the generic `L¹` cutoff-gradient limit for every
  `Integrable` finite-Pi vector field, the generic expanding-ball `L¹` tail
  limit, generic cutoff main-term dominated convergence,
  open-box/off-countable to closed-box a.e. transfer,
  trace-to-coordinate `IntegrableOn` transfer, and the finite-box signed
  face-term wrapper with trace-integrability input, and the reusable theorem
  that a compactly supported `C¹` finite-dimensional vector field has zero
  whole-space divergence integral. It also specializes the plateau theorem to
  an inner closed Pi-box inside a larger open Pi-box. It contains no
  generator-domain, semigroup, invariant-law, reversibility, or KL/FI semantics.
- `AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/Langevin.lean`
  contains Langevin-specific blue leaves: finite Euclidean basis/coordinate
  displays of the formal expression `Delta f - <grad V, grad f>`, supplied
  coordinate-to-Mathlib weighted-divergence handoffs, the `exp(-V)` handoffs
  that discharge only the Gibbs-weight gradient premise, the one-dimensional
  Gibbs-weighted generator pointwise identity, the multidimensional
  inner-product supplied-hypothesis weighted-divergence algebra handoff,
  finite-coordinate aggregation handoff, the explicit Pi trace display, and
  the closed-box trace `IntegrableOn` handoff under global `C¹/C²` regularity
  for the canonical Mathlib `fderiv` trace, and whole-space integrability of
  the concrete Gibbs-weighted first-derivative coordinate field from finite
  Gibbs mass and a uniform `fderiv` bound, concrete compact-test generator
  integrability, expanding-ball Gibbs-tail convergence, and whole-space
  Gibbs-weighted integration by parts for `C_c^2` tests. It also assembles the scalar
  display `ContinuousOn` fact from global `C¹/C²` and proves the explicit
  Pi-field `HasFDerivAt` needed by the trace handoff. It is not a closed
  semigroup-generator, invariant-law, reversibility, or semigroup-domain theorem.
- `AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/LangevinGenerator.lean`
  names the `C_c^2` test core, the displayed operator, an explicit candidate
  generator core/domain agreement contract, and normalized-Gibbs generator
  mean-zero on that core. `WeakGenerator.lean` contains the separate abstract
  integrated-semigroup-generator contract and its invariance theorem.

## Immediate Library Boundary

The next high-value roots, ordered by the active textbook dependency, are:

1. `SDE/REG`: instantiate the integrated semigroup-generator contract for the
   actual Langevin evolution, including the right derivative of Gibbs pairings.
2. `SDE/DENS/FI`: extend normalized-Gibbs generator mean-zero from the
   `C_c^2` core to the semigroup-stable domain, or supply an equivalent
   martingale-problem/Fokker-Planck uniqueness theorem.
3. `CONV/MEAS`: finite-dimensional Prekopa-Leindler and Brunn-Minkowski
   interfaces, using `Lean-Asymptotic-Statistical-Theory/ForMathlib` as a
   reference but porting only small local leaves.
4. `DENS/CONV`: nonquadratic coercive Gibbs envelopes for Lebesgue targets.
5. `PATH/GAUSS`: Brownian/path-space change of measure beyond finite
   cylinders.
6. `DISC`: LMC/MALA/HMC/proximal samplers only after the above roots are local.

## Rigor Contract

Whenever the textbook uses a standard analytic phrase such as Fokker-Planck,
Girsanov, integration by parts, regularity assumptions, or invariant measure,
the Lean plan must expose the hidden assumptions: measurability,
integrability, domination, differentiability, boundary decay, positivity, and
representative choices.  Unsupported assumptions are recorded as red proof
obligations rather than being silently added to close a theorem.
