import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicBlockWeights

open scoped BigOperators NNReal
open ElementaryItoIntegral SampledElementaryApproximation DyadicElementaryRefinement

private theorem fine_right_le_coarse_point_iff
    {T : ℝ≥0} (hT : 0 < T) {m n : ℕ} (hmn : m ≤ n)
    (k : Fin (2 ^ m + 1)) (i : Fin (2 ^ n)) :
    regularGridTimes (dyadicMesh T n) (2 ^ n) i.succ ≤
      regularGridTimes (dyadicMesh T m) (2 ^ m) k ↔
    (coarseCell hmn i).val < k.val := by
  let j := coarseCell hmn i
  let s := regularGridTimes (dyadicMesh T m) (2 ^ m)
  let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
  have hs := regularGridTimes_strictMono (dyadicMesh_pos hT m) (2 ^ m)
  have ht := regularGridTimes_strictMono (dyadicMesh_pos hT n) (2 ^ n)
  change t i.succ ≤ s k ↔ j.val < k.val
  constructor
  · intro h
    by_contra! hkj
    have hkl : k ≤ j.castSucc := hkj
    have hleft := (hs.monotone hkl).trans (coarse_left_endpoint_le_fine_left (T := T) hmn i)
    exact (not_le.mpr (hleft.trans_lt (ht Fin.castSucc_lt_succ))) h
  · intro hjk
    have hkr : j.succ ≤ k := Nat.succ_le_iff.2 hjk
    exact (fine_right_endpoint_le_coarse_right (T := T) hmn i).trans (hs.monotone hkr)

/-- Group a weighted fine sum into coarse blocks by differencing inclusive prefix sums. -/
theorem dyadic_sum_coarse_weight_eq_prefix_differences
    {T : ℝ≥0} (hT : 0 < T) {m n : ℕ} (hmn : m ≤ n)
    (w : Fin (2 ^ m) → ℝ) (z : Fin (2 ^ n) → ℝ) :
    let s := regularGridTimes (dyadicMesh T m) (2 ^ m)
    let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
    let P := fun k => ∑ i : Fin (2 ^ n), if t i.succ ≤ s k then z i else 0
    (∑ i : Fin (2 ^ n), w (coarseCell hmn i) * z i) =
      ∑ j : Fin (2 ^ m), w j * (P j.succ - P j.castSucc) := by
  intro s t P
  have hcell (i : Fin (2 ^ n)) (j : Fin (2 ^ m)) :
      (if t i.succ ≤ s j.succ then z i else 0) -
        (if t i.succ ≤ s j.castSucc then z i else 0) =
      if coarseCell hmn i = j then z i else 0 := by
    change (if regularGridTimes (dyadicMesh T n) (2 ^ n) i.succ ≤
        regularGridTimes (dyadicMesh T m) (2 ^ m) j.succ then z i else 0) -
      (if regularGridTimes (dyadicMesh T n) (2 ^ n) i.succ ≤
        regularGridTimes (dyadicMesh T m) (2 ^ m) j.castSucc then z i else 0) = _
    simp only [fine_right_le_coarse_point_iff hT hmn, Fin.val_succ, Fin.val_castSucc]
    rcases lt_trichotomy (coarseCell hmn i).val j.val with h | h | h
    · have hne : coarseCell hmn i ≠ j := fun he => h.ne (congrArg Fin.val he)
      simp only [if_pos h, if_pos (h.trans (Nat.lt_succ_self _)), if_neg hne, sub_self]
    · have he : coarseCell hmn i = j := Fin.ext h
      simp [he]
    · have hne : coarseCell hmn i ≠ j := fun he => h.ne (congrArg Fin.val he).symm
      simp only [if_neg (not_lt.mpr (Nat.succ_le_iff.2 h)), if_neg (not_lt.mpr h.le),
        if_neg hne, sub_self]
  calc
    _ = ∑ i : Fin (2 ^ n), ∑ j : Fin (2 ^ m),
        w j * (if coarseCell hmn i = j then z i else 0) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [Finset.sum_eq_single (coarseCell hmn i)]
      · simp
      · intro j _ hj
        simp [Ne.symm hj]
      · simp
    _ = _ := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro j _
      simp only [P, ← Finset.sum_sub_distrib, Finset.mul_sum, hcell]

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicBlockWeights
