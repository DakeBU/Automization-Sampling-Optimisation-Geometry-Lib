import GC43Fubini
import Mathlib.Probability.Kernel.CondDistrib
import Mathlib.Probability.Independence.Basic

/-! Conditional laws with an arbitrary measurable history and an arbitrary underlying experiment. -/
noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H X Y Z : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  [MeasurableSpace X] [MeasurableSpace Y] [MeasurableSpace Z]

/-- A version-independent formulation of a constant conditional law. The measurable
history may encode any sub-σ-algebra by the identity map to its own measurable space. -/
def LawGiven (μ : Measure Ω) (history : Ω → H) (value : Ω → X) (ν : Measure X) : Prop :=
  MeasurePreserving (fun ω => (history ω,value ω)) μ ((μ.map history).prod ν)

theorem LawGiven.of_joint {μ : Measure Ω} {h : Ω → H} {x : Ω → X}
    {ρ : Measure H} {ν : Measure X} [IsProbabilityMeasure ν]
    (hp : MeasurePreserving (fun ω => (h ω,x ω)) μ (ρ.prod ν)) : LawGiven μ h x ν := by
  have hm : MeasurePreserving h μ ρ := (measurePreserving_fst (μ := ρ) (ν := ν)).comp hp
  simpa [LawGiven, hm.map_eq] using hp

theorem LawGiven.condDistrib_eq {μ : Measure Ω} [IsFiniteMeasure μ]
    [StandardBorelSpace X] [Nonempty X] {h : Ω → H} {x : Ω → X}
    {ν : Measure X} [IsFiniteMeasure ν] (hp : LawGiven μ h x ν) :
    condDistrib x h μ =ᵐ[μ.map h] Kernel.const H ν := by
  have hx : Measurable x := measurable_snd.comp hp.measurable
  apply condDistrib_ae_eq_of_measure_eq_compProd h hx.aemeasurable
  simpa only [Measure.compProd_const] using hp.map_eq

theorem LawGiven.of_condDistrib {μ : Measure Ω} [IsFiniteMeasure μ]
    [StandardBorelSpace X] [Nonempty X] {h : Ω → H} {x : Ω → X}
    {ν : Measure X} [IsFiniteMeasure ν] (hh : Measurable h) (hx : Measurable x)
    (hp : condDistrib x h μ =ᵐ[μ.map h] Kernel.const H ν) : LawGiven μ h x ν := by
  refine ⟨hh.prodMk hx, ?_⟩
  simpa only [Measure.compProd_const] using
    (condDistrib_ae_eq_iff_measure_eq_compProd h hx.aemeasurable (Kernel.const H ν)).mp hp

theorem LawGiven.map_history {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {x : Ω → X}
    {ν : Measure X} [IsProbabilityMeasure ν] (hp : LawGiven μ h x ν)
    {f : H → Y} (hf : Measurable f) : LawGiven μ (fun ω => f (h ω)) x ν := by
  exact LawGiven.of_joint (((⟨hf,rfl⟩ : MeasurePreserving f (μ.map h) ((μ.map h).map f)).prod
    (MeasurePreserving.id ν)).comp hp)

theorem LawGiven.congr_ae {μ : Measure Ω} {h h' : Ω → H} {x x' : Ω → X}
    {ν : Measure X} (hp : LawGiven μ h x ν) (hm : Measurable h') (xm : Measurable x')
    (he : h =ᵐ[μ] h') (xe : x =ᵐ[μ] x') : LawGiven μ h' x' ν := by
  refine ⟨hm.prodMk xm,?_⟩
  rw [← Measure.map_congr he, ← hp.map_eq]
  apply Measure.map_congr
  filter_upwards [he,xe] with ω hh hx using Prod.ext hh.symm hx.symm

theorem LawGiven.restrict_history {μ : Measure Ω} [IsFiniteMeasure μ]
    {h : Ω → H} {x : Ω → X} {ν : Measure X} [IsProbabilityMeasure ν]
    (hp : LawGiven μ h x ν) {s : Set H} (hs : MeasurableSet s) :
    LawGiven (μ.restrict (h ⁻¹' s)) h x ν := by
  let t : Set (H × X) := s ×ˢ Set.univ
  have ht : MeasurableSet t := hs.prod MeasurableSet.univ
  have he : (fun ω => (h ω,x ω)) ⁻¹' t = h ⁻¹' s := by ext ω; simp [t]
  apply LawGiven.of_joint (ρ := (μ.map h).restrict s)
  refine ⟨hp.measurable,?_⟩
  rw [← he, ← Measure.restrict_map hp.measurable ht, hp.map_eq, Measure.restrict_prod_eq_prod_univ]

/-- Independent auxiliary randomness can be adjoined to any history without
changing the conditional law. Independence is required only of the actual joint
history and value, on their original probability space. -/
theorem LawGiven.independent_auxiliary {μ : Measure Ω} [IsProbabilityMeasure μ]
    {h : Ω → H} {x : Ω → X} {ν : Measure X} [IsProbabilityMeasure ν]
    (hp : LawGiven μ h x ν) {z : Ω → Z} (hz : Measurable z)
    (hi : IndepFun (fun ω => (h ω,x ω)) z μ) :
    LawGiven μ (fun ω => (h ω,z ω)) x ν := by
  let ρ := μ.map h
  let ζ := μ.map z
  have hall : MeasurePreserving (fun ω => ((h ω,x ω),z ω)) μ ((ρ.prod ν).prod ζ) := by
    refine ⟨hp.measurable.prodMk hz,?_⟩
    rw [hi.map_prod_eq_prod_map_map hp.measurable.aemeasurable hz.aemeasurable, hp.map_eq]
  let perm := (measurePreserving_prodAssoc ρ ζ ν).symm.comp
    (((MeasurePreserving.id ρ).prod (Measure.measurePreserving_swap (μ := ν) (ν := ζ))).comp
      (measurePreserving_prodAssoc ρ ν ζ))
  exact LawGiven.of_joint (perm.comp hall)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
