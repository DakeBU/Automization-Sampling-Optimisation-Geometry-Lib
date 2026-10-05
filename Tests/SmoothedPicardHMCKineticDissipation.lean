import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.KineticDissipation

open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.KineticDissipation

-- A genuine two-dimensional input with kappa2 and explicit H=(1/2)I.
-- No eigenbasis, dissipation or exact-kernel contract is assumed by the test.
example (x p : EuclideanSpace ℝ (Fin 2)) :
    (1/16 : ℝ) * ((3/4 : ℝ)*‖x‖^2 + inner ℝ x p + ‖p‖^2) ≤
      (1/2 : ℝ)*‖x‖^2 + (1/2 : ℝ)*inner ℝ x p + ‖p‖^2 := by
  let H : EuclideanSpace ℝ (Fin 2) →ₗ[ℝ] EuclideanSpace ℝ (Fin 2) :=
    (1/2 : ℝ) • LinearMap.id
  have hH : H.IsSymmetric := by
    intro u v
    simp [H, real_inner_smul_left, real_inner_smul_right]
  have hlo (v : EuclideanSpace ℝ (Fin 2)) :
      1/(2*(2:ℝ))*‖v‖^2 ≤ inner ℝ v (H v) := by
    simp only [H, LinearMap.smul_apply, LinearMap.id_apply, real_inner_smul_right,
      real_inner_self_eq_norm_sq]
    nlinarith [sq_nonneg ‖v‖]
  have hup (v : EuclideanSpace ℝ (Fin 2)) : inner ℝ v (H v) ≤ ‖v‖^2 := by
    simp only [H, LinearMap.smul_apply, LinearMap.id_apply, real_inner_smul_right,
      real_inner_self_eq_norm_sq]
    nlinarith [sq_nonneg ‖v‖]
  have t := source_kinetic_dissipation (by norm_num : (1:ℝ) ≤ 2) H hH hlo hup x p
  simp only [H, LinearMap.smul_apply, LinearMap.id_apply, real_inner_smul_right,
    real_inner_self_eq_norm_sq, real_inner_comm p x] at t
  norm_num at t
  nlinarith only [t, real_inner_comm x p]

-- The full theorem also retains the empty-dimensional boundary.
example (x p : EuclideanSpace ℝ (Fin 0)) :
    1/(8*(1:ℝ)) * ((1/(2*(1:ℝ))+1/2)*‖x‖^2 + inner ℝ x p + ‖p‖^2) ≤
      inner ℝ x x + 2*inner ℝ p x - 1/(1:ℝ)*inner ℝ x p + ‖p‖^2 := by
  apply source_kinetic_dissipation (by norm_num : (1:ℝ) ≤ 1) LinearMap.id
  · intro u v; rfl
  · intro v; simp only [LinearMap.id_apply, real_inner_self_eq_norm_sq]
    nlinarith [sq_nonneg ‖v‖]
  · intro v; simp

#print axioms AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.KineticDissipation.source_kinetic_dissipation
