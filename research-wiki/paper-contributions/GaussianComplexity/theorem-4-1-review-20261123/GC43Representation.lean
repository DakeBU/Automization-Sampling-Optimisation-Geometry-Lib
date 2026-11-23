import GC43Extension
import GC43RealizedPath
import GC43WalkLaw

/-! Lemma 4.3 for the returned point of an adaptive first-order algorithm
on the full Haar hidden-eigenbasis family. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

theorem actual_output_representation {d q : ℕ} (κ : ℝ) (hq : 2*q+1 ≤ d)
    {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]
    (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State) :
    HasKrylovRepresentation (q := q) κ (experimentLaw κ q ρ alg) := by
  let n := 2*q+1
  let P := alternatingProgram alg κ q
  let F := BlockFrame.initial d
  let Noise := Fin n → Space d
  let ν : Measure Noise := Measure.pi (fun _ => stdGaussian (Space d))
  let U := orthogonalHaar d
  let : IsProbabilityMeasure U := (orthogonalHaar_spec d).1
  let : IsProbabilityMeasure ν := by dsimp [ν]; infer_instance
  let allG (z : Seed × Orientation d × Noise) : Noise :=
    startArray P 0 n F (alg.start z.1,0) z.2.1 z.2.2
  let g (z : Seed × Orientation d × Noise) : Starts d q := fun i => allG z (evenIndex q i)
  have hstate : Measurable (fun z : Seed × Orientation d × Noise => (alg.start z.1,(0 : Vec d))) :=
    (alg.measurable_start.comp measurable_fst).prodMk measurable_const
  have hAll : Measurable allG :=
    measurable_startArray P 0 n hq (F := fun _ => F) measurable_const measurable_const hstate
      (measurable_fst.comp measurable_snd) (measurable_snd.comp measurable_snd)
  have hg : Measurable g := (even_starts_law d q).measurable.comp hAll
  apply representation_of_fixed_seeds κ ρ alg ν g hg
  · intro s
    exact ((even_starts_law d q).comp (walk_starts_law P 0 n hq F (alg.start s,0))).map_eq
  · intro s
    have hr : ∀ᵐ z ∂U.prod ν, ∀ i, Regular (z.2 i) :=
      (measurePreserving_snd (μ := U) (ν := ν)).quasiMeasurePreserving.ae (regular_start_array d n)
    filter_upwards [hr] with z hz
    exact actual_output_mem_walk alg κ q hq z.1 s z.2 hz

#print axioms actual_output_representation
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
