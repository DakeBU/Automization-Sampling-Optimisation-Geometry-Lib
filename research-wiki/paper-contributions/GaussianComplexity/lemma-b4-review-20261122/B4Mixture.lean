import Mathlib.MeasureTheory.Measure.Prod

/-!
Compare two experiments by exposing the same sphere observation in each.
The continuation may use every retained latent variable.
-/

open MeasureTheory

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

/-- A common observation law and equal conditional output laws give equal
output laws after mixing. The two latent distributions may differ. -/
theorem map_prod_eq_of_fiber_maps {Z V X : Type*}
    [MeasurableSpace Z] [MeasurableSpace V] [MeasurableSpace X]
    (σ : Measure Z) (ν₁ ν₂ : Measure V) [SFinite ν₁] [SFinite ν₂]
    (f : Z × V → X) (hf : Measurable f)
    (h : ∀ z, ν₁.map (fun v => f (z,v)) = ν₂.map (fun v => f (z,v))) :
    (σ.prod ν₁).map f = (σ.prod ν₂).map f := by
  ext s hs
  rw [Measure.map_apply hf hs, Measure.map_apply hf hs,
    Measure.prod_apply (hf hs), Measure.prod_apply (hf hs)]
  apply lintegral_congr
  intro z
  have hz := congrArg (fun μ : Measure X => μ s) (h z)
  have hm : Measurable (fun v : V => f (z,v)) := hf.comp measurable_prodMk_left
  change ν₁.map (fun v => f (z,v)) s = ν₂.map (fun v => f (z,v)) s at hz
  rw [Measure.map_apply hm hs, Measure.map_apply hm hs] at hz
  exact hz

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
