import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Dynamics.Ergodic.MeasurePreserving
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

open Matrix MeasureTheory ProbabilityTheory Set
open scoped NNReal ENNReal
set_option autoImplicit false

/-!
# Actual Gaussian coordinate-event separation for the zero-query case

Zhou--Suzuki, arXiv:2610.20492v1, Section3.3 zero-query paragraph.
The precision matrices are I and diag(kappa,1,...,1); their actual inverse-
covariance Gaussian laws are separated by the closed first-coordinate event.
This is the analytical auxiliary, before an actual algorithm/common-law adapter.
The two spectra differ, so no disclosed-spectrum experiment is asserted.
-/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation

theorem actual_zero_query_gaussian_event_gap {d : ℕ} (hd : 1 ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) :
  let A₁ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => if i.val = 0 then κ else 1)
  let ν₀ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d))
      (1 : Matrix (Fin d) (Fin d) ℝ)⁻¹
  let ν₁ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A₁⁻¹
  let B : Set (EuclideanSpace ℝ (Fin d)) :=
    {x | |WithLp.ofLp x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ) / 2}
  (1 : ℝ) / 8 < ν₁.real B - ν₀.real B
:= by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin d)
  let i₀ : Fin d := ⟨0, hd⟩
  let eigenvalue : Fin d → ℝ := fun i => if i.val = 0 then κ else 1
  let A₁ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let ν₀ : Measure E := multivariateGaussian (0 : E) (1 : Matrix (Fin d) (Fin d) ℝ)⁻¹
  let ν₁ : Measure E := multivariateGaussian (0 : E) A₁⁻¹
  let e : E → ℝ := fun x => x i₀
  let γ : Measure ℝ := gaussianReal 0 1
  let v : ℝ≥0 := (κ⁻¹).toNNReal
  let s : Set ℝ := Icc (-(1 / 2 : ℝ)) (1 / 2)
  let t : Set ℝ := Icc (-1) 1
  let D : Set ℝ := t \ s
  have hκpos : 0 < κ := by linarith
  have heigenvaluepos (i : Fin d) : 0 < eigenvalue i := by
    dsimp [eigenvalue]
    split_ifs <;> linarith
  have hApos : A₁.PosDef := Matrix.PosDef.diagonal heigenvaluepos
  have hinv : A₁⁻¹ = Matrix.diagonal (fun i => (eigenvalue i)⁻¹) := by
    apply Matrix.inv_eq_left_inv
    change Matrix.diagonal (fun i => (eigenvalue i)⁻¹) * Matrix.diagonal eigenvalue = 1
    ext i j
    by_cases hij : i = j
    · subst j
      simp [ne_of_gt (heigenvaluepos i)]
    · simp [hij]
  have hp₀ : MeasurePreserving e ν₀ γ := by
    simpa [e, ν₀, γ] using
      (measurePreserving_eval_multivariateGaussian (μ := (0 : E))
        (S := (1 : Matrix (Fin d) (Fin d) ℝ)⁻¹)
        (by simpa using (Matrix.PosSemidef.one : (1 : Matrix (Fin d) (Fin d) ℝ).PosSemidef))
        (i := i₀))
  have hp₁ : MeasurePreserving e ν₁ (gaussianReal 0 v) := by
    simpa [e, ν₁, v, hinv, eigenvalue, i₀] using
      (measurePreserving_eval_multivariateGaussian (μ := (0 : E))
        hApos.inv.posSemidef (i := i₀))
  have hB : {x : E | |WithLp.ofLp x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ) / 2} =
      e ⁻¹' s := by
    ext x
    change |x i₀| ≤ (1 : ℝ) / 2 ↔
      -((1 : ℝ) / 2) ≤ x i₀ ∧ x i₀ ≤ (1 : ℝ) / 2
    exact abs_le
  have hm₀ : ν₀.real (e ⁻¹' s) = γ.real s :=
    hp₀.measureReal_preimage measurableSet_Icc.nullMeasurableSet
  have hm₁ : ν₁.real (e ⁻¹' s) = (gaussianReal 0 v).real s :=
    hp₁.measureReal_preimage measurableSet_Icc.nullMeasurableSet
  have hinvpos : 0 < κ⁻¹ := inv_pos.mpr hκpos
  let c : ℝ := Real.sqrt (κ⁻¹)
  have hc0 : 0 ≤ c := Real.sqrt_nonneg _
  have hcsq : c ^ 2 = κ⁻¹ := Real.sq_sqrt hinvpos.le
  have hinvsmall : κ⁻¹ ≤ 1 / 4 := by
    have hmul : κ * κ⁻¹ = 1 := mul_inv_cancel₀ (ne_of_gt hκpos)
    nlinarith [mul_nonneg (sub_nonneg.mpr hκ) hinvpos.le]
  have hcsmall : c ≤ 1 / 2 := by nlinarith
  have hscale : γ.map (fun x => c * x) = gaussianReal 0 v := by
    dsimp only [γ]
    rw [gaussianReal_map_const_mul]
    simp only [mul_zero, mul_one]
    congr 1
    apply NNReal.eq
    simpa only [v, NNReal.coe_mk, Real.coe_toNNReal _ hinvpos.le] using hcsq
  have hsubset : t ⊆ (fun x : ℝ => c * x) ⁻¹' s := by
    intro x hx
    change -1 ≤ x ∧ x ≤ 1 at hx
    change -(1 / 2 : ℝ) ≤ c * x ∧ c * x ≤ 1 / 2
    constructor
    · nlinarith [mul_nonneg hc0 (by linarith : 0 ≤ x + 1)]
    · nlinarith [mul_nonneg hc0 (by linarith : 0 ≤ 1 - x)]
  have hmass : γ.real t ≤ (gaussianReal 0 v).real s := by
    rw [← hscale, map_measureReal_apply (by fun_prop) measurableSet_Icc]
    exact measureReal_mono hsubset
  have hst : s ⊆ t := by
    intro x hx
    change -(1 / 2 : ℝ) ≤ x ∧ x ≤ 1 / 2 at hx
    exact ⟨by linarith, by linarith⟩
  have hDmeas : MeasurableSet D := measurableSet_Icc.diff measurableSet_Icc
  have htfinite : volume t ≠ ⊤ := by
    simp [t, Real.volume_Icc]
  have hDfinite : volume D ≠ ⊤ :=
    measure_ne_top_of_subset (sdiff_subset : D ⊆ t) htfinite
  have hDvol : volume.real D = 1 := by
    dsimp only [D]
    rw [measureReal_sdiff hst measurableSet_Icc htfinite]
    norm_num [s, t, Real.volume_real_Icc]
  let a : ℝ := (Real.sqrt (2 * Real.pi) * Real.exp (1 / 2))⁻¹
  have hsqrtpos : 0 < Real.sqrt (2 * Real.pi) := Real.sqrt_pos.mpr (by positivity)
  have hsqrtsq : Real.sqrt (2 * Real.pi) ^ 2 = 2 * Real.pi :=
    Real.sq_sqrt (by positivity)
  have hsqrtlt : Real.sqrt (2 * Real.pi) < 4 := by nlinarith [Real.pi_lt_four]
  have hepos : 0 < Real.exp (1 / 2 : ℝ) := Real.exp_pos _
  have hesq : Real.exp (1 / 2 : ℝ) ^ 2 = Real.exp 1 := by
    rw [pow_two, ← Real.exp_add]
    norm_num
  have helt : Real.exp (1 / 2 : ℝ) < 2 := by nlinarith [Real.exp_one_lt_three]
  have hprodpos : 0 < Real.sqrt (2 * Real.pi) * Real.exp (1 / 2) :=
    mul_pos hsqrtpos hepos
  have hprodlt : Real.sqrt (2 * Real.pi) * Real.exp (1 / 2) < 8 := by
    calc
      _ < 4 * Real.exp (1 / 2) := mul_lt_mul_of_pos_right hsqrtlt hepos
      _ < 4 * 2 := mul_lt_mul_of_pos_left helt (by norm_num)
      _ = 8 := by norm_num
  have hnum : (1 : ℝ) / 8 < a := by
    have h : (1 : ℝ) / 8 < 1 / (Real.sqrt (2 * Real.pi) * Real.exp (1 / 2)) :=
      (lt_div_iff₀ hprodpos).mpr (by nlinarith)
    simpa only [a, one_div] using h
  have haform : a = (Real.sqrt (2 * Real.pi))⁻¹ * Real.exp (-(1 / 2 : ℝ)) := by
    simp only [a, mul_inv, Real.exp_neg]
  have hpdf (x : ℝ) (hx : x ∈ D) : a ≤ gaussianPDFReal 0 1 x := by
    have hxt : -1 ≤ x ∧ x ≤ 1 := hx.1
    have hxsq : x ^ 2 ≤ 1 := by
      nlinarith [mul_nonneg (by linarith : 0 ≤ 1 - x) (by linarith : 0 ≤ 1 + x)]
    rw [haform]
    simp only [gaussianPDFReal, NNReal.coe_one, mul_one, sub_zero]
    apply mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr (by nlinarith))
    exact inv_nonneg.mpr (Real.sqrt_nonneg _)
  have hint : a ≤ ∫ x in D, gaussianPDFReal 0 1 x := by
    have h := setIntegral_mono_on (integrableOn_const hDfinite)
      (integrable_gaussianPDFReal 0 1).restrict hDmeas hpdf
    simpa only [setIntegral_const, hDvol, smul_eq_mul, one_mul] using h
  have hγD : a ≤ γ.real D := by
    have hnonneg : 0 ≤ ∫ x in D, gaussianPDFReal 0 1 x :=
      integral_nonneg (gaussianPDFReal_nonneg 0 1)
    dsimp only [γ, Measure.real]
    rw [gaussianReal_apply_eq_integral 0 (by norm_num : (1 : ℝ≥0) ≠ 0) D,
      ENNReal.toReal_ofReal hnonneg]
    exact hint
  have hdiff : γ.real D = γ.real t - γ.real s :=
    measureReal_sdiff hst measurableSet_Icc
  change (1 : ℝ) / 8 < ν₁.real {x : E | |WithLp.ofLp x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ) / 2} -
    ν₀.real {x : E | |WithLp.ofLp x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ) / 2}
  rw [hB, hm₀, hm₁]
  linarith

end AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation
