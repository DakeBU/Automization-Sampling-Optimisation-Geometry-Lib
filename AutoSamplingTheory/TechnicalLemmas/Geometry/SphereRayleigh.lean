import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereGradient
import Mathlib.Analysis.InnerProductSpace.Rayleigh

/-!
# Rayleigh objectives on the unit sphere

Boumal Example 3.62: the induced gradient of the literal sphere restriction
of a symmetric quadratic is its projected ambient gradient. Critical points
are exactly unit eigenvectors. The pairing uses the actual sphere inclusion
differential; it does not replace the induced metric by a chart metric.
-/

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleigh

open Metric InnerProductSpace
open scoped Manifold InnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]

/-- The concrete Rayleigh vector is the unique ambient tangent representative
of the genuine sphere differential with the inclusion-induced pairing. -/
theorem sphere_rayleigh_characterization
    (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (A : E →L[ℝ] E) (hA : A.IsSymmetric) (x : sphere (0 : E) 1) :
    ∀ z : (ℝ ∙ (x : E))ᗮ,
      ((∀ w : TangentSpace (𝓡 n) x,
        mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x w =
          ⟪mvfderiv (𝓡 n) ((↑) : sphere (0 : E) 1 → E) x w, (z : E)⟫_ℝ) ↔
        (z : E) = (2 : ℝ) • (A (x : E) - ⟪(x : E), A (x : E)⟫_ℝ • (x : E))) := by
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  have hg : HasGradientAt (fun y : E => ⟪y, A y⟫_ℝ) ((2 : ℝ) • A (x : E)) (x : E) := by
    apply hasGradientAt_iff_hasFDerivAt.mpr
    have hraw := (hA.hasStrictFDerivAt_reApplyInnerSelf (x : E)).hasFDerivAt
    have hfun : (fun y : E => ⟪y, A y⟫_ℝ) = A.reApplyInnerSelf := by
      funext y
      simp [ContinuousLinearMap.reApplyInnerSelf_apply, real_inner_comm]
    have hlin : toDual ℝ E ((2 : ℝ) • A (x : E)) =
        (2 : ℕ) • innerSL ℝ (A (x : E)) := by
      ext v
      simp [toDual_apply_apply, two_smul]
    rw [hfun, hlin]
    exact hraw
  let K := (ℝ ∙ (x : E))ᗮ
  have hproj (u : E) : (K.orthogonalProjectionOnto u : E) =
      u - ⟪(x : E), u⟫_ℝ • (x : E) := by
    change (ℝ ∙ (x : E))ᗮ.starProjection u = _
    rw [Submodule.starProjection_orthogonal_val,
      Submodule.starProjection_unit_singleton ℝ hx]
  have hp : (K.orthogonalProjectionOnto ((2 : ℝ) • A (x : E)) : E) =
      (2 : ℝ) • (A (x : E) - ⟪(x : E), A (x : E)⟫_ℝ • (x : E)) := by
    rw [hproj]
    simp [inner_smul_right, smul_sub, smul_smul]
  intro z
  rw [SphereGradient.sphere_gradient_characterization n x hg z]
  constructor
  · intro hz
    exact (congrArg (fun v : K => (v : E)) hz).trans hp
  · intro hz
    apply Subtype.ext
    exact hz.trans hp.symm

/-- Genuine sphere stationarity is equivalent both to the Rayleigh-coefficient
equation and to actual eigenvectorhood; unit membership supplies nonzeroness. -/
theorem sphere_rayleigh_stationary_iff
    (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (A : E →L[ℝ] E) (hA : A.IsSymmetric) (x : sphere (0 : E) 1) :
    (mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x = 0 ↔
      A (x : E) = ⟪(x : E), A (x : E)⟫_ℝ • (x : E)) ∧
    (mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x = 0 ↔
      ∃ μ : ℝ, Module.End.HasEigenvector A.toLinearMap μ (x : E)) := by
  have hx : ‖(x : E)‖ = 1 := mem_sphere_zero_iff_norm.mp x.property
  have hxne : (x : E) ≠ 0 := by
    intro hz
    simp [hz] at hx
  have hzero := sphere_rayleigh_characterization n A hA x 0
  have hd :
      mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x = 0 ↔
        A (x : E) = ⟪(x : E), A (x : E)⟫_ℝ • (x : E) := by
    have he :
        mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x = 0 ↔
          ∀ w : TangentSpace (𝓡 n) x,
            mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x w = 0 := by
      constructor
      · intro h w
        rw [h]
        rfl
      · intro h
        ext w
        exact h w
    rw [he]
    have hs : (0 : E) = (2 : ℝ) •
        (A (x : E) - ⟪(x : E), A (x : E)⟫_ℝ • (x : E)) ↔
          A (x : E) = ⟪(x : E), A (x : E)⟫_ℝ • (x : E) := by
      rw [eq_comm, smul_eq_zero, sub_eq_zero]
      simp
    have hpair :
        (∀ w : TangentSpace (𝓡 n) x,
          mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ⟪(y : E), A (y : E)⟫_ℝ) x w = 0) ↔
          (0 : E) = (2 : ℝ) • (A (x : E) - ⟪(x : E), A (x : E)⟫_ℝ • (x : E)) := by
      simpa only [Submodule.coe_zero, inner_zero_right] using hzero
    exact hpair.trans hs
  refine ⟨hd, ?_⟩
  constructor
  · intro h
    exact ⟨⟪(x : E), A (x : E)⟫_ℝ,
      Module.End.mem_eigenspace_iff.mpr (hd.mp h), hxne⟩
  · rintro ⟨μ, hμ⟩
    have hAx : A (x : E) = μ • (x : E) := hμ.apply_eq_smul
    have hcoef : ⟪(x : E), A (x : E)⟫_ℝ = μ := by
      rw [hAx, inner_smul_right]
      simp [hx]
    apply hd.mpr
    rw [hcoef]
    exact hAx

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleigh
