import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.MeasureTheory.Function.L2Space

/- Actual Gaussian momentum averaging on the same PBPS process and phase operator. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

private def actual_position_l2_statement
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
theorem actual_position_l2_averaging
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_position_l2_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_position_l2_statement
  intro c Φ S rate Λ τ next record P ε history Rec Hist readTime Δ Prefix m zAt K qReal q A eventTime I N liveTime d survival weight C Path Ψ Γ ρ R Vy nu
  obtain ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, h108⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality.actual_l2_flip_duality
      hα hαβ hV hH hη hβη
  refine ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, ?_⟩
  intro y xRef
  obtain ⟨L, hL0, hL, hR, hJrep, hJJ, hLadj⟩ := h108 y xRef
  refine ⟨L, hL0, hL, hR, ?_⟩
  intro J
  refine ⟨hJrep, hJJ, hLadj, ?_⟩
  intro mu
  have hfst : MeasurePreserving Prod.fst (nu y) mu := measurePreserving_fst
  refine ⟨hfst, ?_⟩
  intro B M
  have hBrep (f : Lp ℝ 2 mu) :
      (B f : (E × E) → ℝ) =ᵐ[nu y] fun z => f z.1 :=
    Lp.coeFn_compMeasurePreserving f hfst
  have hBn : ‖B.toContinuousLinearMap‖ ≤ 1 := B.norm_toContinuousLinearMap_le
  have hMn : ‖M‖ ≤ 1 := by
    change ‖B.toContinuousLinearMap.adjoint‖ ≤ 1
    rw [ContinuousLinearMap.adjoint.norm_map]
    exact hBn
  have hMB : M.comp B.toContinuousLinearMap = ContinuousLinearMap.id ℝ (Lp ℝ 2 mu) :=
    B.adjoint_comp_self
  have havg (G : (E × E) → ℝ) (hG : MemLp G 2 (nu y)) :
      (∀ᵐ x ∂mu, Integrable (fun p => G (x, p)) (stdGaussian E)) ∧
      ∃ hbar : MemLp (fun x => ∫ p, G (x, p) ∂stdGaussian E) 2 mu,
        M (hG.toLp G) = hbar.toLp (fun x => ∫ p, G (x, p) ∂stdGaussian E) := by
    have hprod : Integrable G (mu.prod (stdGaussian E)) := hG.integrable (by norm_num)
    have hbar1 : Integrable (fun x => ∫ p, G (x, p) ∂stdGaussian E) mu :=
      hprod.integral_prod_left
    have hMg : Integrable (M (hG.toLp G) : E → ℝ) mu :=
      (Lp.memLp (M (hG.toLp G))).integrable (by norm_num)
    have heq : (M (hG.toLp G) : E → ℝ) =ᵐ[mu]
        (fun x => ∫ p, G (x, p) ∂stdGaussian E) := by
      apply Integrable.ae_eq_of_forall_setIntegral_eq _ _ hMg hbar1
      intro s hs hms
      let i : Lp ℝ 2 mu := indicatorConstLp 2 hs hms.ne (1 : ℝ)
      have hi : (i : E → ℝ) =ᵐ[mu] s.indicator (fun _ => (1 : ℝ)) :=
        indicatorConstLp_coeFn
      have hi' := hfst.quasiMeasurePreserving.ae_eq hi
      let H : E × E → ℝ := fun z => s.indicator (fun _ => (1 : ℝ)) z.1 * G z
      have hH : Integrable H (mu.prod (stdGaussian E)) := by
        have hfun : H = (Prod.fst ⁻¹' s).indicator G := by
          funext z
          by_cases hz : z.1 ∈ s <;> simp [H, Set.indicator, hz]
        rw [hfun]
        exact hprod.indicator (hs.preimage measurable_fst)
      calc
        (∫ x in s, M (hG.toLp G) x ∂mu) = ⟪i, M (hG.toLp G)⟫_ℝ :=
          (L2.inner_indicatorConstLp_one hs hms.ne _).symm
        _ = ⟪B i, hG.toLp G⟫_ℝ := ContinuousLinearMap.adjoint_inner_right _ _ _
        _ = ∫ z, H z ∂nu y := by
          rw [L2.inner_def]
          apply integral_congr_ae
          filter_upwards [hBrep i, hi', hG.coeFn_toLp] with z hb hi hg
          change i z.1 = s.indicator (fun _ => (1 : ℝ)) z.1 at hi
          simp only [hb, hi, hg, H, RCLike.inner_apply, conj_trivial]
          exact mul_comm _ _
        _ = ∫ x, ∫ p, H (x, p) ∂stdGaussian E ∂mu := integral_prod H hH
        _ = ∫ x, s.indicator (fun _ => (1 : ℝ)) x *
            (∫ p, G (x, p) ∂stdGaussian E) ∂mu := by
          simp only [H, integral_const_mul]
        _ = ∫ x in s, (∫ p, G (x, p) ∂stdGaussian E) ∂mu := by
          rw [← integral_indicator hs]
          congr 1
          funext x
          by_cases hx : x ∈ s <;> simp [Set.indicator, hx]
    have hbar : MemLp (fun x => ∫ p, G (x, p) ∂stdGaussian E) 2 mu :=
      MemLp.ae_eq heq (Lp.memLp (M (hG.toLp G)))
    refine ⟨hprod.prod_right_ae, hbar, ?_⟩
    apply Lp.ext
    exact heq.trans hbar.coeFn_toLp.symm
  have hJB (f : Lp ℝ 2 mu) : J (B f) = B f := by
    apply Lp.ext
    filter_upwards [hJrep (B f), hR.quasiMeasurePreserving.ae_eq_comp (hBrep f),
      hBrep f] with z hj hb hb'
    change (J (B f)) z = (B f) z
    rw [hj, hb']
    simpa only [Function.comp_def, R] using hb
  have hJadj : J.toContinuousLinearMap.adjoint = J.toContinuousLinearMap := by
    apply ContinuousLinearMap.ext
    intro f
    apply ext_inner_right ℝ
    intro g
    rw [ContinuousLinearMap.adjoint_inner_left]
    change ⟪f, J g⟫_ℝ = ⟪J f, g⟫_ℝ
    calc
      ⟪f, J g⟫_ℝ = ⟪J f, J (J g)⟫_ℝ := (J.inner_map_map f (J g)).symm
      _ = ⟪J f, g⟫_ℝ := by rw [hJJ]
  have hJBmap : J.toContinuousLinearMap.comp B.toContinuousLinearMap = B.toContinuousLinearMap :=
    ContinuousLinearMap.ext hJB
  have hMJ : M.comp J.toContinuousLinearMap = M := by
    have hh := congrArg (fun U => ContinuousLinearMap.adjoint U) hJBmap
    simpa only [ContinuousLinearMap.adjoint_comp, hJadj] using hh
  refine ⟨hBrep, hBn, hMn, hMB, havg, hJB, hMJ, ?_⟩
  intro Kpos
  refine ⟨?_, ?_⟩
  · change M.comp ((L 0).comp B.toContinuousLinearMap) = _
    rw [hL0, ContinuousLinearMap.id_comp, hMB]
  · intro T
    refine ⟨?_, ?_, ?_⟩
    · change (M.comp ((L T).comp B.toContinuousLinearMap)).adjoint = _
      rw [ContinuousLinearMap.adjoint_comp, ContinuousLinearMap.adjoint_comp]
      change (M.comp (L T).adjoint).comp B.toContinuousLinearMap.adjoint.adjoint = _
      rw [ContinuousLinearMap.adjoint_adjoint, hLadj T]
      apply ContinuousLinearMap.ext
      intro f
      change M (J (L T (J (B f)))) = M (L T (B f))
      rw [hJB]
      exact congrArg (fun U : Lp ℝ 2 (nu y) →L[ℝ] Lp ℝ 2 mu => U (L T (B f))) hMJ
    · change ‖M.comp ((L T).comp B.toContinuousLinearMap)‖ ≤ 1
      have hn : ‖(L T).comp B.toContinuousLinearMap‖ ≤ 1 := by
        calc
          _ ≤ ‖L T‖ * ‖B.toContinuousLinearMap‖ := ContinuousLinearMap.opNorm_comp_le _ _
          _ ≤ 1 * 1 := mul_le_mul (hL T).1 hBn (norm_nonneg _) zero_le_one
          _ = 1 := one_mul 1
      calc
        _ ≤ ‖M‖ * ‖(L T).comp B.toContinuousLinearMap‖ := ContinuousLinearMap.opNorm_comp_le _ _
        _ ≤ 1 * 1 := mul_le_mul hMn hn (norm_nonneg _) zero_le_one
        _ = 1 := one_mul 1
    · intro f hf kTf
      let F : E × E → ℝ := fun z => f z.1
      have hF : MemLp F 2 (nu y) := hf.comp_measurePreserving hfst
      have hBF : B (hf.toLp f) = hF.toLp F := by
        apply Lp.ext
        exact (hBrep (hf.toLp f)).trans
          ((hfst.quasiMeasurePreserving.ae_eq_comp hf.coeFn_toLp).trans hF.coeFn_toLp.symm)
      obtain ⟨hsec, ⟨hop, heop⟩, _⟩ := (hL T).2 F hF
      obtain ⟨houter, hk, he⟩ := havg (fun z => ∫ w, F (Z y xRef z T w) ∂P) hop
      refine ⟨Measure.ae_ae_of_ae_prod hsec, houter, hk, ?_⟩
      change M (L T (B (hf.toLp f))) = _
      rw [hBF, heop]
      exact he

#print axioms actual_position_l2_averaging
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging
