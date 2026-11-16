import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteVariationDyadicQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoStoppedRowQV

/-! # Adding a continuous finite-variation drift to a stopped Itô row -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoFiniteVariationQV

open Filter MeasureTheory Set
open scoped NNReal ENNReal BigOperators
open BrownianMotion ProgressiveL2 StoppingTime ElementaryItoIntegral
  SampledElementaryApproximation DyadicElementaryRefinement EuclideanBrownianCoordinates
  ItoIntegralProcess ItoIntegralProcessAfterHorizon ItoStoppedRowQV
  RandomStoppingProcessConsistency FiniteVariationDyadicQV

/-- A continuous finite-variation drift leaves the stopped Itô row's
quadratic variation unchanged in probability. -/
theorem tendstoInMeasure_dyadic_sq_increments_stopped_ito_add_boundedVariation
    {Omega J : Type*} [MeasurableSpace Omega] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)}
    {mu : Measure Omega} [IsFiniteMeasure mu] {T : ℝ≥0}
    {B : ℝ≥0 → Omega → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration mu)
    (eta : J → ProgressiveL2Integrand filtration mu T)
    (tau : Omega → ℝ≥0)
    (htau : IsChewiStoppingTime filtration (fun omega => (tau omega : WithTop ℝ≥0)))
    (htauT : ∀ omega, tau omega ≤ T)
    (A : ℝ≥0 → Omega → ℝ)
    (hAmeas : ∀ t ≤ T, AEStronglyMeasurable (A t) mu)
    (hA : ∀ᵐ omega ∂mu, ContinuousOn (fun t => A t omega) (Set.Icc 0 T) ∧
      BoundedVariationOn (fun t => A t omega) (Set.Icc 0 T)) :
    let hcoord := (coordinateFamily hB).isBrownian
    let X := fun t omega => A t omega + ∑ j : J,
      itoIntegralProcess (eta j) hT (hcoord j) hUsual (min (tau omega) t) omega
    TendstoInMeasure mu
      (fun level omega =>
        let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
        ∑ i : Fin (2 ^ level), (X (times i.succ) omega - X (times i.castSucc) omega)^2)
      atTop (fun omega => ∑ j : J, ∫ t in Set.Iic (tau omega),
        (eta j).process t omega ^ 2 ∂(TimeMeasure.upTo T)) := by
  intro hcoord X
  let coordinate (j : J) := itoIntegralProcess (eta j) hT (hcoord j) hUsual
  let M (t : ℝ≥0) (omega : Omega) := ∑ j : J, coordinate j (min (tau omega) t) omega
  let times (level : ℕ) := regularGridTimes (dyadicMesh T level) (2 ^ level)
  let Q (f : ℝ≥0 → Omega → ℝ) (level : ℕ) (omega : Omega) :=
    ∑ i : Fin (2 ^ level), (f (times level i.succ) omega - f (times level i.castSucc) omega)^2
  let E (omega : Omega) := ∑ j : J, ∫ t in Set.Iic (tau omega),
    (eta j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
  have hCont (j : J) (omega : Omega) : Continuous (fun t => coordinate j t omega) :=
    itoIntegralProcess_continuous (eta j) hT (hcoord j) hUsual omega
  have hMC (omega : Omega) : Continuous (fun t => M t omega) :=
    continuous_finsetSum _ (fun j _ => (hCont j omega).comp (continuous_const.min continuous_id))
  have hM (t : ℝ≥0) : AEStronglyMeasurable (M t) mu := by
    have hCoordinate (j : J) : AEStronglyMeasurable
        (fun omega => coordinate j (min (tau omega) t) omega) mu := by
      have hs := ((itoIntegralProcess_stronglyAdapted (eta j) hT (hcoord j) hUsual).stoppedProcess
        (hCont j) htau) t
      apply (hs.mono (filtration.le t)).aestronglyMeasurable.congr
      exact Eventually.of_forall fun omega => by
        rw [stoppedProcess_coe_apply, min_comm]
    apply (Finset.aestronglyMeasurable_sum Finset.univ (fun j _ => hCoordinate j)).congr
    filter_upwards [] with omega
    simp only [M, Finset.sum_apply]
  have hTime (level : ℕ) (k : Fin (2 ^ level + 1)) : times level k ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT level) _).monotone
      (Fin.le_last k)).trans_eq (regularDyadic_last_time T level)
  have hQ (f : ℝ≥0 → Omega → ℝ)
      (hf : ∀ t ≤ T, AEStronglyMeasurable (f t) mu) (level : ℕ) :
      AEStronglyMeasurable (Q f level) mu := by
    have hCell (i : Fin (2 ^ level)) : AEStronglyMeasurable
        (fun omega => (f (times level i.succ) omega - f (times level i.castSucc) omega)^2) mu :=
      ((hf _ (hTime level i.succ)).sub (hf _ (hTime level i.castSucc))).pow 2
    apply (Finset.aestronglyMeasurable_sum Finset.univ (fun i _ => hCell i)).congr
    filter_upwards [] with omega
    simp only [Q, Finset.sum_apply]
  have hX (t : ℝ≥0) (ht : t ≤ T) : AEStronglyMeasurable (X t) mu :=
    (hAmeas t ht).add (hM t)
  have hLimit : (∀ level, Integrable (fun omega => Q M level omega - E omega) mu) ∧
      Tendsto (fun level => ∫ omega, |Q M level omega - E omega| ∂mu) atTop (nhds 0) :=
    tendsto_dyadic_stopped_ito_row_quadraticVariation_L1 hB hT hUsual eta tau htau htauT
  have hE : AEStronglyMeasurable E mu := by
    apply ((hQ M (fun t _ => hM t) 0).sub (hLimit.1 0).aestronglyMeasurable).congr
    exact Eventually.of_forall fun omega => sub_sub_cancel _ _
  have hMeasure : TendstoInMeasure mu (Q M) atTop E := by
    apply tendstoInMeasure_of_tendsto_eLpNorm (p := 1) (by norm_num) (hQ M (fun t _ => hM t)) hE
    have hNorm (level : ℕ) : eLpNorm (Q M level - E) 1 mu =
        ENNReal.ofReal (∫ omega, |Q M level omega - E omega| ∂mu) := by
      rw [eLpNorm_one_eq_lintegral_enorm]
      simpa only [Real.norm_eq_abs, Pi.sub_apply] using
        (ofReal_integral_norm_eq_lintegral_enorm (hLimit.1 level)).symm
    simpa only [hNorm, Function.comp_def, ENNReal.ofReal_zero] using
      ENNReal.continuous_ofReal.continuousAt.tendsto.comp hLimit.2
  change TendstoInMeasure mu (Q X) atTop E
  refine (exists_seq_tendstoInMeasure_atTop_iff (hQ X hX)).2 ?_
  intro n hn
  obtain ⟨k, hk, hPath⟩ := (hMeasure.comp hn.tendsto_atTop).exists_seq_tendsto_ae
  refine ⟨k, hk, ?_⟩
  filter_upwards [hA, hPath] with omega ha hPath
  have hDrift := tendsto_dyadic_sq_increments_sub_of_continuous_boundedVariation
    (fun t => M t omega) (fun t => A t omega) T (hMC omega).continuousOn ha.1 ha.2
  have hDiff : Tendsto (fun level => Q X level omega - Q M level omega) atTop (nhds 0) := by
    refine (tendsto_congr' (Eventually.of_forall fun level => ?_)).1 hDrift
    dsimp only [Q, times, X, M, coordinate]
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have hSum := (hDiff.comp (hn.tendsto_atTop.comp hk.tendsto_atTop)).add hPath
  simpa only [Function.comp_def, sub_add_cancel, zero_add] using hSum

#print axioms tendstoInMeasure_dyadic_sq_increments_stopped_ito_add_boundedVariation

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoFiniteVariationQV
