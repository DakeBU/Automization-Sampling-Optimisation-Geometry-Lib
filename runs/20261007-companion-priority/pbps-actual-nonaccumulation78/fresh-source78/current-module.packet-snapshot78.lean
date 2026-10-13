import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.Topology.Order.WithTop

/-! Prospective statement only, PBPS arXiv2609.06905v1 Appendix A.1 Ex9.
Source standing analytic conditions and exact stopped recurrence are retained.
Actual inputs use the canonical Exp(1) product. No supplied stochastic/cap/time
certificate and no global physical-time process, Markov or invariance claim. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

private def actual_fixed_reference_event_time_nonaccumulation_statement
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
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ sample ∂P,
      (∀ t : ℝ≥0, ∀ᶠ n : ℕ in atTop,
        (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) n) ∧
      (∀ t : ℝ≥0, {n : ℕ | eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0)}.Finite)


set_option maxHeartbeats 800000 in
theorem actual_fixed_reference_event_time_nonaccumulation
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_fixed_reference_event_time_nonaccumulation_statement hα hαβ hV hH hη hβη := by
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
          S xRef (Φ y xRef (((τ y xRef a.2 e).untopD 0 : ℝ≥0) : ℝ) a.2))
  let record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ →
      ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef z₀ e n =>
    Nat.rec (Sum.inl (0, z₀)) (fun k r => next y xRef (e k) r) n
  let eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ e n => (record y xRef z₀ e n).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  change ∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ sample ∂P,
    (∀ t : ℝ≥0, ∀ᶠ n : ℕ in atTop,
      (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) n) ∧
    (∀ t : ℝ≥0, {n : ℕ | eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0)}.Finite)
  -- Reuse the actual deterministic recurrence; no cap or recurrence is supplied.
  rcases ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
      hα hαβ hV hH hη hβη with
    ⟨hinit, _, _, _, _, htime, hstop, _, hcap, _⟩
  -- The good event supplies all positive thresholds and divergent actual sums.
  rcases AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws with
    ⟨_, _, _, hgood, hdiv⟩
  intro y xRef z₀
  filter_upwards [hgood, hdiv] with sample hpos hsum
  have hepos (k : ℕ) : 0 < ε sample k :=
    Real.toNNReal_pos.mpr (hpos k).1
  obtain ⟨hC, hinc, hzero⟩ := hcap y xRef z₀ (ε sample)
  have hescape : ∀ t : ℝ≥0, ∀ᶠ n : ℕ in atTop,
      (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) n := by
    -- Zero cap forces the first positive-threshold update to stop; it absorbs.
    by_cases hC0 : C y xRef z₀ = 0
    · have hfirst : record y xRef z₀ (ε sample) 1 = Sum.inr () :=
        hzero hC0 0 (0, z₀) (hinit y xRef z₀ (ε sample)) (hepos 0)
      intro t
      filter_upwards [eventually_ge_atTop (1 : ℕ)] with n hn
      obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hn
      have hs : record y xRef z₀ (ε sample) (1 + k) = Sum.inr () :=
        hstop y xRef z₀ (ε sample) 1 k hfirst
      change (t : WithTop ℝ≥0) < (record y xRef z₀ (ε sample) (1 + k)).elim _ _
      rw [hs]
      exact WithTop.coe_lt_top t
    -- Positive cap: inductively compare every actual clock with partial sums/C.
    · have hCp : 0 < C y xRef z₀ := lt_of_le_of_ne hC (Ne.symm hC0)
      let cap : ℝ≥0 := Real.toNNReal (C y xRef z₀)
      have hcapcoe : (cap : ℝ) = C y xRef z₀ := Real.coe_toNNReal _ hC
      have hcapPos : 0 < cap := Real.toNNReal_pos.mpr hCp
      have hbound (n : ℕ) :
          (((∑ k ∈ Finset.range n, ε sample k) / cap : ℝ≥0) : WithTop ℝ≥0) ≤
            eventTime y xRef z₀ (ε sample) n := by
        induction n with
        | zero => simpa using (htime y xRef z₀ (ε sample)).1.ge
        | succ n ih =>
          have hi := hinc hCp n
          have hterm : Real.toNNReal ((ε sample n : ℝ) / C y xRef z₀) =
              ε sample n / cap := by
            rw [Real.toNNReal_div (ε sample n).coe_nonneg, Real.toNNReal_coe]
          rw [hterm] at hi
          calc
            (((∑ k ∈ Finset.range (n + 1), ε sample k) / cap : ℝ≥0) : WithTop ℝ≥0)
                = (((∑ k ∈ Finset.range n, ε sample k) / cap : ℝ≥0) : WithTop ℝ≥0) +
                    ((ε sample n / cap : ℝ≥0) : WithTop ℝ≥0) := by
                      rw [Finset.sum_range_succ, add_div, WithTop.coe_add]
            _ ≤ eventTime y xRef z₀ (ε sample) n +
                    ((ε sample n / cap : ℝ≥0) : WithTop ℝ≥0) := add_le_add ih le_rfl
            _ ≤ eventTime y xRef z₀ (ε sample) (n + 1) := hi
      intro t
      have hs : ∀ᶠ n : ℕ in atTop,
          (t : ℝ) * C y xRef z₀ < ∑ k ∈ Finset.range n, (ε sample k : ℝ) :=
        hsum.eventually (eventually_gt_atTop ((t : ℝ) * C y xRef z₀))
      filter_upwards [hs] with n hn
      have ht : t < (∑ k ∈ Finset.range n, ε sample k) / cap := by
        apply (NNReal.coe_lt_coe).mp
        push_cast
        rw [hcapcoe]
        exact (lt_div_iff₀ hCp).mpr hn
      exact lt_of_lt_of_le (WithTop.coe_lt_coe.mpr ht) (hbound n)
  refine ⟨hescape, ?_⟩
  -- The bounded-horizon index set is contained in a finite initial interval.
  intro t
  obtain ⟨N, hN⟩ := eventually_atTop.mp (hescape t)
  apply (Set.finite_Iio N).subset
  intro n hn
  exact lt_of_not_ge (fun hge => (not_lt_of_ge hn) (hN n hge))

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation
