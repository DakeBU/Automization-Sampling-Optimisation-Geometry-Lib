import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange

open Matrix
open scoped BigOperators
set_option autoImplicit false

/-! The actual range theorem supplies one common coefficient witness for both
Euclidean quadratic identities. No concentration event or norm bound is a
premise; the later inequalities of Lemma 4.4 remain separate. -/
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumKrylovRange

private theorem actual_krylov_quadratic_coordinates {d q : ℕ} (κ : ℝ) (hκ : 2 ≤ κ) (hq : 2 * q + 1 < d)
    (x : EuclideanSpace ℝ (Fin d × Fin (q + 1))) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let g : Fin (q + 1) → Fin d → ℝ := fun a i => WithLp.ofLp x (i, a)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let B : Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i a =>
    (Real.sqrt (d : ℝ))⁻¹ * g a.1 i * t i a.2
  let K : Submodule ℝ (Fin d → ℝ) :=
    Submodule.span ℝ (Set.range (fun a : Fin (q + 1) × Fin (q + 1) =>
      (Λ ^ a.2.val).mulVec (g a.1)))
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  ∀ v : Fin d → ℝ, v ∈ K →
    ∃ c : Fin (q + 1) × Fin (q + 1) → ℝ,
      B.mulVec c = v ∧
      ‖(WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))‖ ^ 2 =
        (∑ a : Fin (q + 1) × Fin (q + 1), c a * ((B.transpose * B).mulVec c) a) ∧
      (inner ℝ (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))
        (WithLp.toLp 2 (D.mulVec v) : EuclideanSpace ℝ (Fin d))) =
        (∑ a : Fin (q + 1) × Fin (q + 1), c a * ((B.transpose * D * B).mulVec c) a) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let g : Fin (q + 1) → Fin d → ℝ := fun a i => WithLp.ofLp x (i, a)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let B : Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i a =>
    (Real.sqrt (d : ℝ))⁻¹ * g a.1 i * t i a.2
  let K : Submodule ℝ (Fin d → ℝ) :=
    Submodule.span ℝ (Set.range (fun a : Fin (q + 1) × Fin (q + 1) =>
      (Λ ^ a.2.val).mulVec (g a.1)))
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  have hr :=
    AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange.actual_cosine_feature_krylov_range
      κ hκ hq x
  change Set.range (fun c : Fin (q + 1) × Fin (q + 1) → ℝ => B.mulVec c) =
    (K : Set (Fin d → ℝ)) at hr
  change ∀ v : Fin d → ℝ, v ∈ K →
    ∃ c : Fin (q + 1) × Fin (q + 1) → ℝ,
      B.mulVec c = v ∧
      ‖(WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))‖ ^ 2 =
        (∑ a : Fin (q + 1) × Fin (q + 1), c a * ((B.transpose * B).mulVec c) a) ∧
      (inner ℝ (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))
        (WithLp.toLp 2 (D.mulVec v) : EuclideanSpace ℝ (Fin d))) =
        (∑ a : Fin (q + 1) × Fin (q + 1), c a * ((B.transpose * D * B).mulVec c) a)
  intro v hv
  have hvimage : v ∈ Set.range (fun c : Fin (q + 1) × Fin (q + 1) → ℝ => B.mulVec c) := by
    rw [hr]
    exact hv
  obtain ⟨c, hc⟩ := hvimage
  change B.mulVec c = v at hc
  have hcoord (u : Fin d → ℝ) :
      inner ℝ (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))
        (WithLp.toLp 2 u : EuclideanSpace ℝ (Fin d)) =
      c ⬝ᵥ (B.transpose.mulVec u) := by
    rw [EuclideanSpace.inner_toLp_toLp]
    simp only [star_trivial]
    rw [Matrix.dotProduct_transpose_mulVec, hc]
  refine ⟨c, hc, ?_, ?_⟩
  · calc
      ‖(WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))‖ ^ 2 =
          inner ℝ (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))
            (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d)) :=
        (real_inner_self_eq_norm_sq _).symm
      _ = c ⬝ᵥ (B.transpose.mulVec v) := hcoord v
      _ = c ⬝ᵥ ((B.transpose * B).mulVec c) := by
        rw [← hc, Matrix.mulVec_mulVec]
      _ = ∑ a, c a * ((B.transpose * B).mulVec c) a := rfl
  · rw [hcoord]
    change c ⬝ᵥ (B.transpose.mulVec (D.mulVec v)) =
      c ⬝ᵥ ((B.transpose * D * B).mulVec c)
    simp only [← Matrix.mulVec_mulVec, hc]

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumKrylovRange
