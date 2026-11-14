import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic.Ring

open Matrix InnerProductSpace
set_option autoImplicit false

/-!
# Actual fixed-spectrum first-order replies

Zhou--Suzuki arXiv:2610.20492v1, Section2 Equation1, Section4.1
Equation11 and the ordinary quadratic-calculus meaning in AppendixC.4.
For the literal cosine-grid precision and every full real orthogonal O,
the exact precision-matvec reply is the genuine Euclidean gradient.
Derivative existence is produced before identifying the total gradient.
The actual centered potential value is recovered from that same reply.

The focused Test combines this result with the identical canonical same-O
affine precision provider. No operational query count, adaptive transcript,
Gaussian target/TV, finite-precision or expected-cost transport is asserted.
The remaining C4 regularity/minimizer and both main bounds are separate.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder

theorem actual_first_order_query {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
    let query : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
    ∀ x : EuclideanSpace ℝ (Fin d),
      HasGradientAt f (query x) x ∧
      (f x, gradient f x) = (inner ℝ x (query x) / 2, query x) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let query : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
  let E := EuclideanSpace ℝ (Fin d)
  let H : E →L[ℝ] E := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A
  -- The actual family's existing canonical producer supplies symmetry.
  have hA : A.IsHermitian :=
    (FixedSpectrumAdmissibility.actual_precision_admissible hd hκ O).1.1
  have hself : IsSelfAdjoint A := hA
  have hH : H.IsSymmetric :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp
      (hself.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)))
  have hquery (x : E) : query x = H x := rfl
  have hf : f = fun y : E => (1 / 2 : ℝ) * inner ℝ y (H y) := by
    funext y
    dsimp only [f]
    rw [show inner ℝ y (H y) = (WithLp.ofLp y) ⬝ᵥ (A *ᵥ WithLp.ofLp y) from
      Matrix.inner_toEuclideanCLM A y y]
    ring
  -- Differentiate the actual function and identify its Riesz functional.
  have hgrad (y : E) : HasGradientAt f (H y) y := by
    have hraw := ((hasFDerivAt_id y).inner ℝ H.hasFDerivAt).const_mul (1 / 2 : ℝ)
    have hlin : (1 / 2 : ℝ) •
        ((fderivInnerCLM ℝ (y, H y)).comp ((ContinuousLinearMap.id ℝ E).prod H)) =
        toDual ℝ E (H y) := by
      ext v
      change (1 / 2 : ℝ) * (inner ℝ y (H v) + inner ℝ v (H y)) = inner ℝ (H y) v
      rw [← hH.apply_clm y v, (real_inner_comm v (H y)).symm]
      ring
    apply hasGradientAt_iff_hasFDerivAt.mpr
    rw [hf, ← hlin]
    exact hraw
  intro x
  have hg : HasGradientAt f (query x) x := (hquery x).symm ▸ hgrad x
  refine ⟨hg, Prod.ext ?_ hg.gradient⟩
  change f x = inner ℝ x (query x) / 2
  rw [hquery]
  exact congrArg (fun t : ℝ => t / 2) (Matrix.inner_toEuclideanCLM A x x).symm

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder
