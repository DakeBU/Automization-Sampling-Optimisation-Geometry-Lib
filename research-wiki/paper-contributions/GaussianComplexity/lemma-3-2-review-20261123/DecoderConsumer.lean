import GC32Decoder

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

namespace DecoderConsumer

/-- Two size-three blocks and one identity coordinate. -/
theorem two_blocks_one_tail (W : Fin 2 → O 3) (x : E 7) :
    batchDecode 7 3 4 x (fun s => oracleAnswer W (batchPlan 7 3 x s)) =
      precisionReply (blockPrecision (d := 7) (n := 3) 4 W) x :=
  batchDecode_precisionReply (d := 7) (n := 3) (by decide) (by decide) (by norm_num) W x

example (κ : ℝ) (x : E 7) (a : Fin 4 → Vec 3) :
    (batchDecode 7 3 κ x a).2 (decoderCoordinates 7 3 (Sum.inr 0)) =
      x (decoderCoordinates 7 3 (Sum.inr 0)) := by
  simp [batchDecode, decodedGradient]

example (x : E 7) :
    (batchPlan 7 3 x (Fin.natAdd 2 (1 : Fin 2))).2.2 = true := rfl

/-- The same equality includes the no-tail case. -/
example (W : Fin 1 → O 3) (x : E 3) :
    batchDecode 3 3 4 x (fun s => oracleAnswer W (batchPlan 3 3 x s)) =
      actualReply (d := 3) (n := 3) 4 W x :=
  batchDecode_oracleAnswer (d := 3) (n := 3) (by decide) (by decide) (by norm_num) W x

example (j : Fin 2) :
    (List.ofFn (batchLabel 2)).countP (fun v => decide (v = j)) = 2 :=
  count_batchLabel 2 j

#print axioms two_blocks_one_tail
end DecoderConsumer
