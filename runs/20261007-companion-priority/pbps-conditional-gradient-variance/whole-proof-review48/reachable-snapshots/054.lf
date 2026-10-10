import AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-!
# Gibbs withDensity integral rewrites

This file contains Bochner-integral bridges for Chewi-style Gibbs
`withDensity` measures.  The leaves here do not prove stationarity,
reversibility, normalization, or integrability of a potential.  They only
rewrite Bochner integrals against a Gibbs `withDensity` measure back to
weighted integrals against the base measure.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace GibbsIntegral

open scoped ENNReal NNReal

open MeasureTheory

variable {α F : Type*} [MeasurableSpace α] [NormedAddCommGroup F] [NormedSpace ℝ F]

/-- Bochner integrals against a Gibbs `withDensity` measure rewrite to a
base-measure integral weighted by the real Gibbs density.

The only scalar hypothesis needed for this algebraic rewrite is `Z ≠ 0`, which
keeps the `ℝ≥0∞` density `Z⁻¹ * exp(-V)` finite.  Finiteness of the normalizing
integral and probability-measure normalization are separate Gibbs leaves. -/
theorem integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul
    (μ : Measure α) {V : α → ℝ} (hV : AEMeasurable V μ)
    {Z : ℝ≥0∞} (hZ0 : Z ≠ 0) (g : α → F) :
    ∫ x, g x ∂μ.withDensity (fun x => Z⁻¹ * Measure.Gibbs.gibbsDensityENNReal V x) =
      ∫ x, (Z.toReal⁻¹ * Real.exp (-V x)) • g x ∂μ := by
  let f : α → ℝ≥0∞ := fun x => Z⁻¹ * Measure.Gibbs.gibbsDensityENNReal V x
  have hf_meas : AEMeasurable f μ := by
    exact AEMeasurable.const_mul
      (Measure.Gibbs.aemeasurable_gibbsDensityENNReal μ hV) Z⁻¹
  have hf_top : ∀ᵐ x ∂μ, f x < ∞ := by
    filter_upwards with x
    have hZpos : 0 < Z := bot_lt_iff_ne_bot.mpr hZ0
    have hZinv_lt_top : Z⁻¹ < ∞ := ENNReal.inv_lt_top.mpr hZpos
    have hg_lt_top : Measure.Gibbs.gibbsDensityENNReal V x < ∞ :=
      Measure.Gibbs.gibbsDensityENNReal_lt_top V x
    exact ENNReal.mul_lt_top hZinv_lt_top hg_lt_top
  rw [integral_withDensity_eq_integral_toReal_smul₀ hf_meas hf_top]
  apply integral_congr_ae
  filter_upwards with x
  simp [f, Measure.Gibbs.gibbsDensityENNReal, ENNReal.toReal_mul, ENNReal.toReal_inv,
    ENNReal.toReal_ofReal (Real.exp_nonneg _)]

/-- Source-facing specialization of the Gibbs integral rewrite where the scalar
is the Gibbs lintegral.  The finite-normalizer proof, when needed to obtain a
probability measure, remains a separate input to the probability-measure leaf. -/
theorem integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul
    (μ : Measure α) {V : α → ℝ} (hV : AEMeasurable V μ)
    (hZ0 : ∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂μ ≠ 0) (g : α → F) :
    ∫ x, g x ∂μ.withDensity
        (fun x =>
          (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂μ)⁻¹ *
            Measure.Gibbs.gibbsDensityENNReal V x) =
      ∫ x,
        ((∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂μ).toReal⁻¹ *
          Real.exp (-V x)) • g x ∂μ :=
  integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul
    μ hV hZ0 g

/-- Nonzero-base-measure specialization of the source-facing Gibbs integral
rewrite.  It discharges the nonzero Gibbs normalizer from positivity of
`exp (-V)` and `[NeZero μ]`.

This remains only a Bochner-integral rewrite.  If a later theorem needs a
probability measure, it must also supply the finite-normalizer hypothesis to
the separate Gibbs probability leaf. -/
theorem integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul_of_neZero
    (μ : Measure α) [NeZero μ] {V : α → ℝ} (hV : AEMeasurable V μ) (g : α → F) :
    ∫ x, g x ∂μ.withDensity
        (fun x =>
          (∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂μ)⁻¹ *
            Measure.Gibbs.gibbsDensityENNReal V x) =
      ∫ x,
        ((∫⁻ y, Measure.Gibbs.gibbsDensityENNReal V y ∂μ).toReal⁻¹ *
          Real.exp (-V x)) • g x ∂μ :=
  integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul
    μ hV (Measure.Gibbs.lintegral_gibbsDensityENNReal_ne_zero μ hV) g

end GibbsIntegral
end Measure
end TechnicalLemmas
end AutoSamplingTheory
