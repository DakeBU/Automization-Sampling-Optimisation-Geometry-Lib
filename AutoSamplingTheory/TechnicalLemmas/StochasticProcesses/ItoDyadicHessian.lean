import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactStateRepresentative
import AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanRowRegularity
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicWeightedCovariation
import Mathlib.Analysis.Calculus.ContDiff.Comp

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicHessian

open Filter MeasureTheory Set
open scoped BigOperators NNReal Topology
open BrownianMotion ProgressiveL2 ElementaryItoIntegral SampledElementaryApproximation
  DyadicElementaryRefinement EuclideanBrownianCoordinates ItoIntegralProcess
  ItoDyadicWeightedCovariation FiniteSumConvergenceInMeasure ItoEuclideanRowRegularity
open AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates

open CompactStateRepresentative

set_option maxHeartbeats 500000 in
/-- The actual quadratic Taylor terms of the completed vector Itô process
converge to the Hessian contraction against its diffusion columns. -/
theorem tendstoInMeasure_dyadic_half_hessian_increments
    {Ω I J : Type*} [MeasurableSpace Ω] [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J]
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
    let H := fderiv ℝ (fderiv ℝ f)
    let σ := fun (j : J) (t : ℝ≥0) (ω : Ω) =>
      WithLp.toLp 2 (fun i : I => (η i j).process t ω)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, X t ω ∈ K) →
    TendstoInMeasure μ (fun n ω =>
      let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
      ∑ i : Fin (2 ^ n),
        let Δ := X (t i.succ) ω - X (t i.castSucc) ω
        (1 / 2 : ℝ) * H (X (t i.castSucc) ω) Δ Δ) atTop
      (fun ω => ∫ s, (1 / 2 : ℝ) * (∑ j : J, H (X s ω) (σ j s ω) (σ j s ω))
        ∂(TimeMeasure.upTo T)) := by
  intro X H σ hRange
  let t (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  let e := EuclideanSpace.basisFun I ℝ
  let W (q : I × I) (s : ℝ≥0) (ω : Ω) := (1 / 2 : ℝ) * H (X s ω) (e q.1) (e q.2)
  let Δ (n : ℕ) (i : Fin (2 ^ n)) (ω : Ω) := X (t n i.succ) ω - X (t n i.castSucc) ω
  let b (q : I × I) (s : ℝ≥0) (ω : Ω) :=
    ∑ j : J, (η q.1 j).process s ω * (η q.2 j).process s ω
  let F (q : I × I) (n : ℕ) (ω : Ω) :=
    ∑ i : Fin (2 ^ n), W q (t n i.castSucc) ω * (Δ n i ω q.1 * Δ n i ω q.2)
  let G (q : I × I) (ω : Ω) := ∫ s, W q s ω * b q s ω ∂(TimeMeasure.upTo T)
  have hH : ContinuousOn H K := fun x hx =>
    (((hf x hx).fderiv_right (m := 1) (by decide)).continuousAt_fderiv
      (by decide)).continuousWithinAt
  have hEntry (q : I × I) :
      ContinuousOn (fun x => (1 / 2 : ℝ) * H x (e q.1) (e q.2)) K :=
    continuousOn_const.mul ((hH.clm_apply continuousOn_const).clm_apply continuousOn_const)
  obtain ⟨hXm, hXc⟩ := measurable_continuousOn_euclidean_ito_rows
    hB hT hUsual η A hAmeas (fun i => (hA i).mono fun _ h => h.1)
  have hWm (q : I × I) (s : ℝ≥0) (hs : s ≤ T) : AEStronglyMeasurable (W q s) μ := by
    have hY := (measurable_restrictState hK.isClosed.measurableSet fallback).comp (hXm s hs)
    refine ((hEntry q).domRestrict.measurable.comp hY).aestronglyMeasurable.congr ?_
    filter_upwards [hRange] with ω hr
    change (1 / 2 : ℝ) * H (restrictState fallback (X s ω) : EuclideanSpace ℝ I)
      (e q.1) (e q.2) = W q s ω
    rw [coe_restrictState_of_mem fallback (hr s hs)]
  have hWc : ∀ᵐ ω ∂μ, ∀ q : I × I, ContinuousOn (fun s => W q s ω) (Icc 0 T) := by
    filter_upwards [hXc, hRange] with ω hω hr q
    exact (hEntry q).comp hω (fun s hs => hr s hs.2)
  have hLim (q : I × I) : TendstoInMeasure μ (F q) atTop (G q) :=
    tendstoInMeasure_dyadic_weighted_covariation_of_ito_rows hB hT hUsual
      (η q.1) (η q.2) (A q.1) (A q.2) (W q) (hAmeas q.1) (hAmeas q.2)
      (hWm q) (hA q.1) (hA q.2) (hWc.mono fun _ h => h q)
  have ht (n : ℕ) (i : Fin (2 ^ n + 1)) : t n i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT n) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T n)
  have hFm (q : I × I) (n : ℕ) : AEStronglyMeasurable (F q n) μ := by
    have hΔm (i : Fin (2 ^ n)) (j : I) : AEStronglyMeasurable (fun ω => Δ n i ω j) μ :=
      ((EuclideanSpace.proj j).continuous.measurable.comp
        ((hXm _ (ht n i.succ)).sub (hXm _ (ht n i.castSucc)))).aestronglyMeasurable
    have hCell (i : Fin (2 ^ n)) :
        AEStronglyMeasurable (fun ω => W q (t n i.castSucc) ω *
          (Δ n i ω q.1 * Δ n i ω q.2)) μ :=
      (hWm q _ (ht n i.castSucc)).mul ((hΔm i q.1).mul (hΔm i q.2))
    exact (Finset.aestronglyMeasurable_sum Finset.univ fun i _ => hCell i).congr
      (Eventually.of_forall fun ω => by simp only [F, Finset.sum_apply])
  have hHalf (x v : EuclideanSpace ℝ I) :
      (1 / 2 : ℝ) * H x v v = ∑ q : I × I,
        ((1 / 2 : ℝ) * H x (e q.1) (e q.2)) * (v q.1 * v q.2) := by
    rw [euclidean_bilinear_eq_sum_basis (H x) v v, Finset.mul_sum, Fintype.sum_prod_type]
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    ring
  have hSum := tendstoInMeasure_fintype_sum hFm hLim
  refine TendstoInMeasure.congr ?_ ?_ hSum
  · intro n
    exact Eventually.of_forall fun ω => by
      change (∑ q : I × I, ∑ i : Fin (2 ^ n),
        W q (t n i.castSucc) ω * (Δ n i ω q.1 * Δ n i ω q.2)) =
        ∑ i : Fin (2 ^ n), (1 / 2 : ℝ) * H (X (t n i.castSucc) ω) (Δ n i ω) (Δ n i ω)
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro i _
      exact (hHalf _ _).symm
  · have hProduct : ∀ᵐ ω ∂μ, ∀ q : I × I, ∀ j : J,
        Integrable (fun s => (η q.1 j).process s ω * (η q.2 j).process s ω)
          (TimeMeasure.upTo T) :=
      ae_all_iff.2 fun q => ae_all_iff.2 fun j =>
        ((η q.1 j).memLp.integrable_mul (η q.2 j).memLp).prod_right_ae
    filter_upwards [hProduct, hWc] with ω hp hw
    let ν := TimeMeasure.upTo T
    have hMem : ∀ᵐ s ∂ν, s ∈ Icc (0 : ℝ≥0) T :=
      (TimeMeasure.ae_mem_Ioc_zero_upTo T).mono fun _ hs => ⟨hs.1.le, hs.2⟩
    have hRest : ν.restrict (Icc 0 T) = ν := Measure.restrict_eq_self_of_ae_mem hMem
    have hInt (q : I × I) : Integrable (fun s => W q s ω * b q s ω) ν := by
      have hDensity : Integrable (fun s => b q s ω) ν := integrable_finsetSum _ (fun j _ => hp q j)
      obtain ⟨C, hC⟩ := isCompact_Icc.bddAbove_image (hw q).norm
      have hMeas : AEStronglyMeasurable (fun s => W q s ω) ν := by
        rw [← hRest]
        exact (hw q).aestronglyMeasurable measurableSet_Icc
      exact hDensity.bdd_mul hMeas (hMem.mono fun s hs => hC ⟨s, hs, rfl⟩)
    change (∑ q : I × I, ∫ s, W q s ω * b q s ω ∂ν) =
      ∫ s, (1 / 2 : ℝ) * (∑ j : J, H (X s ω) (σ j s ω) (σ j s ω)) ∂ν
    rw [← integral_finsetSum _ (fun q _ => hInt q)]
    apply integral_congr_ae
    exact Eventually.of_forall fun s => by
      simp only [b, Finset.mul_sum]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro j _
      exact (hHalf _ (σ j s ω)).symm

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicHessian
