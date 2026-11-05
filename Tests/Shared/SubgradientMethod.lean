import AutoSamplingTheory.TechnicalLemmas.Analysis.SubgradientMethod

open AutoSamplingTheory.TechnicalLemmas.Analysis
open SubgradientMethod ConvexSubgradient
open scoped NNReal RealInnerProductSpace

-- All endpoint cases in the weighted statement, including N=0 and zero steps.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {f : E → ℝ} {G : ℝ≥0} {x g : ℕ → E} {a : ℕ → ℝ}
    (hf : LipschitzWith G f) (ha : ∀ k, 0 ≤ a k)
    (hs : ∀ k, SupportsAt f (x k) (g k))
    (hx : ∀ k, x (k + 1) = x k - a k • g k) (z : E) :
    2 * (∑ k ∈ Finset.range 0, a k * (f (x k) - f z)) ≤
      ‖x 0 - z‖ ^ 2 + (G : ℝ) ^ 2 * (∑ k ∈ Finset.range 0, (a k) ^ 2) - ‖x 0 - z‖ ^ 2 :=
  sum_weighted_gap_le hf ha hs hx z 0

-- A genuine nonsmooth objective: |x|, with positive iterates and geometrically
-- decreasing steps. No differentiability or supplied norm-bound premise.
example (N : ℕ) (hN : 0 < N) :
    ∃ i < N, |(1 / 2 : ℝ) ^ i| ≤
      (1 + ∑ k ∈ Finset.range N, ((1 / 2 : ℝ) ^ (k + 1)) ^ 2) /
        (2 * ∑ k ∈ Finset.range N, (1 / 2 : ℝ) ^ (k + 1)) := by
  have hLip : LipschitzWith 1 (fun x : ℝ => |x|) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    simpa only [NNReal.coe_one, one_mul, Real.dist_eq] using abs_abs_sub_abs_le_abs_sub x y
  have hs (k : ℕ) : SupportsAt (fun x : ℝ => |x|) ((1 / 2 : ℝ) ^ k) 1 := by
    intro z
    change |(1 / 2 : ℝ) ^ k| + inner ℝ (1 : ℝ) (z - (1 / 2 : ℝ) ^ k) ≤ |z|
    rw [abs_of_nonneg (pow_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2) k)]
    simpa using le_abs_self z
  have hx (k : ℕ) : (1 / 2 : ℝ) ^ (k + 1) =
      (1 / 2 : ℝ) ^ k - (1 / 2 : ℝ) ^ (k + 1) • (1 : ℝ) := by
    simp only [smul_eq_mul, mul_one, pow_succ]
    ring
  simpa using exists_gap_le hLip
    (fun k => pow_pos (by norm_num : (0 : ℝ) < 1 / 2) (k + 1)) hs hx 0 hN

#print axioms SubgradientMethod.norm_le_of_supportsAt
#print axioms SubgradientMethod.sum_weighted_gap_le
#print axioms SubgradientMethod.exists_gap_le
