import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock

/-! Actual conditional survival: source-implicit live-guarded conditional survival.
The deterministic event depth is fixed. A Borel duration may depend on the
actual finite history, including its last live state/time, but not unused inputs.
Stopped histories contribute zero; no fictitious next state/wait is introduced.
The identity is unnormalized, including null history events.
No random-depth restart, physical-time memorylessness or full path-law claim. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival
open InnerProductSpace MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_conditional_next_wait_survival_statement
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
    let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
    let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun w k => Real.toNNReal (w k)
    let history : E → E → (E × E) → (n : ℕ) → (ℕ → ℝ) →
        (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) :=
      fun y xRef z₀ n w j => record y xRef z₀ (ε w) j.val
    let liveSurvival : E → E → ((ℝ≥0 × (E × E)) ⊕ Unit) → ℝ≥0 → ℝ → Prop :=
      fun y xRef r u e => match r with
        | Sum.inl a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)
        | Sum.inr _ => False
    let survivalWeight : E → E → ((ℝ≥0 × (E × E)) ⊕ Unit) → ℝ≥0 → ℝ≥0∞ :=
      fun y xRef r u => match r with
        | Sum.inl a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))
        | Sum.inr _ => 0
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      ∀ d : (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) → ℝ≥0,
      Measurable d →
      MeasurableSet {p : (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) × (ℕ → ℝ) |
        liveSurvival y xRef (p.1 ⟨n, Nat.lt_succ_self n⟩) (d p.1) (p.2 0)} ∧
      Measurable (fun h : Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit) =>
        survivalWeight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d h)) ∧
      (∀ h : Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit),
        survivalWeight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d h) ≤ 1) ∧
      (∀ A : Set (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)), MeasurableSet A →
        P {w : ℕ → ℝ | history y xRef z₀ n w ∈ A ∧
          liveSurvival y xRef (record y xRef z₀ (ε w) n)
            (d (history y xRef z₀ n w)) (w n)} =
        ∫⁻ h in A, survivalWeight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d h)
          ∂(Measure.map (history y xRef z₀ n) P))


set_option maxHeartbeats 1000000 in
/-- Conditional next-wait survival for the actual finite stopped history.
The duration is a Borel function of that entire history. No normalization or
strict positivity of the history event is required. -/
theorem actual_conditional_next_wait_survival
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_conditional_next_wait_survival_statement hα hαβ hV hH hη hβη := by
  classical
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
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun w k => Real.toNNReal (w k)
  let history : E → E → (E × E) → (n : ℕ) → (ℕ → ℝ) →
      (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) :=
    fun y xRef z₀ n w j => record y xRef z₀ (ε w) j.val
  let liveSurvival : E → E → ((ℝ≥0 × (E × E)) ⊕ Unit) → ℝ≥0 → ℝ → Prop :=
    fun y xRef r u e => match r with
      | Sum.inl a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)
      | Sum.inr _ => False
  let survivalWeight : E → E → ((ℝ≥0 × (E × E)) ⊕ Unit) → ℝ≥0 → ℝ≥0∞ :=
    fun y xRef r u => match r with
      | Sum.inl a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))
      | Sum.inr _ => 0
  change
  ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
    ∀ d : (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) → ℝ≥0,
    Measurable d →
    MeasurableSet {p : (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) × (ℕ → ℝ) |
      liveSurvival y xRef (p.1 ⟨n, Nat.lt_succ_self n⟩) (d p.1) (p.2 0)} ∧
    Measurable (fun h : Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit) =>
      survivalWeight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d h)) ∧
    (∀ h : Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit),
      survivalWeight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d h) ≤ 1) ∧
    (∀ A : Set (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)), MeasurableSet A →
      P {w : ℕ → ℝ | history y xRef z₀ n w ∈ A ∧
        liveSurvival y xRef (record y xRef z₀ (ε w) n)
          (d (history y xRef z₀ n w)) (w n)} =
      ∫⁻ h in A, survivalWeight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d h)
        ∂(Measure.map (history y xRef z₀ n) P))

  have hh := ActualHazardClock.actual_integrated_hazard_clock_laws hα hαβ hV hH hη hβη
  rcases hh with ⟨hΛc, hΛm, hInt, hΛpos, hcross, hfinite, hτm, hSurv, hcap, hfloor⟩
  have hτtyped : Measurable (fun a : (E × E) × (E × E) × ℝ≥0 =>
      τ a.1.1 a.1.2 a.2.1 a.2.2) := hτm
  have hΛtyped : Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) := hΛm
  have hi := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
  letI : IsProbabilityMeasure P := hi.1
  letI : IsProbabilityMeasure (expMeasure (1 : ℝ)) :=
    isProbabilityMeasure_expMeasure zero_lt_one
  intro y xRef z₀ n d hd
  let D := ((ℝ≥0 × (E × E)) ⊕ Unit)
  let Hist := Fin (n + 1) → D
  let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
  let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
  let Y : (ℕ → ℝ) → (ℕ → ℝ) := fun w k => w (n + k)
  have hp := ActualFiniteHistoryTailLaw.actual_finite_history_tail_law
    hα hαβ hV hH hη hβη y xRef z₀ n
  have hH : Measurable H := hp.1
  have hY : Measurable Y := hp.2.1
  have hjoint : Measure.map (fun w => (H w, Y w)) P =
      (Measure.map H P).prod P := hp.2.2.2.2.2.2.1
  -- A stopped record has no next wait. The following zero-valued observable
  -- is only used under a strict nonnegative-duration comparison, hence false.
  let waitObs : D × ℝ → WithTop ℝ≥0 := fun q => match q.1 with
    | Sum.inl a => τ y xRef a.2 (Real.toNNReal q.2)
    | Sum.inr _ => 0
  have hwait : Measurable waitObs := by
    let e := MeasurableEquiv.sumProdDistrib (ℝ≥0 × (E × E)) Unit ℝ
    have hl : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
        τ y xRef q.1.2 (Real.toNNReal q.2)) :=
      hτtyped.comp (f := fun q : (ℝ≥0 × (E × E)) × ℝ =>
        ((y, xRef), q.1.2, Real.toNNReal q.2))
        ((measurable_const : Measurable (fun _ : (ℝ≥0 × (E × E)) × ℝ =>
        (y, xRef))).prodMk (measurable_fst.snd.prodMk
          (measurable_real_toNNReal.comp measurable_snd)))
    have heq : waitObs = (Sum.elim
        (fun q : (ℝ≥0 × (E × E)) × ℝ => τ y xRef q.1.2 (Real.toNNReal q.2))
        (fun _ : Unit × ℝ => (0 : WithTop ℝ≥0))) ∘ e := by
      funext q
      rcases q with ⟨a | a, t⟩ <;> rfl
    rw [heq]
    exact (hl.sumElim (measurable_const : Measurable (fun _ : Unit × ℝ =>
      (0 : WithTop ℝ≥0)))).comp e.measurable
  have hwaitEq (r : D) (u : ℝ≥0) (e : ℝ) :
      liveSurvival y xRef r u e ↔ (u : WithTop ℝ≥0) < waitObs (r, e) := by
    cases r with
    | inl a => rfl
    | inr a =>
      simp only [liveSurvival, waitObs, false_iff]
      exact not_lt.mpr (WithTop.coe_le_coe.mpr (show (0 : ℝ≥0) ≤ u from zero_le))
  let B : Set (Hist × (ℕ → ℝ)) := {p |
    liveSurvival y xRef (p.1 last) (d p.1) (p.2 0)}
  have hB : MeasurableSet B := by
    have hm := measurableSet_lt (WithTop.measurable_coe.comp (hd.comp measurable_fst))
      (hwait.comp (f := fun p : Hist × (ℕ → ℝ) => (p.1 last, p.2 0))
        (((measurable_pi_apply last).comp measurable_fst).prodMk
        ((measurable_pi_apply 0).comp measurable_snd)))
    simpa only [B, hwaitEq, Function.comp_def] using hm
  -- Joint Borel hazard gives a Borel exponential weight, including dead records.
  let weightObs : D × ℝ≥0 → ℝ≥0∞ := fun q => match q.1 with
    | Sum.inl a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 q.2))
    | Sum.inr _ => 0
  have hweightObs : Measurable weightObs := by
    let e := MeasurableEquiv.sumProdDistrib (ℝ≥0 × (E × E)) Unit ℝ≥0
    have hl : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ≥0 =>
        ENNReal.ofReal (Real.exp (-Λ y xRef q.1.2 q.2))) := by
      exact (hΛtyped.comp (f := fun q : (ℝ≥0 × (E × E)) × ℝ≥0 =>
        (((y, xRef), q.1.2), q.2)) (((measurable_const : Measurable
        (fun _ : (ℝ≥0 × (E × E)) × ℝ≥0 => (y, xRef))).prodMk
          measurable_fst.snd).prodMk measurable_snd)).neg.exp.ennreal_ofReal
    have heq : weightObs = (Sum.elim
        (fun q : (ℝ≥0 × (E × E)) × ℝ≥0 =>
          ENNReal.ofReal (Real.exp (-Λ y xRef q.1.2 q.2)))
        (fun _ : Unit × ℝ≥0 => (0 : ℝ≥0∞))) ∘ e := by
      funext q
      rcases q with ⟨a | a, t⟩ <;> rfl
    rw [heq]
    exact (hl.sumElim (measurable_const : Measurable
      (fun _ : Unit × ℝ≥0 => (0 : ℝ≥0∞)))).comp e.measurable
  let weight : Hist → ℝ≥0∞ := fun h => survivalWeight y xRef (h last) (d h)
  have hw : Measurable weight :=
    hweightObs.comp ((measurable_pi_apply last).prodMk hd)
  have hbound (h : Hist) : weight h ≤ 1 := by
    change survivalWeight y xRef (h last) (d h) ≤ 1
    cases h last with
    | inr a => simp [survivalWeight]
    | inl a =>
      change ENNReal.ofReal (Real.exp (-Λ y xRef a.2 (d h))) ≤ 1
      exact ENNReal.ofReal_le_one.mpr
        (Real.exp_le_one_iff.mpr (neg_nonpos.mpr ((hΛpos y xRef a.2).2.1 (d h))))
  -- For every fixed live history, integrate only its independent next clock.
  have hfiber (h : Hist) : P {w : ℕ → ℝ |
      liveSurvival y xRef (h last) (d h) (w 0)} = weight h := by
    cases hr : h last with
    | inr a => simp [liveSurvival, weight, survivalWeight, hr]
    | inl a =>
      let z := a.2
      let f : ℝ → WithTop ℝ≥0 := fun e => τ y xRef z (Real.toNNReal e)
      have hf : Measurable f := hτtyped.comp (f := fun e : ℝ =>
        ((y, xRef), z, Real.toNNReal e))
        ((measurable_const : Measurable (fun _ : ℝ => (y, xRef))).prodMk
          ((measurable_const : Measurable (fun _ : ℝ => z)).prodMk
            measurable_real_toNNReal))
      have hs := hSurv y xRef z
      letI : IsProbabilityMeasure (Measure.map f (expMeasure (1 : ℝ))) := hs.1
      have ht : Measure.map f (expMeasure (1 : ℝ))
          (Set.Ioi ((d h : ℝ≥0) : WithTop ℝ≥0)) =
          ENNReal.ofReal (Real.exp (-Λ y xRef z (d h))) := by
        rw [← ofReal_measureReal, hs.2 (d h)]
      calc
        P {w : ℕ → ℝ | liveSurvival y xRef (Sum.inl a) (d h) (w 0)} =
            (Measure.map (fun w : ℕ → ℝ => w 0) P)
              (f ⁻¹' Set.Ioi ((d h : ℝ≥0) : WithTop ℝ≥0)) := by
          rw [Measure.map_apply (measurable_pi_apply 0)
            (measurableSet_Ioi.preimage hf)]
          simp only [liveSurvival, hr, f, z]
          rfl
        _ = (expMeasure (1 : ℝ)) (f ⁻¹' Set.Ioi ((d h : ℝ≥0) : WithTop ℝ≥0)) := by
          rw [(hi.2.1 0).2.2]
        _ = Measure.map f (expMeasure (1 : ℝ))
            (Set.Ioi ((d h : ℝ≥0) : WithTop ℝ≥0)) :=
          (Measure.map_apply hf measurableSet_Ioi).symm
        _ = weight h := by simpa only [weight, survivalWeight, hr, z] using ht
  refine ⟨hB, hw, hbound, ?_⟩
  intro A hA
  let C : Set (Hist × (ℕ → ℝ)) := {p | p.1 ∈ A ∧ p ∈ B}
  have hC : MeasurableSet C := (hA.preimage measurable_fst).inter hB
  calc
    P {w : ℕ → ℝ | H w ∈ A ∧ liveSurvival y xRef
        (record y xRef z₀ (ε w) n) (d (H w)) (w n)} =
        (Measure.map (fun w => (H w, Y w)) P) C := by
      rw [Measure.map_apply (hH.prodMk hY) hC]
      rfl
    _ = ((Measure.map H P).prod P) C := by rw [hjoint]
    _ = ∫⁻ h : Hist, P {w : ℕ → ℝ | (h, w) ∈ C} ∂Measure.map H P :=
      Measure.prod_apply hC
    _ = ∫⁻ h : Hist, A.indicator weight h ∂Measure.map H P := by
      apply lintegral_congr
      intro h
      by_cases ha : h ∈ A
      · simpa only [C, B, Set.mem_setOf_eq, ha, true_and,
          Set.indicator_of_mem ha] using hfiber h
      · simp only [C, Set.mem_setOf_eq, ha, false_and, Set.setOf_false,
          measure_empty, Set.indicator_of_notMem ha]
    _ = ∫⁻ h in A, survivalWeight y xRef (h last) (d h) ∂Measure.map H P :=
      lintegral_indicator hA weight

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival
