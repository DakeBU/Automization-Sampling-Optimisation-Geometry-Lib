import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity

/-!
# Actual Gaussian law equals the literal determinant-family precision density

Zhou--Suzuki arXiv:2610.20492v1, Eq4, AppendixB2.2 density p_O and Eq26.
The source lower bound supplies SPD internally, then the exact canonical shared
Gaussian precision-density theorem is consumed. Mixture/TV claims are separate.
-/

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity

theorem gaussian_law_eq_density {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) (O : Matrix.orthogonalGroup (Fin n) ℝ) :
    ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹ =
      (volume : Measure (EuclideanSpace ℝ (Fin n))).withDensity (fun x =>
        ENNReal.ofReal (Real.sqrt (singleBlockPrecision κ O).det /
          (2 * Real.pi) ^ ((n : ℝ) / 2) *
            Real.exp (-((WithLp.ofLp x) ⬝ᵥ
              (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2))) := by
  have hr := singleBlockPrecision_regular hn hκ O
  have hA : (singleBlockPrecision κ O).PosDef := by
    apply Matrix.posDef_iff_dotProduct_mulVec.mpr
    refine ⟨hr.1, ?_⟩
    intro v hv
    have hvE : (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin n)) ≠ 0 := by
      intro h
      exact hv (congrArg WithLp.ofLp h)
    have hp := sq_pos_of_pos (norm_pos_iff.mpr hvE)
    rw [EuclideanSpace.real_norm_sq_eq] at hp
    have hdot : 0 < v ⬝ᵥ v := by simpa only [dotProduct, pow_two] using hp
    simpa only [star_trivial] using lt_of_lt_of_le hdot (hr.2 v).1
  exact multivariateGaussian_eq_withDensity_of_posDef _ hA

end AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
