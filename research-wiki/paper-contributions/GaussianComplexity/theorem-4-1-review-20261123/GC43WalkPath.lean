import GC43Regular

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

variable {N : ℕ} {State : Type*} [MeasurableSpace State]

structure WalkPath (P : Program N State) (clock : ℕ) (A : O N) (s : State) (D : O N) (r : ℕ)
    {fuel : ℕ} (R : Fin fuel → Report N State) : Prop where
  first (i : Fin fuel) (hi : i.val = 0) :
    (R i).priorState = s ∧ (R i).priorDomain = D ∧ (R i).priorRank = r
  adjacent (i j : Fin fuel) (hij : j.val = i.val+1) :
    (R j).priorState = P.update (clock+i.val) (R i).priorState (R i).answer ∧
    (R j).priorDomain = (R i).nextDomain ∧ (R j).priorRank = (R i).nextRank
  answer (i : Fin fuel) :
    (R i).answer = if P.back (clock+i.val) then act A⁻¹ (P.vector (clock+i.val) (R i).priorState)
      else act A (P.vector (clock+i.val) (R i).priorState)
  start_mem (i : Fin fuel) (hb : P.back (clock+i.val) = true) :
    (R i).answer ∈ exposedSpace (R i).priorDomain (R i).priorRank ⊔ ℝ ∙ (R i).start.ofLp
  growth (i : Fin fuel) :
    exposedSpace (R i).nextDomain (R i).nextRank ≤
      exposedSpace (R i).priorDomain (R i).priorRank ⊔
        ℝ ∙ (if P.back (clock+i.val) then (R i).answer else P.vector (clock+i.val) (R i).priorState)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
