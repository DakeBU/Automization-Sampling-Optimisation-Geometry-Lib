import Mathlib.Probability.Kernel.CondDistrib
import Mathlib.Probability.Kernel.Composition.Prod

/-!
# Parameterized pushforward of a probability measure

A measurable family of maps sends independent parameter and noise to a joint law whose
regular conditional distribution is represented by the pointwise pushforward of the noise law.
-/

open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory

namespace AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward

variable {Z V G : Type*} [MeasurableSpace Z] [MeasurableSpace V] [MeasurableSpace G]

/-- Start at `z`, sample noise with law `μ`, and apply `F z`. -/
noncomputable def kernel (μ : Measure V) (F : Z → V → G) : Kernel Z G :=
  ((Kernel.id : Kernel Z Z) ×ₖ Kernel.const Z μ).map (fun p : Z × V => F p.1 p.2)

/-- Full measurability of the parameterized map makes the pushforward kernel Markov. -/
theorem isMarkovKernel_kernel (μ : Measure V) [IsProbabilityMeasure μ] (F : Z → V → G)
    (hF : Measurable (fun p : Z × V => F p.1 p.2)) :
    IsMarkovKernel (kernel μ F) :=
  Kernel.IsMarkovKernel.map _ hF

/-- The pushforward kernel has this representative at every parameter. -/
theorem kernel_apply (μ : Measure V) [IsProbabilityMeasure μ] (F : Z → V → G)
    (hF : Measurable (fun p : Z × V => F p.1 p.2)) (z : Z) :
    kernel μ F z = μ.map (F z) := by
  rw [kernel, Kernel.map_apply _ hF, Kernel.prod_apply, Kernel.id_apply,
    Kernel.const_apply, Measure.dirac_prod, Measure.map_map hF measurable_prodMk_left]
  rfl

/-- Keeping the parameter as the first coordinate gives the kernel composition product. -/
theorem map_prod_eq_compProd (σ : Measure Z) [SFinite σ]
    (μ : Measure V) [IsProbabilityMeasure μ] (F : Z → V → G)
    (hF : Measurable (fun p : Z × V => F p.1 p.2)) :
    (σ.prod μ).map (fun p : Z × V => (p.1, F p.1 p.2)) = σ ⊗ₘ kernel μ F := by
  let : IsMarkovKernel (kernel μ F) := isMarkovKernel_kernel μ F hF
  have hpair : Measurable (fun p : Z × V => (p.1, F p.1 p.2)) :=
    measurable_fst.prodMk hF
  ext s hs
  rw [Measure.map_apply hpair hs, Measure.prod_apply (hpair hs), Measure.compProd_apply hs]
  refine lintegral_congr fun z => ?_
  have hFz : Measurable (F z) := hF.comp (measurable_prodMk_left (x := z))
  rw [kernel_apply μ F hF z, Measure.map_apply hFz (measurable_prodMk_left hs)]
  rfl

/-- The canonical disintegration kernel agrees with the explicit version almost everywhere. -/
theorem condKernel_map_prod_ae_eq_kernel [StandardBorelSpace G] [Nonempty G]
    (σ : Measure Z) [IsFiniteMeasure σ] (μ : Measure V) [IsProbabilityMeasure μ]
    (F : Z → V → G) (hF : Measurable (fun p : Z × V => F p.1 p.2)) :
    ((σ.prod μ).map (fun p : Z × V => (p.1, F p.1 p.2))).condKernel =ᵐ[σ] kernel μ F := by
  let : IsMarkovKernel (kernel μ F) := isMarkovKernel_kernel μ F hF
  let ρ := (σ.prod μ).map (fun p : Z × V => (p.1, F p.1 p.2))
  have hρ : ρ = σ ⊗ₘ kernel μ F := map_prod_eq_compProd σ μ F hF
  have hfst : ρ.fst = σ := by rw [hρ, Measure.fst_compProd]
  have hκ : ρ = ρ.fst ⊗ₘ kernel μ F := by rwa [hfst]
  have h := eq_condKernel_of_measure_eq_compProd (kernel μ F) hκ
  simpa only [hfst] using Filter.EventuallyEq.symm h

end AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
