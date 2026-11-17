import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanTaylorRemainder
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicPrefixQV

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoActualTaylorRemainder

open Filter MeasureTheory Set
open scoped BigOperators NNReal
open BrownianMotion ProgressiveL2 ElementaryItoIntegral SampledElementaryApproximation
  DyadicElementaryRefinement EuclideanBrownianCoordinates ItoIntegralProcess ItoDyadicPrefixQV
  ItoEuclideanRowRegularity ItoEuclideanTaylorRemainder
open AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder

open CompactStateRepresentative

/-- The dyadic second-order Taylor residual of the actual completed
Euclidean Itô process vanishes in measure. -/
theorem tendstoInMeasure_dyadic_actual_ito_taylor_remainder
    {Ω I J : Type*} [MeasurableSpace Ω] [Fintype I] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : I → J → ProgressiveL2Integrand filtration μ T) (A : I → ℝ≥0 → Ω → ℝ)
    (hAmeas : ∀ i t, t ≤ T → AEStronglyMeasurable (A i t) μ)
    (hA : ∀ i, ∀ᵐ ω ∂μ, ContinuousOn (fun t => A i t ω) (Icc 0 T) ∧
      BoundedVariationOn (fun t => A i t ω) (Icc 0 T))
    {K : Set (EuclideanSpace ℝ I)} (hK : IsCompact K) (fallback : K) (f : EuclideanSpace ℝ I → ℝ)
    (hf : ∀ x ∈ K, ContDiffAt ℝ 2 f x) :
    let X := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => A i t ω + ∑ j : J,
      itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, X t ω ∈ K) →
    TendstoInMeasure μ (fun n ω =>
      let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n), secondOrderRemainder f (X (t i.castSucc) ω)
        (X (t i.succ) ω - X (t i.castSucc) ω)) atTop (fun _ => 0) := by
  intro X hRange
  let t (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  let Y (s : ℝ≥0) (ω : Ω) : K := restrictState fallback (X (min s T) ω)
  have ht (n : ℕ) (i : Fin (2 ^ n + 1)) : t n i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT n) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T n)
  obtain ⟨hXm, hXc⟩ := measurable_continuousOn_euclidean_ito_rows
    hB hT hUsual η A hAmeas (fun i => (hA i).mono fun _ h => h.1)
  have hY (s : ℝ≥0) : Measurable (Y s) :=
    (measurable_restrictState hK.isClosed.measurableSet fallback).comp
      (hXm _ (min_le_right s T))
  have hYc : ∀ᵐ ω ∂μ, ContinuousOn (fun s => Y s ω) (Icc 0 T) := by
    filter_upwards [hXc, hRange] with ω hω hr
    apply Topology.IsEmbedding.subtypeVal.continuousOn_iff.2
    refine hω.congr fun s hs => ?_
    change (restrictState fallback (X (min s T) ω) : EuclideanSpace ℝ I) = X s ω
    rw [min_eq_left hs.2, coe_restrictState_of_mem fallback (hr s hs.2)]
  let Q (i : I) (ω : Ω) :=
    ∑ j : J, ∫ s in Iic T, (η i j).process s ω ^ 2 ∂(TimeMeasure.upTo T)
  have hQV (j : I) : TendstoInMeasure μ (fun n ω =>
      ∑ i : Fin (2 ^ n), ((Y (t n i.succ) ω : EuclideanSpace ℝ I) j -
        (Y (t n i.castSucc) ω : EuclideanSpace ℝ I) j) ^ 2) atTop (Q j) := by
    have h := tendstoInMeasure_dyadic_prefix_sq_increments_of_ito_row hB hT hUsual
      (η j) (A j) (hAmeas j) (hA j) 0 (Fin.last (2 ^ (0 : ℕ)))
    simp only [regularDyadic_last_time] at h
    apply TendstoInMeasure.congr_left ?_ h
    intro n
    filter_upwards [hRange] with ω hr
    apply Finset.sum_congr rfl
    intro i _
    have hs : regularGridTimes (dyadicMesh T n) (2 ^ n) i.succ ≤ T := ht n i.succ
    simp only [if_pos hs, Y, min_eq_left (ht n i.succ), min_eq_left (ht n i.castSucc),
      coe_restrictState_of_mem fallback (hr _ (ht n i.succ)),
      coe_restrictState_of_mem fallback (hr _ (ht n i.castSucc))]
    rfl
  have h := tendstoInMeasure_dyadic_sum_secondOrderRemainder_of_coordinate_qv
    hK f hf hT Y hY hYc Q hQV
  apply TendstoInMeasure.congr_left ?_ h
  intro n
  filter_upwards [hRange] with ω hr
  apply Finset.sum_congr rfl
  intro i _
  change secondOrderRemainder f (Y (t n i.castSucc) ω : EuclideanSpace ℝ I)
    ((Y (t n i.succ) ω : EuclideanSpace ℝ I) - Y (t n i.castSucc) ω) = _
  dsimp only [Y]
  rw [min_eq_left (ht n i.succ), min_eq_left (ht n i.castSucc),
    coe_restrictState_of_mem fallback (hr _ (ht n i.succ)),
    coe_restrictState_of_mem fallback (hr _ (ht n i.castSucc))]

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoActualTaylorRemainder
