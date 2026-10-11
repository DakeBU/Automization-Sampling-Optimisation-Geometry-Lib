import AutoSamplingTheory.TechnicalLemmas.Geometry.AffineGradient

noncomputable section

namespace AutoSamplingTheory.Tests.Shared.AffineGradient

open scoped InnerProductSpace
open TechnicalLemmas.Geometry.AffineGradient

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

-- An actual linear objective, restricted through a translated inclusion.
-- The translation affects the value, while the gradient remains a vector in K.
example (K : Submodule ℝ E) [CompleteSpace K] (a g : E) (u : K) :
    HasGradientAt (fun v : K => inner ℝ g (a + (v : E)))
      (K.orthogonalProjectionOnto g) u := by
  apply hasGradientAt_affine_restriction
  exact hasGradientAt_iff_hasFDerivAt.mpr (InnerProductSpace.toDual ℝ E g).hasFDerivAt

-- A nonzero ambient normal gradient becomes zero after restriction.
-- This would fail for an adapter that returned the ambient gradient unchanged.
example (K : Submodule ℝ E) [CompleteSpace K] (a n : E) (u : K)
    (hn : n ∈ Kᗮ) :
    HasGradientAt (fun v : K => inner ℝ n (a + (v : E))) 0 u := by
  have h : HasGradientAt (fun v : K => inner ℝ n (a + (v : E)))
      (K.orthogonalProjectionOnto n) u := by
    apply hasGradientAt_affine_restriction
    exact hasGradientAt_iff_hasFDerivAt.mpr (InnerProductSpace.toDual ℝ E n).hasFDerivAt
  simpa only [K.orthogonalProjectionOnto_eq_zero_iff.mpr hn] using h

#print axioms TechnicalLemmas.Geometry.AffineGradient.hasGradientAt_affine_restriction

end AutoSamplingTheory.Tests.Shared.AffineGradient
