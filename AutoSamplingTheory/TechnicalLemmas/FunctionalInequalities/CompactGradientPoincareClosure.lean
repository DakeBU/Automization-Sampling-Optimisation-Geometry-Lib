/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare
import Mathlib.Probability.Moments.Variance

/-!
# Poincaré on the closure of the compact gradient pairs

An explicit Euclidean graph-closure step for Chewi, *Log-Concave Sampling*,
Exercise 1.7 and the density discussion in §2.1.1. This does not assume or
prove single-valuedness of the closure for an arbitrary measure.
-/

set_option autoImplicit false

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactGradientPoincareClosure

open MeasureTheory InnerProductSpace
open scoped ContDiff RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Compact smooth LSI gives the same-constant variance bound on the joint
`L² × L²` closure of the original compact smooth function/gradient pairs. -/
theorem poincare_of_compact_logSobolev_on_gradient_closure
    (μ : Measure E) [IsProbabilityMeasure μ] (C : ℝ) (hC : 0 < C)
    (hLSI : ∀ v : E → ℝ, ContDiff ℝ ∞ v → HasCompactSupport v →
      (∫ x, (v x)^2 * Real.log ((v x)^2) ∂μ) -
        (∫ x, (v x)^2 ∂μ) * Real.log (∫ x, (v x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient v x‖^2 ∂μ)
    (p : Lp ℝ 2 μ × Lp E 2 μ)
    (hp : p ∈ closure {r | ∃ g : E → ℝ, ContDiff ℝ ∞ g ∧ HasCompactSupport g ∧
        r.1 =ᵐ[μ] g ∧ r.2 =ᵐ[μ] gradient g}) :
    ProbabilityTheory.variance (p.1 : E → ℝ) μ ≤ C * ‖p.2‖^2 := by
  have norm_sq (z : Lp E 2 μ) : ‖z‖^2 = ∫ x, ‖z x‖^2 ∂μ := by
    rw [← real_inner_self_eq_norm_sq, L2.inner_def]
    simp only [real_inner_self_eq_norm_sq]
  have hone : MemLp (fun _ : E => (1 : ℝ)) 2 μ := memLp_const 1
  let one := hone.toLp (fun _ : E => (1 : ℝ))
  have mean (a : Lp ℝ 2 μ) : inner ℝ one a = ∫ x, a x ∂μ := by
    rw [L2.inner_def]
    apply integral_congr_ae
    filter_upwards [hone.coeFn_toLp] with x hx
    change inner ℝ (one x) (a x) = a x
    rw [show one x = 1 from hx]
    simp
  have var (a : Lp ℝ 2 μ) :
      ProbabilityTheory.variance (a : E → ℝ) μ = ‖a‖^2 - (inner ℝ one a)^2 := by
    have ha : ‖a‖^2 = ∫ x, (a x)^2 ∂μ := by
      rw [← real_inner_self_eq_norm_sq, L2.inner_def]
      simp only [real_inner_self_eq_norm_sq, Real.norm_eq_abs, sq_abs]
    rw [ProbabilityTheory.variance_eq_sub (Lp.memLp a), mean, ha]
    rfl
  let S : Set (Lp ℝ 2 μ × Lp E 2 μ) :=
    {r | ProbabilityTheory.variance (r.1 : E → ℝ) μ ≤ C * ‖r.2‖^2}
  have hS : IsClosed S := by
    dsimp only [S]
    simp_rw [var]
    exact isClosed_le
      ((continuous_fst.norm.pow 2).sub ((continuous_const.inner continuous_fst).pow 2))
      (continuous_const.mul (continuous_snd.norm.pow 2))
  have hcompact : {r : Lp ℝ 2 μ × Lp E 2 μ | ∃ g : E → ℝ,
      ContDiff ℝ ∞ g ∧ HasCompactSupport g ∧ r.1 =ᵐ[μ] g ∧
      r.2 =ᵐ[μ] gradient g} ⊆ S := by
    rintro ⟨a, b⟩ ⟨g, hg, hgc, ha, hb⟩
    change ProbabilityTheory.variance (a : E → ℝ) μ ≤ C * ‖b‖^2
    have henergy : (∫ x, ‖b x‖^2 ∂μ) = ∫ x, ‖gradient g x‖^2 ∂μ :=
      integral_congr_ae (hb.mono fun _ hx => congrArg (fun v : E => ‖v‖^2) hx)
    rw [ProbabilityTheory.variance_congr ha,
      ProbabilityTheory.variance_eq_integral hg.continuous.measurable.aemeasurable,
      norm_sq b, henergy]
    exact CompactLogSobolevPoincare.poincare_of_compact_logSobolev μ C hC hLSI g hg hgc
  exact closure_minimal hcompact hS hp

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactGradientPoincareClosure
