import GC32Indistinguishability
import Mathlib.Probability.Distributions.Uniform

/-!
An independent randomized adaptive consumer of the first-order output theorem.
The seed chooses an initial vector and controls stopping after one or two
interactions. A second query uses the returned value and gradient.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

namespace GC32AdaptiveWitness

abbrev St := Bool × ℕ × E 11

private noncomputable def probe (b : Bool) : E 11 :=
  WithLp.toLp 2 (fun i : Fin 11 =>
    if i = 10 then (if b then 2 else 1) else if i = 0 ∨ i = 6 then 1 else 0)

private def move (s : St) : Unit ⊕ E 11 :=
  if s.2.1 = 0 ∨ (s.2.1 = 1 ∧ s.1 = true) then .inr s.2.2 else .inl ()

private noncomputable def learned (x : E 11) (a : Reply 11) : E 11 := a.2 + a.1 • x

private noncomputable def alg : Algorithm 11 Bool St where
  start b := (b, 0, probe b)
  next := move
  update s x a := (s.1, s.2.1+1, learned x a)
  output s := s.2.2 + probe s.1
  measurable_start := measurable_of_countable _
  measurable_next := by
    have hc : Measurable (fun s : St => s.2.1) := measurable_fst.comp measurable_snd
    have hb : Measurable (fun s : St => s.1) := measurable_fst
    apply Measurable.ite ((hc (measurableSet_singleton 0)).union
      ((hc (measurableSet_singleton 1)).inter (hb (measurableSet_singleton true))))
      (measurable_inr.comp (measurable_snd.comp measurable_snd)) measurable_const
  measurable_update := by
    let P := St × E 11 × Reply 11
    have hs : Measurable (fun p : P => p.1.1) := measurable_fst.comp measurable_fst
    have hc : Measurable (fun p : P => p.1.2.1) := measurable_fst.comp
      (measurable_snd.comp measurable_fst)
    have hx : Measurable (fun p : P => p.2.1) := measurable_fst.comp measurable_snd
    have ha : Measurable (fun p : P => p.2.2) := measurable_snd.comp measurable_snd
    exact hs.prodMk ((hc.add_const 1).prodMk (ha.snd.add (ha.fst.smul hx)))
  measurable_output := (measurable_snd.comp measurable_snd).add
    ((measurable_of_countable probe).comp measurable_fst)

/-- The last coordinate is the identity tail following two size-five blocks. -/
theorem nonzero_tail (b : Bool) : probe b (decoderCoordinates 11 5 (Sum.inr 0)) =
    (if b then 2 else 1 : ℝ) := by
  have hidx : decoderCoordinates 11 5 (Sum.inr 0) = (10 : Fin 11) := by decide
  rw [hidx]
  simp [probe]

/-- After the first true oracle response the false seed stops; the other seed
forms its next point from both the value and the gradient. -/
theorem exact_paths (A : Precision 11) :
    let x₀ := probe false
    let x₁ := probe true
    let y := learned x₁ (precisionReply A x₁)
    alg.sample 2 A false = learned x₀ (precisionReply A x₀) + x₀ ∧
      alg.sample 2 A true = learned y (precisionReply A y) + x₁ := by
  constructor <;> rfl

private noncomputable def fair : Measure Bool := (PMF.uniformOfFintype Bool).toMeasure
private instance : IsProbabilityMeasure fair := inferInstanceAs
  (IsProbabilityMeasure (PMF.uniformOfFintype Bool).toMeasure)

/-- At d = 11 and n = 5, the fair-seed algorithm has the same output law
averaged over either precision prior, after at most two first-order queries. -/
theorem mean_output :
    (hardPrior 11 5 4 1).bind (alg.outputLaw fair 2) =
      (hardPrior 11 5 4 (-1)).bind (alg.outputLaw fair 2) :=
  averaged_first_order_indistinguishability (by decide) (by decide) (by norm_num)
    (by decide) fair alg

#print axioms mean_output
#print axioms exact_paths

end GC32AdaptiveWitness
