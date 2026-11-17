import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess

/-! # Cellwise isometry for the completed Itô process -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralIncrement

open Filter MeasureTheory Set
open scoped NNReal
open BrownianMotion ProgressiveL2 ElementaryItoIntegral ItoIntegralProcess
  ItoTerminalCompletion ElementaryItoL2

/-- A deterministic-cell increment of the completed Itô process has squared
expectation equal to the probability-time energy on that cell. -/
theorem itoIntegralProcess_increment_isometry
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ}
    (eta : ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu)
    {s t : ℝ≥0} (hst : s ≤ t) (htT : t ≤ T) :
    let increment := fun omega =>
      itoIntegralProcess eta hT hB hUsual t omega - itoIntegralProcess eta hT hB hUsual s omega
    MemLp increment 2 mu ∧
      (∫ omega, (increment omega)^2 ∂mu) =
        ∫ z in Prod.snd ⁻¹' Set.Ico s t,
          (processFunction eta.process z)^2 ∂(processTimeMeasure mu T) := by
  intro increment
  let right := eta.restrictAt t
  let left := eta.restrictAt s
  let difference := ProgressiveL2Algebra.sub right left
  let L := itoIntegralTerminal difference hT hB
  have hL : L = itoIntegralTerminal right hT hB - itoIntegralTerminal left hT hB :=
    itoIntegralTerminal_sub right left hT hB
  have hCoe := Lp.coeFn_sub (itoIntegralTerminal right hT hB) (itoIntegralTerminal left hT hB)
  have hInc : increment =ᵐ[mu] fun omega => L omega := by
    rw [hL]
    filter_upwards [itoIntegralProcess_at_eq_terminal eta hT hB hUsual htT,
      itoIntegralProcess_at_eq_terminal eta hT hB hUsual (hst.trans htT),hCoe] with omega hRt hLt hSub
    exact (congrArg₂ (· - ·) hRt hLt).trans hSub.symm
  refine ⟨(memLp_congr_ae hInc).2 (Lp.memLp L), ?_⟩
  let cell : Set (Omega × ℝ≥0) := Prod.snd ⁻¹' Set.Ico s t
  have hRep : processFunction difference.process =
      cell.indicator (processFunction eta.process) := by
    funext z
    change (if z.2 < t then eta.process z.2 z.1 else 0) -
        (if z.2 < s then eta.process z.2 z.1 else 0) = _
    by_cases hs : z.2 < s
    · simp [cell, hs, hs.trans_le hst, not_le.mpr hs]
    · by_cases ht : z.2 < t
      · simp [cell, hs, ht, le_of_not_gt hs, processFunction]
      · simp [cell, hs, ht]
  have hSq : (fun z => (processFunction difference.process z)^2) =
      cell.indicator (fun z => (processFunction eta.process z)^2) := by
    funext z
    rw [hRep]
    by_cases hz : z ∈ cell <;> simp [hz]
  calc
    _ = ∫ omega, (L omega)^2 ∂mu :=
      integral_congr_ae (hInc.mono fun _ h => congrArg (· ^ (2 : ℕ)) h)
    _ = ‖L‖^2 := by
      have h := norm_sq_toLp_eq_integral_sq (Lp.memLp L)
      rw [Lp.toLp_coeFn] at h
      exact h.symm
    _ = ‖integrandToLp difference hB‖^2 := by
      rw [show ‖L‖ = ‖integrandToLp difference hB‖ from itoIntegralTerminal_norm difference hT hB]
    _ = ∫ z, (processFunction difference.process z)^2 ∂(processTimeMeasure mu T) :=
      norm_sq_toLp_eq_integral_sq difference.memLp
    _ = _ := by
      rw [hSq, integral_indicator (measurable_snd measurableSet_Ico)]

#print axioms itoIntegralProcess_increment_isometry

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralIncrement
