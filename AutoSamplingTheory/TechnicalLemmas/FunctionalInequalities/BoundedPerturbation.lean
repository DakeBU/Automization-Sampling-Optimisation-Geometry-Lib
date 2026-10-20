import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-!
# Bounded changes of measure for entropy and logarithmic Sobolev inequalities

These canonical measure-theoretic results retain a fixed test-function class and
energy density. All entropy and energy tests are restricted to the displayed
finite-integral domain. No geometric base inequality or Sobolev extension is
inferred. The exponential perturbation factor is proved by cancellation of
the same normalization integral in the two measure comparisons.
-/

open MeasureTheory Filter

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BoundedPerturbation

noncomputable section

variable {X : Type*} [MeasurableSpace X]

noncomputable def entropy (μ : Measure X) (g : X → ℝ) : ℝ :=
  (∫ x, g x * Real.log (g x) ∂μ) - (∫ x, g x ∂μ) * Real.log (∫ x, g x ∂μ)

private def cost (s t : ℝ) : ℝ := s * Real.log (s / t) - s + t

private lemma cost_nonneg {s t : ℝ} (hs : 0 ≤ s) (ht : 0 < t) :
    0 ≤ cost s t := by
  rcases hs.eq_or_lt with rfl | hs
  · simp [cost, ht.le]
  have h := Real.log_le_sub_one_of_pos (div_pos ht hs)
  have heq : Real.log (t / s) = -Real.log (s / t) := by
    rw [Real.log_div (ne_of_gt ht) (ne_of_gt hs),
      Real.log_div (ne_of_gt hs) (ne_of_gt ht)]
    ring
  rw [heq] at h
  have hmul := mul_le_mul_of_nonneg_left h hs.le
  have hdiv : s * (t / s) = t := by field_simp
  dsimp [cost]
  nlinarith

private lemma cost_expand {s t : ℝ} (ht : 0 < t) :
    cost s t = s * Real.log s - s * Real.log t - s + t := by
  by_cases hs : s = 0
  · simp [cost, hs]
  rw [cost, Real.log_div hs (ne_of_gt ht)]
  ring

variable {X : Type*} [MeasurableSpace X]

private lemma integrable_cost {μ : Measure X} [IsProbabilityMeasure μ]
    {g : X → ℝ} (hg : Integrable g μ)
    (hlog : Integrable (fun x => g x * Real.log (g x)) μ) {t : ℝ} (ht : 0 < t) :
    Integrable (fun x => cost (g x) t) μ := by
  simp_rw [cost_expand ht]
  exact ((hlog.sub (hg.mul_const _)).sub hg).add (integrable_const _)

private lemma integral_cost {μ : Measure X} [IsProbabilityMeasure μ]
    {g : X → ℝ} (hg : Integrable g μ)
    (hlog : Integrable (fun x => g x * Real.log (g x)) μ) {t : ℝ} (ht : 0 < t) :
    (∫ x, cost (g x) t ∂μ) = entropy μ g + cost (∫ x, g x ∂μ) t := by
  simp_rw [cost_expand ht]
  rw [integral_add (f := fun x => g x * Real.log (g x) - g x * Real.log t - g x)
      (g := fun _ => t) ((hlog.sub (hg.mul_const _)).sub hg) (integrable_const _),
    integral_sub (f := fun x => g x * Real.log (g x) - g x * Real.log t)
      (g := g) (hlog.sub (hg.mul_const _)) hg,
    integral_sub (f := fun x => g x * Real.log (g x))
      (g := fun x => g x * Real.log t) hlog (hg.mul_const _), integral_mul_const]
  simp [entropy]
  ring

private theorem entropy_le_integral_cost {μ : Measure X} [IsProbabilityMeasure μ]
    {g : X → ℝ} (hg0 : 0 ≤ᵐ[μ] g) (hg : Integrable g μ)
    (hlog : Integrable (fun x => g x * Real.log (g x)) μ) {t : ℝ} (ht : 0 < t) :
    entropy μ g ≤ ∫ x, cost (g x) t ∂μ := by
  rw [integral_cost hg hlog ht]
  exact le_add_of_nonneg_right (cost_nonneg (integral_nonneg_of_ae hg0) ht)

theorem entropy_le_mul_of_measure_le {μ ν : Measure X}
    [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] {g : X → ℝ} {b : ℝ}
    (hb : 0 ≤ b) (hν : ν ≤ ENNReal.ofReal b • μ)
    (hg0 : 0 ≤ᵐ[μ] g) (hg : Integrable g μ)
    (hlog : Integrable (fun x => g x * Real.log (g x)) μ) :
    entropy ν g ≤ b * entropy μ g := by
  have hνμ : ν ≪ μ := Measure.absolutelyContinuous_of_le_smul hν
  have hgn : Integrable g ν := (hg.smul_measure ENNReal.ofReal_ne_top).mono_measure hν
  have hln : Integrable (fun x => g x * Real.log (g x)) ν :=
    (hlog.smul_measure ENNReal.ofReal_ne_top).mono_measure hν
  have hgn0 : 0 ≤ᵐ[ν] g := hνμ.ae_le hg0
  have hm0 : 0 ≤ ∫ x, g x ∂μ := integral_nonneg_of_ae hg0
  rcases hm0.eq_or_lt with hm | hm
  · have hgzero : g =ᵐ[μ] 0 := (integral_eq_zero_iff_of_nonneg_ae hg0 hg).1 hm.symm
    have hgnzero : g =ᵐ[ν] 0 := hνμ.ae_le hgzero
    have hlogzero : (fun x => g x * Real.log (g x)) =ᵐ[μ] 0 :=
      hgzero.mono fun x hx => by simp [hx]
    have hlognzero : (fun x => g x * Real.log (g x)) =ᵐ[ν] 0 :=
      hgnzero.mono fun x hx => by simp [hx]
    simp [entropy, integral_congr_ae hgzero, integral_congr_ae hgnzero,
      integral_congr_ae hlogzero, integral_congr_ae hlognzero]
  · calc
      entropy ν g ≤ ∫ x, cost (g x) (∫ y, g y ∂μ) ∂ν :=
        entropy_le_integral_cost hgn0 hgn hln hm
      _ ≤ ∫ x, cost (g x) (∫ y, g y ∂μ) ∂(ENNReal.ofReal b • μ) :=
        integral_mono_measure hν
          (by filter_upwards [Measure.ae_smul_measure hg0 (ENNReal.ofReal b)] with x hx
              exact cost_nonneg hx hm)
          ((integrable_cost hg hlog hm).smul_measure ENNReal.ofReal_ne_top)
      _ = b * entropy μ g := by
        rw [integral_smul_measure, ENNReal.toReal_ofReal hb, smul_eq_mul,
          integral_cost hg hlog hm]
        simp [cost]

/- The energy functional is held fixed while the probability law changes.
   For the usual gradient form choose Γ f = ‖∇f‖². -/
def EnergyLogSobolev (μ : Measure X) (Γ : (X → ℝ) → X → ℝ)
    (admissible : (X → ℝ) → Prop) (C : ℝ) : Prop :=
  ∀ f : X → ℝ,
    admissible f →
    Integrable (fun x => (f x) ^ 2) μ →
    Integrable (fun x => (f x) ^ 2 * Real.log ((f x) ^ 2)) μ →
    Integrable (Γ f) μ →
    (0 ≤ᵐ[μ] Γ f) →
    entropy μ (fun x => (f x) ^ 2) ≤ 2 * C * ∫ x, Γ f x ∂μ

