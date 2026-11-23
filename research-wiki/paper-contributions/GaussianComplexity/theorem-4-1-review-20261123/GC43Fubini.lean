import GC43WalkStarts
import GC43ConsLaw

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {A B C V : Type*} [MeasurableSpace A] [MeasurableSpace B] [MeasurableSpace C]
  [MeasurableSpace V]

theorem split_noise {k : ℕ} (μ : Measure A) [SigmaFinite μ] (ν : Measure B) [SigmaFinite ν] :
    MeasurePreserving (fun p : A × (Fin (k+1) → B) => (p.2 0, (p.1, Fin.tail p.2)))
      (μ.prod (Measure.pi (fun _ : Fin (k+1) => ν)))
      (ν.prod (μ.prod (Measure.pi (fun _ : Fin k => ν)))) := by
  let η := Measure.pi (fun _ : Fin k => ν)
  have ht : MeasurePreserving (fun z : Fin (k+1) → B => (z 0, Fin.tail z))
      (Measure.pi (fun _ : Fin (k+1) => ν)) (ν.prod η) := by
    convert measurePreserving_piFinSuccAbove (fun _ : Fin (k+1) => ν) (0 : Fin (k+1)) using 1
    funext z
    apply Prod.ext rfl
    funext i
    change z i.succ = z ((0 : Fin (k+1)).succAbove i)
    rw [Fin.succAbove_zero]
  exact (measurePreserving_prodAssoc ν μ η).comp
    (((Measure.measurePreserving_swap (μ := μ) (ν := ν)).prod (MeasurePreserving.id η)).comp
      ((measurePreserving_prodAssoc μ ν η).symm.comp ((MeasurePreserving.id μ).prod ht)))

theorem split_informative {k : ℕ} (μ : Measure A) [SigmaFinite μ] (ν : Measure B) [SigmaFinite ν]
    (σ : Measure C) [SigmaFinite σ] (η : Measure V) [SigmaFinite η] (read : A → C × V)
    (hread : MeasurePreserving read μ (σ.prod η)) :
    MeasurePreserving
      (fun p : A × (Fin (k+1) → B) => ((p.2 0,(read p.1).1),((read p.1).2,Fin.tail p.2)))
      (μ.prod (Measure.pi (fun _ : Fin (k+1) => ν)))
      ((ν.prod σ).prod (η.prod (Measure.pi (fun _ : Fin k => ν)))) := by
  let ξ := Measure.pi (fun _ : Fin k => ν)
  exact (measurePreserving_prodAssoc ν σ (η.prod ξ)).symm.comp
    (((MeasurePreserving.id ν).prod (measurePreserving_prodAssoc σ η ξ)).comp
      (((MeasurePreserving.id ν).prod (hread.prod (MeasurePreserving.id ξ))).comp (split_noise μ ν)))

theorem full_haar_observation {N m : ℕ} [NeZero m] (F : BlockFrame N m) (b : Bool) (v : Vec N) :
    MeasurePreserving (frameObservation F b v) (orthogonalHaar m) (sphereProbability m) := by
  let u := frameUnit F b v
  have hr : MeasurePreserving (fun W : O m => rotate W u) (orthogonalHaar m) (sphereProbability m) :=
    ⟨(continuous_rotate.comp (continuous_id.prodMk continuous_const)).measurable, haar_rotate_fixed u⟩
  cases b
  · exact hr
  · have hi : MeasurePreserving (Inv.inv : O m → O m) (orthogonalHaar m) (orthogonalHaar m) := by
      refine ⟨measurable_inv,?_⟩
      rw [haar_as_components, Measure.map_smul, Measure.map_add _ _ measurable_inv,
        componentHaar_map_inv, componentHaar_map_inv]
    exact hr.comp hi

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
