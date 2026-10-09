# Log-Concave Sampling Foundation DAG

Generated: `2026-08-02 02:28:31`

Primary source: `https://chewisinho.github.io/main.pdf`

Local source: `/home/nitanda_sub/mark/repos/outer_papers/sampling_theory_sde/Chewi-Log-Concave-Sampling/main.pdf`

This is the master visualization ledger for `ASTIS-CHEWI-001`.  The goal is
to avoid one oversized graph: every chapter or major theorem should point
to shared root nodes and then have its own smaller subtree.  Shared labels make
common Lean leaves reusable across chapters and later theorem subtrees.

## Global Spine

```mermaid
flowchart LR
  Source[Log-Concave Sampling textbook]
  Mathlib[Mathlib API search]
  ASTRef[External Lean references]
  REG[REG hidden regularity contracts]
  MEAS[MEAS law map and measures]
  KERN[KERN conditional kernels]
  DENS[DENS densities RN KL Renyi]
  GAUSS[GAUSS Gaussian products]
  CONV[CONV convex log-concave PL BM]
  FI[FI PI LSI transport concentration]
  SDE[SDE semigroup generator Langevin weak-FP]
  PATH[PATH Girsanov Doob Follmer bridge]
  DISC[DISC LMC HMC MALA proximal]
  Consumers[textbook theorem and algorithm consumers]

  Source --> MEAS
  Source --> CONV
  Source --> FI
  Source --> SDE
  Source --> PATH
  Source --> DISC
  Mathlib --> MEAS
  Mathlib --> DENS
  Mathlib --> CONV
  Mathlib --> FI
  ASTRef --> CONV
  ASTRef --> GAUSS
  ASTRef --> DENS
  ASTRef --> PATH
  REG -. required by every leaf .-> MEAS
  REG -. required by every leaf .-> CONV
  REG -. required by every leaf .-> SDE
  MEAS --> KERN
  MEAS --> DENS
  DENS --> FI
  GAUSS --> PATH
  CONV --> FI
  FI --> SDE
  SDE --> DISC
  PATH --> DISC
  DISC --> Consumers
```

## Blue/Red Lean Tree Status

Blue nodes are compiled local ASTIS declarations or modules covered by
`lake build`.  Red nodes are the todo branches I can keep driving with
Mathlib-first leaves and explicit source/regularity contracts.

Rendered status tree:
`docs/assets/log_concave_sampling_status.svg`

```mermaid
flowchart TD
  Root[ASTIS-CHEWI-001<br/>Log-concave sampling Lean tree]
  MEAS[MEAS/KERN<br/>measure and kernels]
  DENS[DENS/CONV<br/>densities and convexity]
  GAUSS[GAUSS<br/>Gaussian infrastructure]
  FI[FI<br/>functional inequalities]
  SDE[SDE/PATH<br/>continuous-time and transforms]
  DISC[DISC<br/>sampling algorithms]

  Root --> MEAS
  Root --> DENS
  Root --> GAUSS
  Root --> FI
  Root --> SDE
  Root --> DISC

  MEAS --> LawMap[Probability.LawMap]
  MEAS --> CondKernel[Probability.ConditionalKernel]
  MEAS --> PiUpdate[Measure.Product coordinate update]
  MEAS --> Transport[Measure.Transport]

  DENS --> LogConcavity[Geometry.LogConcavity]
  DENS --> LogConcavityTensor[Log-concavity algebra/tensorization]
  DENS --> LogConcavityMaps[Log-concavity under maps]
  DENS --> LogConcavityLevels[Log-concavity level sets]
  DENS --> NegLogPotential[Negative-log potential geometry]
  DENS --> GibbsQuadLogConcavity[Quadratic Gibbs log-concavity]
  DENS --> ShiftedGibbsQuad[Shifted quadratic Gibbs geometry]
  DENS --> PairKernelGeometry[Two-point Gaussian/proximal kernel geometry]
  DENS --> RN[Measure.RadonNikodym]
  DENS --> PiDensity[Measure.pi withDensity product]
  DENS --> Gibbs[Measure.Gibbs]
  DENS --> GibbsIntegral[Gibbs withDensity Bochner integral rewrite]
  DENS --> GibbsPotentialEnv[Potential lower-bound envelope]
  DENS --> GibbsFiniteEnv[Finite-measure Gibbs envelope]
  DENS --> GibbsQuadEnv[Quadratic Lebesgue Gibbs envelope]
  DENS --> KLDV[InformationTheory.KLDensity/DV]
  DENS --> PLBM[Prekopa/Brunn/Convex]
  DENS --> GibbsEnv[General coercivity Gibbs envelope]
  DENS --> Renyi[Renyi density calculus]

  GAUSS --> Gaussian[ProbabilityDistributions.Gaussian]
  GAUSS --> GaussianLinear[Product Gaussian linear forms]
  GAUSS --> GaussianMGF[Product Gaussian MGF / normalizer]
  GAUSS --> GaussianScalarShift[Scalar Gaussian Esscher shift]
  GAUSS --> GaussianProductShift[Product Gaussian shifted density]
  GAUSS --> GaussianCOM[Product Gaussian change of measure]
  GAUSS --> GaussianEuclidean[EuclideanSpace Gaussian pushforward]
  GAUSS --> GaussianStd[stdGaussian inner-product change of measure]
  GAUSS --> GaussianPath[Full path-space Gaussian / Girsanov]

  FI --> LSI[FunctionalInequalities.LogSobolev]
  FI --> PITI[PI/TI/Isoperimetry]
  FI --> Preserve[Preservation/tensorization]

  SDE --> WeakGen[StochasticProcesses.WeakGenerator]
  SDE --> FP[StochasticProcesses.FokkerPlanckAlgebra]
  SDE --> Langevin1D[StochasticProcesses.Langevin expression display/algebra]
  SDE --> BoxDiv[Analysis.Calculus.Divergence box face-term wrapper]
  SDE --> AEBridge[Analysis.Calculus.Divergence a.e. trace bridge]
  SDE --> IntTransfer[Analysis.Calculus.Divergence trace-to-coordinate IntegrableOn]
  SDE --> ExplicitTrace[StochasticProcesses.Langevin explicit trace display]
  SDE --> DisplayContinuity[Scalar display ContinuousOn from components]
  SDE --> TraceIntegrability[Trace IntegrableOn under global C1/C2]
  SDE --> TestRegularity[Global C1/C2 components and Pi field fderiv]
  SDE --> CutoffBase[Reusable smooth cutoffs and plateaus]
  SDE --> CutoffFirst[Scale-uniform cutoff first derivative]
  SDE --> CutoffL1[Generic L1 cutoff-gradient limit]
  SDE --> CutoffMain[Generic cutoff main-term DCT]
  SDE --> CutoffSecond[Second-order cutoff on demand]
  SDE --> GirsanovFinite[StochasticProcesses.Girsanov finite cylinder]
  SDE --> Langevin[Semigroup/Ito/invariant Gibbs law]
  SDE --> Path[Girsanov/Doob/Follmer]

  DISC --> LMC[LMC interpolation]
  DISC --> HMC[HMC/underdamped/RM]
  DISC --> MALA[MALA/proximal/high-accuracy]

  classDef root fill:#f8fafc,stroke:#475569,color:#0f172a,stroke-width:2px;
  classDef compiled fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef todo fill:#fee2e2,stroke:#dc2626,color:#450a0a,stroke-width:2px;
  class Root,MEAS,DENS,GAUSS,FI,SDE,DISC root;
  class LawMap,CondKernel,PiUpdate,LogConcavity,LogConcavityTensor,LogConcavityMaps,LogConcavityLevels,NegLogPotential,GibbsQuadLogConcavity,ShiftedGibbsQuad,PairKernelGeometry,RN,PiDensity,Gibbs,GibbsIntegral,GibbsPotentialEnv,GibbsFiniteEnv,GibbsQuadEnv,KLDV,Renyi,Gaussian,GaussianLinear,GaussianMGF,GaussianScalarShift,GaussianProductShift,GaussianCOM,GaussianEuclidean,GaussianStd,LSI,WeakGen,FP,Langevin1D,BoxDiv,AEBridge,IntTransfer,ExplicitTrace,DisplayContinuity,TraceIntegrability,TestRegularity,CutoffBase,CutoffFirst,CutoffL1,GirsanovFinite compiled;
  class Transport,PLBM,GibbsEnv,GaussianPath,PITI,Preserve,CutoffSecond,Langevin,Path,LMC,HMC,MALA todo;
```

| Family | Branch/leaf | Target | Color status | Role |
| --- | --- | --- | --- | --- |
| MEAS/KERN | Probability.LawMap | TechnicalLemmas/Probability/LawMap.lean | compiled-blue | law-map and weak-test integral rewrites |
| MEAS/KERN | Probability.ConditionalKernel | TechnicalLemmas/Probability/ConditionalKernel.lean | compiled-blue | condDistrib and conditional-integral representatives |
| MEAS/KERN | Measure.Transport | TechnicalLemmas/Measure/Transport.lean | todo-red | transport/coupling/Wasserstein interfaces |
| DENS/CONV | Geometry.LogConcavity | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | positive log-concavity, norm-square and absolute-value convexity, and convex-potential Gibbs shape |
| DENS/CONV | Log-concavity algebra/tensorization | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | pointwise products, nonnegative real powers, and Cartesian-product density factors preserve log-concavity |
| DENS/CONV | Log-concavity under maps | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | linear and affine precomposition preserve log-concavity on preimage domains |
| DENS/CONV | Log-concavity level sets | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | positive log-concave functions are quasiconcave; convex superlevel restrictions remain log-concave |
| GEOM/GAUSS/SDE | EuclideanSpace coordinate inner products | TechnicalLemmas/Geometry/EuclideanSpaceCoordinates.lean | compiled-blue | finite-dimensional coordinate formulas for `inner ℝ u v`, including direct `EuclideanSpace` vectors and `WithLp.toLp 2` coordinate functions |
| ANALYSIS/SDE | Laplacian standard-basis formula | TechnicalLemmas/Analysis/Calculus/Laplacian.lean | compiled-blue | Mathlib `Laplacian.laplacian` equals the finite standard-orthonormal-basis second-derivative sum; no IBP or invariant-law proof |
| ANALYSIS/SDE | Gradient coordinate-unit line derivative | TechnicalLemmas/Analysis/Calculus/Gradient.lean | compiled-blue | a supplied Mathlib gradient gives the coordinate-unit line derivative equal to the corresponding gradient coordinate; no divergence or IBP proof |
| ANALYSIS/SDE | Gibbs-weight gradient chain rule | TechnicalLemmas/Analysis/Calculus/Gradient.lean | compiled-blue | a supplied `HasGradientAt V gradV x` or `DifferentiableAt ℝ V x` gives Mathlib `gradient (exp(-V))` and coordinate chain-rule displays; no weighted divergence, coordinate product-rule, or IBP proof |
| ANALYSIS/SDE | Line-derivative product rule | TechnicalLemmas/Analysis/Calculus/LineDeriv.lean | compiled-blue | Mathlib `HasDerivAt.mul` exposed as real-valued `HasLineDerivAt` and `lineDeriv` product rules, explicit coordinate `lineDeriv (exp(-V) * g)` leaves, and `fderiv`-to-`iteratedFDeriv` coordinate wiring; no divergence or IBP proof |
| DENS/CONV/SDE | Negative-log potential geometry | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | positive log-concave densities have convex negative-log potentials and convex energy sublevels |
| DENS/CONV | Quadratic Gibbs log-concavity | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | nonnegative quadratic norm potentials and explicit normalized quadratic Gibbs densities are log-concave |
| DENS/CONV | Absolute-linear Laplace geometry | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | one-dimensional potentials `a\|x\|+b` and positive rescaled Laplace shapes are log-concave |
| DENS/CONV/GAUSS | Shifted quadratic Gibbs geometry | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | shifted potentials `a‖x-m‖^2+b` and explicit shifted quadratic densities are log-concave |
| DENS/CONV/GAUSS/DISC | Two-point Gaussian/proximal kernel geometry | TechnicalLemmas/Geometry/LogConcavity.lean | compiled-blue | two-point potentials `a‖x-y‖^2+b` and Gaussian-kernel shapes are log-concave on product space |
| DENS/CONV | Measure.RadonNikodym | TechnicalLemmas/Measure/RadonNikodym.lean | compiled-blue | withDensity, reciprocal-lintegral normalization, RN wrappers |
| DENS/MEAS | Measure.pi withDensity product | TechnicalLemmas/Measure/RadonNikodym.lean | compiled-blue | finite-product ENNReal Fubini and coordinatewise density-tilt decomposition |
| MEAS/FI/SDE | Measure.Product coordinate update | TechnicalLemmas/Measure/Product.lean | compiled-blue | finite product-law coordinate replacement map, measure-preserving wrapper, Bochner integral rewrite, and a.e. slice integrability |
| DENS/CONV | Measure.Gibbs | TechnicalLemmas/Measure/Gibbs.lean | compiled-blue | Gibbs ENNReal density, measurability, envelope comparison, and normalization |
| DENS/MEAS/SDE | Gibbs withDensity Bochner integral rewrite | TechnicalLemmas/Measure/GibbsIntegral.lean | compiled-blue | Bochner integrals under `Z⁻¹ exp(-V)` withDensity rewrite to density-weighted base-measure integrals |
| DENS/CONV | Normalized Gibbs real-density bridge | TechnicalLemmas/Measure/GibbsLogConcavity.lean | compiled-blue | finite nonzero ENNReal normalizer plus convex or strongly convex potential gives a real-valued normalized Gibbs density shape that is log-concave |
| DENS/CONV | Potential lower-bound envelope | TechnicalLemmas/Measure/Gibbs.lean | compiled-blue | `W ≤ V` a.e. and finite `∫ exp(-W)` imply finite `∫ exp(-V)` and normalized Gibbs law |
| DENS/CONV | Finite-measure Gibbs envelope | TechnicalLemmas/Measure/Gibbs.lean | compiled-blue | finite base measure plus a.e. constant lower bound on `V` gives finite Gibbs normalizer and normalized target law |
| DENS/CONV/ANALYSIS | Quadratic Lebesgue Gibbs envelope | TechnicalLemmas/Analysis/Integrability.lean | compiled-blue | finite-dimensional Lebesgue quadratic tails have exact ENNReal normalizers, and quadratic lower bounds give normalized Gibbs target laws |
| DENS/CONV/ANALYSIS | One-dimensional Laplace normalizer | TechnicalLemmas/Analysis/Integrability.lean | compiled-blue | exact `∫ exp (-(a\|x\|+b)) = 2 exp(-b)/a`, exact ENNReal normalizer, and explicit normalized Laplace law on `ℝ` |
| DENS/CONV | InformationTheory.KLDensity/DV | TechnicalLemmas/InformationTheory/{KLDensity,DonskerVaradhan}.lean | compiled-blue | KL pointwise algebra and DV energy leaves |
| DENS/CONV | Prekopa/Brunn/Convex | TechnicalLemmas/Geometry/{Convex,PrekopaLeindler,BrunnMinkowski}.lean | todo-red | finite-dimensional PL/BM and convex-measure preservation |
| DENS/CONV | Concrete Gibbs envelope | TechnicalLemmas/Measure/Gibbs.lean or Analysis/Integrability.lean | todo-red | general nonquadratic Lebesgue coercivity/growth assumptions beyond finite-dimensional quadratic and one-dimensional Laplace envelopes |
| DENS/CONV | Renyi density calculus | TechnicalLemmas/InformationTheory/Renyi.lean | compiled-blue | Renyi integrand positivity, measurability, finite-envelope, and pointwise derivative leaves |
| GAUSS | ProbabilityDistributions.Gaussian | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | Gaussian moments, coordinate laws, finite linear forms, MGF normalizers, shifted densities, and variance packaging |
| GAUSS | Product Gaussian linear forms | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | finite product-Gaussian linear-form integrability and zero mean |
| GAUSS | Product Gaussian MGF / normalizer | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | finite product-Gaussian linear-form MGF and centered Esscher mass-one normalizer |
| GAUSS | Scalar Gaussian Esscher shift | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | one-dimensional Gaussian exponential tilt shifts the mean |
| GAUSS | Product Gaussian shifted density | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | finite product standard Gaussian withDensity tilt equals shifted product Gaussian |
| GAUSS | Product Gaussian change of measure | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | finite shifted product-Gaussian integrals rewrite as centered weighted integrals |
| GAUSS | EuclideanSpace Gaussian pushforward | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | transport finite product-Gaussian Esscher change-of-measure through `WithLp.toLp 2` |
| GAUSS | stdGaussian inner-product change of measure | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | compiled-blue | rewrite the Euclidean change-of-measure against Mathlib `stdGaussian` with inner-product/norm exponent |
| GAUSS | Full path-space Gaussian / Girsanov | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | todo-red | Brownian/path-space RN derivative beyond finite-dimensional cylinders |
| FI | FunctionalInequalities.LogSobolev | TechnicalLemmas/FunctionalInequalities/LogSobolev.lean | compiled-blue | LSI to KL/FI bookkeeping and sqrt-density handoffs |
| FI | PI/TI/Isoperimetry | TechnicalLemmas/FunctionalInequalities/{Poincare,Transport,Isoperimetry}.lean | todo-red | Poincare, transport inequalities, concentration, isoperimetry |
| FI | Preservation/tensorization | TechnicalLemmas/FunctionalInequalities/Preservation.lean | todo-red | tensorization and preservation under log-concavity operations |
| SDE/PATH | StochasticProcesses.WeakGenerator | TechnicalLemmas/StochasticProcesses/WeakGenerator.lean | compiled-blue | sample-to-law weak-generator rewrite |
| SDE/PATH | StochasticProcesses.FokkerPlanckAlgebra | TechnicalLemmas/StochasticProcesses/FokkerPlanckAlgebra.lean | compiled-blue | weak-FP and Fisher/IBP scalar algebra |
| SDE/PATH | StochasticProcesses.Langevin | TechnicalLemmas/StochasticProcesses/Langevin.lean | compiled-blue | Finite Euclidean pointwise display and supplied-hypothesis Langevin algebra: basis/coordinate display for the formal expression `Δ f - <∇V, ∇f>`, supplied coordinate-to-Mathlib weighted-divergence handoffs, `exp(-V)` handoffs discharging only the Gibbs-weight gradient premise, pointwise coordinateDivergence display, finite-box signed face-term wrapper with explicit assumptions, 1D pointwise derivative, finite-coordinate aggregation, and EuclideanSpace inner-product notation wrappers; no box-integrability discharge, semigroup-generator, IBP, stationarity, or invariant-law proof |
| ANALYSIS/SDE | Reusable smooth cutoffs and plateaus | TechnicalLemmas/Analysis/Calculus/{Cutoff,Divergence}.lean | compiled-blue | unit and radial smooth cutoffs, support/tsupport and compact-support bounds, pointwise exhaustion, compact-in-open plateau, and finite Pi-box plateau |
| ANALYSIS/SDE | Scale-uniform cutoff first derivative | TechnicalLemmas/Analysis/Calculus/{Cutoff,Divergence}.lean | compiled-blue | one unit-cutoff constant controls every positive-scale radial fderiv by C/R; the totalized fderiv vanishes on the closed outer region; PiLp chain-rule and standard-basis trace bridges expose the cutoff cross term |
| ANALYSIS/SDE | Generic L1 cutoff-gradient limit | TechnicalLemmas/Analysis/Calculus/Divergence.lean | compiled-blue | for every Integrable finite-Pi vector field, the norm integral of the PiLp-wrapped radial cutoff derivative applied to the field tends to zero |
| ANALYSIS/SDE | Generic cutoff main-term dominated convergence | TechnicalLemmas/Analysis/Calculus/Divergence.lean | compiled-blue | for every Integrable normed-space-valued field, multiplication by the PiLp-wrapped radial cutoff converges under the integral to the original field |
| ANALYSIS/SDE | Gibbs source and generator-display integrability | TechnicalLemmas/StochasticProcesses/Langevin.lean plus on-demand cutoff leaves | compiled-blue | finite Gibbs mass plus bounded genuine first derivative gives Integrable exp(-V)-weighted coordinate fields; compact C_c^2 tests give both the concrete Integrable generator display and the compiled whole-space identity integral exp(-V) Lf = 0 |
| SDE/PATH | StochasticProcesses.Girsanov finite cylinder | TechnicalLemmas/StochasticProcesses/Girsanov.lean | compiled-blue | finite-dimensional cylindrical Gaussian Girsanov weight, RN density, and integral change-of-measure |
| SDE/PATH | Semigroup/Ito/invariant Gibbs law | TechnicalLemmas/StochasticProcesses/{MarkovSemigroup,Ito}.lean plus stronger Langevin analytic leaves | todo-red | semigroup domains, invariant Gibbs law, Ito interfaces |
| SDE/PATH | Girsanov/Doob/Follmer | TechnicalLemmas/StochasticProcesses/{Girsanov,DoobTransform,FollmerDrift}.lean | todo-red | path-space RN derivatives and bridge transforms |
| DISC | LMC interpolation | SamplingAlgorithms/LangevinMonteCarlo.lean | todo-red | LMC interpolation, coupling, KL/FI derivative consumers |
| DISC | HMC/underdamped/RM | SamplingAlgorithms/{HamiltonianMonteCarlo,UnderdampedLangevin,RandomizedMidpoint}.lean | todo-red | faster low-accuracy sampler transition/generator contracts |
| DISC | MALA/proximal/high-accuracy | SamplingAlgorithms/{MetropolisAdjustedLangevin,ProximalSampler}.lean | todo-red | acceptance kernels, detailed balance, restricted Gaussian oracles |

## Shared Root Nodes

| Label | Shared root | Target module/root | Role | Status |
| --- | --- | --- | --- | --- |
| MEAS | measure-space and law transport | TechnicalLemmas/Probability/LawMap.lean | push forward laws, weak-test integrals, map/withDensity/RN bridges | partial-compiled-local |
| KERN | conditional kernels and representatives | TechnicalLemmas/Probability/ConditionalKernel.lean | condDistrib pairings, conditional drifts, a.e. representative discipline | partial-compiled-local |
| DENS | densities, RN derivative, KL/Renyi integrands | TechnicalLemmas/Geometry/LogConcavity.lean; Measure/{Gibbs,RadonNikodym}.lean; InformationTheory/* | positive density APIs, density-to-potential extraction, log-concavity algebra/tensorization, level-set quasiconcavity/restriction, linear/affine precomposition, centered/shifted/two-point quadratic and one-dimensional Laplace Gibbs log-concavity, Gibbs ENNReal density, finite-measure, exact quadratic, and exact one-dimensional Laplace Lebesgue normalization, absolute continuity, withDensity, pointwise entropy algebra | partial-compiled-local |
| GAUSS | Gaussian and product Gaussian infrastructure | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | standard Gaussian laws, moments, MGF, finite-dimensional tilts, shifted and two-point quadratic density geometry | partial-compiled-local |
| CONV | convex and log-concave geometry | TechnicalLemmas/Geometry/{Convex,LogConcavity,PrekopaLeindler}.lean | convex functions/sets, negative-log potentials, log-concave superlevels, quadratic norm potentials, log-concavity products/powers and linear/affine pullbacks, Prekopa-Leindler, Brunn-Minkowski | partial-compiled-local |
| FI | functional inequalities | TechnicalLemmas/FunctionalInequalities/* | PI, LSI, transport, concentration, isoperimetry, preservation | planned-plus-LSI-bookkeeping-compiled |
| SDE | semigroup, generator, weak-FP, Langevin | TechnicalLemmas/StochasticProcesses/* | Markov semigroups, invariant Gibbs law, generator/KL dissipation | partial-compiled-local |
| PATH | path-space change of measure | TechnicalLemmas/StochasticProcesses/{Girsanov,DoobTransform,FollmerDrift}.lean | Girsanov, Doob transform, Follmer drift, Schrodinger bridge | planned |
| DISC | algorithm discretization layer | SamplingAlgorithms/* | LMC, randomized midpoint, HMC, underdamped, MALA, proximal sampler | planned-consumer |
| REG | hidden regularity contracts | research-wiki/technical-lemmas/hidden_regularities.md | measurability, integrability, domination, smoothness, boundary, positivity | protocol |

## Chapter And Theorem Subtree Registry

| Chapter/topic | Shared labels | Subtree to draw/formalize | First lower-agent leaf | Status |
| --- | --- | --- | --- | --- |
| 1.1 stochastic calculus | MEAS, GAUSS, REG | Ito/quadratic-variation/Taylor local-error subtree | quadratic variation normalization and finite-dimensional Ito test identity | partial-local-compiled |
| 1.2 Markov semigroups | MEAS, SDE, REG | semigroup -> generator-domain -> weak-test derivative subtree | semigroup test-function pairing under generator-domain hypotheses | planned |
| 1.3 optimal transport geometry | MEAS, CONV, REG | couplings -> Wasserstein distance -> geodesic convexity subtree | law-map/coupling measurable pushforward interface | planned |
| 1.4 Langevin as gradient flow | DENS, FI, SDE, REG | Gibbs density -> generator -> KL/FI dissipation -> WGF contract | Whole-space IBP, the C_c^2 core-domain contract, normalized-Gibbs core annihilation, and the abstract semigroup/domain-to-invariance bridge compile; concrete Langevin semigroup instantiation and domain extension remain | abstract-semigroup-invariance-bridge-compiled |
| 2 functional inequalities | CONV, DENS, FI, REG | PI/LSI/TI/isoperimetry plus preservation-operation subtrees | log-concavity products, nonnegative powers, product-domain tensorization, linear/affine precomposition, negative-log potential convexity, superlevel convexity, plus Prekopa-Leindler preservation audit | partial-local-compiled |
| 3 stochastic analysis topics | PATH, DENS, SDE, REG | Girsanov -> Doob transform -> Follmer drift -> Schrodinger bridge | finite-dimensional Gaussian Esscher density, stdGaussian inner-product form, cylindrical Girsanov integral, and RN/withDensity identity compiled; full Brownian path packaging remains | finite-girsanov-rn-cylinder-compiled |
| 4 Langevin Monte Carlo | MEAS, KERN, SDE, DENS, REG, DISC | coupling/interpolation/convex-optimization/Girsanov proof subtrees | LMC interpolation weak-test law derivative under domination; two-point Gaussian transition-kernel geometry compiled | partial-local-compiled |
| 5 faster low-accuracy samplers | GAUSS, SDE, DISC, REG | randomized midpoint, HMC, underdamped generator subtrees | Hamiltonian/underdamped transition-kernel regularity contract | planned |
| 6 Renyi divergence | DENS, FI, SDE, REG | Renyi density algebra -> interpolation/Girsanov derivative subtrees | Renyi density algebra with positivity and finite-integral contracts | first algebra leaves compiled |
| 7 high-accuracy samplers | KERN, DENS, DISC, REG | rejection/MH/MALA kernels, detailed balance, warm-start subtrees | proposal/acceptance Markov-kernel mass and reversibility contract | planned |
| 8 proximal sampler | CONV, GAUSS, KERN, DISC, REG | restricted Gaussian oracle -> conditional laws -> proximal transition subtree | two-point Gaussian/proximal kernel log-concavity and log-concave superlevel restriction compiled; restricted Gaussian conditional law remains | kernel-geometry-compiled |
| 9-12 lower bounds, structure, non-log-concave, diffusion models | MEAS, DENS, SDE, PATH, DISC, REG | consumer subtrees after core log-concave foundation stabilizes | source-specific leaf only after shared roots are compiled | deferred-consumer |

## Chapter 1 Langevin Continuous-Time Subtree

```mermaid
flowchart TD
  C1[Ch.1 Langevin diffusion]
  SC[1.1 stochastic calculus]
  MS[1.2 Markov semigroup]
  OT[1.3 optimal transport]
  WGF[1.4 Wasserstein gradient flow]
  GAUSS[GAUSS Gaussian increments]
  TAY[Taylor/Ito local error]
  SEM[Markov semigroup operator]
  GEN[generator-domain contract]:::blue
  GENALG[Gibbs-weight generator algebra]:::blue
  BOX[finite-box divergence<br/>and zero-face handoffs]:::blue
  LOCAL[local/exact-support<br/>cutoff leaves]:::blue
  PLATEAU[compact-in-open and Pi-box<br/>plateau cutoffs]:::blue
  RADIAL[radial cutoff family<br/>compact support + pointwise limit]:::blue
  DERIV1[scale-uniform fderiv<br/>O(R^-1)]:::blue
  DSUP[closed outer region<br/>totalized fderiv = 0]:::blue
  PIB[PiLp derivative and<br/>smulRight trace bridges]:::blue
  DERIV2[Hessian/Laplacian<br/>O(R^-2)]:::blue
  TAIL[generic L1 cutoff-gradient limit<br/>from Integrable field]:::blue
  SOURCEINT[Gibbs source-field<br/>integrability]:::blue
  MAINCONV[generic main-term<br/>dominated convergence]:::blue
  MAININT[concrete generator-display<br/>integrability for C_c^2 tests]:::blue
  GIBBSTAIL[Gibbs-tail passage]:::blue
  IBP[whole-space weighted IBP]:::blue
  BRIDGE[abstract semigroup/domain<br/>to invariance]:::blue
  CONCRETE[concrete Langevin semigroup<br/>and stable domain]:::red
  INV[invariant Gibbs law]:::red
  KL[KL/FI dissipation]
  W2[Wasserstein gradient-flow contract]
  REG[REG hidden regularity]

  C1 --> SC
  C1 --> MS
  C1 --> OT
  C1 --> WGF
  SC --> GAUSS --> TAY
  MS --> SEM --> GEN --> BRIDGE
  GEN --> GENALG --> BOX --> IBP --> BRIDGE --> CONCRETE --> INV
  LOCAL --> BOX
  LOCAL --> PLATEAU
  PLATEAU --> BOX
  RADIAL --> DERIV1 --> PIB --> TAIL --> IBP
  SOURCEINT --> IBP
  MAINCONV --> MAININT --> IBP
  GIBBSTAIL --> IBP
  RADIAL --> DSUP
  RADIAL --> DERIV2
  WGF --> INV --> KL --> W2
  REG -.-> TAY
  REG -.-> GEN
  REG -.-> GENALG
  REG -.-> BOX
  REG -.-> DERIV1
  REG -.-> DSUP
  REG -.-> PIB
  REG -.-> DERIV2
  REG -.-> TAIL
  REG -.-> SOURCEINT
  REG -.-> MAINCONV
  REG -.-> IBP
  REG -.-> INV

  classDef blue fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef red fill:#fee2e2,stroke:#dc2626,color:#450a0a,stroke-width:2px;
```

## Chapter 2 Functional-Inequality Subtree

```mermaid
flowchart TD
  C2[Ch.2 functional inequalities]
  DEF[PI LSI TI definitions]
  SEM[semigroup proof route]
  PRES[preservation operations]
  CONC[concentration and isoperimetry]
  DISC[discrete space/time]
  CONV[CONV log-concavity]
  PL[Prekopa-Leindler]
  LSI[LSI to KL/FI compiled bookkeeping]
  REG[REG hidden regularity]

  C2 --> DEF
  C2 --> SEM
  C2 --> PRES
  C2 --> CONC
  C2 --> DISC
  CONV --> PL --> PRES
  DEF --> LSI
  SEM --> LSI
  REG -.-> PL
  REG -.-> LSI
```

## Chapter 4 LMC Interpolation Subtree

```mermaid
flowchart TD
  C4[Ch.4 Langevin Monte Carlo]
  COUP[Wasserstein coupling proof]
  INT[interpolation proof]
  OPT[convex optimization proof]
  GIR[Girsanov proof]
  LAW[MEAS law-map derivative]
  KERN[KERN conditional drift]
  WFP[SDE weak-FP bridge]
  KL[DENS KL/FI derivative]
  PATH[PATH change of measure]
  DISC[DISC LMC theorem]
  REG[REG hidden regularity]

  C4 --> COUP
  C4 --> INT
  C4 --> OPT
  C4 --> GIR
  INT --> LAW --> WFP
  KERN --> WFP
  WFP --> KL --> DISC
  GIR --> PATH --> DISC
  REG -.-> LAW
  REG -.-> WFP
  REG -.-> KL
```

## Chapter 3 Path-Space Stochastic Analysis Subtree

```mermaid
flowchart TD
  C3[Ch.3 stochastic analysis topics]
  QV[quadratic variation]
  COM[change of measure in path space]
  DOOB[Doob transform]
  FOLL[Follmer drift]
  SB[Schrodinger bridge]
  GAUSS[GAUSS finite Gaussian shifts]
  CYL[finite-dimensional Girsanov cylinder]
  RN[PATH RN derivative]
  BRIDGE[bridge drift transform]
  REG[REG path regularity]

  C3 --> QV
  C3 --> COM
  C3 --> DOOB
  C3 --> FOLL
  C3 --> SB
  GAUSS --> CYL --> RN
  COM --> RN
  DOOB --> BRIDGE
  FOLL --> BRIDGE
  SB --> BRIDGE
  REG -.-> QV
  REG -.-> RN
  REG -.-> BRIDGE
```

## Chapter 5 Faster Low-Accuracy Samplers Subtree

```mermaid
flowchart TD
  C5[Ch.5 faster low-accuracy samplers]
  RMD[randomized midpoint]
  HMC[Hamiltonian Monte Carlo]
  ULD[underdamped Langevin]
  GAUSS[GAUSS update noise]
  GEN[SDE generator contracts]
  KERN[DISC transition kernels]
  RATE[low-accuracy rate theorem]
  REG[REG smoothness and moments]

  C5 --> RMD
  C5 --> HMC
  C5 --> ULD
  GAUSS --> KERN
  RMD --> KERN
  HMC --> GEN
  ULD --> GEN
  GEN --> RATE
  KERN --> RATE
  REG -.-> GEN
  REG -.-> KERN
```

## Chapter 6 Renyi Divergence Subtree

```mermaid
flowchart TD
  C6[Ch.6 Renyi divergence]
  LMCINT[LMC interpolation route]
  LMCGIR[LMC Girsanov route]
  ULMC[ULMC Girsanov route]
  RENYI[DENS Renyi density calculus]
  FI[FI differential inequality]
  PATH[PATH change of measure]
  DISC[DISC algorithm theorem]
  REG[REG integrability and positivity]

  C6 --> LMCINT
  C6 --> LMCGIR
  C6 --> ULMC
  RENYI --> FI --> DISC
  PATH --> RENYI
  LMCINT --> FI
  LMCGIR --> PATH
  ULMC --> PATH
  REG -.-> RENYI
  REG -.-> FI
```

## Chapter 7 High-Accuracy Samplers Subtree

```mermaid
flowchart TD
  C7[Ch.7 high-accuracy samplers]
  RS[rejection sampling]
  MH[Metropolis-Hastings filter]
  MC[discrete-time Markov chains]
  COLD[MALA cold start]
  WARM[MALA warm start]
  KERN[KERN Markov kernels]
  BAL[detailed balance and reversibility]
  DENS[DENS warm-start densities]
  DISC[DISC high-accuracy theorem]
  REG[REG acceptance and support]

  C7 --> RS
  C7 --> MH
  C7 --> MC
  C7 --> COLD
  C7 --> WARM
  KERN --> BAL --> DISC
  DENS --> WARM --> DISC
  MH --> BAL
  MC --> KERN
  REG -.-> KERN
  REG -.-> BAL
```

## Chapter 8 Proximal Sampler Subtree

```mermaid
flowchart TD
  C8[Ch.8 proximal sampler]
  RGO[restricted Gaussian oracle]
  SLC[strong log-concavity]
  STR[simultaneous flow and time reversal]
  LC[log-concavity]
  FI[functional inequalities]
  IMPL[RGO implementations]
  CONV[CONV proximal geometry]
  GAUSS[GAUSS two-point kernels]
  KERN[KERN conditional law]
  DISC[DISC proximal transition]
  REG[REG oracle and support]

  C8 --> RGO
  C8 --> SLC
  C8 --> STR
  C8 --> LC
  C8 --> FI
  C8 --> IMPL
  CONV --> GAUSS --> KERN --> DISC
  RGO --> KERN
  LC --> CONV
  FI --> DISC
  REG -.-> KERN
```

## Chapter 9 Lower-Bound Subtree

```mermaid
flowchart TD
  C9[Ch.9 lower bounds]
  QUERY[query complexity model]
  ONE[one-dimensional constructions]
  CONST[constant-dimensional constructions]
  GAUSS[Gaussian lower bounds]
  ORACLE[DISC oracle interface]
  INFO[DENS information comparison]
  GROOT[GAUSS comparison lemmas]
  REG[REG model assumptions]

  C9 --> QUERY
  C9 --> ONE
  C9 --> CONST
  C9 --> GAUSS
  QUERY --> ORACLE
  ONE --> INFO
  CONST --> INFO
  GAUSS --> GROOT --> INFO
  REG -.-> ORACLE
```

## Chapter 10 Structured-Sampling Subtree

```mermaid
flowchart TD
  C10[Ch.10 structured sampling]
  SG[stochastic gradients]
  COORD[coordinate methods]
  MIRROR[mirror Langevin]
  ORACLE[MEAS noisy oracle laws]
  GEOM[CONV mirror geometry]
  GEN[SDE generator]
  DISC[DISC structured updates]
  REG[REG unbiasedness and smoothness]

  C10 --> SG
  C10 --> COORD
  C10 --> MIRROR
  SG --> ORACLE --> DISC
  COORD --> DISC
  MIRROR --> GEOM --> GEN --> DISC
  REG -.-> ORACLE
  REG -.-> GEOM
```

## Chapter 11 Non-Log-Concave Sampling Subtree

```mermaid
flowchart TD
  C11[Ch.11 non-log-concave sampling]
  STAT[approximate stationarity via FI]
  FIB[Fisher information bounds]
  APP[applications]
  LB[lower bounds]
  FI[FI score and Fisher algebra]
  SDE[SDE weak-FP]
  DISC[DISC algorithm consumers]
  REG[REG nonconvex regularity]

  C11 --> STAT
  C11 --> FIB
  C11 --> APP
  C11 --> LB
  STAT --> FI
  FIB --> FI --> SDE --> DISC
  APP --> DISC
  REG -.-> FI
  REG -.-> SDE
```

## Chapter 12 Diffusion-Generative-Models Subtree

```mermaid
flowchart TD
  C12[Ch.12 diffusion generative models]
  INTRO[introduction]
  SCORE[score matching and variants]
  DISCANA[discretization analysis]
  DENS[DENS score density]
  PATH[PATH reverse-time change of measure]
  SDE[SDE forward/reverse dynamics]
  DISC[DISC discretization theorem]
  REG[REG score and time regularity]

  C12 --> INTRO
  C12 --> SCORE
  C12 --> DISCANA
  SCORE --> DENS
  DENS --> PATH --> SDE
  SDE --> DISC
  DISCANA --> DISC
  REG -.-> DENS
  REG -.-> SDE
```


## Open Leaf Queue

| Open leaf | Label | Target file | Mathlib/external borrow plan | Status |
| --- | --- | --- | --- | --- |
| logConcaveOn_density_def | CONV/DENS | TechnicalLemmas/Geometry/LogConcavity.lean | Mathlib `ConcaveOn`, `ConcaveOn.subset`, `strictConcaveOn_log_Ioi`; AST Prekopa files for next statement style | core API, negative-log potential extraction, quasiconcavity/superlevel convexity and restriction, linear/affine precomposition, product/power/product-domain tensorization, norm-square convexity, centered/shifted/two-point quadratic Gibbs log-concavity, and Gibbs positive-rescale leaves compiled; next Prekopa/RN integration |
| prekopaLeindler_finiteDimensional | CONV/MEAS | TechnicalLemmas/Geometry/PrekopaLeindler.lean | external `AsymptoticStatistics/ForMathlib/PrekopaLeindler.lean`; Mathlib lacks direct PL package | external-port-audit |
| brunnMinkowski_oneDim_outerMeasure | CONV/MEAS | TechnicalLemmas/Geometry/BrunnMinkowski.lean | external `Brunn1D.lean`; Mathlib convex/volume APIs | external-port-audit |
| gibbsDensity_withDensity_normalized | DENS/CONV | TechnicalLemmas/Geometry/LogConcavity.lean; then TechnicalLemmas/Measure/{Gibbs,RadonNikodym}.lean | compiled `logConcaveOn_const_mul_exp_neg_of_convexOn`, log-concavity linear/affine precomposition and product/rpow/tensorization leaves, centered/shifted/two-point quadratic and one-dimensional Laplace normalized-density log-concavity, `gibbsDensityENNReal`, nonzero/finite envelope leaves, finite-measure lower-bound normalization, and `Analysis.Integrability` exact quadratic plus exact one-dimensional Laplace Lebesgue Gibbs normalizers; next generalize beyond finite-dimensional quadratic and one-dimensional Laplace tails | convex shape plus map pullbacks, product/power tensorization, centered/shifted/two-point quadratic and one-dimensional Laplace Gibbs log-concavity, Gibbs density, measurability, nonzero integral, finite-by-envelope, finite-measure lower-bound envelope, exact quadratic and exact one-dimensional Laplace Lebesgue normalizers, and normalized withDensity probability bridges compiled; general coercivity envelopes remain |
| langevinGenerator_invariant_gibbs_weak | SDE/DENS/FI | TechnicalLemmas/StochasticProcesses/Langevin.lean | compiled Langevin algebra and IBP, explicit C_c^2 core/domain agreement, normalized-Gibbs core annihilation, and the abstract integrated-semigroup-generator invariance bridge; ASTIS WeakGenerator, LangevinGenerator, and GibbsIntegral supply the interfaces | analytic core, core-domain contract, normalized core mean-zero, and abstract semigroup bridge compile; concrete Langevin semigroup construction plus extension to a semigroup-stable domain remain red before invariant Gibbs law |
| lsi_tensorization_or_preservation_contract | FI/CONV | TechnicalLemmas/FunctionalInequalities/Preservation.lean | Mathlib convex/Jensen APIs; SLT/AST reference style for functional inequality statements | planned |
| gaussianEsscher_shift_density | GAUSS/PATH | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | external `GaussianMGF.lean`, `PiWithDensity.lean`, `GaussianShift.lean` | formalized-local-density-half |
| gaussianShift_change_of_measure | GAUSS/PATH | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | external `GaussianShift.lean`; local `stdGaussianPi_withDensity_exp_shift` | formalized-local-product-measure |
| gaussianShift_euclidean_pushforward | GAUSS/PATH | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | Mathlib `EuclideanSpace`/`WithLp.toLp`; local `stdGaussianPi_shift_integral` | formalized-local-euclidean-pushforward |
| gaussianShift_stdGaussian_inner | GAUSS/PATH | TechnicalLemmas/ProbabilityDistributions/Gaussian.lean | Mathlib `map_pi_eq_stdGaussian`, `PiLp.inner_apply`, `EuclideanSpace.real_norm_sq_eq` | formalized-local-stdGaussian-inner |
| finiteGaussianGirsanov_cylinder | PATH/GAUSS | TechnicalLemmas/StochasticProcesses/Girsanov.lean | compiled `stdGaussian_shift_integral_map_toLp`; finite-dimensional cylindrical path-coordinate packaging | formalized-local-cylinder |
| finiteGaussianGirsanov_rn_density | PATH/MEAS/GAUSS | TechnicalLemmas/StochasticProcesses/Girsanov.lean | compiled `measurableEquiv_map_withDensity`, product Gaussian withDensity shift, and `map_pi_eq_stdGaussian` | formalized-local-rn-density |
| lmcInterpolation_weakGenerator | DISC/SDE/KERN | SamplingAlgorithms/LangevinMonteCarlo.lean | ASTIS LawMap/ConditionalKernel/WeakGenerator; textbook LMC interpolation as the consumer route | planned-generalization |
| renyiDensity_pointwiseDerivative | DENS/FI | TechnicalLemmas/InformationTheory/Renyi.lean | compiled `renyiIntegrand`, positivity, measurability, finite-envelope, and `HasDerivAt` rpow-product leaves; next add full divergence/log-normalization and path derivative contracts | first-leaves-compiled |
| mhKernel_detailedBalance | DISC/KERN | SamplingAlgorithms/MetropolisAdjustedLangevin.lean | Mathlib probability kernels/Markov-chain APIs if present; otherwise local kernel contracts | mathlib-search-required |

## Mathlib And External API Audit

| Area | Mathlib surface | External reference | Gap / next action |
| --- | --- | --- | --- |
| convex/log-concave base | `Analysis/Convex/*`, `ConvexOn`, `ConcaveOn`, log convexity examples | `ForMathlib/PrekopaLeindler.lean`, `Brunn1D.lean`, `Anderson.lean` | No direct Mathlib Prekopa-Leindler/Brunn-Minkowski package observed. |
| density/RN/withDensity | `Probability/Density.lean`, `Measure/Decomposition/*`, `withDensity`, `rnDeriv` | `RnDerivSqrt.lean`, `HellingerProduct.lean`, `L2.lean` | Gibbs nonzero, finite-by-envelope, finite-measure bounded-below, exact quadratic Lebesgue, and exact one-dimensional Laplace normalization contracts are compiled; need general coercivity/growth leaves proving tail-integrable envelopes. |
| Gaussian/product Gaussian | `Probability.Distributions.Gaussian.Real`, CLT/charFun support | `PiGaussian.lean`, `GaussianMGF.lean`, `GaussianShift.lean`, `PiWithDensity.lean` | Product Gaussian MGF, normalizer, shifted withDensity identity, product integral change-of-measure, EuclideanSpace pushforward bridge, and stdGaussian inner-product form are compiled; Brownian/path packaging remains. |
| conditional kernels | `Probability.Kernel.CondDistrib`, conditional expectation APIs | `CondExpL2.lean`, Markov-kernel/selection files | Need fixed representative policy for conditional drifts in algorithm proofs. |
| SDE/semigroup/Langevin | general topology/calculus/integration; no full finite-dimensional Ito/SDE library observed | ASTIS WeakGenerator/FokkerPlanckAlgebra, source-cited textbook route | Finite-dimensional cylindrical Girsanov integral and RN/withDensity identity are compiled; Ito, generator domains, invariant Gibbs proof, and full Brownian path-space change of measure remain real analytic leaves. |
| information theory | `InformationTheory/KullbackLeibler/KLFun.lean`, convexity of KL integrand | ASTIS `KLDensity`, `DonskerVaradhan`, external Hellinger/RN files | Renyi divergence and derivative identities need new local leaves. |
| algorithms | kernel/measure infrastructure; search per algorithm before local coding | AST Gaussian/conditional references and textbook algorithm proof routes | LMC/HMC/MALA/proximal trees should be consumers until shared roots compile. |

## Review Rule

Every subtree edge must eventually be one of:

- a compiled ASTIS-owned Lean declaration;
- a Mathlib theorem/API name used directly;
- an external reference theorem with a local port plan;
- a source-cited `ProofObligation` whose hidden regularity is explicit.

Do not add a chapter theorem node unless it reuses the shared roots above or
creates a new shared root with a label and reviewer contract.
