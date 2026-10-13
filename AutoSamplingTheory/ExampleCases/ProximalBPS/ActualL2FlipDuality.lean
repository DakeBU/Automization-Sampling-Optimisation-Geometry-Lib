import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.SimpleFuncDenseLp

/-! Actual real-L2 momentum-flip duality. The same clock process and expectation family are retained; ASTIS expands the source density step into canonical pullback and continuous pairings. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

private def actual_l2_flip_statement
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
            ∀ T : ℝ≥0, (A T).adjoint =
              J.toContinuousLinearMap.comp ((A T).comp J.toContinuousLinearMap))

set_option maxHeartbeats 2200000
set_option maxRecDepth 12000
theorem actual_l2_flip_duality
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_l2_flip_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_l2_flip_statement
  intro c Φ S rate Λ τ next record P ε history Rec Hist readTime Δ Prefix m zAt K qReal q A eventTime I N liveTime d survival weight C Path Ψ Γ ρ R Vy nu
  obtain ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, h107⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation.actual_l2_expectation_contraction
      hα hαβ hV hH hη hβη
  refine ⟨Z, hZm, hZa, hZf, hZ0, h106, hBorel, ?_⟩
  intro y xRef
  obtain ⟨L, hL0, hL⟩ := h107 y xRef
  refine ⟨L, hL0, hL, ?_⟩
  have hRm : Measurable R := by dsimp [R]; fun_prop
  have hneg : Measure.map (fun p : E => -p) (stdGaussian E) = stdGaussian E := by
    simpa using (stdGaussian_map (LinearIsometryEquiv.neg ℝ (E := E)))
  have hR : MeasurePreserving R (nu y) (nu y) := by
    refine ⟨hRm, ?_⟩
    change Measure.map (Prod.map id (fun p : E => -p))
      (((volume : Measure E).tilted (fun x => -Vy y x)).prod (stdGaussian E)) = _
    rw [← Measure.map_prod_map _ _ measurable_id (by fun_prop), hneg, Measure.map_id]
  refine ⟨hR, ?_⟩
  intro J
  have hJrep (f : Lp ℝ 2 (nu y)) :
      (J f : (E × E) → ℝ) =ᵐ[nu y] fun z => f (R z) :=
    Lp.coeFn_compMeasurePreserving f hR
  have hJJ (f : Lp ℝ 2 (nu y)) : J (J f) = f := by
    apply Lp.ext
    filter_upwards [hJrep (J f), hR.quasiMeasurePreserving.ae_eq_comp (hJrep f)] with z hz hz'
    simpa only [Function.comp_def, R, neg_neg] using hz.trans hz'
  refine ⟨hJrep, hJJ, ?_⟩
  intro T
  have hrep (G : (E × E) → ℝ) (hG : MemLp G 2 (nu y)) :
      (L T (hG.toLp G) : (E × E) → ℝ) =ᵐ[nu y]
        fun z => ∫ w, G (Z y xRef z T w) ∂P := by
    obtain ⟨_, ⟨hOp, he⟩, _⟩ := (hL T).2 G hG
    rw [he]
    exact hOp.coeFn_toLp
  have hsimple (f g : Lp.simpleFunc ℝ 2 (nu y)) :
      ⟪(f : Lp ℝ 2 (nu y)), L T g⟫_ℝ = ⟪J g, L T (J f)⟫_ℝ := by
    let F := Lp.simpleFunc.toSimpleFunc f
    let G := Lp.simpleFunc.toSimpleFunc g
    have hF : MemLp F 2 (nu y) := Lp.simpleFunc.memLp f
    have hG : MemLp G 2 (nu y) := Lp.simpleFunc.memLp g
    have hFrep : (f : (E × E) → ℝ) =ᵐ[nu y] F :=
      (Lp.simpleFunc.toSimpleFunc_eq_toFun f).symm
    have hGrep : (g : (E × E) → ℝ) =ᵐ[nu y] G :=
      (Lp.simpleFunc.toSimpleFunc_eq_toFun g).symm
    have hFto : hF.toLp F = (f : Lp ℝ 2 (nu y)) := by
      apply Lp.ext
      exact hF.coeFn_toLp.trans hFrep.symm
    have hGto : hG.toLp G = (g : Lp ℝ 2 (nu y)) := by
      apply Lp.ext
      exact hG.coeFn_toLp.trans hGrep.symm
    have hFR : MemLp (fun z => F (R z)) 2 (nu y) := hF.comp_measurePreserving hR
    have hJfto : J f = hFR.toLp (fun z => F (R z)) := by
      apply Lp.ext
      exact ((hJrep f).trans (hR.quasiMeasurePreserving.ae_eq_comp hFrep)).trans
        hFR.coeFn_toLp.symm
    have hJg : (J g : (E × E) → ℝ) =ᵐ[nu y] fun z => G (R z) :=
      (hJrep g).trans (hR.quasiMeasurePreserving.ae_eq_comp hGrep)
    have hLg := hrep G hG
    rw [hGto] at hLg
    have hLJf := hrep (fun z => F (R z)) hFR
    rw [← hJfto] at hLJf
    obtain ⟨CF, hCF⟩ := F.exists_forall_norm_le
    obtain ⟨CG, hCG⟩ := G.exists_forall_norm_le
    have hBF : ∀ z, |F z| ≤ max CF 0 := by
      intro z
      exact le_trans (by simpa only [Real.norm_eq_abs] using hCF z) (le_max_left _ _)
    have hBG : ∀ z, |G z| ≤ max CG 0 := by
      intro z
      exact le_trans (by simpa only [Real.norm_eq_abs] using hCG z) (le_max_left _ _)
    have hd := ((h106 y xRef T).2 F G (max CF 0) (max CG 0)
      F.measurable G.measurable (le_max_right _ _) (le_max_right _ _) hBF hBG).2.2
    calc
      ⟪(f : Lp ℝ 2 (nu y)), L T g⟫_ℝ =
          ∫ z, F z * (∫ w, G (Z y xRef z T w) ∂P) ∂nu y := by
        rw [L2.inner_def]
        apply integral_congr_ae
        filter_upwards [hFrep, hLg] with z hz hz'
        simp only [RCLike.inner_apply, conj_trivial, hz, hz', mul_comm]
      _ = ∫ z, G (R z) * (∫ w, F (R (Z y xRef z T w)) ∂P) ∂nu y := hd
      _ = ⟪J g, L T (J f)⟫_ℝ := by
        rw [L2.inner_def]
        apply integral_congr_ae
        filter_upwards [hJg, hLJf] with z hz hz'
        simp only [RCLike.inner_apply, conj_trivial, hz, hz', mul_comm]
  have hpair (f g : Lp ℝ 2 (nu y)) :
      ⟪f, L T g⟫_ℝ = ⟪J g, L T (J f)⟫_ℝ := by
    apply (Lp.simpleFunc.denseRange (E := ℝ) (μ := nu y) (p := 2) (by norm_num)).induction_on₂
      (p := fun f g => ⟪f, L T g⟫_ℝ = ⟪J g, L T (J f)⟫_ℝ) _ hsimple f g
    exact isClosed_eq (continuous_fst.inner ((L T).continuous.comp continuous_snd))
      ((J.continuous.comp continuous_snd).inner
        ((L T).continuous.comp (J.continuous.comp continuous_fst)))
  apply ContinuousLinearMap.ext
  intro f
  apply ext_inner_right ℝ
  intro g
  calc
    ⟪(L T).adjoint f, g⟫_ℝ = ⟪f, L T g⟫_ℝ := (L T).adjoint_inner_left g f
    _ = ⟪J g, L T (J f)⟫_ℝ := hpair f g
    _ = ⟪g, J (L T (J f))⟫_ℝ := by
      rw [← J.inner_map_map g (J (L T (J f))), hJJ]
    _ = ⟪J (L T (J f)), g⟫_ℝ := real_inner_comm _ _

#print axioms actual_l2_flip_duality
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality
