import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicElementaryRefinement
import Mathlib.Topology.EMetricSpace.BoundedVariation

/-! # Continuous finite variation does not change dyadic quadratic variation -/

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteVariationDyadicQV

open Filter Set
open scoped NNReal ENNReal BigOperators
open FiniteTimeGrid SampledElementaryApproximation DyadicElementaryRefinement

/-- The square-increment difference from adding a continuous finite-variation
path tends to zero on the full deterministic dyadic grids. -/
theorem tendsto_dyadic_sq_increments_sub_of_continuous_boundedVariation
    (X A : ℝ≥0 → ℝ) (T : ℝ≥0)
    (hX : ContinuousOn X (Set.Icc 0 T))
    (hA : ContinuousOn A (Set.Icc 0 T))
    (hVar : BoundedVariationOn A (Set.Icc 0 T)) :
    Tendsto (fun level : ℕ =>
      let times := regularGridTimes (dyadicMesh T level) (2 ^ level)
      ∑ i : Fin (2 ^ level),
        (((X (times i.succ) + A (times i.succ)) -
          (X (times i.castSucc) + A (times i.castSucc)))^2 -
          (X (times i.succ) - X (times i.castSucc))^2))
      atTop (nhds 0) := by
  let I := Set.Icc (0 : ℝ≥0) T
  let V := (eVariationOn A I).toReal
  let u (level k : ℕ) := (k : ℝ≥0) * dyadicMesh T level
  let times (level : ℕ) := regularGridTimes (dyadicMesh T level) (2 ^ level)
  have hu (level : ℕ) : Monotone (u level) := by
    intro a b hab
    exact mul_le_mul_of_nonneg_right (Nat.cast_le.mpr hab) (show 0 ≤ dyadicMesh T level from bot_le)
  have hEnd (level : ℕ) : u level (2 ^ level) = T :=
    regularDyadic_last_time T level
  have hMem (level : ℕ) (k : Fin (2 ^ level + 1)) : times level k ∈ I :=
    ⟨bot_le, (hu level (Nat.lt_succ_iff.mp k.isLt)).trans_eq (hEnd level)⟩
  have hCellDist (level : ℕ) (i : Fin (2 ^ level)) :
      dist (times level i.succ) (times level i.castSucc) = (dyadicMesh T level : ℝ) := by
    have hCell : times level i.succ = times level i.castSucc + dyadicMesh T level :=
      dyadic_activeCell_right i
    rw [NNReal.dist_eq, hCell, NNReal.coe_add, add_sub_cancel_left]
    exact abs_of_nonneg (NNReal.coe_nonneg _)
  have hSum (level : ℕ) :
      (∑ i : Fin (2 ^ level), |A (times level i.succ) - A (times level i.castSucc)|) ≤ V := by
    have h := eVariationOn.sum_le_of_monotoneOn_Iic (f := A) (s := I)
      ((hu level).monotoneOn (Iic (2 ^ level)))
      (fun k hk => ⟨bot_le, (hu level hk).trans_eq (hEnd level)⟩)
    have hr := ENNReal.toReal_mono hVar h
    rw [ENNReal.toReal_sum (fun k _ => edist_ne_top _ _)] at hr
    rw [show (∑ i : Fin (2 ^ level), |A (times level i.succ) - A (times level i.castSucc)|) =
        ∑ k ∈ Finset.range (2 ^ level), |A (u level (k + 1)) - A (u level k)| from
          Fin.sum_univ_eq_sum_range (fun k => |A (u level (k + 1)) - A (u level k)|) _]
    simpa only [← Real.dist_eq, edist_dist, ENNReal.toReal_ofReal dist_nonneg, V] using hr
  rw [Metric.tendsto_nhds]
  intro epsilon he
  let c := epsilon / (4 * (V + 1))
  have hv : 0 ≤ V := ENNReal.toReal_nonneg
  have hc : 0 < c := by dsimp [c]; positivity
  obtain ⟨dx, hdx, hx⟩ := Metric.uniformContinuousOn_iff.1
    (isCompact_Icc.uniformContinuousOn_of_continuous hX) c hc
  obtain ⟨da, hda, ha⟩ := Metric.uniformContinuousOn_iff.1
    (isCompact_Icc.uniformContinuousOn_of_continuous hA) c hc
  filter_upwards [eventually_dyadicMesh_lt T hdx, eventually_dyadicMesh_lt T hda]
    with level hmx hma
  change dist (∑ i : Fin (2 ^ level),
    (((X (times level i.succ) + A (times level i.succ)) -
      (X (times level i.castSucc) + A (times level i.castSucc)))^2 -
      (X (times level i.succ) - X (times level i.castSucc))^2)) 0 < epsilon
  let a := fun (i : Fin (2 ^ level)) => A (times level i.succ) - A (times level i.castSucc)
  let x := fun (i : Fin (2 ^ level)) => X (times level i.succ) - X (times level i.castSucc)
  have hFactor (i : Fin (2 ^ level)) :
      ((X (times level i.succ) + A (times level i.succ)) -
        (X (times level i.castSucc) + A (times level i.castSucc)))^2 -
        (X (times level i.succ) - X (times level i.castSucc))^2 =
        a i * (2 * x i + a i) := by dsimp [a, x]; ring
  simp only [Real.dist_eq, sub_zero, hFactor]
  have habs (i : Fin (2 ^ level)) : |2 * x i + a i| ≤ 3 * c := by
    have hx' : |x i| < c := by
      simpa only [x, Real.dist_eq] using hx _ (hMem level i.succ) _ (hMem level i.castSucc)
        ((hCellDist level i).trans_lt hmx)
    have ha' : |a i| < c := by
      simpa only [a, Real.dist_eq] using ha _ (hMem level i.succ) _ (hMem level i.castSucc)
        ((hCellDist level i).trans_lt hma)
    have h := abs_add_le (2 * x i) (a i)
    rw [abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2)] at h
    linarith
  calc
    _ ≤ ∑ i : Fin (2 ^ level), |a i * (2 * x i + a i)| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i : Fin (2 ^ level), |a i| * (3 * c) := by
      simp only [abs_mul]
      exact Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left (habs i) (abs_nonneg _))
    _ ≤ V * (3 * c) := by
      rw [← Finset.sum_mul]
      exact mul_le_mul_of_nonneg_right (hSum level) (by positivity)
    _ < epsilon := by
      dsimp [c]
      rw [← mul_assoc, ← mul_div_assoc]
      apply (div_lt_iff₀ (show 0 < 4 * (V + 1) by positivity)).2
      nlinarith

#print axioms tendsto_dyadic_sq_increments_sub_of_continuous_boundedVariation

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteVariationDyadicQV
