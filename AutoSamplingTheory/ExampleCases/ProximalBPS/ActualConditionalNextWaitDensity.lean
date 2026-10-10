import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw
import Mathlib.Probability.Kernel.WithDensity

/-! Actual conditional finite next-wait density, Appendix A.1.
ASTIS source-implicit completion of one finite next-jump density factor in
PBPS arXiv2609.06905v1 (A.1),(A.2),(A.7). Real Lebesgue time on the strict
interval 0<s<d(h) is exactly the real-time reference used by producer86.
No endpoint-mass equivalence, normalization, finite-wait guarantee or restart.
The zero extraction outside the finite guard is only a total observable.
Kernel.withDensity's measurable branch is identified explicitly by the proved fiber equality.
Full ordered-time iteration and final survival/path assembly remain open. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity
open InnerProductSpace MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_conditional_next_wait_density_statement
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
      Measurable (waitObs y xRef) ∧ Measurable (density y xRef) ∧
      (∀ q, density y xRef q ≠ ⊤) ∧
      (∀ d : (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) → ℝ≥0,
        Measurable d →
        let Hist := Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)
        let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
        let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
        let μ : Measure Hist := Measure.map H P
        let D : Hist → ℝ → ℝ≥0∞ := fun h s =>
          if 0 < s ∧ s < (d h : ℝ) then density y xRef (h last, s) else 0
        let K : Kernel Hist ℝ := (Kernel.const Hist (volume : Measure ℝ)).withDensity D
        let B : Set (ℕ → ℝ) := {w |
          (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
          waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
            ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
        let X : (ℕ → ℝ) → Hist × ℝ := fun w =>
          (H w, timeObs y xRef (record y xRef z₀ (ε w) n, w n))
        let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
          (fun p => D p.1 p.2)
        Measurable (Function.uncurry D) ∧
        (∀ h, K h = (volume : Measure ℝ).withDensity (D h)) ∧
        IsFiniteKernel K ∧ (∀ h, K h Set.univ ≤ 1) ∧
        MeasurableSet B ∧ Measurable X ∧
        Measure.map X (P.restrict B) = ν ∧ ν Set.univ ≤ 1 ∧
        (∀ F : Hist × ℝ → ℝ≥0∞, Measurable F →
          Measurable (fun h => ∫⁻ s : ℝ, F (h, s) * D h s) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, F (X w) ∂P) =
              ∫⁻ h in A, (∫⁻ s : ℝ, F (h, s) * D h s) ∂μ)))


set_option maxHeartbeats 1600000 in
theorem actual_conditional_next_wait_density
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1):
    actual_conditional_next_wait_density_statement hα hαβ hV hH hη hβη := by
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
    Measurable (waitObs y xRef) ∧ Measurable (density y xRef) ∧
    (∀ q, density y xRef q ≠ ⊤) ∧
    (∀ d : (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) → ℝ≥0,
      Measurable d →
      let Hist := Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)
      let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
      let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
      let μ : Measure Hist := Measure.map H P
      let D : Hist → ℝ → ℝ≥0∞ := fun h s =>
        if 0 < s ∧ s < (d h : ℝ) then density y xRef (h last, s) else 0
      let K : Kernel Hist ℝ := (Kernel.const Hist (volume : Measure ℝ)).withDensity D
      let B : Set (ℕ → ℝ) := {w |
        (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
        waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
          ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
      let X : (ℕ → ℝ) → Hist × ℝ := fun w =>
        (H w, timeObs y xRef (record y xRef z₀ (ε w) n, w n))
      let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
        (fun p => D p.1 p.2)
      Measurable (Function.uncurry D) ∧
      (∀ h, K h = (volume : Measure ℝ).withDensity (D h)) ∧
      IsFiniteKernel K ∧ (∀ h, K h Set.univ ≤ 1) ∧
      MeasurableSet B ∧ Measurable X ∧
      Measure.map X (P.restrict B) = ν ∧ ν Set.univ ≤ 1 ∧
      (∀ F : Hist × ℝ → ℝ≥0∞, Measurable F →
        Measurable (fun h => ∫⁻ s : ℝ, F (h, s) * D h s) ∧
        (∀ A : Set Hist, MeasurableSet A →
          (∫⁻ w in B ∩ H ⁻¹' A, F (X w) ∂P) =
            ∫⁻ h in A, (∫⁻ s : ℝ, F (h, s) * D h s) ∂μ)))

  have hc := ActualHazardClock.actual_integrated_hazard_clock_laws hα hαβ hV hH hη hβη
  have hτ : Measurable (fun a : (E × E) × (E × E) × ℝ≥0 =>
      τ a.1.1 a.1.2 a.2.1 a.2.2) := hc.2.2.2.2.2.2.1
  have hΛ : Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) := hc.2.1
  have hf := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hr := ActualBounceRate.actual_bounce_rate_energy_laws hα hαβ hV hH hη hβη
  have hi := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
  letI : IsProbabilityMeasure P := hi.1
  intro y xRef z₀ n
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist := Fin (n + 1) → Rec
  let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
  -- Total clock and density observables are jointly Borel, including stopped0.
  have hw : Measurable (waitObs y xRef) := by
    let e := MeasurableEquiv.sumProdDistrib (ℝ≥0 × (E × E)) Unit ℝ
    have hl : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
        τ y xRef q.1.2 (Real.toNNReal q.2)) :=
      hτ.comp (f := fun q : (ℝ≥0 × (E × E)) × ℝ =>
        ((y, xRef), q.1.2, Real.toNNReal q.2))
        (measurable_const.prodMk (measurable_fst.snd.prodMk
          (measurable_real_toNNReal.comp measurable_snd)))
    have heq : waitObs y xRef = (Sum.elim
        (fun q : (ℝ≥0 × (E × E)) × ℝ => τ y xRef q.1.2 (Real.toNNReal q.2))
        (fun _ : Unit × ℝ => (0 : WithTop ℝ≥0))) ∘ e := by
      funext q; rcases q with ⟨a | a, t⟩ <;> rfl
    rw [heq]
    exact (hl.sumElim (measurable_const : Measurable
      (fun _ : Unit × ℝ => (0 : WithTop ℝ≥0)))).comp e.measurable
  have ht : Measurable (timeObs y xRef) :=
    measurable_subtype_coe.comp (hw.untopD 0)
  have hρ : Measurable (density y xRef) := by
    let e := MeasurableEquiv.sumProdDistrib (ℝ≥0 × (E × E)) Unit ℝ
    have hφ : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ => Φ y xRef q.2 q.1.2) :=
      hf.1.measurable.comp (f := fun q : (ℝ≥0 × (E × E)) × ℝ =>
        ((y, xRef), q.2, q.1.2))
        (measurable_const.prodMk (measurable_snd.prodMk measurable_fst.snd))
    have hl : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
        ENNReal.ofReal (rate xRef (Φ y xRef q.2 q.1.2) *
          Real.exp (-Λ y xRef q.1.2 (Real.toNNReal q.2)))) := by
      have hrateArgs : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
          (xRef, Φ y xRef q.2 q.1.2)) :=
        (measurable_const : Measurable
          (fun _ : (ℝ≥0 × (E × E)) × ℝ => xRef)).prodMk hφ
      have hrate : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
          rate xRef (Φ y xRef q.2 q.1.2)) := hr.2.1.measurable.comp hrateArgs
      have hΛArgs : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
          (((y, xRef), q.1.2), Real.toNNReal q.2)) :=
        (((measurable_const : Measurable
          (fun _ : (ℝ≥0 × (E × E)) × ℝ => (y, xRef))).prodMk
          measurable_fst.snd).prodMk (measurable_real_toNNReal.comp measurable_snd))
      have hhazard : Measurable (fun q : (ℝ≥0 × (E × E)) × ℝ =>
          Λ y xRef q.1.2 (Real.toNNReal q.2)) := hΛ.comp hΛArgs
      exact (hrate.mul hhazard.neg.exp).ennreal_ofReal
    have heq : density y xRef = (Sum.elim
        (fun q : (ℝ≥0 × (E × E)) × ℝ => ENNReal.ofReal
          (rate xRef (Φ y xRef q.2 q.1.2) *
            Real.exp (-Λ y xRef q.1.2 (Real.toNNReal q.2))))
        (fun _ : Unit × ℝ => (0 : ℝ≥0∞))) ∘ e := by
      funext q; rcases q with ⟨a | a, t⟩ <;> rfl
    rw [heq]
    exact (hl.sumElim (measurable_const : Measurable
      (fun _ : Unit × ℝ => (0 : ℝ≥0∞)))).comp e.measurable
  have hρfin (q : Rec × ℝ) : density y xRef q ≠ ⊤ := by
    rcases q with ⟨a | a, t⟩
    · exact ENNReal.ofReal_ne_top
    · exact ENNReal.zero_ne_top
  refine ⟨hw, hρ, hρfin, ?_⟩
  intro d hd
  let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
  let Y : (ℕ → ℝ) → (ℕ → ℝ) := fun w k => w (n + k)
  let μ : Measure Hist := Measure.map H P
  let D : Hist → ℝ → ℝ≥0∞ := fun h s =>
    if 0 < s ∧ s < (d h : ℝ) then density y xRef (h last, s) else 0
  let K : Kernel Hist ℝ := (Kernel.const Hist (volume : Measure ℝ)).withDensity D
  let W : Hist × (ℕ → ℝ) → WithTop ℝ≥0 :=
    fun p => waitObs y xRef (p.1 last, p.2 0)
  let Q : Set (Hist × (ℕ → ℝ)) := {p |
    (0 : WithTop ℝ≥0) < W p ∧ W p < ((d p.1 : ℝ≥0) : WithTop ℝ≥0)}
  let G : Hist × (ℕ → ℝ) → Hist × ℝ :=
    fun p => (p.1, timeObs y xRef (p.1 last, p.2 0))
  let B : Set (ℕ → ℝ) := {w |
    (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
    waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
      ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
  let X : (ℕ → ℝ) → Hist × ℝ := fun w =>
    (H w, timeObs y xRef (record y xRef z₀ (ε w) n, w n))
  let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
    (fun p => D p.1 p.2)
  have hp := ActualFiniteHistoryTailLaw.actual_finite_history_tail_law
    hα hαβ hV hH hη hβη y xRef z₀ n
  have hHm : Measurable H := hp.1
  have hY : Measurable Y := hp.2.1
  have hjoint : Measure.map (fun w => (H w, Y w)) P = μ.prod P := hp.2.2.2.2.2.2.1
  letI : IsProbabilityMeasure μ := Measure.isProbabilityMeasure_map hHm.aemeasurable
  have hargs : Measurable (fun p : Hist × (ℕ → ℝ) => (p.1 last, p.2 0)) :=
    ((measurable_pi_apply last).comp measurable_fst).prodMk
      ((measurable_pi_apply 0).comp measurable_snd)
  have hW : Measurable W := hw.comp hargs
  have hQ : MeasurableSet Q :=
    (measurableSet_lt measurable_const hW).inter
      (measurableSet_lt hW (WithTop.measurable_coe.comp (hd.comp measurable_fst)))
  have hG : Measurable G := measurable_fst.prodMk (ht.comp hargs)
  have hXeq : X = G ∘ (fun w => (H w, Y w)) := rfl
  have hBeq : B = (fun w => (H w, Y w)) ⁻¹' Q := rfl
  have hB : MeasurableSet B := hBeq ▸ hQ.preimage (hHm.prodMk hY)
  have hX : Measurable X := hXeq ▸ hG.comp (hHm.prodMk hY)
  have hD : Measurable (Function.uncurry D) := by
    have hguard : MeasurableSet {p : Hist × ℝ | 0 < p.2 ∧ p.2 < (d p.1 : ℝ)} :=
      (measurableSet_lt measurable_const measurable_snd).inter
        (measurableSet_lt measurable_snd (measurable_subtype_coe.comp (hd.comp measurable_fst)))
    exact (hρ.comp (((measurable_pi_apply last).comp measurable_fst).prodMk
      measurable_snd)).piecewise hguard measurable_const
  have hK (h : Hist) : K h = (volume : Measure ℝ).withDensity (D h) :=
    Kernel.withDensity_apply _ hD h
  -- Restrict the deterministic Ioc law by Iio: strict endpoints on BOTH sides.
  have hfiber (h : Hist) :
      Measure.map (fun w : ℕ → ℝ => timeObs y xRef (h last, w 0))
        (P.restrict {w | (h, w) ∈ Q}) = (volume : Measure ℝ).withDensity (D h) := by
    cases ha : h last with
    | inr a =>
      simp [Q, W, waitObs, timeObs, density, D, ha]
    | inl a =>
      let U : (ℕ → ℝ) → WithTop ℝ≥0 := fun w => τ y xRef a.2 (ε w 0)
      let f : (ℕ → ℝ) → ℝ := fun w => ((U w).untopD 0 : ℝ≥0)
      let A : Set (ℕ → ℝ) := {w | (0 : WithTop ℝ≥0) < U w ∧
        U w ≤ ((d h : ℝ≥0) : WithTop ℝ≥0)}
      let ρ : Measure ℝ := (volume.restrict (Set.Ioc (0 : ℝ) (d h : ℝ))).withDensity
        (fun s => density y xRef (Sum.inl a, s))
      have hfirst := ActualFiniteFirstEventLaw.actual_finite_first_event_law
        hα hαβ hV hH hη hβη y xRef a.2
      have hfm : Measurable f := hfirst.2.1
      have hclosed : Measure.map f (P.restrict A) = ρ := (hfirst.2.2.2 (d h)).2.1
      have hset : A ∩ f ⁻¹' Set.Iio (d h : ℝ) = {w | (h, w) ∈ Q} := by
        ext w
        simp only [Set.mem_inter_iff, A, Set.mem_ofPred_eq, Set.mem_preimage,
          Set.mem_Iio, Q, W, waitObs, ha]
        change ((0 : WithTop ℝ≥0) < U w ∧ U w ≤ ↑(d h)) ∧
          (((U w).untopD 0 : ℝ≥0) : ℝ) < (d h : ℝ) ↔
            (0 : WithTop ℝ≥0) < U w ∧ U w < ↑(d h)
        cases hu : U w using WithTop.recTopCoe with
        | top =>
          simp only [WithTop.not_top_le_coe, and_false, false_and]
          exact iff_of_false id (fun hs => (not_lt_of_ge le_top) hs.2)
        | coe s =>
          have hz : (0 : WithTop ℝ≥0) < (s : WithTop ℝ≥0) ↔ 0 < s := by
            have hz0 : ((0 : ℝ≥0) : WithTop ℝ≥0) < (s : WithTop ℝ≥0) ↔
                (0 : ℝ≥0) < s := WithTop.coe_lt_coe
            simpa only [WithTop.coe_zero] using hz0
          simp only [WithTop.untopD_coe, WithTop.coe_le_coe,
            WithTop.coe_lt_coe, NNReal.coe_lt_coe, hz]
          exact ⟨fun v => ⟨v.1.1, v.2⟩, fun v => ⟨⟨v.1, v.2.le⟩, v.2⟩⟩
      have hstrict : Measure.map f (P.restrict {w | (h, w) ∈ Q}) = ρ.restrict (Set.Iio (d h : ℝ)) := by
        rw [← hclosed, Measure.restrict_map hfm measurableSet_Iio,
          Measure.restrict_restrict (measurableSet_Iio.preimage hfm), Set.inter_comm, hset]
      simp only [timeObs, waitObs, ha]
      change Measure.map f (P.restrict {w | (h, w) ∈ Q}) = _
      rw [hstrict]
      dsimp only [ρ]
      rw [restrict_withDensity measurableSet_Iio,
        Measure.restrict_restrict measurableSet_Iio]
      have hinterval : Set.Iio (d h : ℝ) ∩ Set.Ioc (0 : ℝ) (d h : ℝ) =
          Set.Ioo (0 : ℝ) (d h : ℝ) := by ext s; simp; grind
      rw [hinterval, ← withDensity_indicator measurableSet_Ioo]
      congr 1
      funext s
      simp [D, ha, Set.indicator, Set.mem_Ioo]
  have hmass (h : Hist) : K h Set.univ ≤ 1 := by
    rw [hK, ← hfiber]
    have hfm : Measurable (fun w : ℕ → ℝ => timeObs y xRef (h last, w 0)) :=
      ht.comp (measurable_const.prodMk (measurable_pi_apply 0))
    rw [Measure.map_apply hfm MeasurableSet.univ, Set.preimage_univ,
      Measure.restrict_apply MeasurableSet.univ, Set.univ_inter]
    exact prob_le_one
  have hfinite : IsFiniteKernel K := ⟨⟨1, ENNReal.one_lt_top, hmass⟩⟩
  -- The actual complete history and unchanged unused tail have the product law.
  have hmap : Measure.map X (P.restrict B) = ν := by
    apply Measure.ext
    intro C hC
    let L : Set (Hist × (ℕ → ℝ)) := G ⁻¹' C ∩ Q
    have hL : MeasurableSet L := (hC.preimage hG).inter hQ
    calc
      Measure.map X (P.restrict B) C =
          (Measure.map (fun w => (H w, Y w)) P) L := by
        rw [Measure.map_apply hX hC, Measure.restrict_apply (hC.preimage hX),
          Measure.map_apply (hHm.prodMk hY) hL]
        rfl
      _ = (μ.prod P) L := by rw [hjoint]
      _ = ∫⁻ h : Hist, P {w : ℕ → ℝ | (h, w) ∈ L} ∂μ := Measure.prod_apply hL
      _ = ∫⁻ h : Hist, ((volume : Measure ℝ).withDensity (D h))
          ((fun s : ℝ => (h, s)) ⁻¹' C) ∂μ := by
        apply lintegral_congr
        intro h
        have hs : MeasurableSet ((fun s : ℝ => (h, s)) ⁻¹' C) :=
          hC.preimage (measurable_const.prodMk measurable_id)
        have htm : Measurable (fun w : ℕ → ℝ => timeObs y xRef (h last, w 0)) :=
          ht.comp (measurable_const.prodMk (measurable_pi_apply 0))
        rw [← hfiber, Measure.map_apply htm hs,
          Measure.restrict_apply (hs.preimage htm)]
        rfl
      _ = ∫⁻ h : Hist, (∫⁻ s : ℝ, C.indicator (fun p => D p.1 p.2) (h, s)) ∂μ := by
        apply lintegral_congr
        intro h
        have hs : MeasurableSet ((fun s : ℝ => (h, s)) ⁻¹' C) :=
          hC.preimage (measurable_const.prodMk measurable_id)
        rw [withDensity_apply _ hs, ← lintegral_indicator hs]
        rfl
      _ = ∫⁻ p in C, D p.1 p.2 ∂μ.prod (volume : Measure ℝ) := by
        exact (lintegral_prod (C.indicator (Function.uncurry D))
          (hD.indicator hC).aemeasurable).symm.trans (lintegral_indicator hC _)
      _ = ν C := (withDensity_apply _ hC).symm
  have hνmass : ν Set.univ ≤ 1 := by
    rw [← hmap, Measure.map_apply hX MeasurableSet.univ, Set.preimage_univ,
      Measure.restrict_apply MeasurableSet.univ, Set.univ_inter]
    exact prob_le_one
  refine ⟨hD, hK, hfinite, hmass, hB, hX, hmap, hνmass, ?_⟩
  intro F hF
  have hFD : Measurable (fun p : Hist × ℝ => F p * D p.1 p.2) := hF.mul hD
  refine ⟨hFD.lintegral_prod_right', ?_⟩
  intro A hA
  let f : Hist × ℝ → ℝ≥0∞ := (Prod.fst ⁻¹' A).indicator F
  have hm : Measurable f := hF.indicator (hA.preimage measurable_fst)
  calc
    (∫⁻ w in B ∩ H ⁻¹' A, F (X w) ∂P) =
        ∫⁻ w in B, f (X w) ∂P := by
      rw [Set.inter_comm B, ← Measure.restrict_restrict (hA.preimage hHm),
        ← lintegral_indicator (hA.preimage hHm)]
      apply lintegral_congr
      intro w
      simp [f, X, Set.indicator, and_comm]
    _ = ∫⁻ p, f p ∂ν := by rw [← hmap, lintegral_map hm hX]
    _ = ∫⁻ p : Hist × ℝ, f p * D p.1 p.2 ∂μ.prod (volume : Measure ℝ) := by
      change (∫⁻ p, f p ∂(μ.prod (volume : Measure ℝ)).withDensity (Function.uncurry D)) = _
      exact (lintegral_withDensity_eq_lintegral_mul _ hD hm).trans
        (lintegral_congr fun p => mul_comm _ _)
    _ = ∫⁻ h : Hist, (∫⁻ s : ℝ, f (h, s) * D h s) ∂μ :=
      lintegral_prod _ (hm.mul hD).aemeasurable
    _ = ∫⁻ h in A, (∫⁻ s : ℝ, F (h, s) * D h s) ∂μ := by
      rw [← lintegral_indicator hA]
      apply lintegral_congr
      intro h
      by_cases ha : h ∈ A
      · rw [Set.indicator_of_mem ha]
        apply lintegral_congr; intro s; simp [f, ha]
      · simp [f, ha]

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity
