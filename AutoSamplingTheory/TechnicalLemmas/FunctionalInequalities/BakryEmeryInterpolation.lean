import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.SemigroupDecay
import Mathlib.Analysis.Calculus.Deriv.MeanValue

/-!
# Scalar Bakry--Émery interpolation

The Bakry--Émery gradient argument studies a backward interpolation quantity
whose derivative is bounded below by a constant multiple of itself.  This file
isolates the scalar comparison step: exponential growth along the interpolation
is equivalent to exponential contraction when its endpoints are read in the
opposite direction.

The theorem does not construct a Markov semigroup, identify a carré du champ,
or prove the interpolation derivative formula.  Those remain model-facing
analytic inputs.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace FunctionalInequalities
namespace SemigroupDecay

open Filter Set
open scoped Topology

noncomputable section

/-- A lower differential bound along a backward interpolation gives the
endpoint contraction estimate used in the Bakry--Émery method.

No sign condition on `interpolation` or `rate` is needed for this scalar
comparison. -/
theorem backward_interpolation_contraction_of_growth
    {interpolation interpolation' : ℝ → ℝ} {rate s t : ℝ}
    (hcontinuous : Continuous interpolation)
    (hderiv : ∀ u : ℝ,
      HasDerivWithinAt interpolation (interpolation' u) (Ici u) u)
    (hgrowth : ∀ u : ℝ,
      rate * interpolation u ≤ interpolation' u)
    (hst : s ≤ t) :
    interpolation s ≤
      interpolation t * Real.exp (-rate * (t - s)) := by
  have hbound : ∀ x ∈ Ico s t,
      -interpolation' x ≤ rate * (-interpolation x) + 0 := by
    intro x _hx
    have hneg := neg_le_neg (hgrowth x)
    simpa [neg_mul] using hneg
  have hgronwall :=
    le_gronwallBound_of_liminf_deriv_right_le
      (f := fun x => -interpolation x)
      (f' := fun x => -interpolation' x)
      (δ := -interpolation s)
      (K := rate)
      (ε := 0)
      (a := s)
      (b := t)
      hcontinuous.neg.continuousOn
      (fun x _hx r hr => by
        simpa [slope] using ((hderiv x).neg.liminf_right_slope_le hr))
      le_rfl
      hbound
      t
      ⟨hst, le_rfl⟩
  rw [gronwallBound_ε0] at hgronwall
  have hexponential_growth :
      interpolation s * Real.exp (rate * (t - s)) ≤ interpolation t := by
    linarith
  have hscaled := mul_le_mul_of_nonneg_right hexponential_growth
    (Real.exp_nonneg (-rate * (t - s)))
  have hinverse :
      Real.exp (rate * (t - s)) * Real.exp (-rate * (t - s)) = 1 := by
    rw [← Real.exp_add]
    have hzero : rate * (t - s) + -rate * (t - s) = 0 := by ring
    rw [hzero, Real.exp_zero]
  calc
    interpolation s =
        (interpolation s * Real.exp (rate * (t - s))) *
          Real.exp (-rate * (t - s)) := by
      rw [mul_assoc, hinverse, mul_one]
    _ ≤ interpolation t * Real.exp (-rate * (t - s)) := hscaled

/-- Interval-scoped Bakry--Émery comparison.

If an interpolation has derivative at every point of `[s, t]` and its
derivative dominates `rate` times the interpolation on `(s, t)`, then reading
the endpoints in the backward direction gives exponential contraction.  The
statement asks for no sign condition on the interpolation or on `rate` and
allows the degenerate interval `s = t`. -/
theorem backward_endpoint_contraction_of_growth_on_Icc
    {interpolation interpolation' : ℝ → ℝ} {rate s t : ℝ}
    (hst : s ≤ t)
    (hinterpolation : ∀ u ∈ Icc s t,
      HasDerivAt interpolation (interpolation' u) u)
    (hgrowth : ∀ u ∈ Ioo s t,
      rate * interpolation u ≤ interpolation' u) :
    interpolation s ≤
      interpolation t * Real.exp (-rate * (t - s)) := by
  let weighted : ℝ → ℝ := fun u =>
    interpolation u * Real.exp (-rate * (u - s))
  have hweighted : ∀ u ∈ Icc s t,
      HasDerivAt weighted
        ((interpolation' u - rate * interpolation u) *
          Real.exp (-rate * (u - s))) u := by
    intro u hu
    have hinner :
        HasDerivAt (fun v : ℝ => -rate * (v - s)) (-rate) u := by
      simpa using ((hasDerivAt_id u).sub_const s).const_mul (-rate)
    have hexp := (Real.hasDerivAt_exp (-rate * (u - s))).comp u hinner
    have hmul := (hinterpolation u hu).mul hexp
    change HasDerivAt
      (fun v => interpolation v * Real.exp (-rate * (v - s)))
      ((interpolation' u - rate * interpolation u) *
        Real.exp (-rate * (u - s))) u
    exact hmul.congr_deriv (by
      simp only [Function.comp_apply]
      ring)
  have hmono : MonotoneOn weighted (Icc s t) := by
    apply monotoneOn_of_deriv_nonneg (convex_Icc s t)
    · exact continuousOn_of_forall_continuousAt fun u hu =>
        (hweighted u hu).continuousAt
    · intro u hu
      exact (hweighted u (interior_subset hu)).differentiableAt.differentiableWithinAt
    · intro u hu
      rw [(hweighted u (interior_subset hu)).deriv]
      exact mul_nonneg (sub_nonneg.mpr
        (hgrowth u (by simpa only [interior_Icc] using hu)))
        (Real.exp_nonneg _)
  have hend := hmono ⟨le_rfl, hst⟩ ⟨hst, le_rfl⟩ hst
  simpa only [weighted, sub_self, mul_zero, Real.exp_zero, mul_one] using hend

end

end SemigroupDecay
end FunctionalInequalities
end TechnicalLemmas
end AutoSamplingTheory
