import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Probability.Process.HittingTime
import Mathlib.Probability.Distributions.Exponential
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order

/-! Prospective actual PBPS integrated hazard and first-clock statement only.
No source/header admission or theorem proof is supplied by this file. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock
open InnerProductSpace MeasureTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_integrated_hazard_clock_statement
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
    let W : E → E → (E × E) → Measure (WithTop ℝ≥0) := fun y xRef z =>
      Measure.map (fun e : ℝ => τ y xRef z (Real.toNNReal e))
        ProbabilityTheory.expMeasure1
    Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
    Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
    (∀ y xRef : E, ∀ z : E × E, ∀ t : ℝ≥0,
      IntervalIntegrable (fun s : ℝ => rate xRef (Φ y xRef s z)) volume 0 (t : ℝ)) ∧
    (∀ y xRef : E, ∀ z : E × E,
      Λ y xRef z 0 = 0 ∧ (∀ t : ℝ≥0, 0 ≤ Λ y xRef z t) ∧
      Monotone (Λ y xRef z)) ∧
    (∀ y xRef : E, ∀ z : E × E, ∀ e t : ℝ≥0,
      τ y xRef z e ≤ (t : WithTop ℝ≥0) ↔ (e : ℝ) ≤ Λ y xRef z t) ∧
    (∀ y xRef : E, ∀ z : E × E, ∀ e : ℝ≥0,
      (τ y xRef z e = ⊤ ↔ ∀ t : ℝ≥0, Λ y xRef z t < (e : ℝ)) ∧
      (τ y xRef z e ≠ ⊤ → Λ y xRef z (τ y xRef z e).untopA = (e : ℝ)) ∧
      (0 < e → (0 : WithTop ℝ≥0) < τ y xRef z e) ∧ τ y xRef z 0 = 0) ∧
    Measurable (fun a : (E × E) × (E × E) × ℝ≥0 =>
      τ a.1.1 a.1.2 a.2.1 a.2.2) ∧
    (∀ y xRef : E, ∀ z : E × E, IsProbabilityMeasure (W y xRef z) ∧
      ∀ t : ℝ≥0, (W y xRef z).real (Set.Ioi (t : WithTop ℝ≥0)) =
        Real.exp (-Λ y xRef z t)) ∧
    (∀ y xRef : E, ∀ z : E × E, 0 ≤ C y xRef z ∧
      ∀ t : ℝ≥0, Λ y xRef z t ≤ C y xRef z * (t : ℝ)) ∧
    (∀ y xRef : E, ∀ z : E × E, ∀ e : ℝ≥0,
      (0 < C y xRef z →
        (Real.toNNReal ((e : ℝ) / C y xRef z) : WithTop ℝ≥0) ≤ τ y xRef z e) ∧
      (C y xRef z = 0 → 0 < e → τ y xRef z e = ⊤))

theorem actual_integrated_hazard_clock_laws
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_integrated_hazard_clock_statement hα hαβ hV hH hη hβη := by
