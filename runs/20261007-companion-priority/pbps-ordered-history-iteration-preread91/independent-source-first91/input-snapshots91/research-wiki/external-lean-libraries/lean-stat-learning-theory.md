# YuanheZ/lean-stat-learning-theory

- Public repository: https://github.com/YuanheZ/lean-stat-learning-theory
- Paper: https://arxiv.org/abs/2602.02285
- Local checkout: `/home/nitanda_sub/mark/repos/outer_repos/sampling_theory_sde/lean-stat-learning-theory`
- Current audited checkout: `d0f506f0a695018265dccb33bcb05e2f5ca1c876`
  on `main`, tagged `v4.32.0`.
- Latest verification: `git fetch --prune origin` and fast-forward on 2026-07-16
  left local `HEAD` equal to `origin/main`.  The checkout has only untracked
  `.lake/` cache files, not source edits.  The focused target
  `lake build SLT.GaussianSobolevDense.Cutoff` passed at this commit under Lean
  `v4.32.0` (3115 jobs, including rebuilt dependencies).
- Role: audited port/reference source for probability, Gaussian,
  concentration, entropy duality, log-Sobolev/Poincare, product-measure
  slicing, matrix concentration, and discretization proof style.

ASTIS keeps this project as audited port/reference memory rather than a Lake
dependency because toolchains differ.  Useful theorems become callable only
after they are copied as ASTIS-owned Lean declarations and pass the local build,
or they remain recorded in the port queue.

## Current Useful Surfaces

| SLT file/family | ASTIS use |
|---|---|
| `SLT/EfronStein.lean` | coordinate replacement under product laws, especially `map_update_prod_pi` and integral rewrites for `Function.update` |
| `SLT/GaussianLSI/SubAddEnt/Basic.lean` | product-coordinate slice integrability and AE nonnegativity patterns such as `integrable_update_slice` |
| `SLT/GaussianLSI/SubAddEnt/Subadditivity.lean` | coordinate selection maps, tower properties, and entropy subadditivity staging |
| `SLT/GaussianLSI/SubAddEnt/Decomposition.lean` | entropy telescoping/decomposition patterns for product laws |
| `SLT/GaussianLSI/Entropy.lean` and `SLT/GaussianLSI/DualEntApp.lean` | entropy, Jensen, and Gibbs-duality proof patterns |
| `SLT/GaussianMeasure.lean` | `stdGaussianPi`, coordinate laws, independence, linear MGFs, and Gaussian tail/mean identities |
| `SLT/GaussianLSI/TensorizedGLSI.lean` | `partialDeriv`, `sliceFunction`, derivative of slices, and tensorized Gaussian LSI proof architecture |
| `SLT/GaussianPoincare/*` | Rademacher/Efron-Stein/limit architecture for Gaussian Poincare |
| `SLT/GaussianSobolevDense/Defs.lean` | radial smooth cutoff definitions: the support, compact-support, smoothness, range, and pointwise-exhaustion base has been ported as ASTIS-owned declarations in `Analysis/Calculus/Cutoff.lean` |
| `SLT/GaussianSobolevDense/Cutoff.lean` | the scalar derivative bound, norm-scaling bound, strengthened one-constant-for-all-R radial first-derivative theorem, and closed outer derivative-zero leaf have been ported as ASTIS-owned declarations; ASTIS also supplies the finite-Pi derivative/trace consumer bridge; dominated cutoff limits remain reference targets before IBP |
| `SLT/GaussianPoincare/TaylorBound.lean` | compact-support derivative support/boundedness patterns: `deriv_hasCompactSupport`, `deriv2_hasCompactSupport`, `deriv_bounded_of_compactlySupported`; closest SLT staging pattern for no-boundary/IBP prerequisites |
| `SLT/MeasureInfrastructure.lean` | Chernoff, layer-cake, Jensen, finite sup/union, and integrability proof patterns |
| `SLT/HansonWright.lean`, `SLT/MatrixInfra/*`, `SLT/RMT/*`, `SLT/TDudley.lean` | later matrix concentration, empirical-process, and random-matrix proof patterns |

Immediate port candidates for the log-concave sampling tree:

- `Measure.pi` coordinate replacement: port an ASTIS-owned version of
  `map_update_prod_pi` into a focused product-measure module.
- coordinate slices: reuse the `partialDeriv`/`sliceFunction` pattern when
  formalizing product/tensorization arguments and coordinate Langevin leaves.
- Gaussian product law surface: mirror the `stdGaussianPi` and coordinate-law
  interface when strengthening ASTIS Gaussian transition kernels and LMC noise.
- entropy/Jensen surface: reuse the proof staging around `entropy_nonneg`,
  conditional entropy, and subadditivity for FI/LSI chapters.
- cutoff/no-boundary surface: the radial support/exhaustion, scale-uniform
  first-derivative, closed outer derivative-zero, finite-Pi consumer bases,
  generic `L¹` cutoff-gradient limit, and generic cutoff main-term dominated
  convergence from `Integrable` fields are now ported;
  continue using `GaussianSobolevDense/Cutoff.lean` and
  `GaussianPoincare/TaylorBound.lean` as proof-pattern memory for ASTIS-owned
  dominated-limit leaves, and for Hessian/Laplacian leaves only when a named
  second-order consumer requires them.
- Gaussian tensorization: use the LSI/Poincare files as proof architecture
  references only; no theorem is callable until ported locally.

Recommended migration order for ASTIS roots:

1. `MEAS/KERN`: product update, Fubini, and slice-integrability facts.
2. `GAUSS/MEAS`: product Gaussian law and coordinate/linear functional facts.
3. `GAUSS/FI/DENS/REG`: coordinate derivative slicing and tensorized Gaussian
   LSI proof architecture.
4. `REG/CALC/SDE`: use the compiled generic `L¹` cutoff-gradient and main-term
   dominated-convergence limits plus the concrete Gibbs/source-field integrability
   leaf, separately prove concrete Langevin generator-display integrability, and add Hessian/Laplacian facts only
   for named second-order consumers.
5. `FI/DENS/MEAS`: entropy/Jensen and Gibbs-duality infrastructure.
6. `FI/MEAS`: entropy chain rule and product subadditivity.
