import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension
import Mathlib.MeasureTheory.Group.Prod

/-! Prospective statement only: actual next absolute event-time density.
Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1
(A.1),(A.2), one ordered-coordinate ingredient of (A.7), and Appendix A.2.
The actual time observer reads the next literal stopped/live record.
Only strict finite events a(H_n)<U<b(H_n) are represented by this density.
The stopped time0 and negative auxiliary flow are totalizations, not events.
Ordered iteration, final survival, full (A.7) and restart remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime
open InnerProductSpace MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_absolute_next_event_time_statement
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
    let waitObs : E → E → (((ℝ≥0 × (E × E)) ⊕ Unit) × ℝ) → WithTop ℝ≥0 :=
      fun y xRef q => match q.1 with
        | Sum.inl a => τ y xRef a.2 (Real.toNNReal q.2)
        | Sum.inr _ => 0
    let timeObs : E → E → (((ℝ≥0 × (E × E)) ⊕ Unit) × ℝ) → ℝ :=
      fun y xRef q => ((waitObs y xRef q).untopD 0 : ℝ≥0)
    let density : E → E → (((ℝ≥0 × (E × E)) ⊕ Unit) × ℝ) → ℝ≥0∞ :=
      fun y xRef q => match q.1 with
        | Sum.inl a => ENNReal.ofReal (rate xRef (Φ y xRef q.2 a.2) *
            Real.exp (-Λ y xRef a.2 (Real.toNNReal q.2)))
        | Sum.inr _ => 0
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
      let Hist := Fin (n + 1) → Rec
      let HistNext := Fin (n + 2) → Rec
      let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
      let lastNext : Fin (n + 2) := ⟨n + 1, Nat.lt_succ_self (n + 1)⟩
      let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
      let Hnext : (ℕ → ℝ) → HistNext := history y xRef z₀ (n + 1)
      let readTime : Rec → ℝ := fun r => match r with
        | Sum.inl q => (q.1 : ℝ)
        | Sum.inr _ => 0
      let a : Hist → ℝ := fun h => readTime (h last)
      let U : (ℕ → ℝ) → ℝ := fun w => readTime (Hnext w lastNext)
      let appendRel : Hist × ℝ → HistNext := fun p =>
        Fin.snoc p.1 (match p.1 last with
          | Sum.inl q => Sum.inl (q.1 + Real.toNNReal p.2,
              S xRef (Φ y xRef p.2 q.2))
          | Sum.inr _ => Sum.inr ())
      let appendAbs : Hist × ℝ → HistNext := fun p => appendRel (p.1, p.2 - a p.1)
      let liftAbs : Hist × ℝ → HistNext × ℝ := fun p => (appendAbs p, p.2)
      Measurable H ∧ Measurable Hnext ∧ Measurable a ∧ Measurable U ∧
      Measurable appendAbs ∧ Measurable liftAbs ∧
      (∀ p : Hist × ℝ, ∀ j : Fin (n + 1), appendAbs p j.castSucc = p.1 j) ∧
      (∀ b : Hist → ℝ≥0, Measurable b →
        let d : Hist → ℝ≥0 := fun h => Real.toNNReal ((b h : ℝ) - a h)
        let μ : Measure Hist := Measure.map H P
        let D : Hist → ℝ → ℝ≥0∞ := fun h u =>
          if a h < u ∧ u < (b h : ℝ) then density y xRef (h last, u - a h) else 0
        let Brel : Set (ℕ → ℝ) := {w |
          (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
          waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
            ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
        let B : Set (ℕ → ℝ) := {w |
          (∃ q, H w last = Sum.inl q) ∧
          (∃ q, Hnext w lastNext = Sum.inl q) ∧
          a (H w) < U w ∧ U w < (b (H w) : ℝ)}
        let X : (ℕ → ℝ) → Hist × ℝ := fun w => (H w, U w)
        let Y : (ℕ → ℝ) → HistNext × ℝ := fun w => (Hnext w, U w)
        let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
          (fun p => D p.1 p.2)
        Measurable (Function.uncurry D) ∧
        (∀ h : Hist, (∫⁻ u : ℝ, D h u) ≤ 1) ∧
        MeasurableSet B ∧ Measurable X ∧ Measurable Y ∧ Brel = B ∧
        (∀ w ∈ B, U w = a (H w) +
          timeObs y xRef (record y xRef z₀ (ε w) n, w n)) ∧
        (∀ w ∈ B, Hnext w = appendAbs (X w)) ∧
        Measure.map X (P.restrict B) = ν ∧
        Measure.map Y (P.restrict B) = Measure.map liftAbs ν ∧
        Measure.map Hnext (P.restrict B) = Measure.map appendAbs ν ∧
        ν Set.univ ≤ 1 ∧
        (∀ G : Hist × ℝ → ℝ≥0∞, Measurable G →
          Measurable (fun h => ∫⁻ u : ℝ, G (h, u) * D h u) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, G (X w) ∂P) =
              ∫⁻ h in A, (∫⁻ u : ℝ, G (h, u) * D h u) ∂μ)) ∧
        (∀ F : HistNext × ℝ → ℝ≥0∞, Measurable F →
          Measurable (fun h => ∫⁻ u : ℝ, F (liftAbs (h, u)) * D h u) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, F (Y w) ∂P) =
              ∫⁻ h in A, (∫⁻ u : ℝ, F (liftAbs (h, u)) * D h u) ∂μ)))

set_option maxHeartbeats 2400000 in
theorem actual_absolute_next_event_time_law
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_absolute_next_event_time_statement hα hαβ hV hH hη hβη := by
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
  let waitObs : E → E → (((ℝ≥0 × (E × E)) ⊕ Unit) × ℝ) → WithTop ℝ≥0 :=
    fun y xRef q => match q.1 with
      | Sum.inl a => τ y xRef a.2 (Real.toNNReal q.2)
      | Sum.inr _ => 0
  let timeObs : E → E → (((ℝ≥0 × (E × E)) ⊕ Unit) × ℝ) → ℝ :=
    fun y xRef q => ((waitObs y xRef q).untopD 0 : ℝ≥0)
  let density : E → E → (((ℝ≥0 × (E × E)) ⊕ Unit) × ℝ) → ℝ≥0∞ :=
    fun y xRef q => match q.1 with
      | Sum.inl a => ENNReal.ofReal (rate xRef (Φ y xRef q.2 a.2) *
          Real.exp (-Λ y xRef a.2 (Real.toNNReal q.2)))
      | Sum.inr _ => 0
  change
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
      let Hist := Fin (n + 1) → Rec
      let HistNext := Fin (n + 2) → Rec
      let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
      let lastNext : Fin (n + 2) := ⟨n + 1, Nat.lt_succ_self (n + 1)⟩
      let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
      let Hnext : (ℕ → ℝ) → HistNext := history y xRef z₀ (n + 1)
      let readTime : Rec → ℝ := fun r => match r with
        | Sum.inl q => (q.1 : ℝ)
        | Sum.inr _ => 0
      let a : Hist → ℝ := fun h => readTime (h last)
      let U : (ℕ → ℝ) → ℝ := fun w => readTime (Hnext w lastNext)
      let appendRel : Hist × ℝ → HistNext := fun p =>
        Fin.snoc p.1 (match p.1 last with
          | Sum.inl q => Sum.inl (q.1 + Real.toNNReal p.2,
              S xRef (Φ y xRef p.2 q.2))
          | Sum.inr _ => Sum.inr ())
      let appendAbs : Hist × ℝ → HistNext := fun p => appendRel (p.1, p.2 - a p.1)
      let liftAbs : Hist × ℝ → HistNext × ℝ := fun p => (appendAbs p, p.2)
      Measurable H ∧ Measurable Hnext ∧ Measurable a ∧ Measurable U ∧
      Measurable appendAbs ∧ Measurable liftAbs ∧
      (∀ p : Hist × ℝ, ∀ j : Fin (n + 1), appendAbs p j.castSucc = p.1 j) ∧
      (∀ b : Hist → ℝ≥0, Measurable b →
        let d : Hist → ℝ≥0 := fun h => Real.toNNReal ((b h : ℝ) - a h)
        let μ : Measure Hist := Measure.map H P
        let D : Hist → ℝ → ℝ≥0∞ := fun h u =>
          if a h < u ∧ u < (b h : ℝ) then density y xRef (h last, u - a h) else 0
        let Brel : Set (ℕ → ℝ) := {w |
          (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
          waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
            ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
        let B : Set (ℕ → ℝ) := {w |
          (∃ q, H w last = Sum.inl q) ∧
          (∃ q, Hnext w lastNext = Sum.inl q) ∧
          a (H w) < U w ∧ U w < (b (H w) : ℝ)}
        let X : (ℕ → ℝ) → Hist × ℝ := fun w => (H w, U w)
        let Y : (ℕ → ℝ) → HistNext × ℝ := fun w => (Hnext w, U w)
        let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
          (fun p => D p.1 p.2)
        Measurable (Function.uncurry D) ∧
        (∀ h : Hist, (∫⁻ u : ℝ, D h u) ≤ 1) ∧
        MeasurableSet B ∧ Measurable X ∧ Measurable Y ∧ Brel = B ∧
        (∀ w ∈ B, U w = a (H w) +
          timeObs y xRef (record y xRef z₀ (ε w) n, w n)) ∧
        (∀ w ∈ B, Hnext w = appendAbs (X w)) ∧
        Measure.map X (P.restrict B) = ν ∧
        Measure.map Y (P.restrict B) = Measure.map liftAbs ν ∧
        Measure.map Hnext (P.restrict B) = Measure.map appendAbs ν ∧
        ν Set.univ ≤ 1 ∧
        (∀ G : Hist × ℝ → ℝ≥0∞, Measurable G →
          Measurable (fun h => ∫⁻ u : ℝ, G (h, u) * D h u) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, G (X w) ∂P) =
              ∫⁻ h in A, (∫⁻ u : ℝ, G (h, u) * D h u) ∂μ)) ∧
        (∀ F : HistNext × ℝ → ℝ≥0∞, Measurable F →
          Measurable (fun h => ∫⁻ u : ℝ, F (liftAbs (h, u)) * D h u) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, F (Y w) ∂P) =
              ∫⁻ h in A, (∫⁻ u : ℝ, F (liftAbs (h, u)) * D h u) ∂μ)))

  have h90 := ActualFiniteHistoryExtension.actual_finite_history_extension
    hα hαβ hV hH hη hβη
  have h89 := ActualConditionalNextWaitDensity.actual_conditional_next_wait_density
    hα hαβ hV hH hη hβη
  intro y xRef z₀ n
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist := Fin (n + 1) → Rec
  let HistNext := Fin (n + 2) → Rec
  let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
  let lastNext : Fin (n + 2) := ⟨n + 1, Nat.lt_succ_self (n + 1)⟩
  let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
  let Hnext : (ℕ → ℝ) → HistNext := history y xRef z₀ (n + 1)
  let readTime : Rec → ℝ := fun r => match r with
    | Sum.inl q => (q.1 : ℝ)
    | Sum.inr _ => 0
  let a : Hist → ℝ := fun h => readTime (h last)
  let U : (ℕ → ℝ) → ℝ := fun w => readTime (Hnext w lastNext)
  let appendRel : Hist × ℝ → HistNext := fun p =>
    Fin.snoc p.1 (match p.1 last with
      | Sum.inl q => Sum.inl (q.1 + Real.toNNReal p.2,
          S xRef (Φ y xRef p.2 q.2))
      | Sum.inr _ => Sum.inr ())
  let appendAbs : Hist × ℝ → HistNext := fun p => appendRel (p.1, p.2 - a p.1)
  let liftAbs : Hist × ℝ → HistNext × ℝ := fun p => (appendAbs p, p.2)
  change Measurable H ∧ Measurable Hnext ∧ Measurable a ∧ Measurable U ∧
    Measurable appendAbs ∧ Measurable liftAbs ∧
    (∀ p : Hist × ℝ, ∀ j : Fin (n + 1), appendAbs p j.castSucc = p.1 j) ∧ _
  have hnext : Measurable Hnext := (h90 y xRef z₀ n).1
  have hrel : Measurable appendRel := (h90 y xRef z₀ n).2.1
  have hprefix (p : Hist × ℝ) (j : Fin (n + 1)) : appendRel p j.castSucc = p.1 j :=
    (h90 y xRef z₀ n).2.2.2.1 p j
  have hhistory : Measurable H := by
    apply measurable_pi_lambda
    intro j
    exact (measurable_pi_apply j.castSucc).comp hnext
  have hread : Measurable readTime := by
    change Measurable (Sum.elim (fun q : ℝ≥0 × (E × E) => (q.1 : ℝ))
      (fun _ : Unit => (0 : ℝ)))
    exact (measurable_coe_nnreal_real.comp measurable_fst).sumElim measurable_const
  have ha : Measurable a := hread.comp (measurable_pi_apply last)
  have hU : Measurable U := hread.comp ((measurable_pi_apply lastNext).comp hnext)
  have happend : Measurable appendAbs :=
    hrel.comp (measurable_fst.prodMk (measurable_snd.sub (ha.comp measurable_fst)))
  have hlift : Measurable liftAbs := happend.prodMk measurable_snd
  refine ⟨hhistory, hnext, ha, hU, happend, hlift,
    (fun p j => hprefix (p.1, p.2 - a p.1) j), ?_⟩
  intro b hb
  let d : Hist → ℝ≥0 := fun h => Real.toNNReal ((b h : ℝ) - a h)
  let μ : Measure Hist := Measure.map H P
  let D : Hist → ℝ → ℝ≥0∞ := fun h u =>
    if a h < u ∧ u < (b h : ℝ) then density y xRef (h last, u - a h) else 0
  let Brel : Set (ℕ → ℝ) := {w |
    (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
    waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
      ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
  let B : Set (ℕ → ℝ) := {w |
    (∃ q, H w last = Sum.inl q) ∧
    (∃ q, Hnext w lastNext = Sum.inl q) ∧
    a (H w) < U w ∧ U w < (b (H w) : ℝ)}
  let X : (ℕ → ℝ) → Hist × ℝ := fun w => (H w, U w)
  let Y : (ℕ → ℝ) → HistNext × ℝ := fun w => (Hnext w, U w)
  let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
    (fun p => D p.1 p.2)
  change Measurable (Function.uncurry D) ∧
    (∀ h : Hist, (∫⁻ u : ℝ, D h u) ≤ 1) ∧ _
  have hd : Measurable d := measurable_real_toNNReal.comp
    ((measurable_coe_nnreal_real.comp hb).sub ha)
  have hrho : Measurable (density y xRef) := (h89 y xRef z₀ n).2.1
  have hD : Measurable (Function.uncurry D) := by
    have hguard : MeasurableSet {p : Hist × ℝ |
        a p.1 < p.2 ∧ p.2 < (b p.1 : ℝ)} :=
      (measurableSet_lt (ha.comp measurable_fst) measurable_snd).inter
        (measurableSet_lt measurable_snd
          (measurable_coe_nnreal_real.comp (hb.comp measurable_fst)))
    exact (hrho.comp (((measurable_pi_apply last).comp measurable_fst).prodMk
      (measurable_snd.sub (ha.comp measurable_fst)))).piecewise hguard measurable_const
  let Drel : Hist → ℝ → ℝ≥0∞ := fun h s =>
    if 0 < s ∧ s < (d h : ℝ) then density y xRef (h last, s) else 0
  have h89d := (h89 y xRef z₀ n).2.2.2 d hd
  have hcutoff (h : Hist) (s : ℝ) :
      (a h < a h + s ∧ a h + s < (b h : ℝ)) ↔
        (0 < s ∧ s < (d h : ℝ)) := by
      change (a h < a h + s ∧ a h + s < (b h : ℝ)) ↔
        (0 < s ∧ s < (Real.toNNReal ((b h : ℝ) - a h) : ℝ))
      rw [Real.coe_toNNReal']
      constructor
      · intro hs
        refine ⟨by linarith [hs.1], ?_⟩
        exact lt_of_lt_of_le (by linarith [hs.2]) (le_max_left _ _)
      · intro hs
        refine ⟨by linarith [hs.1], ?_⟩
        rcases lt_max_iff.mp hs.2 with hb' | hzero
        · linarith
        · linarith [hs.1]
  have hshift (h : Hist) (s : ℝ) : D h (a h + s) = Drel h s := by
    simp only [D, Drel, add_sub_cancel_left, hcutoff h s]
  have hrelative_fiber (h : Hist) : (∫⁻ s : ℝ, Drel h s) ≤ 1 := by
    calc
      (∫⁻ s : ℝ, Drel h s) =
          ((volume : Measure ℝ).withDensity (Drel h)) Set.univ := by
        rw [withDensity_apply _ MeasurableSet.univ, setLIntegral_univ]
      _ ≤ 1 := by
        have hbnd := h89d.2.2.2.1 h
        rw [h89d.2.1 h] at hbnd
        exact hbnd
  have hfiber (h : Hist) : (∫⁻ u : ℝ, D h u) ≤ 1 := by
    calc
      (∫⁻ u : ℝ, D h u) = ∫⁻ s : ℝ, D h (a h + s) :=
        ((measurePreserving_add_left (volume : Measure ℝ) (a h)).lintegral_comp
          hD.of_uncurry_left).symm
      _ = ∫⁻ s : ℝ, Drel h s := lintegral_congr (hshift h)
      _ ≤ 1 := hrelative_fiber h
  have h90d := (h90 y xRef z₀ n).2.2.2.2 d hd
  have hBrel : MeasurableSet Brel := h90d.1
  have hactualRel (w : ℕ → ℝ) (hw : w ∈ Brel) :
      Hnext w = appendRel (H w, timeObs y xRef (record y xRef z₀ (ε w) n, w n)) :=
    h90d.2.2.1 w hw
  have hguarded (w : ℕ → ℝ) :
      (w ∈ Brel ↔ w ∈ B) ∧
      (w ∈ Brel → U w = a (H w) +
        timeObs y xRef (record y xRef z₀ (ε w) n, w n)) := by
    cases hrec : record y xRef z₀ (ε w) n with
    | inr q =>
      have hold : H w last = Sum.inr q := hrec
      have hnew : Hnext w lastNext = Sum.inr () := by
        change next y xRef (ε w n) (record y xRef z₀ (ε w) n) = _
        simp only [next, hrec]
      simp [Brel, B, waitObs, hrec, hold, hnew]
    | inl q =>
      have hold : H w last = Sum.inl q := hrec
      have htime : a (H w) = (q.1 : ℝ) := by simp only [a, readTime, hold]
      cases ht : τ y xRef q.2 (Real.toNNReal (w n)) using WithTop.recTopCoe with
      | top =>
        have hnew : Hnext w lastNext = Sum.inr () := by
          change next y xRef (ε w n) (record y xRef z₀ (ε w) n) = _
          simp [next, hrec, ε, ht]
        simp [Brel, B, waitObs, hrec, ht, hnew]
        constructor
        · exact not_lt_of_ge le_top
        · intro hw
          exact ((not_lt_of_ge le_top) hw).elim
      | coe v =>
        have hnew : Hnext w lastNext =
            Sum.inl (q.1 + v, S xRef (Φ y xRef (v : ℝ) q.2)) := by
          change next y xRef (ε w n) (record y xRef z₀ (ε w) n) = _
          simp only [next, hrec, ε, ht, WithTop.coe_ne_top, if_false,
            WithTop.untopD_coe]
        have hu : U w = (q.1 : ℝ) + (v : ℝ) := by
          simp only [U, readTime, hnew, NNReal.coe_add]
        have hz : (0 : WithTop ℝ≥0) < (v : WithTop ℝ≥0) ↔ 0 < v := by
          simpa only [WithTop.coe_zero] using
            (WithTop.coe_lt_coe : ((0 : ℝ≥0) : WithTop ℝ≥0) < (v : WithTop ℝ≥0) ↔ 0 < v)
        constructor
        · have hcore : (0 < v ∧ v < d (H w)) ↔
              ((q.1 : ℝ) < (q.1 : ℝ) + (v : ℝ) ∧
                (q.1 : ℝ) + (v : ℝ) < (b (H w) : ℝ)) := by
            simpa only [htime, NNReal.coe_pos, NNReal.coe_lt_coe] using
              (hcutoff (H w) (v : ℝ)).symm
          simp only [Brel, B, Set.mem_ofPred_eq, waitObs, hrec, ht, hz,
            WithTop.coe_lt_coe, hold, hnew, htime, hu]
          constructor
          · intro hv
            exact ⟨⟨q, rfl⟩, ⟨(q.1 + v, S xRef (Φ y xRef (v : ℝ) q.2)), rfl⟩,
              hcore.mp hv⟩
          · intro hw
            exact hcore.mpr hw.2.2
        · intro _
          simp only [hu, htime, timeObs, waitObs, hrec, ht, WithTop.untopD_coe]
  have hBeq : Brel = B := Set.ext (fun w => (hguarded w).1)
  have hB : MeasurableSet B := hBeq ▸ hBrel
  have hX : Measurable X := hhistory.prodMk hU
  have hY : Measurable Y := hnext.prodMk hU
  have hclock (w : ℕ → ℝ) (hw : w ∈ B) : U w = a (H w) +
      timeObs y xRef (record y xRef z₀ (ε w) n, w n) :=
    (hguarded w).2 ((hguarded w).1.mpr hw)
  have hactual (w : ℕ → ℝ) (hw : w ∈ B) : Hnext w = appendAbs (X w) := by
    have htime : U w - a (H w) =
        timeObs y xRef (record y xRef z₀ (ε w) n, w n) := by
      rw [hclock w hw, add_sub_cancel_left]
    change Hnext w = appendRel (H w, U w - a (H w))
    rw [htime]
    exact hactualRel w ((hguarded w).1.mpr hw)
  let oldPrefix : HistNext → Hist := fun h j => h j.castSucc
  have hprefixM : Measurable oldPrefix := by
    apply measurable_pi_lambda
    intro j
    exact measurable_pi_apply j.castSucc
  have hprefixRel (p : Hist × ℝ) : oldPrefix (appendRel p) = p.1 := by
    funext j
    exact hprefix p j
  have hprefixActual (w : ℕ → ℝ) : oldPrefix (Hnext w) = H w := rfl
  have htranslate (G : Hist × ℝ → ℝ≥0∞) (hG : Measurable G) (h : Hist) :
      (∫⁻ s : ℝ, G (h, a h + s) * Drel h s) =
        ∫⁻ u : ℝ, G (h, u) * D h u := by
    calc
      (∫⁻ s : ℝ, G (h, a h + s) * Drel h s) =
          ∫⁻ s : ℝ, G (h, a h + s) * D h (a h + s) :=
        lintegral_congr (fun s => by rw [hshift h s])
      _ = ∫⁻ u : ℝ, G (h, u) * D h u :=
        (measurePreserving_add_left (volume : Measure ℝ) (a h)).lintegral_comp
          ((hG.comp (measurable_const.prodMk measurable_id)).mul hD.of_uncurry_left)
  have hGtests (G : Hist × ℝ → ℝ≥0∞) (hG : Measurable G) :
      Measurable (fun h => ∫⁻ u : ℝ, G (h, u) * D h u) ∧
      (∀ A : Set Hist, MeasurableSet A →
        (∫⁻ w in B ∩ H ⁻¹' A, G (X w) ∂P) =
          ∫⁻ h in A, (∫⁻ u : ℝ, G (h, u) * D h u) ∂μ) := by
    let Grel : HistNext × ℝ → ℝ≥0∞ := fun q =>
      G (oldPrefix q.1, a (oldPrefix q.1) + q.2)
    have hp : Measurable (fun q : HistNext × ℝ => oldPrefix q.1) :=
      hprefixM.comp measurable_fst
    have hGrel : Measurable Grel := hG.comp (hp.prodMk ((ha.comp hp).add measurable_snd))
    have htest := h90d.2.2.2.2.2.2 Grel hGrel
    refine ⟨(hG.mul hD).lintegral_prod_right', ?_⟩
    intro A hA
    have htestA :
        (∫⁻ w in Brel ∩ H ⁻¹' A,
          Grel (Hnext w, timeObs y xRef (record y xRef z₀ (ε w) n, w n)) ∂P) =
          ∫⁻ h in A, (∫⁻ s : ℝ, Grel (appendRel (h, s), s) * Drel h s) ∂μ :=
      htest.2 A hA
    rw [hBeq] at htestA
    calc
      (∫⁻ w in B ∩ H ⁻¹' A, G (X w) ∂P) =
          ∫⁻ w in B ∩ H ⁻¹' A,
            Grel (Hnext w, timeObs y xRef (record y xRef z₀ (ε w) n, w n)) ∂P := by
        apply setLIntegral_congr_fun (hB.inter (hA.preimage hhistory))
        intro w hw
        change G (H w, U w) =
          G (oldPrefix (Hnext w), a (oldPrefix (Hnext w)) +
            timeObs y xRef (record y xRef z₀ (ε w) n, w n))
        rw [hprefixActual, hclock w hw.1]
      _ = ∫⁻ h in A, (∫⁻ s : ℝ, Grel (appendRel (h, s), s) * Drel h s) ∂μ := htestA
      _ = ∫⁻ h in A, (∫⁻ u : ℝ, G (h, u) * D h u) ∂μ := by
        apply setLIntegral_congr_fun hA
        intro h _
        simpa only [Grel, hprefixRel] using htranslate G hG h
  -- Reuse the canonical actual input probability; no new normalization premise.
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  letI : IsProbabilityMeasure μ := Measure.isProbabilityMeasure_map hhistory.aemeasurable
  have hmapX : Measure.map X (P.restrict B) = ν := by
    apply Measure.ext_of_lintegral
    intro G hG
    have huniv := (hGtests G hG).2 Set.univ MeasurableSet.univ
    simp only [Set.preimage_univ, Set.inter_univ, setLIntegral_univ] at huniv
    calc
      (∫⁻ p, G p ∂Measure.map X (P.restrict B)) =
          ∫⁻ w in B, G (X w) ∂P := lintegral_map hG hX
      _ = ∫⁻ h, (∫⁻ u : ℝ, G (h, u) * D h u) ∂μ := huniv
      _ = ∫⁻ p : Hist × ℝ, G p * D p.1 p.2 ∂μ.prod (volume : Measure ℝ) :=
        (lintegral_prod _ (hG.mul hD).aemeasurable).symm
      _ = ∫⁻ p, G p ∂ν := by
        change _ = ∫⁻ p, G p ∂(μ.prod (volume : Measure ℝ)).withDensity (Function.uncurry D)
        exact ((lintegral_withDensity_eq_lintegral_mul _ hD hG).trans
          (lintegral_congr fun p => mul_comm _ _)).symm
  have hYactual (w : ℕ → ℝ) (hw : w ∈ B) : Y w = liftAbs (X w) :=
    Prod.ext (hactual w hw) rfl
  have hmapY : Measure.map Y (P.restrict B) = Measure.map liftAbs ν := by
    rw [← hmapX, Measure.map_map hlift hX]
    exact Measure.map_congr (ae_restrict_of_forall_mem hB hYactual)
  have hmarginal : Measure.map Hnext (P.restrict B) = Measure.map appendAbs ν := by
    rw [← hmapX, Measure.map_map happend hX]
    exact Measure.map_congr (ae_restrict_of_forall_mem hB hactual)
  have hmass : ν Set.univ ≤ 1 := by
    rw [← hmapX, Measure.map_apply hX MeasurableSet.univ, Set.preimage_univ,
      Measure.restrict_apply MeasurableSet.univ, Set.univ_inter]
    exact prob_le_one
  refine ⟨hD, hfiber, hB, hX, hY, hBeq, hclock, hactual,
    hmapX, hmapY, hmarginal, hmass, hGtests, ?_⟩
  intro F hF
  have htest := hGtests (F ∘ liftAbs) (hF.comp hlift)
  refine ⟨htest.1, ?_⟩
  intro A hA
  calc
    (∫⁻ w in B ∩ H ⁻¹' A, F (Y w) ∂P) =
        ∫⁻ w in B ∩ H ⁻¹' A, (F ∘ liftAbs) (X w) ∂P := by
      apply setLIntegral_congr_fun (hB.inter (hA.preimage hhistory))
      intro w hw
      exact congrArg F (hYactual w hw.1)
    _ = ∫⁻ h in A, (∫⁻ u : ℝ, F (liftAbs (h, u)) * D h u) ∂μ := htest.2 A hA

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime
