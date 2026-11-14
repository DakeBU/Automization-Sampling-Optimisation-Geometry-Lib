import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Int.Basic
import Mathlib.Algebra.BigOperators.Field

open scoped BigOperators
set_option autoImplicit false

/-! Actual cosine-frame identities for arXiv2610.20492v1 Appendix C.2 Fact C.5.
The source range is exactly2q+1<d, includingq0. Gaussian Gram centering is a
private genuine consumer; range/Krylov, concentration and main bounds are separate. -/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram

theorem actual_cosine_frame_gram {d q : ℕ} (hq : 2 * q + 1 < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  t.transpose * t = (d : ℝ) • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) ∧
    t.transpose * D * t = 0 ∧
    ∀ i : Fin d, ∑ k : Fin (q + 1), (t i k) ^ 2 ≤ 2 * ((q : ℝ) + 1)
:= by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  let C : ℤ → Fin d → ℝ := fun k i => Real.cos ((k : ℝ) * θ i)
  let c : Fin (q + 1) → ℝ := fun k => if k.val = 0 then 1 else Real.sqrt 2
  let n : ℤ := 2 * (q : ℤ) + 1
  have hd : 2 ≤ d := by omega
  have hqd : 2 * (q : ℤ) + 1 < (d : ℤ) := by exact_mod_cast hq
  have hmode (k : ℤ) (hlo : -(2 * (d : ℤ)) < k) (hhi : k < 2 * (d : ℤ)) :
      (∑ i : Fin d, C k i) = if k = 0 then (d : ℝ) else 0 := by
    by_cases hk0 : k = 0
    · subst k
      simp [C]
    · have hnd : ¬ (2 * (d : ℤ)) ∣ k := by
        intro hdiv
        by_cases hk : 0 ≤ k
        · exact hk0 (Int.eq_zero_of_dvd_of_nonneg_of_lt hk hhi hdiv)
        · have hz := Int.eq_zero_of_dvd_of_nonneg_of_lt
            (show 0 ≤ -k by omega) (show -k < 2 * (d : ℤ) by omega)
            (dvd_neg.mpr hdiv)
          omega
      simpa [C, θ, hnd, hk0] using
        (AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias.actual_midpoint_grid_cosine_alias hd k)
  have hzero (k : ℤ) (hk0 : 0 < k) (hk1 : k < 2 * (d : ℤ)) :
      (∑ i : Fin d, C k i) = 0 := by
    rw [hmode k (by omega) hk1, if_neg (ne_of_gt hk0)]
  have hprod (a b : ℤ) (i : Fin d) :
      C a i * C b i = (C (a - b) i + C (a + b) i) / 2 := by
    dsimp only [C]
    rw [Int.cast_sub, Int.cast_add, sub_mul, add_mul]
    nlinarith [Real.two_mul_cos_mul_cos ((a : ℝ) * θ i) ((b : ℝ) * θ i)]
  have hpair (a b : ℤ) :
      (∑ i : Fin d, C a i * C b i) =
        ((∑ i : Fin d, C (a - b) i) + (∑ i : Fin d, C (a + b) i)) / 2 := by
    simp_rw [hprod]
    simp only [← Finset.sum_div, Finset.sum_add_distrib]
  have htriple (a b : ℤ) :
      (∑ i : Fin d, C n i * (C a i * C b i)) =
        (((∑ i : Fin d, C (n - (a - b)) i) + (∑ i : Fin d, C (n + (a - b)) i)) +
          ((∑ i : Fin d, C (n - (a + b)) i) + (∑ i : Fin d, C (n + (a + b)) i))) / 4 := by
    have hp (i : Fin d) : C n i * (C a i * C b i) =
        ((C (n - (a - b)) i + C (n + (a - b)) i) +
          (C (n - (a + b)) i + C (n + (a + b)) i)) / 4 := by
      calc
        _ = (C n i * C (a - b) i + C n i * C (a + b) i) / 2 := by
          rw [hprod a b i]
          ring
        _ = _ := by rw [hprod n (a - b) i, hprod n (a + b) i]; ring
    simp_rw [hp]
    simp only [← Finset.sum_div, Finset.sum_add_distrib]
  have ht (i : Fin d) (j : Fin (q + 1)) : t i j = c j * C (j.val : ℤ) i := by
    by_cases hj : j.val = 0
    · simp only [t, c, if_pos hj, C, hj, Int.natCast_zero, Int.cast_zero, zero_mul,
        Real.cos_zero, one_mul]
    · simp only [t, c, if_neg hj, C, Int.cast_natCast]
  have hjbound (j : Fin (q + 1)) : (j.val : ℤ) ≤ (q : ℤ) := by
    exact_mod_cast (show j.val ≤ q by omega)
  have hgram (j k : Fin (q + 1)) :
      (∑ i : Fin d, t i j * t i k) = if j = k then (d : ℝ) else 0 := by
    have hs : (∑ i : Fin d, t i j * t i k) =
        c j * c k * (((∑ i : Fin d, C ((j.val : ℤ) - k.val) i) +
          (∑ i : Fin d, C ((j.val : ℤ) + k.val) i)) / 2) := by
      calc
        _ = c j * c k * (∑ i : Fin d, C (j.val : ℤ) i * C (k.val : ℤ) i) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro i _
          rw [ht, ht]
          ring
        _ = _ := by rw [hpair]
    rw [hs, hmode _ (by have := hjbound j; have := hjbound k; omega)
      (by have := hjbound j; have := hjbound k; omega),
      hmode _ (by omega) (by have := hjbound j; have := hjbound k; omega)]
    by_cases heq : j = k
    · subst k
      simp only [sub_self, ite_true]
      by_cases hj : j.val = 0
      · simp only [c, if_pos hj, hj, Int.natCast_zero, zero_add, ite_true,
          one_mul, add_self_div_two]
      · have hsum : (j.val : ℤ) + j.val ≠ 0 := by omega
        rw [if_neg hsum]
        simp only [c, if_neg hj, add_zero]
        have hsqrt : Real.sqrt 2 * Real.sqrt 2 = (2 : ℝ) := by
          nlinarith [Real.sq_sqrt (show 0 ≤ (2 : ℝ) by norm_num)]
        rw [hsqrt]
        ring
    · have hdiff : (j.val : ℤ) - k.val ≠ 0 := by
        intro h
        apply heq
        apply Fin.ext
        omega
      have hsum : (j.val : ℤ) + k.val ≠ 0 := by
        intro h
        apply heq
        apply Fin.ext
        omega
      simp [heq, hdiff, hsum]
  have hweighted (j k : Fin (q + 1)) :
      (∑ i : Fin d, C n i * (C (j.val : ℤ) i * C (k.val : ℤ) i)) = 0 := by
    rw [htriple]
    have hj := hjbound j
    have hk := hjbound k
    have hf1 := hzero (n - ((j.val : ℤ) - k.val)) (by dsimp [n]; omega) (by dsimp [n]; omega)
    have hf2 := hzero (n + ((j.val : ℤ) - k.val)) (by dsimp [n]; omega) (by dsimp [n]; omega)
    have hf3 := hzero (n - ((j.val : ℤ) + k.val)) (by dsimp [n]; omega) (by dsimp [n]; omega)
    have hf4 := hzero (n + ((j.val : ℤ) + k.val)) (by dsimp [n]; omega) (by dsimp [n]; omega)
    rw [hf1, hf2, hf3, hf4]
    norm_num
  change t.transpose * t = (d : ℝ) • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) ∧
    t.transpose * D * t = 0 ∧
    ∀ i : Fin d, ∑ k : Fin (q + 1), (t i k) ^ 2 ≤ 2 * ((q : ℝ) + 1)
  constructor
  · ext j k
    change (∑ i : Fin d, t i j * t i k) = (d : ℝ) * (if j = k then 1 else 0)
    simpa only [mul_ite, mul_one, mul_zero] using hgram j k
  constructor
  · ext j k
    change (∑ i : Fin d, (t.transpose * D) j i * t i k) = 0
    have hm (i : Fin d) : (t.transpose * D) j i = t i j * C n i := by
      simp [D, Matrix.mul_diagonal, Matrix.transpose_apply, C, n]
    simp_rw [hm, ht]
    calc
      _ = c j * c k * (∑ i : Fin d, C n i * (C (j.val : ℤ) i * C (k.val : ℤ) i)) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        ring
      _ = 0 := by rw [hweighted]; ring
  · intro i
    have hb (k : Fin (q + 1)) : (t i k) ^ 2 ≤ if k.val = 0 then 1 else 2 := by
      by_cases hk : k.val = 0
      · simp only [t, if_pos hk, one_pow, le_refl]
      · simp only [t, if_neg hk, mul_pow, Real.sq_sqrt (show 0 ≤ (2 : ℝ) by norm_num)]
        nlinarith [Real.cos_sq_le_one ((k.val : ℝ) * θ i)]
    calc
      _ ≤ ∑ k : Fin (q + 1), (if k.val = 0 then (1 : ℝ) else 2) :=
        Finset.sum_le_sum (fun k _ => hb k)
      _ = 1 + 2 * (q : ℝ) := by rw [Fin.sum_univ_succ]; simp [mul_comm]
      _ ≤ 2 * ((q : ℝ) + 1) := by linarith

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
