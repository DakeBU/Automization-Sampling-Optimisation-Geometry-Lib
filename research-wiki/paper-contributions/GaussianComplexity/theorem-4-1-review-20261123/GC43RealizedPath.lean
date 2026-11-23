import GC43ReportSpan
import GC43WalkProof
import GC43WalkStarts

/-! The true bounded algorithm's output on each regular realization of the extended walk. -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

theorem actual_output_mem_walk {d : ℕ} {Seed State : Type*}
    [MeasurableSpace Seed] [MeasurableSpace State] (alg : Algorithm d Seed State)
    (κ : ℝ) (q : ℕ) (hf : 2*q+1 ≤ d) (O : HaarConditional.O d) (s : Seed)
    (noise : Fin (2*q+1) → E d) (hnoise : ∀ i, Regular (noise i)) :
    O.val.transpose *ᵥ WithLp.ofLp (alg.sample q (hiddenPrecision κ O) s) ∈
      krylov d q κ (fun i => startArray (alternatingProgram alg κ q) 0 (2*q+1)
        (BlockFrame.initial d) (alg.start s,0) O noise (evenIndex q i)) := by
  let P := alternatingProgram alg κ q
  let R := walk P 0 (2*q+1) (BlockFrame.initial d) (alg.start s,0) O noise
  have hp : WalkPath P 0 O (alg.start s,0) 1 0 R := by
    simpa only [R,BlockFrame.initial_realize,show (BlockFrame.initial d).domain = 1 from rfl,
      show (BlockFrame.initial d).rank = 0 from rfl] using
      walk_path P 0 (2*q+1) (BlockFrame.initial d) (alg.start s,0) O noise hf hnoise
  exact actual_output_mem_of_walkPath alg κ q O s R hp

#print axioms actual_output_mem_walk

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
