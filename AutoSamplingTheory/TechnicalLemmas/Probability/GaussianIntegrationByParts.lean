import Mathlib.Probability.Distributions.Gaussian.Multivariate
import AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Tactic

open MeasureTheory ProbabilityTheory
open scoped InnerProductSpace ENNReal

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianIntegrationByParts

section GaussianDensityHelpers
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private def standardWeight (x : E) : ℝ :=
  ((Real.sqrt (2 * Real.pi))⁻¹) ^ Module.finrank ℝ E * Real.exp (-‖x‖^2 / 2)

private theorem standardWeight_pos (x : E) : 0 < standardWeight x := by
  dsimp [standardWeight]
  positivity

private theorem standardGaussian_density :
    stdGaussian E = (volume : Measure E).withDensity
      (fun x => ENNReal.ofReal (standardWeight x)) := by
  have h := AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity
    (E := E) 1 (by norm_num)
  simpa only [Real.sqrt_one, one_smul, Measure.map_id', mul_one,
    standardWeight] using h

private theorem standardGaussian_weighted_integral (g : E → ℝ) :
    (∫ x, g x ∂stdGaussian E) = ∫ x, standardWeight x * g x := by
  rw [standardGaussian_density]
  rw [integral_withDensity_eq_integral_toReal_smul (by unfold standardWeight; fun_prop)
    (ae_of_all _ fun _ => ENNReal.ofReal_lt_top) g]
  apply integral_congr_ae
  filter_upwards with x
  simp only [ENNReal.toReal_ofReal (standardWeight_pos x).le, smul_eq_mul]

private theorem standardGaussian_weighted_integrable {g : E → ℝ}
    (hg : Integrable g (stdGaussian E)) :
    Integrable (fun x => standardWeight x * g x) (volume : Measure E) := by
  rw [standardGaussian_density] at hg
  have h := (integrable_withDensity_iff (by unfold standardWeight; fun_prop)
    (ae_of_all _ fun _ => ENNReal.ofReal_lt_top)).1 hg
  simpa only [ENNReal.toReal_ofReal (standardWeight_pos _).le, mul_comm] using h

private theorem standardWeight_hasFDerivAt (x : E) :
    HasFDerivAt (standardWeight : E → ℝ)
      (-(standardWeight x) • innerSL ℝ x) x := by
  let c : ℝ := ((Real.sqrt (2 * Real.pi))⁻¹) ^ Module.finrank ℝ E
  have h := (((hasFDerivAt_id x).norm_sq.const_mul (-1 / 2 : ℝ)).exp).const_mul c
  convert h using 1
  all_goals try rfl
  · funext y
    dsimp only [standardWeight, c, id]
    congr 1
    ring
  · ext v
    dsimp only [standardWeight, c, id]
    simp only [smul_apply, smul_eq_mul, innerSL_apply_apply,
      ContinuousLinearMap.comp_apply, ContinuousLinearMap.id_apply]
    have he : (-1 / 2 : ℝ) * ‖x‖^2 = -‖x‖^2 / 2 := by ring
    rw [he]
    ring

end GaussianDensityHelpers

theorem standard_gaussian_stein_of_integrable_fderiv
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (f : E → ℝ) (v : E) (hf : Differentiable ℝ f)
    (hfi : Integrable f (stdGaussian E))
    (hxf : Integrable (fun x => ⟪x,v⟫_ℝ * f x) (stdGaussian E))
    (hdf : Integrable (fun x => fderiv ℝ f x v) (stdGaussian E)) :
    (∫ x, ⟪x,v⟫_ℝ * f x ∂stdGaussian E) =
      ∫ x, fderiv ℝ f x v ∂stdGaussian E := by
  let : CompleteSpace E := FiniteDimensional.complete ℝ E
  have hDw (x : E) : fderiv ℝ (standardWeight : E → ℝ) x v =
      -standardWeight x*inner ℝ x v := by
    rw [(standardWeight_hasFDerivAt x).fderiv]
    simp only [smul_apply, smul_eq_mul, innerSL_apply_apply]
  have hwp := standardGaussian_weighted_integrable hfi
  have hwdf := standardGaussian_weighted_integrable hdf
  have hwxf := standardGaussian_weighted_integrable hxf
  have hDwf : Integrable (fun x => fderiv ℝ (standardWeight : E → ℝ) x v*f x)
      (volume : Measure E) := by
    convert hwxf.neg using 1
    ext x
    rw [hDw]
    simp only [Pi.neg_apply]
    ring
  have hparts := integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable hDwf hwdf hwp
    (fun x _ => (standardWeight_hasFDerivAt x).differentiableAt)
    (fun x _ => hf x)
  rw [standardGaussian_weighted_integral, standardGaussian_weighted_integral]
  calc
    (∫ x, standardWeight x*(inner ℝ x v*f x)) =
        -(∫ x, fderiv ℝ (standardWeight : E → ℝ) x v*f x) := by
      rw [← integral_neg]
      apply integral_congr_ae
      filter_upwards with x
      rw [hDw]
      ring
    _ = ∫ x, standardWeight x*fderiv ℝ f x v := hparts.symm

#print axioms standard_gaussian_stein_of_integrable_fderiv

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianIntegrationByParts
