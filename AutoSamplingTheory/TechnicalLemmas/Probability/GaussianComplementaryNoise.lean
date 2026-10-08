import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Analysis.InnerProductSpace.Adjoint

/-!
# Complementary linear Gaussian noise

The law-level prerequisite for the covariance-restoration step in the pinned
OpenAI log-concave sampling compiler (`lem:compiler-absorption`) and Gaussian
momentum refresh. This is standard Gaussian calculus, not a claim of new
research mathematics or completion of either source algorithm.

Independence is encoded by the actual product measure. The covariance balance
is an explicit library premise; an application must construct and prove it.
It does not certify physical query invariance, randomized execution semantics,
conditional independence, recursive errors, or a query complexity bound.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianComplementaryNoise

variable {E F G : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
  [MeasurableSpace F] [BorelSpace F]
  [NormedAddCommGroup G] [InnerProductSpace ℝ G] [FiniteDimensional ℝ G]
  [MeasurableSpace G] [BorelSpace G]

/-- Independent standard Gaussians passed through two complementary linear
maps sum to an exact standard Gaussian. The maps may be singular and the
spaces may have dimension zero. Balance is expressed on adjoints, avoiding an
arbitrary basis or matrix representation. -/
theorem map_stdGaussian_product_of_adjoint_norm_sq
    (A : E →L[ℝ] G) (B : F →L[ℝ] G)
    (hbalance : ∀ t : G, ‖A.adjoint t‖ ^ 2 + ‖B.adjoint t‖ ^ 2 = ‖t‖ ^ 2) :
    ((stdGaussian E).prod (stdGaussian F)).map (fun p => A p.1 + B p.2) =
      stdGaussian G := by
  change ((stdGaussian E).prod (stdGaussian F)).map (A.coprod B) = _
  apply Measure.ext_of_charFun
  funext t
  rw [charFun_eq_charFunDual_toDualMap, charFunDual_map, charFunDual_prod]
  have hA : ((innerSL ℝ t).comp (A.coprod B)).comp
      (ContinuousLinearMap.inl ℝ E F) = innerSL ℝ (A.adjoint t) := by
    ext x
    simp [ContinuousLinearMap.adjoint_inner_left]
  have hB : ((innerSL ℝ t).comp (A.coprod B)).comp
      (ContinuousLinearMap.inr ℝ E F) = innerSL ℝ (B.adjoint t) := by
    ext x
    simp [ContinuousLinearMap.adjoint_inner_left]
  change charFunDual (stdGaussian E)
      (((innerSL ℝ t).comp (A.coprod B)).comp (ContinuousLinearMap.inl ℝ E F)) *
    charFunDual (stdGaussian F)
      (((innerSL ℝ t).comp (A.coprod B)).comp (ContinuousLinearMap.inr ℝ E F)) = _
  rw [hA, hB, charFunDual_stdGaussian, charFunDual_stdGaussian,
    charFun_stdGaussian, ← Complex.exp_add]
  congr 1
  simp only [innerSL_apply_norm]
  rw [← Complex.ofReal_pow, ← Complex.ofReal_pow, ← Complex.ofReal_pow]
  push_cast
  have hb := congrArg (fun x : ℝ => (x : ℂ)) (hbalance t)
  push_cast at hb
  linear_combination -hb / 2

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianComplementaryNoise
