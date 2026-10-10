import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
import Mathlib.MeasureTheory.MeasurableSpace.Constructions

/-! Prospective exact statement82 only; no theorem proof or admission.
PBPS arXiv2609.06905v1 AppendixA.1 Ex22 small-time continuity ingredient.
The actual phase/recurrence and all original six analytic conditions are literal.
The first-event defect probability and zero-time stochastic continuity are the
new obligations. Markov/restart/semigroup/invariance/L2 and main/cost remain open. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

private def actual_small_time_stochastic_continuity_statement
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


set_option maxHeartbeats 1600000 in
/-- Actual PBPS phase-flow defect probability and zero-time stochastic continuity.
This source prerequisite asserts no process Markov or full L2 semigroup result. -/
theorem actual_small_time_stochastic_continuity
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_small_time_stochastic_continuity_statement hα hαβ hV hH hη hβη := by
  classical
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
  obtain ⟨Z, hZM, hcovered, hfallback, hAE⟩ :=
    ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase
      hα hαβ hV hH hη hβη
  rcases ActualHazardClock.actual_integrated_hazard_clock_laws
    hα hαβ hV hH hη hβη with
    ⟨hΛC, _, _, hΛbasic, _, _, hτM, hW, _, _⟩
  have hflow := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hΦC := hflow.1
  have hΦ0 := hflow.2.2.1
  have hinput :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
  letI : IsProbabilityMeasure P := hinput.1
  refine ⟨Z, hZM, hcovered, hfallback, hAE, ?_⟩
  intro y xRef z₀
  have hZtM (t : ℝ≥0) : Measurable (Z y xRef z₀ t) := by
    have hargs : Measurable (fun sample : ℕ → ℝ => (((y, xRef), z₀), t, sample)) :=
      measurable_const.prodMk (measurable_const.prodMk measurable_id)
    have hc := hZM.comp hargs
    exact hc
  have hdefectM (t : ℝ≥0) :
      MeasurableSet {sample : ℕ → ℝ | Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} :=
    (measurableSet_eq_fun (hZtM t) measurable_const).compl
  let w : (ℕ → ℝ) → WithTop ℝ≥0 := fun sample => τ y xRef z₀ (ε sample 0)
  let g : ℝ → WithTop ℝ≥0 := fun e => τ y xRef z₀ (Real.toNNReal e)
  have hgM : Measurable g := by
    have hargs : Measurable (fun e : ℝ => ((y, xRef), z₀, Real.toNNReal e)) :=
      measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal)
    have hc := hτM.comp hargs
    exact hc
  have hwM : Measurable w := hgM.comp (measurable_pi_apply 0)
  have hwlaw : P.map w = (expMeasure (1 : ℝ)).map g := by
    calc
      P.map w = (P.map (fun sample : ℕ → ℝ => sample 0)).map g :=
        (Measure.map_map hgM (measurable_pi_apply 0)).symm
      _ = (expMeasure (1 : ℝ)).map g := by rw [(hinput.2.1 0).2.2]
  have hsurvival (t : ℝ≥0) :
      P.real {sample : ℕ → ℝ | (t : WithTop ℝ≥0) < w sample} =
        Real.exp (-Λ y xRef z₀ t) := by
    calc
      P.real {sample : ℕ → ℝ | (t : WithTop ℝ≥0) < w sample} =
          (P.map w).real (Set.Ioi (t : WithTop ℝ≥0)) :=
        (map_measureReal_apply hwM measurableSet_Ioi).symm
      _ = Real.exp (-Λ y xRef z₀ t) := by
        rw [hwlaw]
        exact (hW y xRef z₀).2 t
  have hfirst (sample : ℕ → ℝ) :
      eventTime y xRef z₀ (ε sample) 1 = w sample := by
    change (if τ y xRef z₀ (ε sample 0) = ⊤ then Sum.inr () else
      Sum.inl (0 + (τ y xRef z₀ (ε sample 0)).untopD 0,
        S xRef (Φ y xRef (((τ y xRef z₀ (ε sample 0)).untopD 0 : ℝ≥0) : ℝ) z₀))).elim
          (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤) = τ y xRef z₀ (ε sample 0)
    cases hc : τ y xRef z₀ (ε sample 0) using WithTop.recTopCoe with
    | top => simp only [if_pos rfl, Sum.elim_inr]
    | coe s => simp only [WithTop.coe_ne_top, if_false, WithTop.untopD_coe,
        zero_add, Sum.elim_inl]
  have hnoevent (t : ℝ≥0) (sample : ℕ → ℝ)
      (ht : (t : WithTop ℝ≥0) < w sample) :
      Z y xRef z₀ t sample = Φ y xRef (t : ℝ) z₀ := by
    have he := hcovered y xRef z₀ sample t 0 (0, z₀)
      (show eventTime y xRef z₀ (ε sample) 0 ≤ (t : WithTop ℝ≥0) from
        show (0 : WithTop ℝ≥0) ≤ (t : WithTop ℝ≥0) from bot_le)
      (by change (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) 1
          rw [hfirst sample]; exact ht) rfl
    simpa only [tsub_zero] using he
  have hbound (t : ℝ≥0) :
      P.real {sample : ℕ → ℝ | Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ≤
        1 - Real.exp (-Λ y xRef z₀ t) := by
    have hsub : {sample : ℕ → ℝ | Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ⊆
        {sample : ℕ → ℝ | (t : WithTop ℝ≥0) < w sample}ᶜ := by
      intro sample hs ht
      exact hs (hnoevent t sample ht)
    calc
      P.real {sample : ℕ → ℝ | Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ≤
          P.real {sample : ℕ → ℝ | (t : WithTop ℝ≥0) < w sample}ᶜ := measureReal_mono hsub
      _ = 1 - Real.exp (-Λ y xRef z₀ t) := by
        have hsM : MeasurableSet {sample : ℕ → ℝ | (t : WithTop ℝ≥0) < w sample} :=
          measurableSet_Ioi.preimage hwM
        rw [measureReal_compl hsM, probReal_univ, hsurvival]
  refine ⟨fun t => ⟨hdefectM t, hbound t⟩, ?_⟩
  intro δ hδ
  have htailM (t : ℝ≥0) :
      MeasurableSet {sample : ℕ → ℝ | δ ≤ ‖Z y xRef z₀ t sample - z₀‖} :=
    measurableSet_le measurable_const (((hZtM t).sub measurable_const).norm)
  refine ⟨htailM, ?_⟩
  have hφ : Continuous (fun t : ℝ≥0 => Φ y xRef (t : ℝ) z₀) := by
    have hc := hΦC.comp (continuous_const.prodMk (continuous_subtype_val.prodMk continuous_const))
    exact hc
  have hLambdaCont : Continuous (Λ y xRef z₀) := by
    have hc := hΛC.comp (continuous_const.prodMk continuous_id)
    exact hc
  have hnorm : Tendsto (fun t : ℝ≥0 => ‖Φ y xRef (t : ℝ) z₀ - z₀‖) (𝓝 0) (𝓝 0) := by
    have hc : Continuous (fun t : ℝ≥0 => ‖Φ y xRef (t : ℝ) z₀ - z₀‖) :=
      (hφ.sub continuous_const).norm
    simpa only [NNReal.coe_zero, hΦ0, sub_self, norm_zero] using
      hc.tendsto (0 : ℝ≥0)
  have hsmall : ∀ᶠ t : ℝ≥0 in 𝓝 0, ‖Φ y xRef (t : ℝ) z₀ - z₀‖ < δ :=
    (tendsto_order.1 hnorm).2 δ hδ
  have hbzero : Tendsto (fun t : ℝ≥0 => 1 - Real.exp (-Λ y xRef z₀ t))
      (𝓝 0) (𝓝 0) := by
    have he : Tendsto (fun t : ℝ≥0 => Real.exp (-Λ y xRef z₀ t)) (𝓝 0)
        (𝓝 (Real.exp (-Λ y xRef z₀ 0))) :=
      (Real.continuous_exp.tendsto _).comp ((hLambdaCont.tendsto 0).neg)
    simpa only [(hΛbasic y xRef z₀).1, neg_zero, Real.exp_zero, sub_self] using
      (show Tendsto (fun t : ℝ≥0 => 1 - Real.exp (-Λ y xRef z₀ t)) (𝓝 0)
        (𝓝 (1 - Real.exp (-Λ y xRef z₀ 0))) from tendsto_const_nhds.sub he)
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds hbzero
  · exact Filter.Eventually.of_forall fun _ => measureReal_nonneg
  · filter_upwards [hsmall] with t ht
    apply (measureReal_mono (show
      {sample : ℕ → ℝ | δ ≤ ‖Z y xRef z₀ t sample - z₀‖} ⊆
      {sample : ℕ → ℝ | Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} from ?_)).trans (hbound t)
    intro sample hs he
    change δ ≤ ‖Z y xRef z₀ t sample - z₀‖ at hs
    rw [he] at hs
    exact (not_le.mpr ht) hs

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity
