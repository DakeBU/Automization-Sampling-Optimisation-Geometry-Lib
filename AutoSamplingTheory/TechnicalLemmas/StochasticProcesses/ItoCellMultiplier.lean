import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.RandomStoppingProcessConsistency
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcessCongruence

/-! # A past event as a multiplier on a deterministic Itô cell -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCellMultiplier

open Filter MeasureTheory Set
open scoped NNReal
open BrownianMotion ProgressiveL2 StoppingTime
  ProgressiveL2Algebra ProgressiveL2Stopping ItoIntegralProcess ItoIntegralProcessCongruence
  RandomStoppingProcessConsistency

attribute [local instance] Classical.propDecidable

/-- The literal integrand restricted to a past event and to a right-closed
time cell integrates to the corresponding event times the completed increment. -/
theorem itoIntegralProcess_event_cell_multiplier
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ}
    (eta : ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    {s t : ℝ≥0} (hst : s ≤ t) (htT : t ≤ T)
    (event : Set Omega) (hEvent : MeasurableSet[filtration s] event) :
    ∃ theta : ProgressiveL2Integrand filtration mu T,
      (∀ (r : ℝ≥0) (omega : Omega),
        theta.process r omega = if omega ∈ event ∧ s < r ∧ r ≤ t then eta.process r omega else 0) ∧
      ∀ u : ℝ≥0, u ≤ T →
        itoIntegralProcess theta hT hB hUsual u =ᵐ[mu]
          fun omega => if omega ∈ event then
            itoIntegralProcess eta hT hB hUsual (min t u) omega -
              itoIntegralProcess eta hT hB hUsual (min s u) omega
            else 0 := by
  classical
  let tau (omega : Omega) := if omega ∈ event then t else s
  have htau : IsChewiStoppingTime filtration (fun omega => (tau omega : WithTop ℝ≥0)) := by
    have hComplement : MeasurableSet[filtration s] eventᶜ :=
      @MeasurableSet.compl Omega event (filtration s) hEvent
    have heq : (fun omega => (tau omega : WithTop ℝ≥0)) =
        eventᶜ.piecewise (fun _ => (s : WithTop ℝ≥0)) (fun _ => (t : WithTop ℝ≥0)) := by
      funext omega
      by_cases he : omega ∈ event <;> simp [tau, Set.piecewise, he] <;> rfl
    rw [heq]
    exact isStoppingTime_piecewise_const hst hComplement
  have htauT (omega : Omega) : tau omega ≤ T := by
    by_cases he : omega ∈ event
    · simpa [tau, he] using htT
    · simpa [tau, he] using hst.trans htT
  let p := stop eta (fun omega => (tau omega : WithTop ℝ≥0)) htau
  let q := stop eta (fun _ => (s : WithTop ℝ≥0)) (isChewiStoppingTime_const filtration s)
  let theta := ProgressiveL2Algebra.sub p q
  refine ⟨theta, ?_, ?_⟩
  · intro r omega
    change ((if (r : WithTop ℝ≥0) ≤ (tau omega : WithTop ℝ≥0) then eta.process r omega else 0) -
      (if (r : WithTop ℝ≥0) ≤ (s : WithTop ℝ≥0) then eta.process r omega else 0)) = _
    by_cases he : omega ∈ event
    · rw [show tau omega = t from if_pos he]
      by_cases hrs : r ≤ s
      · rw [if_pos (WithTop.coe_le_coe.mpr (hrs.trans hst)), if_pos (WithTop.coe_le_coe.mpr hrs),
          if_neg (fun h => (not_lt.mpr hrs) h.2.1), sub_self]
      · have hsr : s < r := lt_of_not_ge hrs
        rw [if_neg (fun h => hrs (WithTop.coe_le_coe.mp h)), sub_zero]
        by_cases hrt : r ≤ t
        · rw [if_pos (WithTop.coe_le_coe.mpr hrt), if_pos ⟨he, hsr, hrt⟩]
        · rw [if_neg (fun h => hrt (WithTop.coe_le_coe.mp h)), if_neg (fun h => hrt h.2.2)]
    · rw [show tau omega = s from if_neg he, sub_self, if_neg (fun h => he h.1)]
  · intro u hu
    have heq : (ProgressiveL2Algebra.add theta q).toLp = p.toLp := by
      rw [ProgressiveL2Algebra.toLp_add]
      dsimp only [theta]
      rw [ProgressiveL2Algebra.toLp_sub, sub_add_cancel]
    filter_upwards [itoIntegralProcess_add theta q hT hB hUsual hu,
      itoIntegralProcess_congr_toLp_ae _ _ hT hB hUsual heq hu,
      itoIntegralProcess_stop_ae eta hT tau htau htauT hB hUsual hu,
      itoIntegralProcess_stop_ae eta hT (fun _ => s) (isChewiStoppingTime_const filtration s)
        (fun _ => hst.trans htT) hB hUsual hu] with omega hadd hcon hp hq
    have h := eq_sub_of_add_eq (hadd.symm.trans hcon)
    change itoIntegralProcess theta hT hB hUsual u omega =
      itoIntegralProcess p hT hB hUsual u omega -
        itoIntegralProcess q hT hB hUsual u omega at h
    change itoIntegralProcess p hT hB hUsual u omega =
      itoIntegralProcess eta hT hB hUsual (min (tau omega) u) omega at hp
    change itoIntegralProcess q hT hB hUsual u omega =
      itoIntegralProcess eta hT hB hUsual (min s u) omega at hq
    rw [hp, hq] at h
    by_cases he : omega ∈ event <;> simpa [tau, he] using h

#print axioms itoIntegralProcess_event_cell_multiplier

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCellMultiplier
