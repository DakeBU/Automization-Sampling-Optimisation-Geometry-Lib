import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments

open Matrix InnerProductSpace MeasureTheory ProbabilityTheory
open scoped BigOperators
set_option autoImplicit false

/-!
Actual target norm-square consumer. The full rotated Gaussian law is genuinely
used to transport canonical diagonal L1 and the finite inverse-spectrum mean.
No moment/law/integrability certificate is an input. This is the norm component,
not all Lemma4.5, a pass probability, algorithm or query/cost assertion.
-/
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumTargetLaw

private theorem actual_target_gaussian_norm_mean {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ) (O : Matrix.orthogonalGroup (Fin d) ℝ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
  Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
    (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) =
      ∑ i : Fin d, ((κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))⁻¹
:= by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin d)
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let μ : Measure E := multivariateGaussian (0 : E) Λ⁻¹
  let ν : Measure E := multivariateGaussian (0 : E) A⁻¹
  let R : E → E := fun z =>
    WithLp.toLp 2 ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z)
  let g : E → ℝ := fun x => ‖x‖ ^ 2
  have hLaw : μ.map R = ν :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw.actual_rotated_gaussian_target hd hκ O
  have hm :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments.actual_diagonal_gaussian_quadratic_means
      hd hκ 1 (by decide) (Nat.lt_of_lt_of_le (by decide : 1 < 2) hd)
  have hLint : Integrable g μ := hm.1
  have hmean : (∫ x, g x ∂μ) =
      ∑ i : Fin d, ((κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))⁻¹ := hm.2.2.1
  have hR : Measurable R :=
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) (O : Matrix (Fin d) (Fin d) ℝ)).continuous.measurable
  have hnorm (z : E) : ‖R z‖ = ‖z‖ :=
    ContinuousLinearMap.norm_map_of_mem_unitary
      (Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)) O.property) z
  have hg : Continuous g := continuous_norm.pow 2
  have hcomp : g ∘ R = g := by
    funext z
    change ‖R z‖ ^ 2 = ‖z‖ ^ 2
    rw [hnorm]
  have hmapLint : Integrable g (μ.map R) :=
    (integrable_map_measure hg.aestronglyMeasurable hR.aemeasurable).2
      (by rw [hcomp]; exact hLint)
  change Integrable g ν ∧ (∫ x, g x ∂ν) = _
  rw [← hLaw]
  refine ⟨hmapLint, ?_⟩
  rw [integral_map hR.aemeasurable hg.aestronglyMeasurable]
  change (∫ x, (g ∘ R) x ∂μ) = _
  rw [hcomp]
  exact hmean

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumTargetLaw
