import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
import Mathlib.Data.Set.Card
import Mathlib.Order.Interval.Set.Nat
import Mathlib.MeasureTheory.Constructions.Pi

/-!
# Actual finite-count history and coordinate-product path law

An ASTIS completion of the terminal-survival / finite-count ingredient of
Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1 (A.7), with the
actual Borel construction of Appendix A.2. The original six analytic hypotheses
are unchanged. This module assembles previously verified actual dynamics,
finite-prefix density and conditional survival; it derives endpoint nullity,
count interpretation, and a joint unnormalized history/path law internally.

Paths carry the coordinate-product sigma algebra. Fixed-horizon almost-sure
claims are not a uniform no-jump event over all horizons. Hazard stitching,
left limits, the full countable A.7 expansion, restart/Markovness, invariance,
hypocoercivity, implementation errors and expected oracle costs remain separate.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2400000
open scoped Classical

private theorem measurable_finite_fold {X Y : Type*}
    [MeasurableSpace X] [MeasurableSpace Y] (n : ℕ)
    (f : X → Y → Fin n → X)
    (hf : ∀ j, Measurable (fun p : X × Y => f p.1 p.2 j))
    (x : Y → X) (hx : Measurable x) :
    Measurable (fun y => Fin.foldl n (fun z j => f z y j) (x y)) := by
  induction n with
  | zero => simpa only [Fin.foldl_zero] using hx
  | succ n ih =>
    have hr := ih (fun z y j => f z y j.castSucc) (fun j => hf j.castSucc)
    simpa only [Fin.foldl_succ_last, Function.comp_def, id_eq] using
      (hf (Fin.last n)).comp (hr.prodMk measurable_id)

private theorem measurable_record_step {X Y : Type*}
    [MeasurableSpace X] [MeasurableSpace Y]
    (Φ : Y → ℝ≥0 → X → X)
    (hΦ : Measurable (fun p : Y × ℝ≥0 × X => Φ p.1 p.2.1 p.2.2))
    (s : ℝ≥0) :
    Measurable (fun p : ((ℝ≥0 × X) ⊕ Unit) × (X × Y) =>
      p.1.elim (fun a => if a.1 ≤ s then Φ p.2.2 (s - a.1) a.2 else p.2.1)
        (fun _ => p.2.1)) := by
  classical
  let e := MeasurableEquiv.sumProdDistrib (ℝ≥0 × X) Unit (X × Y)
  have hl : Measurable (fun p : (ℝ≥0 × X) × (X × Y) =>
      if p.1.1 ≤ s then Φ p.2.2 (s - p.1.1) p.1.2 else p.2.1) := by
    apply Measurable.ite (measurableSet_le measurable_fst.fst measurable_const)
    · exact hΦ.comp (measurable_snd.snd.prodMk
        ((measurable_const.sub measurable_fst.fst).prodMk measurable_fst.snd))
    · exact measurable_snd.fst
  convert (hl.sumElim (measurable_snd.fst :
    Measurable (fun p : Unit × (X × Y) => p.2.1))).comp e.measurable using 1
  funext p
  rcases p with ⟨a | a, q⟩ <;> rfl

private theorem measurable_history_interpolation {X Y : Type*}
    [MeasurableSpace X] [MeasurableSpace Y]
    (Φ : Y → ℝ≥0 → X → X)
    (hΦ : Measurable (fun p : Y × ℝ≥0 × X => Φ p.1 p.2.1 p.2.2))
    (n : ℕ) (T : ℝ≥0)
    (h : Y → Fin n → ((ℝ≥0 × X) ⊕ Unit)) (hh : Measurable h)
    (z₀ : Y → X) (hz₀ : Measurable z₀) :
    Measurable (fun y => fun s : {s : ℝ≥0 // s ≤ T} =>
      Fin.foldl n (fun z j => (h y j).elim
        (fun a => if a.1 ≤ s.val then Φ y (s.val - a.1) a.2 else z)
        (fun _ => z)) (z₀ y)) := by
  classical
  apply measurable_pi_lambda
  intro s
  apply measurable_finite_fold n _ _ z₀ hz₀
  intro j
  exact (measurable_record_step Φ hΦ s.val).comp
    (((measurable_pi_apply j).comp (hh.comp measurable_snd)).prodMk measurable_id)

/- The last eligible index, rather than a maximum chosen by an unmeasurable
path-space operation, determines each coordinate of the literal fold. -/

private theorem finite_fold_last_eligible {X : Type*} (n : ℕ)
    (b : Fin n → Prop) [DecidablePred b] (v : Fin n → X) (x : X)
    (j : Fin n) (hj : b j) (hafter : ∀ k : Fin n, j < k → ¬ b k) :
    Fin.foldl n (fun z k => if b k then v k else z) x = v j := by
  induction n with
  | zero => exact Fin.elim0 j
  | succ n ih =>
    induction j using Fin.lastCases with
    | last => simp only [Fin.foldl_succ_last, if_pos hj]
    | cast j =>
      rw [Fin.foldl_succ_last, if_neg (hafter (Fin.last n) (Fin.castSucc_lt_last j))]
      exact ih (fun k => b k.castSucc) (fun k => v k.castSucc) j hj
        (fun k hk => hafter k.castSucc (Fin.castSucc_lt_castSucc_iff.mpr hk))


/- Small constructor identity suggested by the independent fragment diagnostic.
Keep case elimination outside the actual theorem's large literal context. -/

private theorem terminal_elim_identity {X : Type*} (T : ℝ≥0)
    (g : X → ℝ≥0 → ℝ≥0∞) (r : (ℝ≥0 × X) ⊕ Unit) :
    r.elim (fun a => g a.2 (T - r.elim Prod.fst (fun _ => 0))) (fun _ => 0) =
      r.elim (fun a => g a.2 (T - a.1)) (fun _ => 0) := by
  cases r <;> rfl

private theorem measurable_terminal_record_weight {X Y : Type*}
    [MeasurableSpace X] [MeasurableSpace Y]
    (L : Y → X → ℝ≥0 → ℝ)
    (hL : Measurable (fun p : (Y × X) × ℝ≥0 => L p.1.1 p.1.2 p.2))
    (T : ℝ≥0) :
    Measurable (fun p : ((ℝ≥0 × X) ⊕ Unit) × Y =>
      p.1.elim (fun a => ENNReal.ofReal (Real.exp (-L p.2 a.2 (T - a.1)))) (fun _ => 0)) := by
  let e := MeasurableEquiv.sumProdDistrib (ℝ≥0 × X) Unit Y
  have hl : Measurable (fun p : (ℝ≥0 × X) × Y =>
      ENNReal.ofReal (Real.exp (-L p.2 p.1.2 (T - p.1.1)))) :=
    (hL.comp (f := fun p : (ℝ≥0 × X) × Y => ((p.2, p.1.2), T - p.1.1))
      ((measurable_snd.prodMk measurable_fst.snd).prodMk
        (measurable_const.sub measurable_fst.fst))).neg.exp.ennreal_ofReal
  convert (hl.sumElim (measurable_const : Measurable (fun _ : Unit × Y => (0 : ℝ≥0∞)))).comp
    e.measurable using 1
  funext p
  rcases p with ⟨a | a, q⟩ <;> rfl

private theorem real_time_history_fold {X : Type*} (Φ : ℝ → X → X)
    (n : ℕ) (t : Fin n → ℝ) (ht : ∀ k, 0 ≤ t k) (z : Fin n → X) (z₀ : X)
    (s : ℝ≥0) (j : Fin n) (hj : t j ≤ (s : ℝ))
    (hafter : ∀ k : Fin n, j < k → (s : ℝ) < t k) :
    Fin.foldl n (fun x k => if Real.toNNReal (t k) ≤ s then
      Φ (((s - Real.toNNReal (t k)) : ℝ≥0) : ℝ) (z k) else x) z₀ =
      Φ ((s : ℝ) - t j) (z j) := by
  have hcoe (k : Fin n) : (Real.toNNReal (t k) : ℝ) = t k := Real.coe_toNNReal (t k) (ht k)
  have hj' : Real.toNNReal (t j) ≤ s := by
    exact_mod_cast (show (Real.toNNReal (t j) : ℝ) ≤ (s : ℝ) by rw [hcoe]; exact hj)
  have ha (k : Fin n) (hjk : j < k) : ¬ Real.toNNReal (t k) ≤ s := by
    intro hk
    have hkr : (Real.toNNReal (t k) : ℝ) ≤ (s : ℝ) := by exact_mod_cast hk
    rw [hcoe] at hkr
    exact not_lt_of_ge hkr (hafter k hjk)
  rw [finite_fold_last_eligible n (fun k => Real.toNNReal (t k) ≤ s)
    (fun k => Φ (((s - Real.toNNReal (t k)) : ℝ≥0) : ℝ) (z k)) z₀ j hj' ha,
    NNReal.coe_sub hj', hcoe]

private theorem actual_history_interpolation_measurable
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    ∀ n : ℕ, ∀ T : ℝ≥0,
      Measurable (fun p : ((E × E) × (E × E)) × Hist n =>
        Ψ p.1.1.1 p.1.1.2 p.1.2 n T p.2) := by
  classical
  let c : E → E → E := fun y xRef => y - η • gradient V xRef
  let Φ : E → E → ℝ → (E × E) → (E × E) := fun y xRef t z =>
    (c y xRef + Real.cos t • (z.1 - c y xRef) +
        (Real.sqrt η * Real.sin t) • z.2,
     (-Real.sin t / Real.sqrt η) • (z.1 - c y xRef) + Real.cos t • z.2)
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
  let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
    fun y xRef z₀ n T h s =>
      Fin.foldl (n + 1) (fun z j => (h j).elim
        (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
        (fun _ => z)) z₀
  change ∀ n : ℕ, ∀ T : ℝ≥0,
    Measurable (fun p : ((E × E) × (E × E)) × Hist n =>
      Ψ p.1.1.1 p.1.1.2 p.1.2 n T p.2)
  have hf := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws
    hα hαβ hV hH hη hβη
  have hΦ : Measurable (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) := hf.2.1
  intro n T
  let Y := ((E × E) × (E × E)) × Hist n
  have hΦY : Measurable (fun p : Y × ℝ≥0 × (E × E) =>
      Φ p.1.1.1.1 p.1.1.1.2 (p.2.1 : ℝ) p.2.2) :=
    hΦ.comp (f := fun p : Y × ℝ≥0 × (E × E) =>
      (p.1.1.1, (p.2.1 : ℝ), p.2.2)) (measurable_fst.fst.fst.prodMk
      ((measurable_coe_nnreal_real.comp measurable_snd.fst).prodMk measurable_snd.snd))
  exact measurable_history_interpolation
    (fun p : Y => fun t z => Φ p.1.1.1 p.1.1.2 (t : ℝ) z)
    hΦY (n + 1) T (fun p : Y => p.2) measurable_snd
    (fun p : Y => p.1.2) measurable_fst.snd

private theorem localized_survival_history_measure {Ω H : Type*}
    [MeasurableSpace Ω] [MeasurableSpace H]
    (μ : Measure Ω) (history : Ω → H) (S : Set Ω) (weight : H → ℝ≥0∞)
    (hh : Measurable history)
    (hset : ∀ A : Set H, MeasurableSet A →
      μ (history ⁻¹' A ∩ S) = ∫⁻ h in A, weight h ∂Measure.map history μ)
    (A : Set H) (hA : MeasurableSet A) :
    Measure.map history (μ.restrict (history ⁻¹' A ∩ S)) =
      ((Measure.map history μ).restrict A).withDensity weight := by
  apply Measure.ext
  intro B hB
  rw [Measure.map_apply hh hB, Measure.restrict_apply (hB.preimage hh),
    withDensity_apply weight hB, Measure.restrict_restrict hB,
    ← hset (B ∩ A) (hB.inter hA)]
  congr 1
  ext w
  simp only [Set.mem_inter_iff, Set.mem_preimage]
  exact and_assoc.symm

private theorem actual_terminal_survival_history_tests
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
    let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
      fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
    let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
      fun y xRef r u e => r.elim
        (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
    let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
      fun y xRef r u => r.elim
        (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0,
      ∀ A : Set (Hist n), MeasurableSet A →
      let H := history y xRef z₀ n
      let W : Hist n → ℝ≥0∞ := fun h =>
        weight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d n T h)
      let C : Set (ℕ → ℝ) := {w | H w ∈ A ∧
        survival y xRef (record y xRef z₀ (ε w) n) (d n T (H w)) (w n)}
      Measurable H ∧ Measurable W ∧ MeasurableSet C ∧
      Measure.map H (P.restrict C) = ((Measure.map H P).restrict A).withDensity W ∧
      (∀ F : Hist n → ℝ≥0∞, Measurable F →
        (∫⁻ w in C, F (H w) ∂P) = ∫⁻ h in A, F h * W h ∂Measure.map H P) := by
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
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
  let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
    fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
  let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
    fun y xRef r u e => r.elim
      (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
  let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
    fun y xRef r u => r.elim
      (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
  change
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0,
      ∀ A : Set (Hist n), MeasurableSet A →
      let H := history y xRef z₀ n
      let W : Hist n → ℝ≥0∞ := fun h =>
        weight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d n T h)
      let C : Set (ℕ → ℝ) := {w | H w ∈ A ∧
        survival y xRef (record y xRef z₀ (ε w) n) (d n T (H w)) (w n)}
      Measurable H ∧ Measurable W ∧ MeasurableSet C ∧
      Measure.map H (P.restrict C) = ((Measure.map H P).restrict A).withDensity W ∧
      (∀ F : Hist n → ℝ≥0∞, Measurable F →
        (∫⁻ w in C, F (H w) ∂P) = ∫⁻ h in A, F h * W h ∂Measure.map H P)
  intro y xRef z₀ n T A hA
  let H := history y xRef z₀ n
  let W : Hist n → ℝ≥0∞ := fun h =>
    weight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d n T h)
  let S₀ : Set (ℕ → ℝ) := {w |
    survival y xRef (record y xRef z₀ (ε w) n) (d n T (H w)) (w n)}
  let C : Set (ℕ → ℝ) := H ⁻¹' A ∩ S₀
  change Measurable H ∧ Measurable W ∧ MeasurableSet C ∧
    Measure.map H (P.restrict C) = ((Measure.map H P).restrict A).withDensity W ∧
    (∀ F : Hist n → ℝ≥0∞, Measurable F →
      (∫⁻ w in C, F (H w) ∂P) = ∫⁻ h in A, F h * W h ∂Measure.map H P)
  have hH : Measurable H :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law
      hα hαβ hV hH hη hβη y xRef z₀ n).1
  have hd : Measurable (d n T) :=
    measurable_const.sub (((measurable_fst : Measurable
      (fun p : ℝ≥0 × (E × E) => p.1)).sumElim measurable_const).comp
        (measurable_pi_apply (⟨n, Nat.lt_succ_self n⟩ : Fin (n + 1))))
  have h88 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival.actual_conditional_next_wait_survival
    hα hαβ hV ‹∀ x v : E, (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2› hη hβη y xRef z₀ n (d n T) hd
  let weight' : Rec → ℝ≥0 → ℝ≥0∞ := fun r u => match r with
    | Sum.inl a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))
    | Sum.inr _ => 0
  let survival' : Rec → ℝ≥0 → ℝ → Prop := fun r u e => match r with
    | Sum.inl a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)
    | Sum.inr _ => False
  change MeasurableSet {p : Hist n × (ℕ → ℝ) |
      survival' (p.1 ⟨n, Nat.lt_succ_self n⟩) (d n T p.1) (p.2 0)} ∧
    Measurable (fun h : Hist n => weight' (h ⟨n, Nat.lt_succ_self n⟩) (d n T h)) ∧
    (∀ h : Hist n, weight' (h ⟨n, Nat.lt_succ_self n⟩) (d n T h) ≤ 1) ∧
    (∀ B : Set (Hist n), MeasurableSet B →
      P {w | H w ∈ B ∧ survival' (record y xRef z₀ (ε w) n) (d n T (H w)) (w n)} =
        ∫⁻ h in B, weight' (h ⟨n, Nat.lt_succ_self n⟩) (d n T h) ∂Measure.map H P) at h88
  have hweight : weight' = weight y xRef := by
    funext r u
    cases r <;> rfl
  have hsurvival : survival' = survival y xRef := by
    funext r u e
    cases r <;> rfl
  rw [hweight, hsurvival] at h88
  have hW : Measurable W := h88.2.1
  have hS : MeasurableSet S₀ := by
    have hm : Measurable (fun w : ℕ → ℝ => (H w, fun k : ℕ => w (n + k))) :=
      hH.prodMk (measurable_pi_lambda _ fun k => measurable_pi_apply (n + k))
    simpa only [Set.preimage_ofPred_eq, Nat.add_zero] using h88.1.preimage hm
  have hC : MeasurableSet C := (hA.preimage hH).inter hS
  have hset : ∀ B : Set (Hist n), MeasurableSet B →
      P (H ⁻¹' B ∩ S₀) = ∫⁻ h in B, W h ∂Measure.map H P := h88.2.2.2
  have hlaw := localized_survival_history_measure P H S₀ W hH hset A hA
  refine ⟨hH, hW, hC, hlaw, ?_⟩
  intro F hF
  rw [← lintegral_map hF hH, hlaw,
    lintegral_withDensity_eq_lintegral_mul _ hW hF]
  exact lintegral_congr fun h => mul_comm _ _

private theorem actual_terminal_weighted_prefix_tests
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let readTime : Rec → ℝ := fun r => match r with
      | Sum.inl q => (q.1 : ℝ)
      | Sum.inr _ => 0
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ := fun y xRef z₀ n T t =>
      ∏ i : Fin n,
        rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
          (zAt y xRef z₀ n T t i.castSucc)) *
        Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
          (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
    let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
      ENNReal.ofReal (qReal y xRef z₀ n T t)
    let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
      {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
        StrictMono (fun j => readTime (h j)) ∧
        ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
    let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
    let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
      fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
    let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
      fun y xRef r u e => r.elim
        (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
    let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
      fun y xRef r u => r.elim
        (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
    let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
      fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
        survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
      fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
    let ρ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ≥0∞ :=
      fun y xRef z₀ n T t => q y xRef z₀ n T t *
        weight y xRef ((K y xRef z₀ n T t) ⟨n, Nat.lt_succ_self n⟩)
          (d n T (K y xRef z₀ n T t))
    ∀ n : ℕ, ∀ T : ℝ≥0,
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        ρ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        MeasurableSet (C y xRef z₀ n T) ∧
        Measurable (ρ y xRef z₀ n T) ∧
        (∀ F : Hist n × Path T → ℝ≥0∞, Measurable F →
          (∫⁻ w in C y xRef z₀ n T,
            F (history y xRef z₀ n w, Ψ y xRef z₀ n T (history y xRef z₀ n w)) ∂P) =
              ∫⁻ t : Prefix n T, F (K y xRef z₀ n T t, Γ y xRef z₀ n T t) *
                ρ y xRef z₀ n T t ∂m n T) ∧
        Measure.map (fun w => (history y xRef z₀ n w,
          Ψ y xRef z₀ n T (history y xRef z₀ n w))) (P.restrict (C y xRef z₀ n T)) =
          Measure.map (fun t => (K y xRef z₀ n T t, Γ y xRef z₀ n T t))
            ((m n T).withDensity (ρ y xRef z₀ n T)) ∧
        (∫⁻ t : Prefix n T, ρ y xRef z₀ n T t ∂m n T) = P (C y xRef z₀ n T) ∧
        P (C y xRef z₀ n T) ≤ 1) := by
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
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let readTime : Rec → ℝ := fun r => match r with
    | Sum.inl q => (q.1 : ℝ)
    | Sum.inr _ => 0
  let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
    {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
  let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
  let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
    Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
  let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
    Fin.induction z₀ (fun i z =>
      S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
  let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Hist n := fun y xRef z₀ n T t j =>
    Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
  let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ := fun y xRef z₀ n T t =>
    ∏ i : Fin n,
      rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
        (zAt y xRef z₀ n T t i.castSucc)) *
      Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
        (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
  let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
    ENNReal.ofReal (qReal y xRef z₀ n T t)
  let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
    {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
      StrictMono (fun j => readTime (h j)) ∧
      ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
  let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
  let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
    fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
  let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
    fun y xRef r u e => r.elim
      (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
  let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
    fun y xRef r u => r.elim
      (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
  let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
    fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
      survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
  let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
  let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
    fun y xRef z₀ n T h s =>
      Fin.foldl (n + 1) (fun z j => (h j).elim
        (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
        (fun _ => z)) z₀
  let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
    fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
  let ρ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ≥0∞ :=
    fun y xRef z₀ n T t => q y xRef z₀ n T t *
      weight y xRef ((K y xRef z₀ n T t) ⟨n, Nat.lt_succ_self n⟩)
        (d n T (K y xRef z₀ n T t))
  change
    ∀ n : ℕ, ∀ T : ℝ≥0,
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        ρ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        MeasurableSet (C y xRef z₀ n T) ∧
        Measurable (ρ y xRef z₀ n T) ∧
        (∀ F : Hist n × Path T → ℝ≥0∞, Measurable F →
          (∫⁻ w in C y xRef z₀ n T,
            F (history y xRef z₀ n w, Ψ y xRef z₀ n T (history y xRef z₀ n w)) ∂P) =
              ∫⁻ t : Prefix n T, F (K y xRef z₀ n T t, Γ y xRef z₀ n T t) *
                ρ y xRef z₀ n T t ∂m n T) ∧
        Measure.map (fun w => (history y xRef z₀ n w,
          Ψ y xRef z₀ n T (history y xRef z₀ n w))) (P.restrict (C y xRef z₀ n T)) =
          Measure.map (fun t => (K y xRef z₀ n T t, Γ y xRef z₀ n T t))
            ((m n T).withDensity (ρ y xRef z₀ n T)) ∧
        (∫⁻ t : Prefix n T, ρ y xRef z₀ n T t ∂m n T) = P (C y xRef z₀ n T) ∧
        P (C y xRef z₀ n T) ≤ 1)
  intro n T
  have h92 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law
    hα hαβ hV hH hη hβη n T
  have hA : MeasurableSet (A n T) := h92.2.1
  have hK : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      K p.1.1.1 p.1.1.2 p.1.2 n T p.2) := h92.2.2.1
  have hq : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      q p.1.1.1 p.1.1.2 p.1.2 n T p.2) := h92.2.2.2.1
  have hΨ : Measurable (fun p : ((E × E) × (E × E)) × Hist n =>
      Ψ p.1.1.1 p.1.1.2 p.1.2 n T p.2) :=
    actual_history_interpolation_measurable hα hαβ hV hH hη hβη n T
  have hΓ : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) :=
    hΨ.comp (f := fun p : ((E × E) × (E × E)) × Prefix n T =>
      (p.1, K p.1.1.1 p.1.1.2 p.1.2 n T p.2)) (measurable_fst.prodMk hK)
  have hΛ : Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws
      hα hαβ hV hH hη hβη).2.1
  have hWjoint : Measurable (fun p : ((E × E) × (E × E)) × Hist n =>
      weight p.1.1.1 p.1.1.2 (p.2 ⟨n, Nat.lt_succ_self n⟩) (d n T p.2)) := by
    have hg : Measurable (fun p : ((E × E) × (E × E)) × Hist n =>
        (p.2 ⟨n, Nat.lt_succ_self n⟩).elim
          (fun a => ENNReal.ofReal (Real.exp (-Λ p.1.1.1 p.1.1.2 a.2 (T - a.1))))
          (fun _ => 0)) := (measurable_terminal_record_weight
      (fun y : E × E => Λ y.1 y.2) hΛ T).comp
      (f := fun p : ((E × E) × (E × E)) × Hist n =>
        (p.2 ⟨n, Nat.lt_succ_self n⟩, p.1.1))
      (((measurable_pi_apply (⟨n, Nat.lt_succ_self n⟩ : Fin (n+1))).comp measurable_snd).prodMk
        measurable_fst.fst)
    have he : (fun p : ((E × E) × (E × E)) × Hist n =>
        weight p.1.1.1 p.1.1.2 (p.2 ⟨n, Nat.lt_succ_self n⟩) (d n T p.2)) =
        (fun p : ((E × E) × (E × E)) × Hist n =>
          (p.2 ⟨n, Nat.lt_succ_self n⟩).elim
            (fun a => ENNReal.ofReal (Real.exp (-Λ p.1.1.1 p.1.1.2 a.2 (T - a.1))))
            (fun _ => 0)) :=
      funext (fun p => terminal_elim_identity T
        (fun z u => ENNReal.ofReal (Real.exp (-Λ p.1.1.1 p.1.1.2 z u)))
        (p.2 ⟨n, Nat.lt_succ_self n⟩))
    rw [he]
    exact hg
  have hρjoint : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      ρ p.1.1.1 p.1.1.2 p.1.2 n T p.2) :=
    hq.mul (hWjoint.comp (f := fun p : ((E × E) × (E × E)) × Prefix n T =>
      (p.1, K p.1.1.1 p.1.1.2 p.1.2 n T p.2)) (measurable_fst.prodMk hK))
  refine ⟨hΓ, hρjoint, ?_⟩
  intro y xRef z₀
  let H := history y xRef z₀ n
  let W : Hist n → ℝ≥0∞ := fun h =>
    weight y xRef (h ⟨n, Nat.lt_succ_self n⟩) (d n T h)
  have hST := actual_terminal_survival_history_tests hα hαβ hV hH hη hβη
    y xRef z₀ n T (A n T) hA
  have hHM : Measurable H := hST.1
  have hW : Measurable W := hST.2.1
  have hKM : Measurable (K y xRef z₀ n T) := hK.comp
    (f := fun t : Prefix n T => (((y,xRef),z₀),t)) (measurable_const.prodMk measurable_id)
  have hqM : Measurable (q y xRef z₀ n T) := hq.comp
    (f := fun t : Prefix n T => (((y,xRef),z₀),t)) (measurable_const.prodMk measurable_id)
  have hΨM : Measurable (Ψ y xRef z₀ n T) := hΨ.comp
    (f := fun h : Hist n => (((y,xRef),z₀),h)) (measurable_const.prodMk measurable_id)
  have hρM : Measurable (ρ y xRef z₀ n T) := hqM.mul (hW.comp hKM)
  have ht : ∀ F : Hist n × Path T → ℝ≥0∞, Measurable F →
      (∫⁻ w in C y xRef z₀ n T, F (H w, Ψ y xRef z₀ n T (H w)) ∂P) =
        ∫⁻ t : Prefix n T, F (K y xRef z₀ n T t, Γ y xRef z₀ n T t) *
          ρ y xRef z₀ n T t ∂m n T := by
    intro F hF
    have hFΨ : Measurable (fun h : Hist n => F (h, Ψ y xRef z₀ n T h)) :=
      hF.comp (measurable_id.prodMk hΨM)
    have htests := (h92.2.2.2.2 y xRef z₀).2.2.2.2.2.2.1
    calc
      _ = ∫⁻ h in A n T, F (h, Ψ y xRef z₀ n T h) * W h ∂Measure.map H P :=
        hST.2.2.2.2 _ hFΨ
      _ = ∫⁻ w in H ⁻¹' A n T, F (H w, Ψ y xRef z₀ n T (H w)) * W (H w) ∂P :=
        setLIntegral_map hA (hFΨ.mul hW) hHM
      _ = ∫⁻ t : Prefix n T,
          (F (K y xRef z₀ n T t, Ψ y xRef z₀ n T (K y xRef z₀ n T t)) *
            W (K y xRef z₀ n T t)) * q y xRef z₀ n T t ∂m n T :=
        htests _ (hFΨ.mul hW)
      _ = _ := by
        apply lintegral_congr
        intro t
        dsimp only [ρ, Γ, W]
        ac_rfl
  refine ⟨hST.2.2.1, hρM, ht, ?_, ?_, ?_⟩
  · apply Measure.ext_of_lintegral
    intro F hF
    have hJ : Measurable (fun w => (H w, Ψ y xRef z₀ n T (H w))) :=
      hHM.prodMk (hΨM.comp hHM)
    have hL : Measurable (fun t => (K y xRef z₀ n T t, Γ y xRef z₀ n T t)) :=
      hKM.prodMk (hΨM.comp hKM)
    have hFL : Measurable (fun t : Prefix n T =>
        F (K y xRef z₀ n T t, Γ y xRef z₀ n T t)) := hF.comp hL
    rw [lintegral_map hF hJ, lintegral_map hF hL,
      lintegral_withDensity_eq_lintegral_mul _ hρM hFL, ht F hF]
    exact lintegral_congr fun _ => mul_comm _ _
  · have hm := ht (fun _ => 1) measurable_const
    simpa only [one_mul, setLIntegral_one] using hm.symm
  · letI : IsProbabilityMeasure P :=
      AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
    exact prob_le_one

private theorem finite_history_fold_eq_process {X : Type*}
    (Φ : ℝ≥0 → X → X) (r : ℕ → ((ℝ≥0 × X) ⊕ Unit)) (z₀ : X)
    (n : ℕ) (T : ℝ≥0)
    (hzero : r 0 = Sum.inl (0, z₀))
    (hlive : ∀ k : Fin (n + 1), ∃ a : ℝ≥0 × X, r k.val = Sum.inl a)
    (hend : (T : WithTop ℝ≥0) < (r (n + 1)).elim (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤))
    (Z : ℝ≥0 → X)
    (hZ : ∀ s : ℝ≥0, ∀ k : ℕ, ∀ a : ℝ≥0 × X,
      (r k).elim (fun b => (b.1 : WithTop ℝ≥0)) (fun _ => ⊤) ≤ (s : WithTop ℝ≥0) →
      (s : WithTop ℝ≥0) < (r (k+1)).elim (fun b => (b.1 : WithTop ℝ≥0)) (fun _ => ⊤) →
      r k = Sum.inl a → Z s = Φ (s - a.1) a.2) :
    ∀ s : ℝ≥0, s ≤ T →
      Fin.foldl (n + 1) (fun z j => (r j.val).elim
        (fun a => if a.1 ≤ s then Φ (s - a.1) a.2 else z) (fun _ => z)) z₀ = Z s := by
  classical
  intro s hs
  let time : ℕ → WithTop ℝ≥0 := fun k =>
    (r k).elim (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  let p : ℕ → Prop := fun k => time k ≤ (s : WithTop ℝ≥0)
  have hp0 : p 0 := by
    simp only [p, time, hzero, Sum.elim_inl]
    exact WithTop.coe_le_coe.mpr zero_le
  let k := Nat.findGreatest p n
  have hkn : k ≤ n := Nat.findGreatest_le n
  have hkp : p k := Nat.findGreatest_spec (Nat.zero_le n) hp0
  have hnext : (s : WithTop ℝ≥0) < time (k+1) := by
    by_cases hlast : k = n
    · rw [hlast]
      exact lt_of_le_of_lt (WithTop.coe_le_coe.mpr hs) hend
    · exact lt_of_not_ge (Nat.findGreatest_is_greatest (Nat.lt_succ_self k)
        (by omega : k + 1 ≤ n))
  let j : Fin (n + 1) := ⟨k, by omega⟩
  let a : Fin (n + 1) → ℝ≥0 × X := fun i => Classical.choose (hlive i)
  have ha (i : Fin (n + 1)) : r i.val = Sum.inl (a i) := Classical.choose_spec (hlive i)
  have hj : (a j).1 ≤ s := by
    have h := hkp
    change time j.val ≤ (s : WithTop ℝ≥0) at h
    simpa only [time, ha, Sum.elim_inl, WithTop.coe_le_coe] using h
  have hafter (i : Fin (n+1)) (hji : j < i) : ¬ (a i).1 ≤ s := by
    intro hi
    have hpi : p i.val := by
      simp only [p, time, ha, Sum.elim_inl]
      exact WithTop.coe_le_coe.mpr hi
    exact (Nat.findGreatest_is_greatest (show k < i.val from hji) (by omega)) hpi
  calc
    _ = Fin.foldl (n+1) (fun z i => if (a i).1 ≤ s then Φ (s - (a i).1) (a i).2 else z) z₀ := by
      congr 1
      funext z i
      rw [ha]
      rfl
    _ = Φ (s - (a j).1) (a j).2 :=
      finite_fold_last_eligible (n+1) (fun i => (a i).1 ≤ s)
        (fun i => Φ (s - (a i).1) (a i).2) z₀ j hj hafter
    _ = Z s := (hZ s k (a j) hkp hnext (ha j)).symm

private theorem terminal_event_after (T a : ℝ≥0) (q : WithTop ℝ≥0)
    (hq : ((T-a : ℝ≥0) : WithTop ℝ≥0) < q) :
    (T : WithTop ℝ≥0) < (if q = ⊤ then ⊤ else ((a + q.untopD 0 : ℝ≥0) : WithTop ℝ≥0)) := by
  classical
  by_cases htop : q = ⊤
  · rw [if_pos htop]
    exact WithTop.coe_lt_top T
  lift q to ℝ≥0 using htop
  simp only [WithTop.coe_ne_top, if_false, WithTop.untopD_coe, WithTop.coe_lt_coe] at hq ⊢
  calc
    T ≤ (T-a) + a := le_tsub_add
    _ < q + a := by simpa only [add_comm] using add_lt_add_right hq a
    _ = a + q := add_comm _ _

private theorem actual_history_path_identification
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let readTime : Rec → ℝ := fun r => match r with
      | Sum.inl q => (q.1 : ℝ)
      | Sum.inr _ => 0
    let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
      {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
        StrictMono (fun j => readTime (h j)) ∧
        ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
    let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
      fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
        (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
    let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
    let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
      fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
    let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
      fun y xRef r u e => r.elim
        (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
    let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
      fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
        survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E), w ∈ I y xRef z₀ s n →
          record y xRef z₀ (ε w) n = Sum.inl a →
          Z y xRef z₀ s w = Φ y xRef ((s - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        (¬ ∃ n, w ∈ I y xRef z₀ s n) → Z y xRef z₀ s w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ w ∂P, Z y xRef z₀ 0 w = z₀) ∧
      (∀ n : ℕ, ∀ T : ℝ≥0, ∀ y xRef : E, ∀ z₀ : E × E,
        ∀ w ∈ C y xRef z₀ n T,
          Ψ y xRef z₀ n T (history y xRef z₀ n w) =
            (fun s : {s : ℝ≥0 // s ≤ T} => Z y xRef z₀ s.val w)) := by
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
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let readTime : Rec → ℝ := fun r => match r with
    | Sum.inl q => (q.1 : ℝ)
    | Sum.inr _ => 0
  let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
    {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
      StrictMono (fun j => readTime (h j)) ∧
      ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
  let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
    fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
      (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
  let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
  let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
    fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
  let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
    fun y xRef r u e => r.elim
      (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
  let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
    fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
      survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
  let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
  let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
    fun y xRef z₀ n T h s =>
      Fin.foldl (n + 1) (fun z j => (h j).elim
        (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
        (fun _ => z)) z₀
  change
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E), w ∈ I y xRef z₀ s n →
          record y xRef z₀ (ε w) n = Sum.inl a →
          Z y xRef z₀ s w = Φ y xRef ((s - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        (¬ ∃ n, w ∈ I y xRef z₀ s n) → Z y xRef z₀ s w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ w ∂P, Z y xRef z₀ 0 w = z₀) ∧
      (∀ n : ℕ, ∀ T : ℝ≥0, ∀ y xRef : E, ∀ z₀ : E × E,
        ∀ w ∈ C y xRef z₀ n T,
          Ψ y xRef z₀ n T (history y xRef z₀ n w) =
            (fun s : {s : ℝ≥0 // s ≤ T} => Z y xRef z₀ s.val w))
  obtain ⟨Z, hZM, hZarc, hZfallback, hZgood⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase
      hα hαβ hV hH hη hβη
  refine ⟨Z, hZM, ?_, hZfallback, ?_, ?_⟩
  · intro y xRef z₀ w s n a hi hr
    exact hZarc y xRef z₀ w s n a hi.1 hi.2 hr
  · intro y xRef z₀
    filter_upwards [hZgood y xRef z₀] with w hw
    exact hw.2
  · intro n T y xRef z₀ w hw
    have hlive (k : Fin (n+1)) : ∃ a : ℝ≥0 × (E × E),
        record y xRef z₀ (ε w) k.val = Sum.inl a := hw.1.1 k
    obtain ⟨a, ha⟩ := hlive ⟨n, Nat.lt_succ_self n⟩
    have hsurv : ((T - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y xRef a.2 (ε w n) := by
      have hh := hw.2
      change survival y xRef (record y xRef z₀ (ε w) n)
        (T - liveTime (record y xRef z₀ (ε w) n)) (w n) at hh
      rw [ha] at hh
      exact hh
    have hnext : eventTime y xRef z₀ w (n+1) =
        (if τ y xRef a.2 (ε w n) = ⊤ then ⊤ else
          ((a.1 + (τ y xRef a.2 (ε w n)).untopD 0 : ℝ≥0) : WithTop ℝ≥0)) := by
      change (next y xRef (ε w n) (record y xRef z₀ (ε w) n)).elim _ _ = _
      rw [ha]
      dsimp only [next]
      split_ifs <;> rfl
    have hend : (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n+1) := by
      rw [hnext]
      exact terminal_event_after T a.1 (τ y xRef a.2 (ε w n)) hsurv
    funext s
    exact finite_history_fold_eq_process (fun u => Φ y xRef (u : ℝ))
      (record y xRef z₀ (ε w)) z₀ n T rfl hlive hend
      (fun u => Z y xRef z₀ u w)
      (fun u k a hlo hhi hr => hZarc y xRef z₀ w u k a hlo hhi hr) s.val s.property

private theorem find_decidable_eq (p : ℕ → Prop) (d₁ d₂ : DecidablePred p)
    (h : ∃ n, p n) : @Nat.find p d₁ h = @Nat.find p d₂ h := by
  have hd : d₁ = d₂ := Subsingleton.elim _ _
  cases hd
  rfl

private theorem measurable_first_available {Ω : Type*} [MeasurableSpace Ω]
    (I : ℕ → Set Ω) (hI : ∀ n, MeasurableSet (I n)) :
    Measurable (fun w => if h : ∃ n, w ∈ I n then Nat.find h else 0) := by
  classical
  let U : Set Ω := {w | ∃ n, w ∈ I n}
  have hU : MeasurableSet U := by
    change MeasurableSet {w | ∃ n, w ∈ I n}
    simpa only [Set.ofPred_exists, Set.ofPred_mem_eq] using MeasurableSet.iUnion hI
  have hm : Measurable (fun w : U => Nat.find w.property) :=
    measurable_find (fun w : U => w.property)
      (fun n => (hI n).preimage measurable_subtype_coe)
  exact hm.dite measurable_const hU

private theorem monotone_intervals_unique (t : ℕ → WithTop ℝ≥0) (ht : Monotone t)
    (T : ℝ≥0) (i j : ℕ) (hi : t i ≤ T ∧ (T : WithTop ℝ≥0) < t (i + 1))
    (hj : t j ≤ T ∧ (T : WithTop ℝ≥0) < t (j + 1)) : i = j := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with hij | hji
  · exact (not_lt_of_ge (le_trans (ht (Nat.succ_le_of_lt hij)) hj.1)) hi.2
  · exact (not_lt_of_ge (le_trans (ht (Nat.succ_le_of_lt hji)) hi.1)) hj.2

private theorem interval_count_cardinality (t : ℕ → WithTop ℝ≥0) (ht : Monotone t)
    (T : ℝ≥0) (N : ℕ) (hN : t N ≤ T ∧ (T : WithTop ℝ≥0) < t (N + 1))
    (hno : ∀ j : ℕ, 0 < j → t j ≠ (T : WithTop ℝ≥0)) :
    {j : ℕ | 0 < j ∧ t j < (T : WithTop ℝ≥0)}.Finite ∧
    {j : ℕ | 0 < j ∧ t j ≤ (T : WithTop ℝ≥0)}.Finite ∧
    N = {j : ℕ | 0 < j ∧ t j < (T : WithTop ℝ≥0)}.ncard ∧
    N = {j : ℕ | 0 < j ∧ t j ≤ (T : WithTop ℝ≥0)}.ncard := by
  have hle (j : ℕ) : t j ≤ (T : WithTop ℝ≥0) ↔ j ≤ N := by
    constructor
    · intro hj
      by_contra h
      exact not_lt_of_ge (le_trans (ht (by omega)) hj) hN.2
    · intro hj
      exact le_trans (ht hj) hN.1
  have hclosed : {j : ℕ | 0 < j ∧ t j ≤ (T : WithTop ℝ≥0)} = Set.Ioc 0 N := by
    ext j
    simp only [Set.mem_ofPred_eq, Set.mem_Ioc, hle]
  have hopen : {j : ℕ | 0 < j ∧ t j < (T : WithTop ℝ≥0)} = Set.Ioc 0 N := by
    ext j
    simp only [Set.mem_ofPred_eq, Set.mem_Ioc]
    constructor
    · rintro ⟨hj, htj⟩
      exact ⟨hj, (hle j).mp htj.le⟩
    · rintro ⟨hj, hjN⟩
      exact ⟨hj, lt_of_le_of_ne ((hle j).mpr hjN) (hno j hj)⟩
  rw [hopen, hclosed]
  exact ⟨Set.finite_Ioc 0 N, Set.finite_Ioc 0 N, by simp, by simp⟩

private theorem actual_count_selector_measurable
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
    let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
      fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
        (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
    let N : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → ℕ := fun y xRef z₀ T w =>
      if h : ∃ n, w ∈ I y xRef z₀ T n then Nat.find h else 0
    Measurable (fun p : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
      N p.1.1.1 p.1.1.2 p.1.2 p.2.1 p.2.2) := by
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
  let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
    fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
      (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
  let N : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → ℕ := fun y xRef z₀ T w =>
    if h : ∃ n, w ∈ I y xRef z₀ T n then Nat.find h else 0
  change
    Measurable (fun p : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
      N p.1.1.1 p.1.1.2 p.1.2 p.2.1 p.2.2)
  have h76 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  have hε : Measurable ε := measurable_pi_lambda _ fun n =>
    measurable_real_toNNReal.comp (measurable_pi_apply n)
  let X := ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ)
  have hm (n : ℕ) : Measurable (fun p : X => eventTime p.1.1.1 p.1.1.2 p.1.2 p.2.2 n) :=
    (h76.2.2.2.2.1 n).comp
      (f := fun p : X => (p.1.1, p.1.2, ε p.2.2))
      (measurable_fst.fst.prodMk (measurable_fst.snd.prodMk (hε.comp measurable_snd.snd)))
  have hT : Measurable (fun p : X => (p.2.1 : WithTop ℝ≥0)) :=
    WithTop.measurable_coe.comp measurable_snd.fst
  have hI (n : ℕ) : MeasurableSet {p : X | p.2.2 ∈ I p.1.1.1 p.1.1.2 p.1.2 p.2.1 n} :=
    (measurableSet_le (hm n) hT).inter (measurableSet_lt hT (hm (n + 1)))
  have hfirst := measurable_first_available
    (fun n => {p : X | p.2.2 ∈ I p.1.1.1 p.1.1.2 p.1.2 p.2.1 n}) hI
  convert hfirst using 1
  funext p
  dsimp only [N]
  split_ifs <;> first | exact find_decidable_eq _ _ _ _ | rfl | contradiction

private theorem actual_prescribed_path_interpolation
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
    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, z.2 - (2 * inner ℝ z.2 (gradient V z.1 - gradient V xRef) /
        ‖gradient V z.1 - gradient V xRef‖ ^ 2) • (gradient V z.1 - gradient V xRef))
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
      fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
    ∀ n : ℕ, ∀ T : ℝ≥0, ∀ y xRef : E, ∀ z₀ : E × E,
      ∀ t : Prefix n T, ∀ s : {s : ℝ≥0 // s ≤ T}, ∀ j : Fin (n + 1),
        (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j ≤ (s.val : ℝ) →
        (∀ k : Fin (n + 1), j < k → (s.val : ℝ) < (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) k) →
        Γ y xRef z₀ n T t s =
          Φ y xRef ((s.val : ℝ) - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j) (zAt y xRef z₀ n T t j) := by
  classical
  let c : E → E → E := fun y xRef => y - η • gradient V xRef
  let Φ : E → E → ℝ → (E × E) → (E × E) := fun y xRef t z =>
    (c y xRef + Real.cos t • (z.1 - c y xRef) +
        (Real.sqrt η * Real.sin t) • z.2,
     (-Real.sin t / Real.sqrt η) • (z.1 - c y xRef) + Real.cos t • z.2)
  let S : E → (E × E) → (E × E) := fun xRef z =>
    (z.1, z.2 - (2 * inner ℝ z.2 (gradient V z.1 - gradient V xRef) /
      ‖gradient V z.1 - gradient V xRef‖ ^ 2) • (gradient V z.1 - gradient V xRef))
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
    {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
  let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
  let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
    Fin.induction z₀ (fun i z =>
      S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
  let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Hist n := fun y xRef z₀ n T t j =>
    Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
  let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
  let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
    fun y xRef z₀ n T h s =>
      Fin.foldl (n + 1) (fun z j => (h j).elim
        (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
        (fun _ => z)) z₀
  let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
    fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
  change
    ∀ n : ℕ, ∀ T : ℝ≥0, ∀ y xRef : E, ∀ z₀ : E × E,
      ∀ t : Prefix n T, ∀ s : {s : ℝ≥0 // s ≤ T}, ∀ j : Fin (n + 1),
        (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j ≤ (s.val : ℝ) →
        (∀ k : Fin (n + 1), j < k → (s.val : ℝ) < (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) k) →
        Γ y xRef z₀ n T t s =
          Φ y xRef ((s.val : ℝ) - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j) (zAt y xRef z₀ n T t j)
  intro n T y xRef z₀ t s j hj hafter
  have hnonneg (k : Fin (n + 1)) :
      0 ≤ (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) k := by
    have hk := t.property.1.monotone (Fin.zero_le k)
    simpa only [Fin.cons_zero] using hk
  exact real_time_history_fold (Φ y xRef) (n + 1)
    (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ)) hnonneg
    (zAt y xRef z₀ n T t) z₀ s.val j hj hafter

private theorem subtype_coordinate_null (n : ℕ) (D : Set (Fin n → ℝ))
    (i : Fin n) (t : ℝ) :
    (Measure.comap (fun x : D => x.val) (volume : Measure (Fin n → ℝ)))
      {x | x.val i = t} = 0 := by
  have hm : MeasurableSet {x : D | x.val i = t} :=
    measurableSet_eq_fun ((measurable_pi_apply i).comp measurable_subtype_coe) measurable_const
  apply le_antisymm _ zero_le
  calc
    _ ≤ (volume : Measure (Fin n → ℝ))
        ((fun x : D => x.val) '' {x | x.val i = t}) :=
      Measure.comap_apply_le _ _ hm.nullMeasurableSet
    _ ≤ (volume : Measure (Fin n → ℝ)) {x | x i = t} := by
      apply measure_mono
      rintro x ⟨y, hy, rfl⟩
      exact hy
    _ = 0 := Measure.pi_hyperplane (fun _ : Fin n => (volume : Measure ℝ)) i t

private theorem weighted_map_coordinate_null
    {Ω X : Type*} [MeasurableSpace Ω] [MeasurableSpace X]
    (P : Measure Ω) (B : Set Ω) (H : Ω → X)
    (n : ℕ) (D : Set (Fin n → ℝ)) (K : D → X) (q : D → ℝ≥0∞)
    (obs : X → ℝ) (i : Fin n) (t : ℝ)
    (hH : Measurable H) (hK : Measurable K) (hobs : Measurable obs)
    (hcoord : ∀ x, obs (K x) = x.val i)
    (hlaw : Measure.map H (P.restrict B) =
      Measure.map K ((Measure.comap (fun x : D => x.val) volume).withDensity q)) :
    P ({w | obs (H w) = t} ∩ B) = 0 := by
  have hs : MeasurableSet {x | obs x = t} := measurableSet_eq_fun hobs measurable_const
  have hnull := withDensity_absolutelyContinuous
    (Measure.comap (fun x : D => x.val) volume) q (subtype_coordinate_null n D i t)
  have heval := congrArg (fun μ : Measure X => μ {x | obs x = t}) hlaw
  rw [Measure.map_apply hH hs, Measure.map_apply hK hs,
    Measure.restrict_apply (hs.preimage hH)] at heval
  have heq : K ⁻¹' {x | obs x = t} = {x : D | x.val i = t} := by
    ext x
    simp only [Set.mem_preimage, Set.mem_ofPred_eq, hcoord]
  rw [heq, hnull] at heval
  exact heval

private theorem live_prefix_strict_guard {X : Type*}
    (r : ℕ → (ℝ≥0 × X) ⊕ Unit)
    (hmono : Monotone (fun k => (r k).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)))
    (hstrict : ∀ k a b, r k = Sum.inl a → r (k+1) = Sum.inl b → a.1 < b.1)
    (n : ℕ) (T : ℝ≥0)
    (hend : (r n).elim (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤) < T) :
    (∀ j : Fin (n+1), ∃ a, r j.val = Sum.inl a) ∧
      StrictMono (fun j : Fin (n+1) => (r j.val).elim (fun a => (a.1 : ℝ)) (fun _ => 0)) ∧
      (∀ j : Fin n, (r j.succ.val).elim (fun a => (a.1 : ℝ)) (fun _ => 0) < T) := by
  have hfinite (k : ℕ) (hk : k ≤ n) :
      (r k).elim (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤) < T :=
    lt_of_le_of_lt (hmono hk) hend
  have hlive (j : Fin (n+1)) : ∃ a, r j.val = Sum.inl a := by
    have hh := hfinite j.val (Nat.le_of_lt_succ j.isLt)
    cases hr : r j.val with
    | inl a => exact ⟨a, rfl⟩
    | inr u => simp only [hr, Sum.elim_inr, not_top_lt] at hh
  refine ⟨hlive, ?_, ?_⟩
  · apply Fin.strictMono_iff_lt_succ.mpr
    intro j
    obtain ⟨a, ha⟩ := hlive j.castSucc
    obtain ⟨b, hb⟩ := hlive j.succ
    simp only [ha, hb, Sum.elim_inl]
    exact NNReal.coe_lt_coe.mpr (hstrict j.val a b ha hb)
  · intro j
    obtain ⟨a, ha⟩ := hlive j.succ
    have hh := hfinite j.succ.val (Nat.le_of_lt_succ j.succ.isLt)
    rw [ha] at hh ⊢
    exact NNReal.coe_lt_coe.mpr (WithTop.coe_lt_coe.mp hh)

private theorem actual_fixed_horizon_endpoint_nullity
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let readTime : Rec → ℝ := fun r => match r with
      | Sum.inl q => (q.1 : ℝ)
      | Sum.inr _ => 0
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ := fun y xRef z₀ n T t =>
      ∏ i : Fin n,
        rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
          (zAt y xRef z₀ n T t i.castSucc)) *
        Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
          (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
    let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
      ENNReal.ofReal (qReal y xRef z₀ n T t)
    let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
      {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
        StrictMono (fun j => readTime (h j)) ∧
        ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
    let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
      ∀ᵐ w ∂P, ∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0) := by
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
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let readTime : Rec → ℝ := fun r => match r with
    | Sum.inl q => (q.1 : ℝ)
    | Sum.inr _ => 0
  let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
    {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
  let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
  let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
    Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
  let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
    Fin.induction z₀ (fun i z =>
      S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
  let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Hist n := fun y xRef z₀ n T t j =>
    Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
  let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ := fun y xRef z₀ n T t =>
    ∏ i : Fin n,
      rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
        (zAt y xRef z₀ n T t i.castSucc)) *
      Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
        (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
  let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
    ENNReal.ofReal (qReal y xRef z₀ n T t)
  let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
    {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
      StrictMono (fun j => readTime (h j)) ∧
      ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
  let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  change
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
      ∀ᵐ w ∂P, ∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)
  intro y xRef z₀ T
  have h76 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  have hmono (w : ℕ → ℝ) : Monotone (eventTime y xRef z₀ w) :=
    (h76.2.2.2.2.2.1 y xRef z₀ (ε w)).2
  have hgood := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.2.2.2.1
  have hguard : ∀ᵐ w ∂P, ∀ n : ℕ,
      eventTime y xRef z₀ w n < ((T+1 : ℝ≥0) : WithTop ℝ≥0) →
        history y xRef z₀ n w ∈ A n (T+1) := by
    filter_upwards [hgood] with w hw
    intro n hn
    have hstrict (k : ℕ) (a b : ℝ≥0 × (E × E))
        (ha : record y xRef z₀ (ε w) k = Sum.inl a)
        (hb : record y xRef z₀ (ε w) (k+1) = Sum.inl b) : a.1 < b.1 :=
      (h76.2.2.2.2.2.2.2.2.2 y xRef z₀ (ε w) k a ha).2 b
        (Real.toNNReal_pos.mpr (hw k).1) hb
    have hh := live_prefix_strict_guard (record y xRef z₀ (ε w)) (hmono w) hstrict n (T+1) hn
    have heq (r : Rec) : readTime r = r.elim (fun a => (a.1 : ℝ)) (fun _ => 0) := by
      cases r <;> rfl
    exact ⟨hh.1, by simpa only [history, heq] using hh.2.1,
      by simpa only [history, heq] using hh.2.2⟩
  have hzero (n : ℕ) : P ({w | eventTime y xRef z₀ w (n+1) = (T : WithTop ℝ≥0)} ∩
      {w | history y xRef z₀ (n+1) w ∈ A (n+1) (T+1)}) = 0 := by
    have h92 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law
      hα hαβ hV hH hη hβη (n+1) (T+1)
    have hh := h92.2.2.2.2 y xRef z₀
    let obs : Hist (n+1) → ℝ := fun h => readTime (h (Fin.last (n+1)))
    have hread : Measurable readTime := by
      apply Measurable.sumElim
      · exact measurable_coe_nnreal_real.comp measurable_fst
      · exact measurable_const
    have hobs : Measurable obs := hread.comp (measurable_pi_apply (Fin.last (n+1)))
    have hK : Measurable (K y xRef z₀ (n+1) (T+1)) :=
      h92.2.2.1.comp (measurable_const (a := ((y,xRef),z₀)) |>.prodMk measurable_id)
    have hcoord (t : Prefix (n+1) (T+1)) :
        obs (K y xRef z₀ (n+1) (T+1) t) = t.val (Fin.last n) := by
      have hpos : 0 < t.val (Fin.last n) := by
        have ht := t.property.1 (show (0 : Fin (n+2)) < (Fin.last n).succ by
          change 0 < n+1; omega)
        simpa only [Fin.cons_zero, Fin.cons_succ] using ht
      change (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin (n+1) → ℝ) : Fin (n+2) → ℝ) (Fin.last (n+1))) : ℝ) = _
      change (Real.toNNReal (t.val (Fin.last n)) : ℝ) = _
      exact Real.coe_toNNReal _ hpos.le
    have hz := weighted_map_coordinate_null P
      (history y xRef z₀ (n+1) ⁻¹' A (n+1) (T+1)) (history y xRef z₀ (n+1))
      (n+1) (Δ (n+1) (T+1)) (K y xRef z₀ (n+1) (T+1))
      (q y xRef z₀ (n+1) (T+1)) obs (Fin.last n) (T : ℝ)
      hh.1 hK hobs hcoord hh.2.2.2.2.2.1
    apply measure_mono_null _ hz
    intro w hw
    refine ⟨?_, hw.2⟩
    obtain ⟨a, ha⟩ := hw.2.1 (Fin.last (n+1))
    change record y xRef z₀ (ε w) (n+1) = Sum.inl a at ha
    have he : a.1 = T := by
      have ht := hw.1
      change (record y xRef z₀ (ε w) (n+1)).elim _ _ = _ at ht
      rw [ha] at ht
      exact WithTop.coe_inj.mp ht
    change readTime (record y xRef z₀ (ε w) (n+1)) = (T : ℝ)
    rw [ha]
    exact congrArg (fun x : ℝ≥0 => (x : ℝ)) he
  have havoid (n : ℕ) : ∀ᵐ w ∂P, ¬ (eventTime y xRef z₀ w (n+1) = (T : WithTop ℝ≥0) ∧
      history y xRef z₀ (n+1) w ∈ A (n+1) (T+1)) := by
    rw [ae_iff]
    simpa only [not_not, Set.ofPred_and] using hzero n
  filter_upwards [hguard, ae_all_iff.mpr havoid] with w hg hn
  intro j hj heq
  obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hj)
  apply hn n
  refine ⟨heq, hg (n+1) ?_⟩
  rw [heq]
  exact WithTop.coe_lt_coe.mpr (lt_add_one T)

private theorem actual_count_event_identification
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let readTime : Rec → ℝ := fun r => match r with
      | Sum.inl q => (q.1 : ℝ)
      | Sum.inr _ => 0
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ := fun y xRef z₀ n T t =>
      ∏ i : Fin n,
        rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
          (zAt y xRef z₀ n T t i.castSucc)) *
        Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
          (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
    let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
      ENNReal.ofReal (qReal y xRef z₀ n T t)
    let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
      {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
        StrictMono (fun j => readTime (h j)) ∧
        ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
    let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
      fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
        (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
    let N : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → ℕ := fun y xRef z₀ T w =>
      if h : ∃ n, w ∈ I y xRef z₀ T n then Nat.find h else 0
    let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
    let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
      fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
    let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
      fun y xRef r u e => r.elim
        (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
    let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
      fun y xRef r u => r.elim
        (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
    let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
      fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
        survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
      (∀ n : ℕ, ∀ w ∈ C y xRef z₀ n T, w ∈ I y xRef z₀ T n) ∧
      (∀ᵐ w ∂P, (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
        (∀ k : ℕ, N y xRef z₀ T w = k ↔ w ∈ C y xRef z₀ k T) ∧
        {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.Finite ∧
        {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.Finite ∧
        N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.ncard ∧
        N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.ncard) ∧
      (Pairwise fun i j : ℕ => Disjoint (C y xRef z₀ i T) (C y xRef z₀ j T)) ∧
      P (⋃ k : ℕ, C y xRef z₀ k T) = 1 := by
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
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let readTime : Rec → ℝ := fun r => match r with
    | Sum.inl q => (q.1 : ℝ)
    | Sum.inr _ => 0
  let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
    {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
  let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
  let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
    Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
  let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
    Fin.induction z₀ (fun i z =>
      S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
  let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Hist n := fun y xRef z₀ n T t j =>
    Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
  let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ := fun y xRef z₀ n T t =>
    ∏ i : Fin n,
      rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
        (zAt y xRef z₀ n T t i.castSucc)) *
      Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
        (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
  let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
    ENNReal.ofReal (qReal y xRef z₀ n T t)
  let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
    {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
      StrictMono (fun j => readTime (h j)) ∧
      ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
  let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
    fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
      (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
  let N : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → ℕ := fun y xRef z₀ T w =>
    if h : ∃ n, w ∈ I y xRef z₀ T n then Nat.find h else 0
  let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
  let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
    fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
  let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
    fun y xRef r u e => r.elim
      (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
  let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
    fun y xRef r u => r.elim
      (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
  let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
    fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
      survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
  change
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
      (∀ n : ℕ, ∀ w ∈ C y xRef z₀ n T, w ∈ I y xRef z₀ T n) ∧
      (∀ᵐ w ∂P, (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
        (∀ k : ℕ, N y xRef z₀ T w = k ↔ w ∈ C y xRef z₀ k T) ∧
        {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.Finite ∧
        {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.Finite ∧
        N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.ncard ∧
        N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.ncard) ∧
      (Pairwise fun i j : ℕ => Disjoint (C y xRef z₀ i T) (C y xRef z₀ j T)) ∧
      P (⋃ k : ℕ, C y xRef z₀ k T) = 1
  intro y xRef z₀ T
  have h76 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  have hmono (w : ℕ → ℝ) : Monotone (eventTime y xRef z₀ w) :=
    (h76.2.2.2.2.2.1 y xRef z₀ (ε w)).2
  have hraw : ∀ n : ℕ, ∀ w ∈ C y xRef z₀ n T, w ∈ I y xRef z₀ T n := by
    intro n w hw
    obtain ⟨a, ha⟩ := hw.1.1 (Fin.last n)
    change record y xRef z₀ (ε w) n = Sum.inl a at ha
    have htime : a.1 ≤ T := by
      cases n with
      | zero =>
        have hz : (0 : ℝ≥0) = a.1 := congrArg Prod.fst (Sum.inl.inj ha)
        rw [← hz]; exact zero_le
      | succ n =>
        have ht := hw.1.2.2 (Fin.last n)
        change readTime (record y xRef z₀ (ε w) (n+1)) < (T : ℝ) at ht
        rw [ha] at ht
        exact (NNReal.coe_lt_coe.mp ht).le
    have hsurv : ((T - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y xRef a.2 (ε w n) := by
      have hh := hw.2
      change survival y xRef (record y xRef z₀ (ε w) n)
        (T - liveTime (record y xRef z₀ (ε w) n)) (w n) at hh
      rw [ha] at hh
      exact hh
    constructor
    · change (record y xRef z₀ (ε w) n).elim _ _ ≤ _
      rw [ha]; exact WithTop.coe_le_coe.mpr htime
    · have hnext : eventTime y xRef z₀ w (n+1) =
          (if τ y xRef a.2 (ε w n) = ⊤ then ⊤ else
            ((a.1 + (τ y xRef a.2 (ε w n)).untopD 0 : ℝ≥0) : WithTop ℝ≥0)) := by
        change (next y xRef (ε w n) (record y xRef z₀ (ε w) n)).elim _ _ = _
        rw [ha]; dsimp only [next]; split_ifs <;> rfl
      rw [hnext]
      exact terminal_event_after T a.1 (τ y xRef a.2 (ε w n)) hsurv
  have hgood := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.2.2.2.1
  have hcover := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover
    hα hαβ hV hH hη hβη y xRef z₀
  have hno := actual_fixed_horizon_endpoint_nullity hα hαβ hV hH hη hβη y xRef z₀ T
  have hAE : ∀ᵐ w ∂P,
      (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
      (∃ k, w ∈ I y xRef z₀ T k) ∧
      (∀ k, w ∈ I y xRef z₀ T k ↔ w ∈ C y xRef z₀ k T) := by
    filter_upwards [hgood, hcover, hno] with w hw hc hn
    refine ⟨hn, (hc.1 T).exists, ?_⟩
    intro k
    refine ⟨?_, hraw k w⟩
    intro hi
    have hstrict (l : ℕ) (a b : ℝ≥0 × (E × E))
        (ha : record y xRef z₀ (ε w) l = Sum.inl a)
        (hb : record y xRef z₀ (ε w) (l+1) = Sum.inl b) : a.1 < b.1 :=
      (h76.2.2.2.2.2.2.2.2.2 y xRef z₀ (ε w) l a ha).2 b
        (Real.toNNReal_pos.mpr (hw l).1) hb
    have hg := live_prefix_strict_guard (record y xRef z₀ (ε w)) (hmono w) hstrict k (T+1)
      (lt_of_le_of_lt hi.1 (WithTop.coe_lt_coe.mpr (lt_add_one T)))
    have heq (r : Rec) : readTime r = r.elim (fun a => (a.1 : ℝ)) (fun _ => 0) := by
      cases r <;> rfl
    refine ⟨⟨hg.1, ?_, ?_⟩, ?_⟩
    · simpa only [history, heq] using hg.2.1
    · intro j
      have hjle : eventTime y xRef z₀ w j.succ.val ≤ (T : WithTop ℝ≥0) :=
        le_trans (hmono w (Nat.le_of_lt_succ j.succ.isLt)) hi.1
      have hjlt := lt_of_le_of_ne hjle (hn j.succ.val (Nat.succ_pos _))
      obtain ⟨a, ha⟩ := hg.1 j.succ
      change (record y xRef z₀ (ε w) j.succ.val).elim _ _ < _ at hjlt
      change readTime (record y xRef z₀ (ε w) j.succ.val) < (T : ℝ)
      rw [ha] at hjlt ⊢
      exact NNReal.coe_lt_coe.mpr (WithTop.coe_lt_coe.mp hjlt)
    · obtain ⟨a, ⟨ha, hat, haw⟩, _⟩ := hc.2 T k hi.1 hi.2
      change record y xRef z₀ (ε w) k = Sum.inl a at ha
      change survival y xRef (record y xRef z₀ (ε w) k)
        (T - liveTime (record y xRef z₀ (ε w) k)) (w k)
      rw [ha]
      exact haw
  have hcount : ∀ᵐ w ∂P,
      (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
      (∀ k : ℕ, N y xRef z₀ T w = k ↔ w ∈ C y xRef z₀ k T) ∧
      {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.Finite ∧
      {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.Finite ∧
      N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.ncard ∧
      N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.ncard := by
    filter_upwards [hAE] with w hw
    have hN : w ∈ I y xRef z₀ T (N y xRef z₀ T w) := by
      dsimp only [N]
      split_ifs with hex
      · exact Nat.find_spec hex
      · exact False.elim (hex hw.2.1)
    refine ⟨hw.1, ?_, interval_count_cardinality (eventTime y xRef z₀ w) (hmono w)
      T (N y xRef z₀ T w) hN hw.1⟩
    intro k
    rw [← hw.2.2 k]
    constructor
    · intro hk; rw [← hk]; exact hN
    · intro hk
      exact monotone_intervals_unique (eventTime y xRef z₀ w) (hmono w) T _ _ hN hk
  refine ⟨hraw, hcount, ?_, ?_⟩
  · intro i j hij
    apply Set.disjoint_left.mpr
    intro w hi hj
    exact hij (monotone_intervals_unique (eventTime y xRef z₀ w) (hmono w) T i j
      (hraw i w hi) (hraw j w hj))
  · letI : IsProbabilityMeasure P :=
      AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
    have hfull : ∀ᵐ w ∂P, w ∈ ⋃ k : ℕ, C y xRef z₀ k T := by
      filter_upwards [hAE] with w hw
      obtain ⟨k, hk⟩ := hw.2.1
      exact Set.mem_iUnion.mpr ⟨k, (hw.2.2 k).mp hk⟩
    exact (measure_congr (ae_eq_univ.mpr hfull)).trans (measure_univ : P Set.univ = 1)

private def actual_finite_count_path_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop := by
  classical
  exact
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let readTime : Rec → ℝ := fun r => match r with
      | Sum.inl q => (q.1 : ℝ)
      | Sum.inr _ => 0
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ := fun y xRef z₀ n T t =>
      ∏ i : Fin n,
        rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
          (zAt y xRef z₀ n T t i.castSucc)) *
        Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
          (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
    let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
      ENNReal.ofReal (qReal y xRef z₀ n T t)
    let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
      {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
        StrictMono (fun j => readTime (h j)) ∧
        ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
    let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
      fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
        (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
    let N : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → ℕ := fun y xRef z₀ T w =>
      if h : ∃ n, w ∈ I y xRef z₀ T n then Nat.find h else 0
    let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
    let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
      fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
    let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
      fun y xRef r u e => r.elim
        (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
    let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
      fun y xRef r u => r.elim
        (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
    let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
      fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
        survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
      fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
    let ρ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ≥0∞ :=
      fun y xRef z₀ n T t => q y xRef z₀ n T t *
        weight y xRef ((K y xRef z₀ n T t) ⟨n, Nat.lt_succ_self n⟩)
          (d n T (K y xRef z₀ n T t))
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E), w ∈ I y xRef z₀ s n →
          record y xRef z₀ (ε w) n = Sum.inl a →
          Z y xRef z₀ s w = Φ y xRef ((s - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        (¬ ∃ n, w ∈ I y xRef z₀ s n) → Z y xRef z₀ s w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ w ∂P, Z y xRef z₀ 0 w = z₀) ∧
      (∀ n : ℕ, ∀ T : ℝ≥0,
        Measurable (fun p : ((E × E) × (E × E)) × Hist n =>
          Ψ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
        Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
          Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
        Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
          ρ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
        (∀ y xRef : E, ∀ z₀ : E × E,
          let H := history y xRef z₀ n
          let ZT : (ℕ → ℝ) → Path T := fun w s => Z y xRef z₀ s.val w
          Measurable H ∧ Measurable ZT ∧ Measurable (N y xRef z₀ T) ∧
          MeasurableSet (C y xRef z₀ n T) ∧
          (∀ t : Prefix n T, ∀ s : {s : ℝ≥0 // s ≤ T}, ∀ j : Fin (n + 1),
            (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j ≤ (s.val : ℝ) →
            (∀ k : Fin (n + 1), j < k → (s.val : ℝ) < (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) k) →
            Γ y xRef z₀ n T t s =
              Φ y xRef ((s.val : ℝ) - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j) (zAt y xRef z₀ n T t j)) ∧
          (∀ w ∈ C y xRef z₀ n T, Ψ y xRef z₀ n T (H w) = ZT w) ∧
          (∀ᵐ w ∂P, (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
            (∀ k : ℕ, N y xRef z₀ T w = k ↔ w ∈ C y xRef z₀ k T) ∧
            {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.Finite ∧
            {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.Finite ∧
            N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.ncard ∧
            N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.ncard) ∧
          (Pairwise fun i j : ℕ => Disjoint (C y xRef z₀ i T) (C y xRef z₀ j T)) ∧
          P (⋃ k : ℕ, C y xRef z₀ k T) = 1 ∧
          Measure.map (fun w => (H w, ZT w)) (P.restrict {w | N y xRef z₀ T w = n}) =
            Measure.map (fun t => (K y xRef z₀ n T t, Γ y xRef z₀ n T t))
              ((m n T).withDensity (ρ y xRef z₀ n T)) ∧
          (∀ F : Hist n × Path T → ℝ≥0∞, Measurable F →
            (∫⁻ w in {w | N y xRef z₀ T w = n}, F (H w, ZT w) ∂P) =
              ∫⁻ t : Prefix n T, F (K y xRef z₀ n T t, Γ y xRef z₀ n T t) *
                ρ y xRef z₀ n T t ∂m n T) ∧
          (∫⁻ t : Prefix n T, ρ y xRef z₀ n T t ∂m n T) = P {w | N y xRef z₀ T w = n} ∧
          P {w | N y xRef z₀ T w = n} ≤ 1))

/-- Exact sealed finite-count law; every probability/process ingredient is derived in the proof. -/
theorem actual_finite_count_path_law
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_finite_count_path_statement hα hαβ hV hH hη hβη := by
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
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let readTime : Rec → ℝ := fun r => match r with
    | Sum.inl q => (q.1 : ℝ)
    | Sum.inr _ => 0
  let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
    {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
  let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
  let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
    Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
  let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
    Fin.induction z₀ (fun i z =>
      S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
  let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → Hist n := fun y xRef z₀ n T t j =>
    Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
  let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ := fun y xRef z₀ n T t =>
    ∏ i : Fin n,
      rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
        (zAt y xRef z₀ n T t i.castSucc)) *
      Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
        (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
  let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
      Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
    ENNReal.ofReal (qReal y xRef z₀ n T t)
  let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
    {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
      StrictMono (fun j => readTime (h j)) ∧
      ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
  let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
    fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
      (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
  let N : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → ℕ := fun y xRef z₀ T w =>
    if h : ∃ n, w ∈ I y xRef z₀ T n then Nat.find h else 0
  let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
  let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
    fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
  let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
    fun y xRef r u e => r.elim
      (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
  let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
    fun y xRef r u => r.elim
      (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
  let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
    fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
      survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
  let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
  let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
    fun y xRef z₀ n T h s =>
      Fin.foldl (n + 1) (fun z j => (h j).elim
        (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
        (fun _ => z)) z₀
  let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
    fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
  let ρ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ≥0∞ :=
    fun y xRef z₀ n T t => q y xRef z₀ n T t *
      weight y xRef ((K y xRef z₀ n T t) ⟨n, Nat.lt_succ_self n⟩)
        (d n T (K y xRef z₀ n T t))
  change
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E), w ∈ I y xRef z₀ s n →
          record y xRef z₀ (ε w) n = Sum.inl a →
          Z y xRef z₀ s w = Φ y xRef ((s - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        (¬ ∃ n, w ∈ I y xRef z₀ s n) → Z y xRef z₀ s w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ w ∂P, Z y xRef z₀ 0 w = z₀) ∧
      (∀ n : ℕ, ∀ T : ℝ≥0,
        Measurable (fun p : ((E × E) × (E × E)) × Hist n =>
          Ψ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
        Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
          Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
        Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
          ρ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
        (∀ y xRef : E, ∀ z₀ : E × E,
          let H := history y xRef z₀ n
          let ZT : (ℕ → ℝ) → Path T := fun w s => Z y xRef z₀ s.val w
          Measurable H ∧ Measurable ZT ∧ Measurable (N y xRef z₀ T) ∧
          MeasurableSet (C y xRef z₀ n T) ∧
          (∀ t : Prefix n T, ∀ s : {s : ℝ≥0 // s ≤ T}, ∀ j : Fin (n + 1),
            (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j ≤ (s.val : ℝ) →
            (∀ k : Fin (n + 1), j < k → (s.val : ℝ) < (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) k) →
            Γ y xRef z₀ n T t s =
              Φ y xRef ((s.val : ℝ) - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j) (zAt y xRef z₀ n T t j)) ∧
          (∀ w ∈ C y xRef z₀ n T, Ψ y xRef z₀ n T (H w) = ZT w) ∧
          (∀ᵐ w ∂P, (∀ j : ℕ, 0 < j → eventTime y xRef z₀ w j ≠ (T : WithTop ℝ≥0)) ∧
            (∀ k : ℕ, N y xRef z₀ T w = k ↔ w ∈ C y xRef z₀ k T) ∧
            {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.Finite ∧
            {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.Finite ∧
            N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j < (T : WithTop ℝ≥0)}.ncard ∧
            N y xRef z₀ T w = {j : ℕ | 0 < j ∧ eventTime y xRef z₀ w j ≤ (T : WithTop ℝ≥0)}.ncard) ∧
          (Pairwise fun i j : ℕ => Disjoint (C y xRef z₀ i T) (C y xRef z₀ j T)) ∧
          P (⋃ k : ℕ, C y xRef z₀ k T) = 1 ∧
          Measure.map (fun w => (H w, ZT w)) (P.restrict {w | N y xRef z₀ T w = n}) =
            Measure.map (fun t => (K y xRef z₀ n T t, Γ y xRef z₀ n T t))
              ((m n T).withDensity (ρ y xRef z₀ n T)) ∧
          (∀ F : Hist n × Path T → ℝ≥0∞, Measurable F →
            (∫⁻ w in {w | N y xRef z₀ T w = n}, F (H w, ZT w) ∂P) =
              ∫⁻ t : Prefix n T, F (K y xRef z₀ n T t, Γ y xRef z₀ n T t) *
                ρ y xRef z₀ n T t ∂m n T) ∧
          (∫⁻ t : Prefix n T, ρ y xRef z₀ n T t ∂m n T) = P {w | N y xRef z₀ T w = n} ∧
          P {w | N y xRef z₀ T w = n} ≤ 1))
  obtain ⟨Z, hZM, hZarc, hZfallback, hZzero, hZpath⟩ :=
    actual_history_path_identification hα hαβ hV hH hη hβη
  refine ⟨Z, hZM, hZarc, hZfallback, hZzero, ?_⟩
  intro n T
  have hΨ := actual_history_interpolation_measurable hα hαβ hV hH hη hβη n T
  have hW := actual_terminal_weighted_prefix_tests hα hαβ hV hH hη hβη n T
  refine ⟨hΨ, hW.1, hW.2.1, ?_⟩
  intro y xRef z₀
  let H := history y xRef z₀ n
  let ZT : (ℕ → ℝ) → Path T := fun w s => Z y xRef z₀ s.val w
  have hWL := hW.2.2 y xRef z₀
  have hHM : Measurable H :=
    ((AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law
      hα hαβ hV hH hη hβη n T).2.2.2.2 y xRef z₀).1
  have hZT : Measurable ZT := by
    apply measurable_pi_lambda
    intro s
    exact hZM.comp (f := fun w : ℕ → ℝ => (((y,xRef),z₀),(s.val,w)))
      (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  have hNM : Measurable (N y xRef z₀ T) :=
    (actual_count_selector_measurable hα hαβ hV hH hη hβη).comp
      (f := fun w : ℕ → ℝ => (((y,xRef),z₀),(T,w)))
      (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  have hc := actual_count_event_identification hα hαβ hV hH hη hβη y xRef z₀ T
  have heq : {w | N y xRef z₀ T w = n} =ᵐ[P] C y xRef z₀ n T := by
    filter_upwards [hc.2.1] with w hw
    exact propext (hw.2.1 n)
  have hr : P.restrict {w | N y xRef z₀ T w = n} = P.restrict (C y xRef z₀ n T) :=
    Measure.restrict_congr_set heq
  have hp : ∀ w ∈ C y xRef z₀ n T, Ψ y xRef z₀ n T (H w) = ZT w :=
    hZpath n T y xRef z₀
  refine ⟨hHM, hZT, hNM, hWL.1,
    actual_prescribed_path_interpolation hα hαβ hV hH hη hβη n T y xRef z₀,
    hp, hc.2.1, hc.2.2.1, hc.2.2.2, ?_, ?_, ?_, ?_⟩
  · rw [hr]
    calc
      Measure.map (fun w => (H w, ZT w)) (P.restrict (C y xRef z₀ n T)) =
          Measure.map (fun w => (H w, Ψ y xRef z₀ n T (H w))) (P.restrict (C y xRef z₀ n T)) := by
        apply Measure.map_congr
        exact ae_restrict_of_forall_mem hWL.1 (fun w hw => Prod.ext rfl (hp w hw).symm)
      _ = _ := hWL.2.2.2.1
  · intro F hF
    rw [hr]
    calc
      (∫⁻ w, F (H w, ZT w) ∂P.restrict (C y xRef z₀ n T)) =
          ∫⁻ w, F (H w, Ψ y xRef z₀ n T (H w)) ∂P.restrict (C y xRef z₀ n T) := by
        apply lintegral_congr_ae
        exact ae_restrict_of_forall_mem hWL.1 (fun w hw => congrArg (fun z => F (H w,z)) (hp w hw).symm)
      _ = _ := hWL.2.2.1 F hF
  · exact hWL.2.2.2.2.1.trans (measure_congr heq).symm
  · rw [measure_congr heq]
    exact hWL.2.2.2.2.2

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath
