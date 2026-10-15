import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2StrongContinuity
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel
import Mathlib.Probability.Kernel.Invariance

/-!
# Actual PBPS probability kernel and real-L2 realization

The fixed-reference phase law in arXiv:2609.06905v1 Appendix A.1 is joined
to its observable operator in Definition D.2 on the SAME actual path witness.
All six original analytic hypotheses are retained; kernel invariance, fiber
integrability, AE representative equality, positivity and constants are derived.
Probability fibers do not establish process Markovness or a semigroup law.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualKernelL2Realization
open MeasureTheory InnerProductSpace ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Classical Topology
noncomputable section
set_option autoImplicit false

private def actual_kernel_l2_realization_statement
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
      (∃ Kphase : Kernel (((E × E) × (E × E)) × ℝ≥0) (E × E),
        IsMarkovKernel Kphase ∧
        (∀ y xRef : E, ∀ z : E × E, ∀ T : ℝ≥0,
          Kphase (((y, xRef), z), T) = Measure.map (Z y xRef z T) P) ∧
        (∀ y xRef : E, ∀ T : ℝ≥0,
          (Kphase.comap (fun z : E × E => (((y, xRef), z), T))
            (by fun_prop)).Invariant (nu y)) ∧
      (∀ y xRef : E,
        ∃ A : ℝ≥0 → (Lp ℝ 2 (nu y) →L[ℝ] Lp ℝ 2 (nu y)),
          A 0 = ContinuousLinearMap.id ℝ (Lp ℝ 2 (nu y)) ∧
          (∀ f : Lp ℝ 2 (nu y),
            Tendsto (fun t : ℝ≥0 => A t f) (𝓝 0) (𝓝 f)) ∧
          (∀ T : ℝ≥0, ∀ f : Lp ℝ 2 (nu y),
            (∀ᵐ z ∂nu y, Integrable (f : (E × E) → ℝ)
              (Kphase (((y, xRef), z), T))) ∧
            (A T f : (E × E) → ℝ) =ᵐ[nu y]
              fun z => ∫ z', f z' ∂Kphase (((y, xRef), z), T)) ∧
          (∀ T : ℝ≥0, ∀ f : Lp ℝ 2 (nu y),
            (∀ᵐ z ∂nu y, 0 ≤ f z) → ∀ᵐ z ∂nu y, 0 ≤ A T f z) ∧
          (∀ T : ℝ≥0, ∀ r : ℝ,
            ∃ hr : MemLp (fun _ : E × E => r) 2 (nu y),
              A T (hr.toLp (fun _ : E × E => r)) =
                hr.toLp (fun _ : E × E => r)) ∧
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
                  ∃ hk : MemLp kTf 2 mu, Kpos T (hf.toLp f) = hk.toLp kTf))

set_option maxHeartbeats 2200000
set_option maxRecDepth 12000

/-- The actual fixed-reference phase kernel preserves its Gibbs law and realizes
the same real-L2 family, with AE positivity and every constant class fixed.
This does not prove process Markovness, restart or Chapman--Kolmogorov. -/
theorem actual_kernel_l2_realization
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_kernel_l2_realization_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_kernel_l2_realization_statement
  intro c Φ S rate Λ τ next record P ε history Rec Hist readTime Δ Prefix m zAt K qReal q A eventTime I N liveTime d survival weight C Path Ψ Γ ρ R Vy nu
  obtain ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, h110⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2StrongContinuity.actual_l2_strong_continuity
      hα hαβ hV hH hη hβη
  obtain ⟨Zk, _hZkm, hZka, hZkf, _hZkgood,
      Kphase, hK, hfiber, _hset, _hinit, _hbounded⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel.actual_phase_transition_kernel
      hα hαβ hV hH hη hβη
  -- Same literal recursion and raw fallback identify the two path witnesses.
  have hZeq : Zk = Z := by
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
      exact (hZka y xRef z w t n a hn.1 hn.2 ha).trans
        (hZa y xRef z w t n a hn ha).symm
    · exact (hZkf y xRef z w t hx).trans (hZf y xRef z w t hx).symm
  rw [hZeq] at hfiber
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  letI : IsMarkovKernel Kphase := hK
  have hzM (y xRef : E) (z : E × E) (T : ℝ≥0) :
      Measurable (Z y xRef z T) := hZm.comp
    (show Measurable (fun w : ℕ → ℝ => (((y, xRef), z), T, w)) from
      measurable_const.prodMk (measurable_const.prodMk measurable_id))
  -- A fixed-time endpoint pushforward, not a restart/Markov argument.
  have hInv (y xRef : E) (T : ℝ≥0) :
      (Kphase.comap (fun z : E × E => (((y, xRef), z), T))
        (by fun_prop)).Invariant (nu y) := by
    let κ : Kernel (E × E) (E × E) :=
      Kphase.comap (fun z : E × E => (((y, xRef), z), T)) (by fun_prop)
    have he := (h106 y xRef T).1
    change (nu y).bind κ = nu y
    calc
      (nu y).bind κ =
          Measure.map (fun a : (E × E) × (ℕ → ℝ) => Z y xRef a.1 T a.2)
            ((nu y).prod P) := by
        ext s hs
        rw [Measure.bind_apply hs κ.aemeasurable, Measure.map_apply he.measurable hs,
          Measure.prod_apply (he.measurable hs)]
        apply lintegral_congr_ae
        filter_upwards with z
        change Kphase (((y, xRef), z), T) s =
          P ((Z y xRef z T) ⁻¹' s)
        rw [hfiber, Measure.map_apply (hzM y xRef z T) hs]
      _ = nu y := he.map_eq
  refine ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, Kphase, hK, hfiber, hInv, ?_⟩
  intro y xRef
  obtain ⟨L, hL0, hSC, hL, hRest⟩ := h110 y xRef
  have hnorm := ActualPhaseNormalization.actual_phase_gibbs_normalization
    hα hαβ hV hH hη hβη y
  letI : IsProbabilityMeasure (nu y) := by
    have hp := hnorm.2.2.2.2.2.1
    rw [hnorm.2.2.2.2.2.2] at hp
    exact hp
  have hreal (T : ℝ≥0) (f : Lp ℝ 2 (nu y)) :
      (∀ᵐ z ∂nu y, Integrable (f : (E × E) → ℝ)
        (Kphase (((y, xRef), z), T))) ∧
      (L T f : (E × E) → ℝ) =ᵐ[nu y]
        fun z => ∫ z', f z' ∂Kphase (((y, xRef), z), T) := by
    let opG : (E × E) → ℝ := fun z => ∫ w, f (Z y xRef z T w) ∂P
    have hclock := (hL T).2 (f : (E × E) → ℝ) (Lp.memLp f)
    obtain ⟨hOp, heq⟩ := hclock.2.1
    have heq' : L T f = hOp.toLp opG := by
      simpa only [Lp.toLp_coeFn] using heq
    have hae : (L T f : (E × E) → ℝ) =ᵐ[nu y] opG := by
      rw [heq']
      exact hOp.coeFn_toLp
    have hinter (z : E × E) :
        (∫ z', f z' ∂Kphase (((y, xRef), z), T)) = opG z := by
      rw [hfiber]
      exact integral_map (hzM y xRef z T).aemeasurable
        (Lp.stronglyMeasurable f).aestronglyMeasurable
    refine ⟨?_, ?_⟩
    · filter_upwards [hclock.1] with z hz
      rw [hfiber]
      exact (integrable_map_measure
        (Lp.stronglyMeasurable f).aestronglyMeasurable (hzM y xRef z T).aemeasurable).2 hz
    · filter_upwards [hae] with z hz
      exact hz.trans (hinter z).symm
  refine ⟨L, hL0, hSC, hreal, ?_, ?_, hL, hRest⟩
  · intro T f hf
    let κ : Kernel (E × E) (E × E) :=
      Kphase.comap (fun z : E × E => (((y, xRef), z), T)) (by fun_prop)
    have hcomp : ∀ᵐ z ∂((nu y).bind κ), 0 ≤ f z := by
      rw [(hInv y xRef T).def]
      exact hf
    have hfib := Measure.ae_ae_of_ae_comp (κ := κ) hcomp
    filter_upwards [(hreal T f).2, hfib] with z hz hzz
    rw [hz]
    exact integral_nonneg_of_ae hzz
  · intro T r
    have hr : MemLp (fun _ : E × E => r) 2 (nu y) := memLp_const r
    let f : Lp ℝ 2 (nu y) := hr.toLp (fun _ : E × E => r)
    let κ : Kernel (E × E) (E × E) :=
      Kphase.comap (fun z : E × E => (((y, xRef), z), T)) (by fun_prop)
    have hcae : (f : (E × E) → ℝ) =ᵐ[nu y] fun _ => r := hr.coeFn_toLp
    have hcomp : ∀ᵐ z ∂((nu y).bind κ), f z = r := by
      rw [(hInv y xRef T).def]
      exact hcae
    have hfib := Measure.ae_ae_of_ae_comp (κ := κ) hcomp
    refine ⟨hr, ?_⟩
    change L T f = f
    apply Lp.ext
    filter_upwards [(hreal T f).2, hcae, hfib] with z hz hzr hfz
    calc
      L T f z = ∫ z', f z' ∂Kphase (((y, xRef), z), T) := hz
      _ = ∫ _ : E × E, r ∂Kphase (((y, xRef), z), T) := integral_congr_ae hfz
      _ = r := by simp
      _ = f z := hzr.symm

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualKernelL2Realization

