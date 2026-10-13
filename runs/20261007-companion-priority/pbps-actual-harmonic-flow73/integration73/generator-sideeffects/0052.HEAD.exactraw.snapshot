# AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity

- File: `AutoSamplingTheory/TechnicalLemmas/Geometry/LogConcavity.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: positive-function log-concavity API over Mathlib ConcaveOn; negative-log potential convexity and energy sublevels; quasiconcavity, convex superlevel sets, and restricted superlevel log-concavity; linear/affine precomposition; products, nonnegative powers, product-domain tensorization; norm-square, absolute-linear, and centered/shifted/two-point quadratic-potential convexity; explicit normalized quadratic, Laplace, and Gaussian-kernel log-concavity
- Mathlib-quality status: compiled CONV/DENS leaf with density-to-potential extraction, level-set/restriction geometry, map-stability, algebra, one-dimensional Laplace geometry, and centered/shifted/two-point quadratic Gibbs geometry; extend toward Prekopa-Leindler interfaces

## Imports

- `Mathlib.Analysis.Convex.SpecificFunctions.Basic`
- `Mathlib.Analysis.Convex.Quasiconvex`
- `Mathlib.Analysis.Normed.Module.Convex`
- `Mathlib.Analysis.SpecialFunctions.Pow.Real`
- `Mathlib.LinearAlgebra.FiniteDimensional.Defs`

## Representative Declarations And Exports

- `LogConcaveOn`
- `logConcaveOn_iff`
- `logConcaveOn_of_concave_log`
- `LogConcaveOn.pos`
- `LogConcaveOn.concaveOn_log`
- `LogConcaveOn.convexOn_neg_log`
- `LogConcaveOn.convex_sublevel_neg_log`
- `LogConcaveOn.convex_domain`
- `LogConcaveOn.convex_superlevel`
- `LogConcaveOn.quasiconcaveOn`
- `LogConcaveOn.subset`
- `LogConcaveOn.restrict_superlevel`
- `LogConcaveOn.comp_linearMap`
- `LogConcaveOn.comp_affineMap`
- `LogConcaveOn.mul`
- `LogConcaveOn.rpow`
- `LogConcaveOn.prod`
- `LogConcaveOn.const_mul`
- `logConcaveOn_const`
- `logConcaveOn_exp_neg_of_convexOn`
- `logConcaveOn_const_mul_exp_neg_of_convexOn`
- `convexOn_univ_abs`
- `convexOn_univ_const_mul_abs_add`
- `logConcaveOn_exp_neg_abs_linear`
- `logConcaveOn_const_mul_exp_neg_abs_linear`
- `logConcaveOn_explicit_abs_linear_normalized_density`
- `convexOn_univ_norm_sq`
- `convexOn_univ_const_mul_norm_sq_add`
- `logConcaveOn_exp_neg_quadratic_norm`
- `logConcaveOn_const_mul_exp_neg_quadratic_norm`
- `logConcaveOn_explicit_quadratic_normalized_density`
- `convexOn_univ_const_mul_norm_sub_sq_add`
- `logConcaveOn_exp_neg_shifted_quadratic_norm`
- `logConcaveOn_const_mul_exp_neg_shifted_quadratic_norm`
- `logConcaveOn_explicit_shifted_quadratic_normalized_density`
- `convexOn_univ_const_mul_norm_fst_sub_snd_sq_add`
- `logConcaveOn_exp_neg_pair_sub_quadratic_norm`
- `logConcaveOn_const_mul_exp_neg_pair_sub_quadratic_norm`
- `logConcaveOn_explicit_pair_sub_quadratic_kernel`
- `logConcaveOn_id_Ioi`

## Curated Formalized Memory Entries

- `geometry.log-concavity.def` -> `LogConcaveOn` (Mathlib.Analysis.Convex.Function; Mathlib.Analysis.Convex.SpecificFunctions.Basic)
- `geometry.log-concavity.negative-log-potential-convex` -> `convexOn_neg_log` (Mathlib.Analysis.Convex.Function)
- `geometry.log-concavity.negative-log-potential-sublevel-convex` -> `convex_sublevel_neg_log` (Mathlib.Analysis.Convex.Quasiconvex; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.log-concavity.positive-ray-id` -> `logConcaveOn_id_Ioi` (Mathlib.Analysis.Convex.SpecificFunctions.Basic)
- `geometry.log-concavity.linear-precomposition` -> `comp_linearMap` (Mathlib.Analysis.Convex.Function)
- `geometry.log-concavity.affine-precomposition` -> `comp_affineMap` (Mathlib.Analysis.Convex.Function)
- `geometry.log-concavity.convex-superlevel` -> `convex_superlevel` (Mathlib.Analysis.Convex.Quasiconvex; Mathlib.Analysis.SpecialFunctions.Log.Basic)
- `geometry.log-concavity.quasiconcave` -> `quasiconcaveOn` (Mathlib.Analysis.Convex.Quasiconvex; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.log-concavity.restrict-superlevel` -> `restrict_superlevel` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.log-concavity.positive-rescale` -> `const_mul` (Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic)
- `geometry.log-concavity.pointwise-product` -> `mul` (Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic)
- `geometry.log-concavity.nonnegative-rpow` -> `rpow` (Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Pow.Real)
- `geometry.log-concavity.product-domain-product` -> `prod` (Mathlib.Analysis.Convex.Basic; Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic)
- `geometry.gibbs-density.convex-potential` -> `logConcaveOn_const_mul_exp_neg_of_convexOn` (Mathlib.Analysis.Convex.Function; Mathlib.Analysis.SpecialFunctions.Log.Basic)
- `geometry.convexity.absolute-value` -> `convexOn_univ_abs` (Mathlib.Analysis.Normed.Module.Convex)
- `geometry.convexity.absolute-linear-potential` -> `convexOn_univ_const_mul_abs_add` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.absolute-linear-potential-logconcave` -> `logConcaveOn_exp_neg_abs_linear` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.absolute-linear-positive-rescale-logconcave` -> `logConcaveOn_const_mul_exp_neg_abs_linear` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.explicit-laplace-normalized-logconcave` -> `logConcaveOn_explicit_abs_linear_normalized_density` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.convexity.norm-square` -> `convexOn_univ_norm_sq` (Mathlib.Analysis.Normed.Group.Basic; Mathlib.Analysis.Normed.MulAction; Mathlib.Algebra.Order.GroupWithZero.Unbundled.Basic)
- `geometry.convexity.quadratic-norm-potential` -> `convexOn_univ_const_mul_norm_sq_add` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.Convex.Function)
- `geometry.gibbs-density.quadratic-potential-logconcave` -> `logConcaveOn_exp_neg_quadratic_norm` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.quadratic-positive-rescale-logconcave` -> `logConcaveOn_const_mul_exp_neg_quadratic_norm` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.explicit-quadratic-normalized-logconcave` -> `logConcaveOn_explicit_quadratic_normalized_density` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.SpecialFunctions.Pow.Real)
- `geometry.convexity.shifted-quadratic-norm-potential` -> `convexOn_univ_const_mul_norm_sub_sq_add` (Mathlib.Analysis.Convex.Function; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.shifted-quadratic-potential-logconcave` -> `logConcaveOn_exp_neg_shifted_quadratic_norm` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.shifted-quadratic-positive-rescale-logconcave` -> `logConcaveOn_const_mul_exp_neg_shifted_quadratic_norm` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.explicit-shifted-quadratic-normalized-logconcave` -> `logConcaveOn_explicit_shifted_quadratic_normalized_density` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.SpecialFunctions.Pow.Real)
- `geometry.convexity.pair-sub-quadratic-kernel-potential` -> `convexOn_univ_const_mul_norm_fst_sub_snd_sq_add` (Mathlib.Analysis.Convex.Function; AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.pair-sub-quadratic-kernel-logconcave` -> `logConcaveOn_exp_neg_pair_sub_quadratic_norm` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.pair-sub-quadratic-kernel-positive-rescale-logconcave` -> `logConcaveOn_const_mul_exp_neg_pair_sub_quadratic_norm` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity)
- `geometry.gibbs-density.explicit-pair-sub-quadratic-kernel-logconcave` -> `logConcaveOn_explicit_pair_sub_quadratic_kernel` (AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity; Mathlib.Analysis.SpecialFunctions.Pow.Real)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
