import GC3AdaptiveFactorization

/-! A raw B.3 consumer. The second query sense depends on the first actual
answer. Its zero input exposes no direction, so two requests leave two of the
three matrix coordinates unexposed in the selected block. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminedHistoryWitness

private def first : Query 1 3 := (0,Pi.single 0 1,false)
private def second (b : Bool) : Query 1 3 := (0,0,b)

private def sense (r : Record 1 3) : Bool :=
  match r with
  | none => false
  | some a => decide (0 < a.2 0)

private def selector (h : Trace 1 3) : Option (Query 1 3) :=
  if h.length = 0 then some first else
    if h.length = 1 then some (second (sense (tupleAt none 1 h 0))) else none

private theorem measurable_sense : Measurable sense := by
  have hb : Measurable (fun a : Query 1 3 × Vec 3 => decide (0 < a.2 0)) := by
    have h : Measurable (fun a : Query 1 3 × Vec 3 => if 0 < a.2 0 then true else false) :=
      Measurable.ite
        (measurableSet_lt measurable_const ((measurable_pi_apply (0 : Fin 3)).comp measurable_snd))
        measurable_const measurable_const
    simpa using h
  convert measurable_option_cases (id : Record 1 3 → _) measurable_id (fun _ => false)
    measurable_const (fun _ (a : Query 1 3 × Vec 3) => decide (0 < a.2 0))
    (hb.comp measurable_snd) using 1
  funext r
  cases r <;> rfl

private theorem measurable_selector : Measurable selector := by
  have hr : Measurable (fun h : Trace 1 3 => tupleAt none 1 h 0) :=
    (measurable_pi_apply 0).comp (measurable_tupleAt none 1)
  have hm : Measurable second := Measurable.of_discrete
  exact Measurable.ite (measurable_trace_length (measurableSet_singleton 0)) measurable_const
    (Measurable.ite (measurable_trace_length (measurableSet_singleton 1))
      (measurable_some.comp (hm.comp (measurable_sense.comp hr))) measurable_const)

private theorem witness_path (A : Ambient 1 3) :
    ∃ b : Bool, rawRun selector 2 [] A =
      [some (first,oracleAnswer A first),some (second b,oracleAnswer A (second b))] := by
  refine ⟨sense (some (first,oracleAnswer A first)),?_⟩
  simp [rawRun,selector,tupleAt]

private theorem recordStep_zero_vector (F : PublicFrame 3) (b : Bool) (y : Vec 3) :
    PublicFrame.recordStep F b 0 y = F := by
  rcases F with ⟨m,F⟩
  cases m with
  | zero => rfl
  | succ m =>
    cases m with
    | zero => rfl
    | succ n =>
      apply PublicFrame.recordStep_zero
      exact (frameComplement_zero_iff F b 0).2 (Submodule.zero_mem _)

/-- The recorded block count is two on every draw. Only the first query
changes rank, independently of its actual reply or the second query's sense. -/
theorem two_requests_one_exposure (A : Ambient 1 3) :
    let h := rawRun selector 2 [] A
    blockCount 0 h = 2 ∧ (PublicFrame.foldFrames h 0).2.rank = 1 ∧
      (PublicFrame.foldFrames h 0).1 = 2 := by
  obtain ⟨b,hb⟩ := witness_path A
  dsimp only
  rw [hb]
  have hfirst : frameComplement (BlockFrame.initial 3) false (Pi.single 0 1) ≠ 0 := by
    rw [ne_eq,frameComplement_zero_iff]
    change Pi.single 0 (1:ℝ) ∉ exposedSpace (1 : O 3) 0
    rw [exposedSpace_initial]
    simp
  let y := oracleAnswer A first
  let r := PublicFrame.recordStep ⟨3,BlockFrame.initial 3⟩ false (Pi.single 0 1) y
  have hf : PublicFrame.foldFrames
      [some (first,oracleAnswer A first),some (second b,oracleAnswer A (second b))] 0 = r := by
    simp [PublicFrame.foldFrames,PublicFrame.updateRecord, PublicFrame.initialFrames, first,second,
      recordStep_zero_vector,r,y]
  rw [hf]
  dsimp only [r]
  rw [PublicFrame.recordStep_informative (n := 1) _ _ _ _ hfirst]
  exact ⟨by simp [blockCount,first,second],rfl,rfl⟩

/-- The full product-Haar posterior, not only the count calculation, applies
at both signs to this actual history-dependent raw policy. -/
theorem posterior_for_witness (b : ℝ) (hb : b = -1 ∨ b = 1) :
    Factorization b (Measure.pi fun _ : Fin 1 => componentHaar 3 b) (rawRun selector 2 []) := by
  apply adaptive_posterior_factorization (T := 1) (by decide) selector measurable_selector 2 b hb
  apply Filter.Eventually.of_forall
  intro W i
  exact (blockCount_le_length i _).trans_eq (length_rawRun selector 2 [] W)

#print axioms two_requests_one_exposure
#print axioms posterior_for_witness
end AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminedHistoryWitness
