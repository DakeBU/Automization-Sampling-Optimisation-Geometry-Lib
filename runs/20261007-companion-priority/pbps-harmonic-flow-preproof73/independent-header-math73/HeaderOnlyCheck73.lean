import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic

/-!
Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Algorithm 1 and Appendix A.1:
the literal deterministic harmonic arcs, their ODE and conserved energy.
This deterministic statement asserts no stochastic process or probability kernel.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow
open InnerProductSpace
open scoped ContDiff NNReal Topology
noncomputable section
set_option autoImplicit false

private def actual_harmonic_flow_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop :=
    let c : E → E → E := fun y xRef => y - η • gradient V xRef
    let Φ : E → E → ℝ → (E × E) → (E × E) := fun y xRef t z =>
      (c y xRef + Real.cos t • (z.1 - c y xRef) +
          (Real.sqrt η * Real.sin t) • z.2,
       (-Real.sin t / Real.sqrt η) • (z.1 - c y xRef) + Real.cos t • z.2)
    let H : E → E → (E × E) → ℝ := fun y xRef z =>
      (η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 + ‖z.2‖ ^ 2) / 2
    Continuous (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) ∧
    Measurable (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) ∧
    (∀ y xRef : E, ∀ z : E × E, Φ y xRef 0 z = z) ∧
    (∀ y xRef : E, ∀ s t : ℝ, ∀ z : E × E,
      Φ y xRef (s + t) z = Φ y xRef s (Φ y xRef t z)) ∧
    (∀ y xRef : E, ∀ t : ℝ, ∀ z : E × E,
      Φ y xRef (-t) (Φ y xRef t z) = z ∧
      Φ y xRef t (Φ y xRef (-t) z) = z) ∧
    (∀ y xRef : E, ∀ t : ℝ, ∀ z : E × E,
      HasDerivAt (fun s : ℝ => (Φ y xRef s z).1)
        (Real.sqrt η • (Φ y xRef t z).2) t ∧
      HasDerivAt (fun s : ℝ => (Φ y xRef s z).2)
        (-(Real.sqrt η)⁻¹ • ((Φ y xRef t z).1 - y) -
          Real.sqrt η • gradient V xRef) t) ∧
    (∀ y xRef : E, ∀ z : E × E, 0 ≤ H y xRef z) ∧
    (∀ y xRef : E, ∀ t : ℝ, ∀ z : E × E,
      H y xRef (Φ y xRef t z) = H y xRef z) ∧
    (∀ y xRef : E, ∀ z : E × E,
      Φ y xRef Real.pi z = ((2 : ℝ) • c y xRef - z.1, -z.2))


def prospective_public_target
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop :=
    actual_harmonic_flow_statement hα hαβ hV hH hη hβη

#check @actual_harmonic_flow_statement
#check @prospective_public_target
#check @AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
#check @Continuous.measurable
#check @Real.hasDerivAt_sin
#check @Real.hasDerivAt_cos

section CarrierOnly
variable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
[FiniteDimensional ℝ F] [MeasurableSpace F] [BorelSpace F]
#synth CompleteSpace F
#synth SecondCountableTopology F
#synth BorelSpace (F × F)
#synth BorelSpace ((F × F) × ℝ × (F × F))
end CarrierOnly
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow
