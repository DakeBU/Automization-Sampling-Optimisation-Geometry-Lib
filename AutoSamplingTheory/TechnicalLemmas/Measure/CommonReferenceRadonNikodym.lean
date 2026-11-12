import AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym
import Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym

/-!
# Radon--Nikodym quotient for two densities over a common reference measure

Chewi Theorem 8.3.1 proves the simultaneous `f`-divergence identity by writing
both laws as densities with respect to one reference measure `m` and then using
the pointwise quotient `p / q`.  The theorem statement, however, is written in
terms of the canonical Radon--Nikodym derivative `dμ/dν`.

Mathlib already supplies the two nontrivial ingredients:

* `Measure.rnDeriv_withDensity_left`, for changing the numerator measure by a
  density;
* `Measure.rnDeriv_withDensity_right`, for changing the denominator measure by
  a density.

This file only joins those canonical results when both measures come from the
same base measure.  It does not introduce a second Radon--Nikodym derivative.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace CommonReferenceRadonNikodym

open MeasureTheory
open scoped ENNReal NNReal

noncomputable section

variable {α : Type*} [MeasurableSpace α]

/-- If two measures have ENNReal densities `p` and `q` with respect to the same
sigma-finite reference measure, and `q` is finite and nonzero almost
everywhere, then the canonical Mathlib Radon--Nikodym derivative of
`m.withDensity p` with respect to `m.withDensity q` is `p / q` almost
everywhere with respect to the denominator measure.

Finiteness of `p` is also explicit because Mathlib's left-with-density theorem
needs it.  These are the exact totalization boundaries at which the quotient
formula can otherwise become misleading. -/
theorem rnDeriv_withDensity_div
    (m : Measure α) [SigmaFinite m]
    (p q : α → ℝ≥0∞)
    (hp : AEMeasurable p m)
    (hq : AEMeasurable q m)
    (hp_ne_top : ∀ᵐ x ∂m, p x ≠ ∞)
    (hq_ne_zero : ∀ᵐ x ∂m, q x ≠ 0)
    (hq_ne_top : ∀ᵐ x ∂m, q x ≠ ∞) :
    (m.withDensity p).rnDeriv (m.withDensity q) =ᵐ[m.withDensity q]
      fun x => p x / q x := by
  letI : SigmaFinite (m.withDensity q) :=
    SigmaFinite.withDensity_of_ne_top hq_ne_top
  have hq_ac : m.withDensity q ≪ m :=
    withDensity_absolutelyContinuous m q
  have hp_den : AEMeasurable p (m.withDensity q) :=
    hp.mono_ac hq_ac
  have hleft :=
    Measure.rnDeriv_withDensity_left
      (μ := m) (ν := m.withDensity q) (f := p) hp_den hp_ne_top
  have hright :=
    Measure.rnDeriv_withDensity_right m m hq hq_ne_zero hq_ne_top
  have hself : m.rnDeriv m =ᵐ[m] fun _ => 1 :=
    m.rnDeriv_self
  filter_upwards [hleft, hq_ac.ae_le hright, hq_ac.ae_le hself] with x hxLeft hxRight hxSelf
  rw [hxLeft, hxRight, hxSelf]
  simp [div_eq_mul_inv]

end

end CommonReferenceRadonNikodym
end Measure
end TechnicalLemmas
end AutoSamplingTheory
