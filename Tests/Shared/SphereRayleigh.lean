import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleigh

noncomputable section

namespace AutoSamplingTheory.Tests.Shared.SphereRayleigh

open Metric InnerProductSpace
open scoped Manifold InnerProductSpace
open TechnicalLemmas.Geometry.SphereRayleigh

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]

-- Identity has a nonzero ambient gradient 2x and zero constrained differential.
-- The test constructs both facts, including actual eigenvectorhood.
example (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (x : sphere (0 : E) 1) :
    mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 =>
      ⟪(y : E), ContinuousLinearMap.id ℝ E (y : E)⟫_ℝ) x = 0 ∧
      Module.End.HasEigenvector (ContinuousLinearMap.id ℝ E).toLinearMap 1 (x : E) ∧
        (2 : ℝ) • (x : E) ≠ 0 := by
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  have hxne : (x : E) ≠ 0 := by
    intro hz
    simp [hz] at hx
  have hA : (ContinuousLinearMap.id ℝ E).IsSymmetric := LinearMap.IsSymmetric.id
  refine ⟨(sphere_rayleigh_stationary_iff n _ hA x).1.mpr ?_, ?_, ?_⟩
  · simp [hx]
  · exact ⟨Module.End.mem_eigenspace_iff.mpr (by simp), hxne⟩
  · simp [hxne]

-- A genuine symmetric rank-two operator exchanges orthogonal unit directions.
-- At x the constrained gradient is 2u, and x is not stationary. This checks
-- the coefficient, tangent candidate, and both positive/negative semantics.
example (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (x : sphere (0 : E) 1) (u : E) (hu : ‖u‖ = 1) (hxu : ⟪(x : E), u⟫_ℝ = 0) :
    let A := (innerSL ℝ (x : E)).smulRight u + (innerSL ℝ u).smulRight (x : E)
    (∀ w : TangentSpace (𝓡 n) x,
      mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x w =
        ⟪mvfderiv (𝓡 n) ((↑) : sphere (0 : E) 1 → E) x w, (2 : ℝ) • u⟫_ℝ) ∧
      mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x ≠ 0 := by
  intro A
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  have hux : ⟪u, (x : E)⟫_ℝ = 0 := by rw [real_inner_comm, hxu]
  have hA : A.IsSymmetric := by
    intro v w
    change ⟪⟪(x : E), v⟫_ℝ • u + ⟪u, v⟫_ℝ • (x : E), w⟫_ℝ =
      ⟪v, ⟪(x : E), w⟫_ℝ • u + ⟪u, w⟫_ℝ • (x : E)⟫_ℝ
    simp only [inner_add_left, inner_add_right, inner_smul_left, inner_smul_right,
      starRingEnd_apply, star_trivial]
    rw [real_inner_comm v u, real_inner_comm v (x : E)]
    ring
  have hAx : A (x : E) = u := by simp [A, hx, hux]
  have hz : (2 : ℝ) • u ∈ (ℝ ∙ (x : E))ᗮ := by
    rw [Submodule.mem_orthogonal_singleton_iff_inner_right]
    simp [inner_smul_right, hxu]
  refine ⟨(sphere_rayleigh_characterization n A hA x ⟨(2 : ℝ) • u, hz⟩).mpr ?_, ?_⟩
  · simp [hAx, hxu]
  · intro hd
    have he := (sphere_rayleigh_stationary_iff n A hA x).1.mp hd
    have hu0 : u = 0 := by simpa [hAx, hxu] using he
    simp [hu0] at hu

#print axioms TechnicalLemmas.Geometry.SphereRayleigh.sphere_rayleigh_characterization
#print axioms TechnicalLemmas.Geometry.SphereRayleigh.sphere_rayleigh_stationary_iff

end AutoSamplingTheory.Tests.Shared.SphereRayleigh
