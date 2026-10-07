import AutoSamplingTheory.TechnicalLemmas.Measure.Transport
import Mathlib.Probability.Kernel.Disintegration.StandardBorel

/-!
# Gluing of transport plans

For finite measures on a standard Borel space, disintegrate the second plan
and compose it with the first:

`γ₁₂₃ := γ₁₂ ⊗ₘ (γ₂₃.condKernel ∘ π₂)`.

This is the measure-theoretic core of the gluing argument used for the
Wasserstein triangle inequality.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace TransportGluing

open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory ENNReal

/-- The three-coordinate measure used in the gluing argument:

`γ₁₂₃(dx,dy,dz) = γ₁₂(dx,dy) γ₂₃(dz | y)`.

The product is encoded as `((x,y),z)`. -/
noncomputable def gluingMeasure
    {α : Type*} [MeasurableSpace α] [StandardBorelSpace α] [Nonempty α]
    (γ₁₂ γ₂₃ : Measure (α × α)) [IsFiniteMeasure γ₂₃] :
    Measure ((α × α) × α) :=
  γ₁₂ ⊗ₘ Kernel.prodMkLeft α γ₂₃.condKernel

/-- The `(x,y)` marginal of `γ₁₂₃` is the prescribed first plan:

`(π₁₂)♯ γ₁₂₃ = γ₁₂`. -/
@[simp]
theorem fst_gluingMeasure
    {α : Type*} [MeasurableSpace α] [StandardBorelSpace α] [Nonempty α]
    (γ₁₂ γ₂₃ : Measure (α × α)) [SFinite γ₁₂] [IsFiniteMeasure γ₂₃] :
    (gluingMeasure γ₁₂ γ₂₃).fst = γ₁₂ := by
  unfold gluingMeasure
  exact Measure.fst_compProd _ _

/-- If the second marginal of the first plan is the first marginal of the
second plan, then the `(y,z)` marginal of the glued measure is exactly the
second plan:

`(π₂₃)♯ γ₁₂₃ = γ₂₃`. -/
theorem map_snd_fst_gluingMeasure
    {α : Type*} [MeasurableSpace α] [StandardBorelSpace α] [Nonempty α]
    (γ₁₂ γ₂₃ : Measure (α × α)) [SFinite γ₁₂] [IsFiniteMeasure γ₂₃]
    (hshared : γ₁₂.snd = γ₂₃.fst) :
    Measure.map (fun p : ((α × α) × α) => (p.1.2, p.2))
        (gluingMeasure γ₁₂ γ₂₃) = γ₂₃ := by
  let q : ((α × α) × α) → α × α := fun p => (p.1.2, p.2)
  have hq : Measurable q :=
    (measurable_snd.comp measurable_fst).prodMk measurable_snd
  ext s hs
  rw [Measure.map_apply hq hs]
  unfold gluingMeasure
  rw [Measure.compProd_apply (hs.preimage hq)]
  change (∫⁻ a : α × α,
      γ₂₃.condKernel a.2 (Prod.mk a.2 ⁻¹' s) ∂γ₁₂) = γ₂₃ s
  let F : α → ℝ≥0∞ := fun y => γ₂₃.condKernel y (Prod.mk y ⁻¹' s)
  have hF : Measurable F := Kernel.measurable_kernel_prodMk_left hs
  calc
    (∫⁻ a : α × α, γ₂₃.condKernel a.2 (Prod.mk a.2 ⁻¹' s) ∂γ₁₂) =
        ∫⁻ y, F y ∂γ₁₂.snd := by
      rw [Measure.snd]
      exact (lintegral_map hF measurable_snd).symm
    _ = ∫⁻ y, F y ∂γ₂₃.fst := by rw [hshared]
    _ = (γ₂₃.fst ⊗ₘ γ₂₃.condKernel) s := by
      rw [Measure.compProd_apply hs]
    _ = γ₂₃ s := by rw [Measure.disintegrate γ₂₃ γ₂₃.condKernel]

/-- Source-shaped gluing statement for two couplings with a shared middle
marginal. It packages the two pair-marginal identities without assuming
optimality of either plan. -/
theorem exists_gluing_of_isCoupling
    {α : Type*} [MeasurableSpace α] [StandardBorelSpace α] [Nonempty α]
    {μ₁ μ₂ μ₃ : Measure α}
    (γ₁₂ γ₂₃ : Measure (α × α))
    [IsProbabilityMeasure μ₁] [IsProbabilityMeasure μ₂] [IsProbabilityMeasure μ₃]
    (h₁₂ : Transport.IsCoupling γ₁₂ μ₁ μ₂)
    (h₂₃ : Transport.IsCoupling γ₂₃ μ₂ μ₃) :
    ∃ γ₁₂₃ : Measure ((α × α) × α),
      γ₁₂₃.fst = γ₁₂ ∧
      Measure.map (fun p : ((α × α) × α) => (p.1.2, p.2)) γ₁₂₃ = γ₂₃ := by
  letI : IsProbabilityMeasure γ₁₂ :=
    Transport.isProbabilityMeasure_of_isCoupling_left h₁₂
  letI : IsProbabilityMeasure γ₂₃ :=
    Transport.isProbabilityMeasure_of_isCoupling_left h₂₃
  refine ⟨gluingMeasure γ₁₂ γ₂₃, fst_gluingMeasure γ₁₂ γ₂₃, ?_⟩
  exact map_snd_fst_gluingMeasure γ₁₂ γ₂₃ (h₁₂.2.trans h₂₃.1.symm)

end TransportGluing
end Measure
end TechnicalLemmas
end AutoSamplingTheory
