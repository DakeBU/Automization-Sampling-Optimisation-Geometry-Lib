import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
import AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
import AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Integral.Prod

/-!
# Actual PBPS phase Gibbs normalization

An explicit completion of the proportionality in arXiv:2609.06905v1, Eq. (3.1).
The six original analytic assumptions imply a positive finite phase partition
and identify its normalized density with the conditional position Gibbs law
times standard Gaussian momentum. All finite dimensions, including zero, are
covered. This is no process-invariance, error or oracle-cost theorem.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

set_option linter.unusedVariables false in
private def actual_phase_normalization_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop := by
  classical
  exact
    let d : ℕ := Module.finrank ℝ E
    let Vy : E → E → ℝ := fun y x => V x + ‖x - y‖ ^ 2 / (2 * η)
    let U : E → E × E → ℝ := fun y z =>
      V z.1 + ‖z.1 - y‖ ^ 2 / (2 * η) + ‖z.2‖ ^ 2 / 2
    let w : E → E × E → ℝ := fun y z => Real.exp (-U y z)
    let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
    let Zx : E → ℝ := fun y => ∫ x : E, Real.exp (-Vy y x) ∂volume
    let C : ℝ := (Real.sqrt (2 * Real.pi)) ^ d
    let Zphase : E → ℝ≥0∞ := fun y => ∫⁻ z, ENNReal.ofReal (w y z) ∂ell
    let piY : E → Measure E := fun y => (volume : Measure E).tilted (fun x => -Vy y x)
    let nu : E → Measure (E × E) := fun y =>
      ell.withDensity (fun z => (Zphase y)⁻¹ * ENNReal.ofReal (w y z))
    let gamma : Measure E := ProbabilityTheory.stdGaussian E
    ∀ y : E,
      Integrable (fun x => Real.exp (-Vy y x)) (volume : Measure E) ∧
      0 < Zx y ∧
      Zphase y = ENNReal.ofReal (Zx y * C) ∧
      0 < Zphase y ∧
      Zphase y < ⊤ ∧
      IsProbabilityMeasure (nu y) ∧
      nu y = (piY y).prod gamma


/-- Positive finite normalization and exact product-law identification for the
actual target phase energy. Integrability and all density identities are
derived internally; no normalizer or minimizer is an additional hypothesis. -/
theorem actual_phase_gibbs_normalization
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_phase_normalization_statement hα hαβ hV hH hη hβη := by

  dsimp only [actual_phase_normalization_statement]
  intro y
  let Vy : E → ℝ := fun x => V x + ‖x - y‖ ^ 2 / (2 * η)
  let U : E × E → ℝ := fun z => V z.1 + ‖z.1 - y‖ ^ 2 / (2 * η) + ‖z.2‖ ^ 2 / 2
  let f : E → ℝ := fun x => Real.exp (-Vy x)
  let g : E → ℝ := fun p => Real.exp (-‖p‖ ^ 2 / 2)
  let C : ℝ := (Real.sqrt (2 * Real.pi)) ^ Module.finrank ℝ E
  let Z : ℝ := ∫ x, f x ∂(volume : Measure E)
  let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
  let Zp : ℝ≥0∞ := ∫⁻ z, ENNReal.ofReal (Real.exp (-U z)) ∂ell
  change Integrable f volume ∧ 0 < Z ∧ Zp = ENNReal.ofReal (Z * C) ∧
    0 < Zp ∧ Zp < ⊤ ∧
    IsProbabilityMeasure (ell.withDensity (fun z => Zp⁻¹ * ENNReal.ofReal (Real.exp (-U z)))) ∧
    ell.withDensity (fun z => Zp⁻¹ * ENNReal.ofReal (Real.exp (-U z))) =
      ((volume : Measure E).tilted (fun x => -Vy x)).prod (stdGaussian E)
  have hsc := AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV (fun x v => (hH x v).1)
  have hbase := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn hα (hV.differentiable (by norm_num)) hsc
  have hVy : Continuous Vy := hV.continuous.add (((continuous_id.sub continuous_const).norm.pow 2).div_const (2 * η))
  have hfc : Continuous f := Real.continuous_exp.comp hVy.neg
  have hgc : Continuous g := Real.continuous_exp.comp ((continuous_norm.pow 2).neg.div_const 2)
  have hf : Integrable f (volume : Measure E) := by
    refine hbase.mono' hfc.aestronglyMeasurable ?_
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    apply Real.exp_le_exp.mpr
    dsimp [Vy]
    have : 0 ≤ ‖x - y‖ ^ 2 / (2 * η) := by positivity
    linarith
  have hZ : 0 < Z := integral_exp_pos hf
  have hC : 0 < C := by dsimp [C]; positivity
  have hCg : (∫⁻ p : E, ENNReal.ofReal (g p) ∂volume) = ENNReal.ofReal C := by
    have h := AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_mul_norm_sq_eq (E := E) (a := (1 / 2 : ℝ)) (by norm_num)
    have hn : (Real.pi / (1 / 2 : ℝ)) ^ ((Module.finrank ℝ E : ℝ) / 2) = C := by
      dsimp [C]
      rw [Real.sqrt_eq_rpow, ← Real.rpow_mul_natCast (by positivity)]
      congr 1 <;> ring
    rw [hn] at h
    convert h using 1
    congr 1
    funext p
    congr 2
    dsimp [g]
    ring
  have hw (z : E × E) : Real.exp (-U z) = f z.1 * g z.2 := by
    dsimp [U, f, g, Vy]
    rw [← Real.exp_add]
    congr 1
    ring
  have hphase : Zp = ENNReal.ofReal (Z * C) := by
    calc
      Zp = ∫⁻ z : E × E, ENNReal.ofReal (f z.1) * ENNReal.ofReal (g z.2) ∂ell := by
        apply lintegral_congr
        intro z
        rw [hw, ENNReal.ofReal_mul (Real.exp_nonneg _)]
      _ = (∫⁻ x : E, ENNReal.ofReal (f x) ∂volume) * ∫⁻ p : E, ENNReal.ofReal (g p) ∂volume :=
        lintegral_prod_mul hfc.measurable.ennreal_ofReal.aemeasurable hgc.measurable.ennreal_ofReal.aemeasurable
      _ = ENNReal.ofReal (Z * C) := by
        rw [← ofReal_integral_eq_lintegral_ofReal hf (ae_of_all _ (fun x => Real.exp_nonneg _)), hCg, ← ENNReal.ofReal_mul hZ.le]
  have hpos : 0 < Zp := by rw [hphase]; exact ENNReal.ofReal_pos.mpr (mul_pos hZ hC)
  have hfin : Zp < ⊤ := by rw [hphase]; exact ENNReal.ofReal_lt_top
  have hprob : IsProbabilityMeasure (ell.withDensity (fun z => Zp⁻¹ * ENNReal.ofReal (Real.exp (-U z)))) :=
    AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs ell U hpos.ne' hfin.ne
  refine ⟨hf, hZ, hphase, hpos, hfin, hprob, ?_⟩
  have hgamma : stdGaussian E = (volume : Measure E).withDensity (fun p => ENNReal.ofReal (C⁻¹ * g p)) := by
    have h := AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity (E := E) 1 (by norm_num)
    have hid : (fun z : E => Real.sqrt 1 • z) = id := by funext z; simp
    rw [hid, Measure.map_id] at h
    simpa only [mul_one, inv_pow, C, g] using h
  rw [hgamma, Measure.tilted, prod_withDensity ((hfc.measurable.div_const Z).ennreal_ofReal) ((hgc.measurable.const_mul C⁻¹).ennreal_ofReal)]
  apply withDensity_congr_ae
  filter_upwards with z
  rw [hphase, hw, ENNReal.ofReal_mul hZ.le, ENNReal.ofReal_mul (Real.exp_nonneg _), ENNReal.ofReal_div_of_pos hZ, ENNReal.ofReal_mul (inv_nonneg.mpr hC.le), ENNReal.ofReal_inv_of_pos hC]
  rw [ENNReal.mul_inv (Or.inr ENNReal.ofReal_ne_top) (Or.inl ENNReal.ofReal_ne_top)]
  simp only [div_eq_mul_inv, f]
  ac_rfl

#print axioms actual_phase_gibbs_normalization
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization
