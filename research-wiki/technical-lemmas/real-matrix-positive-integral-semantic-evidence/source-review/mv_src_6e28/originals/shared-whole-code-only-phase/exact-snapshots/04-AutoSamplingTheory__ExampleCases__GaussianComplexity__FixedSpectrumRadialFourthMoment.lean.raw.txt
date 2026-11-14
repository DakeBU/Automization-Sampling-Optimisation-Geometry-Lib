import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.Distributions.Gaussian.Fernique
import Mathlib.Probability.Independence.Integration
import Mathlib.MeasureTheory.Integral.Pi
import Mathlib.MeasureTheory.SpecificCodomains.Pi
import Mathlib.Analysis.CStarAlgebra.Matrix

/-!
# The radial fourth matrix moment of a standard Gaussian row

Appendix C.2 Ex113 evaluates the unnormalized weighted second-moment matrix.
Its integrability and all scalar fourth and mixed moments are internal.
-/

noncomputable section
open MeasureTheory ProbabilityTheory WithLp
open scoped Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment

theorem actual_radial_fourth_moment_matrix
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let weighted : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => R x • G x
  Integrable weighted μ ∧
    (∫ x, weighted x ∂μ) = (r + 2) • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) := by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let weighted : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ := fun x => R x • G x
  let entry (i j : Fin (q + 1)) (x : E) : ℝ := R x * (x i * x j)
  have radius_four_integrable : Integrable (fun x : E => ‖x‖ ^ 4) μ :=
    (IsGaussian.memLp_id μ 4 (by norm_num)).integrable_norm_pow (by norm_num)
  have entry_integrable (i j : Fin (q + 1)) : Integrable (entry i j) μ := by
    have entry_continuous : Continuous (entry i j) := by
      exact (continuous_norm.pow 2).mul
        ((PiLp.continuous_apply 2 (fun _ : Fin (q + 1) => ℝ) i).mul
          (PiLp.continuous_apply 2 (fun _ : Fin (q + 1) => ℝ) j))
    apply radius_four_integrable.mono' entry_continuous.aestronglyMeasurable
    filter_upwards with x
    calc
      ‖entry i j x‖ = R x * (‖x i‖ * ‖x j‖) := by
        simp [entry, R, norm_mul, Real.norm_eq_abs]
      _ ≤ R x * (‖x‖ * ‖x‖) :=
        mul_le_mul_of_nonneg_left
          (mul_le_mul (PiLp.norm_apply_le x i) (PiLp.norm_apply_le x j)
            (norm_nonneg _) (norm_nonneg _)) (sq_nonneg _)
      _ = ‖x‖ ^ 4 := by dsimp [R]; ring
  let rows : E → Fin (q + 1) → Fin (q + 1) → ℝ := fun x i j => entry i j x
  have rows_integrable : Integrable rows μ :=
    Integrable.of_eval (fun i => Integrable.of_eval (fun j => entry_integrable i j))
  let ofRows : (Fin (q + 1) → Fin (q + 1) → ℝ) ≃L[ℝ]
      Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    (Matrix.ofLinearEquiv ℝ).toContinuousLinearEquiv
  have weighted_integrable : Integrable weighted μ := by
    change Integrable (fun x => ofRows (rows x)) μ
    exact ofRows.toContinuousLinearMap.integrable_comp rows_integrable
  have integral_entry (i j : Fin (q + 1)) :
      (∫ x, weighted x ∂μ) i j = ∫ x, entry i j x ∂μ := by
    have transport := ofRows.integral_comp_comm rows (μ := μ)
    change (∫ x, weighted x ∂μ) = ofRows (∫ x, rows x ∂μ) at transport
    rw [transport]
    change ((∫ x, rows x ∂μ) i) j = _
    rw [MeasureTheory.eval_integral (fun i => rows_integrable.eval i) i]
    exact MeasureTheory.eval_integral (fun j => entry_integrable i j) j

  -- A coordinate reflection preserves the law and radius, and negates an off-diagonal entry.
  have off_diagonal (i j : Fin (q + 1)) (hij : i ≠ j) :
      (∫ x, entry i j x ∂μ) = 0 := by
    let flip : E ≃ₗᵢ[ℝ] E :=
      LinearIsometryEquiv.piLpCongrRight 2 fun k : Fin (q + 1) =>
        if k = i then LinearIsometryEquiv.neg ℝ else LinearIsometryEquiv.refl ℝ ℝ
    have flip_apply (x : E) (k : Fin (q + 1)) :
        flip x k = if k = i then -x k else x k := by
      change (if k = i then (LinearIsometryEquiv.neg ℝ : ℝ ≃ₗᵢ[ℝ] ℝ)
        else LinearIsometryEquiv.refl ℝ ℝ) (x k) = _
      split_ifs <;> rfl
    have flip_entry (x : E) : entry i j (flip x) = -entry i j x := by
      have radius_eq : R (flip x) = R x := congrArg (fun t : ℝ => t ^ 2) (flip.norm_map x)
      simp only [entry, radius_eq, flip_apply]
      simp [hij.symm]
    have law : Measure.map flip μ = μ := stdGaussian_map flip
    have integrand_measurable : AEStronglyMeasurable (entry i j) (Measure.map flip μ) := by
      rw [law]
      exact (entry_integrable i j).aestronglyMeasurable
    have transport := integral_map flip.continuous.measurable.aemeasurable integrand_measurable
    rw [law] at transport
    simp_rw [flip_entry] at transport
    rw [integral_neg] at transport
    linarith

  -- The canonical coordinate pushforward exposes the independent scalar Gaussian laws.
  let ν : Measure (Fin (q + 1) → ℝ) := Measure.pi (fun _ => gaussianReal 0 1)
  have law : Measure.map (toLp 2) ν = μ := map_pi_eq_stdGaussian
  have pullback (f : E → ℝ) (hf : AEStronglyMeasurable f μ) :
      (∫ x, f x ∂μ) = ∫ u, f (toLp 2 u) ∂ν := by
    have hm : AEStronglyMeasurable f (Measure.map (toLp 2) ν) := by rwa [law]
    have transport := integral_map (φ := toLp 2) (μ := ν) (by fun_prop) hm
    rwa [law] at transport
  have scalar_integrable (n : ℕ) : Integrable (fun t : ℝ => t ^ n) (gaussianReal 0 1) := by
    have interior_point : (0 : ℝ) ∈ interior (integrableExpSet id (gaussianReal 0 1)) := by
      simp [integrableExpSet_id_gaussianReal]
    simpa only [Pi.pow_apply, id_eq] using
      integrable_pow_of_mem_interior_integrableExpSet interior_point n
  have coordinate_integrable (i : Fin (q + 1)) (n : ℕ) :
      Integrable (fun u : Fin (q + 1) → ℝ => (u i) ^ n) ν :=
    (measurePreserving_eval (fun _ : Fin (q + 1) => gaussianReal 0 1) i).integrable_comp_of_integrable
      (scalar_integrable n)
  have scalar_second : (∫ t : ℝ, t ^ 2 ∂gaussianReal 0 1) = 1 := by
    have moment := variance_id_gaussianReal (μ := 0) (v := 1)
    rw [variance_eq_integral (by fun_prop)] at moment
    simpa only [integral_id_gaussianReal, sub_zero, id_eq, NNReal.coe_one] using moment
  have coordinate_second (i : Fin (q + 1)) :
      (∫ u : Fin (q + 1) → ℝ, (u i) ^ 2 ∂ν) = 1 := by
    change (∫ u : Fin (q + 1) → ℝ, (u i) ^ 2 ∂Measure.pi (fun _ => gaussianReal 0 1)) = 1
    rw [integral_comp_eval (μ := fun _ : Fin (q + 1) => gaussianReal 0 1)
      (i := i) (f := fun t : ℝ => t ^ 2) (scalar_integrable 2).aestronglyMeasurable]
    exact scalar_second
  have coordinate_fourth (i : Fin (q + 1)) :
      (∫ u : Fin (q + 1) → ℝ, (u i) ^ 4 ∂ν) = 3 := by
    change (∫ u : Fin (q + 1) → ℝ, (u i) ^ 4 ∂Measure.pi (fun _ => gaussianReal 0 1)) = 3
    rw [integral_comp_eval (μ := fun _ : Fin (q + 1) => gaussianReal 0 1)
      (i := i) (f := fun t : ℝ => t ^ 4) (scalar_integrable 4).aestronglyMeasurable]
    simpa using
      AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment.integral_pow_four_gaussianReal_zero 1
  have independent_squares :
      iIndepFun (fun i : Fin (q + 1) => fun u : Fin (q + 1) → ℝ => (u i) ^ 2) ν :=
    iIndepFun_pi (X := fun _ : Fin (q + 1) => fun t : ℝ => t ^ 2) (fun _ => by fun_prop)
  have mixed_integrable (k i : Fin (q + 1)) :
      Integrable (fun u : Fin (q + 1) → ℝ => (u k) ^ 2 * (u i) ^ 2) ν := by
    by_cases hki : k = i
    · subst k
      convert coordinate_integrable i 4 using 1
      funext u
      ring
    · exact (independent_squares.indepFun hki).integrable_mul
        (coordinate_integrable k 2) (coordinate_integrable i 2)
  have mixed_value (k i : Fin (q + 1)) :
      (∫ u : Fin (q + 1) → ℝ, (u k) ^ 2 * (u i) ^ 2 ∂ν) =
        if k = i then 3 else 1 := by
    by_cases hki : k = i
    · subst k
      simp only [ite_true]
      simpa only [← pow_add] using coordinate_fourth i
    · rw [(independent_squares.indepFun hki).integral_fun_mul_eq_mul_integral
        (coordinate_integrable k 2).aestronglyMeasurable
        (coordinate_integrable i 2).aestronglyMeasurable, coordinate_second, coordinate_second]
      simp [hki]
  have diagonal_value (i : Fin (q + 1)) : (∫ x, entry i i x ∂μ) = r + 2 := by
    have entry_expansion (u : Fin (q + 1) → ℝ) :
        entry i i (toLp 2 u) = ∑ k : Fin (q + 1), (u k) ^ 2 * (u i) ^ 2 := by
      change ‖(toLp 2 u : E)‖ ^ 2 * (u i * u i) = _
      rw [EuclideanSpace.real_norm_sq_eq]
      change (∑ k : Fin (q + 1), (u k) ^ 2) * (u i * u i) = _
      simp only [Finset.sum_mul, pow_two]
    calc
      (∫ x, entry i i x ∂μ) = ∫ u, ∑ k : Fin (q + 1), (u k) ^ 2 * (u i) ^ 2 ∂ν := by
        rw [pullback _ (entry_integrable i i).aestronglyMeasurable]
        simp_rw [entry_expansion]
      _ = ∑ k : Fin (q + 1), ∫ u, (u k) ^ 2 * (u i) ^ 2 ∂ν :=
        integral_finsetSum _ (fun k _ => mixed_integrable k i)
      _ = ∑ k : Fin (q + 1), if k = i then (3 : ℝ) else 1 := by simp_rw [mixed_value]
      _ = ∑ k : Fin (q + 1), ((if k = i then (2 : ℝ) else 0) + 1) := by
        apply Finset.sum_congr rfl
        intro k _
        split_ifs <;> norm_num
      _ = r + 2 := by simp [Finset.sum_add_distrib, r]; ring
  refine ⟨weighted_integrable, ?_⟩
  change (∫ x, weighted x ∂μ) = (r + 2) • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ)
  ext i j
  rw [integral_entry]
  by_cases hij : i = j
  · subst j
    simpa using diagonal_value i
  · simpa [hij] using off_diagonal i j

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
