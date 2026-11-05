import AutoSamplingTheory.ExampleCases.GaussianComplexity.EvaluatedGaussian
import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

noncomputable section

-- A genuine consumer: actual determinant-conditioned Gaussian target measures.
-- This evaluates their ordered test gap. No TV or query lower bound is claimed.
example {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
    let v : ℝ := ((-1 : ℝ) ^ n / (n : ℝ)) * ((s - 1) / (s + 1)) ^ n *
      (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) / (1 - r ^ 2)
    Integrable t (νpos.bind γ) ∧ Integrable t (νneg.bind γ) ∧
      ((∫ x, t x ∂νpos.bind γ) - (∫ x, t x ∂νneg.bind γ)) = 2 * v ∧
      ((∫ x, t x ∂νpos.bind γ) - (∫ x, t x ∂νneg.bind γ)) ≠ 0 := by
  dsimp only
  have ht := SelectedTilt.selected_tilt hn hκ
  have hm := MixtureExpectation.actual_mixture_expectation_gap hn hκ ht.2.2.1.le
  have he := EvaluatedGaussian.selected_gaussian_value hn hκ
  have hgap := hm.2.2.2.2.2.2.trans (congrArg (fun z : ℝ => 2 * z) he.2.2.1)
  refine ⟨hm.1, hm.2.1, hgap, ?_⟩
  rw [hgap]
  have hn3 : (3 : ℝ) ≤ n := by exact_mod_cast hn
  have hn0 : (0 : ℝ) < n := by linarith
  have hs : (2 : ℝ) ≤ Real.sqrt κ := Real.le_sqrt_of_sq_le (by linarith)
  have hratio : 0 < (Real.sqrt κ - 1) / (Real.sqrt κ + 1) :=
    div_pos (by linarith) (by linarith)
  have hbase : 0 < 1 - 1 / (n : ℝ) := by
    have := (div_lt_one hn0).mpr (by linarith : (1 : ℝ) < n)
    linarith
  have hden : 0 < 1 -
      ((1 - 1 / (n : ℝ)) * ((Real.sqrt κ - 1) / (Real.sqrt κ + 1))) ^ 2 := by
    have hr := ht.1
    have hr1 := ht.2.1
    nlinarith
  exact mul_ne_zero (by norm_num)
    (div_ne_zero
      (mul_ne_zero
        (mul_ne_zero (div_ne_zero (pow_ne_zero n (by norm_num)) (ne_of_gt hn0))
          (pow_ne_zero n (ne_of_gt hratio)))
        (ne_of_gt (Real.rpow_pos_of_pos hbase _)))
      (ne_of_gt hden))

#print axioms EvaluatedGaussian.selected_gaussian_value
#print axioms selected_numerator_value

end