theorem energyLogSobolev_of_measure_comparison {μ ν : Measure X}
    [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    {Γ : (X → ℝ) → X → ℝ} {admissible : (X → ℝ) → Prop} {C a b : ℝ}
    (hC : 0 ≤ C) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hμ : μ ≤ ENNReal.ofReal a • ν) (hν : ν ≤ ENNReal.ofReal b • μ)
    (hLS : EnergyLogSobolev μ Γ admissible C) :
    EnergyLogSobolev ν Γ admissible (C * a * b) := by
  intro f hfAd hf hflog hΓ hΓ0
  have hfμ := (hf.smul_measure ENNReal.ofReal_ne_top).mono_measure hμ
  have hflogμ := (hflog.smul_measure ENNReal.ofReal_ne_top).mono_measure hμ
  have hΓμ := (hΓ.smul_measure ENNReal.ofReal_ne_top).mono_measure hμ
  have hΓμ0 : 0 ≤ᵐ[μ] Γ f :=
    (Measure.absolutelyContinuous_of_le_smul hμ).ae_le hΓ0
  have hE : (∫ x, Γ f x ∂μ) ≤ a * ∫ x, Γ f x ∂ν := by
    calc
      _ ≤ ∫ x, Γ f x ∂(ENNReal.ofReal a • ν) :=
        integral_mono_measure hμ (Measure.ae_smul_measure hΓ0 _)
          (hΓ.smul_measure ENNReal.ofReal_ne_top)
      _ = _ := by rw [integral_smul_measure, ENNReal.toReal_ofReal ha, smul_eq_mul]
  calc
    entropy ν (fun x => (f x) ^ 2) ≤ b * entropy μ (fun x => (f x) ^ 2) :=
      entropy_le_mul_of_measure_le hb hν (Eventually.of_forall fun x => sq_nonneg _)
        hfμ hflogμ
    _ ≤ b * (2 * C * ∫ x, Γ f x ∂μ) :=
      mul_le_mul_of_nonneg_left (hLS f hfAd hfμ hflogμ hΓμ hΓμ0) hb
    _ ≤ b * (2 * C * (a * ∫ x, Γ f x ∂ν)) :=
      mul_le_mul_of_nonneg_left
        (mul_le_mul_of_nonneg_left hE (by positivity)) hb
    _ = 2 * (C * a * b) * ∫ x, Γ f x ∂ν := by ring

theorem energyLogSobolev_tilted {μ : Measure X} [IsProbabilityMeasure μ]
    {Γ : (X → ℝ) → X → ℝ} {admissible : (X → ℝ) → Prop} {C l u : ℝ} {B : X → ℝ}
    (hC : 0 ≤ C) (hB : AEMeasurable B μ)
    (hl : ∀ᵐ x ∂μ, l ≤ B x) (hu : ∀ᵐ x ∂μ, B x ≤ u)
    (hLS : EnergyLogSobolev μ Γ admissible C) :
    EnergyLogSobolev (μ.tilted B) Γ admissible (C * Real.exp (u - l)) := by
  have hExp : Integrable (fun x => Real.exp (B x)) μ :=
    (integrable_const (Real.exp u)).mono'
      (Real.measurable_exp.comp_aemeasurable hB).aestronglyMeasurable (by
        filter_upwards [hu] with x hx
        simpa only [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)] using Real.exp_le_exp.mpr hx)
  have := isProbabilityMeasure_tilted hExp
  let Z := ∫ x, Real.exp (B x) ∂μ
  have hZ : 0 < Z := integral_exp_pos hExp
  have hupper : μ.tilted B ≤ ENNReal.ofReal (Real.exp u / Z) • μ := by
    rw [Measure.tilted, ← withDensity_const]
    apply withDensity_mono
    filter_upwards [hu] with x hx
    exact ENNReal.ofReal_le_ofReal (div_le_div_of_nonneg_right (Real.exp_le_exp.mpr hx) hZ.le)
  have hlower : μ ≤ ENNReal.ofReal (Z / Real.exp l) • μ.tilted B := by
    calc
      μ = μ.withDensity (fun _ => 1) := withDensity_one.symm
      _ ≤ μ.withDensity (fun x => ENNReal.ofReal (Z / Real.exp l) *
          ENNReal.ofReal (Real.exp (B x) / Z)) := by
        apply withDensity_mono
        filter_upwards [hl] with x hx
        rw [← ENNReal.ofReal_mul (by positivity)]
        have heq : (Z / Real.exp l) * (Real.exp (B x) / Z) =
            Real.exp (B x) / Real.exp l := by field_simp
        rw [heq, ← ENNReal.ofReal_one]
        exact ENNReal.ofReal_le_ofReal
          ((one_le_div (Real.exp_pos _)).2 (Real.exp_le_exp.mpr hx))
      _ = ENNReal.ofReal (Z / Real.exp l) • μ.tilted B :=
        withDensity_smul' _ _ ENNReal.ofReal_ne_top
  have hconst : C * (Z / Real.exp l) * (Real.exp u / Z) = C * Real.exp (u - l) := by
    rw [Real.exp_sub]
    field_simp [ne_of_gt hZ]
  rw [← hconst]
  exact energyLogSobolev_of_measure_comparison hC (by positivity) (by positivity)
    hlower hupper hLS

end
end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BoundedPerturbation
