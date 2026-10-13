import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Probability.Kernel.CompProdEqIff
import Mathlib.Probability.Kernel.Disintegration.Basic
import Mathlib.Tactic.FieldSimp

/-!
# The backward conditional kernel of a Gaussian augmentation

For an arbitrary probability input law, construct the everywhere-defined
normalized quadratic tilt and prove that it disintegrates the actual Gaussian
augmentation. The positive normalizer and joint measurability are derived, not
assumed. This fills the conditional-law step in arXiv:2609.06905v1, §2.2,
(2.7)-(2.8), and supplies the RGO law used in arXiv:2609.06906v1, §3.4.

The existing generic augmentation density is reused from its historical
ProximalBPS module. No curvature or Gibbs-density premise is needed here.
The result selects one everywhere-defined version; it does not identify an
arbitrary conditional version at every point, construct an implementable
sampler, or establish PBPS invariance, mixing, or query costs.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The normalized quadratic tilt is a measurable Markov kernel and a backward
conditional law of the actual Gaussian augmentation, for every positive noise
variance. The input law may be singular and need not have any finite moments. -/
theorem exists_tilted_isCondKernel (μ : Measure E) [IsProbabilityMeasure μ]
    {η : ℝ} (hη : 0 < η) :
    let J := Measure.map
      (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    ∃ R : Kernel E E, IsMarkovKernel R ∧
      (∀ y, R y = μ.tilted (fun x => -‖x - y‖ ^ 2 / (2 * η))) ∧
      (J.map Prod.swap).IsCondKernel R := by
  classical
  let J := Measure.map
    (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
    (μ.prod (stdGaussian E))
  let w : E → E → ℝ := fun y x => Real.exp (-‖x - y‖ ^ 2 / (2 * η))
  let Z : E → ℝ := fun y => ∫ x, w y x ∂μ
  have hw : Measurable (Function.uncurry w) := by fun_prop
  have hI (y : E) : Integrable (w y) μ := by
    refine (integrable_const (1 : ℝ)).mono' (by fun_prop) ?_
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    exact Real.exp_le_one_iff.mpr
      (div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg _)) (by positivity))
  have hZpos (y : E) : 0 < Z y := integral_exp_pos (hI y)
  have hZ : Measurable Z := hw.stronglyMeasurable.integral_prod_right.measurable
  let d : E → E → ℝ≥0∞ := fun y x => ENNReal.ofReal (w y x / Z y)
  have hd : Measurable (Function.uncurry d) :=
    (hw.div (hZ.comp measurable_fst)).ennreal_ofReal
  let R : Kernel E E := (Kernel.const E μ).withDensity d
  have hRfiber (y : E) : R y = μ.tilted (fun x => -‖x - y‖ ^ 2 / (2 * η)) := by
    rw [show R = (Kernel.const E μ).withDensity d from rfl,
      Kernel.withDensity_apply _ hd]
    rfl
  have hR : IsMarkovKernel R := ⟨fun y => by
    rw [hRfiber]
    exact isProbabilityMeasure_tilted (hI y)⟩
  let C : ℝ := ((Real.sqrt (2 * Real.pi * η))⁻¹) ^ Module.finrank ℝ E
  have hC : 0 ≤ C := by positivity
  let a : E → ℝ≥0∞ := fun y => ENNReal.ofReal (C * Z y)
  have ha : Measurable a := (measurable_const.mul hZ).ennreal_ofReal
  let ν : Measure E := volume.withDensity a
  have hJ : J.map Prod.swap = (volume.prod μ).withDensity
      (fun p : E × E => ENNReal.ofReal (C * w p.1 p.2)) := by
    dsimp only [J]
    rw [ExampleCases.ProximalBPS.GaussianAugmentation.augmentation_eq_withDensity μ η hη]
    change ((μ.prod volume).withDensity _).map
      (MeasurableEquiv.prodComm : E × E ≃ᵐ E × E) = _
    rw [Measure.RadonNikodym.measurableEquiv_map_withDensity
      (MeasurableEquiv.prodComm : E × E ≃ᵐ E × E) _ (by fun_prop)]
    change ((μ.prod volume).map Prod.swap).withDensity _ = _
    rw [Measure.prod_swap]
    congr 1
    funext p
    change ENNReal.ofReal (C * Real.exp (-‖p.1 - p.2‖ ^ 2 / (2 * η))) =
      ENNReal.ofReal (C * Real.exp (-‖p.2 - p.1‖ ^ 2 / (2 * η)))
    rw [norm_sub_rev p.1 p.2]
  have hcomp : ν ⊗ₘ R = J.map Prod.swap := by
    rw [hJ]
    change ν ⊗ₘ (Kernel.const E μ).withDensity d = _
    rw [Measure.compProd_withDensity hd, Measure.compProd_const]
    change ((volume.withDensity a).prod μ).withDensity _ = _
    rw [prod_withDensity_left ha]
    rw [← withDensity_mul _
      (show Measurable (fun p : E × E => a p.1) from ha.comp measurable_fst)
      (show Measurable (fun p : E × E => d p.1 p.2) from hd)]
    congr 1
    funext p
    change ENNReal.ofReal (C * Z p.1) * ENNReal.ofReal (w p.1 p.2 / Z p.1) = _
    rw [← ENNReal.ofReal_mul (mul_nonneg hC (hZpos p.1).le)]
    congr 1
    field_simp [(hZpos p.1).ne']
  have hf := congrArg Measure.fst hcomp
  rw [Measure.fst_compProd] at hf
  refine ⟨R, hR, hRfiber, ⟨?_⟩⟩
  rw [← hf]
  exact hcomp

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
