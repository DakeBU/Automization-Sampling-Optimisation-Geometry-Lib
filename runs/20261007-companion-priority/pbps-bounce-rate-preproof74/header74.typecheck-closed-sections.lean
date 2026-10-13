import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic

/-!
Chen--Chewi--Lu--Zhang arXiv:2609.06905v1, Section2 (reflection), Algorithm1,
AppendixA.1 Ex4--6. Actual zero-safe Borel bounce and energy-layer rate bound.
This statement asserts no random path, clock, Markov kernel or nonexplosion.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate
open InnerProductSpace
open scoped ContDiff NNReal Topology
noncomputable section
set_option autoImplicit false

private def actual_bounce_rate_energy_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop :=
    let c : E → E → E := fun y xRef => y - η • gradient V xRef
    let h : E → E → E := fun xRef x => gradient V x - gradient V xRef
    let R : E → E → E := fun n p =>
      p - (2 * inner ℝ p n / ‖n‖ ^ 2) • n
    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, R (h xRef z.1) z.2)
    let rate : E → (E × E) → ℝ := fun xRef z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (h xRef z.1))
    let H : E → E → (E × E) → ℝ := fun y xRef z =>
      (η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 + ‖z.2‖ ^ 2) / 2
    Measurable (fun a : E × (E × E) => S a.1 a.2) ∧
    Continuous (fun a : E × (E × E) => rate a.1 a.2) ∧
    Measurable (fun a : E × (E × E) => rate a.1 a.2) ∧
    (∀ p : E, R 0 p = p) ∧
    (∀ n p : E, R n (R n p) = p ∧ ‖R n p‖ = ‖p‖ ∧
      inner ℝ (R n p) n = -inner ℝ p n) ∧
    (∀ xRef : E, ∀ z : E × E,
      (S xRef z).1 = z.1 ∧ S xRef (S xRef z) = z) ∧
    (∀ y xRef : E, ∀ z : E × E,
      H y xRef (S xRef z) = H y xRef z) ∧
    (∀ xRef : E, ∀ z : E × E, 0 ≤ rate xRef z ∧
      rate xRef (S xRef z) =
        Real.sqrt η * max 0 (-inner ℝ z.2 (h xRef z.1)) ∧
      rate xRef z - rate xRef (S xRef z) =
        Real.sqrt η * inner ℝ z.2 (h xRef z.1)) ∧
    (∀ xRef x p : E, h xRef x = 0 →
      S xRef (x,p) = (x,p) ∧ rate xRef (x,p) = 0) ∧
    (∀ y xRef : E, ∀ z₀ : E × E,
      0 ≤ H y xRef z₀ ∧
      ∀ z : E × E, H y xRef z = H y xRef z₀ →
        ‖z.2‖ ≤ Real.sqrt (2 * H y xRef z₀) ∧
        ‖z.1 - c y xRef‖ ≤ Real.sqrt (2 * η * H y xRef z₀) ∧
        rate xRef z ≤ Real.sqrt η * (β : ℝ) *
          Real.sqrt (2 * H y xRef z₀) *
          (Real.sqrt (2 * η * H y xRef z₀) + ‖c y xRef - xRef‖))

#check actual_bounce_rate_energy_statement
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate
