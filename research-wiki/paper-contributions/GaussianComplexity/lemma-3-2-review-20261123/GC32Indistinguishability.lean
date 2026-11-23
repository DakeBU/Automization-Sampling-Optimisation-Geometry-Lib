import GC32Algorithm
import GC32Batch
import SeededTranscript
import AveragedOutput

/-!
# Lemma 3.2 · Averaged first-order output laws

Zhou–Suzuki, *On Complexity of Gaussian Sampling*, Section 3.2, equation (7).
The prior is a measure on the actual precision matrices. Its integrand is
the law of the algorithm's output when the precision is fixed and the entire
independent seed is sampled. The algorithm supplies no primitive-query
policy, decoder, or coupling.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarBatchProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.TechnicalLemmas.Analysis
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

/-- Equation (5) pushes the same-sign product Haar measure onto the block
precision with its remaining identity coordinates. -/
noncomputable def hardPrior (d n : ℕ) (κ b : ℝ) : Measure (Precision d) :=
  (Measure.pi fun _ : Fin (d/n) => componentHaar n b).map (blockPrecision κ)

variable {d n T : ℕ} {κ : ℝ} {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]

set_option backward.isDefEq.respectTransparency false in
set_option maxHeartbeats 1000000 in
/-- Under the two hidden signs, the product experiment with the actual
independent seed gives the same law for the returned Euclidean vector. -/
theorem sampled_output_same_law (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ) (hT : 2*T < n)
    (ρ : Measure Seed) (alg : Algorithm d Seed State) :
    let μ := fun b : ℝ => Measure.pi fun _ : Fin (d/n) => componentHaar n b
    let answer := fun p : Seed × (Fin (d/n) → O n) =>
      alg.sample T (blockPrecision κ p.2) p.1
    (ρ.prod (μ 1)).map answer = (ρ.prod (μ (-1))).map answer := by
  let k := d/n
  let m := k+k
  have hk : 0 < k := Nat.div_pos hnd (by omega)
  have hm : 0 < m := by dsimp [m]; omega
  have hfuel : m*T = 2*T*k := by dsimp [m]; ring
  obtain ⟨choose,read,hchoose,hread,hsim⟩ := compile_batch m hm alg.next alg.update
    (batchPlan d n) (batchDecode d n κ) alg.measurable_next alg.measurable_update
    (measurable_batchPlan d n) (measurable_batchDecode d n κ) (batchLabel k) (batchPlan_label d n)
  let select (s : Seed) := choose (alg.start s)
  let output (p : Seed × Trace k n) := alg.output (read (alg.start p.1) p.2).1
  have hs : Measurable (Function.uncurry select) :=
    hchoose.comp ((alg.measurable_start.comp measurable_fst).prodMk measurable_snd)
  have ho : Measurable output :=
    alg.measurable_output.comp (hread.comp ((alg.measurable_start.comp measurable_fst).prodMk measurable_snd)).fst
  have hpath (p : Seed × (Fin k → O n)) :
      output (p.1, seededTranscript select (2*T*k) p) = alg.sample T (blockPrecision κ p.2) p.1 ∧
      ∀ j, blockCount j (seededTranscript select (2*T*k) p) ≤ 2*T := by
    have h := hsim (alg.start p.1) p.2 T
    dsimp only at h
    have hreply : (fun x => batchDecode d n κ x (fun slot => oracleAnswer p.2 (batchPlan d n x slot))) =
        precisionReply (blockPrecision κ p.2) := funext (batchDecode_precisionReply hn hnd hκ p.2)
    rw [hfuel, hreply] at h
    refine ⟨congrArg (fun z : State × Option Unit => alg.output z.1) h.1, ?_⟩
    intro j
    change blockCount j (rawRun (choose (alg.start p.1)) (2*T*k) [] p.2) ≤ 2*T
    rw [h.2.2 j, count_batchLabel]
    exact Nat.mul_le_mul_left 2 h.2.1
  have cap (b : ℝ) (_ : b = -1 ∨ b = 1) :
      ∀ᵐ p ∂ρ.prod (Measure.pi fun _ : Fin k => componentHaar n b),
        ∀ j, blockCount j (seededTranscript select (2*T*k) p) ≤ 2*T :=
    ae_of_all _ fun p => (hpath p).2
  have he := seeded_readout_indistinguishability hT ρ select hs cap output ho
  dsimp only at he ⊢
  have hy := funext fun p => (hpath p).1
  rw [hy] at he
  exact he

set_option backward.isDefEq.respectTransparency false in
set_option maxHeartbeats 800000 in
/-- Lemma 3.2, equation (7). Every Borel randomized first-order algorithm
with budget T < n/2 has equal prior-averaged output laws under D₊ and D₋. -/
theorem averaged_first_order_indistinguishability
    (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ) (hT : 2*T < n)
    (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State) :
    (hardPrior d n κ 1).bind (alg.outputLaw ρ T) =
      (hardPrior d n κ (-1)).bind (alg.outputLaw ρ T) := by
  let μ (b : ℝ) := Measure.pi fun _ : Fin (d/n) => componentHaar n b
  let answer := fun p : Seed × (Fin (d/n) → O n) => alg.sample T (blockPrecision κ p.2) p.1
  have mean (b : ℝ) (hb : b = -1 ∨ b = 1) :
      (hardPrior d n κ b).bind (alg.outputLaw ρ T) = (ρ.prod (μ b)).map answer := by
    let := isProbabilityMeasure_componentHaar (n := n) (by omega) hb
    exact averaged_output_eq_seeded_pushforward ρ (μ b) (blockPrecision (d := d) (n := n) κ)
      (continuous_blockPrecision d n κ).measurable
      (fun p : Seed × Precision d => alg.sample T p.2 p.1) (alg.measurable_sample T)
  rw [mean 1 (Or.inr rfl), mean (-1) (Or.inl rfl)]
  exact sampled_output_same_law hn hnd hκ hT ρ alg

#print axioms averaged_first_order_indistinguishability

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
