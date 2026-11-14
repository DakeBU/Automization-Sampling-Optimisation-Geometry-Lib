import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import Mathlib.Probability.Distributions.Gaussian.Multivariate

open Matrix MeasureTheory ProbabilityTheory
open scoped BigOperators
set_option autoImplicit false

/-! Actual Gaussian Gram integrability and means consume the cosine-frame identities.
No independent/moment/Gram or integrability certificate is supplied by the caller;
range/Krylov, concentration, oracle/cap/cost and full lower bounds are separate. -/
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumCosineGram

private theorem actual_gaussian_gram_means {d q : ℕ} (hq : 2 * q + 1 < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  let μ : Measure (EuclideanSpace ℝ (Fin d × Fin (q + 1))) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d × Fin (q + 1)))
      (1 : Matrix (Fin d × Fin (q + 1)) (Fin d × Fin (q + 1)) ℝ)
  let B : EuclideanSpace ℝ (Fin d × Fin (q + 1)) →
      Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun x i a =>
    (Real.sqrt (d : ℝ))⁻¹ * WithLp.ofLp x (i, a.1) * t i a.2
  ∀ a b : Fin (q + 1) × Fin (q + 1),
    Integrable (fun x => ((B x).transpose * B x) a b) μ ∧
    Integrable (fun x => ((B x).transpose * D * B x) a b) μ ∧
    (∫ x, ((B x).transpose * B x) a b ∂μ) = (if a = b then 1 else 0) ∧
    (∫ x, ((B x).transpose * D * B x) a b ∂μ) = 0
:= by
  classical
  dsimp only
  let I := Fin d × Fin (q + 1)
  let J := Fin (q + 1) × Fin (q + 1)
  let E := EuclideanSpace ℝ I
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let D : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal w
  let μ : Measure E := multivariateGaussian (0 : E) (1 : Matrix I I ℝ)
  let scale : ℝ := (Real.sqrt (d : ℝ))⁻¹
  let B : E → Matrix (Fin d) J ℝ := fun x i a => scale * x (i, a.1) * t i a.2
  have hframe :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram hq
  change t.transpose * t = (d : ℝ) • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) ∧
    t.transpose * D * t = 0 ∧
    (∀ i : Fin d, ∑ k : Fin (q + 1), (t i k) ^ 2 ≤ 2 * ((q : ℝ) + 1)) at hframe
  have hgram (j k : Fin (q + 1)) :
      (∑ i : Fin d, t i j * t i k) = if j = k then (d : ℝ) else 0 := by
    have h := congrArg (fun M : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ => M j k) hframe.1
    change (∑ i : Fin d, t i j * t i k) = (d : ℝ) * (if j = k then 1 else 0) at h
    simpa only [mul_ite, mul_one, mul_zero] using h
  have hweighted (j k : Fin (q + 1)) :
      (∑ i : Fin d, t i j * w i * t i k) = 0 := by
    have h := congrArg (fun M : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ => M j k) hframe.2.1
    change (∑ i : Fin d, (t.transpose * D) j i * t i k) = 0 at h
    simpa only [D, Matrix.mul_diagonal, Matrix.transpose_apply] using h
  have hL2 (u : I) : MemLp (fun x : E => x u) 2 μ :=
    IsGaussian.memLp_dual μ (EuclideanSpace.proj u) 2 (by simp)
  have hmean (u : I) : (∫ x : E, x u ∂μ) = 0 := by
    calc
      _ = (EuclideanSpace.proj u) (∫ x : E, x ∂μ) :=
        (EuclideanSpace.proj (𝕜 := ℝ) u).integral_comp_comm
          (μ := μ) (φ := fun x : E => x) IsGaussian.integrable_fun_id
      _ = 0 := by
        rw [show (∫ x : E, x ∂μ) = (0 : E) from integral_id_multivariateGaussian]
        exact map_zero _
  have hxyint (u v : I) : Integrable (fun x : E => x u * x v) μ :=
    (hL2 u).integrable_mul (hL2 v)
  have hxymean (u v : I) :
      (∫ x : E, x u * x v ∂μ) = if u = v then (1 : ℝ) else 0 := by
    have h := covariance_eval_multivariateGaussian (μ := (0 : E))
      (S := (1 : Matrix I I ℝ)) Matrix.PosSemidef.one u v
    change covariance (fun x : E => x u) (fun x : E => x v) μ =
      (if u = v then (1 : ℝ) else 0) at h
    simpa only [covariance, hmean, sub_zero] using h
  have hdpos : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hscale : scale ^ 2 * (d : ℝ) = 1 := by
    dsimp only [scale]
    rw [inv_pow, Real.sq_sqrt hdpos.le]
    exact inv_mul_cancel₀ (ne_of_gt hdpos)
  have hf (a b : J) : (fun x : E => ((B x).transpose * B x) a b) =
      (fun x : E => ∑ i : Fin d, (scale ^ 2 * (t i a.2 * t i b.2)) *
        (x (i, a.1) * x (i, b.1))) := by
    funext x
    change (∑ i : Fin d, B x i a * B x i b) = _
    apply Finset.sum_congr rfl
    intro i _
    dsimp only [B]
    ring
  have hfw (a b : J) : (fun x : E => ((B x).transpose * D * B x) a b) =
      (fun x : E => ∑ i : Fin d, (scale ^ 2 * (t i a.2 * w i * t i b.2)) *
        (x (i, a.1) * x (i, b.1))) := by
    funext x
    change (∑ i : Fin d, ((B x).transpose * D) a i * B x i b) = _
    apply Finset.sum_congr rfl
    intro i _
    simp only [D, Matrix.mul_diagonal]
    change (scale * x (i, a.1) * t i a.2) * w i *
      (scale * x (i, b.1) * t i b.2) = _
    ring
  change ∀ a b : J,
    Integrable (fun x : E => ((B x).transpose * B x) a b) μ ∧
    Integrable (fun x : E => ((B x).transpose * D * B x) a b) μ ∧
    (∫ x : E, ((B x).transpose * B x) a b ∂μ) = (if a = b then 1 else 0) ∧
    (∫ x : E, ((B x).transpose * D * B x) a b ∂μ) = 0
  intro a b
  have hi (i : Fin d) : Integrable (fun x : E =>
      (scale ^ 2 * (t i a.2 * t i b.2)) * (x (i, a.1) * x (i, b.1))) μ :=
    (hxyint (i, a.1) (i, b.1)).const_mul _
  have hwi (i : Fin d) : Integrable (fun x : E =>
      (scale ^ 2 * (t i a.2 * w i * t i b.2)) * (x (i, a.1) * x (i, b.1))) μ :=
    (hxyint (i, a.1) (i, b.1)).const_mul _
  have hdelta (i : Fin d) : (if (i, a.1) = (i, b.1) then (1 : ℝ) else 0) =
      (if a.1 = b.1 then 1 else 0) := by simp
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [hf]
    exact integrable_finsetSum _ (fun i _ => hi i)
  · rw [hfw]
    exact integrable_finsetSum _ (fun i _ => hwi i)
  · rw [hf, integral_finsetSum _ (fun i _ => hi i)]
    simp_rw [integral_const_mul, hxymean, hdelta]
    calc
      _ = (if a.1 = b.1 then (1 : ℝ) else 0) * scale ^ 2 *
          (∑ i : Fin d, t i a.2 * t i b.2) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        ring
      _ = _ := by
        rw [hgram]
        by_cases h1 : a.1 = b.1
        · by_cases h2 : a.2 = b.2
          · have heq : a = b := Prod.ext h1 h2
            simp only [if_pos h1, if_pos h2, if_pos heq, one_mul]
            exact hscale
          · have hne : a ≠ b := fun h => h2 (congrArg Prod.snd h)
            simp [h1, h2, hne]
        · have hne : a ≠ b := fun h => h1 (congrArg Prod.fst h)
          simp [h1, hne]
  · rw [hfw, integral_finsetSum _ (fun i _ => hwi i)]
    simp_rw [integral_const_mul, hxymean, hdelta]
    calc
      _ = (if a.1 = b.1 then (1 : ℝ) else 0) * scale ^ 2 *
          (∑ i : Fin d, t i a.2 * w i * t i b.2) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro i _
        ring
      _ = 0 := by rw [hweighted]; ring

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumCosineGram
