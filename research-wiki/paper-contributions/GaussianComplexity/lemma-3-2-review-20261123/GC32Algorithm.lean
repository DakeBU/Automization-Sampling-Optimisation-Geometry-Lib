import GC32Decoder
import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle

/-!
# Budgeted first-order output on a fixed precision matrix

Section 2 of Zhou–Suzuki allows the next query, stopping decision and output
to depend measurably on the seed and the previous oracle answers. The state
can store that entire history. The output is read from the state after at
most T interactions, both on early stopping and at the budget boundary.
-/

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol (measurable_append_singleton)
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)

abbrev Precision (d : ℕ) := Matrix (Fin d) (Fin d) ℝ
scoped instance precisionSpace (d : ℕ) : MeasurableSpace (Precision d) := borel _
scoped instance precisionBorel (d : ℕ) : BorelSpace (Precision d) := ⟨rfl⟩

abbrev Reply (d : ℕ) := ℝ × E d

/-- The left branch stops and the right branch supplies the next point. The
readout also handles algorithms that use the last permissible response. -/
structure Algorithm (d : ℕ) (Seed State : Type*) [MeasurableSpace Seed] [MeasurableSpace State] where
  start : Seed → State
  next : State → Unit ⊕ E d
  update : State → E d → Reply d → State
  output : State → E d
  measurable_start : Measurable start
  measurable_next : Measurable next
  measurable_update : Measurable (fun p : State × E d × Reply d => update p.1 p.2.1 p.2.2)
  measurable_output : Measurable output

variable {d : ℕ} {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]

/-- Realize arbitrary complete-history algorithms with the seed and all
chronological query/response records as their state. -/
def Algorithm.ofHistory
    (next : Seed × List (E d × Reply d) → Unit ⊕ E d)
    (output : Seed × List (E d × Reply d) → E d)
    (hn : Measurable next) (ho : Measurable output) :
    Algorithm d Seed (Seed × List (E d × Reply d)) where
  start s := (s, [])
  next := next
  update s x a := (s.1, s.2 ++ [(x,a)])
  output := output
  measurable_start := measurable_id.prodMk measurable_const
  measurable_next := hn
  measurable_update := (measurable_fst.comp measurable_fst).prodMk
    (measurable_append_singleton (measurable_snd.comp measurable_fst) measurable_snd)
  measurable_output := ho

namespace Algorithm

variable (alg : Algorithm d Seed State)

/-- Sample returned on the actual fixed precision A with the indicated seed. -/
noncomputable def sample (T : ℕ) (A : Precision d) (s : Seed) : E d :=
  alg.output (run alg.next alg.update (precisionReply A) T (alg.start s)).1.1

/-- The fixed-input law includes all of the algorithm's internal randomness. -/
noncomputable def outputLaw (ρ : Measure Seed) (T : ℕ) (A : Precision d) : Measure (E d) :=
  ρ.map (alg.sample T A)

/-- A budgeted execution with a jointly measurable family of oracles has a
jointly measurable final state in its oracle parameter and starting state. -/
theorem measurable_run_state {P : Type*} [MeasurableSpace P]
    (oracle : P → E d → Reply d) (hm : Measurable (Function.uncurry oracle)) (T : ℕ) :
    Measurable (fun z : P × State => (run alg.next alg.update (oracle z.1) T z.2).1.1) := by
  induction T with
  | zero =>
    convert (measurable_snd : Measurable (Prod.snd : P × State → State)) using 1
    funext z
    cases h : alg.next z.2 <;> simp [run, h]
  | succ T ih =>
    let Z := P × State
    have hd : Measurable (fun z : Z =>
        (MeasurableEquiv.prodSumDistrib Z Unit (E d)) (z, alg.next z.2)) :=
      (MeasurableEquiv.prodSumDistrib Z Unit (E d)).measurable.comp
        (measurable_id.prodMk (alg.measurable_next.comp measurable_snd))
    have hp : Measurable (fun z : Z × E d => oracle z.1.1 z.2) :=
      hm.comp ((measurable_fst.comp measurable_fst).prodMk measurable_snd)
    have hs : Measurable (fun z : Z × E d => alg.update z.1.2 z.2 (oracle z.1.1 z.2)) :=
      alg.measurable_update.comp
        ((measurable_snd.comp measurable_fst).prodMk (measurable_snd.prodMk hp))
    have hhalt : Measurable (fun z : Z × Unit => z.1.2) := measurable_snd.comp measurable_fst
    have hmore := ih.comp ((measurable_fst.comp measurable_fst).prodMk hs)
    convert (hhalt.sumElim hmore).comp hd using 1
    funext z
    cases h : alg.next z.2 <;> rw [run, h] <;> simp only [Function.comp_apply, h] <;> rfl

set_option backward.isDefEq.respectTransparency false in
set_option maxHeartbeats 800000 in
theorem measurable_sample (T : ℕ) :
    Measurable (fun p : Seed × Precision d => alg.sample T p.2 p.1) := by
  have hm : Measurable (Function.uncurry (@precisionReply d)) :=
    (continuous_precisionReply d).measurable
  have hi : Measurable (fun p : Seed × Precision d => (p.2, alg.start p.1)) :=
    measurable_snd.prodMk (alg.measurable_start.comp measurable_fst)
  let execState (p : Precision d × State) : State :=
    (run alg.next alg.update (precisionReply p.1) T p.2).1.1
  have hrun : Measurable execState := alg.measurable_run_state (@precisionReply d) hm T
  change Measurable (alg.output ∘ execState ∘ (fun p : Seed × Precision d => (p.2, alg.start p.1)))
  exact alg.measurable_output.comp (hrun.comp hi)

end Algorithm

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
