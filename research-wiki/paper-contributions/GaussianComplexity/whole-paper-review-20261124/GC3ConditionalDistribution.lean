import GC3AdaptiveFactorization
import Mathlib.MeasureTheory.Constructions.Polish.Basic

/-! The explicit posterior is a version of the regular conditional distribution in Mathlib. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Topology TopologicalSpace Set
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior

private instance orthogonal_polish (N : ℕ) : PolishSpace (O N) := by
  let := metrizableSpaceMetric (O N)
  infer_instance

private theorem sigma_borel {I : Type*} [Countable I] {α : I → Type*}
    [∀ i, TopologicalSpace (α i)] [∀ i, MeasurableSpace (α i)] [∀ i, BorelSpace (α i)] :
    BorelSpace (Σ i, α i) := by
  refine ⟨le_antisymm ?_ ?_⟩
  · intro s hs
    have hf (i : I) : MeasurableSet (Sigma.mk i ⁻¹' s) := MeasurableSpace.measurableSet_iInf.mp hs i
    let : MeasurableSpace (Σ i, α i) := borel _
    let : BorelSpace (Σ i, α i) := ⟨rfl⟩
    have hu : s = ⋃ i, Sigma.mk i '' (Sigma.mk i ⁻¹' s) := by
      ext x
      rcases x with ⟨i,x⟩
      constructor
      · intro hx; exact mem_iUnion.mpr ⟨i,x,hx,rfl⟩
      · intro hx
        obtain ⟨j,y,hy,he⟩ := mem_iUnion.mp hx
        exact he ▸ hy
    rw [hu]
    exact MeasurableSet.iUnion (fun i =>
      (IsClosedEmbedding.sigmaMk (i := i)).measurableEmbedding.measurableSet_image.mpr (hf i))
  · apply MeasurableSpace.generateFrom_le
    intro s hs
    exact MeasurableSpace.measurableSet_iInf.mpr (fun _ => (hs.preimage continuous_sigmaMk).measurableSet)

instance standardBorel_taggedTuple (k : ℕ) : StandardBorelSpace (TaggedTuple k) := by
  let : BorelSpace (TaggedTuple k) := sigma_borel
  infer_instance

theorem conditional_distribution_of_raw_residual {N k T : ℕ} (hN : 2*T < N)
    (select : Trace k N → Option (Query k N)) (hs : Measurable select)
    (t : ℕ) (b : ℝ) (hb : b = -1 ∨ b = 1)
    (cap : ∀ᵐ A ∂(Measure.pi fun _ : Fin k => componentHaar N b),
      ∀ j, blockCount j (rawRun select t [] A) ≤ 2*T) :
    let μ := Measure.pi fun _ : Fin k => componentHaar N b
    let h := rawRun select t []
    let _ := isProbabilityMeasure_componentHaar (by omega : 0 < N) hb
    let _ : IsProbabilityMeasure μ := by dsimp [μ]; infer_instance
    condDistrib (fun A => historyResidual (h A) A) h μ =ᵐ[μ.map h] posterior k N b := by
  let μ := Measure.pi fun _ : Fin k => componentHaar N b
  let h := rawRun select t []
  let := isProbabilityMeasure_componentHaar (by omega : 0 < N) hb
  let _ : IsProbabilityMeasure μ := by dsimp [μ]; infer_instance
  let _ := markov_residualKernel (N := N) (k := k) hb
  let _ : IsMarkovKernel (posterior k N b) := inferInstanceAs
    (IsMarkovKernel ((residualKernel b).comap PublicFrame.foldFrames PublicFrame.measurable_foldFrames))
  have hp := adaptive_posterior_factorization hN select hs t b hb cap
  have hm : Measurable h := measurable_rawRun_fixed select hs t []
  exact condDistrib_ae_eq_of_measure_eq_compProd_of_measurable hm
    (hp.measurable_residual.comp (hm.prodMk measurable_id)) hp.joint

#print axioms conditional_distribution_of_raw_residual
end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
