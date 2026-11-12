import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian

noncomputable section

namespace AutoSamplingTheory.Tests.Shared.SphereRayleighHessian

open Metric InnerProductSpace
open scoped InnerProductSpace
open TechnicalLemmas.Geometry.SphereRayleighHessian

-- Repeated eigenvalues require no nondegeneracy: the identity's Hessian
-- vanishes even at points with nonzero tangent directions.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (x : sphere (0 : E) 1) (u : (ℝ ∙ (x : E))ᗮ) :
    halfRayleighTangentHessian (ContinuousLinearMap.id ℝ E) x u = 0 := by
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  rw [(sphere_half_rayleigh_tangent_hessian_apply (ContinuousLinearMap.id ℝ E) x u).1]
  simp [hx]

-- The top eigenvector of a rank-one orthogonal projector is stationary,
-- but a nonzero orthogonal direction detects strictly negative curvature.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (x : sphere (0 : E) 1) (u : (ℝ ∙ (x : E))ᗮ) (hu : (u : E) ≠ 0) :
    let A := (innerSL ℝ (x : E)).smulRight (x : E)
    halfRayleighGradientExtension A (x : E) = 0 ∧
      ⟪(u : E), (halfRayleighTangentHessian A x u : E)⟫_ℝ < 0 := by
  intro A
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  have hxu := Submodule.mem_orthogonal_singleton_iff_inner_right.mp u.property
  have hAx : A (x : E) = (x : E) := by simp [A, hx]
  have hAu : A (u : E) = 0 := by simp [A, hxu]
  constructor
  · simp [halfRayleighGradientExtension, hAx, hx]
  · rw [(sphere_half_rayleigh_tangent_hessian_apply A x u).2, hAu, hAx]
    simpa [hx] using sq_pos_of_pos (norm_pos_iff.mpr hu)

-- The source includes ambient dimension one, with zero tangent space.
example : Module.End.HasEigenvector (ContinuousLinearMap.id ℝ ℝ).toLinearMap 1 1 ∧
    ∀ μ : ℝ, Module.End.HasEigenvalue (ContinuousLinearMap.id ℝ ℝ).toLinearMap μ → 1 ≤ μ := by
  let x : sphere (0 : ℝ) 1 := ⟨1, mem_sphere_zero_iff_norm.mpr norm_one⟩
  let A := ContinuousLinearMap.id ℝ ℝ
  have hsym : A.IsSymmetric := by
    intro y z
    rfl
  have hgrad : halfRayleighGradientExtension A (x : ℝ) = 0 := by
    simp [halfRayleighGradientExtension, A, x]
  have hpsd (u : (ℝ ∙ (x : ℝ))ᗮ) :
      0 ≤ ⟪(u : ℝ), (halfRayleighTangentHessian A x u : ℝ)⟫_ℝ := by
    rw [(sphere_half_rayleigh_tangent_hessian_apply A x u).2]
    simp [A, x]
  simpa [A, x] using (sphere_half_rayleigh_second_order_stationary_min A hsym x hgrad hpsd).2

#print axioms sphere_half_rayleigh_gradient_pairing
#print axioms sphere_half_rayleigh_tangent_hessian_apply
#print axioms sphere_half_rayleigh_second_order_stationary_min

end AutoSamplingTheory.Tests.Shared.SphereRayleighHessian
