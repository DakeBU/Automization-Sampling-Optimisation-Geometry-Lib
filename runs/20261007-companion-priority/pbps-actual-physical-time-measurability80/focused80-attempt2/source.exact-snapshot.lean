import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover
import Mathlib.MeasureTheory.MeasurableSpace.Constructions

/-! Prospective statement80 only. PBPS arXiv2609.06905v1 Appendix A.1.
ASTIS total measurable representative of literal actual harmonic interpolation.
Standing V/alpha/beta/eta are fixed; phase map is jointly Borel in finite
parameters, finite physical time and canonical threshold sample. Uncovered
points explicitly take initial phase; covered last-live infinite-wait arcs
are not fallback points. Per-parameter AE event is common to all finite times;
no uniform parameter event, random-initial law, Markov/invariance or main claim. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

private def actual_physical_time_measurable_phase_statement
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


set_option maxHeartbeats 1600000 in
theorem actual_physical_time_measurable_phase
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_physical_time_measurable_phase_statement hα hαβ hV hH hη hβη := by
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
  have h76 := ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  rcases h76 with ⟨hinit, _, _, hrecordM, htimeM, hmono, _, _, _, hstrict⟩
  have hflow := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hΦM : Measurable (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) := hflow.2.1
  have hΦ0 : ∀ y xRef : E, ∀ z : E × E, Φ y xRef 0 z = z := hflow.2.2.1
  have hεM : Measurable ε := measurable_pi_lambda _ fun n =>
    measurable_real_toNNReal.comp (measurable_pi_apply n)
  let A := ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ)
  let args : A → (E × E) × (E × E) × (ℕ → ℝ≥0) :=
    fun a => (a.1.1, a.1.2, ε a.2.2)
  have hargs : Measurable args := measurable_fst.fst.prodMk
    (measurable_fst.snd.prodMk (hεM.comp measurable_snd.snd))
  have hrM (n : ℕ) : Measurable (fun a : A =>
      record a.1.1.1 a.1.1.2 a.1.2 (ε a.2.2) n) := (hrecordM n).comp hargs
  have hTM (n : ℕ) : Measurable (fun a : A =>
      eventTime a.1.1.1 a.1.1.2 a.1.2 (ε a.2.2) n) := (htimeM n).comp hargs
  have htM : Measurable (fun a : A => (a.2.1 : WithTop ℝ≥0)) :=
    WithTop.measurable_coe.comp measurable_snd.fst
  let D : ℕ → Set A := fun n => {a |
    eventTime a.1.1.1 a.1.1.2 a.1.2 (ε a.2.2) n ≤ (a.2.1 : WithTop ℝ≥0) ∧
    (a.2.1 : WithTop ℝ≥0) < eventTime a.1.1.1 a.1.1.2 a.1.2 (ε a.2.2) (n + 1)}
  have hDM (n : ℕ) : MeasurableSet (D n) :=
    (measurableSet_le (hTM n) htM).inter (measurableSet_lt htM (hTM (n + 1)))
  have hdisj (n m : ℕ) (a : A) (hn : a ∈ D n) (hm : a ∈ D m) : n = m := by
    have hmon : Monotone (eventTime a.1.1.1 a.1.1.2 a.1.2 (ε a.2.2)) :=
      (hmono a.1.1.1 a.1.1.2 a.1.2 (ε a.2.2)).2
    rcases lt_trichotomy n m with hlt | heq | hgt
    · exact False.elim ((not_lt_of_ge hm.1) (hn.2.trans_le (hmon (Nat.succ_le_of_lt hlt))))
    · exact heq
    · exact False.elim ((not_lt_of_ge hn.1) (hm.2.trans_le (hmon (Nat.succ_le_of_lt hgt))))
  -- This total auxiliary projection is used only on D_n, where the record is live.
  -- Its zero branch never supplies a source phase for a stopped record.
  let L : ℕ → A → ℝ≥0 × (E × E) := fun n a =>
    (record a.1.1.1 a.1.1.2 a.1.2 (ε a.2.2) n).elim id (fun _ => (0, (0, 0)))
  have hLM (n : ℕ) : Measurable (L n) :=
    (measurable_id.sumElim measurable_const).comp (hrM n)
  let branch : ℕ → A → E × E := fun n a =>
    Φ a.1.1.1 a.1.1.2 ((a.2.1 - (L n a).1 : ℝ≥0) : ℝ) (L n a).2
  have hbM (n : ℕ) : Measurable (branch n) :=
    hΦM.comp (measurable_fst.fst.prodMk
      ((measurable_coe_nnreal_real.comp (measurable_snd.fst.sub (hLM n).fst)).prodMk
        (hLM n).snd))
  let sets : Option ℕ → Set A
    | none => (⋃ n, D n)ᶜ
    | some n => D n
  let values : Option ℕ → A → E × E
    | none => fun a => a.1.2
    | some n => branch n
  have hsM (i : Option ℕ) : MeasurableSet (sets i) := by
    cases i with
    | none => exact (MeasurableSet.iUnion hDM).compl
    | some n => exact hDM n
  have hvM (i : Option ℕ) : Measurable (values i) := by
    cases i with
    | none => exact measurable_fst.snd
    | some n => exact hbM n
  have hcompat : Pairwise (fun i j => Set.EqOn (values i) (values j) (sets i ∩ sets j)) := by
    intro i j hij a ha
    cases i with
    | none =>
      cases j with
      | none => exact False.elim (hij rfl)
      | some m => exact False.elim (ha.1 (Set.mem_iUnion.mpr ⟨m, ha.2⟩))
    | some n =>
      cases j with
      | none => exact False.elim (ha.2 (Set.mem_iUnion.mpr ⟨n, ha.1⟩))
      | some m => exact False.elim (hij (congrArg some (hdisj n m a ha.1 ha.2)))
  obtain ⟨f, hfM, hf⟩ := exists_measurable_piecewise sets hsM values hvM hcompat
  let Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E) :=
    fun y xRef z₀ t sample => f (((y, xRef), z₀), t, sample)
  have hZ (y xRef : E) (z₀ : E × E) (sample : ℕ → ℝ) (t : ℝ≥0)
      (n : ℕ) (a : ℝ≥0 × (E × E))
      (hl : eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0))
      (hu : (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1))
      (hr : record y xRef z₀ (ε sample) n = Sum.inl a) :
      Z y xRef z₀ t sample = Φ y xRef ((t - a.1 : ℝ≥0) : ℝ) a.2 := by
    have heq := hf (some n) (show (((y, xRef), z₀), t, sample) ∈ sets (some n) from ⟨hl, hu⟩)
    change f (((y, xRef), z₀), t, sample) = _
    rw [heq]
    dsimp [values, branch, L]
    rw [hr]
    rfl
  refine ⟨Z, hfM, hZ, ?_, ?_⟩
  · intro y xRef z₀ sample t hn
    exact hf none (show (((y, xRef), z₀), t, sample) ∈ sets none from by
      intro hx
      obtain ⟨n, hnD⟩ := Set.mem_iUnion.mp hx
      exact hn ⟨n, hnD⟩)
  · intro y xRef z₀
    have hc := ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover
      hα hαβ hV hH hη hβη y xRef z₀
    have hp := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.2.2.2.1
    filter_upwards [hc, hp] with sample hcover hpositive
    constructor
    · intro t
      obtain ⟨n, hn, huniq⟩ := hcover.1 t
      obtain ⟨a, ha, hau⟩ := hcover.2 t n hn.1 hn.2
      exact ⟨n, a, hn.1, hn.2, ha.1, ha.2.1, ha.2.2,
        hZ y xRef z₀ sample t n a hn.1 hn.2 ha.1⟩
    · have hi0 : record y xRef z₀ (ε sample) 0 = Sum.inl (0, z₀) :=
        hinit y xRef z₀ (ε sample)
      have hT0 : eventTime y xRef z₀ (ε sample) 0 = 0 :=
        (hmono y xRef z₀ (ε sample)).1
      have hepos : 0 < ε sample 0 := Real.toNNReal_pos.mpr (hpositive 0).1
      have hfirst : (0 : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) 1 := by
        cases hr1 : record y xRef z₀ (ε sample) 1 with
        | inr u =>
          change (0 : WithTop ℝ≥0) <
            (record y xRef z₀ (ε sample) 1).elim (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
          rw [hr1]
          exact WithTop.coe_lt_top (0 : ℝ≥0)
        | inl b =>
          have hbpos : 0 < b.1 :=
            (hstrict y xRef z₀ (ε sample) 0 (0, z₀) hi0).2 b hepos hr1
          change (0 : WithTop ℝ≥0) <
            (record y xRef z₀ (ε sample) 1).elim (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
          rw [hr1]
          exact WithTop.coe_lt_coe.mpr hbpos
      have heq := hZ y xRef z₀ sample 0 0 (0, z₀)
        (by rw [hT0]; rfl) hfirst hi0
      simpa only [tsub_zero, NNReal.coe_zero, hΦ0] using heq

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
