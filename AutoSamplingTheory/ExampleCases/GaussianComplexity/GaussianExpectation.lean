import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureFubini
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-!
# Actual signed Gaussian test expectation through Eq21

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.2.2 H definition through Eq21.
Bounded-test Gaussian L1, weighted-volume L1, exact density transport and outer
signed Haar L1 are produced internally using identical compiled parents.
Conditioned target mixtures, H-to-TV, Poisson and main bounds remain separate.
-/

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureFubini

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation

theorem actual_gaussian_transform {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) {ℓ : ℝ} (hℓ : 0 ≤ ℓ) :
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
    let a : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => κ + 1 + 4 * ℓ - (κ - 1) * U O
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
          Real.exp (-((WithLp.ofLp x) ⬝ᵥ
            (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    (∀ O, Integrable t (γ O) ∧ Integrable (fun x => t x * p O x) volume ∧
      (∫ x, t x ∂γ O) = ∫ x, t x * p O x) ∧
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O)) (orthogonalHaar n) ∧
    (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O) ∂orthogonalHaar n) =
      ((-1 : ℝ) ^ (n - 1) * (Real.sqrt κ - 1) ^ (n - 1) /
        (2 : ℝ) ^ ((n : ℝ) / 2)) *
        (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
          ((Real.sqrt κ + 1) * U O - (Real.sqrt κ - 1)) /
            (a O) ^ ((n : ℝ) / 2) ∂orthogonalHaar n) := by
  classical
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
  let a : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => κ + 1 + 4 * ℓ - (κ - 1) * U O
  let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
  let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
    fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
      (singleBlockPrecision κ O)⁻¹
  have htcont : Continuous t := by dsimp [t]; fun_prop
  have htbound (x : EuclideanSpace ℝ (Fin n)) : ‖t x‖ ≤ 1 := by
    dsimp [t]
    rw [abs_of_pos (Real.exp_pos _)]
    apply Real.exp_le_one_iff.mpr
    exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hℓ) (sq_nonneg _)
  have hp0 (O : Matrix.orthogonalGroup (Fin n) ℝ) (x : EuclideanSpace ℝ (Fin n)) :
      0 ≤ p O x := by dsimp [p]; positivity
  have hpmeas (O : Matrix.orthogonalGroup (Fin n) ℝ) :
      Measurable (fun x => ENNReal.ofReal (p O x)) := by dsimp [p]; fun_prop
  have hfinite (O : Matrix.orthogonalGroup (Fin n) ℝ) :
      ∀ᵐ x ∂(volume : Measure (EuclideanSpace ℝ (Fin n))),
        ENNReal.ofReal (p O x) < ⊤ := Filter.Eventually.of_forall fun _ => ENNReal.ofReal_lt_top
  have hpoint (O : Matrix.orthogonalGroup (Fin n) ℝ) :
      Integrable t (γ O) ∧ Integrable (fun x => t x * p O x) volume ∧
        (∫ x, t x ∂γ O) = ∫ x, t x * p O x := by
    let : IsProbabilityMeasure (γ O) := by dsimp [γ]; infer_instance
    have htL : Integrable t (γ O) :=
      (integrable_const (1 : ℝ)).mono' htcont.aestronglyMeasurable
        (Filter.Eventually.of_forall htbound)
    have hd : γ O = volume.withDensity (fun x => ENNReal.ofReal (p O x)) :=
      gaussian_law_eq_density hn hκ O
    have htd : Integrable t (volume.withDensity (fun x => ENNReal.ofReal (p O x))) := by
      rw [← hd]
      exact htL
    have hw := (integrable_withDensity_iff (hpmeas O) (hfinite O)).mp htd
    have hw' : Integrable (fun x => t x * p O x) volume := by
      simpa only [ENNReal.toReal_ofReal (hp0 O _)] using hw
    refine ⟨htL, hw', ?_⟩
    rw [hd, integral_withDensity_eq_integral_toReal_smul (hpmeas O) (hfinite O)]
    apply integral_congr_ae
    exact Filter.Eventually.of_forall fun x => by
      change (ENNReal.ofReal (p O x)).toReal * t x = t x * p O x
      rw [ENNReal.toReal_ofReal (hp0 O x), mul_comm]
  have hlit := literal_mixture_transform hn hκ hℓ
  have hjoint : Integrable
      (fun z : Matrix.orthogonalGroup (Fin n) ℝ × EuclideanSpace ℝ (Fin n) =>
        (z.1 : Matrix (Fin n) (Fin n) ℝ).det * (t z.2 * p z.1 z.2))
      ((orthogonalHaar n).prod volume) := hlit.1
  have houter : Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O)) (orthogonalHaar n) := by
    have hi := hjoint.integral_prod_left
    apply hi.congr
    exact Filter.Eventually.of_forall fun O => by
      change (∫ x, (O : Matrix (Fin n) (Fin n) ℝ).det * (t x * p O x)) =
        (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O)
      rw [integral_const_mul, (hpoint O).2.2]
  refine ⟨hpoint, houter, ?_⟩
  calc
    _ = (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)
          ∂orthogonalHaar n) := by
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun O => by
        change (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x ∂γ O) =
          (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)
        rw [(hpoint O).2.2]
    _ = _ := hlit.2.2

end AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation
