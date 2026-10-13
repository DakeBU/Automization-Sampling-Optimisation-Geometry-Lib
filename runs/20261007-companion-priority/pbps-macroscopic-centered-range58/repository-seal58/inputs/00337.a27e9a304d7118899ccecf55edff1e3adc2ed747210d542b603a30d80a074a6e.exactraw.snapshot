import Mathlib.MeasureTheory.Function.FactorsThrough
import Mathlib.MeasureTheory.Function.ConditionalExpectation.AEMeasurable

/-! The actual real L2 pullback fills exactly the comap-measurable closed subspace.
The reverse inclusion uses a genuine AE representative, measurable factorization,
and pushforward square integrability. No probability or StandardBorel assumption.
Canonical shared background for the PBPS macroscopic range identification. -/

open MeasureTheory
namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange
noncomputable section
set_option autoImplicit false

theorem l2_pullback_range_eq_lpMeas
    {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]
    {μ : Measure X} {ν : Measure Y} {f : X → Y}
    (hf : MeasurePreserving f μ ν) :
    (Lp.compMeasurePreservingₗᵢ ℝ f hf).toLinearMap.range =
      lpMeas ℝ ℝ (MeasurableSpace.comap f (inferInstance : MeasurableSpace Y)) 2 μ := by
  classical
  ext v
  constructor
  · rintro ⟨u, rfl⟩
    apply mem_lpMeas_iff_aestronglyMeasurable.mpr
    have hu : AEStronglyMeasurable (u : Y → ℝ) (μ.map f) := by
      rw [hf.map_eq]
      exact Lp.aestronglyMeasurable u
    exact (hu.comp_ae_measurable' hf.aemeasurable).congr
      (Lp.coeFn_compMeasurePreserving u hf).symm
  · intro hv
    have hm := mem_lpMeas_iff_aestronglyMeasurable.mp hv
    obtain ⟨g, hg, heq⟩ := hm.stronglyMeasurable_mk.exists_eq_measurable_comp
    have hvg : (v : X → ℝ) =ᵐ[μ] g ∘ f :=
      hm.ae_eq_mk.trans (Filter.Eventually.of_forall (fun x => congrFun heq x))
    have hcomp : MemLp (g ∘ f) 2 μ := (Lp.memLp v).ae_eq hvg
    have hgLp : MemLp g 2 ν := by
      rw [← hf.map_eq]
      exact (memLp_map_measure_iff hg.aestronglyMeasurable hf.aemeasurable).mpr hcomp
    have hgAE : (hgLp.toLp g : Y → ℝ) =ᵐ[μ.map f] g := by
      rw [hf.map_eq]
      exact hgLp.coeFn_toLp
    refine ⟨hgLp.toLp g, ?_⟩
    apply Lp.ext
    exact (Lp.coeFn_compMeasurePreserving (hgLp.toLp g) hf).trans
      ((ae_eq_comp hf.aemeasurable hgAE).trans hvg.symm)

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange
