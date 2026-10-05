import Mathlib.Analysis.Normed.Group.Uniform
import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.Topology.Order.Compact
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Quadratic regularization: existence, radius and accuracy

Chewi arXiv2605.07006v1 Section4.1 Lemma4.2, the objective and radius comparisons.
Construct the regularized minimizer rather than assuming it. Source Euclidean
spaces are proper, and source smoothness implies the continuity used here.
This comparison component does not need convexity, differentiability or C².
It does not prove curvature, solver costs or first-order oracle/class semantics.
-/
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationTransfer
open Set Metric

/-- A continuous objective with an attained minimum has an actual regularized
minimum in a proper normed group; its radius and approximate values transfer. -/
theorem exists_minimizer_radius_and_accuracy
    {E : Type*} [NormedAddCommGroup E] [ProperSpace E]
    {f : E → ℝ} (hf : Continuous f) {z x₀ : E} (hz : IsMinOn f univ z)
    {R ε : ℝ} (hR : 0 < R) (hε : 0 < ε) (hx : ‖z-x₀‖ ≤ R) :
    let δ := ε/R^2
    let W := fun x => f x + δ/2*‖x-x₀‖^2
    ∃ w, IsMinOn W univ w ∧ ‖w-x₀‖ ≤ ‖z-x₀‖ ∧
      ∀ x, W x - W w ≤ ε/2 → f x - f z ≤ ε := by
  let δ := ε/R^2
  let W := fun x => f x + δ/2*‖x-x₀‖^2
  have hδ : 0 < δ := div_pos hε (sq_pos_of_pos hR)
  have hn : Continuous (fun x : E => ‖x-x₀‖^2) :=
    ((continuous_id.sub continuous_const).norm).pow 2
  have hW : Continuous W := hf.add (continuous_const.mul hn)
  have hzball : z ∈ closedBall x₀ R := by simpa [mem_closedBall, dist_eq_norm] using hx
  obtain ⟨w, _, hw⟩ := (isCompact_closedBall x₀ R).exists_isMinOn ⟨z,hzball⟩ hW.continuousOn
  have hwz : W w ≤ W z := hw hzball
  have hglobal : IsMinOn W univ w := by
    intro x _
    by_cases hb : x ∈ closedBall x₀ R
    · exact hw hb
    · have hr : R < ‖x-x₀‖ := by simpa [mem_closedBall, dist_eq_norm] using hb
      have hs : ‖z-x₀‖^2 ≤ ‖x-x₀‖^2 := by
        nlinarith [norm_nonneg (z-x₀), norm_nonneg (x-x₀)]
      have hzfx : f z ≤ f x := hz (mem_univ x)
      have hquad := mul_le_mul_of_nonneg_left hs (le_of_lt (div_pos hδ (by norm_num : (0:ℝ)<2)))
      have hzW : W z ≤ W x := by dsimp [W]; linarith
      exact hwz.trans hzW
  have hradius : ‖w-x₀‖ ≤ ‖z-x₀‖ := by
    have hzw : f z ≤ f w := hz (mem_univ w)
    have hs : ‖w-x₀‖^2 ≤ ‖z-x₀‖^2 := by
      dsimp [W] at hwz
      nlinarith
    nlinarith [norm_nonneg (w-x₀), norm_nonneg (z-x₀)]
  refine ⟨w,hglobal,hradius,?_⟩
  intro x he
  have hbase : f x ≤ W x := by
    dsimp [W]
    exact le_add_of_nonneg_right (mul_nonneg (div_nonneg hδ.le (by norm_num)) (sq_nonneg _))
  have hs : ‖z-x₀‖^2 ≤ R^2 := by nlinarith [norm_nonneg (z-x₀)]
  have hquad := mul_le_mul_of_nonneg_left hs (le_of_lt (div_pos hδ (by norm_num : (0:ℝ)<2)))
  have hid : δ/2*R^2 = ε/2 := by dsimp [δ]; field_simp
  rw [hid] at hquad
  dsimp [W] at hwz
  change W x - W w ≤ ε/2 at he
  have : W w ≤ f z + ε/2 := by dsimp [W]; linarith
  linarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationTransfer
