import AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio
import Mathlib.InformationTheory.KullbackLeibler.Basic

/-!
# KL divergence between two exponential tilts

This file converts Mathlib's canonical Radon--Nikodym log-likelihood ratio into
the explicit normalized log-density-ratio representative used in smooth paper
calculations.  The conversion is measure-theoretic only: it does not transport
classical derivatives across almost-everywhere equality.
-/

namespace AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedKL

open MeasureTheory

noncomputable section

variable {X : Type*} [MeasurableSpace X]

/-- If the explicit normalized log-ratio of two integrable exponential tilts
is integrable under the left tilt, then their canonical KL divergence is
finite and its real value is the integral of that explicit representative.

The integrability premise is deliberately stated for the displayed
representative.  Almost-everywhere equality is used only to transfer
integrability and the integral, never to transfer classical derivatives. -/
theorem finite_klDiv_and_toReal_eq_integral_normalizedLogRatio
    (mu : Measure X) [SigmaFinite mu] [NeZero mu] (f g : X → ℝ)
    (hf : Measurable f)
    (hfi : Integrable (fun x => Real.exp (f x)) mu)
    (hgi : Integrable (fun x => Real.exp (g x)) mu)
    (hrep : Integrable
      (fun x =>
        f x - Real.log (∫ z, Real.exp (f z) ∂mu) - g x +
          Real.log (∫ z, Real.exp (g z) ∂mu))
      (mu.tilted f)) :
    InformationTheory.klDiv (mu.tilted f) (mu.tilted g) ≠ ⊤ ∧
      (InformationTheory.klDiv (mu.tilted f) (mu.tilted g)).toReal =
        ∫ x,
          (f x - Real.log (∫ z, Real.exp (f z) ∂mu) - g x +
            Real.log (∫ z, Real.exp (g z) ∂mu)) ∂(mu.tilted f) := by
  let _ : IsProbabilityMeasure (mu.tilted f) := isProbabilityMeasure_tilted hfi
  let _ : IsProbabilityMeasure (mu.tilted g) := isProbabilityMeasure_tilted hgi
  have hae := TiltedLogRatio.llr_tilted_tilted_ae mu f g hf hfi hgi
  have hac : mu.tilted f ≪ mu.tilted g :=
    (tilted_absolutelyContinuous mu f).trans (absolutelyContinuous_tilted hgi)
  have hllr : Integrable (MeasureTheory.llr (mu.tilted f) (mu.tilted g))
      (mu.tilted f) :=
    hrep.congr hae.symm
  constructor
  · exact InformationTheory.klDiv_ne_top hac hllr
  · rw [InformationTheory.toReal_klDiv_of_measure_eq hac (by simp)]
    exact integral_congr_ae hae

end

end AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedKL
