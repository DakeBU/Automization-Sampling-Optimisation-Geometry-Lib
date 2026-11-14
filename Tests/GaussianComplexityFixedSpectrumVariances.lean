import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

/-!
Actual consumer of both quadratic L2 results and both variance<=2M bounds.
This is a private numerical generalization of the variance clause of Ex25:
tau is explicitly assumed to lie in [0,1/2]. It is not a public source Anchor,
a concrete query threshold, an orthogonally rotated law or a sampling lower
bound. No independence between Q and norm squared is asserted or used.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

private theorem actual_gaussian_contrast_variance_le {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) (τ : ℝ) (hτ0 : 0 ≤ τ) (hτ1 : τ ≤ 1 / 2) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let Z : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (-1 : ℝ) ^ n * Q x - 2 * τ * ‖x‖ ^ 2
  MemLp Z 2 μ ∧ Var[Z; μ] ≤ 8 * M := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let N : EuclideanSpace ℝ (Fin d) → ℝ := fun x => ‖x‖ ^ 2
  let X : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (-1 : ℝ) ^ n * Q x
  let Z : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (-1 : ℝ) ^ n * Q x - 2 * τ * ‖x‖ ^ 2
  change MemLp Z 2 μ ∧ Var[Z; μ] ≤ 8 * M
  rcases actual_diagonal_gaussian_quadratic_variances hd hκ n hn hnd with
    ⟨hN, hQ, _, _, hNbound, hQbound, _⟩
  have hX : MemLp X 2 μ := hQ.const_mul _
  have hZ : MemLp Z 2 μ := hX.sub (hN.const_mul (2 * τ))
  have hsign : ((-1 : ℝ) ^ n) ^ 2 = 1 := by
    rw [← pow_mul, Nat.mul_comm, pow_mul]
    norm_num
  have hXvar : Var[X; μ] = Var[Q; μ] := by
    change Var[fun x => (-1 : ℝ) ^ n * Q x; μ] = _
    rw [variance_const_mul, hsign, one_mul]
  have hXbound : Var[X; μ] ≤ 2 * M := by rw [hXvar]; exact hQbound
  have hM : 0 ≤ M := by linarith [variance_nonneg N μ]
  -- Centered L2 estimate: positivity of Var(X+N) bounds the cross term.
  -- Both L2 inputs are needed by variance_fun_add and variance_fun_sub.
  have hcross : -2 * cov[X, N; μ] ≤ 4 * M := by
    have h := variance_nonneg (fun x => X x + N x) μ
    rw [variance_fun_add hX hN] at h
    linarith
  have hZvar : Var[Z; μ] = Var[X; μ] - 4 * τ * cov[X, N; μ] +
      4 * τ ^ 2 * Var[N; μ] := by
    have h := variance_fun_sub hX (hN.const_mul (2 * τ))
    rw [variance_const_mul (2 * τ) N μ,
      covariance_const_mul_right (2 * τ)] at h
    change Var[Z; μ] = _ at h
    rw [h]
    ring
  have htriangle : Var[Z; μ] ≤ 2 * M * (1 + 2 * τ) ^ 2 := by
    calc
      _ = Var[X; μ] + (2 * τ) * (-2 * cov[X, N; μ]) +
          (4 * τ ^ 2) * Var[N; μ] := by rw [hZvar]; ring
      _ ≤ 2 * M + (2 * τ) * (4 * M) + (4 * τ ^ 2) * (2 * M) := by
        exact add_le_add
          (add_le_add hXbound (mul_le_mul_of_nonneg_left hcross (by positivity)))
          (mul_le_mul_of_nonneg_left hNbound (by positivity))
      _ = _ := by ring
  have hτsq : (1 + 2 * τ) ^ 2 ≤ 4 := by nlinarith
  refine ⟨hZ, htriangle.trans ?_⟩
  calc
    2 * M * (1 + 2 * τ) ^ 2 ≤ 2 * M * 4 :=
      mul_le_mul_of_nonneg_left hτsq (by positivity)
    _ = 8 * M := by ring
