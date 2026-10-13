import AutoSamplingTheory.TechnicalLemmas.Geometry.LogConcavity
import Mathlib.Analysis.Convex.Strong

/-!
# Strong convexity leaves

Small strong-convexity bridges for log-concave sampling targets.  The main
consumer is Gibbs normalization: a strongly convex potential with an exposed
global minimizer has a centered quadratic lower envelope.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Geometry
namespace StrongConvexity

open Set

/-- A nonnegatively strongly convex function is convex.

This is the small Mathlib-facing bridge from Chewi's strong-convexity
assumptions to ordinary convex-potential density geometry. -/
theorem convexOn_of_strongConvexOn_nonneg
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {s : Set E} {V : E → ℝ} {k : ℝ}
    (hV : StrongConvexOn s k V) (hk : 0 ≤ k) :
    ConvexOn ℝ s V := by
  simpa using (StrongConvexOn.mono (s := s) (f := V) hk hV)

/-- A strongly convex potential with nonnegative modulus gives a log-concave
unnormalized Gibbs density shape. -/
theorem logConcaveOn_exp_neg_of_strongConvexOn
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {s : Set E} {V : E → ℝ} {k : ℝ}
    (hV : StrongConvexOn s k V) (hk : 0 ≤ k) :
    LogConcavity.LogConcaveOn s (fun x => Real.exp (-V x)) :=
  LogConcavity.logConcaveOn_exp_neg_of_convexOn
    (convexOn_of_strongConvexOn_nonneg hV hk)

/-- Positive scalar normalization preserves the log-concavity of a Gibbs shape
whose potential is strongly convex with nonnegative modulus. -/
theorem logConcaveOn_const_mul_exp_neg_of_strongConvexOn
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {s : Set E} {V : E → ℝ} {k c : ℝ}
    (hV : StrongConvexOn s k V) (hk : 0 ≤ k) (hc : 0 < c) :
    LogConcavity.LogConcaveOn s (fun x => c * Real.exp (-V x)) :=
  LogConcavity.logConcaveOn_const_mul_exp_neg_of_convexOn
    (convexOn_of_strongConvexOn_nonneg hV hk) hc

/-- A strongly convex function with a global minimizer has a centered quadratic
lower bound.

The constant `k / 4` is the midpoint consequence of Mathlib's
`StrongConvexOn` convention.  It is intentionally not the sharp `k / 2`
first-order/subgradient bound, because this leaf requires no differentiability
or limiting argument and is enough for Gibbs-tail integrability. -/
theorem centered_quadratic_lower_bound_of_strongConvexOn_minimizer
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {V : E → ℝ} {k : ℝ} (hV : StrongConvexOn (Set.univ : Set E) k V)
    (x₀ : E) (hx₀ : IsMinOn V (Set.univ : Set E) x₀) :
    ∀ x : E, V x₀ + (k / 4) * ‖x - x₀‖ ^ 2 ≤ V x := by
  intro x
  have hx₀_min : ∀ y : E, V x₀ ≤ V y := isMinOn_univ_iff.mp hx₀
  have hmid_min : V x₀ ≤ V ((1 / 2 : ℝ) • x₀ + (1 / 2 : ℝ) • x) := hx₀_min _
  have hstrong :=
    hV.2 (by simp : x₀ ∈ (Set.univ : Set E)) (by simp : x ∈ (Set.univ : Set E))
      (by norm_num : 0 ≤ (1 / 2 : ℝ)) (by norm_num : 0 ≤ (1 / 2 : ℝ))
      (by norm_num : (1 / 2 : ℝ) + (1 / 2 : ℝ) = 1)
  have hstrong' :
      V ((1 / 2 : ℝ) • x₀ + (1 / 2 : ℝ) • x) ≤
        (1 / 2 : ℝ) * V x₀ + (1 / 2 : ℝ) * V x - (k / 8) * ‖x - x₀‖ ^ 2 := by
    rw [norm_sub_rev x₀ x] at hstrong
    convert hstrong using 1
    · simp [smul_eq_mul]
      ring_nf
  have hle := hmid_min.trans hstrong'
  nlinarith

end StrongConvexity
end Geometry
end TechnicalLemmas
end AutoSamplingTheory
