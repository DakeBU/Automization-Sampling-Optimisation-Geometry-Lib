import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Tactic

/-!
# The squared norm of a finite-dimensional standard Gaussian

This is the coordinate-free second-moment identity needed by several sampling
algorithms.  Mathlib supplies the Gaussian `L²` fact and covariance identity;
finite-dimensional Parseval turns their directional form into the squared-norm
formula.  No independence, higher moment, or sampling-algorithm statement is
included here.
-/

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment

/-- A standard Gaussian on a finite-dimensional real inner-product space has
integrable squared norm, with expectation equal to the real dimension. -/
theorem integrable_norm_sq_and_integral_stdGaussian
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    Integrable (fun x : E => ‖x‖ ^ 2) (stdGaussian E) ∧
      (∫ x : E, ‖x‖ ^ 2 ∂stdGaussian E) = Module.finrank ℝ E := by
  classical
  have hi : Integrable (fun x : E => ‖x‖ ^ 2) (stdGaussian E) :=
    (memLp_two_iff_integrable_sq_norm (by fun_prop)).1 IsGaussian.memLp_two_id
  let b := stdOrthonormalBasis ℝ E
  have hdir (i) : (∫ x : E, (inner ℝ (b i) x) ^ 2 ∂stdGaussian E) = 1 := by
    have hh := covarianceBilin_apply (μ := stdGaussian E)
      IsGaussian.memLp_two_id (b i) (b i)
    rw [covarianceBilin_stdGaussian] at hh
    change inner ℝ (b i) (b i) = _ at hh
    simpa [integral_id_stdGaussian, real_inner_self_eq_norm_sq,
      b.orthonormal.norm_eq_one, pow_two] using hh.symm
  have hL1 (i) : Integrable (fun x : E => (inner ℝ (b i) x) ^ 2)
      (stdGaussian E) := by
    apply hi.mono' (by fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    have hb := norm_inner_le_norm (𝕜 := ℝ) (b i) x
    rw [b.orthonormal.norm_eq_one, one_mul] at hb
    have hsq := (sq_le_sq₀ (norm_nonneg (inner ℝ (b i) x)) (norm_nonneg x)).2 hb
    simpa [Real.norm_eq_abs, sq_abs] using hsq
  refine ⟨hi, ?_⟩
  calc
    (∫ x : E, ‖x‖ ^ 2 ∂stdGaussian E) =
        ∫ x : E, ∑ i, (inner ℝ (b i) x) ^ 2 ∂stdGaussian E := by
      apply integral_congr_ae
      filter_upwards with x
      simpa [Real.norm_eq_abs, sq_abs] using (b.sum_sq_norm_inner_right x).symm
    _ = ∑ i, ∫ x : E, (inner ℝ (b i) x) ^ 2 ∂stdGaussian E :=
      integral_finsetSum _ (fun i _ => hL1 i)
    _ = Module.finrank ℝ E := by simp [hdir]

end AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
