import Mathlib.Analysis.Calculus.Deriv.Comp

/-!
# Extension-independent derivatives along feasible curves

The relative germ of an ambient map determines its derivative on every actual
velocity of a curve locally in the feasible set. This is the explicit
extension-independence step following Boumal §3.4 Proposition 3.35. The general
normed-space interface does not define a manifold tangent space or identify
the complete manifold differential.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.CurveExtension

open Filter Set
open scoped Topology

variable {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]

/-- Ambient maps agreeing locally relative to a feasible set have equal actual
derivatives on the velocity of any differentiable curve locally in that set.
The maps need only be genuinely differentiable at the actual curve point. -/
theorem fderiv_eq_on_curve_velocity
    {s : Set E} {f g : E → F} {c : ℝ → E} {t₀ : ℝ} {v : E}
    (hf : DifferentiableAt ℝ f (c t₀))
    (hg : DifferentiableAt ℝ g (c t₀))
    (hc : HasDerivAt c v t₀)
    (hcs : ∀ᶠ t in 𝓝 t₀, c t ∈ s)
    (hfg : f =ᶠ[𝓝[s] (c t₀)] g) :
    fderiv ℝ f (c t₀) v = fderiv ℝ g (c t₀) v := by
  have hcts : Tendsto c (𝓝 t₀) (𝓝[s] (c t₀)) :=
    tendsto_nhdsWithin_iff.mpr ⟨hc.continuousAt, hcs⟩
  have hcomp : (f ∘ c) =ᶠ[𝓝 t₀] (g ∘ c) := hfg.comp_tendsto hcts
  have hfc := hf.hasFDerivAt.comp_hasDerivAt t₀ hc
  have hgc := hg.hasFDerivAt.comp_hasDerivAt t₀ hc
  exact (hfc.congr_of_eventuallyEq hcomp.symm).unique hgc

end AutoSamplingTheory.TechnicalLemmas.Geometry.CurveExtension
