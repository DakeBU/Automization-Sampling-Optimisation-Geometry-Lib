import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess

/-! # Completed Itô increments of dyadic elementary integrands -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralElementaryIncrement

open Filter MeasureTheory
open scoped NNReal BigOperators
open BrownianMotion ProgressiveL2 ElementaryItoIntegral ElementaryItoProcess
  ProgressiveL2Density DyadicElementaryRefinement ItoIntegralProcess ItoTerminalCompletion

/-- On an elementary integrand's own grid, its completed Itô increment is the
cell coefficient times the increment of its driving Brownian motion. -/
theorem itoIntegralProcess_elementary_grid_increment_ae
    {Omega : Type*} {m : MeasurableSpace Omega}
    {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} [IsFiniteMeasure mu]
    {T : ℝ≥0} {B : ℝ≥0 → Omega → ℝ}
    (q : DyadicElementaryProcess filtration T) (hT : 0 < T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu) (i : Fin (2 ^ q.level)) :
    let I := itoIntegralProcess (elementaryIntegrand q hB) hT hB hUsual
    (fun omega => I (q.process.times i.succ) omega -
      I (q.process.times i.castSucc) omega) =ᵐ[mu]
      fun omega => q.process.coeff i omega *
        (B (q.process.times i.succ) omega - B (q.process.times i.castSucc) omega) := by
  intro I
  have hlast : q.process.times (Fin.last (2 ^ q.level)) = T := by
    rw [q.times_eq, regularDyadic_last_time]
  have htime (k : Fin (2 ^ q.level + 1)) : q.process.times k ≤ T :=
    (q.process.times_strictMono.monotone (Fin.le_last k)).trans_eq hlast
  have hcomplete (t : ℝ≥0) (htT : t ≤ T) :
      I t =ᵐ[mu] elementaryItoProcess q.process B T t := by
    by_cases ht : t = 0
    · subst t
      dsimp only [I]
      rw [itoIntegralProcess_at_zero, elementaryItoProcess_zero]
    · exact (itoIntegralProcess_at_eq_terminal _ hT hB hUsual htT).trans
        (itoIntegralTerminal_restrictAt_elementary_ae q hT hB (pos_of_ne_zero ht) htT)
  filter_upwards [hcomplete _ (htime i.succ), hcomplete _ (htime i.castSucc)]
    with omega hr hl
  rw [hr, hl]
  simp only [elementaryItoProcess, min_eq_left (htime _), elementaryItoIntegral,
    ← Finset.sum_sub_distrib]
  have hmono := q.process.times_strictMono.monotone
  have hi : q.process.times i.castSucc ≤ q.process.times i.succ :=
    hmono (Fin.castSucc_le_succ (i := i))
  rw [Finset.sum_eq_single i]
  · simp [hi]
  · intro j _ hji
    rcases lt_or_gt_of_ne hji with hj | hj
    · have hjt : q.process.times j.succ ≤ q.process.times i.castSucc :=
        hmono (Fin.le_iff_val_le_val.mpr hj)
      have hjl : q.process.times j.castSucc ≤ q.process.times i.castSucc :=
        (hmono (Fin.castSucc_le_succ (i := j))).trans hjt
      simp [min_eq_left hjt, min_eq_left hjl, min_eq_left (hjt.trans hi),
        min_eq_left (hjl.trans hi)]
    · have hjt : q.process.times i.succ ≤ q.process.times j.castSucc :=
        hmono (Fin.le_iff_val_le_val.mpr hj)
      have hjr : q.process.times i.succ ≤ q.process.times j.succ :=
        hjt.trans (hmono (Fin.castSucc_le_succ (i := j)))
      simp [min_eq_right hjt, min_eq_right hjr, min_eq_right (hi.trans hjt),
        min_eq_right (hi.trans hjr)]
  · simp

#print axioms itoIntegralProcess_elementary_grid_increment_ae

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralElementaryIncrement
