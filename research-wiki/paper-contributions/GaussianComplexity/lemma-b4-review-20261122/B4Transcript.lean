import B4FramedTuple
import B4Mixture
import B4Protocol
import HaarOrientedSection

/-!
# Padded transcript indistinguishability

Lemma B.4 of Zhou–Suzuki, arXiv:2610.20492v1. A deterministic Borel rule
chooses the next primitive query from the complete chronological history,
or stops. The transcript records the query and its actual ambient matrix
answer, with a distinguished padding value after stopping.

We compare continuations backwards in their remaining length. At each query
we may expose an auxiliary sphere direction even for a zero residual input.
The oracle still records its true answer in that case. At a fixed sphere
value the same smaller frames work for both determinant signs. The query cap
keeps the residual dimension strictly larger than the remaining budget.
-/

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarOrientedSection
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

private theorem prior_probability {k : ℕ} (d : Fin k → ℕ) (hd : ∀ j, 0 < d j)
    (b : ℝ) (hb : b = -1 ∨ b = 1) :
    IsProbabilityMeasure (Measure.pi fun j => componentHaar (d j) b) := by
  let : ∀ j, IsProbabilityMeasure (componentHaar (d j) b) := fun j =>
    isProbabilityMeasure_componentHaar (hd j) hb
  infer_instance

private theorem budget_after_query {k n : ℕ} (d budget : Fin (k+1) → ℕ)
    (i : Fin (k+1)) (hd : d i = n+2) (room : ∀ j, budget j < d j) :
    ∀ j, spend budget i j < resampleDim d i n j := by
  intro j
  by_cases he : j = i
  · subst j
    have h := room i
    simp only [spend, resampleDim, Function.update_self]
    omega
  · simpa only [spend, resampleDim, Function.update_of_ne he] using room j

/-- From any fixed public history and any common ambient frames, the true
remaining answers have the same law under the two residual Haar products. -/
theorem framed_run_same_law {k N : ℕ}
    (select : Trace (k+1) N → Option (Query (k+1) N)) (hm : Measurable select) (fuel : ℕ)
    (d budget : Fin (k+1) → ℕ) (room : ∀ j, budget j < d j)
    (past : Trace (k+1) N) (F : ∀ j, BlockFrame N (d j)) :
    let read := fun w => run select fuel budget past (ambientTuple F w)
    (Measure.pi fun j => componentHaar (d j) 1).map read =
      (Measure.pi fun j => componentHaar (d j) (-1)).map read := by
  induction fuel generalizing d budget past with
  | zero =>
    let hd := fun j => Nat.zero_lt_of_lt (room j)
    let := prior_probability d hd 1 (Or.inr rfl)
    let := prior_probability d hd (-1) (Or.inl rfl)
    simp only [run, Measure.map_const, measure_univ, one_smul]
  | succ t ih =>
    let μ (b : ℝ) := Measure.pi fun j => componentHaar (d j) b
    have hd (j) := Nat.zero_lt_of_lt (room j)
    let := prior_probability d hd 1 (Or.inr rfl)
    let := prior_probability d hd (-1) (Or.inl rfl)
    cases hq : select past with
    | none => simp only [run, hq, Measure.map_const, measure_univ, one_smul]
    | some q =>
      by_cases hleft : 0 < budget q.1
      swap
      · simp only [run, hq, if_neg hleft, Measure.map_const, measure_univ, one_smul]
      let i := q.1
      let n := d i - 2
      have hi : d i = n+2 := by have := room i; change 0 < budget i at hleft; dsimp [n]; omega
      obtain ⟨Q,hQ,hcols⟩ := exists_measurable_oriented_section n
      let hc := fun z => (hcols z).2
      let hdet := fun z => (hcols z).1
      obtain ⟨u,y,_,next,hnext⟩ := split_ambient_tuple F i n hi q.2.1 q.2.2 Q hc
      let d' := resampleDim d i n
      let ν (b : ℝ) := Measure.pi fun j => componentHaar (d' j) b
      let σ := sphereProbability (n+2)
      have room' := budget_after_query d budget i hi room
      let := prior_probability d' (fun j => Nat.zero_lt_of_lt (room' j)) 1 (Or.inr rfl)
      let := prior_probability d' (fun j => Nat.zero_lt_of_lt (room' j)) (-1) (Or.inl rfl)
      let rebuild := fun p : S (n+2) × (∀ j, O (d' j)) => rebuildHaarTuple d i n hi Q q.2.2 u p.1 p.2
      let read := fun w => run select (t+1) budget past (ambientTuple F w)
      have hr : Measurable read := (measurable_run_fixed select hm _ _ _).comp (measurable_ambientTuple F)
      have hchange (b : ℝ) (hb : b = -1 ∨ b = 1) :
          (μ b).map read = (σ.prod (ν b)).map (read ∘ rebuild) := by
        have h := measurePreserving_rebuildHaarTuple d i n hi b hb Q hQ hc hdet q.2.2 u
        rw [← Measure.map_map hr h.measurable, h.map_eq]
      change (μ 1).map read = (μ (-1)).map read
      rw [hchange 1 (Or.inr rfl), hchange (-1) (Or.inl rfl)]
      apply map_prod_eq_of_fiber_maps σ (ν 1) (ν (-1)) (read ∘ rebuild)
        (hr.comp (measurable_rebuildHaarTuple d i n hi Q hQ q.2.2 u))
      intro z
      let e : Record (k+1) N := some (q, y z)
      let tail := fun V => run select t (spend budget i) (past ++ [e]) (ambientTuple (next z) V)
      have htail : Measurable tail :=
        (measurable_run_fixed select hm _ _ _).comp (measurable_ambientTuple (next z))
      have factor : (fun V => (read ∘ rebuild) (z,V)) = List.cons e ∘ tail := by
        funext V
        obtain ⟨hW,hy⟩ := hnext z V
        let W := ambientTuple F (rebuild (z,V))
        have hans : oracleAnswer W q = y z := by
          change (if q.2.2 then act (W q.1)⁻¹ q.2.1 else act (W q.1) q.2.1) = y z at hy
          cases h : q.2.2 <;> simpa only [oracleAnswer, h, Bool.false_eq_true, if_false, if_true] using hy
        change run select (t+1) budget past W = e :: tail V
        simp only [run, hq, if_pos hleft, hans]
        change e :: run select t (spend budget i) (past ++ [e]) W = e :: tail V
        exact congrArg (fun A => e :: run select t (spend budget i) (past ++ [e]) A) hW
      rw [factor, ← Measure.map_map (measurable_cons_record e) htail,
        ← Measure.map_map (measurable_cons_record e) htail]
      exact congrArg (Measure.map (List.cons e)) (ih d' (spend budget i) room' (past ++ [e]) (next z))

/-- Zhou–Suzuki, Lemma B.4. With at most (2T<N) actual primitive queries
per block, the complete transcript padded to (2Tk) slots has identical
laws for the two determinant signs. Each cap is required only almost
everywhere under the corresponding actual experiment. -/
theorem padded_transcript_indistinguishability {N k T : ℕ} (hN : 2*T < N)
    (select : Trace k N → Option (Query k N)) (hm : Measurable select)
    (cap : ∀ b : ℝ, b = -1 ∨ b = 1 →
      ∀ᵐ W ∂(Measure.pi fun _ : Fin k => componentHaar N b),
        ∀ j, blockCount j (rawRun select (2*T*k) [] W) ≤ 2*T) :
    (Measure.pi fun _ : Fin k => componentHaar N 1).map (rawRun select (2*T*k) []) =
      (Measure.pi fun _ : Fin k => componentHaar N (-1)).map (rawRun select (2*T*k) []) := by
  have pos : 0 < N := by omega
  cases k with
  | zero =>
    let := prior_probability (fun _ : Fin 0 => N) (fun _ => pos) 1 (Or.inr rfl)
    let := prior_probability (fun _ : Fin 0 => N) (fun _ => pos) (-1) (Or.inl rfl)
    simp only [Nat.mul_zero, rawRun, Measure.map_const, measure_univ, one_smul]
  | succ k =>
    let fuel := 2*T*(k+1)
    let budget := fun _ : Fin (k+1) => 2*T
    have hc (b : ℝ) (hb : b = -1 ∨ b = 1) :
        (Measure.pi fun _ : Fin (k+1) => componentHaar N b).map (rawRun select fuel []) =
          (Measure.pi fun _ : Fin (k+1) => componentHaar N b).map (run select fuel budget []) := by
      apply Measure.map_congr
      filter_upwards [cap b hb] with W hW
      exact (run_eq_rawRun_of_cap select fuel budget [] W hW).symm
    rw [hc 1 (Or.inr rfl), hc (-1) (Or.inl rfl)]
    have h := framed_run_same_law select hm fuel (fun _ => N) budget (fun _ => hN) []
      (fun _ => BlockFrame.initial N)
    have hF (W : Fin (k+1) → O N) : ambientTuple (fun _ => BlockFrame.initial N) W = W := by
      funext j
      exact BlockFrame.initial_realize _ _
    dsimp only at h
    simpa only [hF] using h

#print axioms padded_transcript_indistinguishability

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
