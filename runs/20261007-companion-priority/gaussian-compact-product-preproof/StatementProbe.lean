import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Integral.Pi
import Mathlib.Analysis.Calculus.FDeriv.Const

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators

#check (∀ (n : ℕ) (f : (Fin n → ℝ) → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f),
    let γ : Measure (Fin n → ℝ) := Measure.pi (fun _ : Fin n => gaussianReal 0 1)
    let D : Fin n → (Fin n → ℝ) → ℝ := fun i x => fderiv ℝ f x (Pi.single i 1)
    Integrable (fun x => (f x)^2) γ ∧
    Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) γ ∧
    (∀ i, Integrable (fun x => (D i x)^2) γ) ∧
    Integrable (fun x => ∑ i, (D i x)^2) γ ∧
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
    2 * ∫ x, ∑ i, (D i x)^2 ∂γ)
