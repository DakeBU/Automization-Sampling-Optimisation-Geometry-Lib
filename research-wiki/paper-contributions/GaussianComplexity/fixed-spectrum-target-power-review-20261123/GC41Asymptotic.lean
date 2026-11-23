import GC41Target
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumThreshold
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

/-! The target-side test in Section 4.3 of Zhou–Suzuki, in diagonal coordinates. -/

open MeasureTheory ProbabilityTheory
open scoped BigOperators
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent

def diagonalLaw (d : ℕ) (κ : ℝ) : Measure (EuclideanSpace ℝ (Fin d)) :=
  multivariateGaussian 0 (FixedSpectrumRotation.diagonalPrecision d κ)⁻¹

def cosineForm {d : ℕ} (n : ℕ) (x : EuclideanSpace ℝ (Fin d)) : ℝ :=
  ∑ i : Fin d, Real.cos ((n : ℝ) * FixedSpectrumRotation.gridAngle d i) * (WithLp.ofLp x i)^2

def queryThreshold (C : ℝ) (d q : ℕ) : ℝ :=
  C * (((q : ℝ) + 1) * Real.sqrt (Real.log (d : ℝ) / (d : ℝ)) +
    (((q : ℝ) + 1) * ((q : ℝ) + 1 + Real.log (d : ℝ)) * Real.log (d : ℝ)) / (d : ℝ))

/-- One dimension cutoff controls the mode, the gap, the shifted threshold and
the squared signal throughout the prescribed condition-number and query ranges. -/
theorem eventual_source_signal (C : ℝ) (hC : 0 < C) {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) :
    ∃ d₀ : ℕ, ∀ d : ℕ, d₀ ≤ d → ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ q : ℕ, (q : ℝ) ≤ δ/256 * Real.sqrt κ * Real.log (d : ℝ) →
      let n := 2*q + 1
      let τ := queryThreshold C d q
      let μ := diagonalLaw d κ
      let M := ∫ x, ‖x‖^2 ∂μ
      let β := |∫ x, cosineForm n x ∂μ| / M
      2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) ∧
        0 ≤ τ ∧ τ ≤ 1/2 ∧ τ ≤ β/4 ∧ 0 < M ∧ 0 < β ∧ 320 ≤ M*β^2 := by
  let B : ℝ := (1 - Real.exp (-4)) * Real.exp (-3)
  have hB : 0 < B := mul_pos (sub_pos.mpr (Real.exp_lt_one_iff.mpr (by norm_num))) (Real.exp_pos _)
  obtain ⟨J, hJ⟩ := exists_nat_ge (640/B^2)
  obtain ⟨T, hT⟩ := FixedSpectrumThreshold.eventual_actual_gaussian_threshold_small C hC hδ0 hδ1
  obtain ⟨S, hS⟩ := FixedSpectrumSignalStrength.eventual_actual_gaussian_signal_strength hδ0 hδ1
  obtain ⟨K, hK⟩ := FixedSpectrumModeGap.eventual_source_query_mode_gap hδ0 hδ1
  refine ⟨max (max K T) (max S (J^2)), ?_⟩
  intro d hd κ hκ hkcap q hq
  obtain ⟨⟨hdK, hdT⟩, hdS, hdJ⟩ := (max_le_iff.mp hd).imp max_le_iff.mp max_le_iff.mp
  obtain ⟨hd2, hn, hnd, hgap⟩ := hK d hdK κ hκ hkcap q hq
  obtain ⟨ht0, ht1, htβ⟩ := hT d hdT κ hκ hkcap q hq
  obtain ⟨hM, hβ, _, _, hs⟩ := hS d hdS κ hκ hkcap q hq
  refine ⟨hd2, hn, hnd, hgap, ht0, ht1, htβ, hM, hβ, le_trans ?_ hs⟩
  have hr : (J : ℝ) ≤ Real.sqrt (d : ℝ) :=
    Real.le_sqrt_of_sq_le (by exact_mod_cast hdJ)
  change 320 ≤ (B^2/2) * Real.sqrt (d : ℝ)
  calc
    320 = (B^2/2) * (640/B^2) := by field_simp [hB.ne']; ring
    _ ≤ _ := mul_le_mul_of_nonneg_left (hJ.trans hr) (by positivity)

/-- Chebyshev's inequality at the mean for a contrast of two dependent
quadratic statistics. Nonnegativity of the variance of their sum controls the covariance. -/
private theorem contrast_probability {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    [IsProbabilityMeasure μ] {X Y : Ω → ℝ} (hX : MemLp X 2 μ) (hY : MemLp Y 2 μ)
    (hmeas : Measurable (fun x => X x - Y x)) {M m : ℝ}
    (hXvar : Var[X; μ] ≤ 2*M) (hYvar : Var[Y; μ] ≤ 2*M)
    (hm : m = ∫ x, X x - Y x ∂μ) (hmpos : 0 < m) (hs : 80*M ≤ m^2) :
    (9/10 : ℝ) ≤ μ.real {x | 0 < X x - Y x} := by
  let Z := fun x => X x - Y x
  have hZ : MemLp Z 2 μ := hX.sub hY
  have hv : Var[Z; μ] ≤ 8*M := by
    have h := variance_nonneg (fun x => X x + Y x) μ
    rw [variance_fun_add hX hY] at h
    change Var[fun x => X x - Y x; μ] ≤ _
    rw [variance_fun_sub hX hY]
    linarith
  have hsub : {x | Z x ≤ 0} ⊆ {x | m ≤ |Z x - (∫ y, Z y ∂μ)|} := by
    intro x hx
    change Z x ≤ 0 at hx
    change m ≤ |Z x - (∫ y, Z y ∂μ)|
    rw [← hm, abs_of_nonpos (by linarith : Z x - m ≤ 0)]
    linarith
  have hbad : μ {x | Z x ≤ 0} ≤ ENNReal.ofReal (1/10 : ℝ) := by
    refine (measure_mono hsub).trans ((meas_ge_le_variance_div_sq hZ hmpos).trans ?_)
    apply ENNReal.ofReal_le_ofReal
    apply (div_le_iff₀ (sq_pos_of_pos hmpos)).mpr
    linarith
  have hb : μ.real {x | Z x ≤ 0} ≤ (1/10 : ℝ) := by
    simpa [Measure.real_def] using ENNReal.toReal_mono ENNReal.ofReal_ne_top hbad
  have he : {x | 0 < Z x} = {x | Z x ≤ 0}ᶜ := by ext x; simp
  change 9/10 ≤ μ.real {x | 0 < Z x}
  rw [he, probReal_compl_eq_one_sub (measurableSet_le hmeas measurable_const)]
  linarith

/-- For the diagonal Gaussian target, the signed, shifted source statistic is
strictly positive with probability at least 9/10, uniformly in the hard regime. -/
theorem eventual_diagonal_detector_probability (C : ℝ) (hC : 0 < C) {δ : ℝ}
    (hδ0 : 0 < δ) (hδ1 : δ < 1) :
    ∃ d₀ : ℕ, ∀ d : ℕ, d₀ ≤ d → ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ q : ℕ, (q : ℝ) ≤ δ/256 * Real.sqrt κ * Real.log (d : ℝ) →
      (9/10 : ℝ) ≤ (diagonalLaw d κ).real
        {x | 0 < (-1 : ℝ)^(2*q+1) * cosineForm (2*q+1) x - 2 * queryThreshold C d q * ‖x‖^2} := by
  obtain ⟨D, hD⟩ := eventual_source_signal C hC hδ0 hδ1
  refine ⟨D, ?_⟩
  intro d hd κ hκ hkcap q hq
  let μ := diagonalLaw d κ
  let n := 2*q+1
  let τ := queryThreshold C d q
  let Q := @cosineForm d n
  let N := fun x : EuclideanSpace ℝ (Fin d) => ‖x‖^2
  let M := ∫ x, N x ∂μ
  let b := ∫ x, Q x ∂μ
  let β := |b|/M
  let s := (-1 : ℝ)^n
  have hs := hD d hd κ hκ hkcap q hq
  change 2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) ∧
    0 ≤ τ ∧ τ ≤ 1/2 ∧ τ ≤ β/4 ∧ 0 < M ∧ 0 < β ∧ 320 ≤ M*β^2 at hs
  obtain ⟨hd2, hn, hnd, hgap, ht0, ht1, htβ, hM, hβ, hsignal⟩ := hs
  obtain ⟨_, hb, _, _⟩ :=
    FixedSpectrumBias.actual_diagonal_gaussian_exponential_bias hd2 hκ n hn hnd hgap
  change 0 < s*b at hb
  have hsign : s^2 = 1 := by
    dsimp [s]
    rw [← pow_mul, Nat.mul_comm n 2, pow_mul]
    norm_num
  have hmeanQ : s*b = β*M := by
    change s*b = (|b|/M)*M
    rw [div_mul_cancel₀ _ hM.ne', ← abs_of_pos hb, abs_mul]
    simp [s]
  obtain ⟨hN, hQ, _, _, hvN, hvQ, _⟩ :=
    FixedSpectrumVariances.actual_diagonal_gaussian_quadratic_variances hd2 hκ n hn hnd
  change MemLp N 2 μ at hN
  change MemLp Q 2 μ at hQ
  change Var[N; μ] ≤ 2*M at hvN
  change Var[Q; μ] ≤ 2*M at hvQ
  let m := (β-2*τ)*M
  have hhalf : β*M/2 ≤ m := by
    have h := mul_le_mul_of_nonneg_right htβ hM.le
    dsimp [m]; nlinarith
  have hr : 0 < β*M/2 := by positivity
  have hmpos : 0 < m := hr.trans_le hhalf
  have hlarge : 80*M ≤ m^2 := by
    have h := mul_le_mul_of_nonneg_right hsignal hM.le
    nlinarith only [h, pow_le_pow_left₀ hr.le hhalf 2]
  have : IsProbabilityMeasure μ := by dsimp [μ, diagonalLaw]; infer_instance
  apply contrast_probability μ (hQ.const_mul s) (hN.const_mul (2*τ)) _ _ _ _ hmpos hlarge
  · have hc (i : Fin d) : Measurable (fun x : EuclideanSpace ℝ (Fin d) => WithLp.ofLp x i) :=
      (EuclideanSpace.proj i).continuous.measurable
    exact ((Finset.measurable_sum _ (fun i _ => ((hc i).pow_const 2).const_mul _)).const_mul s).sub
      ((measurable_norm.pow_const 2).const_mul (2*τ))
  · rw [variance_const_mul, hsign, one_mul]
    exact hvQ
  · rw [variance_const_mul]
    calc
      _ ≤ (2*τ)^2 * (2*M) := mul_le_mul_of_nonneg_left hvN (sq_nonneg _)
      _ ≤ 1*(2*M) := mul_le_mul_of_nonneg_right (by nlinarith : (2*τ)^2 ≤ 1) (by positivity)
      _ = _ := one_mul _
  · rw [integral_sub ((hQ.const_mul s).integrable (by norm_num))
        ((hN.const_mul (2*τ)).integrable (by norm_num)), integral_const_mul, integral_const_mul]
    change (β-2*τ)*M = s*b - 2*τ*M
    rw [hmeanQ]
    ring

#print axioms eventual_source_signal
#print axioms eventual_diagonal_detector_probability

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
