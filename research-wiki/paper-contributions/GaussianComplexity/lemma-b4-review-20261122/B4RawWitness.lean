import B4Transcript
import Mathlib.Tactic.FinCases

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace B4RawWitness

def first : Query 2 3 := (0, ![1, 0, 0], false)
def second (y : Vec 3) : Query 2 3 := (1, y, true)

private def answerOf (r : Record 2 3) : Vec 3 :=
  match r with | none => 0 | some e => e.2

/-- Only actual ambient answers enter the adaptive block and vector choice. -/
def observed (h : Trace 2 3) : Vec 3 :=
  match h[0]? with
  | none => 0
  | some r => answerOf r

noncomputable def choose (h : Trace 2 3) : Option (Query 2 3) :=
  if h.length = 0 then some first
  else if h.length = 1 ∧ 0 < observed h 0 then some (second (observed h))
  else none

theorem positive_path (W : Fin 2 → O 3) (hp : 0 < oracleAnswer W first 0) :
    let y := oracleAnswer W first
    let q := second y
    rawRun choose 4 [] W = [some (first, y), some (q, oracleAnswer W q), none, none] := by
  simp [rawRun, choose, observed, answerOf, hp]

theorem nonpositive_path (W : Fin 2 → O 3) (hp : ¬ 0 < oracleAnswer W first 0) :
    rawRun choose 4 [] W = [some (first, oracleAnswer W first), none, none, none] := by
  simp [rawRun, choose, observed, answerOf, hp]

theorem actual_cap (W : Fin 2 → O 3) (j : Fin 2) :
    blockCount j (rawRun choose 4 [] W) ≤ 2*1 := by
  by_cases hp : 0 < oracleAnswer W first 0
  · rw [positive_path W hp]
    fin_cases j <;> norm_num [blockCount, first, second]
  · rw [nonpositive_path W hp]
    fin_cases j <;> norm_num [blockCount, first, second]

private theorem measurable_observed : Measurable observed := by
  have hc : Measurable answerOf := by
    convert measurable_option_cases (id : Record 2 3 → _) measurable_id (fun _ => (0 : Vec 3))
      measurable_const (fun _ (q : Query 2 3 × Vec 3) => q.2) (measurable_snd.comp measurable_snd) using 1
    funext r
    cases r <;> rfl
  convert measurable_option_cases (fun h : Trace 2 3 => h[0]?) (measurable_trace_read 0)
    (fun _ => (0 : Vec 3)) measurable_const (fun _ r => answerOf r) (hc.comp measurable_snd) using 1
  funext h
  cases he : h[0]? <;> simp only [observed, he]

theorem measurable_choose : Measurable choose := by
  have hl : Measurable (@List.length (Record 2 3)) := measurable_trace_length
  have hy := (measurable_pi_apply (0 : Fin 3)).comp measurable_observed
  have hs : Measurable second :=
    measurable_const.prodMk (measurable_id.prodMk measurable_const)
  apply Measurable.ite (hl (measurableSet_singleton 0)) measurable_const
  exact Measurable.ite ((hl (measurableSet_singleton 1)).inter (measurableSet_lt measurable_const hy))
    (measurable_some.comp (hs.comp measurable_observed)) measurable_const

/-- Compare genuine padded raw oracle transcripts on the two determinant components. -/
theorem signed_full_transcript :
    (Measure.pi fun _ : Fin 2 => componentHaar 3 1).map (rawRun choose 4 []) =
      (Measure.pi fun _ : Fin 2 => componentHaar 3 (-1)).map (rawRun choose 4 []) :=
  padded_transcript_indistinguishability (T := 1) (by decide) choose measurable_choose
    (fun _ _ => ae_of_all _ actual_cap)

#print axioms signed_full_transcript

end B4RawWitness
