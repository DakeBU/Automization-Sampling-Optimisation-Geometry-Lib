import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoContinuousRowQV
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.RandomStoppingProcessConsistency

/-! # Dyadic quadratic variation at one common bounded stopping time -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoStoppedRowQV

open Filter MeasureTheory Set
open scoped NNReal BigOperators
open BrownianMotion ProgressiveL2 StoppingTime EuclideanBrownianCoordinates
  ItoIntegralProcess SampledElementaryApproximation DyadicElementaryRefinement
  ProgressiveL2Stopping RandomStoppingProcessConsistency ItoContinuousRowQV

/-- Evaluate the actual Itô row at the common stopped time. Its dyadic
quadratic variation converges in `L¹` to the original energy up to the stop. -/
theorem tendsto_dyadic_stopped_ito_row_quadraticVariation_L1
    {Omega J : Type*} [MeasurableSpace Omega] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Omega)}
    {mu : Measure Omega} [IsFiniteMeasure mu] {T : ℝ≥0}
    {B : ℝ≥0 → Omega → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration mu) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration mu)
    (eta : J → ProgressiveL2Integrand filtration mu T)
    (tau : Omega → ℝ≥0)
    (htau : IsChewiStoppingTime filtration (fun omega => (tau omega : WithTop ℝ≥0)))
    (htauT : ∀ omega, tau omega ≤ T) :
    let hcoord := (coordinateFamily hB).isBrownian
    let row := fun t omega =>
      ∑ j : J, itoIntegralProcess (eta j) hT (hcoord j) hUsual (min (tau omega) t) omega
    let error := fun level omega =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      (∑ i : Fin (2 ^ level), (row (times i.succ) omega -
        row (times i.castSucc) omega)^2) -
      ∑ j : J, ∫ t in Set.Iic (tau omega), (eta j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
    (∀ level, Integrable (error level) mu) ∧
      Tendsto (fun level => ∫ omega, |error level omega| ∂mu) atTop (nhds 0) := by
  intro hcoord row error
  let times (level : ℕ) := regularGridTimes (dyadicMesh T level) (2 ^ level)
  let stoppedEta (j : J) := stop (eta j) (fun omega => (tau omega : WithTop ℝ≥0)) htau
  let stoppedRow (t : ℝ≥0) (omega : Omega) :=
    ∑ j : J, itoIntegralProcess (stoppedEta j) hT (hcoord j) hUsual t omega
  let stoppedError (level : ℕ) (omega : Omega) :=
    (∑ i : Fin (2 ^ level), (stoppedRow (times level i.succ) omega -
      stoppedRow (times level i.castSucc) omega)^2) -
    ∑ j : J, ∫ t, (stoppedEta j).process t omega ^ 2 ∂(TimeMeasure.upTo T)
  have htime (level : ℕ) (k : Fin (2 ^ level + 1)) : times level k ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT level) _).monotone
      (Fin.le_last k)).trans_eq (regularDyadic_last_time T level)
  have hAt (level : ℕ) (k : Fin (2 ^ level + 1)) (j : J) :
      ∀ᵐ omega ∂mu,
        itoIntegralProcess (stoppedEta j) hT (hcoord j) hUsual (times level k) omega =
          itoIntegralProcess (eta j) hT (hcoord j) hUsual (min (tau omega) (times level k)) omega :=
    itoIntegralProcess_stop_ae (eta j) hT tau htau htauT (hcoord j) hUsual (htime level k)
  have hEnergy (j : J) (omega : Omega) :
      (∫ t, (stoppedEta j).process t omega ^ 2 ∂(TimeMeasure.upTo T)) =
        ∫ t in Set.Iic (tau omega), (eta j).process t omega ^ 2 ∂(TimeMeasure.upTo T) := by
    rw [← integral_indicator measurableSet_Iic]
    apply integral_congr_ae
    filter_upwards [] with t
    change (if (t : WithTop ℝ≥0) ≤ (tau omega : WithTop ℝ≥0)
      then (eta j).process t omega else 0)^2 = _
    by_cases ht : t ≤ tau omega
    · rw [if_pos (WithTop.coe_le_coe.mpr ht),
        Set.indicator_of_mem (show t ∈ Set.Iic (tau omega) from ht)]
    · rw [if_neg (fun h => ht (WithTop.coe_le_coe.mp h)),
        Set.indicator_of_notMem (show t ∉ Set.Iic (tau omega) from ht)]
      norm_num
  have hEq (level : ℕ) : stoppedError level =ᵐ[mu] error level := by
    filter_upwards [ae_all_iff.2 fun k => ae_all_iff.2 (hAt level k)] with omega homega
    have hRow (k : Fin (2 ^ level + 1)) : stoppedRow (times level k) omega =
        row (times level k) omega :=
      Finset.sum_congr rfl (fun j _ => homega k j)
    simp only [stoppedError, error, hEnergy, hRow]
    rfl
  have hLimit : (∀ level, Integrable (stoppedError level) mu) ∧
      Tendsto (fun level => ∫ omega, |stoppedError level omega| ∂mu) atTop (nhds 0) :=
    tendsto_dyadic_ito_row_quadraticVariation_L1 hB hT hUsual stoppedEta
  refine ⟨fun level => (hLimit.1 level).congr (hEq level), ?_⟩
  exact (tendsto_congr' (Eventually.of_forall fun level =>
    integral_congr_ae ((hEq level).mono fun _ h => congrArg abs h))).1 hLimit.2

#print axioms tendsto_dyadic_stopped_ito_row_quadraticVariation_L1

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoStoppedRowQV
