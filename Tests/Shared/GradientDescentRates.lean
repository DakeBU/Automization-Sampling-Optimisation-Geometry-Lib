import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates
open Set
open scoped RealInnerProductSpace

-- Actual quadratic and actual iterates, arbitrary comparator, all 0<h<=1.
-- The h=1 endpoint and positive-base inverse form are exercised together.
example (x z h : ℝ) (hh : 0 < h) (hs : h ≤ 1) {N : ℕ} (hN : 0 < N) :
    let X := (fun t : ℝ => t - h * t)^[N] x
    X^2/2 - z^2/2 ≤ (x-z)^2 / (2*h*N) ∧
    X^2/2 - z^2/2 ≤ (1-h)^N * (x-z)^2 / (2*(1-(1-h)^N)) ∧
    (h < 1 → X^2/2 - z^2/2 ≤ 1 / (2*((1-h)^(-(N:ℤ))-1)) * (x-z)^2) := by
  let f : ℝ → ℝ := fun t => t^2/2
  have hf : ContDiff ℝ 1 f := (contDiff_id.pow 2).div_const 2
  have hg (t : ℝ) : gradient f t = t := by
    have hd : HasDerivAt f t t := by
      simpa [f] using ((hasDerivAt_id t).pow 2).div_const (2 : ℝ)
    exact hd.hasGradientAt.gradient
  have hc : StrongConvexOn univ 1 f := by
    rw [strongConvexOn_iff_convex]
    have he : (fun t : ℝ => f t - (1 : ℝ)/2 * ‖t‖^2) = fun _ => 0 := by
      funext t; simp [f, Real.norm_eq_abs, sq_abs]; ring
    rw [he]
    exact convexOn_const _ convex_univ
  have hu : ∀ a b, f b ≤ f a + inner ℝ (gradient f a) (b-a) + 1/2*‖b-a‖^2 := by
    intro a b; rw [hg]; simp only [f, Real.inner_apply, Real.norm_eq_abs, sq_abs]; nlinarith
  have cv := convex_value_le hf (hc.convexOn (by intro r; positivity)) hh (by simpa using hs) hu x z hN
  have sc := strongly_convex_value_le hf hc (by norm_num) hh (by simpa using hs)
    (by simpa using hs) hu x z hN
  simpa [f, hg, Real.norm_eq_abs, sq_abs] using And.intro cv sc

-- The source's prescribed h=1/beta convex rate is a consumer of the public API.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f : E → ℝ} {β : ℝ} (hf : ContDiff ℝ 1 f) (hc : ConvexOn ℝ univ f)
    (hβ : 0 < β)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y-x) + β/2*‖y-x‖^2)
    (x z : E) {N : ℕ} (hN : 0 < N) :
    f ((fun x => x - β⁻¹ • gradient f x)^[N] x) - f z ≤ β * ‖x-z‖^2 / (2*N) := by
  have hr := convex_value_le hf hc (inv_pos.mpr hβ) (by simp [ne_of_gt hβ]) hu x z hN
  convert hr using 1
  field_simp

-- Totalized inverse powers at q=0 would make the displayed source upper bound false:
-- unit quadratic, h=alpha=beta=N=1, z=0,x0=1 has final gap0.
example : ¬ ((0 : ℝ) ≤ 1 / (2 * ((0 : ℝ) ^ (-(1 : ℤ)) - 1))) := by norm_num

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates.convex_value_le
#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates.strongly_convex_value_le
