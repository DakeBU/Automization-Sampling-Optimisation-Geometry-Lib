import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleigh

/-!
# The half-Rayleigh objective: sphere Hessian and global optimality

Boumal, §5.5, Corollary 5.16, Example 5.17 and Exercise 5.18 (printed p. 96
of the pre-publication PDF). The induced Hessian here is the tangent
projection of the genuine derivative of the actual sphere gradient extension.
The final comparison is specific to the half-normalized symmetric quadratic;
it is not a second-order sufficiency theorem for arbitrary sphere objectives.
-/

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian

open Metric InnerProductSpace
open scoped Manifold InnerProductSpace ContDiff
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleigh

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Ambient extension of the half-Rayleigh gradient on the unit sphere. -/
def halfRayleighGradientExtension (A : E →L[ℝ] E) (y : E) : E :=
  A y - ⟪y, A y⟫_ℝ • y

/-- The polynomial extension is smooth and its derivative is genuine at every point. -/
private theorem half_rayleigh_gradient_extension_derivative (A : E →L[ℝ] E) :
    ContDiff ℝ ∞ (halfRayleighGradientExtension A) ∧
    ∀ x : E, HasFDerivAt (halfRayleighGradientExtension A)
      (A - (⟪x, A x⟫_ℝ • ContinuousLinearMap.id ℝ E +
        (innerSL ℝ (A x) + (innerSL ℝ x).comp A).smulRight x)) x := by
  refine ⟨?_, fun x => ?_⟩
  · change ContDiff ℝ ∞ (fun y : E => A y - ⟪y, A y⟫_ℝ • y)
    exact A.contDiff.sub ((contDiff_id.inner ℝ A.contDiff).smul contDiff_id)
  · have hq : HasFDerivAt (fun y : E => ⟪y, A y⟫_ℝ)
        (innerSL ℝ (A x) + (innerSL ℝ x).comp A) x := by
      have hlin : (fderivInnerCLM ℝ (x, A x)).comp ((ContinuousLinearMap.id ℝ E).prod A) =
          innerSL ℝ (A x) + (innerSL ℝ x).comp A := by
        apply ContinuousLinearMap.ext
        intro u
        simp [real_inner_comm, add_comm]
      rw [← hlin]
      exact (hasFDerivAt_id x).inner ℝ A.hasFDerivAt
    exact A.hasFDerivAt.fun_sub (hq.fun_smul (hasFDerivAt_id x))

/-- Source-specific projected derivative, restricted and corestricted to the actual
orthogonal tangent plane. This is not a general manifold connection. -/
def halfRayleighTangentHessian (A : E →L[ℝ] E) (x : sphere (0 : E) 1) :
    (ℝ ∙ (x : E))ᗮ →L[ℝ] (ℝ ∙ (x : E))ᗮ :=
  let K := (ℝ ∙ (x : E))ᗮ
  K.orthogonalProjectionOnto.comp
    ((fderiv ℝ (halfRayleighGradientExtension A) (x : E)).comp K.subtypeL)

/-- On the sphere the extension is the induced gradient of the literal half quadratic.
The manifold differentiability witness is supplied alongside the pairing. -/
theorem sphere_half_rayleigh_gradient_pairing
    [FiniteDimensional ℝ E] (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (A : E →L[ℝ] E) (hA : A.IsSymmetric) (x : sphere (0 : E) 1) :
    MDifferentiableAt (𝓡 n) 𝓘(ℝ, ℝ)
      (fun y : sphere (0 : E) 1 => (1 / 2 : ℝ) * ⟪(y : E), A (y : E)⟫_ℝ) x ∧
    halfRayleighGradientExtension A (x : E) ∈ (ℝ ∙ (x : E))ᗮ ∧
    ∀ w : TangentSpace (𝓡 n) x,
      mvfderiv (𝓡 n)
        (fun y : sphere (0 : E) 1 => (1 / 2 : ℝ) * ⟪(y : E), A (y : E)⟫_ℝ) x w =
        ⟪mvfderiv (𝓡 n) ((↑) : sphere (0 : E) 1 → E) x w,
          halfRayleighGradientExtension A (x : E)⟫_ℝ := by
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  have hco := (contMDiff_coe_sphere (n := n) (m := 1) x).mdifferentiableAt one_ne_zero
  have hamb : DifferentiableAt ℝ (fun y : E => (1 / 2 : ℝ) * ⟪y, A y⟫_ℝ) (x : E) :=
    ((hasFDerivAt_id (x : E)).inner ℝ A.hasFDerivAt).differentiableAt.const_mul _
  have ht : halfRayleighGradientExtension A (x : E) ∈ (ℝ ∙ (x : E))ᗮ := by
    rw [Submodule.mem_orthogonal_singleton_iff_inner_right]
    simp [halfRayleighGradientExtension, inner_sub_right, real_inner_smul_right, hx]
  refine ⟨hamb.comp_mdifferentiableAt hco, ht, ?_⟩
  let B : E →L[ℝ] E := (1 / 2 : ℝ) • A
  have hB : B.IsSymmetric := by
    intro y z
    change ⟪(1 / 2 : ℝ) • A y, z⟫_ℝ = ⟪y, (1 / 2 : ℝ) • A z⟫_ℝ
    rw [real_inner_smul_left, real_inner_smul_right]
    exact congrArg ((1 / 2 : ℝ) * ·) (hA y z)
  have hF :
      (fun y : sphere (0 : E) 1 => ⟪(y : E), B (y : E)⟫_ℝ) =
        (fun y : sphere (0 : E) 1 => (1 / 2 : ℝ) * ⟪(y : E), A (y : E)⟫_ℝ) := by
    funext y
    simp [B, real_inner_smul_right]
  let z : (ℝ ∙ (x : E))ᗮ := ⟨_, ht⟩
  have hscale : (z : E) =
      (2 : ℝ) • (B (x : E) - ⟪(x : E), B (x : E)⟫_ℝ • (x : E)) := by
    change halfRayleighGradientExtension A (x : E) = _
    norm_num [halfRayleighGradientExtension, B, real_inner_smul_right, smul_sub,
      smul_smul, ← mul_assoc]
  rw [← hF]
  exact (sphere_rayleigh_characterization n B hB x z).mpr hscale

/-- Projecting kills the normal part of the genuine derivative; the remaining
tangent operator and its quadratic form are the two displayed formulas. -/
theorem sphere_half_rayleigh_tangent_hessian_apply
    (A : E →L[ℝ] E) (x : sphere (0 : E) 1) (u : (ℝ ∙ (x : E))ᗮ) :
    halfRayleighTangentHessian A x u =
      (ℝ ∙ (x : E))ᗮ.orthogonalProjectionOnto (A (u : E)) -
        ⟪(x : E), A (x : E)⟫_ℝ • u ∧
    ⟪(u : E), (halfRayleighTangentHessian A x u : E)⟫_ℝ =
      ⟪(u : E), A (u : E)⟫_ℝ - ⟪(x : E), A (x : E)⟫_ℝ * ‖(u : E)‖ ^ 2 := by
  let K := (ℝ ∙ (x : E))ᗮ
  have hvalue : halfRayleighTangentHessian A x u =
      K.orthogonalProjectionOnto (A (u : E)) - ⟪(x : E), A (x : E)⟫_ℝ • u := by
    change K.orthogonalProjectionOnto
      (fderiv ℝ (halfRayleighGradientExtension A) (x : E) (u : E)) = _
    rw [((half_rayleigh_gradient_extension_derivative A).2 (x : E)).fderiv]
    simp [K, Submodule.orthogonalProjectionOnto_orthogonalComplement_singleton_eq_zero]
  refine ⟨hvalue, ?_⟩
  rw [hvalue]
  change ⟪u, K.orthogonalProjectionOnto (A (u : E)) - ⟪(x : E), A (x : E)⟫_ℝ • u⟫_ℝ = _
  rw [inner_sub_right, K.inner_orthogonalProjectionOnto_eq_of_mem_left, real_inner_smul_right]
  change _ - _ * ⟪(u : E), (u : E)⟫_ℝ = _
  rw [real_inner_self_eq_norm_sq]

/-- At a second-order stationary point of the half-Rayleigh objective, the
actual tangent Hessian controls all differences in objective value. -/
theorem sphere_half_rayleigh_second_order_stationary_min
    [FiniteDimensional ℝ E]
    (A : E →L[ℝ] E) (hA : A.IsSymmetric) (x : sphere (0 : E) 1)
    (hgrad : halfRayleighGradientExtension A (x : E) = 0)
    (hpsd : ∀ u : (ℝ ∙ (x : E))ᗮ, 0 ≤
      ⟪(u : E), (halfRayleighTangentHessian A x u : E)⟫_ℝ) :
    let lam := ⟪(x : E), A (x : E)⟫_ℝ
    IsMinOn (fun y : E => (1 / 2 : ℝ) * ⟪y, A y⟫_ℝ) (sphere (0 : E) 1) (x : E) ∧
      Module.End.HasEigenvector A.toLinearMap lam (x : E) ∧
      ∀ μ : ℝ, Module.End.HasEigenvalue A.toLinearMap μ → lam ≤ μ := by
  let lam := ⟪(x : E), A (x : E)⟫_ℝ
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  have hxne : (x : E) ≠ 0 := by
    intro hz
    simp [hz] at hx
  have hAx : A (x : E) = lam • (x : E) := sub_eq_zero.mp hgrad
  have hmin : IsMinOn (fun y : E => (1 / 2 : ℝ) * ⟪y, A y⟫_ℝ)
      (sphere (0 : E) 1) (x : E) := by
    intro y hy
    change (1 / 2 : ℝ) * lam ≤ (1 / 2 : ℝ) * ⟪y, A y⟫_ℝ
    let a := ⟪(x : E), y⟫_ℝ
    let v := y - a • (x : E)
    have hdecomp : y = a • (x : E) + v := by
      dsimp only [v]
      abel
    have horth : ⟪(x : E), v⟫_ℝ = 0 := by
      simp [v, inner_sub_right, real_inner_smul_right, hx, a]
    let u : (ℝ ∙ (x : E))ᗮ :=
      ⟨v, Submodule.mem_orthogonal_singleton_iff_inner_right.mpr horth⟩
    have hvpos := hpsd u
    rw [(sphere_half_rayleigh_tangent_hessian_apply A x u).2] at hvpos
    change 0 ≤ ⟪v, A v⟫_ℝ - lam * ‖v‖ ^ 2 at hvpos
    have hnorm : a ^ 2 + ‖v‖ ^ 2 = 1 := calc
      _ = ‖a • (x : E) + v‖ ^ 2 := by
        rw [norm_add_sq_real, norm_smul, Real.norm_eq_abs,
          real_inner_smul_left, hx, horth, mul_one, sq_abs]
        ring
      _ = 1 := by rw [← hdecomp, mem_sphere_zero_iff_norm.mp hy, one_pow]
    have hcross : ⟪(x : E), A v⟫_ℝ = 0 := calc
      _ = ⟪A (x : E), v⟫_ℝ := (hA (x : E) v).symm
      _ = 0 := by rw [hAx, real_inner_smul_left, horth, mul_zero]
    have hcross' : ⟪v, A (x : E)⟫_ℝ = 0 := by
      rw [real_inner_comm, hAx, real_inner_smul_left, horth, mul_zero]
    have henergy : ⟪y, A y⟫_ℝ = a ^ 2 * lam + ⟪v, A v⟫_ℝ := calc
      _ = ⟪a • (x : E) + v, A (a • (x : E) + v)⟫_ℝ :=
        congrArg (fun z => ⟪z, A z⟫_ℝ) hdecomp
      _ = _ := by
        simp [map_add, map_smul, inner_add_left, inner_add_right,
          real_inner_smul_left, real_inner_smul_right, hcross, hcross', lam]
        ring
    have hscale : lam * (a ^ 2 + ‖v‖ ^ 2) = lam := by rw [hnorm, mul_one]
    nlinarith only [henergy, hscale, hvpos]
  refine ⟨hmin, ⟨Module.End.mem_eigenspace_iff.mpr hAx, hxne⟩, ?_⟩
  intro μ hμ
  obtain ⟨v, hv⟩ := hμ.exists_hasEigenvector
  have hvnorm : 0 < ‖v‖ := norm_pos_iff.mpr hv.2
  let z := ‖v‖⁻¹ • v
  have hznorm : ‖z‖ = 1 := by
    dsimp only [z]
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hvnorm),
      inv_mul_cancel₀ hvnorm.ne']
  have hAv : A v = μ • v := hv.apply_eq_smul
  have hAz : A z = μ • z := by
    dsimp only [z]
    rw [map_smul, hAv, smul_smul, smul_smul, mul_comm]
  have hzval : ⟪z, A z⟫_ℝ = μ := by
    rw [hAz, real_inner_smul_right, real_inner_self_eq_norm_sq, hznorm, one_pow, mul_one]
  have hc := hmin (mem_sphere_zero_iff_norm.mpr hznorm)
  change (1 / 2 : ℝ) * lam ≤ (1 / 2 : ℝ) * ⟪z, A z⟫_ℝ at hc
  rw [hzval] at hc
  linarith only [hc]

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian
