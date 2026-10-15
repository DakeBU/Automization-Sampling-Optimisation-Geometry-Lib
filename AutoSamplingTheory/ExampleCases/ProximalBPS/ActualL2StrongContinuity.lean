import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity
import Mathlib.MeasureTheory.Function.ContinuousMapDense
import Mathlib.Topology.MetricSpace.Equicontinuity
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.MeasureTheory.Function.L2Space

/- PBPS zero-time L2 strong continuity; preserved actual process and averaging. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2StrongContinuity
open MeasureTheory InnerProductSpace ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Classical Topology
noncomputable section
set_option autoImplicit false

private def actual_l2_strong_continuity_statement
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
    let R : E × E → E × E := fun z => (z.1, -z.2)
    let Vy : E → E → ℝ := fun y x => V x + ‖x - y‖ ^ 2 / (2 * η)
    let nu : E → Measure (E × E) := fun y =>
      ((volume : Measure E).tilted (fun x => -Vy y x)).prod
        (ProbabilityTheory.stdGaussian E)
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
      (∀ y xRef : E, ∀ T : ℝ≥0,
        let op : ((E × E) → ℝ) → (E × E) → ℝ :=
          fun G z => ∫ w, G (Z y xRef z T w) ∂P
        let endpoint : (E × E) × (ℕ → ℝ) → E × E :=
          fun a => Z y xRef a.1 T a.2
        MeasurePreserving endpoint ((nu y).prod P) (nu y) ∧
        ∀ F G : (E × E) → ℝ, ∀ C_F C_G : ℝ,
          Measurable F → Measurable G → 0 ≤ C_F → 0 ≤ C_G →
          (∀ z, |F z| ≤ C_F) → (∀ z, |G z| ≤ C_G) →
          Integrable (fun z => F z * op G z) (nu y) ∧
          Integrable (fun z => G (R z) * op (fun a => F (R a)) z) (nu y) ∧
          (∫ z, F z * op G z ∂nu y) =
            ∫ z, G (R z) * op (fun a => F (R a)) z ∂nu y) ∧
      (∀ G : (E × E) → ℝ, Measurable G →
        Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
          ∫ w, G (Z a.1.1.1 a.1.1.2 a.1.2 a.2 w) ∂P) ∧
        ∀ C : ℝ, 0 ≤ C → (∀ z, |G z| ≤ C) →
          ∀ y xRef : E, ∀ z : E × E, ∀ T : ℝ≥0,
            Integrable (fun w => G (Z y xRef z T w)) P ∧
            |∫ w, G (Z y xRef z T w) ∂P| ≤ C) ∧
      (∀ y xRef : E,
        ∃ A : ℝ≥0 → (Lp ℝ 2 (nu y) →L[ℝ] Lp ℝ 2 (nu y)),
          A 0 = ContinuousLinearMap.id ℝ (Lp ℝ 2 (nu y)) ∧
          (∀ f : Lp ℝ 2 (nu y),
            Tendsto (fun t : ℝ≥0 => A t f) (𝓝 0) (𝓝 f)) ∧
          (∀ T : ℝ≥0, ‖A T‖ ≤ 1 ∧
            ∀ G : (E × E) → ℝ, ∀ hG : MemLp G 2 (nu y),
              let opG : (E × E) → ℝ := fun z => ∫ w, G (Z y xRef z T w) ∂P
              (∀ᵐ z ∂nu y, Integrable (fun w => G (Z y xRef z T w)) P) ∧
              (∃ hOp : MemLp opG 2 (nu y), A T (hG.toLp G) = hOp.toLp opG) ∧
              (∫ z, |opG z| ^ 2 ∂nu y) ≤ ∫ z, |G z| ^ 2 ∂nu y) ∧
          ∃ hR : MeasurePreserving R (nu y) (nu y),
            let J : Lp ℝ 2 (nu y) →ₗᵢ[ℝ] Lp ℝ 2 (nu y) :=
              Lp.compMeasurePreservingₗᵢ ℝ R hR
            (∀ f : Lp ℝ 2 (nu y),
              (J f : (E × E) → ℝ) =ᵐ[nu y] fun z => f (R z)) ∧
            (∀ f : Lp ℝ 2 (nu y), J (J f) = f) ∧
            (∀ T : ℝ≥0, (A T).adjoint =
              J.toContinuousLinearMap.comp ((A T).comp J.toContinuousLinearMap)) ∧
            let mu : Measure E := (volume : Measure E).tilted (fun x => -Vy y x)
            ∃ hfst : MeasurePreserving Prod.fst (nu y) mu,
              let B : Lp ℝ 2 mu →ₗᵢ[ℝ] Lp ℝ 2 (nu y) :=
                Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hfst
              let M : Lp ℝ 2 (nu y) →L[ℝ] Lp ℝ 2 mu := B.toContinuousLinearMap.adjoint
              (∀ f : Lp ℝ 2 mu, (B f : (E × E) → ℝ) =ᵐ[nu y] fun z => f z.1) ∧
              ‖B.toContinuousLinearMap‖ ≤ 1 ∧ ‖M‖ ≤ 1 ∧
              M.comp B.toContinuousLinearMap = ContinuousLinearMap.id ℝ (Lp ℝ 2 mu) ∧
              (∀ G : (E × E) → ℝ, ∀ hG : MemLp G 2 (nu y),
                let gbar : E → ℝ := fun x => ∫ p, G (x, p) ∂stdGaussian E
                (∀ᵐ x ∂mu, Integrable (fun p => G (x, p)) (stdGaussian E)) ∧
                ∃ hbar : MemLp gbar 2 mu, M (hG.toLp G) = hbar.toLp gbar) ∧
              (∀ f : Lp ℝ 2 mu, J (B f) = B f) ∧
              M.comp J.toContinuousLinearMap = M ∧
              let Kpos : ℝ≥0 → (Lp ℝ 2 mu →L[ℝ] Lp ℝ 2 mu) :=
                fun T => M.comp ((A T).comp B.toContinuousLinearMap)
              Kpos 0 = ContinuousLinearMap.id ℝ (Lp ℝ 2 mu) ∧
              ∀ T : ℝ≥0, (Kpos T).adjoint = Kpos T ∧ ‖Kpos T‖ ≤ 1 ∧
                ∀ f : E → ℝ, ∀ hf : MemLp f 2 mu,
                  let kTf : E → ℝ := fun x =>
                    ∫ p, (∫ w, f ((Z y xRef (x, p) T w).1) ∂P) ∂stdGaussian E
                  (∀ᵐ x ∂mu, ∀ᵐ p ∂stdGaussian E,
                    Integrable (fun w => f ((Z y xRef (x, p) T w).1)) P) ∧
                  (∀ᵐ x ∂mu, Integrable
                    (fun p => ∫ w, f ((Z y xRef (x, p) T w).1) ∂P) (stdGaussian E)) ∧
                  ∃ hk : MemLp kTf 2 mu, Kpos T (hf.toLp f) = hk.toLp kTf)



set_option maxHeartbeats 2200000
set_option maxRecDepth 12000
open scoped BoundedContinuousFunction

/-- Zero-time strong continuity for every real L2 observable of the same actual
PBPS phase process, retaining its previously proved flip and averaging laws.
This is only the zero-time component of Proposition A.1(ii), not a semigroup law. -/
theorem actual_l2_strong_continuity
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_l2_strong_continuity_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_l2_strong_continuity_statement
  intro c Φ S rate Λ τ next record P ε history Rec Hist readTime Δ Prefix m zAt K qReal q A eventTime I N liveTime d survival weight C Path Ψ Γ ρ R Vy nu
  obtain ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, h109⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging.actual_position_l2_averaging
      hα hαβ hV hH hη hβη
  obtain ⟨Zb, hZbm, hZba, hZbf, hZbAE, hshort, htest, houter⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity
      hα hαβ hV hH hη hβη
  have hZeq : Zb = Z := by
    funext y xRef z t w
    by_cases hx : ∃ n, w ∈ I y xRef z t n
    · obtain ⟨n, hn⟩ := hx
      obtain ⟨a, ha⟩ : ∃ a, record y xRef z (ε w) n = Sum.inl a := by
        cases hr : record y xRef z (ε w) n with
        | inl a => exact ⟨a, rfl⟩
        | inr u =>
          have hh := hn.1
          change (record y xRef z (ε w) n).elim
            (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤) ≤ (t : WithTop ℝ≥0) at hh
          rw [hr] at hh
          exact False.elim ((WithTop.not_top_le_coe t) hh)
      exact (hZba y xRef z w t n a hn.1 hn.2 ha).trans
        (hZa y xRef z w t n a hn ha).symm
    · exact (hZbf y xRef z w t hx).trans (hZf y xRef z w t hx).symm
  rw [hZeq] at houter
  refine ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, ?_⟩
  intro y xRef
  obtain ⟨L, hL0, hL, hR, hJ⟩ := h109 y xRef
  refine ⟨L, hL0, ?_, hL, hR, hJ⟩
  have hnu :
      ((volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))).prod
        (stdGaussian E) = nu y := by
    apply congrArg (fun μ : Measure E => μ.prod (stdGaussian E))
    apply congrArg ((volume : Measure E).tilted)
    funext x
    dsimp only [Vy]
    ring
  letI : IsProbabilityMeasure (nu y) := by
    rw [← hnu]
    exact (houter.1 y).2
  have hcore (g : (E × E) →ᵇ ℝ) :
      Tendsto (fun t : ℝ≥0 => L t (BoundedContinuousFunction.toLp 2 (nu y) ℝ g))
        (𝓝 0) (𝓝 (BoundedContinuousFunction.toLp 2 (nu y) ℝ g)) := by
    let f : Lp ℝ 2 (nu y) := BoundedContinuousFunction.toLp 2 (nu y) ℝ g
    have hf : (f : (E × E) → ℝ) =ᵐ[nu y] g :=
      BoundedContinuousFunction.coeFn_toLp 2 (nu y) ℝ g
    have hg : MemLp g 2 (nu y) := MemLp.ae_eq hf (Lp.memLp f)
    have hfg : hg.toLp g = f := by
      apply Lp.ext
      exact hg.coeFn_toLp.trans hf.symm
    have hlimit := (houter.2 y xRef g g.continuous ‖g‖ (norm_nonneg g)
      (fun z => by simpa only [Real.norm_eq_abs] using g.norm_coe_le_norm z)).2
    dsimp only at hlimit
    rw [hnu] at hlimit
    have hnorm (t : ℝ≥0) :
        ‖L t f - f‖ ^ 2 =
          ∫ z, ((∫ w, g (Z y xRef z t w) ∂P) - g z) ^ 2 ∂nu y := by
      obtain ⟨_, ⟨hop, he⟩, _⟩ := (hL t).2 g hg
      rw [hfg] at he
      have ha : (L t f : (E × E) → ℝ) =ᵐ[nu y]
          (fun z => ∫ w, g (Z y xRef z t w) ∂P) := by
        rw [he]
        exact hop.coeFn_toLp
      rw [← real_inner_self_eq_norm_sq (L t f - f), L2.inner_def]
      apply integral_congr_ae
      filter_upwards [Lp.coeFn_sub (L t f) f, ha, hf] with z hz hzA hzf
      simp only [hz, Pi.sub_apply, hzA, hzf, RCLike.inner_apply, conj_trivial, pow_two]
    have hnormlimit : Tendsto (fun t : ℝ≥0 => ‖L t f - f‖ ^ 2) (𝓝 0) (𝓝 0) := by
      simpa only [hnorm] using hlimit
    have hsqrt := (Real.continuous_sqrt.tendsto 0).comp hnormlimit
    change Tendsto (fun t : ℝ≥0 => Real.sqrt (‖L t f - f‖ ^ 2))
      (𝓝 0) (𝓝 (Real.sqrt 0)) at hsqrt
    have hzero : Tendsto (fun t : ℝ≥0 => ‖L t f - f‖) (𝓝 0) (𝓝 0) := by
      simpa only [Real.sqrt_sq_eq_abs, abs_norm, Real.sqrt_zero] using hsqrt
    exact tendsto_iff_norm_sub_tendsto_zero.mpr hzero
  have hequi : Equicontinuous (fun t : ℝ≥0 => fun f : Lp ℝ 2 (nu y) => L t f) := by
    apply Metric.equicontinuous_of_continuity_modulus id tendsto_id
    intro f g t
    have hlip : LipschitzWith 1 (L t) :=
      ContinuousLinearMap.lipschitzWith_of_opNorm_le (hL t).1
    simpa only [id_eq, NNReal.coe_one, one_mul] using hlip.dist_le_mul f g
  have hclosed : IsClosed {f : Lp ℝ 2 (nu y) |
      Tendsto (fun t : ℝ≥0 => L t f) (𝓝 0) (𝓝 f)} :=
    hequi.isClosed_setOfPred_tendsto continuous_id
  have hdense : DenseRange (BoundedContinuousFunction.toLp 2 (nu y) ℝ :
      ((E × E) →ᵇ ℝ) →L[ℝ] Lp ℝ 2 (nu y)) :=
    BoundedContinuousFunction.toLp_denseRange ℝ (nu y) ℝ (by norm_num)
  have hsubset : Set.range (BoundedContinuousFunction.toLp 2 (nu y) ℝ :
      ((E × E) →ᵇ ℝ) →L[ℝ] Lp ℝ 2 (nu y)) ⊆
      {f : Lp ℝ 2 (nu y) | Tendsto (fun t : ℝ≥0 => L t f) (𝓝 0) (𝓝 f)} := by
    rintro _ ⟨g, rfl⟩
    exact hcore g
  intro f
  exact closure_minimal hsubset hclosed (hdense f)

#print axioms actual_l2_strong_continuity
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2StrongContinuity
