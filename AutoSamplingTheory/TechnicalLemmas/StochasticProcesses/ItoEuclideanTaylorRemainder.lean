import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder
import Mathlib.Analysis.InnerProductSpace.PiL2

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanTaylorRemainder

open Filter MeasureTheory Set
open scoped BigOperators NNReal Topology
open AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicTaylorRemainder
open ElementaryItoIntegral SampledElementaryApproximation

/-- Coordinate quadratic variation suffices for the Taylor remainder
limit of a Euclidean process. -/
theorem tendstoInMeasure_dyadic_sum_secondOrderRemainder_of_coordinate_qv
    {I Ω : Type*} [Fintype I] [MeasurableSpace Ω] {μ : Measure Ω} [IsFiniteMeasure μ]
    {K : Set (EuclideanSpace ℝ I)} (hK : IsCompact K) (f : EuclideanSpace ℝ I → ℝ)
    (hf : ∀ x ∈ K, ContDiffAt ℝ 2 f x)
    {T : ℝ≥0} (hT : 0 < T) (X : ℝ≥0 → Ω → K) (hX : ∀ t, Measurable (X t))
    (hpaths : ∀ᵐ ω ∂μ, ContinuousOn (fun t => X t ω) (Icc 0 T))
    (Q : I → Ω → ℝ)
    (hQV : ∀ j, TendstoInMeasure μ (fun n ω =>
      let times := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n),
        ((X (times i.succ) ω : EuclideanSpace ℝ I) j -
          (X (times i.castSucc) ω : EuclideanSpace ℝ I) j) ^ 2)
      atTop (Q j)) :
    TendstoInMeasure μ (fun n ω =>
      let times := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n), secondOrderRemainder f (X (times i.castSucc) ω : EuclideanSpace ℝ I)
        ((X (times i.succ) ω : EuclideanSpace ℝ I) - (X (times i.castSucc) ω : EuclideanSpace ℝ I)))
      atTop (fun _ => 0) := by
  let times (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  let coord (j : I) (t : ℝ≥0) (ω : Ω) := (X t ω : EuclideanSpace ℝ I) j
  let V (j : I) (n : ℕ) (ω : Ω) := ∑ i : Fin (2 ^ n),
    (coord j (times n i.succ) ω - coord j (times n i.castSucc) ω) ^ 2
  have hcoord (j : I) (t : ℝ≥0) : Measurable (coord j t) :=
    ((EuclideanSpace.proj j).continuous.comp continuous_subtype_val).measurable.comp (hX t)
  have hV (j : I) (n : ℕ) : AEStronglyMeasurable (V j n) μ := by
    have hcell (i : Fin (2 ^ n)) : AEStronglyMeasurable
        (fun ω => (coord j (times n i.succ) ω - coord j (times n i.castSucc) ω) ^ 2) μ :=
      (((hcoord j _).sub (hcoord j _)).pow_const 2).aestronglyMeasurable
    apply (Finset.aestronglyMeasurable_sum Finset.univ (fun i _ => hcell i)).congr
    exact Eventually.of_forall fun ω => by simp only [V, Finset.sum_apply]
  have h := AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure.tendstoInMeasure_fintype_sum hV (G := Q) hQV
  refine tendstoInMeasure_dyadic_sum_secondOrderRemainder hK f hf hT X hX hpaths
    (Q := fun ω => ∑ j, Q j ω) ?_
  apply h.congr_left
  intro n
  filter_upwards [] with ω
  simp only [V, coord, EuclideanSpace.real_norm_sq_eq, PiLp.sub_apply]
  exact Finset.sum_comm

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanTaylorRemainder
