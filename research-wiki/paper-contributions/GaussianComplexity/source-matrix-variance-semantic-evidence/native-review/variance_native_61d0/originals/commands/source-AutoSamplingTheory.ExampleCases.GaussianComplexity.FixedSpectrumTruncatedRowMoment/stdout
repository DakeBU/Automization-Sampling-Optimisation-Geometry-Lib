import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.MeasureTheory.SpecificCodomains.Pi
import Mathlib.LinearAlgebra.Matrix.Kronecker

/-!
# The unnormalized truncated second moment of a Gaussian row

Appendix C.2 uses the canonical standard row law and the closed retained ball.
The coefficient is the retained radial moment divided by the dimension.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment

theorem actual_truncated_row_second_moment
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ := (∫ x, Set.indicator {y : E | R y ≤ L} R x ∂μ) / r
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let kept : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    Set.indicator {y : E | R y ≤ L} G
  Integrable kept μ ∧
    (∫ x, kept x ∂μ) = a • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) := by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ := (∫ x, Set.indicator {y : E | R y ≤ L} R x ∂μ) / r
  let G : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let good : Set E := {x | R x ≤ L}
  let kept : E → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ := good.indicator G
  let entry (i j : Fin (q + 1)) (x : E) : ℝ := kept x i j
  have good_measurable : MeasurableSet good := by
    dsimp [good, R]
    exact measurableSet_le (by fun_prop) measurable_const
  have radius_integrable : Integrable R μ :=
    (AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian
      (E := E)).1
  have entry_formula (i j : Fin (q + 1)) :
      entry i j = good.indicator (fun x : E => x i * x j) := by
    funext x
    by_cases hx : x ∈ good <;> simp [entry, kept, G, Matrix.vecMulVec, hx]
  have retained_radius_integrable : Integrable (good.indicator R) μ :=
    radius_integrable.indicator good_measurable
  have entry_integrable (i j : Fin (q + 1)) : Integrable (entry i j) μ := by
    rw [entry_formula]
    have continuous_product : Continuous (fun x : E => x i * x j) :=
      (PiLp.continuous_apply 2 (fun _ : Fin (q + 1) => ℝ) i).mul
        (PiLp.continuous_apply 2 (fun _ : Fin (q + 1) => ℝ) j)
    apply retained_radius_integrable.mono'
      (continuous_product.aestronglyMeasurable.indicator good_measurable)
    filter_upwards with x
    by_cases hx : x ∈ good
    · simp only [Set.indicator_of_mem hx]
      calc
        ‖x i * x j‖ = ‖x i‖ * ‖x j‖ := norm_mul _ _
        _ ≤ ‖x‖ * ‖x‖ :=
          mul_le_mul (PiLp.norm_apply_le x i) (PiLp.norm_apply_le x j)
            (norm_nonneg _) (norm_nonneg _)
        _ = R x := by simp [R, pow_two]
    · simp [Set.indicator_of_notMem hx]
  let rows : E → Fin (q + 1) → Fin (q + 1) → ℝ := fun x i j => entry i j x
  have rows_integrable : Integrable rows μ :=
    Integrable.of_eval (fun i => Integrable.of_eval (fun j => entry_integrable i j))
  let ofRows : (Fin (q + 1) → Fin (q + 1) → ℝ) ≃L[ℝ]
      Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    (Matrix.ofLinearEquiv ℝ).toContinuousLinearEquiv
  have kept_integrable : Integrable kept μ := by
    change Integrable (fun x => ofRows (rows x)) μ
    exact ofRows.toContinuousLinearMap.integrable_comp rows_integrable
  have integral_entry (i j : Fin (q + 1)) :
      (∫ x, kept x ∂μ) i j = ∫ x, entry i j x ∂μ := by
    have transport := ofRows.integral_comp_comm rows (μ := μ)
    change (∫ x, kept x ∂μ) = ofRows (∫ x, rows x ∂μ) at transport
    rw [transport]
    change ((∫ x, rows x ∂μ) i) j = _
    rw [MeasureTheory.eval_integral (fun i => rows_integrable.eval i) i]
    exact MeasureTheory.eval_integral (fun j => entry_integrable i j) j
  have invariant_integral (e : E ≃ₗᵢ[ℝ] E) (i j : Fin (q + 1)) :
      (∫ x, entry i j (e x) ∂μ) = ∫ x, entry i j x ∂μ := by
    have law : Measure.map e μ = μ := stdGaussian_map e
    have hmeas : AEStronglyMeasurable (entry i j) (Measure.map e μ) := by
      rw [law]
      exact (entry_integrable i j).aestronglyMeasurable
    have transport := integral_map e.continuous.measurable.aemeasurable hmeas
    rw [law] at transport
    exact transport.symm

  -- A sign change cancels every off-diagonal entry.
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
      simp only [entry_formula]
      have radius_eq : R (flip x) = R x := congrArg (fun t : ℝ => t ^ 2) (flip.norm_map x)
      by_cases hx : x ∈ good
      · have hfx : flip x ∈ good := by simpa [good, radius_eq] using hx
        simp [Set.indicator_of_mem hx, Set.indicator_of_mem hfx, flip_apply, hij.symm]
      · have hfx : flip x ∉ good := by simpa [good, radius_eq] using hx
        simp [Set.indicator_of_notMem hx, Set.indicator_of_notMem hfx]
    have h := invariant_integral flip i j
    simp_rw [flip_entry] at h
    rw [integral_neg] at h
    linarith

  -- Swapping two coordinates makes all diagonal expectations equal.
  have diagonal_equal (i j : Fin (q + 1)) :
      (∫ x, entry i i x ∂μ) = ∫ x, entry j j x ∂μ := by
    let swap : E ≃ₗᵢ[ℝ] E :=
      LinearIsometryEquiv.piLpCongrLeft 2 ℝ ℝ (Equiv.swap i j)
    have swap_apply (x : E) : swap x i = x j := by
      change x ((Equiv.swap i j).symm i) = x j
      simp
    have swap_entry (x : E) : entry i i (swap x) = entry j j x := by
      simp only [entry_formula]
      have radius_eq : R (swap x) = R x := congrArg (fun t : ℝ => t ^ 2) (swap.norm_map x)
      by_cases hx : x ∈ good
      · have hsx : swap x ∈ good := by simpa [good, radius_eq] using hx
        simp [Set.indicator_of_mem hx, Set.indicator_of_mem hsx, swap_apply]
      · have hsx : swap x ∉ good := by simpa [good, radius_eq] using hx
        simp [Set.indicator_of_notMem hx, Set.indicator_of_notMem hsx]
    have h := invariant_integral swap i i
    simp_rw [swap_entry] at h
    exact h.symm

  -- The trace is the retained squared radius, so its coefficient is a.
  have trace_pointwise (x : E) :
      (∑ i : Fin (q + 1), entry i i x) = good.indicator R x := by
    simp_rw [entry_formula]
    by_cases hx : x ∈ good
    · simp only [Set.indicator_of_mem hx]
      simpa [R, pow_two] using (EuclideanSpace.real_norm_sq_eq x).symm
    · simp [Set.indicator_of_notMem hx]
  have trace_integral :
      (∑ i : Fin (q + 1), ∫ x, entry i i x ∂μ) = ∫ x, good.indicator R x ∂μ := by
    rw [← integral_finsetSum _ (fun i _ => entry_integrable i i)]
    apply integral_congr_ae
    exact Filter.Eventually.of_forall trace_pointwise
  have r_positive : 0 < r := by
    dsimp [r]
    exact_mod_cast Nat.succ_pos q
  have diagonal_value (i : Fin (q + 1)) : (∫ x, entry i i x ∂μ) = a := by
    have trace_eq := trace_integral
    have sum_equal :
        (∑ j : Fin (q + 1), ∫ x, entry j j x ∂μ) = r * (∫ x, entry i i x ∂μ) := by
      simp_rw [diagonal_equal _ i]
      simp [r]
    rw [sum_equal] at trace_eq
    change (∫ x, entry i i x ∂μ) = (∫ x, good.indicator R x ∂μ) / r
    apply (eq_div_iff (ne_of_gt r_positive)).2
    nlinarith [trace_eq]
  refine ⟨kept_integrable, ?_⟩
  change (∫ x, kept x ∂μ) = a • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ)
  ext i j
  rw [integral_entry]
  by_cases hij : i = j
  · subst j
    simpa using diagonal_value i
  · simpa [hij] using off_diagonal i j

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment
