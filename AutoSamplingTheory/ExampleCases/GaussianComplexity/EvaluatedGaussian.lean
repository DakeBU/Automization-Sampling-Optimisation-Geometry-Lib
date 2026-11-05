import AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedNumerator
import AutoSamplingTheory.ExampleCases.GaussianComplexity.SurfaceLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation

open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.EvaluatedGaussian
set_option autoImplicit false

/-! The evaluated signed Gaussian expectation in Appendix B.2.2, Eq24.
The normalized spherical numerator, the actual Gaussian-to-surface transport,
and the actual density law are canonical dependencies. -/

theorem selected_gaussian_value {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
    let v : ℝ := ((-1 : ℝ) ^ n / (n : ℝ)) * ((s - 1) / (s + 1)) ^ n *
      (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) / (1 - r ^ 2)
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O)) (orthogonalHaar n) ∧
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)) (orthogonalHaar n) ∧
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O) ∂orthogonalHaar n) = v ∧
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x) ∂orthogonalHaar n) = v := by
  let s : ℝ := Real.sqrt κ
  let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
  let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
    (8 * (n : ℝ) * ((n : ℝ) - 1))
  let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
    fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
      (singleBlockPrecision κ O)⁻¹
  let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
      Real.exp (-((WithLp.ofLp x) ⬝ᵥ
        (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
  let v : ℝ := ((-1 : ℝ) ^ n / (n : ℝ)) * ((s - 1) / (s + 1)) ^ n *
    (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) / (1 - r ^ 2)
  change Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ => (O : Matrix (Fin n) (Fin n) ℝ).det *
      (∫ x, t x ∂γ O)) (orthogonalHaar n) ∧
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ => (O : Matrix (Fin n) (Fin n) ℝ).det *
      (∫ x, t x * p O x)) (orthogonalHaar n) ∧
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O)
      ∂orthogonalHaar n) = v ∧
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)
      ∂orthogonalHaar n) = v
  have ht := SelectedTilt.selected_tilt hn hκ
  have hg := GaussianExpectation.actual_gaussian_transform hn hκ
    (ℓ := ℓ) ht.2.2.1.le
  have hpoint : (fun O : Matrix.orthogonalGroup (Fin n) ℝ => (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O)) =ᵐ[
      orthogonalHaar n]
      (fun O : Matrix.orthogonalGroup (Fin n) ℝ => (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)) :=
    Filter.Eventually.of_forall fun O => congrArg
      (fun z => (O : Matrix (Fin n) (Fin n) ℝ).det * z) (hg.1 O).2.2
  have hvalue : (∫ O : Matrix.orthogonalGroup (Fin n) ℝ, (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O)
      ∂orthogonalHaar n) = v := by
    have hs := (SurfaceLaw.selected_surface_transport hn hκ).2.2.2
    have hm := (selected_numerator_value hn hκ).2
    rw [hm] at hs
    calc
      _ = (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (s + 1) ^ n) *
          (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) *
          (-(s - 1) / ((n : ℝ) * (1 - r ^ 2))) := hs
      _ = v := by
        have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast (by omega : n ≠ 0)
        have hsp : s + 1 ≠ 0 := ne_of_gt (by dsimp [s]; positivity)
        have hden : 1 - r ^ 2 ≠ 0 := by
          have hr : 0 < r := ht.1
          have hr1 : r < 1 := ht.2.1
          nlinarith
        have hpow (a : ℝ) : a ^ n = a ^ (n - 1) * a := by
          conv_lhs => rw [← Nat.sub_add_cancel (by omega : 1 ≤ n)]
          rw [pow_succ]
        dsimp only [v]
        rw [div_pow, hpow (-1), hpow (s - 1)]
        field_simp
  exact ⟨hg.2.1, hg.2.1.congr hpoint, hvalue,
    (integral_congr_ae hpoint.symm).trans hvalue⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.EvaluatedGaussian
