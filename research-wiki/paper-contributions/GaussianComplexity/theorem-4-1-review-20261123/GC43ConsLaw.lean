import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.Probability.Kernel.Composition.MeasureCompProd

/-! Prepending a fresh random variable to a continuation of constant conditional law. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ENNReal
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {A B X Y : Type*} [MeasurableSpace A] [MeasurableSpace B] [MeasurableSpace X]
  [MeasurableSpace Y]

theorem pairLaw_of_constant_continuation (μ : Measure A) [SFinite μ] (K : Kernel A B)
    [IsSFiniteKernel K] (ξ : Measure X) (η : Measure Y) [SFinite η]
    (f : A → X) (h : A × B → Y) (hf : MeasurePreserving f μ ξ) (hh : Measurable h)
    (hcond : ∀ᵐ a ∂μ, (K a).map (fun b => h (a,b)) = η) :
    MeasurePreserving (fun p : A × B => (f p.1,h p)) (μ ⊗ₘ K) (ξ.prod η) := by
  have hm : Measurable (fun p : A × B => (f p.1,h p)) := (hf.measurable.comp measurable_fst).prodMk hh
  refine ⟨hm, ?_⟩
  ext s hs
  rw [Measure.map_apply hm hs, Measure.compProd_apply (hm hs), Measure.prod_apply hs,
    ← hf.lintegral_comp (measurable_measure_prodMk_left hs)]
  apply lintegral_congr_ae
  filter_upwards [hcond] with a ha
  have eqmass := congrArg (fun m : Measure Y => m (Prod.mk (f a) ⁻¹' s)) ha
  change ((K a).map (fun b => h (a,b))) _ = _ at eqmass
  have hslic : Measurable (fun b => h (a,b)) := hh.comp measurable_prodMk_left
  rw [Measure.map_apply hslic (measurable_prodMk_left hs)] at eqmass
  exact eqmass

theorem consLaw {n : ℕ} (ξ : Measure X) [SigmaFinite ξ] :
    MeasurePreserving (fun p : X × (Fin n → X) => Fin.cons p.1 p.2)
      (ξ.prod (Measure.pi (fun _ : Fin n => ξ)))
      (Measure.pi (fun _ : Fin (n+1) => ξ)) := by
  have h := (measurePreserving_piFinSuccAbove (fun _ : Fin (n+1) => ξ) 0).symm
  convert h using 1
  funext p
  exact (Fin.insertNth_zero' p.1 p.2).symm

theorem consLaw_of_constant_continuation {n : ℕ} (μ : Measure A) [SFinite μ]
    (K : Kernel A B) [IsSFiniteKernel K] (ξ : Measure X) [SigmaFinite ξ]
    (f : A → X) (h : A × B → Fin n → X) (hf : MeasurePreserving f μ ξ) (hh : Measurable h)
    (hcond : ∀ᵐ a ∂μ, (K a).map (fun b => h (a,b)) = Measure.pi (fun _ : Fin n => ξ)) :
    MeasurePreserving (fun p : A × B => Fin.cons (f p.1) (h p))
      (μ ⊗ₘ K) (Measure.pi (fun _ : Fin (n+1) => ξ)) :=
  (consLaw ξ).comp (pairLaw_of_constant_continuation μ K ξ _ f h hf hh hcond)

theorem consLaw_of_constant_fibers {n : ℕ} (μ : Measure A) [SFinite μ]
    (ν : Measure B) [SFinite ν] (ξ : Measure X) [SigmaFinite ξ]
    (f : A → X) (h : A × B → Fin n → X) (hf : MeasurePreserving f μ ξ) (hh : Measurable h)
    (hcond : ∀ᵐ a ∂μ, ν.map (fun b => h (a,b)) = Measure.pi (fun _ : Fin n => ξ)) :
    MeasurePreserving (fun p : A × B => Fin.cons (f p.1) (h p))
      (μ.prod ν) (Measure.pi (fun _ : Fin (n+1) => ξ)) := by
  simpa only [Measure.compProd_const] using
    consLaw_of_constant_continuation μ (Kernel.const A ν) ξ f h hf hh hcond

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
