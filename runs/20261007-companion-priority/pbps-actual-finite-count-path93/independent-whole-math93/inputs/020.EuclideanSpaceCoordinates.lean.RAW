import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Tactic.Ring

/-!
# Euclidean-space coordinate bridges

Small reusable coordinate identities for finite-dimensional Euclidean spaces.
These leaves are purely linear-algebraic notation bridges; they do not define
gradients, divergence, Hessians, Laplacians, or analytic regularity.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Geometry
namespace EuclideanSpaceCoordinates

open scoped BigOperators RealInnerProductSpace

/-- Inner product of two real coordinate functions after the `EuclideanSpace`
`WithLp.toLp 2` embedding. -/
theorem euclideanSpace_inner_toLp_toLp_eq_sum_mul
    {ι : Type*} [Fintype ι] (u v : ι → ℝ) :
    inner ℝ (WithLp.toLp 2 u : EuclideanSpace ℝ ι)
        (WithLp.toLp 2 v : EuclideanSpace ℝ ι) =
      ∑ i, u i * v i := by
  rw [PiLp.inner_apply]
  refine Finset.sum_congr rfl ?_
  intro i _
  change v i * u i = u i * v i
  ring

/-- Inner product of two real `EuclideanSpace` vectors in coordinates. -/
theorem euclideanSpace_inner_eq_sum_mul
    {ι : Type*} [Fintype ι] (u v : EuclideanSpace ℝ ι) :
    inner ℝ u v = ∑ i, u i * v i := by
  rw [PiLp.inner_apply]
  refine Finset.sum_congr rfl ?_
  intro i _
  change v i * u i = u i * v i
  ring

end EuclideanSpaceCoordinates
end Geometry
end TechnicalLemmas
end AutoSamplingTheory
