import AutoSamplingTheory.Probability
import Mathlib.Analysis.Calculus.MeanValue

/-!
# Weak-generator technical lemmas

Reusable law-level weak-generator rewrites for SDE/Sampling proofs.

This file intentionally does not prove Ito's formula or a Fokker--Planck
density theorem.  It only packages the small Mathlib-facing step from a
sample-space weak-test derivative to a law-level weak-generator identity after
the analytic derivative, law identity, and generator pairings are supplied.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace WeakGenerator

open MeasureTheory
open scoped Topology

/-- Invariance of a measure for a nonnegative-time operator family on an
explicit test class. -/
def IsInvariantOn {E : Type*} [MeasurableSpace E]
    (P : ℝ → (E → ℝ) → E → ℝ) (μ : Measure E) (tests : Set (E → ℝ)) : Prop :=
  ∀ t, 0 ≤ t → ∀ f ∈ tests, ∫ x, P t f x ∂μ = ∫ x, f x ∂μ

/-- Semigroup and integrated-generator data sufficient for the standard
generator-to-invariance argument on an explicit domain.

The time parameter is represented by `ℝ`, but every law is required only for
nonnegative times.  The derivative field is a right derivative on `Ici t`,
which avoids silently extending a Markov semigroup to negative time. -/
structure IntegratedSemigroupGeneratorContract {E : Type*} [MeasurableSpace E]
    (P : ℝ → (E → ℝ) → E → ℝ)
    (generator : (E → ℝ) → E → ℝ)
    (domain : Set (E → ℝ))
    (μ : Measure E) : Prop where
  map_zero : ∀ f, P 0 f = f
  map_add : ∀ s, 0 ≤ s → ∀ t, 0 ≤ t → ∀ f,
    P (s + t) f = P s (P t f)
  orbit_mem_domain : ∀ t, 0 ≤ t → ∀ f ∈ domain, P t f ∈ domain
  pairing_continuousOn : ∀ t, 0 ≤ t → ∀ f ∈ domain,
    ContinuousOn (fun s => ∫ x, P s f x ∂μ) (Set.Icc 0 t)
  pairing_hasDerivWithinAt : ∀ t, 0 ≤ t → ∀ f ∈ domain,
    HasDerivWithinAt
      (fun s => ∫ x, P s f x ∂μ)
      (∫ x, generator (P t f) x ∂μ) (Set.Ici t) t

/-- A semigroup is invariant on its declared generator domain when integrated
generator action vanishes throughout that domain.

This theorem is the operator-domain-to-invariance bridge.  All analytic
content is visible in `IntegratedSemigroupGeneratorContract`; in particular,
the right derivative of the integral pairing and preservation of the domain
are not inferred from a formal differential expression. -/
theorem isInvariantOn_of_integral_generator_eq_zero
    {E : Type*} [MeasurableSpace E]
    {P : ℝ → (E → ℝ) → E → ℝ}
    {generator : (E → ℝ) → E → ℝ}
    {domain : Set (E → ℝ)} {μ : Measure E}
    (hsemigroup : IntegratedSemigroupGeneratorContract P generator domain μ)
    (hgenerator_zero : ∀ f ∈ domain, ∫ x, generator f x ∂μ = 0) :
    IsInvariantOn P μ domain := by
  intro t ht f hf
  have hconstant := constant_of_has_deriv_right_zero
    (hsemigroup.pairing_continuousOn t ht f hf) (fun s hs => by
      have hs0 : 0 ≤ s := hs.1
      simpa [hgenerator_zero (P s f)
        (hsemigroup.orbit_mem_domain s hs0 f hf)] using
        hsemigroup.pairing_hasDerivWithinAt s hs0 f hf)
  have htmem : t ∈ Set.Icc (0 : ℝ) t := ⟨ht, le_rfl⟩
  simpa [hsemigroup.map_zero f] using hconstant t htmem

/-- Move a supplied sample-space generator derivative to a named law path.

In SDE applications, `hderiv` is usually the Ito-generator derivative for a
test function composed with a process, while `hDrift` and `hDiffusion` identify
the sample drift and diffusion-generator terms with law-level weak-test
integrals.  The lemma proves only the reusable rewrite; it does not construct
the process, conditional drift, or Ito theorem.
-/
theorem weakGeneratorFromSampleDerivative {Ω E : Type*}
    [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X : ℝ → Ω → E} {ρ : ℝ → Measure E}
    {φ driftTerm diffusionTerm : E → ℝ}
    {sampleDrift sampleDiffusion : Ω → ℝ} {s0 σ : ℝ}
    (hρ : ∀ s, ρ s = Measure.map (X s) P)
    (hX : ∀ s, AEMeasurable (X s) P)
    (hφ : ∀ s, AEStronglyMeasurable φ (ρ s))
    (hderiv :
      HasDerivAt (fun s => ∫ ω, φ (X s ω) ∂P)
        ((∫ ω, sampleDrift ω ∂P) +
          (σ ^ 2 / 2) * (∫ ω, sampleDiffusion ω ∂P)) s0)
    (hDrift :
      (∫ ω, sampleDrift ω ∂P) = ∫ x, driftTerm x ∂ρ s0)
    (hDiffusion :
      (∫ ω, sampleDiffusion ω ∂P) = ∫ x, diffusionTerm x ∂ρ s0) :
    HasDerivAt (fun s => ∫ x, φ x ∂ρ s)
      ((∫ x, driftTerm x ∂ρ s0) +
        (σ ^ 2 / 2) * (∫ x, diffusionTerm x ∂ρ s0)) s0 := by
  have hbase :
      HasDerivAt (fun s => ∫ x, φ x ∂ρ s)
        ((∫ ω, sampleDrift ω ∂P) +
          (σ ^ 2 / 2) * (∫ ω, sampleDiffusion ω ∂P)) s0 :=
    AutoSamplingTheory.lawIntegralHasDerivAtOfMeasureMapEqAndSample
      (P := P) (X := X) (ρ := ρ) (φ := φ)
      hρ hX hφ hderiv
  simpa [hDrift, hDiffusion] using hbase

end WeakGenerator
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
