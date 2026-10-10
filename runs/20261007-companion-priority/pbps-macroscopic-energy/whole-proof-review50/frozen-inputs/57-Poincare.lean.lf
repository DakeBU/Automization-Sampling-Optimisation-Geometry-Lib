import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Poincare inequality interfaces

This file gives Chapter 2 a mathematical Lean interface rather than only a
string-valued task contract.  It keeps the test class and every integrability
condition explicit.  No Bakry--Emery criterion, tensorization, localization,
or sharp constant is proved here.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace FunctionalInequalities
namespace Poincare

open MeasureTheory
open scoped RealInnerProductSpace

variable {E : Type*} [MeasurableSpace E] [NormedAddCommGroup E]
  [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Variance written as the integral of the squared centered observable.

Admissibility is deliberately separate because the Bochner integral is
totalized outside its integrable domain. -/
noncomputable def variance (μ : Measure E) (f : E → ℝ) : ℝ :=
  ∫ x, (f x - ∫ y, f y ∂μ) ^ 2 ∂μ

/-- The Euclidean/inner-product Dirichlet energy of a test function. -/
noncomputable def dirichletEnergy (μ : Measure E) (f : E → ℝ) : ℝ :=
  ∫ x, ‖gradient f x‖ ^ 2 ∂μ

/-- Exact integrability domain used by the local Poincare interface. -/
def Admissible (μ : Measure E) (f : E → ℝ) : Prop :=
  Integrable f μ ∧
    Integrable (fun x => (f x - ∫ y, f y ∂μ) ^ 2) μ ∧
    Integrable (fun x => ‖gradient f x‖ ^ 2) μ

/-- A measure satisfies the Poincare inequality with constant `C` on an
explicit test class.

The convention is `Var_μ(f) ≤ C * E_μ(f)`.  Probability normalization is
part of the contract rather than an implicit convention. -/
def Satisfies (μ : Measure E) (tests : Set (E → ℝ)) (C : ℝ) : Prop :=
  IsProbabilityMeasure μ ∧ 0 ≤ C ∧
    ∀ f ∈ tests, Admissible μ f → variance μ f ≤ C * dirichletEnergy μ f

omit [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E] in
/-- Variance is nonnegative on its stated integral representation. -/
theorem variance_nonneg {μ : Measure E} {f : E → ℝ} :
    0 ≤ variance μ f := by
  rw [variance]
  exact integral_nonneg_of_ae
    (Filter.Eventually.of_forall fun x => sq_nonneg (f x - ∫ y, f y ∂μ))

/-- Dirichlet energy is nonnegative on its stated integrability domain. -/
theorem dirichletEnergy_nonneg {μ : Measure E} {f : E → ℝ} :
    0 ≤ dirichletEnergy μ f := by
  rw [dirichletEnergy]
  exact integral_nonneg_of_ae
    (Filter.Eventually.of_forall fun x => sq_nonneg ‖gradient f x‖)

/-- Increasing a nonnegative Poincare constant preserves the inequality on
the same test class and admissibility domain. -/
theorem mono_constant {μ : Measure E} {tests : Set (E → ℝ)} {C D : ℝ}
    (hC : Satisfies μ tests C) (hCD : C ≤ D) :
    Satisfies μ tests D := by
  refine ⟨hC.1, hC.2.1.trans hCD, ?_⟩
  intro f hf_tests hf
  exact (hC.2.2 f hf_tests hf).trans
    (mul_le_mul_of_nonneg_right hCD dirichletEnergy_nonneg)

/-- The inequality component can be consumed without unpacking the probability
and nonnegative-constant fields manually. -/
theorem variance_le {μ : Measure E} {tests : Set (E → ℝ)} {C : ℝ}
    (hC : Satisfies μ tests C) {f : E → ℝ}
    (hf_tests : f ∈ tests) (hf : Admissible μ f) :
    variance μ f ≤ C * dirichletEnergy μ f :=
  hC.2.2 f hf_tests hf

/-- Restricting the test class preserves a Poincare inequality and all of its
measure and constant data. -/
theorem mono_tests {μ : Measure E} {small large : Set (E → ℝ)} {C : ℝ}
    (hC : Satisfies μ large C) (hsub : small ⊆ large) :
    Satisfies μ small C := by
  refine ⟨hC.1, hC.2.1, ?_⟩
  intro f hf_tests
  exact hC.2.2 f (hsub hf_tests)

end Poincare
end FunctionalInequalities
end TechnicalLemmas
end AutoSamplingTheory
