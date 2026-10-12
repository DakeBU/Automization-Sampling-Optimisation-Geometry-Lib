import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/- Actual bounded signed Gibbs duality and fixed-time phase invariance,
under the original PBPS analytic assumptions. ASTIS completion of Appendix A.1. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

private def actual_bounded_gibbs_duality_statement
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
            ∫ z, G (R z) * op (fun a => F (R a)) z ∂nu y)


set_option maxHeartbeats 1800000
set_option maxRecDepth 10000
/-- One actual global PBPS process preserves the Gibbs phase law at each fixed time and satisfies bounded signed momentum-flipped duality. -/
theorem actual_bounded_gibbs_duality
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_bounded_gibbs_duality_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_bounded_gibbs_duality_statement
  intro c Φ S rate Λ τ next record P ε history Rec Hist readTime Δ Prefix m zAt K qReal q A eventTime I N liveTime d survival weight C Path Ψ Γ ρ R Vy nu
  obtain ⟨Z, hZm, hZa, hZf, hZ0, h105⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw.actual_countable_endpoint_law
      hα hαβ hV hH hη hβη
  refine ⟨Z, hZm, hZa, hZf, hZ0, ?_⟩
  intro y r T op endpoint
  have h103 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization
    hα hαβ hV hH hη hβη y
  letI : IsProbabilityMeasure (nu y) := by
    have hp := h103.2.2.2.2.2.1
    rw [h103.2.2.2.2.2.2] at hp
    exact hp
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  have hemb : Measurable (fun a : (E × E) × (ℕ → ℝ) => (((y, r), a.1), T, a.2)) :=
    (measurable_const.prodMk measurable_fst).prodMk (measurable_const.prodMk measurable_snd)
  have he : Measurable endpoint := hZm.comp hemb
  let M : (E × E) × (ℕ → ℝ) → (E × E) × (E × E) := fun a => (a.1, endpoint a)
  let Q : Measure ((E × E) × (E × E)) := Measure.map M ((nu y).prod P)
  let J : (E × E) × (E × E) → (E × E) × (E × E) := fun a => (R a.2, R a.1)
  have hM : Measurable M := measurable_fst.prodMk he
  have hJ : MeasurePreserving J Q Q := (h105 y r T).2.2
  letI : IsProbabilityMeasure Q := (h105 y r T).2.1
  have hRm : Measurable R := by dsimp [R]; fun_prop
  have hneg : Measure.map (fun p : E => -p) (stdGaussian E) = stdGaussian E := by
    simpa using (stdGaussian_map (LinearIsometryEquiv.neg ℝ (E := E)))
  have hR : MeasurePreserving R (nu y) (nu y) := by
    refine ⟨hRm, ?_⟩
    change Measure.map (Prod.map id (fun p : E => -p))
      (((volume : Measure E).tilted (fun x => -Vy y x)).prod (stdGaussian E)) = _
    rw [← Measure.map_prod_map _ _ measurable_id (by fun_prop), hneg, Measure.map_id]
  have hMP : MeasurePreserving M ((nu y).prod P) Q := ⟨hM, rfl⟩
  have hfst : MeasurePreserving Prod.fst Q (nu y) := by
    refine ⟨measurable_fst, ?_⟩
    change Measure.map Prod.fst (Measure.map M ((nu y).prod P)) = nu y
    rw [Measure.map_map measurable_fst hM]
    change Measure.map Prod.fst ((nu y).prod P) = nu y
    simp only [Measure.map_fst_prod, measure_univ, one_smul]
  have hinvariant : MeasurePreserving endpoint ((nu y).prod P) (nu y) := by
    have h := hR.comp ((hfst.comp hJ).comp hMP)
    simpa only [Function.comp_def, M, J, R, neg_neg] using h
  refine ⟨hinvariant, ?_⟩
  have htest (F G : (E × E) → ℝ) (CF CG : ℝ)
      (hF : Measurable F) (hG : Measurable G) (hCF : 0 ≤ CF) (hCG : 0 ≤ CG)
      (hFb : ∀ z, |F z| ≤ CF) (hGb : ∀ z, |G z| ≤ CG) :
      Integrable (fun z => F z * op G z) (nu y) ∧
      (∫ z, F z * op G z ∂nu y) = ∫ a, F a.1 * G a.2 ∂Q := by
    let H : (E × E) × (ℕ → ℝ) → ℝ := fun a => F a.1 * G (endpoint a)
    have hHm : Measurable H := (hF.comp measurable_fst).mul (hG.comp he)
    have hHi : Integrable H ((nu y).prod P) :=
      Integrable.of_bound hHm.aestronglyMeasurable (CF * CG)
        (Filter.Eventually.of_forall fun a => by
          change |F a.1 * G (endpoint a)| ≤ CF * CG
          rw [abs_mul]
          exact mul_le_mul (hFb a.1) (hGb (endpoint a)) (abs_nonneg _) hCF)
    have houter : Integrable (fun z => F z * op G z) (nu y) := by
      simpa only [H, endpoint, integral_const_mul] using hHi.integral_prod_left
    refine ⟨houter, ?_⟩
    have hpair : Measurable (fun a : (E × E) × (E × E) => F a.1 * G a.2) :=
      (hF.comp measurable_fst).mul (hG.comp measurable_snd)
    calc
      (∫ z, F z * op G z ∂nu y) = ∫ a, H a ∂((nu y).prod P) := by
        rw [integral_prod H hHi]
        simp only [H, endpoint, op, integral_const_mul]
      _ = ∫ a, F a.1 * G a.2 ∂Q :=
        (integral_map hM.aemeasurable hpair.aestronglyMeasurable).symm
  intro F G CF CG hF hG hCF hCG hFb hGb
  have hleft := htest F G CF CG hF hG hCF hCG hFb hGb
  have hright := htest (fun z => G (R z)) (fun z => F (R z)) CG CF
    (hG.comp hRm) (hF.comp hRm) hCG hCF (fun z => hGb (R z)) (fun z => hFb (R z))
  refine ⟨hleft.1, hright.1, ?_⟩
  rw [hleft.2, hright.2]
  have hpair : Measurable (fun a : (E × E) × (E × E) => F a.1 * G a.2) :=
    (hF.comp measurable_fst).mul (hG.comp measurable_snd)
  calc
    (∫ a, F a.1 * G a.2 ∂Q) = ∫ a, F (J a).1 * G (J a).2 ∂Q := by
      conv_lhs => rw [← hJ.map_eq]
      exact integral_map hJ.measurable.aemeasurable hpair.aestronglyMeasurable
    _ = ∫ a, G (R a.1) * F (R a.2) ∂Q := by
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun a => mul_comm _ _

#print axioms actual_bounded_gibbs_duality
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality
