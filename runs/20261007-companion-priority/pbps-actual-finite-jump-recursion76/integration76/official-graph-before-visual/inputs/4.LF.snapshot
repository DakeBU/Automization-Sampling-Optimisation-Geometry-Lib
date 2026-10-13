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
        (ProbabilityTheory.expMeasure (1 : ℝ))
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

set_option maxHeartbeats 800000 in
private theorem actual_hazard_primitive_laws
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
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
    Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
    Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
    (∀ y xRef : E, ∀ z : E × E, ∀ t : ℝ≥0,
      IntervalIntegrable (fun s : ℝ => rate xRef (Φ y xRef s z)) volume 0 (t : ℝ)) ∧
    (∀ y xRef : E, ∀ z : E × E,
      Λ y xRef z 0 = 0 ∧ (∀ t : ℝ≥0, 0 ≤ Λ y xRef z t) ∧
      Monotone (Λ y xRef z)) ∧
    (∀ y xRef : E, ∀ z : E × E, 0 ≤ C y xRef z ∧
      ∀ t : ℝ≥0, Λ y xRef z t ≤ C y xRef z * (t : ℝ)) := by
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
  change
    Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
    Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
    (∀ y xRef : E, ∀ z : E × E, ∀ t : ℝ≥0,
      IntervalIntegrable (fun s : ℝ => rate xRef (Φ y xRef s z)) volume 0 (t : ℝ)) ∧
    (∀ y xRef : E, ∀ z : E × E,
      Λ y xRef z 0 = 0 ∧ (∀ t : ℝ≥0, 0 ≤ Λ y xRef z t) ∧
      Monotone (Λ y xRef z)) ∧
    (∀ y xRef : E, ∀ z : E × E, 0 ≤ C y xRef z ∧
      ∀ t : ℝ≥0, Λ y xRef z t ≤ C y xRef z * (t : ℝ))

  have hf := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hb := ActualBounceRate.actual_bounce_rate_energy_laws hα hαβ hV hH hη hβη
  have hΦ : Continuous (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) := hf.1
  have hrate : Continuous (fun a : E × (E × E) => rate a.1 a.2) := hb.2.1
  have hrate0 (xRef : E) (z : E × E) : 0 ≤ rate xRef z :=
    (hb.2.2.2.2.2.2.2.1 xRef z).1
  have henergy (y xRef : E) (s : ℝ) (z : E × E) :
      H y xRef (Φ y xRef s z) = H y xRef z := hf.2.2.2.2.2.2.2.1 y xRef s z
  have hcap (y xRef : E) (z : E × E) (s : ℝ) :
      rate xRef (Φ y xRef s z) ≤ C y xRef z :=
    (hb.2.2.2.2.2.2.2.2.2 y xRef z).2 (Φ y xRef s z) (henergy y xRef s z) |>.2.2
  have hC (y xRef : E) (z : E × E) : 0 ≤ C y xRef z := by
    dsimp [C]
    positivity
  have hF : Continuous (fun a : ((E × E) × (E × E)) × ℝ =>
      rate a.1.1.2 (Φ a.1.1.1 a.1.1.2 a.2 a.1.2)) := by
    exact hrate.comp (continuous_fst.fst.snd.prodMk
      (hΦ.comp ((continuous_fst.fst).prodMk
        (continuous_snd.prodMk continuous_fst.snd))))
  have hΛ : Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) := by
    exact (intervalIntegral.continuous_parametric_primitive_of_continuous
      (f := fun (q : (E × E) × (E × E)) (s : ℝ) =>
        rate q.1.2 (Φ q.1.1 q.1.2 s q.2)) (μ := volume) (a₀ := 0) hF).comp
      (continuous_fst.prodMk (NNReal.continuous_coe.comp continuous_snd))
  have hInt (y xRef : E) (z : E × E) (a b : ℝ) :
      IntervalIntegrable (fun s : ℝ => rate xRef (Φ y xRef s z)) volume a b := by
    have hsΦ : Continuous (fun s : ℝ => Φ y xRef s z) := by
      dsimp [Φ]
      fun_prop
    have hc : Continuous (fun s : ℝ => rate xRef (Φ y xRef s z)) :=
      hrate.comp (continuous_const.prodMk hsΦ)
    exact hc.intervalIntegrable a b
  have hbasic (y xRef : E) (z : E × E) :
      Λ y xRef z 0 = 0 ∧ (∀ t : ℝ≥0, 0 ≤ Λ y xRef z t) ∧
      Monotone (Λ y xRef z) := by
    refine ⟨by simp [Λ], ?_, ?_⟩
    · intro t
      exact intervalIntegral.integral_nonneg_of_forall t.coe_nonneg
        (fun s => hrate0 xRef (Φ y xRef s z))
    · intro s t hst
      exact intervalIntegral.integral_mono_interval (le_refl 0) s.coe_nonneg
        (show (s : ℝ) ≤ t from hst)
        (Filter.Eventually.of_forall (fun u => hrate0 xRef (Φ y xRef u z)))
        (hInt y xRef z 0 t)
  have hbound (y xRef : E) (z : E × E) (t : ℝ≥0) :
      Λ y xRef z t ≤ C y xRef z * (t : ℝ) := by
    have hi := intervalIntegral.integral_mono_on t.coe_nonneg
      (hInt y xRef z 0 t) (intervalIntegrable_const (μ := volume))
      (fun s _ => hcap y xRef z s)
    simpa only [intervalIntegral.integral_const, sub_zero, smul_eq_mul, mul_comm] using hi
  exact ⟨hΛ, hΛ.measurable, fun y xRef z t => hInt y xRef z 0 t,
    hbasic, fun y xRef z => ⟨hC y xRef z, hbound y xRef z⟩⟩

set_option maxHeartbeats 1200000 in
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
      (ProbabilityTheory.expMeasure (1 : ℝ))
  change
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
  classical
  have hp :
      Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
        Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
        Λ a.1.1.1 a.1.1.2 a.1.2 a.2) ∧
      (∀ y xRef : E, ∀ z : E × E, ∀ t : ℝ≥0,
        IntervalIntegrable (fun s : ℝ => rate xRef (Φ y xRef s z)) volume 0 (t : ℝ)) ∧
      (∀ y xRef : E, ∀ z : E × E,
        Λ y xRef z 0 = 0 ∧ (∀ t : ℝ≥0, 0 ≤ Λ y xRef z t) ∧
        Monotone (Λ y xRef z)) ∧
      (∀ y xRef : E, ∀ z : E × E, 0 ≤ C y xRef z ∧
        ∀ t : ℝ≥0, Λ y xRef z t ≤ C y xRef z * (t : ℝ)) :=
    actual_hazard_primitive_laws hα hαβ hV hH hη hβη
  rcases hp with ⟨hΛ, hΛmeas, hInt, hbasic, hcaps⟩
  have hcont (y xRef : E) (z : E × E) : Continuous (Λ y xRef z) :=
    hΛ.comp (show Continuous (fun t : ℝ≥0 => (((y, xRef), z), t)) from
      continuous_const.prodMk continuous_id)
  have hτle (y xRef : E) (z : E × E) (e t : ℝ≥0) :
      τ y xRef z e ≤ (t : WithTop ℝ≥0) ↔ (e : ℝ) ≤ Λ y xRef z t := by
    dsimp only [τ, MeasureTheory.hittingAfter]
    simp only [Set.mem_Ici, sub_nonneg, zero_le, true_and]
    split_ifs with hex
    · simp only [WithTop.coe_le_coe]
      constructor
      · intro h
        have hc : IsClosed {s : ℝ≥0 | (e : ℝ) ≤ Λ y xRef z s} :=
          isClosed_le continuous_const (hcont y xRef z)
        exact (hc.csInf_mem hex (OrderBot.bddBelow _)).trans
          ((hbasic y xRef z).2.2 h)
      · intro he
        exact csInf_le (OrderBot.bddBelow _) he
    · constructor
      · intro h
        exact False.elim (WithTop.not_top_le_coe t h)
      · intro he
        exact False.elim (hex ⟨t, he⟩)
  have hτtop (y xRef : E) (z : E × E) (e : ℝ≥0) :
      τ y xRef z e = ⊤ ↔ ∀ t : ℝ≥0, Λ y xRef z t < (e : ℝ) := by
    simp only [τ, MeasureTheory.hittingAfter_eq_top_iff, Set.mem_Ici,
      sub_nonneg, zero_le, true_implies, not_le]
  have hfinite (y xRef : E) (z : E × E) (e : ℝ≥0)
      (hn : τ y xRef z e ≠ ⊤) :
      Λ y xRef z (τ y xRef z e).untopA = (e : ℝ) := by
    let q : ℝ≥0 := (τ y xRef z e).untop hn
    have hq : (q : WithTop ℝ≥0) = τ y xRef z e := WithTop.coe_untop _ _
    have hge : (e : ℝ) ≤ Λ y xRef z q :=
      (hτle y xRef z e q).1 hq.symm.le
    have hval : Λ y xRef z q = (e : ℝ) := by
      apply le_antisymm _ hge
      by_contra h
      have hstrict : (e : ℝ) < Λ y xRef z q := not_le.mp h
      obtain ⟨s, hs, hse⟩ := intermediate_value_Icc (show (0 : ℝ≥0) ≤ q from bot_le)
        (hcont y xRef z).continuousOn
        (show (e : ℝ) ∈ Set.Icc (Λ y xRef z 0) (Λ y xRef z q) from
          ⟨by simpa only [(hbasic y xRef z).1] using e.coe_nonneg, hge⟩)
      have hsq : s < q := by
        by_contra hnot
        have heq : q = s := le_antisymm (not_lt.mp hnot) hs.2
        have hbad : Λ y xRef z q = (e : ℝ) := by simpa only [heq] using hse
        linarith
      have hqs : q ≤ s := by
        exact_mod_cast hq.le.trans ((hτle y xRef z e s).2 hse.ge)
      exact not_le_of_gt hsq hqs
    simpa only [WithTop.untopA_eq_untop hn] using hval
  have hpositive (y xRef : E) (z : E × E) (e : ℝ≥0) (he : 0 < e) :
      (0 : WithTop ℝ≥0) < τ y xRef z e := by
    apply lt_of_not_ge
    intro h
    have hh : (e : ℝ) ≤ 0 := by
      simpa only [(hbasic y xRef z).1] using (hτle y xRef z e 0).1 h
    exact not_le_of_gt (show (0 : ℝ) < e from he) hh
  have hzero (y xRef : E) (z : E × E) : τ y xRef z 0 = 0 := by
    apply le_antisymm _ bot_le
    exact (hτle y xRef z 0 0).2 (by
      simpa only [NNReal.coe_zero, (hbasic y xRef z).1] using (le_refl (0 : ℝ)))
  have hτmeas : Measurable (fun a : (E × E) × (E × E) × ℝ≥0 =>
      τ a.1.1 a.1.2 a.2.1 a.2.2) := by
    apply measurable_of_Iic
    intro b
    induction b using WithTop.recTopCoe with
    | top => simpa using MeasurableSet.univ
    | coe t =>
      have hevent : (fun a : (E × E) × (E × E) × ℝ≥0 =>
          τ a.1.1 a.1.2 a.2.1 a.2.2) ⁻¹' Set.Iic (t : WithTop ℝ≥0) =
          {a | (a.2.2 : ℝ) ≤ Λ a.1.1 a.1.2 a.2.1 t} := by
        ext a
        exact hτle a.1.1 a.1.2 a.2.1 a.2.2 t
      rw [hevent]
      exact measurableSet_le (measurable_coe_nnreal_real.comp measurable_snd.snd)
        (hΛmeas.comp ((measurable_fst.prodMk measurable_snd.fst).prodMk measurable_const))
  have hlaw (y xRef : E) (z : E × E) : IsProbabilityMeasure (W y xRef z) ∧
      ∀ t : ℝ≥0, (W y xRef z).real (Set.Ioi (t : WithTop ℝ≥0)) =
        Real.exp (-Λ y xRef z t) := by
    letI : IsProbabilityMeasure (ProbabilityTheory.expMeasure (1 : ℝ)) :=
      ProbabilityTheory.isProbabilityMeasure_expMeasure zero_lt_one
    have hi : Measurable (fun e : ℝ => ((y, xRef), z, Real.toNNReal e)) :=
      measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal)
    have ht0 := hτmeas.comp hi
    have ht : Measurable (fun e : ℝ => τ y xRef z (Real.toNNReal e)) := ht0
    refine ⟨Measure.isProbabilityMeasure_map ht.aemeasurable, ?_⟩
    intro t
    have hpre : (fun e : ℝ => τ y xRef z (Real.toNNReal e)) ⁻¹'
        Set.Ioi (t : WithTop ℝ≥0) = Set.Ioi (Λ y xRef z t) := by
      ext e
      change (t : WithTop ℝ≥0) < τ y xRef z (Real.toNNReal e) ↔ Λ y xRef z t < e
      rw [← not_le, hτle, not_le]
      simp only [Real.coe_toNNReal', lt_max_iff,
        not_lt.mpr ((hbasic y xRef z).2.1 t), or_false]
    change ((ProbabilityTheory.expMeasure (1 : ℝ)).map
      (fun e : ℝ => τ y xRef z (Real.toNNReal e))
      (Set.Ioi (t : WithTop ℝ≥0))).toReal = _
    rw [Measure.map_apply ht measurableSet_Ioi, hpre]
    change (ProbabilityTheory.expMeasure (1 : ℝ)).real (Set.Ioi (Λ y xRef z t)) = _
    rw [← Set.compl_Iic, measureReal_compl measurableSet_Iic, probReal_univ,
      ← ProbabilityTheory.cdf_eq_real, ProbabilityTheory.cdf_expMeasure_eq zero_lt_one]
    simp only [if_pos ((hbasic y xRef z).2.1 t), one_mul]
    ring
  have hwait (y xRef : E) (z : E × E) (e : ℝ≥0) :
      (0 < C y xRef z →
        (Real.toNNReal ((e : ℝ) / C y xRef z) : WithTop ℝ≥0) ≤ τ y xRef z e) ∧
      (C y xRef z = 0 → 0 < e → τ y xRef z e = ⊤) := by
    constructor
    · intro hC
      by_cases hn : τ y xRef z e = ⊤
      · simp only [hn, le_top]
      · let q : ℝ≥0 := (τ y xRef z e).untop hn
        have hq : (q : WithTop ℝ≥0) = τ y xRef z e := WithTop.coe_untop _ _
        have hval : Λ y xRef z q = (e : ℝ) := by
          simpa only [WithTop.untopA_eq_untop hn] using hfinite y xRef z e hn
        have hb : (e : ℝ) ≤ C y xRef z * (q : ℝ) :=
          hval ▸ (hcaps y xRef z).2 q
        have hdiv : (e : ℝ) / C y xRef z ≤ (q : ℝ) :=
          (div_le_iff₀ hC).2 (by simpa only [mul_comm] using hb)
        exact (WithTop.coe_le_coe.mpr (Real.toNNReal_le_iff_le_coe.mpr hdiv)).trans_eq hq
    · intro hC he
      apply (hτtop y xRef z e).2
      intro t
      have hb : Λ y xRef z t ≤ 0 := by simpa only [hC, zero_mul] using (hcaps y xRef z).2 t
      exact hb.trans_lt (show (0 : ℝ) < e from he)
  exact ⟨hΛ, hΛmeas, hInt, hbasic, hτle,
    fun y xRef z e => ⟨hτtop y xRef z e, hfinite y xRef z e,
      hpositive y xRef z e, hzero y xRef z⟩, hτmeas, hlaw, hcaps, hwait⟩

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock
