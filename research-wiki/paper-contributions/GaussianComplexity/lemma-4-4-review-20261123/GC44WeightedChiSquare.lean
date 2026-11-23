import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence
import Mathlib.Probability.Moments.Basic
import Mathlib.Tactic

/-! Scalar Bernstein concentration for signed weighted Gaussian squares, including arbitrary
unit projections of the independent physical rows of the source experiment. -/

open MeasureTheory ProbabilityTheory Real
open scoped BigOperators NNReal
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.WeightedChiSquare

/-- Exact MGF on its finite domain, including the full negative half-line. -/
theorem gaussian_centered_square_mgf {s : ℝ} (hs : s < 1/2) :
    (∫ x : ℝ, exp (s*(x^2-1)) ∂gaussianReal 0 1) =
      exp (-s) / Real.sqrt (1-2*s) := by
  have hc : 0 < 1-2*s := by linarith
  have hp := Real.pi_pos
  rw [integral_gaussianReal_eq_integral_smul (by norm_num : (1 : ℝ≥0) ≠ 0)]
  simp only [smul_eq_mul]
  have hrewrite (x : ℝ) : gaussianPDFReal 0 1 x * exp (s*(x^2-1)) =
      ((Real.sqrt (2*Real.pi))⁻¹ * exp (-s)) * exp (-((1-2*s)/2)*x^2) := by
    simp only [gaussianPDFReal, NNReal.coe_one, mul_one, sub_zero]
    rw [mul_assoc, ← Real.exp_add, mul_assoc, ← Real.exp_add]
    congr 2
    ring
  simp_rw [hrewrite]
  rw [integral_const_mul, integral_gaussian]
  have harg : Real.pi / ((1-2*s)/2) = (2*Real.pi)/(1-2*s) := by rw [div_div_eq_mul_div]; ring
  rw [harg, Real.sqrt_div (by positivity)]
  field_simp [Real.sqrt_ne_zero'.mpr (by positivity : 0 < 2*Real.pi), Real.sqrt_ne_zero'.mpr hc]

private theorem one_mgf_bound {s : ℝ} (hs : |s| ≤ 1/4) :
    (∫ x : ℝ, exp (s*(x^2-1)) ∂gaussianReal 0 1) ≤ exp (4*s^2) := by
  have h1 := (abs_le.mp hs).2
  have hpos : 0 < 1-2*s := by linarith
  rw [gaussian_centered_square_mgf (by linarith)]
  apply (Real.log_le_log_iff (div_pos (Real.exp_pos _) (Real.sqrt_pos.2 hpos)) (Real.exp_pos _)).mp
  rw [Real.log_div (Real.exp_ne_zero _) (Real.sqrt_ne_zero'.mpr hpos), Real.log_exp,
    Real.log_sqrt hpos.le, Real.log_exp]
  have hl := Real.one_sub_inv_le_log_of_pos hpos
  have hrat : -s - (1-(1-2*s)⁻¹)/2 = 2*s^2/(1-2*s) := by
    apply (eq_div_iff hpos.ne').mpr
    nlinarith only [inv_mul_cancel₀ hpos.ne']
  have hbound : 2*s^2/(1-2*s) ≤ 4*s^2 := by
    apply (div_le_iff₀ hpos).mpr
    nlinarith only [mul_nonneg (sq_nonneg s) (show 0 ≤ 1-4*s by linarith)]
  linarith

variable {Ω ι : Type*} [MeasurableSpace Ω] [Fintype ι]

/-- MGF of a signed weighted sum, with the quadratic constant independent of the number of rows. -/
theorem weighted_mgf (μ : Measure Ω) [IsProbabilityMeasure μ] (X : ι → Ω → ℝ)
    (hX : ∀ i, MeasurePreserving (X i) μ (gaussianReal 0 1)) (hi : iIndepFun X μ)
    (w : ι → ℝ) (t : ℝ) (ht : ∀ i, |t*w i| ≤ 1/4) :
    let Z := fun ω => ∑ i, w i * ((X i ω)^2-1)
    Integrable (fun ω => exp (t*Z ω)) μ ∧ mgf Z μ t ≤ exp (4*t^2 * ∑ i, (w i)^2) := by
  let Y := fun i ω => w i * ((X i ω)^2-1)
  have hYi : iIndepFun Y μ :=
    hi.comp (fun i x => w i*(x^2-1)) (fun _ => by fun_prop)
  have hYm (i : ι) : Measurable (Y i) := (((hX i).measurable.pow_const 2).sub_const 1).const_mul _
  have hid (i : ι) : mgf (Y i) μ t =
      ∫ x : ℝ, exp ((t*w i)*(x^2-1)) ∂gaussianReal 0 1 := by
    rw [← (hX i).map_eq, integral_map (hX i).measurable.aemeasurable
      (show AEStronglyMeasurable (fun x : ℝ => exp ((t*w i)*(x^2-1))) _ by fun_prop)]
    simp only [mgf, Y, mul_assoc]
  have hInt (i : ι) : Integrable (fun ω => exp (t * Y i ω)) μ := by
    by_contra h
    have hzero : mgf (Y i) μ t = 0 := integral_undef h
    have hbound := (abs_le.mp (ht i)).2
    have hp : 0 < 1-2*(t*w i) := by linarith
    rw [hid, gaussian_centered_square_mgf (by linarith)] at hzero
    exact (div_pos (exp_pos _) (Real.sqrt_pos.2 hp)).ne' hzero
  constructor
  · simpa only [Finset.sum_apply, Y] using hYi.integrable_exp_mul_sum hYm
      (s := Finset.univ) (fun i _ => hInt i)
  · have hprod := hYi.mgf_sum (t := t) hYm Finset.univ
    calc
      _ = mgf (∑ i, Y i) μ t := by
        congr 1
        funext ω
        simp only [Finset.sum_apply, Y]
      _ = ∏ i, mgf (Y i) μ t := hprod
      _ ≤ ∏ i, exp (4*(t*w i)^2) := Finset.prod_le_prod
        (fun i _ => mgf_nonneg) (fun i _ => (hid i).le.trans (one_mgf_bound (ht i)))
      _ = _ := by
        rw [← Real.exp_sum, Finset.mul_sum]
        congr 1
        exact Finset.sum_congr rfl (fun i _ => by ring)

private theorem one_sided_tail (μ : Measure Ω) [IsProbabilityMeasure μ] (X : ι → Ω → ℝ)
    (hX : ∀ i, MeasurePreserving (X i) μ (gaussianReal 0 1)) (hi : iIndepFun X μ)
    (w : ι → ℝ) {v L u : ℝ} (hv : 0 < v) (hL : 0 < L) (hu : 0 < u)
    (hw2 : ∑ i, (w i)^2 ≤ v) (hwInf : ∀ i, |w i| ≤ L) :
    μ.real {ω | 4*Real.sqrt (v*u) + 8*L*u ≤ ∑ i, w i*((X i ω)^2-1)} ≤ exp (-u) := by
  let t := min (Real.sqrt u / (2*Real.sqrt v)) (1/(4*L))
  have ht : 0 < t := lt_min (by positivity) (by positivity)
  have htv : t*(2*Real.sqrt v) ≤ Real.sqrt u :=
    (le_div_iff₀ (by positivity)).mp (min_le_left _ _)
  have htL : t*(4*L) ≤ 1 :=
    (le_div_iff₀ (by positivity)).mp (min_le_right _ _)
  have htw (i : ι) : |t*w i| ≤ 1/4 := by
    rw [abs_mul, abs_of_pos ht]
    have h := mul_le_mul_of_nonneg_left (hwInf i) ht.le
    linarith
  obtain ⟨hInt, hmgf⟩ := weighted_mgf μ X hX hi w t htw
  let T := 4*Real.sqrt (v*u)+8*L*u
  have hmulv : 4*t^2*v ≤ u := by
    have h := pow_le_pow_left₀ (by positivity : 0 ≤ t*(2*Real.sqrt v)) htv 2
    rw [mul_pow, mul_pow, Real.sq_sqrt hv.le, Real.sq_sqrt hu.le] at h
    linarith
  have hmulT : 2*u ≤ t*T := by
    dsimp only [T]
    rw [Real.sqrt_mul hv.le]
    rcases le_total (Real.sqrt u / (2*Real.sqrt v)) (1/(4*L)) with h | h
    · have he : t*(2*Real.sqrt v) = Real.sqrt u := by
        rw [show t = _ from min_eq_left h, div_mul_cancel₀ _ (by positivity)]
      have hc := congrArg (fun x : ℝ => x*Real.sqrt u) he
      nlinarith only [hc, Real.sq_sqrt hu.le, mul_nonneg (mul_nonneg ht.le hL.le) hu.le]
    · have he : t*(4*L) = 1 := by
        rw [show t = _ from min_eq_right h, div_mul_cancel₀ _ (by positivity)]
      have hc := congrArg (fun x : ℝ => x*u) he
      nlinarith only [hc, mul_nonneg (mul_nonneg ht.le (Real.sqrt_nonneg v)) (Real.sqrt_nonneg u)]
  have hvar := mul_le_mul_of_nonneg_left hw2 (by positivity : 0 ≤ 4*t^2)
  exact (measure_ge_le_exp_mul_mgf T ht.le hInt).trans <| calc
    _ ≤ exp (-t*T)*exp (4*t^2 * ∑ i, (w i)^2) := mul_le_mul_of_nonneg_left hmgf (exp_pos _).le
    _ ≤ _ := by rw [← Real.exp_add]; apply Real.exp_le_exp.mpr; linarith

/-- Two-sided Bernstein tail for independent standard normals and arbitrary signed weights. -/
theorem weighted_chiSquare_tail (μ : Measure Ω) [IsProbabilityMeasure μ] (X : ι → Ω → ℝ)
    (hX : ∀ i, MeasurePreserving (X i) μ (gaussianReal 0 1)) (hi : iIndepFun X μ)
    (w : ι → ℝ) {v L u : ℝ} (hv : 0 < v) (hL : 0 < L) (hu : 0 < u)
    (hw2 : ∑ i, (w i)^2 ≤ v) (hwInf : ∀ i, |w i| ≤ L) :
    μ.real {ω | 4*Real.sqrt (v*u) + 8*L*u ≤ |∑ i, w i*((X i ω)^2-1)|} ≤ 2*exp (-u) := by
  let S := fun ω => ∑ i, w i*((X i ω)^2-1)
  let T := 4*Real.sqrt (v*u) + 8*L*u
  have hp := one_sided_tail μ X hX hi w hv hL hu hw2 hwInf
  have hn := one_sided_tail μ X hX hi (fun i => - w i) hv hL hu
    (by simpa only [neg_sq] using hw2) (fun i => by simpa only [abs_neg] using hwInf i)
  change μ.real {ω | T ≤ S ω} ≤ _ at hp
  simp only [neg_mul, Finset.sum_neg_distrib] at hn
  change μ.real {ω | T ≤ -S ω} ≤ _ at hn
  have he : {ω | T ≤ |S ω|} = {ω | T ≤ S ω} ∪ {ω | T ≤ -S ω} := by
    ext ω
    change T ≤ |S ω| ↔ T ≤ S ω ∨ T ≤ -S ω
    rw [le_abs', or_comm, le_neg]
  change μ.real {ω | T ≤ |S ω|} ≤ _
  rw [he]
  linarith [measureReal_union_le (μ := μ) {ω | T ≤ S ω} {ω | T ≤ -S ω}]

/-- In the original product space of Gaussian starts, a fixed unit projection of
each physical row has the standard normal law; these projections are independent. -/
theorem projected_source_rows {d q : ℕ} (hq : 2*q+1 < d)
    (z : EuclideanSpace ℝ (Fin (q+1))) (hz : ‖z‖ = 1) :
    let μ := Measure.pi (fun _ : Fin (q+1) => stdGaussian (EuclideanSpace ℝ (Fin d)))
    let X := fun (i : Fin d) (ω : Fin (q+1) → EuclideanSpace ℝ (Fin d)) =>
      inner ℝ z (WithLp.toLp 2 (fun a => ω a i))
    (∀ i, MeasurePreserving (X i) μ (gaussianReal 0 1)) ∧ iIndepFun X μ := by
  let E := EuclideanSpace ℝ (Fin (q+1))
  let f : E →L[ℝ] ℝ := innerSL ℝ z
  have hf : MeasurePreserving f (stdGaussian E) (gaussianReal 0 1) := by
    refine ⟨f.continuous.measurable, ?_⟩
    rw [IsGaussian.map_eq_gaussianReal, integral_strongDual_stdGaussian, variance_dual_stdGaussian]
    simp only [f, innerSL_apply_norm, hz, one_pow, Real.toNNReal_one]
  exact ⟨fun i => hf.comp (FixedSpectrumSourceRowLaw.actual_source_row_marginal_law hq i),
    (FixedSpectrumSourceRowIndependence.actual_source_rows_independent hq).comp
      (fun _ => f) (fun _ => f.continuous.measurable)⟩

theorem projected_source_row_tail {d q : ℕ} (hq : 2*q+1 < d)
    (z : EuclideanSpace ℝ (Fin (q+1))) (hz : ‖z‖ = 1)
    (w : Fin d → ℝ) {v L u : ℝ} (hv : 0 < v) (hL : 0 < L) (hu : 0 < u)
    (hw2 : ∑ i, (w i)^2 ≤ v) (hwInf : ∀ i, |w i| ≤ L) :
    let μ := Measure.pi (fun _ : Fin (q+1) => stdGaussian (EuclideanSpace ℝ (Fin d)))
    μ.real {ω | 4*Real.sqrt (v*u) + 8*L*u ≤
      |∑ i : Fin d, w i*((inner ℝ z (WithLp.toLp 2 (fun a => ω a i)))^2-1)|} ≤ 2*exp (-u) := by
  obtain ⟨hX, hi⟩ := projected_source_rows hq z hz
  exact weighted_chiSquare_tail _ _ hX hi w hv hL hu hw2 hwInf

#print axioms gaussian_centered_square_mgf
#print axioms weighted_chiSquare_tail
#print axioms projected_source_row_tail

end AutoSamplingTheory.ExampleCases.GaussianComplexity.WeightedChiSquare
