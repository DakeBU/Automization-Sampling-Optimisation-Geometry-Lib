import GC3JointIteration

/-! A representation by an observed variable and independent residual noise gives a
posterior kernel when the noise is reassembled into the original hidden object. -/
open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
variable {X Y Z U : Type*} [MeasurableSpace X] [MeasurableSpace Y] [MeasurableSpace Z] [MeasurableSpace U]

theorem joint_of_generated (μ : Measure X) [IsProbabilityMeasure μ]
    (J : Kernel Y X) [IsMarkovKernel J] (a : X → Y) (ha : Measurable a)
    (σ : Measure Z) [IsProbabilityMeasure σ] (ν : Measure U) [IsProbabilityMeasure ν]
    (t : Z → Y) (ht : Measurable t) (gen : Z × U → X) (hg : MeasurePreserving gen (σ.prod ν) μ)
    (agree : ∀ z u, a (gen (z,u)) = t z)
    (fiber : ∀ z, ν.map (fun u => gen (z,u)) = J (t z)) :
    μ.map (fun x => (a x,x)) = (μ.map a) ⊗ₘ J := by
  have haPair : Measurable (fun x => (a x,x)) := ha.prodMk measurable_id
  have hj : μ.map (fun x => (a x,x)) = (σ.map t) ⊗ₘ J := by
    rw [← hg.map_eq, Measure.map_map haPair hg.measurable]
    ext s hs
    have hm := haPair.comp hg.measurable
    rw [Measure.map_apply hm hs, Measure.prod_apply (hm hs), Measure.compProd_apply hs,
      lintegral_map (Kernel.measurable_kernel_prodMk_left hs) ht]
    apply lintegral_congr
    intro z
    rw [← fiber, Measure.map_apply (show Measurable (fun u => gen (z,u)) from hg.measurable.comp measurable_prodMk_left)
      (measurable_prodMk_left hs)]
    congr 1
    ext u
    change (a (gen (z,u)), gen (z,u)) ∈ s ↔ (t z,gen (z,u)) ∈ s
    rw [agree]
  have he := congrArg Measure.fst hj
  rw [Measure.fst_compProd] at he
  change (μ.map (fun x => (a x,x))).map Prod.fst = σ.map t at he
  rw [Measure.map_map measurable_fst haPair] at he
  exact (show μ.map a = σ.map t from he) ▸ hj

theorem joint_of_constant (μ : Measure X) [IsProbabilityMeasure μ]
    (J : Kernel Y X) [IsMarkovKernel J] (a : X → Y) (_ha : Measurable a)
    (t : Y) (agree : ∀ᵐ x ∂μ, a x = t) (hJ : J t = μ) :
    μ.map (fun x => (a x,x)) = (μ.map a) ⊗ₘ J := by
  have he : μ.map (fun x => (a x,x)) = μ.map (Prod.mk t) := by
    apply Measure.map_congr; filter_upwards [agree] with x hx; rw [hx]
  have he' : μ.map a = Measure.dirac t := by
    rw [Measure.map_congr agree]; simp
  rw [he, he']
  ext s hs
  rw [Measure.map_apply measurable_prodMk_left hs, Measure.compProd_apply hs,
    lintegral_dirac' _ (Kernel.measurable_kernel_prodMk_left hs), hJ]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
