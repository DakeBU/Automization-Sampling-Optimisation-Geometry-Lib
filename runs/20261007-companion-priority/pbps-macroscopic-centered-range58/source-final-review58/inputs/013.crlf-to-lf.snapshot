import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation
import Mathlib.MeasureTheory.Measure.Tilted

/-!
# The normalized Gibbs augmentation density

This source-specific integration of shared analytic and Gaussian parents
establishes the actual probability-law identification in Chen, Chewi, Lu and
Zhang, arXiv:2609.06905v1, Section 2.2, equations (2.6)-(2.7):
<https://arxiv.org/html/2609.06905v1#S2.SS2>.

The positive genuine Hessian lower bound and C² regularity imply finite positive
Gibbs mass without an assumed minimizer. The Gaussian augmentation of that Gibbs
probability then has the displayed density relative to product canonical volume.
Positive normalization and probability are explicit conclusions: a zero
totalized tilt cannot satisfy this certificate.

The source upper Hessian bound and upper scale restriction are not needed here.
Finite real inner-product spaces, including dimension zero, are explicit
generalizations. Conditional representatives, process invariance and complexity
are not conclusions. Reflection of this source law is a downstream consumer.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The Gibbs normalizer is strictly positive, its generative Gaussian
augmentation is a probability measure, and this measure has the exact normalized
source density. Integrability, positive normalization and measurable transport
are derived internally from genuine C²/Hessian hypotheses, not supplied. -/
theorem normalized_augmentation_density {V : E → ℝ} {α η : ℝ}
    (hα : 0 < α) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, α * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v)
    (hη : 0 < η) :
    let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let joint := Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    0 < ZV ∧ IsProbabilityMeasure joint ∧
      joint = ((volume : Measure E).prod volume).withDensity (fun p =>
        ENNReal.ofReal
          (((((Real.sqrt (2 * Real.pi * η))⁻¹) ^ Module.finrank ℝ E) / ZV) *
            Real.exp (-V p.1 - ‖p.2 - p.1‖ ^ 2 / (2 * η)))) := by
  let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
  let μ := (volume : Measure E).tilted (fun x => -V x)
  have hi : Integrable (fun x => Real.exp (-V x)) (volume : Measure E) :=
    TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
      hα (hV.differentiable (by norm_num))
      (TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower
        hV hH)
  have hZ : 0 < ZV := integral_exp_pos hi
  have : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hi
  have hΦ : Measurable (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2)) := by
    fun_prop
  refine ⟨hZ, Measure.isProbabilityMeasure_map hΦ.aemeasurable, ?_⟩
  change Measure.map _ (μ.prod (stdGaussian E)) = _
  rw [GaussianAugmentation.augmentation_eq_withDensity μ η hη]
  let f : E → ℝ≥0∞ := fun x => ENNReal.ofReal (Real.exp (-V x) / ZV)
  let q : E × E → ℝ≥0∞ := fun p => ENNReal.ofReal
    (((Real.sqrt (2 * Real.pi * η))⁻¹) ^ Module.finrank ℝ E *
      Real.exp (-‖p.2 - p.1‖ ^ 2 / (2 * η)))
  have hf : Measurable f := by
    exact ((Real.continuous_exp.comp hV.continuous.neg).div_const ZV).measurable.ennreal_ofReal
  have hq : Measurable q := by fun_prop
  have hfp : Measurable (fun p : E × E => f p.1) := hf.comp measurable_fst
  change (((volume : Measure E).withDensity f).prod volume).withDensity q = _
  rw [prod_withDensity_left hf, ← withDensity_mul _ hfp hq]
  congr 1
  funext p
  dsimp only [Pi.mul_apply, f, q]
  rw [← ENNReal.ofReal_mul (div_nonneg (Real.exp_pos _).le hZ.le)]
  congr 1
  rw [show -V p.1 - ‖p.2 - p.1‖ ^ 2 / (2 * η) =
      -V p.1 + (-‖p.2 - p.1‖ ^ 2 / (2 * η)) by ring, Real.exp_add]
  ring

end AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
