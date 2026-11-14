import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment
import Mathlib.Probability.Moments.MGFAnalytic
import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence

/-!
# Actual diagonal Gaussian quadratic variances

Zhou--Suzuki arXiv:2610.20492v1, Appendix C.3, Ex148--149 and p8.2.
Fourth moments, square integrability and coordinate independence are proved
internally for the literal inverse-precision Gaussian. The private test uses
both quadratic variances in the numerical contrast variance bound of Ex25.
The full rotated sampling test and main lower bounds remain separate.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal NNReal Topology
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

private theorem centered_gaussian_square_L2 (v : ℝ≥0) :
    MemLp (fun x : ℝ => x ^ 2) 2 (gaussianReal 0 v) := by
  have hint : (0 : ℝ) ∈ interior (integrableExpSet id (gaussianReal 0 v)) := by
    simp [integrableExpSet_id_gaussianReal]
  have hi := integrable_pow_of_mem_interior_integrableExpSet hint 4
  apply (memLp_two_iff_integrable_sq_norm (by fun_prop)).2
  simpa only [Pi.pow_apply, id_eq, Real.norm_eq_abs, sq_abs, ← pow_mul] using hi

private theorem centered_gaussian_square_variance (v : ℝ≥0) :
    Var[fun x : ℝ => x ^ 2; gaussianReal 0 v] = 2 * (v : ℝ) ^ 2 := by
  have hm2 : (∫ x : ℝ, x ^ 2 ∂gaussianReal 0 v) = (v : ℝ) := by
    have hv := variance_id_gaussianReal (μ := 0) (v := v)
    rw [variance_eq_integral (by fun_prop)] at hv
    simpa only [integral_id_gaussianReal, sub_zero, id_eq] using hv
  rw [variance_eq_sub (centered_gaussian_square_L2 v)]
  change (∫ x : ℝ, (x ^ 2) ^ 2 ∂gaussianReal 0 v) -
    (∫ x : ℝ, x ^ 2 ∂gaussianReal 0 v) ^ 2 = _
  simp only [← pow_mul, hm2,
    AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment.integral_pow_four_gaussianReal_zero]
  ring

theorem actual_diagonal_gaussian_quadratic_variances {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  MemLp (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) 2 μ ∧
  MemLp Q 2 μ ∧
  Var[fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2; μ] =
    2 * ∑ i : Fin d, 1 / (eigenvalue i) ^ 2 ∧
  Var[Q; μ] = 2 * ∑ i : Fin d, (Real.cos ((n : ℝ) * θ i)) ^ 2 / (eigenvalue i) ^ 2 ∧
  Var[fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2; μ] ≤ 2 * M ∧
  Var[Q; μ] ≤ 2 * M ∧
  2 * M ≤ 2 * (d : ℝ) / Real.sqrt κ := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  change MemLp (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) 2 μ ∧
    MemLp Q 2 μ ∧
    Var[fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2; μ] =
      2 * ∑ i : Fin d, 1 / (eigenvalue i) ^ 2 ∧
    Var[Q; μ] = 2 * ∑ i : Fin d, (Real.cos ((n : ℝ) * θ i)) ^ 2 / (eigenvalue i) ^ 2 ∧
    Var[fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2; μ] ≤ 2 * M ∧
    Var[Q; μ] ≤ 2 * M ∧ 2 * M ≤ 2 * (d : ℝ) / Real.sqrt κ
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
  have hcoord (i : Fin d) :
      MemLp (fun x : EuclideanSpace ℝ (Fin d) => (x i) ^ 2) 2 μ ∧
      Var[fun x : EuclideanSpace ℝ (Fin d) => (x i) ^ 2; μ] =
        2 * ((eigenvalue i)⁻¹) ^ 2 := by
    have hentry : (Λ⁻¹ : Matrix (Fin d) (Fin d) ℝ) i i = (eigenvalue i)⁻¹ := by
      rw [hinv]
      simp
    have hmp := measurePreserving_eval_multivariateGaussian
      (μ := (0 : EuclideanSpace ℝ (Fin d))) hΛpos.inv.posSemidef (i := i)
    simp only [PiLp.zero_apply, hentry] at hmp
    have hnonneg : 0 ≤ (eigenvalue i)⁻¹ := inv_nonneg.mpr (heigenpos i).le
    refine ⟨(centered_gaussian_square_L2 _).comp_measurePreserving hmp, ?_⟩
    rw [hmp.variance_fun_comp (f := fun t : ℝ => t ^ 2) (by fun_prop),
      centered_gaussian_square_variance,
      Real.coe_toNNReal _ hnonneg]
  have hjoint : HasGaussianLaw
      (fun x : EuclideanSpace ℝ (Fin d) => fun i : Fin d => x i) μ := by
    exact (IsGaussian.hasGaussianLaw_id (μ := μ)).map_equiv_fun
      (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin d => ℝ))
  have hindep : iIndepFun (fun i : Fin d => fun x : EuclideanSpace ℝ (Fin d) => x i) μ := by
    apply hjoint.iIndepFun_of_covariance_eq_zero
    intro i j hij
    rw [covariance_eval_multivariateGaussian hΛpos.inv.posSemidef, hinv]
    simp [hij]
  have hweighted (a : Fin d → ℝ) :
      MemLp (fun x : EuclideanSpace ℝ (Fin d) => ∑ i : Fin d, a i * (x i) ^ 2) 2 μ ∧
      Var[fun x : EuclideanSpace ℝ (Fin d) => ∑ i : Fin d, a i * (x i) ^ 2; μ] =
        2 * ∑ i : Fin d, (a i) ^ 2 / (eigenvalue i) ^ 2 := by
    have hl2 (i : Fin d) : MemLp (fun x : EuclideanSpace ℝ (Fin d) => a i * (x i) ^ 2) 2 μ :=
      (hcoord i).1.const_mul _
    refine ⟨memLp_finsetSum _ (fun i _ => hl2 i), ?_⟩
    have hpair : Set.Pairwise (↑(Finset.univ : Finset (Fin d)))
        (fun i j => IndepFun (fun x : EuclideanSpace ℝ (Fin d) => a i * (x i) ^ 2)
          (fun x => a j * (x j) ^ 2) μ) := by
      intro i _ j _ hij
      exact (hindep.indepFun hij).comp
        (φ := fun t : ℝ => a i * t ^ 2) (ψ := fun t : ℝ => a j * t ^ 2)
        (by fun_prop) (by fun_prop)
    have hv := IndepFun.variance_sum (fun i _ => hl2 i) hpair
    have hfun : (∑ i : Fin d, fun x : EuclideanSpace ℝ (Fin d) => a i * (x i) ^ 2) =
        (fun x => ∑ i : Fin d, a i * (x i) ^ 2) := by
      funext x
      simp only [Finset.sum_apply]
    rw [hfun] at hv
    rw [hv, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [variance_const_mul, (hcoord i).2, div_eq_mul_inv, inv_pow]
    ring
  have hnorm : (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) =
      (fun x => ∑ i : Fin d, (x i) ^ 2) := funext EuclideanSpace.real_norm_sq_eq
  have hnormw := hweighted (fun _ => 1)
  simp only [one_mul, one_pow] at hnormw
  rw [← hnorm] at hnormw
  have hQw := hweighted (fun i => Real.cos ((n : ℝ) * θ i))
  have hmean : M = ∑ i : Fin d, (eigenvalue i)⁻¹ :=
    (actual_diagonal_gaussian_quadratic_means hd hκ n hn hnd).2.2.1
  have hinvupper (i : Fin d) : (eigenvalue i)⁻¹ ≤ 1 :=
    (inv_le_one₀ (heigenpos i)).2 (heigenlower i)
  have hsqinv (i : Fin d) : 1 / (eigenvalue i) ^ 2 ≤ (eigenvalue i)⁻¹ := by
    have hp : 0 ≤ (eigenvalue i)⁻¹ := inv_nonneg.mpr (heigenpos i).le
    have h := mul_le_mul_of_nonneg_left (hinvupper i) hp
    simpa only [div_eq_mul_inv, one_mul, inv_pow, pow_two, mul_one, mul_inv_rev] using h
  have hcosbound (i : Fin d) :
      (Real.cos ((n : ℝ) * θ i)) ^ 2 / (eigenvalue i) ^ 2 ≤ (eigenvalue i)⁻¹ := by
    calc
      _ ≤ 1 / (eigenvalue i) ^ 2 :=
        div_le_div_of_nonneg_right (Real.cos_sq_le_one _) (sq_nonneg _)
      _ ≤ _ := hsqinv i
  have hnormbound : Var[fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2; μ] ≤ 2 * M := by
    rw [hnormw.2, hmean]
    exact mul_le_mul_of_nonneg_left (Finset.sum_le_sum (fun i _ => hsqinv i)) (by norm_num)
  have hQbound : Var[Q; μ] ≤ 2 * M := by
    rw [hQw.2, hmean]
    exact mul_le_mul_of_nonneg_left (Finset.sum_le_sum (fun i _ => hcosbound i)) (by norm_num)
  have hclosed := actual_diagonal_gaussian_exact_means hd hκ n hn hnd
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  have hm : M = ((d : ℝ) / Real.sqrt κ) *
      ((1 - r ^ (2 * d)) / (1 + r ^ (2 * d))) := hclosed.2.2.1
  have hsqrt : 1 < Real.sqrt κ := by
    nlinarith [Real.sqrt_nonneg κ, Real.sq_sqrt (by linarith : 0 ≤ κ)]
  have hr0 : 0 < r := div_pos (by linarith) (by linarith)
  have hscale : 0 ≤ (d : ℝ) / Real.sqrt κ := div_nonneg (Nat.cast_nonneg _) (by linarith)
  have hpow : 0 ≤ r ^ (2 * d) := pow_nonneg hr0.le _
  have hden : 0 < 1 + r ^ (2 * d) := by positivity
  have hMupper : M ≤ (d : ℝ) / Real.sqrt κ := by
    rw [hm]
    exact mul_le_of_le_one_right hscale ((div_le_one hden).2 (by linarith))
  refine ⟨hnormw.1, hQw.1, hnormw.2, hQw.2, hnormbound, hQbound, ?_⟩
  calc
    2 * M ≤ 2 * ((d : ℝ) / Real.sqrt κ) := mul_le_mul_of_nonneg_left hMupper (by norm_num)
    _ = 2 * (d : ℝ) / Real.sqrt κ := by ring

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances
