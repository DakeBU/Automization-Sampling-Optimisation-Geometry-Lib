import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Analysis.Real.Sqrt
import Mathlib.MeasureTheory.Measure.Count

/-! Actual full Boolean coordinate-flip energy for the compact Gaussian core.
The compact Gaussian LSI and the noncompact SPHMC extension are separate edges. -/

open MeasureTheory ProbabilityTheory Filter
open scoped Topology BigOperators ENNReal
noncomputable section
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy

private def countLaw (n : ℕ) : Measure (Fin n → Bool) :=
  (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count

private instance countLaw_probability (n : ℕ) : IsProbabilityMeasure (countLaw n) := by
  constructor
  unfold countLaw
  simp only [Measure.smul_apply, smul_eq_mul]
  rw [Measure.count_apply_finite Set.univ Set.finite_univ]
  simp only [Set.Finite.toFinset_univ, Finset.card_univ]
  exact ENNReal.inv_mul_cancel (by exact_mod_cast Fintype.card_ne_zero) (by simp)

private def normalizedSum (n : ℕ) (ε : Fin n → Bool) : ℝ :=
  (Real.sqrt (n : ℝ))⁻¹ * ∑ j : Fin n, if ε j then (1 : ℝ) else -1

private theorem compact_derivative_bounds (f : ℝ → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    ∃ B K : ℝ, 0 ≤ B ∧ 0 ≤ K ∧ (∀ x, |deriv f x| ≤ B) ∧
      (∀ x y, |deriv f y - deriv f x| ≤ K * |y-x|) := by
  obtain ⟨B, hB⟩ := hs.deriv.exists_bound_of_continuous
    (hf.continuous_deriv (by norm_num))
  have hd : ContDiff ℝ 1 (deriv f) := hf.deriv'
  obtain ⟨K, hK⟩ := hs.deriv.deriv.exists_bound_of_continuous hd.continuous_deriv_one
  refine ⟨max B 0, max K 0, le_max_right _ _, le_max_right _ _, ?_, ?_⟩
  · intro x
    have hb : |deriv f x| ≤ B := by simpa only [Real.norm_eq_abs] using hB x
    exact hb.trans (le_max_left _ _)
  · intro x y
    simpa only [Real.norm_eq_abs] using
      (convex_univ : Convex ℝ (Set.univ : Set ℝ)).norm_image_sub_le_of_norm_deriv_le
        (fun z _ => hf.differentiable_deriv_two z)
        (fun z _ => (hK z).trans (le_max_left _ _)) (Set.mem_univ x) (Set.mem_univ y)

private theorem bounded_secant (f : ℝ → ℝ) (hf : Differentiable ℝ f)
    (B K : ℝ) (hB : ∀ x, |deriv f x| ≤ B)
    (hK : ∀ x y, |deriv f y - deriv f x| ≤ K * |y-x|)
    (hK0 : 0 ≤ K) (x y : ℝ) :
    ∃ a : ℝ, f y - f x = a * (y-x) ∧ |a| ≤ B ∧
      |a - deriv f x| ≤ K * |y-x| := by
  rcases lt_trichotomy x y with hxy | rfl | hyx
  · obtain ⟨c, hc, he⟩ := exists_deriv_eq_slope f hxy hf.continuous.continuousOn
      hf.differentiableOn
    refine ⟨deriv f c, ?_, hB c, (hK x c).trans ?_⟩
    · exact (eq_div_iff (sub_ne_zero.mpr hxy.ne')).mp he |>.symm
    · apply mul_le_mul_of_nonneg_left _ hK0
      rw [abs_of_pos (sub_pos.mpr hc.1), abs_of_pos (sub_pos.mpr hxy)]
      linarith [hc.2]
  · exact ⟨deriv f x, by simp, hB x, by simp⟩
  · obtain ⟨c, hc, he⟩ := exists_deriv_eq_slope f hyx hf.continuous.continuousOn
      hf.differentiableOn
    refine ⟨deriv f c, ?_, hB c, (hK x c).trans ?_⟩
    · have hp := (eq_div_iff (sub_ne_zero.mpr hyx.ne')).mp he
      nlinarith
    · apply mul_le_mul_of_nonneg_left _ hK0
      rw [abs_of_neg (sub_neg.mpr hc.2), abs_of_neg (sub_neg.mpr hyx)]
      linarith [hc.1]

private theorem squared_increment_error (f : ℝ → ℝ) (hf : Differentiable ℝ f)
    (B K : ℝ) (_hB0 : 0 ≤ B) (hK0 : 0 ≤ K)
    (hB : ∀ x, |deriv f x| ≤ B)
    (hK : ∀ x y, |deriv f y - deriv f x| ≤ K * |y-x|) (x y : ℝ) :
    |(f y - f x)^2 - (deriv f x)^2 * (y-x)^2| ≤
      2 * B * K * |y-x|^3 := by
  obtain ⟨a, ha, hab, had⟩ := bounded_secant f hf B K hB hK hK0 x y
  have hs : |a + deriv f x| ≤ 2 * B :=
    (abs_add_le _ _).trans (by linarith [hB x])
  calc
    |(f y - f x)^2 - (deriv f x)^2 * (y-x)^2| =
        |a - deriv f x| * |a + deriv f x| * |y-x|^2 := by
      rw [ha, ← abs_mul, ← abs_pow, ← abs_mul]
      congr 1
      ring
    _ ≤ (K * |y-x|) * (2 * B) * |y-x|^2 := by
      exact mul_le_mul_of_nonneg_right
        (mul_le_mul had hs (abs_nonneg _) (mul_nonneg hK0 (abs_nonneg _))) (sq_nonneg _)
    _ = 2 * B * K * |y-x|^3 := by ring

private theorem flip_displacement (n : ℕ) (ε : Fin n → Bool) (j : Fin n) :
    normalizedSum n (Function.update ε j (!ε j)) - normalizedSum n ε =
      if ε j then -2 * (Real.sqrt (n : ℝ))⁻¹ else 2 * (Real.sqrt (n : ℝ))⁻¹ := by
  have he : (∑ k : Fin n, (if Function.update ε j (!ε j) k then (1 : ℝ) else -1)) -
      (∑ k : Fin n, if ε k then (1 : ℝ) else -1) =
      (if !ε j then (1 : ℝ) else -1) - (if ε j then (1 : ℝ) else -1) := by
    rw [← Finset.sum_sub_distrib]
    rw [Finset.sum_eq_single j]
    · simp
    · intro k _ hkj
      simp [Function.update_of_ne hkj]
    · simp
  dsimp [normalizedSum]
  rw [← mul_sub, he]
  cases ε j <;> simp <;> ring

private theorem flip_distance (n : ℕ) (ε : Fin n → Bool) (j : Fin n) :
    |normalizedSum n (Function.update ε j (!ε j)) - normalizedSum n ε| =
      2 * (Real.sqrt (n : ℝ))⁻¹ := by
  rw [flip_displacement]
  cases ε j <;> simp [abs_mul, abs_of_nonneg (inv_nonneg.mpr (Real.sqrt_nonneg _))]

private theorem full_flip_pointwise_error (f : ℝ → ℝ) (hf : Differentiable ℝ f)
    (B K : ℝ) (hB0 : 0 ≤ B) (hK0 : 0 ≤ K)
    (hB : ∀ x, |deriv f x| ≤ B)
    (hK : ∀ x y, |deriv f y - deriv f x| ≤ K * |y-x|)
    (n : ℕ) (hn : 0 < n) (ε : Fin n → Bool) :
    |(∑ j : Fin n,
        (f (normalizedSum n (Function.update ε j (!ε j))) - f (normalizedSum n ε))^2) -
      4 * (deriv f (normalizedSum n ε))^2| ≤
        16 * B * K * (Real.sqrt (n : ℝ))⁻¹ := by
  let r : ℝ := (Real.sqrt (n : ℝ))⁻¹
  have hnp : 0 < (n : ℝ) := by exact_mod_cast hn
  have hr : (n : ℝ) * r^2 = 1 := by
    dsimp [r]
    rw [inv_pow, Real.sq_sqrt (le_of_lt hnp)]
    exact mul_inv_cancel₀ (ne_of_gt hnp)
  have hdist (j : Fin n) :
      (normalizedSum n (Function.update ε j (!ε j)) - normalizedSum n ε)^2 =
        (2*r)^2 := by
    rw [← sq_abs, flip_distance]
  have hid : (∑ j : Fin n,
      ((f (normalizedSum n (Function.update ε j (!ε j))) - f (normalizedSum n ε))^2 -
       (deriv f (normalizedSum n ε))^2 * (2*r)^2)) =
      (∑ j : Fin n,
        (f (normalizedSum n (Function.update ε j (!ε j))) - f (normalizedSum n ε))^2) -
       4 * (deriv f (normalizedSum n ε))^2 := by
    rw [Finset.sum_sub_distrib]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    congr 1
    nlinarith [hr]
  rw [← hid]
  calc
    _ ≤ ∑ j : Fin n, |(f (normalizedSum n (Function.update ε j (!ε j))) -
        f (normalizedSum n ε))^2 - (deriv f (normalizedSum n ε))^2 * (2*r)^2| :=
      Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _j : Fin n, 2 * B * K * (2*r)^3 := by
      apply Finset.sum_le_sum
      intro j _
      have h := squared_increment_error f hf B K hB0 hK0 hB hK
        (normalizedSum n ε) (normalizedSum n (Function.update ε j (!ε j)))
      rwa [hdist j, flip_distance] at h
    _ = 16 * B * K * r := by
      simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
      calc
        _ = (16 * B * K * r) * ((n : ℝ) * r^2) := by ring
        _ = _ := by rw [hr, mul_one]


private def flipEnergy (f : ℝ → ℝ) (n : ℕ) (ε : Fin n → Bool) : ℝ :=
  ∑ j : Fin n,
    (f (normalizedSum n (Function.update ε j (!ε j))) - f (normalizedSum n ε))^2

/-- The genuine sum over every Boolean coordinate has Gaussian limit four times
the derivative-square integral. All finite-count L1 domains, including n=0,
are conclusions; no bound, probability or convergence certificate is supplied. -/
theorem compact_count_gaussian_flip_energy_limit
    (f : ℝ → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let μ : (n : ℕ) → Measure (Fin n → Bool) := fun n =>
      (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (n : ℕ) → (Fin n → Bool) → ℝ := fun n ε =>
      (Real.sqrt (n : ℝ))⁻¹ * ∑ j : Fin n, if ε j then (1 : ℝ) else -1
    let γ : Measure ℝ := gaussianReal 0 1
    Integrable (fun x => (deriv f x)^2) γ ∧
    (∀ n : ℕ, Integrable
      (fun ε : Fin n → Bool => ∑ j : Fin n,
        (f (S n (Function.update ε j (!ε j))) - f (S n ε))^2) (μ n)) ∧
    Tendsto (fun n : ℕ => ∫ ε : Fin (n+1) → Bool,
      (∑ j : Fin (n+1),
        (f (S (n+1) (Function.update ε j (!ε j))) - f (S (n+1) ε))^2)
      ∂μ (n+1)) atTop (𝓝 (4 * ∫ x, (deriv f x)^2 ∂γ)) := by
  change Integrable (fun x => (deriv f x)^2) (gaussianReal 0 1) ∧
    (∀ n, Integrable (flipEnergy f n) (countLaw n)) ∧
    Tendsto (fun n => ∫ ε, flipEnergy f (n+1) ε ∂countLaw (n+1)) atTop
      (𝓝 (4 * ∫ x, (deriv f x)^2 ∂gaussianReal 0 1))
  rcases GaussianCompactEntropy.compact_count_gaussian_entropy_limits f hf hs
    with ⟨_, _, iC, jC, _, _, tC, _⟩
  change Tendsto (fun n => ∫ ε, (deriv f (normalizedSum (n+1) ε))^2 ∂countLaw (n+1))
    atTop (𝓝 (∫ x, (deriv f x)^2 ∂gaussianReal 0 1)) at tC
  have iE (n : ℕ) : Integrable (flipEnergy f n) (countLaw n) := Integrable.of_finite
  have iD (n : ℕ) : Integrable (fun ε => (deriv f (normalizedSum n ε))^2) (countLaw n) :=
    (jC n).2.2
  obtain ⟨B, K, hB0, hK0, hB, hK⟩ := compact_derivative_bounds f hf hs
  have hi (n : ℕ) :
      ‖(∫ ε, flipEnergy f (n+1) ε ∂countLaw (n+1)) -
        4 * (∫ ε, (deriv f (normalizedSum (n+1) ε))^2 ∂countLaw (n+1))‖ ≤
        16 * B * K * (Real.sqrt ((n+1 : ℕ) : ℝ))⁻¹ := by
    rw [← integral_const_mul, ← integral_sub (iE (n+1)) ((iD (n+1)).const_mul 4)]
    have hp (ε : Fin (n+1) → Bool) :
        ‖flipEnergy f (n+1) ε - 4 * (deriv f (normalizedSum (n+1) ε))^2‖ ≤
          16 * B * K * (Real.sqrt ((n+1 : ℕ) : ℝ))⁻¹ := by
      simpa only [flipEnergy, Real.norm_eq_abs] using
        full_flip_pointwise_error f (hf.differentiable (by norm_num)) B K hB0 hK0 hB hK
          (n+1) (Nat.succ_pos n) ε
    have h := norm_integral_le_of_norm_le_const (μ := countLaw (n+1))
      (Filter.Eventually.of_forall hp)
    simpa only [measureReal_def, measure_univ, ENNReal.toReal_one, mul_one] using h
  have tr : Tendsto (fun n : ℕ => (Real.sqrt ((n+1 : ℕ) : ℝ))⁻¹) atTop (𝓝 0) :=
    tendsto_inv_atTop_zero.comp
      (Real.tendsto_sqrt_atTop.comp
        (tendsto_natCast_atTop_atTop.comp (tendsto_add_atTop_nat 1)))
  have te : Tendsto (fun n : ℕ =>
      (∫ ε, flipEnergy f (n+1) ε ∂countLaw (n+1)) -
        4 * (∫ ε, (deriv f (normalizedSum (n+1) ε))^2 ∂countLaw (n+1)))
      atTop (𝓝 0) := squeeze_zero_norm hi (by simpa using tr.const_mul (16*B*K))
  have t := te.add (tC.const_mul 4)
  simp only [zero_add, sub_add_cancel] at t
  exact ⟨iC, iE, t⟩

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy
