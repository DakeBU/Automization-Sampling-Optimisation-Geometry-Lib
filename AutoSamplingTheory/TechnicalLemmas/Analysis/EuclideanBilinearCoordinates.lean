import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.Basis.Bilinear

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates

open scoped BigOperators

/-- The ordered coordinate expansion of a continuous bilinear form on Euclidean space. -/
theorem euclidean_bilinear_eq_sum_basis
    {I : Type*} [Fintype I] [DecidableEq I]
    (H : EuclideanSpace ℝ I →L[ℝ] EuclideanSpace ℝ I →L[ℝ] ℝ)
    (x y : EuclideanSpace ℝ I) :
    H x y = ∑ i : I, ∑ j : I,
      x i * y j * H (EuclideanSpace.basisFun I ℝ i) (EuclideanSpace.basisFun I ℝ j) := by
  let E := EuclideanSpace ℝ I
  let e := EuclideanSpace.basisFun I ℝ
  let L : E →ₗ[ℝ] E →ₗ[ℝ] ℝ :=
    (ContinuousLinearMap.coeLM ℝ : (E →L[ℝ] ℝ) →ₗ[ℝ] E →ₗ[ℝ] ℝ).comp H.toLinearMap
  have h := LinearMap.sum_repr_mul_repr_mul e.toBasis e.toBasis (B := L) x y
  simpa [Finsupp.sum_fintype, L, e, EuclideanSpace.basisFun_repr, smul_eq_mul, mul_assoc]
    using h.symm

end AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates
