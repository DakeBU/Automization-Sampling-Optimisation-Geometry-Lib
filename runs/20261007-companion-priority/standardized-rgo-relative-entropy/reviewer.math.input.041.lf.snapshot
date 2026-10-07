import AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym
import Mathlib.InformationTheory.KullbackLeibler.Basic
import Mathlib.MeasureTheory.Measure.LogLikelihoodRatio
import Mathlib.Tactic

/-!
# Canonical Radon--Nikodym density and log-density ratio

This file fixes a single measure-level representative for the frontier sampling
spine.  Mathlib already defines the Radon--Nikodym derivative `mu.rnDeriv pi`
and the log-likelihood ratio

`MeasureTheory.llr mu pi = log ((mu.rnDeriv pi).toReal)`.

ASTIS therefore reuses those objects instead of creating a second KL/RN
hierarchy.  Downstream relative-Fisher and KL-dissipation theorems should import
this bridge and add only the differentiability/Sobolev/integrability hypotheses
needed for the score.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace InformationTheory
namespace RNLogRatio

open MeasureTheory
open scoped ENNReal NNReal

noncomputable section

variable {α : Type*} [MeasurableSpace α]

/-- The canonical real-valued Radon--Nikodym density representative used by
ASTIS.  The underlying measure-theoretic object remains Mathlib's ENNReal-valued
`rnDeriv`; `toReal` is only the real representative needed by calculus. -/
noncomputable def density (mu pi : Measure α) (x : α) : ℝ :=
  (mu.rnDeriv pi x).toReal

/-- The canonical log-density ratio.  This is definitionally Mathlib's
log-likelihood ratio, so KL and Fisher layers share one representative. -/
noncomputable def logRatio (mu pi : Measure α) : α → ℝ :=
  MeasureTheory.llr mu pi

@[simp]
theorem logRatio_apply (mu pi : Measure α) (x : α) :
    logRatio mu pi x = Real.log (density mu pi x) := by
  rfl

@[fun_prop]
theorem measurable_density (mu pi : Measure α) :
    Measurable (density mu pi) := by
  exact (Measure.measurable_rnDeriv mu pi).ennreal_toReal

@[fun_prop]
theorem measurable_logRatio (mu pi : Measure α) :
    Measurable (logRatio mu pi) := by
  simpa [logRatio] using MeasureTheory.measurable_llr mu pi

/-- The real RN density is pointwise nonnegative. -/
theorem density_nonneg (mu pi : Measure α) (x : α) :
    0 ≤ density mu pi x := by
  exact ENNReal.toReal_nonneg

/-- Absolute continuity makes the canonical real RN density positive `mu`-a.e.
The `rnDeriv < ∞` obligation is explicit because `toReal ∞ = 0`. -/
theorem density_ae_pos_of_absolutelyContinuous
    (mu pi : Measure α) [SigmaFinite mu]
    [Measure.HaveLebesgueDecomposition mu pi]
    (hmuPi : mu ≪ pi) :
    ∀ᵐ x ∂mu, 0 < density mu pi x := by
  filter_upwards [Measure.rnDeriv_pos hmuPi,
    hmuPi.ae_le (Measure.rnDeriv_lt_top mu pi)] with x hxPos hxTop
  exact ENNReal.toReal_pos hxPos.ne' hxTop.ne

/-- Exponentiating the canonical log-density ratio recovers the canonical RN
density `mu`-a.e. under absolute continuity. -/
theorem exp_logRatio_ae_eq_density_of_absolutelyContinuous
    (mu pi : Measure α) [SigmaFinite mu]
    [Measure.HaveLebesgueDecomposition mu pi]
    (hmuPi : mu ≪ pi) :
    (fun x => Real.exp (logRatio mu pi x)) =ᵐ[mu] density mu pi := by
  filter_upwards [MeasureTheory.exp_llr_of_ac mu pi hmuPi] with x hx
  simpa [logRatio, density] using hx

/-- The canonical density of a measure relative to itself is one a.e. -/
theorem density_self_ae (mu : Measure α) [SigmaFinite mu] :
    density mu mu =ᵐ[mu] fun _ => 1 := by
  filter_upwards [mu.rnDeriv_self] with x hx
  simp [density, hx]

/-- The canonical log-density ratio of a measure relative to itself is zero
a.e. -/
theorem logRatio_self_ae (mu : Measure α) [SigmaFinite mu] :
    logRatio mu mu =ᵐ[mu] fun _ => 0 := by
  filter_upwards [MeasureTheory.llr_self mu] with x hx
  simpa [logRatio] using hx

/-- For probability measures, finite KL has the source-facing integral form

`KL(mu || pi) = integral log(d mu / d pi) dmu`

at the real-valued level.  Mathlib's `klDiv` remains the canonical ENNReal
measure divergence; this theorem is the bridge used by calculus arguments. -/
theorem toReal_klDiv_eq_integral_logRatio_of_probability
    (mu pi : Measure α) [IsProbabilityMeasure mu] [IsProbabilityMeasure pi]
    (hmuPi : mu ≪ pi) :
    (_root_.InformationTheory.klDiv mu pi).toReal =
      ∫ x, logRatio mu pi x ∂mu := by
  simpa [logRatio] using
    (_root_.InformationTheory.toReal_klDiv_of_measure_eq
      (μ := mu) (ν := pi) hmuPi (by simp))

end

end RNLogRatio
end InformationTheory
end TechnicalLemmas
end AutoSamplingTheory
