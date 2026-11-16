import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicBlockWeights
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicWeightedLimits

open Filter MeasureTheory Set
open scoped BigOperators NNReal Topology
open ElementaryItoIntegral SampledElementaryApproximation FiniteTimeGrid
  DyadicElementaryRefinement DyadicBlockWeights ItoWeightedRiemannSums
open AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral

/-- Cumulative limits on dyadic cutoffs and bounded total absolute mass
imply convergence against every continuous left-endpoint weight. -/
theorem tendsto_dyadic_weighted_sums_of_prefix_limits
    {T : ℝ≥0} (hT : 0 < T) (w b : ℝ≥0 → ℝ)
    (hw : ContinuousOn w (Icc 0 T)) (hb : Integrable b (TimeMeasure.upTo T))
    (z : (n : ℕ) → Fin (2 ^ n) → ℝ) (σ : ℕ → ℕ) (hσ : Tendsto σ atTop atTop)
    (hVar : ∃ M : ℝ, ∀ n, ∑ i : Fin (2 ^ σ n), |z (σ n) i| ≤ M) :
    let t := fun n => regularGridTimes (dyadicMesh T n) (2 ^ n)
    (∀ m (k : Fin (2 ^ m + 1)), Tendsto (fun n =>
      ∑ i : Fin (2 ^ σ n), if t (σ n) i.succ ≤ t m k then z (σ n) i else 0)
      atTop (𝓝 (prefixIntegral b T (t m k)))) →
    Tendsto (fun n => ∑ i : Fin (2 ^ σ n), w (t (σ n) i.castSucc) * z (σ n) i)
      atTop (𝓝 (∫ s, w s * b s ∂(TimeMeasure.upTo T))) := by
  intro t hPrefix
  obtain ⟨M, hM⟩ := hVar
  let C := max M 1
  have hC : 0 < C := zero_lt_one.trans_le (le_max_right _ _)
  let P (m : ℕ) (k : Fin (2 ^ m + 1)) (n : ℕ) :=
    ∑ i : Fin (2 ^ σ n), if t (σ n) i.succ ≤ t m k then z (σ n) i else 0
  let L (m : ℕ) := ∑ j : Fin (2 ^ m), w (t m j.castSucc) *
    (prefixIntegral b T (t m j.succ) - prefixIntegral b T (t m j.castSucc))
  let V (m n : ℕ) := ∑ j : Fin (2 ^ m), w (t m j.castSucc) *
    (P m j.succ n - P m j.castSucc n)
  let S (n : ℕ) := ∑ i : Fin (2 ^ σ n), w (t (σ n) i.castSucc) * z (σ n) i
  let I := ∫ s, w s * b s ∂(TimeMeasure.upTo T)
  have hV (m : ℕ) : Tendsto (V m) atTop (𝓝 (L m)) := by
    refine tendsto_finsetSum _ fun j _ => ?_
    exact ((hPrefix m j.succ).sub (hPrefix m j.castSucc)).const_mul _
  have hL : Tendsto L atTop (𝓝 I) :=
    tendsto_dyadic_weighted_prefixIntegral_sums w b T hT hw hb
  have ht (m : ℕ) (i : Fin (2 ^ m + 1)) : t m i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT m) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T m)
  change Tendsto S atTop (𝓝 I)
  rw [Metric.tendsto_nhds]
  intro ε hε
  let δ := ε / (3 * C)
  have hδ : 0 < δ := div_pos hε (by positivity)
  obtain ⟨r, hr, hwmod⟩ :=
    (Metric.uniformContinuousOn_iff.1 (isCompact_Icc.uniformContinuousOn_of_continuous hw)) δ hδ
  have hChoice : ∀ᶠ m : ℕ in atTop,
      (dyadicMesh T m : ℝ) < r ∧ dist (L m) I < ε / 3 :=
    (eventually_dyadicMesh_lt T hr).and ((Metric.tendsto_nhds.1 hL) _ (by positivity))
  obtain ⟨m, hmMesh, hmL⟩ := hChoice.exists
  filter_upwards [hσ.eventually (eventually_ge_atTop m),
    (Metric.tendsto_nhds.1 (hV m)) (ε / 3) (by positivity)] with n hn hmV
  have hBlock : V m n = ∑ i : Fin (2 ^ σ n),
      w (t m (coarseCell hn i).castSucc) * z (σ n) i :=
    (dyadic_sum_coarse_weight_eq_prefix_differences hT hn
      (fun j => w (t m j.castSucc)) (z (σ n))).symm
  have hOsc (i : Fin (2 ^ σ n)) :
      |w (t (σ n) i.castSucc) - w (t m (coarseCell hn i).castSucc)| ≤ δ := by
    let j := coarseCell hn i
    let x := t (σ n) i.castSucc
    let y := t m j.castSucc
    have hyx : y ≤ x := coarse_left_endpoint_le_fine_left (T := T) hn i
    have hfine : t (σ n) i.castSucc ≤ t (σ n) i.succ :=
      (regularGridTimes_strictMono (dyadicMesh_pos hT (σ n)) _).monotone (Fin.castSucc_le_succ i)
    have hxy : x ≤ y + dyadicMesh T m := by
      exact (hfine.trans (fine_right_endpoint_le_coarse_right (T := T) hn i)).trans_eq
        (dyadic_activeCell_right j)
    have hd : dist x y ≤ (dyadicMesh T m : ℝ) := by
      rw [NNReal.dist_eq, abs_of_nonneg (sub_nonneg.mpr (by exact_mod_cast hyx))]
      exact sub_le_iff_le_add.mpr (by exact_mod_cast (add_comm y (dyadicMesh T m) ▸ hxy))
    exact (Real.dist_eq .. ▸
      hwmod x ⟨bot_le, ht _ _⟩ y ⟨bot_le, ht _ _⟩ (hd.trans_lt hmMesh)).le
  have hApprox : dist (S n) (V m n) ≤ ε / 3 := by
    rw [Real.dist_eq, hBlock]
    dsimp only [S]
    rw [← Finset.sum_sub_distrib]
    calc
      _ ≤ ∑ i : Fin (2 ^ σ n), |w (t (σ n) i.castSucc) * z (σ n) i -
          w (t m (coarseCell hn i).castSucc) * z (σ n) i| :=
        Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ i : Fin (2 ^ σ n), δ * |z (σ n) i| := by
        apply Finset.sum_le_sum
        intro i _
        rw [← sub_mul, abs_mul]
        exact mul_le_mul_of_nonneg_right (hOsc i) (abs_nonneg _)
      _ ≤ δ * C := by
        rw [← Finset.mul_sum]
        exact mul_le_mul_of_nonneg_left ((hM n).trans (le_max_left _ _)) hδ.le
      _ = ε / 3 := by
        dsimp only [δ]
        rw [← div_div, div_mul_cancel₀ _ hC.ne']
  have hTriangle := (dist_triangle (S n) (V m n) I).trans
    (add_le_add (le_refl _) (dist_triangle (V m n) (L m) I))
  linarith

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.DyadicWeightedLimits
