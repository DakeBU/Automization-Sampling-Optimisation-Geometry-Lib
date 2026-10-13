import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.AEEqOfIntegral
import Mathlib.Analysis.InnerProductSpace.Adjoint

/-! Actual PBPS fixed-time L2 expectation contraction. The full literal statement below preserves the original six assumptions and the same global process. ASTIS supplies explicit integrability and quotient-representative construction; no semigroup claim is made. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

private def actual_l2_expectation_statement
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
          ∀ T : ℝ≥0, ‖A T‖ ≤ 1 ∧
            ∀ G : (E × E) → ℝ, ∀ hG : MemLp G 2 (nu y),
              let opG : (E × E) → ℝ := fun z => ∫ w, G (Z y xRef z T w) ∂P
              (∀ᵐ z ∂nu y, Integrable (fun w => G (Z y xRef z T w)) P) ∧
              (∃ hOp : MemLp opG 2 (nu y), A T (hG.toLp G) = hOp.toLp opG) ∧
              (∫ z, |opG z| ^ 2 ∂nu y) ≤ ∫ z, |G z| ^ 2 ∂nu y)

set_option maxHeartbeats 2200000
set_option maxRecDepth 12000
theorem actual_l2_expectation_contraction
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_l2_expectation_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_l2_expectation_statement
  intro c Φ S rate Λ τ next record P ε history Rec Hist readTime Δ Prefix m zAt K qReal q A eventTime I N liveTime d survival weight C Path Ψ Γ ρ R Vy nu
  obtain ⟨Z, hZm, hZa, hZf, hZ0, h106⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality.actual_bounded_gibbs_duality
      hα hαβ hV hH hη hβη
  have hpair_core
      (μ : Measure (E × E)) (ν : Measure (ℕ → ℝ)) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
      (Z : (E × E) × (ℕ → ℝ) → (E × E)) (hZ : MeasurePreserving Z (μ.prod ν) μ) :
      ∃ A : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ, ‖A‖ ≤ 1 ∧
        ∀ f g : Lp ℝ 2 μ,
          ⟪f, A g⟫_ℝ = ∫ p : (E × E) × (ℕ → ℝ), f p.1 * g (Z p) ∂μ.prod ν := by
    have hfst : MeasurePreserving Prod.fst (μ.prod ν) μ := by
      refine ⟨measurable_fst, ?_⟩
      simp only [Measure.map_fst_prod, measure_univ, one_smul]
    let B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 (μ.prod ν) :=
      (Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hfst).toContinuousLinearMap
    let C : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 (μ.prod ν) :=
      (Lp.compMeasurePreservingₗᵢ ℝ Z hZ).toContinuousLinearMap
    let A : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ := B.adjoint.comp C
    have hB : ‖B‖ ≤ 1 := LinearIsometry.norm_toContinuousLinearMap_le _
    have hC : ‖C‖ ≤ 1 := LinearIsometry.norm_toContinuousLinearMap_le _
    refine ⟨A, ?_, ?_⟩
    · calc
        ‖A‖ ≤ ‖B.adjoint‖ * ‖C‖ := ContinuousLinearMap.opNorm_comp_le _ _
        _ = ‖B‖ * ‖C‖ := by rw [ContinuousLinearMap.adjoint.norm_map]
        _ ≤ 1 * 1 := mul_le_mul hB hC (norm_nonneg _) zero_le_one
        _ = 1 := one_mul 1
    · intro f g
      change ⟪f, B.adjoint (C g)⟫_ℝ = _
      rw [ContinuousLinearMap.adjoint_inner_right, L2.inner_def]
      have hb : (B f : (E × E) × (ℕ → ℝ) → ℝ) =ᵐ[μ.prod ν] (fun p => f p.1) :=
        Lp.coeFn_compMeasurePreserving f hfst
      have hc : (C g : (E × E) × (ℕ → ℝ) → ℝ) =ᵐ[μ.prod ν] (fun p => g (Z p)) :=
        Lp.coeFn_compMeasurePreserving g hZ
      apply integral_congr_ae
      filter_upwards [hb, hc] with p hp hq
      rw [hp, hq]
      simp [RCLike.inner_apply, mul_comm]
  have haverage_core
      (μ : Measure (E × E)) (ν : Measure (ℕ → ℝ)) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
      (Z : (E × E) × (ℕ → ℝ) → (E × E)) (hZ : MeasurePreserving Z (μ.prod ν) μ) :
      ∃ A : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ, ‖A‖ ≤ 1 ∧
        ∀ G : (E × E) → ℝ, ∀ hG : MemLp G 2 μ,
          (∀ᵐ x ∂μ, Integrable (fun w => G (Z (x, w))) ν) ∧
          ∃ hOp : MemLp (fun x => ∫ w, G (Z (x, w)) ∂ν) 2 μ,
            A (hG.toLp G) = hOp.toLp (fun x => ∫ w, G (Z (x, w)) ∂ν) := by
    classical
    obtain ⟨A, hA, hpair⟩ := hpair_core μ ν Z hZ
    refine ⟨A, hA, ?_⟩
    intro G hG
    have hfst : MeasurePreserving Prod.fst (μ.prod ν) μ := by
      refine ⟨measurable_fst, ?_⟩
      simp only [Measure.map_fst_prod, measure_univ, one_smul]
    have hprod : Integrable (fun p : (E × E) × (ℕ → ℝ) => G (Z p)) (μ.prod ν) :=
      (hG.comp_measurePreserving hZ).integrable (by norm_num)
    have hop : Integrable (fun x => ∫ w, G (Z (x, w)) ∂ν) μ := hprod.integral_prod_left
    have hAg : Integrable (A (hG.toLp G) : (E × E) → ℝ) μ :=
      (Lp.memLp (A (hG.toLp G))).integrable (by norm_num)
    have heq : (A (hG.toLp G) : (E × E) → ℝ) =ᵐ[μ] (fun x => ∫ w, G (Z (x, w)) ∂ν) := by
      apply Integrable.ae_eq_of_forall_setIntegral_eq _ _ hAg hop
      intro s hs hms
      let i : Lp ℝ 2 μ := indicatorConstLp 2 hs hms.ne (1 : ℝ)
      have hi : (i : (E × E) → ℝ) =ᵐ[μ] s.indicator (fun _ => (1 : ℝ)) := indicatorConstLp_coeFn
      have hi' := hfst.quasiMeasurePreserving.ae_eq hi
      have hg' := hZ.quasiMeasurePreserving.ae_eq hG.coeFn_toLp
      let H : (E × E) × (ℕ → ℝ) → ℝ := fun p => (s.indicator (fun _ => (1 : ℝ)) p.1) * G (Z p)
      have hH : Integrable H (μ.prod ν) := by
        have hfun : H = (Prod.fst ⁻¹' s).indicator (fun p : (E × E) × (ℕ → ℝ) => G (Z p)) := by
          funext p
          by_cases hp : p.1 ∈ s <;> simp [H, Set.indicator, hp]
        rw [hfun]
        exact hprod.indicator (hs.preimage measurable_fst)
      calc
        (∫ x in s, A (hG.toLp G) x ∂μ) = ⟪i, A (hG.toLp G)⟫_ℝ :=
          (L2.inner_indicatorConstLp_one hs hms.ne _).symm
        _ = ∫ p : (E × E) × (ℕ → ℝ), i p.1 * (hG.toLp G) (Z p) ∂μ.prod ν := hpair i (hG.toLp G)
        _ = ∫ p : (E × E) × (ℕ → ℝ), H p ∂μ.prod ν := by
          apply integral_congr_ae
          filter_upwards [hi', hg'] with p hp hq
          change i p.1 = s.indicator (fun _ => (1 : ℝ)) p.1 at hp
          change (hG.toLp G) (Z p) = G (Z p) at hq
          dsimp only [H]
          rw [hp, hq]
        _ = ∫ x, ∫ w, H (x, w) ∂ν ∂μ := integral_prod H hH
        _ = ∫ x, s.indicator (fun _ => (1 : ℝ)) x * (∫ w, G (Z (x, w)) ∂ν) ∂μ := by
          simp only [H, integral_const_mul]
        _ = ∫ x in s, (∫ w, G (Z (x, w)) ∂ν) ∂μ := by
          rw [← integral_indicator hs]
          congr 1
          funext x
          by_cases hx : x ∈ s <;> simp [Set.indicator, hx]
    have hOp : MemLp (fun x => ∫ w, G (Z (x, w)) ∂ν) 2 μ := MemLp.ae_eq heq (Lp.memLp (A (hG.toLp G)))
    refine ⟨hprod.prod_right_ae, hOp, ?_⟩
    apply Lp.ext
    exact heq.trans hOp.coeFn_toLp.symm
  have hsquare_core
      (μ : Measure (E × E)) (G : (E × E) → ℝ) (hG : MemLp G 2 μ) :
      (∫ x, |G x| ^ 2 ∂μ) = ‖hG.toLp G‖ ^ 2 := by
    calc
      (∫ x, |G x| ^ 2 ∂μ) = ∫ x, ⟪(hG.toLp G) x, (hG.toLp G) x⟫_ℝ ∂μ := by
        apply integral_congr_ae
        filter_upwards [hG.coeFn_toLp] with x hx
        rw [hx]
        simp [RCLike.inner_apply, sq_abs, pow_two]
      _ = ⟪hG.toLp G, hG.toLp G⟫_ℝ := rfl
      _ = ‖hG.toLp G‖ ^ 2 := real_inner_self_eq_norm_sq _
  refine ⟨Z, hZm, hZa, hZf, hZ0, h106, ?_, ?_⟩
  · letI : IsProbabilityMeasure P :=
      AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
    intro G hG
    constructor
    · have hmap : Measurable (fun a : (((E × E) × (E × E)) × ℝ≥0) × (ℕ → ℝ) =>
          G (Z a.1.1.1.1 a.1.1.1.2 a.1.1.2 a.1.2 a.2)) :=
        hG.comp (hZm.comp (measurable_fst.fst.prodMk
          (measurable_fst.snd.prodMk measurable_snd)))
      exact hmap.stronglyMeasurable.integral_prod_right.measurable
    · intro C hC hbound y xRef z T
      have hemb : Measurable (fun w : ℕ → ℝ => (((y, xRef), z), T, w)) :=
        measurable_const.prodMk (measurable_const.prodMk measurable_id)
      have hm : Measurable (fun w => G (Z y xRef z T w)) := hG.comp (hZm.comp hemb)
      have hb : ∀ᵐ w ∂P, ‖G (Z y xRef z T w)‖ ≤ C :=
        Filter.Eventually.of_forall fun w => by simpa only [Real.norm_eq_abs] using hbound (Z y xRef z T w)
      refine ⟨Integrable.of_bound hm.aestronglyMeasurable C hb, ?_⟩
      simpa using norm_integral_le_of_norm_le_const hb
  · intro y xRef
    have h103 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization
      hα hαβ hV hH hη hβη y
    letI : IsProbabilityMeasure (nu y) := by
      have hp := h103.2.2.2.2.2.1
      rw [h103.2.2.2.2.2.2] at hp
      exact hp
    letI : IsProbabilityMeasure P :=
      AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
    have hfor : ∀ T : ℝ≥0,
        ∃ L : Lp ℝ 2 (nu y) →L[ℝ] Lp ℝ 2 (nu y), ‖L‖ ≤ 1 ∧
          ∀ G : (E × E) → ℝ, ∀ hG : MemLp G 2 (nu y),
            (∀ᵐ z ∂nu y, Integrable (fun w => G (Z y xRef z T w)) P) ∧
            ∃ hOp : MemLp (fun z => ∫ w, G (Z y xRef z T w) ∂P) 2 (nu y),
              L (hG.toLp G) = hOp.toLp (fun z => ∫ w, G (Z y xRef z T w) ∂P) := by
      intro T
      exact haverage_core (nu y) P (fun a => Z y xRef a.1 T a.2) (h106 y xRef T).1
    choose L hL hrep using hfor
    refine ⟨L, ?_, ?_⟩
    · apply ContinuousLinearMap.ext
      intro f
      obtain ⟨_, hm, he⟩ := hrep 0 (f : (E × E) → ℝ) (Lp.memLp f)
      rw [Lp.toLp_coeFn] at he
      apply Lp.ext
      change (L 0 f : (E × E) → ℝ) =ᵐ[nu y] (f : (E × E) → ℝ)
      have hpoint : ∀ z, (∫ w, f (Z y xRef z 0 w) ∂P) = f z := by
        intro z
        exact integral_eq_const ((hZ0 y xRef z).mono (fun w hw => congrArg f hw))
      rw [he]
      exact hm.coeFn_toLp.trans (Filter.Eventually.of_forall hpoint)
    · intro T
      refine ⟨hL T, ?_⟩
      intro G hG opG
      obtain ⟨hsec, hOp, he⟩ := hrep T G hG
      refine ⟨hsec, ⟨hOp, he⟩, ?_⟩
      rw [hsquare_core (nu y) opG hOp, hsquare_core (nu y) G hG, ← he]
      have hn : ‖L T (hG.toLp G)‖ ≤ ‖hG.toLp G‖ :=
        (ContinuousLinearMap.le_opNorm (L T) (hG.toLp G)).trans
          (mul_le_of_le_one_left (norm_nonneg _) (hL T))
      nlinarith [norm_nonneg (L T (hG.toLp G)), norm_nonneg (hG.toLp G)]

#print axioms actual_l2_expectation_contraction
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation
