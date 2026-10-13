import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LpSpace.Indicator

/-!
# Expectation as an L2 continuous linear functional

For a finite measure `pi`, Mathlib already provides the Hilbert space
`Lp ℝ 2 pi`, its constant functions, and the identity

`<f,g>_{L2(pi)} = integral f(x) g(x) dpi`.

This file packages the constant-one pairing as the canonical expectation
functional on `L2(pi)`.  It is the representation bridge needed to instantiate
abstract semigroup stationarity and reversibility results as integral identities
without inventing a second `L2` space.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace L2Expectation

open MeasureTheory
open scoped ENNReal InnerProductSpace

noncomputable section

variable {α : Type*} [MeasurableSpace α]

/-- The constant-one element of `L²(pi)` for a finite measure. -/
noncomputable def one
    (pi : Measure α) [IsFiniteMeasure pi] : Lp ℝ 2 pi :=
  Lp.const 2 pi (1 : ℝ)

/-- Expectation on `L²(pi)` as the continuous linear functional
`f ↦ <1,f>_{L²(pi)}`. -/
noncomputable def expectation
    (pi : Measure α) [IsFiniteMeasure pi] : Lp ℝ 2 pi →L[ℝ] ℝ :=
  innerSL ℝ (one pi)

@[simp]
theorem expectation_apply_eq_inner
    (pi : Measure α) [IsFiniteMeasure pi]
    (f : Lp ℝ 2 pi) :
    expectation pi f = inner ℝ (one pi) f := by
  rfl

/-- The `L²(pi)` expectation functional is exactly the Bochner integral of the
chosen `Lp` representative.  The equality is representative-safe because both
sides are insensitive to `pi`-a.e. changes. -/
theorem expectation_apply_eq_integral
    (pi : Measure α) [IsFiniteMeasure pi]
    (f : Lp ℝ 2 pi) :
    expectation pi f = ∫ x, f x ∂pi := by
  rw [expectation_apply_eq_inner, MeasureTheory.L2.inner_def]
  apply integral_congr_ae
  filter_upwards
      [Lp.coeFn_const (α := α) (μ := pi) (p := (2 : ℝ≥0∞)) (c := (1 : ℝ))]
      with x hx
  change inner ℝ (one pi x) (f x) = f x
  rw [show one pi x = (1 : ℝ) by simpa [one] using hx]
  simp

/-- Source-facing integral form of the constant-one `L²` pairing. -/
theorem inner_one_eq_integral
    (pi : Measure α) [IsFiniteMeasure pi]
    (f : Lp ℝ 2 pi) :
    inner ℝ (one pi) f = ∫ x, f x ∂pi := by
  simpa [expectation_apply_eq_inner] using expectation_apply_eq_integral pi f

end

end L2Expectation
end Measure
end TechnicalLemmas
end AutoSamplingTheory
