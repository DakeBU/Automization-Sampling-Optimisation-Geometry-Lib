import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure
import Mathlib.MeasureTheory.Function.StronglyMeasurable.Basic

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure

open Filter MeasureTheory
open scoped BigOperators Topology
open CountableConvergenceInMeasure

/-- Finite sums of almost everywhere strongly measurable sequences
preserve convergence in measure on a finite measure space. -/
theorem tendstoInMeasure_fintype_sum
    {I Ω E : Type*} [Fintype I] [MeasurableSpace Ω] [SeminormedAddCommGroup E]
    {μ : Measure Ω} [IsFiniteMeasure μ] {F : I → ℕ → Ω → E} {G : I → Ω → E}
    (hF : ∀ i n, AEStronglyMeasurable (F i n) μ)
    (h : ∀ i, TendstoInMeasure μ (F i) atTop (G i)) :
    TendstoInMeasure μ (fun n ω => ∑ i, F i n ω) atTop (fun ω => ∑ i, G i ω) := by
  have hm (n : ℕ) : AEStronglyMeasurable (fun ω => ∑ i, F i n ω) μ := by
    exact (Finset.aestronglyMeasurable_sum Finset.univ (fun i _ => hF i n)).congr
      (Eventually.of_forall fun ω => by simp only [Finset.sum_apply])
  refine (exists_seq_tendstoInMeasure_atTop_iff hm).2 ?_
  intro n hn
  obtain ⟨k, hk, hPath⟩ := exists_seq_tendsto_ae_of_countable
    (fun i => (h i).comp hn.tendsto_atTop)
  refine ⟨k, hk, ?_⟩
  filter_upwards [hPath] with ω hω
  exact tendsto_finsetSum Finset.univ (fun i _ => hω i)

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure
