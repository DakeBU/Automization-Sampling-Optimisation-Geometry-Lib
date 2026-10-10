import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
import Mathlib.Probability.Kernel.Composition.Prod
import Mathlib.Probability.Kernel.Composition.MapComap

/-! Prospective statement85 only. PBPS arXiv2609.06905v1 AppendixA.1 actual
transition laws and bounded measurable tests. ASTIS all-finite jointly indexed
probability-kernel packaging; the six original analytic conditions and eleven
literal algorithm definitions, actual iidExp1 P and full actual80 Z contract remain.
The SAME actual Z supplies every fiber law, zero-time Dirac initialization and
bounded Borel real-test integrability/expectation transfer. IsMarkovKernel means
probability fibers only, not process Markov/restart/Chapman-Kolmogorov.
Invariance/path-reversal/fullL2/hypocoercivity/implementation/cost/main remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

private def actual_phase_transition_kernel_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop :=
    let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
    let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun sample k => Real.toNNReal (sample k)
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
            S xRef (Φ y xRef (((τ y xRef a.2 e).untopD 0 : ℝ≥0) : ℝ) a.2))
    let record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef z₀ e n =>
      Nat.rec (Sum.inl (0, z₀)) (fun k r => next y xRef (e k) r) n
    let eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ e n => (record y xRef z₀ e n).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ sample : ℕ → ℝ, ∀ t : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E),
          eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) →
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1) →
          record y xRef z₀ (ε sample) n = Sum.inl a →
          Z y xRef z₀ t sample = Φ y xRef ((t - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ sample : ℕ → ℝ, ∀ t : ℝ≥0,
        (¬ ∃ n : ℕ, eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) ∧
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1)) →
          Z y xRef z₀ t sample = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ sample ∂P,
        (∀ t : ℝ≥0, ∃ n : ℕ, ∃ a : ℝ≥0 × (E × E),
          eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) ∧
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1) ∧
          record y xRef z₀ (ε sample) n = Sum.inl a ∧ a.1 ≤ t ∧
          ((t - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y xRef a.2 (ε sample n) ∧
          Z y xRef z₀ t sample = Φ y xRef ((t - a.1 : ℝ≥0) : ℝ) a.2) ∧
        Z y xRef z₀ 0 sample = z₀)
      ∧ (∃ K : Kernel (((E × E) × (E × E)) × ℝ≥0) (E × E),
        IsMarkovKernel K ∧
        (∀ y xRef : E, ∀ z₀ : E × E, ∀ t : ℝ≥0,
          K (((y, xRef), z₀), t) = Measure.map (Z y xRef z₀ t) P) ∧
        (∀ y xRef : E, ∀ z₀ : E × E, ∀ t : ℝ≥0,
          ∀ B : Set (E × E), MeasurableSet B →
            K (((y, xRef), z₀), t) B = P ((Z y xRef z₀ t) ⁻¹' B)) ∧
        (∀ y xRef : E, ∀ z₀ : E × E,
          K (((y, xRef), z₀), 0) = Measure.dirac z₀) ∧
        (∀ y xRef : E, ∀ z₀ : E × E, ∀ t : ℝ≥0,
          ∀ g : (E × E) → ℝ, Measurable g →
            ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |g z| ≤ M) →
              Integrable g (K (((y, xRef), z₀), t)) ∧
              Integrable (fun sample => g (Z y xRef z₀ t sample)) P ∧
              (∫ z, g z ∂K (((y, xRef), z₀), t)) =
                ∫ sample, g (Z y xRef z₀ t sample) ∂P))

#check actual_phase_transition_kernel_statement
#check ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase
#check AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
#check ProbabilityTheory.Kernel.id
#check ProbabilityTheory.Kernel.const
#check ProbabilityTheory.Kernel.prod
#check ProbabilityTheory.Kernel.id_prod_apply
#check ProbabilityTheory.Kernel.map_apply
#check MeasureTheory.Measure.map_apply
#check MeasureTheory.Measure.map_congr
#check MeasureTheory.integral_map
#check MeasureTheory.integrable_map_measure
#check MeasureTheory.Integrable.mono

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel
