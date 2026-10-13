import AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym
import Mathlib.MeasureTheory.Function.SpecialFunctions.Basic

/-!
# Gibbs density leaves

Small measure-theoretic wrappers for Chewi-style Gibbs densities.  The file
connects a real potential `V` to the `ℝ≥0∞` density `ofReal (exp (-V))`;
convexity/log-concavity lives in `Geometry.LogConcavity`, while finite nonzero
normalization constants remain explicit hypotheses.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace Gibbs

open scoped ENNReal NNReal

open MeasureTheory

variable {α : Type*}

/-- The `ℝ≥0∞` density associated with an unnormalized Gibbs potential. -/
noncomputable def gibbsDensityENNReal (V : α → ℝ) : α → ℝ≥0∞ :=
  fun x => ENNReal.ofReal (Real.exp (-V x))

/-- Gibbs densities are pointwise positive. -/
theorem gibbsDensityENNReal_pos (V : α → ℝ) (x : α) :
    0 < gibbsDensityENNReal V x := by
  simpa [gibbsDensityENNReal, ENNReal.ofReal_pos] using Real.exp_pos (-V x)

/-- Gibbs densities are pointwise finite as `ℝ≥0∞` values. -/
theorem gibbsDensityENNReal_lt_top (V : α → ℝ) (x : α) :
    gibbsDensityENNReal V x < ∞ := by
  simp [gibbsDensityENNReal]

variable [MeasurableSpace α]

/-- A measurable potential gives a measurable `ℝ≥0∞` Gibbs density. -/
theorem measurable_gibbsDensityENNReal {V : α → ℝ}
    (hV : Measurable V) :
    Measurable (gibbsDensityENNReal V) := by
  unfold gibbsDensityENNReal
  exact hV.neg.exp.ennreal_ofReal

/-- An a.e.-measurable potential gives an a.e.-measurable `ℝ≥0∞` Gibbs
density. -/
theorem aemeasurable_gibbsDensityENNReal
    (μ : MeasureTheory.Measure α) {V : α → ℝ}
    (hV : AEMeasurable V μ) :
    AEMeasurable (gibbsDensityENNReal V) μ := by
  have hExp : AEMeasurable (fun x => Real.exp (-V x)) μ :=
    Real.measurable_exp.comp_aemeasurable hV.neg
  unfold gibbsDensityENNReal
  exact hExp.ennreal_ofReal

/-- Over a nonzero measure, an a.e.-measurable Gibbs density has nonzero
lintegral because it is pointwise positive. -/
theorem lintegral_gibbsDensityENNReal_ne_zero
    (μ : MeasureTheory.Measure α) [NeZero μ] {V : α → ℝ}
    (hV : AEMeasurable V μ) :
    ∫⁻ x, gibbsDensityENNReal V x ∂μ ≠ 0 := by
  intro hzero
  have hAeZero :
      (gibbsDensityENNReal V) =ᵐ[μ] 0 :=
    (lintegral_eq_zero_iff' (aemeasurable_gibbsDensityENNReal μ hV)).mp hzero
  have hbot : Filter.NeBot (ae μ) := by infer_instance
  have hFalse : ∀ᵐ x ∂μ, False :=
    hAeZero.mono fun x hx => (ne_of_gt (gibbsDensityENNReal_pos V x) hx).elim
  exact hbot.ne (Filter.eventually_false_iff_eq_bot.mp hFalse)

/-- An a.e. finite envelope gives a finite Gibbs normalization constant. -/
theorem lintegral_gibbsDensityENNReal_ne_top_of_ae_le
    (μ : MeasureTheory.Measure α) (V : α → ℝ) (g : α → ℝ≥0∞)
    (hle : ∀ᵐ x ∂μ, gibbsDensityENNReal V x ≤ g x)
    (hgfin : ∫⁻ x, g x ∂μ ≠ ∞) :
    ∫⁻ x, gibbsDensityENNReal V x ∂μ ≠ ∞ :=
  ne_top_of_le_ne_top hgfin (lintegral_mono_ae hle)

omit [MeasurableSpace α] in
/-- If a potential `V` is bounded below by `W` at a point, then the Gibbs
density of `V` is bounded above by the Gibbs density of `W` there. -/
theorem gibbsDensityENNReal_le_of_potential_ge {V W : α → ℝ} {x : α}
    (hWV : W x ≤ V x) :
    gibbsDensityENNReal V x ≤ gibbsDensityENNReal W x := by
  exact ENNReal.ofReal_le_ofReal (Real.exp_le_exp.mpr (neg_le_neg hWV))

/-- A.e. potential lower bounds give a.e. Gibbs-density envelope bounds. -/
theorem gibbsDensityENNReal_ae_le_of_ae_potential_ge
    (μ : MeasureTheory.Measure α) {V W : α → ℝ}
    (hWV : ∀ᵐ x ∂μ, W x ≤ V x) :
    ∀ᵐ x ∂μ, gibbsDensityENNReal V x ≤ gibbsDensityENNReal W x :=
  hWV.mono fun _ hx => gibbsDensityENNReal_le_of_potential_ge hx

/-- A finite Gibbs integral for a lower potential `W` is an envelope proof for
the larger potential `V`. -/
theorem lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge
    (μ : MeasureTheory.Measure α) {V W : α → ℝ}
    (hWV : ∀ᵐ x ∂μ, W x ≤ V x)
    (hWfin : ∫⁻ x, gibbsDensityENNReal W x ∂μ ≠ ∞) :
    ∫⁻ x, gibbsDensityENNReal V x ∂μ ≠ ∞ :=
  lintegral_gibbsDensityENNReal_ne_top_of_ae_le μ V (gibbsDensityENNReal W)
    (gibbsDensityENNReal_ae_le_of_ae_potential_ge μ hWV) hWfin

/-- On a finite base measure, an a.e. lower bound on the potential gives a
finite Gibbs normalization constant.  This is the compact-domain/truncated-law
envelope leaf; coercive Lebesgue tails are a stronger separate theorem. -/
theorem lintegral_gibbsDensityENNReal_ne_top_of_ae_ge_const
    (μ : MeasureTheory.Measure α) [IsFiniteMeasure μ] {V : α → ℝ} {c : ℝ}
    (hcV : ∀ᵐ x ∂μ, c ≤ V x) :
    ∫⁻ x, gibbsDensityENNReal V x ∂μ ≠ ∞ :=
  lintegral_gibbsDensityENNReal_ne_top_of_ae_le μ V
    (fun _ : α => ENNReal.ofReal (Real.exp (-c)))
    (hcV.mono fun x hx => by
      simpa [gibbsDensityENNReal] using
        gibbsDensityENNReal_le_of_potential_ge
          (V := V) (W := fun _ : α => c) (x := x) hx)
    (lintegral_const_lt_top (μ := μ)
      (c := ENNReal.ofReal (Real.exp (-c))) ENNReal.ofReal_ne_top).ne

/-- A finite nonzero Gibbs normalization constant gives a probability measure
through reciprocal-lintegral normalization and `withDensity`. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs
    (μ : MeasureTheory.Measure α) (V : α → ℝ)
    (h0 : ∫⁻ x, gibbsDensityENNReal V x ∂μ ≠ 0)
    (hfin : ∫⁻ x, gibbsDensityENNReal V x ∂μ ≠ ∞) :
    IsProbabilityMeasure
      (μ.withDensity fun x =>
        (∫⁻ y, gibbsDensityENNReal V y ∂μ)⁻¹ * gibbsDensityENNReal V x) :=
  RadonNikodym.isProbabilityMeasure_withDensity_normalized_lintegral μ
    (gibbsDensityENNReal V) h0 hfin

/-- A nonzero base measure and a finite a.e. envelope are enough to normalize a
Gibbs density into a probability measure.  This is the reusable contract that
later coercivity/growth leaves should target. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_le
    (μ : MeasureTheory.Measure α) [NeZero μ] {V : α → ℝ} (g : α → ℝ≥0∞)
    (hV : AEMeasurable V μ)
    (hle : ∀ᵐ x ∂μ, gibbsDensityENNReal V x ≤ g x)
    (hgfin : ∫⁻ x, g x ∂μ ≠ ∞) :
    IsProbabilityMeasure
      (μ.withDensity fun x =>
        (∫⁻ y, gibbsDensityENNReal V y ∂μ)⁻¹ * gibbsDensityENNReal V x) :=
  isProbabilityMeasure_withDensity_normalized_gibbs μ V
    (lintegral_gibbsDensityENNReal_ne_zero μ hV)
    (lintegral_gibbsDensityENNReal_ne_top_of_ae_le μ V g hle hgfin)

/-- A measurable potential `V` whose Gibbs density is dominated by the Gibbs
density of a lower potential `W` with finite integral normalizes to a
probability measure.  This is the first reusable potential-envelope interface
for Chewi-style coercivity/growth proofs. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_potential_ge
    (μ : MeasureTheory.Measure α) [NeZero μ] {V W : α → ℝ}
    (hV : AEMeasurable V μ)
    (hWV : ∀ᵐ x ∂μ, W x ≤ V x)
    (hWfin : ∫⁻ x, gibbsDensityENNReal W x ∂μ ≠ ∞) :
    IsProbabilityMeasure
      (μ.withDensity fun x =>
        (∫⁻ y, gibbsDensityENNReal V y ∂μ)⁻¹ * gibbsDensityENNReal V x) :=
  isProbabilityMeasure_withDensity_normalized_gibbs μ V
    (lintegral_gibbsDensityENNReal_ne_zero μ hV)
    (lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge μ hWV hWfin)

/-- On a finite nonzero base measure, an a.e. lower bound on a measurable
potential is enough to construct the normalized Gibbs probability measure. -/
theorem isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_ge_const
    (μ : MeasureTheory.Measure α) [NeZero μ] [IsFiniteMeasure μ] {V : α → ℝ} {c : ℝ}
    (hV : AEMeasurable V μ)
    (hcV : ∀ᵐ x ∂μ, c ≤ V x) :
    IsProbabilityMeasure
      (μ.withDensity fun x =>
        (∫⁻ y, gibbsDensityENNReal V y ∂μ)⁻¹ * gibbsDensityENNReal V x) :=
  isProbabilityMeasure_withDensity_normalized_gibbs μ V
    (lintegral_gibbsDensityENNReal_ne_zero μ hV)
    (lintegral_gibbsDensityENNReal_ne_top_of_ae_ge_const μ hcV)

end Gibbs
end Measure
end TechnicalLemmas
end AutoSamplingTheory
