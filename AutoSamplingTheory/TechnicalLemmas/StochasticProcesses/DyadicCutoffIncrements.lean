import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicCutoffIncrements

open scoped BigOperators NNReal
open ElementaryItoIntegral SampledElementaryApproximation DyadicElementaryRefinement

/-- Stopping both paths at a coarse grid point retains exactly the fine
cells whose right endpoints lie at or before that grid point. -/
theorem dyadic_sum_mul_stopped_increments_eq_prefix
    {T : ℝ≥0} (hT : 0 < T) {m n : ℕ} (hmn : m ≤ n)
    (k : Fin (2 ^ m + 1)) (X Y : ℝ≥0 → ℝ) :
    let τ := regularGridTimes (dyadicMesh T m) (2 ^ m) k
    let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
    (∑ i : Fin (2 ^ n),
      (X (min τ (t i.succ)) - X (min τ (t i.castSucc))) *
        (Y (min τ (t i.succ)) - Y (min τ (t i.castSucc)))) =
    ∑ i : Fin (2 ^ n), if t i.succ ≤ τ then
      (X (t i.succ) - X (t i.castSucc)) * (Y (t i.succ) - Y (t i.castSucc)) else 0 := by
  intro τ t
  apply Finset.sum_congr rfl
  intro i _
  let j := coarseCell hmn i
  have hstep : t i.castSucc < t i.succ :=
    regularGridTimes_strictMono (dyadicMesh_pos hT n) _ (Fin.castSucc_lt_succ)
  by_cases h : j.val < k.val
  · have hj : j.succ ≤ k := Nat.succ_le_iff.2 h
    have hright : t i.succ ≤ τ :=
      (fine_right_endpoint_le_coarse_right (T := T) hmn i).trans
        ((regularGridTimes_strictMono (dyadicMesh_pos hT m) _).monotone hj)
    rw [if_pos hright, min_eq_right hright, min_eq_right (hstep.le.trans hright)]
  · have hj : k ≤ j.castSucc := Nat.le_of_not_gt h
    have hleft : τ ≤ t i.castSucc :=
      ((regularGridTimes_strictMono (dyadicMesh_pos hT m) _).monotone hj).trans
        (coarse_left_endpoint_le_fine_left (T := T) hmn i)
    rw [if_neg (not_le.mpr (hleft.trans_lt hstep)), min_eq_left (hleft.trans hstep.le), min_eq_left hleft]
    simp

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicCutoffIncrements
