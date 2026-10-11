import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.FDeriv.Add
import Mathlib.Analysis.Calculus.FDeriv.Comp
import Mathlib.Analysis.InnerProductSpace.Projection.Basic

/-!
# Gradients under affine subspace restriction

The inherited inner product identifies the derivative of `v ↦ f (a + v)`
with the orthogonal projection of the ambient gradient. This is a canonical
Hilbert-space prerequisite for Boumal §3.8's projection argument, not a
formalization of the nonlinear embedded-manifold differential adapter.
-/

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.AffineGradient

open scoped InnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Restricting an ambient differentiable objective to an affine subspace
projects its genuine gradient into the direction subspace, with its inherited
metric. Completeness is explicit; no restriction derivative is assumed. -/
theorem hasGradientAt_affine_restriction
    (K : Submodule ℝ E) [CompleteSpace K]
    {f : E → ℝ} {a g : E} {u : K}
    (hf : HasGradientAt f g (a + (u : E))) :
    HasGradientAt (fun v : K => f (a + (v : E)))
      (K.orthogonalProjectionOnto g) u := by
  have hchart : HasFDerivAt (fun v : K => a + (v : E)) K.subtypeL u := by
    convert (hasFDerivAt_const a u).add K.subtypeL.hasFDerivAt using 1 <;>
      first | rfl | simp only [zero_add]
  have hcomp := hf.hasFDerivAt.comp u hchart
  have hdual : (InnerProductSpace.toDual ℝ E g).comp K.subtypeL =
      InnerProductSpace.toDual ℝ K (K.orthogonalProjectionOnto g) := by
    ext v
    simp
  rw [hdual] at hcomp
  exact hasGradientAt_iff_hasFDerivAt.mpr hcomp

end AutoSamplingTheory.TechnicalLemmas.Geometry.AffineGradient
