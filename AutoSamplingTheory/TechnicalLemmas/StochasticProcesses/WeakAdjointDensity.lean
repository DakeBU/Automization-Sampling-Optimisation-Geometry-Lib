import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Selected-time weak adjoint equation for densities

Chewi writes forward equations in the form

`∂ₜ μₜ = Lₜ* μₜ`.

For the simultaneous-flow calculation in Theorem 8.3.1, the exact information
used at a selected time is the weak pairing identity

`∫ φ · pDot dξ = ∫ (L φ) · p dξ`

for the frozen test observables appearing in the proof, where `p` is a density
of the law with respect to a common reference measure `ξ` and `pDot` is its
selected-time density derivative.

Samplinglib already has `WeakForwardEquation.kolmogorov_forward_weak_right` for
the dual action of a fixed continuous linear semigroup.  That theorem does not
cover an arbitrary time-dependent generator `Lₜ` or a common-reference density
presentation.  This module therefore introduces only the small selected-time
contract needed by the abstract Chapter 8 route.

Both pairing integrabilities are explicit.  This prevents Mathlib's totalized
Bochner integral from turning an undefined analytic manipulation into a formal
zero.  The contract does not assert that `pDot` is actually the derivative of a
density path; that remains a separate time-regularity obligation.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace WeakAdjointDensity

open MeasureTheory

noncomputable section

/-- Weak selected-time realization of `densityDot = L* density` on an explicit
test domain.

The generator may itself come from a time-dependent family; only its value at
the selected time appears here.  The two integrability fields are part of the
analytic contract rather than consequences of the scalar equality of the
totalized integrals. -/
structure WeakAdjointDensityEquationAt
    {X : Type*} [MeasurableSpace X]
    (base : Measure X)
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    (density densityDot : X → ℝ)
    (domain : Set (X → ℝ)) : Prop where
  time_pairing_integrable :
    ∀ {phi : X → ℝ}, phi ∈ domain →
      Integrable (fun x => phi x * densityDot x) base
  generator_pairing_integrable :
    ∀ {phi : X → ℝ}, phi ∈ domain →
      Integrable (fun x => generator phi x * density x) base
  pairing_eq :
    ∀ {phi : X → ℝ}, phi ∈ domain →
      (∫ x, phi x * densityDot x ∂base) =
        ∫ x, generator phi x * density x ∂base

/-- Selected test observables have integrable time-derivative pairings. -/
theorem time_pairing_integrable
    {X : Type*} [MeasurableSpace X]
    {base : Measure X}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {density densityDot : X → ℝ}
    {domain : Set (X → ℝ)}
    (h : WeakAdjointDensityEquationAt base generator density densityDot domain)
    {phi : X → ℝ} (hphi : phi ∈ domain) :
    Integrable (fun x => phi x * densityDot x) base :=
  h.time_pairing_integrable hphi

/-- Selected test observables have integrable generator pairings. -/
theorem generator_pairing_integrable
    {X : Type*} [MeasurableSpace X]
    {base : Measure X}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {density densityDot : X → ℝ}
    {domain : Set (X → ℝ)}
    (h : WeakAdjointDensityEquationAt base generator density densityDot domain)
    {phi : X → ℝ} (hphi : phi ∈ domain) :
    Integrable (fun x => generator phi x * density x) base :=
  h.generator_pairing_integrable hphi

/-- Extract the weak-adjoint pairing identity for one admissible observable. -/
theorem pairing_eq
    {X : Type*} [MeasurableSpace X]
    {base : Measure X}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {density densityDot : X → ℝ}
    {domain : Set (X → ℝ)}
    (h : WeakAdjointDensityEquationAt base generator density densityDot domain)
    {phi : X → ℝ} (hphi : phi ∈ domain) :
    (∫ x, phi x * densityDot x ∂base) =
      ∫ x, generator phi x * density x ∂base :=
  h.pairing_eq hphi

end

end WeakAdjointDensity
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
