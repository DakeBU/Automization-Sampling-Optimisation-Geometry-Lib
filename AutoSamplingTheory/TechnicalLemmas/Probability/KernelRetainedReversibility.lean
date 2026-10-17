import Mathlib.Probability.Kernel.Invariance
import Mathlib.Probability.Kernel.Composition.MeasureCompProd

open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal

/-!
# Detailed balance for a retained-coordinate transition

Let the joint law be `μ ⊗ₘ R`. A jointly measurable update `F (a,b)` changes
only `b`. If the update on almost every fiber is reversible under `R a`, the
retained-coordinate joint transition is reversible under the joint law.

This is a canonical nonnegative-flux lemma, not a paper-specific process
construction. It allows s-finite measures and kernels, including zero/empty
cases and infinite fluxes. Markovness, normalization and finite mass are not
assumed. Invariance requires a separate Markov-kernel hypothesis.

Planned consumers: the actual PBPS half-turn adapter (arXiv:2609.06905v1,
Appendix A.2/A.9) and general component-wise Gibbs/heat-bath reversibility.
Disintegration, coordinate transport and the actual all-L2 operator remain
separate obligations. No source theorem or paper completion is claimed here.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Probability.KernelRetainedReversibility

private theorem retained_flux
    {A B : Type*} [MeasurableSpace A] [MeasurableSpace B]
    (μ : Measure A) [SFinite μ]
    (R : Kernel A B) [IsSFiniteKernel R]
    (F : Kernel (A × B) B) [IsSFiniteKernel F]
    {S T : Set (A × B)} (hS : MeasurableSet S) (hT : MeasurableSet T) :
    (∫⁻ z in S, ((Kernel.deterministic Prod.fst measurable_fst) ×ₖ F) z T
      ∂(μ ⊗ₘ R)) =
    ∫⁻ a, ∫⁻ b in Prod.mk a ⁻¹' S, F (a, b) (Prod.mk a ⁻¹' T) ∂R a ∂μ := by
  rw [← lintegral_indicator hS]
  rw [Measure.lintegral_compProd
    ((((Kernel.deterministic Prod.fst measurable_fst) ×ₖ F).measurable_coe hT).indicator hS)]
  apply lintegral_congr
  intro a
  rw [← lintegral_indicator (hS.preimage measurable_prodMk_left)]
  apply lintegral_congr
  intro b
  by_cases hab : (a, b) ∈ S
  · rw [Set.indicator_of_mem hab,
      Set.indicator_of_mem (show b ∈ Prod.mk a ⁻¹' S from hab)]
    exact Kernel.deterministic_prod_apply' measurable_fst F (a, b) hT
  · rw [Set.indicator_of_notMem hab,
      Set.indicator_of_notMem (show b ∉ Prod.mk a ⁻¹' S from hab)]

/-- Almost-everywhere fiber detailed balance lifts to the transition which
retains the first coordinate. Joint measurability comes from the kernel `F`;
measurable joint sets have measurable fiber sections. All integrals are
nonnegative, so no finite-flux or integrability premise is needed. -/
theorem retained_coordinate_isReversible
    {A B : Type*} [MeasurableSpace A] [MeasurableSpace B]
    (μ : Measure A) [SFinite μ]
    (R : Kernel A B) [IsSFiniteKernel R]
    (F : Kernel (A × B) B) [IsSFiniteKernel F]
    (hF : ∀ᵐ a ∂μ, (F.comap (fun b => (a, b))
      (measurable_const.prodMk measurable_id)).IsReversible (R a)) :
    ((Kernel.deterministic Prod.fst measurable_fst) ×ₖ F).IsReversible (μ ⊗ₘ R) := by
  intro S T hS hT
  rw [retained_flux μ R F hS hT, retained_flux μ R F hT hS]
  apply lintegral_congr_ae
  filter_upwards [hF] with a ha
  exact ha (hS.preimage measurable_prodMk_left) (hT.preimage measurable_prodMk_left)

end AutoSamplingTheory.TechnicalLemmas.Probability.KernelRetainedReversibility
