import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import GC47GaussianZero
import GC44GramUse

open Matrix MeasureTheory ProbabilityTheory
open scoped BigOperators
set_option autoImplicit false

/-! Exact expectations of both cosine Gram matrices in Appendix C, Fact C.5.
The flat-coordinate calculation follows the repository's Gaussian Gram regression proof. -/

noncomputable section
open scoped Matrix.Norms.L2Operator
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

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

private theorem matrix_mean {J Ω : Type*} [Fintype J] [DecidableEq J] [MeasurableSpace Ω]
    (μ : Measure Ω) (Y : Ω → Matrix J J ℝ) (M : Matrix J J ℝ)
    (h : ∀ i j, Integrable (fun ω => Y ω i j) μ ∧ (∫ ω, Y ω i j ∂μ) = M i j) :
    Integrable Y μ ∧ (∫ ω, Y ω ∂μ) = M := by
  let rows (ω : Ω) (i j : J) := Y ω i j
  have hi : Integrable rows μ := Integrable.of_eval (fun i => Integrable.of_eval (fun j => (h i j).1))
  let e : (J → J → ℝ) ≃L[ℝ] Matrix J J ℝ := (Matrix.ofLinearEquiv ℝ).toContinuousLinearEquiv
  refine ⟨e.toContinuousLinearMap.integrable_comp hi, ?_⟩
  change (∫ ω, e (rows ω) ∂μ) = M
  rw [e.integral_comp_comm rows]
  ext i j
  change ((∫ ω, rows ω ∂μ) i) j = _
  rw [MeasureTheory.eval_integral (fun i => hi.eval i) i,
    MeasureTheory.eval_integral (fun j => (h i j).1) j, (h i j).2]

/-- The paper's actual independent starting vectors, on any probability space.
Both Bochner matrix expectations and both integrability assertions hold. -/
theorem independent_start_gram_means {d q : ℕ} (hq : 2*q+1 < d)
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) (g : Fin (q+1) → Ω → Space d)
    (hg : ∀ a, MeasurePreserving (g a) μ (stdGaussian (Space d))) (hi : iIndepFun g μ) :
    let B := fun ω => feature d q (fun a => g a ω)
    Integrable (fun ω => (B ω).transpose * B ω) μ ∧
    Integrable (fun ω => (B ω).transpose * cosineDiag d q * B ω) μ ∧
    (∫ ω, (B ω).transpose * B ω ∂μ) = 1 ∧
    (∫ ω, (B ω).transpose * cosineDiag d q * B ω ∂μ) = 0 := by
  classical
  let f (ω : Ω) : Starts d q := fun a => g a ω
  have hf : MeasurePreserving f μ (Measure.pi (fun _ => stdGaussian (Space d))) := by
    refine ⟨measurable_pi_lambda _ (fun a => (hg a).measurable), ?_⟩
    change μ.map (fun ω a => g a ω) = _
    rw [hi.map_fun_eq_pi_map (fun a => (hg a).measurable.aemeasurable)]
    simp_rw [fun a => (hg a).map_eq]
  let I := Fin d × Fin (q+1)
  let E := EuclideanSpace ℝ I
  let ν := stdGaussian E
  let F (ω : Ω) : E := WithLp.toLp 2 (fun i => g i.2 ω i.1)
  have hF : MeasurePreserving F μ ν :=
    (show MeasurePreserving (MeasurableEquiv.toLp 2 (I → ℝ))
      (Measure.pi (fun _ => gaussianReal 0 1)) ν from
      ⟨(MeasurableEquiv.toLp 2 (I → ℝ)).measurable, map_pi_eq_stdGaussian⟩).comp
        ((FixedSpectrumSaturation.flatten_gaussian_starts d (q+1)).comp hf)
  let B (x : E) := feature d q (fun a => WithLp.toLp 2 (fun i => x (i,a)))
  let Y (x : E) := (B x).transpose * B x
  let W (x : E) := (B x).transpose * cosineDiag d q * B x
  have hm := actual_gaussian_gram_means hq
  dsimp only at hm
  rw [multivariateGaussian_zero_one] at hm
  change ∀ a b, Integrable (fun x => Y x a b) ν ∧ Integrable (fun x => W x a b) ν ∧
    (∫ x, Y x a b ∂ν) = (if a = b then 1 else 0) ∧ (∫ x, W x a b ∂ν) = 0 at hm
  have hY := matrix_mean ν Y 1 (fun a b => ⟨(hm a b).1, (hm a b).2.2.1⟩)
  have hW := matrix_mean ν W 0 (fun a b => ⟨(hm a b).2.1, (hm a b).2.2.2⟩)
  have integral (H : E → Matrix (Indices q) (Indices q) ℝ) (h : Integrable H ν) :
      (∫ ω, H (F ω) ∂μ) = ∫ x, H x ∂ν := by
    rw [← hF.map_eq] at h ⊢
    exact (integral_map hF.measurable.aemeasurable h.aestronglyMeasurable).symm
  exact ⟨(hF.integrable_comp hY.1.aestronglyMeasurable).2 hY.1,
    (hF.integrable_comp hW.1.aestronglyMeasurable).2 hW.1,
    (integral Y hY.1).trans hY.2,
    (integral W hW.1).trans hW.2⟩

#print axioms independent_start_gram_means
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
