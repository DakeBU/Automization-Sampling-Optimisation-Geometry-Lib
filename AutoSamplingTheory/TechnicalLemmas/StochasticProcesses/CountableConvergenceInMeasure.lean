import Mathlib.MeasureTheory.Function.ConvergenceInMeasure
import Mathlib.MeasureTheory.OuterMeasure.BorelCantelli

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure

open Filter MeasureTheory Set
open scoped ENNReal Topology

/-- A countable family of limits in measure has a common almost-everywhere subsequence. -/
theorem exists_seq_tendsto_ae_of_countable
    {I Ω E : Type*} [Countable I] [MeasurableSpace Ω] [PseudoEMetricSpace E]
    {μ : Measure Ω} {F : I → ℕ → Ω → E} {G : I → Ω → E}
    (h : ∀ i, TendstoInMeasure μ (F i) atTop (G i)) :
    ∃ k : ℕ → ℕ, StrictMono k ∧ ∀ᵐ ω ∂μ, ∀ i,
      Tendsto (fun n => F i (k n) ω) atTop (𝓝 (G i ω)) := by
  let _ : Encodable I := Encodable.ofCountable I
  let pick (j n : ℕ) := ((Encodable.decode j : Option I).map
    (fun i => ExistsSeqTendstoAe.seqTendstoAeSeq (h i) n)).getD 0
  let bound (n : ℕ) := (Finset.range (n + 1)).sup (fun j => pick j n)
  let k (n : ℕ) := n + bound n
  have hPick (j : ℕ) : Monotone (pick j) := by
    intro m n hmn
    cases hj : (Encodable.decode j : Option I) with
    | none => simp [pick, hj]
    | some i =>
      simpa [pick, hj] using (ExistsSeqTendstoAe.seqTendstoAeSeq_strictMono (h i)).monotone hmn
  have hBound : Monotone bound := by
    intro m n hmn
    apply Finset.sup_le_iff.2
    intro j hj
    exact (hPick j hmn).trans
      (Finset.le_sup (f := fun j => pick j n) (Finset.range_mono (Nat.succ_le_succ hmn) hj))
  have hk : StrictMono k := fun _ _ hmn => Nat.add_lt_add_of_lt_of_le hmn (hBound hmn.le)
  refine ⟨k, hk, ae_all_iff.2 ?_⟩
  intro i
  let S (n : ℕ) : Set Ω := if Encodable.encode i ≤ n then
    {ω | (2 : ℝ≥0∞)⁻¹ ^ n ≤ edist (F i (k n) ω) (G i ω)} else ∅
  have hMeasure (n : ℕ) : μ (S n) ≤ (2 : ℝ≥0∞)⁻¹ ^ n := by
    by_cases hn : Encodable.encode i ≤ n
    · have hp : pick (Encodable.encode i) n ≤ bound n :=
        Finset.le_sup (f := fun j => pick j n) (Finset.mem_range.2 (Nat.lt_succ_of_le hn))
      have hIndex : ExistsSeqTendstoAe.seqTendstoAeSeq (h i) n ≤ k n :=
        (by simpa [pick] using hp : _ ≤ bound n).trans (Nat.le_add_left _ _)
      simpa [S, hn] using ExistsSeqTendstoAe.seqTendstoAeSeq_spec (h i) n (k n) hIndex
    · simp [S, hn]
  have hFinite : (∑' n, μ (S n)) ≠ ∞ := by
    refine ne_top_of_le_ne_top ?_ (ENNReal.tsum_le_tsum hMeasure)
    simpa only [ENNReal.tsum_geometric, ENNReal.one_sub_inv_two, inv_inv] using ENNReal.ofNat_ne_top
  filter_upwards [ae_eventually_notMem hFinite] with ω hω
  refine EMetric.tendsto_atTop.mpr fun ε hε => eventually_atTop.1 ?_
  have hSmall : ∀ᶠ n : ℕ in atTop, (2 : ℝ≥0∞)⁻¹ ^ n < ε :=
    (ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num)).eventually_lt_const hε
  filter_upwards [hω, hSmall, eventually_ge_atTop (Encodable.encode i)] with n hn hs hi
  have hErr : edist (F i (k n) ω) (G i ω) < (2 : ℝ≥0∞)⁻¹ ^ n := by
    simpa [S, hi] using hn
  exact hErr.trans hs

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure
