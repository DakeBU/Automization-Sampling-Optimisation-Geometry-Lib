import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Tactic

/-! Monotone optimality implies a nonexpansive resolvent. This extracts the
existing SPHMC private proof for two actual proximal-estimator/phase consumers;
no new theorem-completion credit is attached to the extraction. -/
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.MonotoneProximalMap
open InnerProductSpace
open scoped RealInnerProductSpace

theorem nonexpansive_of_monotone_optimality
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {g p : E → E} {eta : ℝ} (heta : 0 ≤ eta)
    (hmono : ∀ x y, 0 ≤ inner ℝ (g x - g y) (x - y))
    (heq : ∀ y, p y + eta • g (p y) = y) : LipschitzWith 1 p := by
  apply LipschitzWith.of_dist_le_mul
  intro x y
  simp only [NNReal.coe_one, one_mul, dist_eq_norm]
  have hsub : x - y = (p x - p y) + eta • (g (p x) - g (p y)) := by
    calc
      x - y = (p x + eta • g (p x)) - (p y + eta • g (p y)) :=
        congrArg₂ (fun a b : E => a - b) (heq x).symm (heq y).symm
      _ = _ := by module
  have hpair : ‖p x - p y‖ ^ 2 ≤ inner ℝ (x - y) (p x - p y) := by
    calc
      _ ≤ ‖p x - p y‖ ^ 2 + eta * inner ℝ (g (p x) - g (p y)) (p x - p y) :=
        le_add_of_nonneg_right (mul_nonneg heta (hmono (p x) (p y)))
      _ = inner ℝ (x - y) (p x - p y) := by
        conv_rhs => rw [hsub]
        rw [inner_add_left, real_inner_smul_left, real_inner_self_eq_norm_sq]
  have hbound := hpair.trans (real_inner_le_norm (x - y) (p x - p y))
  by_cases hzero : ‖p x - p y‖ = 0
  · simpa only [hzero] using norm_nonneg (x - y)
  · have hpos : 0 < ‖p x - p y‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hzero)
    nlinarith


end AutoSamplingTheory.TechnicalLemmas.Analysis.MonotoneProximalMap
