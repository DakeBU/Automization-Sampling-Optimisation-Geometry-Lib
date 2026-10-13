import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.MeasurableSpace.Constructions

/-! Actual PBPS bounded-test expectation prerequisite, with its proof below.
PBPS arXiv2609.06905v1 AppendixA.1 Ex22 bounded-test expectation ingredient.
The actual phase/recurrence and all original six analytic conditions are literal.
Measurable/integrable bounded continuous tests, the2M expectation defect estimate
and zero-time expectation convergence are new obligations. Markov/restart/semigroup/invariance/L2 and main/cost remain open. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

private def actual_bounded_test_expectation_continuity_statement
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


set_option maxHeartbeats 1600000 in
/-- Actual PBPS bounded real tests are integrable; their clock expectations obey
the explicit2M first-event defect estimate and converge to the initial value.
This is the source Ex22 pointwise prerequisite, not its full L2 extension. -/
theorem actual_bounded_test_expectation_continuity
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_bounded_test_expectation_continuity_statement hα hαβ hV hH hη hβη := by
  classical
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let c : E → E → E := fun y xRef => y - η • gradient V xRef
  let Φ : E → E → ℝ → (E × E) → (E × E) := fun y xRef t z =>
    (c y xRef + Real.cos t • (z.1 - c y xRef) +
        (Real.sqrt η * Real.sin t) • z.2,
     (-Real.sin t / Real.sqrt η) • (z.1 - c y xRef) + Real.cos t • z.2)
  let rate : E → (E × E) → ℝ := fun xRef z =>
    Real.sqrt η * max 0 (inner ℝ z.2 (gradient V z.1 - gradient V xRef))
  let Λ : E → E → (E × E) → ℝ≥0 → ℝ := fun y xRef z t =>
    ∫ s in (0 : ℝ)..(t : ℝ), rate xRef (Φ y xRef s z)
  obtain ⟨Z, hZM, hcovered, hfallback, hAE, hshort⟩ :=
    ActualSmallTimeContinuity.actual_small_time_stochastic_continuity
      hα hαβ hV hH hη hβη
  have hclock := ActualHazardClock.actual_integrated_hazard_clock_laws
    hα hαβ hV hH hη hβη
  have hΛC := hclock.1
  have hΛbasic := hclock.2.2.2.1
  have hflow := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hΦC := hflow.1
  have hΦ0 := hflow.2.2.1
  have hinput :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
  let : IsProbabilityMeasure P := hinput.1
  refine ⟨Z, hZM, hcovered, hfallback, hAE, hshort, ?_⟩
  intro y xRef z₀ f hf M hM hbound
  have hZtM (t : ℝ≥0) : Measurable (Z y xRef z₀ t) := by
    have hargs : Measurable (fun sample : ℕ → ℝ => (((y, xRef), z₀), t, sample)) :=
      measurable_const.prodMk (measurable_const.prodMk measurable_id)
    exact hZM.comp hargs
  have hfM (t : ℝ≥0) : Measurable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) :=
    hf.measurable.comp (hZtM t)
  have hfi (t : ℝ≥0) : Integrable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) P := by
    apply Integrable.of_bound (hfM t).aestronglyMeasurable M
    exact Filter.Eventually.of_forall fun sample => by
      simpa only [Real.norm_eq_abs] using hbound (Z y xRef z₀ t sample)
  have hestimate (t : ℝ≥0) :
      |(∫ sample, f (Z y xRef z₀ t sample) ∂P) - f (Φ y xRef (t : ℝ) z₀)| ≤
        2 * M * (1 - Real.exp (-Λ y xRef z₀ t)) := by
    let D : Set (ℕ → ℝ) := {sample | Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀}
    have hDM : MeasurableSet D := ((hshort y xRef z₀).1 t).1
    have hbi : Integrable (D.indicator (fun _ : ℕ → ℝ => 2 * M)) P :=
      (integrable_const (2 * M)).indicator hDM
    have hpoint (sample : ℕ → ℝ) :
        ‖f (Z y xRef z₀ t sample) - f (Φ y xRef (t : ℝ) z₀)‖ ≤
          D.indicator (fun _ : ℕ → ℝ => 2 * M) sample := by
      by_cases hd : sample ∈ D
      · rw [Set.indicator_of_mem hd]
        calc
          ‖f (Z y xRef z₀ t sample) - f (Φ y xRef (t : ℝ) z₀)‖ ≤
              ‖f (Z y xRef z₀ t sample)‖ + ‖f (Φ y xRef (t : ℝ) z₀)‖ := norm_sub_le _ _
          _ ≤ M + M := add_le_add
            (by simpa only [Real.norm_eq_abs] using hbound (Z y xRef z₀ t sample))
            (by simpa only [Real.norm_eq_abs] using hbound (Φ y xRef (t : ℝ) z₀))
          _ = 2 * M := by ring
      · have he : Z y xRef z₀ t sample = Φ y xRef (t : ℝ) z₀ := not_ne_iff.mp hd
        simp only [Set.indicator_of_notMem hd, he, sub_self, norm_zero, le_refl]
    have hnorm := norm_integral_le_of_norm_le hbi (Filter.Eventually.of_forall hpoint)
    have hdiff : (∫ sample, f (Z y xRef z₀ t sample) - f (Φ y xRef (t : ℝ) z₀) ∂P) =
        (∫ sample, f (Z y xRef z₀ t sample) ∂P) - f (Φ y xRef (t : ℝ) z₀) := by
      rw [integral_sub (hfi t) (integrable_const _)]
      simp only [integral_const, probReal_univ, one_smul]
    calc
      |(∫ sample, f (Z y xRef z₀ t sample) ∂P) - f (Φ y xRef (t : ℝ) z₀)| =
          ‖∫ sample, f (Z y xRef z₀ t sample) - f (Φ y xRef (t : ℝ) z₀) ∂P‖ := by
        rw [hdiff, Real.norm_eq_abs]
      _ ≤ ∫ sample, D.indicator (fun _ : ℕ → ℝ => 2 * M) sample ∂P := hnorm
      _ = 2 * M * P.real D := by
        rw [integral_indicator_const _ hDM, smul_eq_mul, mul_comm]
      _ ≤ 2 * M * (1 - Real.exp (-Λ y xRef z₀ t)) :=
        mul_le_mul_of_nonneg_left (((hshort y xRef z₀).1 t).2) (by positivity)
  refine ⟨fun t => ⟨hfM t, hfi t, hestimate t⟩, ?_⟩
  have hφ : Continuous (fun t : ℝ≥0 => Φ y xRef (t : ℝ) z₀) := by
    have hargs : Continuous (fun t : ℝ≥0 => ((y, xRef), (t : ℝ), z₀)) :=
      continuous_const.prodMk (continuous_subtype_val.prodMk continuous_const)
    exact hΦC.comp hargs
  have hφlimit : Tendsto (fun t : ℝ≥0 => f (Φ y xRef (t : ℝ) z₀))
      (𝓝 0) (𝓝 (f z₀)) := by
    have hzero : Φ y xRef 0 z₀ = z₀ := hΦ0 y xRef z₀
    have hc : Continuous (fun t : ℝ≥0 => f (Φ y xRef (t : ℝ) z₀)) := hf.comp hφ
    simpa only [NNReal.coe_zero, hzero] using hc.tendsto (0 : ℝ≥0)
  have hLambdaCont : Continuous (Λ y xRef z₀) := by
    have hargs : Continuous (fun t : ℝ≥0 => (((y, xRef), z₀), t)) :=
      continuous_const.prodMk continuous_id
    exact hΛC.comp hargs
  have hbzero : Tendsto (fun t : ℝ≥0 => 1 - Real.exp (-Λ y xRef z₀ t))
      (𝓝 0) (𝓝 0) := by
    have hzero : Λ y xRef z₀ 0 = 0 := (hΛbasic y xRef z₀).1
    have he : Tendsto (fun t : ℝ≥0 => Real.exp (-Λ y xRef z₀ t)) (𝓝 0)
        (𝓝 (Real.exp (-Λ y xRef z₀ 0))) :=
      (Real.continuous_exp.tendsto _).comp ((hLambdaCont.tendsto 0).neg)
    simpa only [hzero, neg_zero, Real.exp_zero, sub_self] using
      (show Tendsto (fun t : ℝ≥0 => 1 - Real.exp (-Λ y xRef z₀ t)) (𝓝 0)
        (𝓝 (1 - Real.exp (-Λ y xRef z₀ 0))) from tendsto_const_nhds.sub he)
  have hscaled : Tendsto (fun t : ℝ≥0 => 2 * M * (1 - Real.exp (-Λ y xRef z₀ t)))
      (𝓝 0) (𝓝 0) := by
    simpa only [mul_zero] using
      (show Tendsto (fun _ : ℝ≥0 => 2 * M) (𝓝 0) (𝓝 (2 * M)) from
        tendsto_const_nhds).mul hbzero
  have habs : Tendsto (fun t : ℝ≥0 =>
      |(∫ sample, f (Z y xRef z₀ t sample) ∂P) - f (Φ y xRef (t : ℝ) z₀)|)
      (𝓝 0) (𝓝 0) :=
    tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hscaled
      (fun _ => abs_nonneg _) hestimate
  have hdiffzero : Tendsto (fun t : ℝ≥0 =>
      (∫ sample, f (Z y xRef z₀ t sample) ∂P) - f (Φ y xRef (t : ℝ) z₀))
      (𝓝 0) (𝓝 0) := by
    apply tendsto_zero_iff_norm_tendsto_zero.mpr
    simpa only [Real.norm_eq_abs] using habs
  simpa only [sub_add_cancel, zero_add] using hdiffzero.add hφlimit

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity
