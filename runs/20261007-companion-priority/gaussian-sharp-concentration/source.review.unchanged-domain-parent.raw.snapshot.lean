import Mathlib.Probability.Distributions.Gaussian.Fernique
import Mathlib.Tactic

/-!
# Genuine Laplace domains for Lipschitz Gaussian observables

Fernique domination gives first moments and every signed centered exponential
moment on a real second-countable Banach Borel space. This proves the domain,
not the sharp Gaussian concentration coefficient. SPHMC's actual Gaussian
output consumes this leaf; its mean is its own Bochner mean, not an assumed
smoothed gradient. Degenerate Gaussian laws and zero Lipschitz constants remain
in the statement.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped NNReal ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential

theorem integrable_and_integrable_exp_centered_of_lipschitz
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [CompleteSpace E] [SecondCountableTopology E] [MeasurableSpace E] [BorelSpace E]
    {μ : MeasureTheory.Measure E} [ProbabilityTheory.IsGaussian μ]
    {L : ℝ≥0} {f : E → ℝ} (hf : LipschitzWith L f) :
    MeasureTheory.Integrable f μ ∧ ∀ t : ℝ,
      MeasureTheory.Integrable
        (fun x => Real.exp (t * (f x - ∫ z, f z ∂μ))) μ := by
  have hbound (x : E) : |f x| ≤ (L : ℝ)*‖x‖+|f 0| := by
    have hd := hf.dist_le_mul x 0
    simp only [dist_eq_norm, sub_zero, Real.norm_eq_abs] at hd
    calc
      |f x| = |(f x-f 0)+f 0| := by congr 1; ring
      _ ≤ |f x-f 0|+|f 0| := abs_add_le _ _
      _ ≤ (L : ℝ)*‖x‖+|f 0| := add_le_add hd le_rfl
  have hi : Integrable f μ :=
    (((IsGaussian.integrable_id (μ := μ)).norm.const_mul (L : ℝ)).add
      (integrable_const |f 0|)).mono' hf.continuous.aestronglyMeasurable
        (ae_of_all _ fun x => by simpa only [Real.norm_eq_abs, Pi.add_apply, id_eq] using hbound x)
  refine ⟨hi,fun t => ?_⟩
  obtain ⟨C,hC,hint⟩ := IsGaussian.exists_integrable_exp_sq μ
  let b : ℝ := |t| *(L : ℝ)
  let D : ℝ := |t| *(|f 0|+|∫ z, f z ∂μ|)
  have hb : 0 ≤ b := mul_nonneg (abs_nonneg _) L.coe_nonneg
  have hdom (x : E) : t*(f x-∫ z, f z ∂μ) ≤
      D+C⁻¹*b^2+C*‖x‖^2 := by
    have hlin : t*(f x-∫ z, f z ∂μ) ≤ b*‖x‖+D := by
      calc
        _ ≤ |t*(f x-∫ z, f z ∂μ)| := le_abs_self _
        _ = |t| *|f x-∫ z, f z ∂μ| := abs_mul _ _
        _ ≤ |t| *(|f x|+|∫ z, f z ∂μ|) :=
          mul_le_mul_of_nonneg_left (by simpa only [sub_zero, zero_sub, abs_neg] using
            (abs_sub_le (f x) 0 (∫ z, f z ∂μ))) (abs_nonneg _)
        _ ≤ |t| *((L : ℝ)*‖x‖+|f 0|+|∫ z, f z ∂μ|) :=
          mul_le_mul_of_nonneg_left (add_le_add (hbound x) le_rfl) (abs_nonneg _)
        _ = b*‖x‖+D := by dsimp [b,D]; ring
    have hy : 2*‖x‖*b ≤ C*‖x‖^2+C⁻¹*b^2 := two_mul_le_add_mul_sq hC
    have hnon : 0 ≤ b*‖x‖ := mul_nonneg hb (norm_nonneg _)
    nlinarith
  apply (hint.const_mul (Real.exp (D+C⁻¹*b^2))).mono'
    (by fun_prop)
  filter_upwards with x
  rw [Real.norm_eq_abs,abs_of_pos (Real.exp_pos _),← Real.exp_add]
  exact Real.exp_le_exp.mpr (hdom x)

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential
end
