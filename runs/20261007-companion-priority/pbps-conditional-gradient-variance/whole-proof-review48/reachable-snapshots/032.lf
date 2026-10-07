import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Generator formulations of Poincare and log-Sobolev inequalities

These definitions follow Chewi's general reversible-Markov-process
formulations.  They are separate from the gradient-energy specialization in
`Poincare.lean`, which applies after the Langevin generator and its integration-
by-parts identity have been identified.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace FunctionalInequalities
namespace Generator

open MeasureTheory

variable {E : Type*} [MeasurableSpace E]

/-- The generator Dirichlet form `E(f,g) = integral f (-L)g d mu`. -/
noncomputable def dirichletForm
    (mu : Measure E) (generator : (E → ℝ) → E → ℝ)
    (f g : E → ℝ) : ℝ :=
  -(∫ x, f x * generator g x ∂mu)

/-- Variance as the squared centered `L2(mu)` norm. -/
noncomputable def variance (mu : Measure E) (f : E → ℝ) : ℝ :=
  ∫ x, (f x - ∫ y, f y ∂mu) ^ 2 ∂mu

/-- Domain conditions needed to read both sides of the generator Poincare
inequality as genuine finite integrals. -/
def PoincareAdmissible
    (mu : Measure E) (generator : (E → ℝ) → E → ℝ)
    (f : E → ℝ) : Prop :=
  Integrable f mu ∧
    Integrable (fun x => (f x - ∫ y, f y ∂mu) ^ 2) mu ∧
    Integrable (fun x => f x * generator f x) mu

/-- Chewi Definition 1.2.19: the generator Poincare inequality
`Var_mu(f) <= C * E(f,f)` for every admissible observable. -/
def SatisfiesPoincare
    (mu : Measure E) (generator : (E → ℝ) → E → ℝ)
    (C : ℝ) : Prop :=
  IsProbabilityMeasure mu ∧ 0 < C ∧
    ∀ f : E → ℝ, PoincareAdmissible mu generator f →
      variance mu f ≤ C * dirichletForm mu generator f f

/-- Relative entropy of a density `rho` with respect to its reference
probability measure.  Mathlib's totalized `Real.log 0 = 0` gives the standard
zero-density convention in the product `rho * log rho`. -/
noncomputable def densityEntropy (mu : Measure E) (rho : E → ℝ) : ℝ :=
  ∫ x, rho x * Real.log (rho x) ∂mu

/-- Domain conditions for the density formulation of log-Sobolev. -/
def LogSobolevAdmissible
    (mu : Measure E) (generator : (E → ℝ) → E → ℝ)
    (rho : E → ℝ) : Prop :=
  (0 ≤ rho) ∧
    Integrable rho mu ∧
    (∫ x, rho x ∂mu) = 1 ∧
    Integrable (fun x => rho x * Real.log (rho x)) mu ∧
    Integrable (fun x => rho x * generator (fun y => Real.log (rho y)) x) mu

/-- Chewi Definition 1.2.25: the density log-Sobolev inequality
`KL(rho mu || mu) <= (C/2) E(rho, log rho)`. -/
def SatisfiesLogSobolev
    (mu : Measure E) (generator : (E → ℝ) → E → ℝ)
    (C : ℝ) : Prop :=
  IsProbabilityMeasure mu ∧ 0 < C ∧
    ∀ rho : E → ℝ, LogSobolevAdmissible mu generator rho →
      densityEntropy mu rho ≤
        (C / 2) * dirichletForm mu generator rho (fun x => Real.log (rho x))

end Generator
end FunctionalInequalities
end TechnicalLemmas
end AutoSamplingTheory
