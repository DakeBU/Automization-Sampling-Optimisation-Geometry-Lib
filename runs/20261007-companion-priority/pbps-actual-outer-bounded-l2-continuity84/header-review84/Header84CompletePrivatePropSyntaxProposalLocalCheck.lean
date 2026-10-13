import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity
import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Prospective exact statement84 only; no theorem proof or admission.
PBPS arXiv2609.06905v1 AppendixA.1 Ex22 bounded-test outer square-integral ingredient.
All six original analytic conditions and the entire actual83 phase contract remain.
Exact conditional Gibbs x Gaussian probability normalization, state measurability,
square integrability, explicit4M2 domination and the outer zero-time limit are outputs.
The source uses C_c; C_b with an explicit global bound is an attributed ASTIS extension.
All-L2 AE operator/invariance/Jensen/contraction/density/Markov/main/cost remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

private def actual_outer_bounded_l2_continuity_statement
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
 ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        (∀ t : ℝ≥0,
          MeasurableSet {sample : ℕ → ℝ |
            Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ∧
          P.real {sample : ℕ → ℝ |
            Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ≤
              1 - Real.exp (-Λ y xRef z₀ t)) ∧
        (∀ δ : ℝ, 0 < δ →
          (∀ t : ℝ≥0, MeasurableSet {sample : ℕ → ℝ |
            δ ≤ ‖Z y xRef z₀ t sample - z₀‖}) ∧
          Tendsto (fun t : ℝ≥0 => P.real {sample : ℕ → ℝ |
            δ ≤ ‖Z y xRef z₀ t sample - z₀‖}) (𝓝 0) (𝓝 0)))

 ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        ∀ f : (E × E) → ℝ, Continuous f →
        ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |f z| ≤ M) →
          (∀ t : ℝ≥0,
            Measurable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) ∧
            Integrable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) P ∧
            |(∫ sample, f (Z y xRef z₀ t sample) ∂P) -
                f (Φ y xRef (t : ℝ) z₀)| ≤
              2 * M * (1 - Real.exp (-Λ y xRef z₀ t))) ∧
          Tendsto (fun t : ℝ≥0 => ∫ sample, f (Z y xRef z₀ t sample) ∂P)
            (𝓝 0) (𝓝 (f z₀)))


 ∧
      (let q : E → Measure E := fun y =>
         (volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))
       let ν : E → Measure (E × E) := fun y => (q y).prod (stdGaussian E)
       (∀ y : E, IsProbabilityMeasure (q y) ∧ IsProbabilityMeasure (ν y)) ∧
       (∀ y xRef : E, ∀ f : (E × E) → ℝ, Continuous f →
         ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |f z| ≤ M) →
           let A : ℝ≥0 → (E × E) → ℝ := fun t z₀ =>
             ∫ sample, f (Z y xRef z₀ t sample) ∂P
           (∀ t : ℝ≥0, Measurable (A t) ∧
             Integrable (fun z₀ : E × E => (A t z₀ - f z₀) ^ 2) (ν y) ∧
             (∀ z₀ : E × E, (A t z₀ - f z₀) ^ 2 ≤ 4 * M ^ 2)) ∧
           Tendsto (fun t : ℝ≥0 =>
             ∫ z₀, (A t z₀ - f z₀) ^ 2 ∂(ν y)) (𝓝 0) (𝓝 0)))

#check actual_outer_bounded_l2_continuity_statement
#check MeasureTheory.StronglyMeasurable.integral_prod_right
#check MeasureTheory.tendsto_integral_filter_of_dominated_convergence
#check MeasureTheory.isProbabilityMeasure_tilted
#check MeasureTheory.tilted_tilted
#check AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity
