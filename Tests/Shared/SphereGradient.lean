import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereGradient
import Mathlib.Analysis.InnerProductSpace.Calculus

noncomputable section

namespace AutoSamplingTheory.Tests.Shared.SphereGradient

open Metric
open scoped Manifold InnerProductSpace
open TechnicalLemmas.Geometry.SphereGradient

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]

-- Construct the true sphere differential and its unique induced representative
-- for an actual linear objective. No gradient/equality conclusion is a premise.
example (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (x : sphere (0 : E) 1) (g : E) :
    ∃! z : (ℝ ∙ (x : E))ᗮ,
      ∀ w : TangentSpace (𝓡 n) x,
        mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => inner ℝ g (y : E)) x w =
          ⟪mvfderiv (𝓡 n) ((↑) : sphere (0 : E) 1 → E) x w, (z : E)⟫_ℝ := by
  have hg : HasGradientAt (fun y : E => inner ℝ g y) g (x : E) :=
    hasGradientAt_iff_hasFDerivAt.mpr (InnerProductSpace.toDual ℝ E g).hasFDerivAt
  let p := (ℝ ∙ (x : E))ᗮ.orthogonalProjectionOnto g
  refine ⟨p, (sphere_gradient_characterization n x hg p).mpr rfl, ?_⟩
  intro z hz
  exact (sphere_gradient_characterization n x hg z).mp hz

-- The actual ambient squared-norm gradient is 2x, but its sphere differential
-- is zero. This detects returning the ambient gradient without projection.
example (n : ℕ) [Fact (Module.finrank ℝ E = n + 1)]
    (x : sphere (0 : E) 1) (w : TangentSpace (𝓡 n) x) :
    mvfderiv (𝓡 n) (fun y : sphere (0 : E) 1 => ‖(y : E)‖ ^ 2) x w = 0 := by
  have hg : HasGradientAt (fun y : E => ‖y‖ ^ 2) ((2 : ℝ) • (x : E)) (x : E) := by
    apply hasGradientAt_iff_hasFDerivAt.mpr
    have he : (2 : ℕ) • innerSL ℝ (x : E) =
        InnerProductSpace.toDual ℝ E ((2 : ℝ) • (x : E)) := by
      ext v
      simp [two_smul, inner_smul_left]
    rw [← he]
    exact (hasStrictFDerivAt_norm_sq (x : E)).hasFDerivAt
  have hp : (ℝ ∙ (x : E))ᗮ.orthogonalProjectionOnto ((2 : ℝ) • (x : E)) = 0 := by
    rw [map_smul, Submodule.orthogonalProjectionOnto_orthogonalComplement_singleton_eq_zero,
      smul_zero]
  have h := (sphere_gradient_characterization n x hg 0).mpr hp.symm w
  simpa using h

#print axioms TechnicalLemmas.Geometry.SphereGradient.sphere_gradient_characterization

end AutoSamplingTheory.Tests.Shared.SphereGradient
