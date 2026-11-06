import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Integral.Bochner.Set

/-!
# Normalized density TV and Hellinger affinity

A shared library interface on an arbitrary common measure space. The inputs
are genuine nonnegative measurable L1 densities of mass one. Event discrepancy
is exactly half the L1 difference and lies between 1-affinity and sqrt(1-a²).
No probability/finiteness assumption is made on the reference measure.
Paper consumers must derive all density conditions from their actual laws.
-/

open MeasureTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity
set_option autoImplicit false

theorem normalized_density_tv_affinity {α : Type*} [MeasurableSpace α]
    (μ : Measure α) {f g : α → ℝ}
    (hf0 : ∀ x, 0 ≤ f x) (hg0 : ∀ x, 0 ≤ g x)
    (hfm : Measurable f) (hgm : Measurable g)
    (hfi : Integrable f μ) (hgi : Integrable g μ)
    (hf1 : (∫ x, f x ∂μ) = 1) (hg1 : (∫ x, g x ∂μ) = 1) :
    let a : ℝ := ∫ x, Real.sqrt (f x * g x) ∂μ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set α, MeasurableSet B ∧
      z = |(∫ x in B, f x ∂μ) - (∫ x in B, g x ∂μ)|}
    Integrable (fun x => Real.sqrt (f x * g x)) μ ∧
    0 ≤ a ∧ a ≤ 1 ∧
    δ = (1 / 2 : ℝ) * (∫ x, |f x - g x| ∂μ) ∧
    1 - a ≤ δ ∧ δ ≤ Real.sqrt (1 - a ^ 2) := by
  classical
  dsimp only
  let F : α → ℝ := fun x => Real.sqrt (f x)
  let G : α → ℝ := fun x => Real.sqrt (g x)
  let a : ℝ := ∫ x, Real.sqrt (f x * g x) ∂μ
  let d : α → ℝ := fun x => f x - g x
  let D : Set ℝ := {z | ∃ B : Set α, MeasurableSet B ∧
    z = |(∫ x in B, f x ∂μ) - (∫ x in B, g x ∂μ)|}
  let H : ℝ := (1 / 2 : ℝ) * ∫ x, |d x| ∂μ
  have hFs (x : α) : F x ^ 2 = f x := Real.sq_sqrt (hf0 x)
  have hGs (x : α) : G x ^ 2 = g x := Real.sq_sqrt (hg0 x)
  have hF0 (x : α) : 0 ≤ F x := Real.sqrt_nonneg _
  have hG0 (x : α) : 0 ≤ G x := Real.sqrt_nonneg _
  have hF : MemLp F 2 μ :=
    (memLp_two_iff_integrable_sq (by dsimp [F]; fun_prop)).2
      (hfi.congr (Filter.Eventually.of_forall (fun x => (hFs x).symm)))
  have hG : MemLp G 2 μ :=
    (memLp_two_iff_integrable_sq (by dsimp [G]; fun_prop)).2
      (hgi.congr (Filter.Eventually.of_forall (fun x => (hGs x).symm)))
  have hmul : Integrable (fun x => F x * G x) μ := hF.integrable_mul hG
  have hprod (x : α) : Real.sqrt (f x * g x) = F x * G x :=
    Real.sqrt_mul (hf0 x) (g x)
  have hL : Integrable (fun x => Real.sqrt (f x * g x)) μ :=
    hmul.congr (Filter.Eventually.of_forall (fun x => (hprod x).symm))
  have ha : (∫ x, F x * G x ∂μ) = a := by
    exact integral_congr_ae (Filter.Eventually.of_forall (fun x => (hprod x).symm))
  have ha0 : 0 ≤ a := integral_nonneg (fun x => Real.sqrt_nonneg _)
  have ha1 : a ≤ 1 := by
    have hc := integral_mul_le_Lp_mul_Lq_of_nonneg
      (p := 2) (q := 2) (Real.holderConjugate_iff.mpr (by norm_num))
      (Filter.Eventually.of_forall hF0) (Filter.Eventually.of_forall hG0)
      (by simpa using hF) (by simpa using hG)
    simp_rw [Real.rpow_two, hFs, hGs] at hc
    rw [hf1, hg1, ha] at hc
    norm_num at hc
    exact hc
  have hdi : Integrable d μ := hfi.sub hgi
  have hd0 : (∫ x, d x ∂μ) = 0 := by
    dsimp [d]
    rw [integral_sub hfi hgi, hf1, hg1, sub_self]
  have hH0 : 0 ≤ H := mul_nonneg (by norm_num) (integral_nonneg (fun _ => abs_nonneg _))
  -- Equal total masses give the factor-one-half event bound.
  have hevent (B : Set α) (hB : MeasurableSet B) :
      |(∫ x in B, f x ∂μ) - (∫ x in B, g x ∂μ)| ≤ H := by
    rw [← integral_sub hfi.integrableOn hgi.integrableOn]
    change |∫ x in B, d x ∂μ| ≤ H
    have hs := integral_add_compl hB hdi
    rw [hd0] at hs
    have hcompl : (∫ x in Bᶜ, d x ∂μ) = -(∫ x in B, d x ∂μ) := by linarith
    have h1 := abs_integral_le_integral_abs (μ := μ.restrict B) (f := d)
    have h2 := abs_integral_le_integral_abs (μ := μ.restrict Bᶜ) (f := d)
    rw [hcompl, abs_neg] at h2
    have hsabs := integral_add_compl hB hdi.abs
    dsimp only [H]
    linarith
  have hDne : D.Nonempty := ⟨0, ∅, MeasurableSet.empty, by simp⟩
  have hDbd : BddAbove D := by
    refine ⟨H, ?_⟩
    rintro z ⟨B, hB, rfl⟩
    exact hevent B hB
  have hsup_le : sSup D ≤ H := by
    apply csSup_le hDne
    rintro z ⟨B, hB, rfl⟩
    exact hevent B hB
  -- The positive set attains half the L1 norm of the zero-mass difference.
  let B : Set α := {x | 0 ≤ d x}
  have hB : MeasurableSet B := measurableSet_le measurable_const (hfm.sub hgm)
  have hpos : (fun x => (d x)⁺) = B.indicator d := by
    funext x
    by_cases hx : 0 ≤ d x
    · simp [B, Set.indicator_of_mem, hx, PosPart.posPart]
    · simp [B, Set.indicator_of_notMem, hx, PosPart.posPart,
        max_eq_right (le_of_lt (lt_of_not_ge hx))]
  have hattain : H = ∫ x in B, d x ∂μ := by
    have he := integral_abs_eq_two_mul_integral_posPart_sub_integral hdi
    rw [hd0, hpos, integral_indicator hB] at he
    dsimp only [H]
    linarith
  have hsup_ge : H ≤ sSup D := by
    have he := le_csSup hDbd (show |(∫ x in B, f x ∂μ) - (∫ x in B, g x ∂μ)| ∈ D
      from ⟨B, hB, rfl⟩)
    rw [← integral_sub hfi.integrableOn hgi.integrableOn] at he
    change |∫ x in B, d x ∂μ| ≤ sSup D at he
    rw [← hattain, abs_of_nonneg hH0] at he
    exact he
  have htv : sSup D = H := le_antisymm hsup_le hsup_ge
  -- min(f,g) ≤ sqrt(f*g) gives the lower comparison.
  have hpoint (x : α) : f x + g x - 2 * Real.sqrt (f x * g x) ≤ |d x| := by
    dsimp only [d]
    by_cases hx : f x ≤ g x
    · rw [abs_of_nonpos (sub_nonpos.mpr hx)]
      have hh : f x ≤ Real.sqrt (f x * g x) :=
        Real.le_sqrt_of_sq_le (by nlinarith [hf0 x])
      linarith
    · rw [abs_of_nonneg (sub_nonneg.mpr (le_of_lt (lt_of_not_ge hx)))]
      have hh : g x ≤ Real.sqrt (f x * g x) :=
        Real.le_sqrt_of_sq_le (by nlinarith [hg0 x])
      linarith
  have hlower : 1 - a ≤ sSup D := by
    have hi := integral_mono ((hfi.add hgi).sub (hL.const_mul 2)) hdi.abs hpoint
    change (∫ x, f x + g x - 2 * Real.sqrt (f x * g x) ∂μ) ≤ _ at hi
    rw [integral_sub (f := fun x => f x + g x) (hfi.add hgi) (hL.const_mul 2), integral_add hfi hgi,
      integral_const_mul, hf1, hg1] at hi
    change 1 + 1 - 2 * a ≤ _ at hi
    rw [htv]
    dsimp only [H]
    linarith
  -- Cauchy-Schwarz on |sqrt f - sqrt g| and sqrt f + sqrt g.
  have hminus : MemLp (fun x => |F x - G x|) 2 μ := by
    simpa only [Real.norm_eq_abs, Pi.sub_apply] using (hF.sub hG).norm
  have hplus : MemLp (fun x => F x + G x) 2 μ := hF.add hG
  have hminusInt : (∫ x, (F x - G x) ^ 2 ∂μ) = 2 - 2 * a := by
    calc
      _ = ∫ x, (f x + g x) - 2 * (F x * G x) ∂μ := by
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun x => by nlinarith [hFs x, hGs x]
      _ = 2 - 2 * a := by
        rw [integral_sub (f := fun x => f x + g x) (hfi.add hgi) (hmul.const_mul 2), integral_add hfi hgi,
          integral_const_mul, hf1, hg1, ha]
        ring
  have hplusInt : (∫ x, (F x + G x) ^ 2 ∂μ) = 2 + 2 * a := by
    calc
      _ = ∫ x, (f x + g x) + 2 * (F x * G x) ∂μ := by
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun x => by nlinarith [hFs x, hGs x]
      _ = 2 + 2 * a := by
        rw [integral_add (f := fun x => f x + g x) (hfi.add hgi) (hmul.const_mul 2), integral_add hfi hgi,
          integral_const_mul, hf1, hg1, ha]
        ring
  have hc := integral_mul_le_Lp_mul_Lq_of_nonneg
    (p := 2) (q := 2) (Real.holderConjugate_iff.mpr (by norm_num))
    (Filter.Eventually.of_forall (fun x => abs_nonneg (F x - G x)))
    (Filter.Eventually.of_forall (fun x => add_nonneg (hF0 x) (hG0 x)))
    (by simpa using hminus) (by simpa using hplus)
  simp_rw [Real.rpow_two, sq_abs] at hc
  rw [hminusInt, hplusInt] at hc
  simp only [← Real.sqrt_eq_rpow] at hc
  have hfactor (x : α) : |d x| = |F x - G x| * (F x + G x) := by
    calc
      _ = |(F x - G x) * (F x + G x)| := by
        congr 1
        dsimp only [d]
        nlinarith [hFs x, hGs x]
      _ = _ := by rw [abs_mul, abs_of_nonneg (add_nonneg (hF0 x) (hG0 x))]
  have hroot : Real.sqrt (2 - 2 * a) * Real.sqrt (2 + 2 * a) =
      2 * Real.sqrt (1 - a ^ 2) := by
    rw [← Real.sqrt_mul (by linarith : 0 ≤ 2 - 2 * a),
      show (2 - 2 * a) * (2 + 2 * a) = 4 * (1 - a ^ 2) by ring,
      Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 4)]
    rw [show Real.sqrt (4 : ℝ) = 2 by
      convert Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 2) using 1
      norm_num]
  have hupper : sSup D ≤ Real.sqrt (1 - a ^ 2) := by
    have hi : (∫ x, |d x| ∂μ) ≤ 2 * Real.sqrt (1 - a ^ 2) := by
      simp_rw [hfactor]
      exact hc.trans_eq hroot
    rw [htv]
    dsimp only [H]
    linarith
  exact ⟨hL, ha0, ha1, htv, hlower, hupper⟩

end AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity
