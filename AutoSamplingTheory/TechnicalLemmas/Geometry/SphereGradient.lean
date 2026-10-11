import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.Analysis.Calculus.Gradient.Basic

/-!
# The induced gradient on a sphere

The actual derivative of the sphere inclusion identifies chart tangent directions
with the ambient orthogonal tangent plane. Pairing through this inclusion gives
the induced metric, rather than the default inner product on chart coordinates.
A genuine ambient gradient therefore determines the unique tangent representative
of the actual restricted manifold differential by orthogonal projection.
-/

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereGradient

open Metric
open scoped Manifold InnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]

/-- The orthogonal projection of the genuine ambient gradient is exactly the
unique ambient tangent vector representing the true sphere differential with
its induced pairing. No default chart metric is identified with this pairing. -/
theorem sphere_gradient_characterization
    (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (x : sphere (0 : E) 1) {f : E → ℝ} {g : E}
    (hf : HasGradientAt f g (x : E)) :
    ∀ z : (ℝ ∙ (x : E))ᗮ,
      ((∀ w : TangentSpace (𝓡 n) x,
        mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => f (y : E)) x w =
          ⟪mvfderiv (𝓡 n) ((↑) : sphere (0 : E) 1 → E) x w, (z : E)⟫_ℝ) ↔
        z = (ℝ ∙ (x : E))ᗮ.orthogonalProjectionOnto g) := by
  let K := (ℝ ∙ (x : E))ᗮ
  let A := mvfderiv (𝓡 n) ((↑) : sphere (0 : E) 1 → E) x
  have hA : A.range = K := range_mvfderiv_subtypeVal x
  have hco := (contMDiff_coe_sphere (n := n) (m := 1) x).mdifferentiableAt one_ne_zero
  have hd : ∀ w : TangentSpace (𝓡 n) x,
      mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => f (y : E)) x w =
        ⟪A w, g⟫_ℝ := by
    intro w
    have hchain := mvfderiv_comp x hf.differentiableAt.mdifferentiableAt hco
    change mvfderiv (𝓡 n) (f ∘ ((↑) : sphere (0 : E) 1 → E)) x w = _
    rw [hchain]
    convert! (hf.fderiv_apply (y := A w)) using 1 <;>
      simp [A, mvfderiv, NormedSpace.fromTangentSpace, real_inner_comm] <;> rfl
  have hp : ∀ w : TangentSpace (𝓡 n) x,
      mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => f (y : E)) x w =
        ⟪A w, (K.orthogonalProjectionOnto g : E)⟫_ℝ := by
    intro w
    have hw : A w ∈ K := hA ▸ (show A w ∈ A.range from ⟨w, rfl⟩)
    rw [hd w]
    exact (K.inner_orthogonalProjectionOnto_eq_of_mem_left ⟨A w, hw⟩ g).symm
  intro z
  constructor
  · intro hz
    apply ext_inner_left ℝ
    intro v
    have hv : (v : E) ∈ A.range := hA.symm ▸ v.property
    obtain ⟨w, hw⟩ := hv
    change ⟪(v : E), (z : E)⟫_ℝ = ⟪(v : E), (K.orthogonalProjectionOnto g : E)⟫_ℝ
    rw [← hw]
    exact (hz w).symm.trans (hp w)
  · rintro rfl
    exact hp

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereGradient
