import Mathlib.MeasureTheory.Constructions.Pi

/-!
Zhou–Suzuki, *On Complexity of Gaussian Sampling*, Appendix B, Lemma B.3.
This finite-product step works at a fixed history and a fixed queried index.
The selected-block observation and residual have product law by the single-block
calculation. All other coordinates are read from the original tuple.
-/

open MeasureTheory

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

variable {k : ℕ} {X : Fin (k + 1) → Type*} [∀ j, MeasurableSpace (X j)]
    {Z R : Type*} [MeasurableSpace Z] [MeasurableSpace R]

/-- Expose one observation and retain the smaller residual together with every
unqueried coordinate, in its original order with the selected index skipped. -/
theorem split_selected_coordinate (μ : ∀ j, Measure (X j)) [∀ j, SigmaFinite (μ j)]
    (i : Fin (k + 1)) (σ : Measure Z) (ν : Measure R) [SFinite ν]
    {step : X i → Z × R} (hstep : MeasurePreserving step (μ i) (σ.prod ν)) :
    MeasurePreserving
      (fun x : ∀ j, X j => ((step (x i)).1, (step (x i)).2, fun l => x (i.succAbove l)))
      (Measure.pi μ) (σ.prod (ν.prod (Measure.pi fun l => μ (i.succAbove l)))) := by
  let rest := Measure.pi fun l => μ (i.succAbove l)
  exact (measurePreserving_prodAssoc σ ν rest).comp
    ((hstep.prod (MeasurePreserving.id rest)).comp (measurePreserving_piFinSuccAbove μ i))

/-- Restore all the original labels after a coordinate update. Off the
selected index the maps `keep` can be the identity, or transports identifying
the old and new dependent factor types. -/
theorem replace_selected_coordinate {Y : Fin (k + 1) → Type*} [∀ j, MeasurableSpace (Y j)]
    (μ : ∀ j, Measure (X j)) [∀ j, SigmaFinite (μ j)]
    (ν : ∀ j, Measure (Y j)) [∀ j, SigmaFinite (ν j)]
    (i : Fin (k + 1)) (σ : Measure Z) [SFinite σ] {step : X i → Z × Y i}
    (hstep : MeasurePreserving step (μ i) (σ.prod (ν i)))
    {keep : ∀ l, X (i.succAbove l) → Y (i.succAbove l)}
    (hkeep : ∀ l, MeasurePreserving (keep l) (μ (i.succAbove l)) (ν (i.succAbove l))) :
    MeasurePreserving
      (fun x : ∀ j, X j => ((step (x i)).1,
        i.insertNth (α := Y) (step (x i)).2 (fun l => keep l (x (i.succAbove l)))))
      (Measure.pi μ) (σ.prod (Measure.pi ν)) := by
  have hrest := measurePreserving_pi (fun l => μ (i.succAbove l))
    (fun l => ν (i.succAbove l)) hkeep
  have hresidual := ((measurePreserving_piFinSuccAbove ν i).symm).comp
    ((MeasurePreserving.id (ν i)).prod hrest)
  exact ((MeasurePreserving.id σ).prod hresidual).comp
    (split_selected_coordinate μ i σ (ν i) hstep)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
