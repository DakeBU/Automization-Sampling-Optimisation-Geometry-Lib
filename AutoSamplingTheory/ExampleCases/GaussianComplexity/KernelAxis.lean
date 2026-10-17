import AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelRotation
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Tactic.Ring

/-!
# Norm-axis reduction of the literal signed Gaussian kernel average

Zhou--Suzuki arXiv:2610.20492v1, Appendix B.2.2 Ex58 and the following
O11 quadratic-form evaluation. Actual Gaussian-law/density identification,
spatial domination/Fubini and the original H(lambda) remain separate.
-/

open Matrix MeasureTheory Set TopologicalSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelRotation

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelAxis

private lemma exists_orthogonal_map {n : ℕ} (x y : EuclideanSpace ℝ (Fin n))
    (h : ‖x‖ = ‖y‖) :
    ∃ Q : Matrix.orthogonalGroup (Fin n) ℝ,
      (Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp x = WithLp.ofLp y := by
  let f : EuclideanSpace ℝ (Fin n) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin n) :=
    (ℝ ∙ (x - y))ᗮ.reflection
  let b := EuclideanSpace.basisFun (Fin n) ℝ
  let Q : Matrix.orthogonalGroup (Fin n) ℝ :=
    ⟨f.toMatrix b.toBasis b.toBasis, f.toMatrix_mem_unitaryGroup b b⟩
  have hm := LinearMap.toMatrix_mulVec_repr b.toBasis b.toBasis f.toLinearEquiv.toLinearMap x
  have hfx : f x = y := Submodule.reflection_sub h
  refine ⟨Q, ?_⟩
  change (Q : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp x = WithLp.ofLp (f x) at hm
  exact hm.trans (congrArg WithLp.ofLp hfx)

private lemma axis_quadratic {n : ℕ} (κ t : ℝ)
    (O : Matrix.orthogonalGroup (Fin n) ℝ) (j : Fin n) :
    (Pi.single j t) ⬝ᵥ (singleBlockPrecision κ O *ᵥ Pi.single j t) =
      (κ + 1 - (κ - 1) * (O : Matrix (Fin n) (Fin n) ℝ) j j) * t ^ 2 / 2 := by
  rw [single_dotProduct]
  change t * ((singleBlockPrecision κ O) j ⬝ᵥ Pi.single j t) = _
  rw [dotProduct_single]
  simp only [singleBlockPrecision, Matrix.sub_apply, Matrix.smul_apply, Matrix.add_apply,
    Matrix.transpose_apply, Matrix.one_apply, ite_true, smul_eq_mul]
  ring

theorem signed_kernel_radial {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) :
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let p : Matrix.orthogonalGroup (Fin n) ℝ → (Fin n → ℝ) → ℝ :=
      fun O v => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
          Real.exp (-(v ⬝ᵥ (singleBlockPrecision κ O *ᵥ v)) / 2)
    let r : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
          Real.exp (-(κ + 1 - (κ - 1) * (O : Matrix (Fin n) (Fin n) ℝ) j0 j0) *
            ‖x‖ ^ 2 / 4)
    ∀ x : EuclideanSpace ℝ (Fin n),
      Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
        (O : Matrix (Fin n) (Fin n) ℝ).det * p O (WithLp.ofLp x)) (orthogonalHaar n) ∧
      Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
        (O : Matrix (Fin n) (Fin n) ℝ).det * r O x) (orthogonalHaar n) ∧
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * p O (WithLp.ofLp x) ∂orthogonalHaar n) =
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * r O x ∂orthogonalHaar n) := by
  classical
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let p : Matrix.orthogonalGroup (Fin n) ℝ → (Fin n → ℝ) → ℝ :=
    fun O v => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-(v ⬝ᵥ (singleBlockPrecision κ O *ᵥ v)) / 2)
  let r : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-(κ + 1 - (κ - 1) * (O : Matrix (Fin n) (Fin n) ℝ) j0 j0) *
          ‖x‖ ^ 2 / 4)
  change ∀ x : EuclideanSpace ℝ (Fin n),
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * p O (WithLp.ofLp x)) (orthogonalHaar n) ∧
    Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * r O x) (orthogonalHaar n) ∧ _
  intro x
  let y : EuclideanSpace ℝ (Fin n) := PiLp.single 2 j0 ‖x‖
  have hnorm : ‖x‖ = ‖y‖ := by simp [y, PiLp.norm_single]
  obtain ⟨Q, hQ⟩ := exists_orthogonal_map x y hnorm
  have hy : WithLp.ofLp y = Pi.single j0 ‖x‖ := rfl
  have hr (O : Matrix.orthogonalGroup (Fin n) ℝ) : p O (WithLp.ofLp y) = r O x := by
    dsimp only [p, r]
    rw [hy, axis_quadratic]
    congr 2
    ring
  have h := signed_kernel_rotation_invariant hn hκ
  change (∀ v : Fin n → ℝ, Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * p O v) (orthogonalHaar n)) ∧ _ at h
  have hrad : Integrable (fun O : Matrix.orthogonalGroup (Fin n) ℝ =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * r O x) (orthogonalHaar n) :=
    (h.1 (WithLp.ofLp y)).congr (Filter.Eventually.of_forall fun O =>
      congrArg (fun z : ℝ => (O : Matrix (Fin n) (Fin n) ℝ).det * z) (hr O))
  refine ⟨h.1 (WithLp.ofLp x), hrad, ?_⟩
  have he := h.2 Q (WithLp.ofLp x)
  rw [hQ] at he
  calc
    _ = ∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det * p O (WithLp.ofLp y) ∂orthogonalHaar n := he.symm
    _ = _ := by
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun O =>
        congrArg (fun z : ℝ => (O : Matrix (Fin n) (Fin n) ℝ).det * z) (hr O)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelAxis
