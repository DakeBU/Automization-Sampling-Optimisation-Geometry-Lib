import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.Topology.Order.Compact
import Mathlib.Tactic

/-!
# Existence of a minimizer for a strongly convex potential

A differentiable function with positive strong-convexity modulus on a
finite-dimensional real inner-product space grows at least quadratically after
its linear first-order term is absorbed.  Hence it attains a global minimum,
and differentiability makes the gradient vanish there.

This is the source-neutral existence step used implicitly by the initialization
proof in Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Lemma 4.16.  It is not a
Gibbs normalization, concentration, transport, or sampler theorem.
-/

noncomputable section

open Set Metric InnerProductSpace
open scoped RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexMinimizer

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E]

/-- A differentiable, positively strongly convex function on a finite-dimensional
real inner-product space has a global minimizer, and its gradient vanishes there.

The proof does not use a totalized derivative as a regularity witness:
`Differentiable` supplies the genuine gradient and continuity. -/
theorem exists_isMinOn_and_gradient_eq_zero
    {V : E → ℝ} {m : ℝ} (hm : 0 < m)
    (hV : Differentiable ℝ V)
    (hsc : StrongConvexOn (Set.univ : Set E) m V) :
    ∃ p : E, IsMinOn V Set.univ p ∧ gradient V p = 0 := by
  let g : E := gradient V 0
  let R : ℝ := 2 * ‖g‖ / m
  have hR : 0 ≤ R := by
    dsimp only [R]
    positivity
  have hfirst (x : E) :
      V 0 + inner ℝ g x + m / 2 * ‖x‖ ^ 2 ≤ V x := by
    simpa only [g, sub_zero] using
      StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hsc
        (fun z _ ↦ (hV z).hasGradientAt) (x := 0) (y := x)
        (Set.mem_univ _) (Set.mem_univ _)
  have houtside {x : E} (hx : R < ‖x‖) : V 0 ≤ V x := by
    have hxpos : 0 < ‖x‖ := lt_of_le_of_lt hR hx
    have hscale : 2 * ‖g‖ < m * ‖x‖ := by
      dsimp only [R] at hx
      have hs := (div_lt_iff₀ hm).mp hx
      simpa [mul_comm] using hs
    have hinner : -(‖g‖ * ‖x‖) ≤ inner ℝ g x :=
      (abs_le.mp (abs_real_inner_le_norm g x)).1
    have hquad : ‖g‖ * ‖x‖ ≤ m / 2 * ‖x‖ ^ 2 := by
      nlinarith [mul_pos hm hxpos]
    linarith [hfirst x]
  have hzero : (0 : E) ∈ closedBall 0 R := by
    simp [hR]
  obtain ⟨p, hpBall, hpMinBall⟩ :=
    (isCompact_closedBall (0 : E) R).exists_isMinOn
      ⟨0, hzero⟩ hV.continuous.continuousOn
  have hpMin : IsMinOn V Set.univ p := by
    intro x _
    by_cases hxBall : x ∈ closedBall (0 : E) R
    · exact hpMinBall hxBall
    · have hx : R < ‖x‖ := by
        simpa [mem_closedBall, dist_eq_norm] using hxBall
      exact (hpMinBall hzero).trans (houtside hx)
  refine ⟨p, hpMin, ?_⟩
  simp [gradient, (hpMin.isLocalMin Filter.univ_mem).fderiv_eq_zero]

end AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexMinimizer
