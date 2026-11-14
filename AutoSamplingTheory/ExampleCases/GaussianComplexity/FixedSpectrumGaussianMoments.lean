import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Tactic.Linarith

/-!
# Actual diagonal inverse-precision Gaussian quadratic means

Zhou--Suzuki, arXiv:2610.20492v1, Appendix C.3, Ex140.
The literal Gaussian measure has covariance Lambda inverse. Positivity,
coordinate second moments and both integrability facts are proved internally.
The focused test consumes these means in the actual Gaussian cosine alias
series; closed C8 sums, fourth moments, variance and bias are separate.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments

theorem actual_diagonal_gaussian_quadratic_means {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
  Integrable Q μ ∧
  (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) = (∑ i : Fin d, (eigenvalue i)⁻¹) ∧
  (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) / eigenvalue i := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  change Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
    Integrable Q μ ∧
    (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) = (∑ i : Fin d, (eigenvalue i)⁻¹) ∧
    (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
      ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) / eigenvalue i
  have heigenlower (i : Fin d) : 1 ≤ eigenvalue i := by
    dsimp [eigenvalue]
    have h := mul_nonneg (by linarith : 0 ≤ κ - 1)
      (by linarith [Real.neg_one_le_cos (θ i)] : 0 ≤ 1 + Real.cos (θ i))
    nlinarith
  have heigenpos (i : Fin d) : 0 < eigenvalue i := by linarith [heigenlower i]
  have heigenne (i : Fin d) : eigenvalue i ≠ 0 := ne_of_gt (heigenpos i)
  have hΛpos : Λ.PosDef := Matrix.PosDef.diagonal heigenpos
  have hinv : Λ⁻¹ = Matrix.diagonal (fun i => (eigenvalue i)⁻¹) := by
    apply Matrix.inv_eq_left_inv
    change Matrix.diagonal (fun i => (eigenvalue i)⁻¹) * Matrix.diagonal eigenvalue = 1
    ext i j
    by_cases hij : i = j
    · subst j
      simp [heigenne]
    · simp [hij]
  have hcoordL2 (i : Fin d) : MemLp (fun x : EuclideanSpace ℝ (Fin d) => x i) 2 μ :=
    IsGaussian.memLp_dual μ (EuclideanSpace.proj i) 2 (by simp)
  have hcoordint (i : Fin d) :
      Integrable (fun x : EuclideanSpace ℝ (Fin d) => (x i) ^ 2) μ :=
    (hcoordL2 i).integrable_sq
  have hmean (i : Fin d) : (∫ x : EuclideanSpace ℝ (Fin d), x i ∂μ) = 0 := by
    calc
      _ = (EuclideanSpace.proj i) (∫ x : EuclideanSpace ℝ (Fin d), x ∂μ) :=
        (EuclideanSpace.proj (𝕜 := ℝ) i).integral_comp_comm
          (μ := μ) (φ := fun x : EuclideanSpace ℝ (Fin d) => x)
          IsGaussian.integrable_fun_id
      _ = 0 := by simp [μ]
  have hmoment (i : Fin d) :
      (∫ x : EuclideanSpace ℝ (Fin d), (x i) ^ 2 ∂μ) = (eigenvalue i)⁻¹ := by
    have hentry : (Λ⁻¹ : Matrix (Fin d) (Fin d) ℝ) i i = (eigenvalue i)⁻¹ := by
      rw [hinv]
      simp
    have hv : Var[fun x : EuclideanSpace ℝ (Fin d) => x i; μ] = (eigenvalue i)⁻¹ :=
      (variance_eval_multivariateGaussian (μ := (0 : EuclideanSpace ℝ (Fin d)))
        hΛpos.inv.posSemidef i).trans hentry
    rw [variance_eq_integral (hcoordL2 i).aemeasurable] at hv
    simpa only [hmean, sub_zero] using hv
  have hnorm : (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) =
      (fun x => ∑ i : Fin d, (x i) ^ 2) :=
    funext EuclideanSpace.real_norm_sq_eq
  have hnormint : Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ := by
    rw [hnorm]
    exact integrable_finsetSum _ (fun i _ => hcoordint i)
  have hQint : Integrable Q μ :=
    integrable_finsetSum _ (fun i _ => (hcoordint i).const_mul _)
  refine ⟨hnormint, hQint, ?_, ?_⟩
  · rw [hnorm, integral_finsetSum _ (fun i _ => hcoordint i)]
    exact Finset.sum_congr rfl (fun i _ => hmoment i)
  · change (∫ x : EuclideanSpace ℝ (Fin d),
      ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (x i) ^ 2 ∂μ) = _
    rw [integral_finsetSum _ (fun i _ => (hcoordint i).const_mul _)]
    apply Finset.sum_congr rfl
    intro i _
    rw [integral_const_mul, hmoment]
    exact (div_eq_mul_inv _ _).symm

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments
