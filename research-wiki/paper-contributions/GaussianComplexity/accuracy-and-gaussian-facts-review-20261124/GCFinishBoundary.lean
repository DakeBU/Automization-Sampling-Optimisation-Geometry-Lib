import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Mathlib.Tactic

/-! Comparison of the two rates in the discussion following Theorem 1.1.
At fixed accuracy the stated lower-bound formula is little-o of d on the edge of the
conjectured range. This is a comparison of formulas, with no sampling upper bound. -/
open Filter Real
open scoped Topology
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison

noncomputable def lowerRate (d κ ε : ℝ) := min d (sqrt κ * log (1 + d/(sqrt κ*ε)))
noncomputable def boundaryCondition (d : ℝ) := (d/log d)^2

theorem boundary_in_range {d : ℝ} (hd : 1 < d) : sqrt (boundaryCondition d)*log d = d := by
  have := log_pos hd
  rw [boundaryCondition, Real.sqrt_sq (by positivity : 0 ≤ d/log d)]
  exact div_mul_cancel₀ _ (log_pos hd).ne'

theorem boundary_rate_identity {d ε : ℝ} (hd : 1 < d) (he : 0 < ε) :
    lowerRate d (boundaryCondition d) ε / d = min 1 (log (1 + log d / ε)/log d) := by
  have hlog := log_pos hd
  have hd0 : d ≠ 0 := by linarith
  rw [lowerRate,boundaryCondition,Real.sqrt_sq (by positivity : 0 ≤ d/log d),
    ← min_div_div_right (by linarith : 0 ≤ d),div_self hd0]
  congr 1
  rw [show d/(d/log d*ε) = log d/ε by field_simp]
  field_simp

/-- For any fixed positive accuracy, the ratio to d tends to zero with integer d. -/
theorem boundary_rate_limit {ε : ℝ} (he : 0 < ε) :
    Tendsto (fun d : ℕ => lowerRate d (boundaryCondition d) ε / d) atTop (𝓝 0) := by
  let x (d : ℕ) := log (d : ℝ)
  let y (d : ℕ) := 1+x d/ε
  have hx : Tendsto x atTop atTop := tendsto_log_atTop.comp tendsto_natCast_atTop_atTop
  have hy : Tendsto y atTop atTop := tendsto_const_nhds.add_atTop (hx.atTop_div_const he)
  have hl : Tendsto (fun d => log (y d)/y d) atTop (𝓝 0) :=
    Real.isLittleO_log_id_atTop.tendsto_div_nhds_zero.comp hy
  have hfactor : Tendsto (fun d => y d/x d) atTop (𝓝 (1/ε)) := by
    have h := (hx.const_div_atTop 1).add (tendsto_const_nhds (x := 1/ε))
    rw [zero_add] at h
    apply h.congr'
    filter_upwards [hx.eventually_gt_atTop 0] with d hd
    dsimp [y]
    field_simp
  have hratio := hl.mul hfactor
  rw [zero_mul] at hratio
  have hmin := (tendsto_const_nhds (x := (1:ℝ))).min hratio
  norm_num only [min_eq_right (by norm_num : (0:ℝ) ≤ 1)] at hmin
  apply hmin.congr'
  filter_upwards [eventually_gt_atTop (1:ℕ),hy.eventually_gt_atTop 0] with d hd hyd
  rw [boundary_rate_identity (by exact_mod_cast hd) he]
  change min 1 (log (y d)/y d*(y d/x d)) = min 1 (log (y d)/x d)
  rw [div_mul_div_cancel₀ hyd.ne']

/-- Every proposed positive constant fails for the displayed rate, within the stated
parameter domain and on the boundary of the conjectured range. -/
theorem boundary_rate_below_every_linear_constant {ε c : ℝ} (he : 0 < ε) (hc : 0 < c) :
    ∀ᶠ d : ℕ in atTop, 4 ≤ boundaryCondition d ∧
      sqrt (boundaryCondition d)*log (d : ℝ) = (d : ℝ) ∧
      lowerRate d (boundaryCondition d) ε < c*d := by
  have h := Real.isLittleO_log_id_atTop.tendsto_div_nhds_zero.comp
    (tendsto_natCast_atTop_atTop (R := ℝ))
  have hs := h.eventually_lt_const (show (0 : ℝ) < 1/2 by norm_num)
  filter_upwards [eventually_gt_atTop (1 : ℕ), hs, (boundary_rate_limit he).eventually_lt_const hc]
    with d hd hsmall hrate
  have hd' : 1 < (d : ℝ) := by exact_mod_cast hd
  have hd0 : 0 < (d : ℝ) := by linarith
  have hl := log_pos hd'
  change log (d : ℝ)/(d : ℝ) < 1/2 at hsmall
  have h2 : 2 ≤ (d : ℝ)/log d := (le_div_iff₀ hl).2 (by linarith [(div_lt_iff₀ hd0).mp hsmall])
  refine ⟨?_, boundary_in_range hd', (div_lt_iff₀ hd0).mp hrate⟩
  unfold boundaryCondition
  nlinarith [sq_nonneg ((d : ℝ)/log d-2)]

#print axioms boundary_rate_below_every_linear_constant
#print axioms boundary_rate_limit
end AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison
