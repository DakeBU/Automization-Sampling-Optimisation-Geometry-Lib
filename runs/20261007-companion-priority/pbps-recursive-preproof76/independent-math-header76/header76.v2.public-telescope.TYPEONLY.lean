import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock
import Mathlib.MeasureTheory.Constructions.BorelSpace.WithTop

/-! Prospective header76 only: actual finite stopped postjump recursion.
Active records are Sum.inl (finite time, phase); Sum.inr () means stopped,
has event time infinity and carries no phase at infinity. Threshold e n is
source E_(n+1). Zero thresholds are a deterministic extension; no global
physical-time phase or iid/nonexplosion/Markov/invariance is asserted. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
open InnerProductSpace MeasureTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_fixed_reference_finite_jump_recursion_statement
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
    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, z.2 - (2 * inner ℝ z.2 (gradient V z.1 - gradient V xRef) /
        ‖gradient V z.1 - gradient V xRef‖ ^ 2) • (gradient V z.1 - gradient V xRef))
    let rate : E → (E × E) → ℝ := fun xRef z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (gradient V z.1 - gradient V xRef))
    let H : E → E → (E × E) → ℝ := fun y xRef z =>
      (η⁻¹ * ‖z.1 - c y xRef‖ ^ 2 + ‖z.2‖ ^ 2) / 2
    let C : E → E → (E × E) → ℝ := fun y xRef z =>
      Real.sqrt η * (β : ℝ) * Real.sqrt (2 * H y xRef z) *
        (Real.sqrt (2 * η * H y xRef z) + ‖c y xRef - xRef‖)
    let Λ : E → E → (E × E) → ℝ≥0 → ℝ := fun y xRef z t =>
      ∫ s in (0 : ℝ)..(t : ℝ), rate xRef (Φ y xRef s z)
    let τ : E → E → (E × E) → ℝ≥0 → WithTop ℝ≥0 := fun y xRef z e =>
      MeasureTheory.hittingAfter
        (fun t : ℝ≥0 => fun a : (E × E) × (E × E) × ℝ≥0 =>
          Λ a.1.1 a.1.2 a.2.1 t - (a.2.2 : ℝ))
        (Set.Ici (0 : ℝ)) 0 ((y, xRef), z, e)
    let next : E → E → ℝ≥0 → ((ℝ≥0 × (E × E)) ⊕ Unit) →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef e r =>
      match r with
      | Sum.inr _ => Sum.inr ()
      | Sum.inl a =>
        if τ y xRef a.2 e = ⊤ then Sum.inr () else
          Sum.inl (a.1 + (τ y xRef a.2 e).untopD 0,
            S xRef (Φ y xRef ((τ y xRef a.2 e).untopD (0 : ℝ≥0) : ℝ) a.2))
    let record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef z₀ e n =>
      Nat.rec (Sum.inl (0, z₀)) (fun k r => next y xRef (e k) r) n
    let eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ e n => (record y xRef z₀ e n).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0,
      record y xRef z₀ e 0 = Sum.inl (0, z₀)) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n : ℕ,
      record y xRef z₀ e (n + 1) = next y xRef (e n) (record y xRef z₀ e n) ∧
      (∀ a : ℝ≥0 × (E × E), record y xRef z₀ e n = Sum.inl a →
        (record y xRef z₀ e (n + 1) = Sum.inr () ↔ τ y xRef a.2 (e n) = ⊤) ∧
        (τ y xRef a.2 (e n) ≠ ⊤ → record y xRef z₀ e (n + 1) =
          Sum.inl (a.1 + (τ y xRef a.2 (e n)).untopD 0,
            S xRef (Φ y xRef ((τ y xRef a.2 (e n)).untopD (0 : ℝ≥0) : ℝ) a.2))))) ∧
    Measurable (fun a : (E × E) × ℝ≥0 × ((ℝ≥0 × (E × E)) ⊕ Unit) =>
      next a.1.1 a.1.2 a.2.1 a.2.2) ∧
    (∀ n : ℕ, Measurable (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
      record a.1.1 a.1.2 a.2.1 a.2.2 n)) ∧
    (∀ n : ℕ, Measurable (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
      eventTime a.1.1 a.1.2 a.2.1 a.2.2 n)) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0,
      eventTime y xRef z₀ e 0 = 0 ∧ Monotone (eventTime y xRef z₀ e)) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n k : ℕ,
      record y xRef z₀ e n = Sum.inr () →
        record y xRef z₀ e (n + k) = Sum.inr ()) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n : ℕ,
      ∀ a : ℝ≥0 × (E × E), record y xRef z₀ e n = Sum.inl a →
        H y xRef a.2 = H y xRef z₀ ∧
        ∀ t : ℝ≥0, (t : WithTop ℝ≥0) < τ y xRef a.2 (e n) →
          H y xRef (Φ y xRef (t : ℝ) a.2) = H y xRef z₀ ∧
          0 ≤ rate xRef (Φ y xRef (t : ℝ) a.2) ∧
          rate xRef (Φ y xRef (t : ℝ) a.2) ≤ C y xRef z₀) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0,
      0 ≤ C y xRef z₀ ∧
      (0 < C y xRef z₀ → ∀ n : ℕ,
        eventTime y xRef z₀ e n +
          (Real.toNNReal ((e n : ℝ) / C y xRef z₀) : WithTop ℝ≥0) ≤
        eventTime y xRef z₀ e (n + 1)) ∧
      (C y xRef z₀ = 0 → ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E),
        record y xRef z₀ e n = Sum.inl a → 0 < e n →
          record y xRef z₀ e (n + 1) = Sum.inr ())) ∧
    (∀ y xRef : E, ∀ z₀ : E × E, ∀ e : ℕ → ℝ≥0, ∀ n : ℕ,
      ∀ a : ℝ≥0 × (E × E), record y xRef z₀ e n = Sum.inl a →
        (e n = 0 → record y xRef z₀ e (n + 1) = Sum.inl (a.1, S xRef a.2)) ∧
        (∀ b : ℝ≥0 × (E × E), 0 < e n →
          record y xRef z₀ e (n + 1) = Sum.inl b → a.1 < b.1))


-- TYPE ONLY: the exact proposed public telescope as a proposition, with no proof.
def independent_public_telescope_TYPEONLY : Prop :=
  ∀
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1),
    actual_fixed_reference_finite_jump_recursion_statement hα hαβ hV hH hη hβη

#print independent_public_telescope_TYPEONLY
#check WithTop.measurable_untopD
#check Measurable.sumElim
#check measurable_fun_sum
#check measurable_pi_apply
#check Measurable.ite

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
