import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/-!
# Actual PBPS countable endpoint-pair law

The nonnegative count expansion and Gibbs averaging of arXiv:2609.06905v1,
Appendix A.1, are identified with the endpoint law of the actual clock process.
The same law is a probability, is the sum of all fixed-count endpoint sectors,
and is preserved by the momentum-flipped endpoint swap. This is the measure
assembly needed before signed duality and marginal invariance.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

set_option linter.unusedVariables false in
private def actual_countable_endpoint_statement
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
      (∀ y r : E, ∀ T : ℝ≥0,
        let B : (n : ℕ) → (E × E) × Prefix n T → (E × E) × (E × E) :=
          fun n q => (q.1, Γ y r q.1 n T q.2 ⟨T, le_rfl⟩)
        let sigma : (n : ℕ) → Measure ((E × E) × Prefix n T) := fun n =>
          ((nu y).prod (m n T)).withDensity (fun q => ρ y r q.1 n T q.2)
        let L : ℕ → Measure ((E × E) × (E × E)) := fun n => Measure.map (B n) (sigma n)
        let M : (E × E) × (ℕ → ℝ) → (E × E) × (E × E) :=
          fun q => (q.1, Z y r q.1 T q.2)
        let Q : Measure ((E × E) × (E × E)) := Measure.map M ((nu y).prod P)
        let J : (E × E) × (E × E) → (E × E) × (E × E) :=
          fun q => (R q.2, R q.1)
        Q = Measure.sum L ∧ IsProbabilityMeasure Q ∧ MeasurePreserving J Q Q)


set_option maxHeartbeats 1600000
set_option maxRecDepth 10000
/-- The actual Gibbs-initialized endpoint law is the countable sector sum, a probability, and preserved by the flipped swap. -/
theorem actual_countable_endpoint_law
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_countable_endpoint_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_countable_endpoint_statement
  intro c Φ S rate Λ τ next record P ε history Rec Hist readTime Δ Prefix m zAt K qReal q A eventTime I N liveTime d survival weight C Path Ψ Γ ρ R Vy nu
  obtain ⟨Z, hZm, hZa, hZf, hZ0, h93⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law
      hα hαβ hV hH hη hβη
  refine ⟨Z, hZm, hZa, hZf, hZ0, ?_⟩
  intro y r T B sigma L M Q J
  have h103 := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization
    hα hαβ hV hH hη hβη y
  letI : IsProbabilityMeasure (nu y) := by
    have hp := h103.2.2.2.2.2.1
    rw [h103.2.2.2.2.2.2] at hp
    exact hp
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  have hembZ : Measurable (fun q : (E × E) × (ℕ → ℝ) => (((y, r), q.1), T, q.2)) :=
    (measurable_const.prodMk measurable_fst).prodMk (measurable_const.prodMk measurable_snd)
  have hZend := hZm.comp hembZ
  have hM : Measurable M := measurable_fst.prodMk hZend
  have hQ : IsProbabilityMeasure Q := Measure.isProbabilityMeasure_map hM.aemeasurable
  have hB (n : ℕ) : Measurable (B n) := by
    have hemb : Measurable (fun q : (E × E) × Prefix n T => (((y, r), q.1), q.2)) :=
      (measurable_const.prodMk measurable_fst).prodMk measurable_snd
    have hp := (h93 n T).2.1.comp hemb
    have he := (measurable_pi_apply (⟨T, le_rfl⟩ : {s : ℝ≥0 // s ≤ T})).comp hp
    exact measurable_fst.prodMk he
  have hρ (n : ℕ) : Measurable (fun q : (E × E) × Prefix n T => ρ y r q.1 n T q.2) := by
    have hemb : Measurable (fun q : (E × E) × Prefix n T => (((y, r), q.1), q.2)) :=
      (measurable_const.prodMk measurable_fst).prodMk measurable_snd
    have h := (h93 n T).2.2.1.comp hemb
    simpa only [Function.comp_def] using h
  have hm (n : ℕ) : SigmaFinite (m n T) := by
    have hcons (i : Fin (n + 1)) :
        Measurable (fun t : Fin n → ℝ => (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) i) := by
      induction i using Fin.cases with
      | zero => exact measurable_const
      | succ i => exact measurable_pi_apply i
    have hs : MeasurableSet (Δ n T) := by
      change MeasurableSet {t : Fin n → ℝ |
        (∀ i j : Fin (n + 1), i < j → (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) i < (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) j) ∧
        ∀ i : Fin n, t i < (T : ℝ)}
      rw [Set.ofPred_and]
      apply MeasurableSet.inter
      · simpa only [← Set.ofPred_forall] using (MeasurableSet.iInter fun (i : Fin (n + 1)) =>
          MeasurableSet.iInter fun (j : Fin (n + 1)) =>
          MeasurableSet.iInter fun (_ : i < j) => measurableSet_lt (hcons i) (hcons j))
      · simpa only [← Set.ofPred_forall] using (MeasurableSet.iInter fun (i : Fin n) =>
          measurableSet_lt (measurable_pi_apply i) (measurable_const (a := (T : ℝ))))
    have hmσ : SigmaFinite ((m n T).map (fun t : Prefix n T => t.val)) := by
      change SigmaFinite ((Measure.comap (fun t : Prefix n T => t.val)
        (volume : Measure (Fin n → ℝ))).map (fun t : Prefix n T => t.val))
      rw [map_comap_subtype_coe hs]
      infer_instance
    exact SigmaFinite.of_map (m n T) measurable_subtype_coe.aemeasurable hmσ
  have hsum : Q = Measure.sum L := by
    apply Measure.ext_of_lintegral
    intro F hF
    let D : ℕ → (E × E) → ℝ≥0∞ := fun n z =>
      ∫⁻ t : Prefix n T, F (B n (z, t)) * ρ y r z n T t ∂m n T
    have hD (n : ℕ) : Measurable (D n) := by
      letI := hm n
      exact ((hF.comp (hB n)).mul (hρ n)).lintegral_prod_right'
    have hz (z : E × E) :
        (∫⁻ w, F (z, Z y r z T w) ∂P) = ∑' n, D n z := by
      have hN : Measurable (N y r z T) := ((h93 0 T).2.2.2 y r z).2.2.1
      have hsets (n : ℕ) : MeasurableSet {w | N y r z T w = n} :=
        (measurableSet_singleton n).preimage hN
      have hdis : Pairwise (fun i j : ℕ => Disjoint {w | N y r z T w = i} {w | N y r z T w = j}) := by
        intro i j hij
        exact Set.disjoint_left.mpr (fun w hi hj => hij (hi.symm.trans hj))
      have hu : (⋃ n : ℕ, {w | N y r z T w = n}) = Set.univ := by
        ext w
        simp
      calc
        (∫⁻ w, F (z, Z y r z T w) ∂P) =
            ∑' n, ∫⁻ w in {w | N y r z T w = n}, F (z, Z y r z T w) ∂P := by
          simpa only [hu, Measure.restrict_univ] using
            (lintegral_iUnion hsets hdis (fun w => F (z, Z y r z T w)))
        _ = ∑' n, D n z := by
          apply tsum_congr
          intro n
          rcases (h93 n T).2.2.2 y r z with
            ⟨hH, hZT, hNN, hC, hGamma, hactual, hAE, hdisjoint, hcover, hlaw, hint, hmass, hbound⟩
          exact hint (fun hp => F (z, hp.2 ⟨T, le_rfl⟩))
            (hF.comp (measurable_const.prodMk ((measurable_pi_apply (⟨T, le_rfl⟩ : {s : ℝ≥0 // s ≤ T})).comp measurable_snd)))
    calc
      (∫⁻ x, F x ∂Q) = ∫⁻ z, ∫⁻ w, F (z, Z y r z T w) ∂P ∂nu y := by
        change (∫⁻ x, F x ∂Measure.map M ((nu y).prod P)) = _
        rw [lintegral_map hF hM]
        exact lintegral_prod (f := fun x => F (M x)) (hF.comp hM).aemeasurable
      _ = ∫⁻ z, ∑' n, D n z ∂nu y := lintegral_congr hz
      _ = ∑' n, ∫⁻ z, D n z ∂nu y := lintegral_tsum (fun n => (hD n).aemeasurable)
      _ = ∑' n, ∫⁻ x, F x ∂L n := by
        apply tsum_congr
        intro n
        letI := hm n
        change (∫⁻ z, ∫⁻ t : Prefix n T, F (B n (z, t)) * ρ y r z n T t ∂m n T ∂nu y) =
          ∫⁻ x, F x ∂Measure.map (B n) (sigma n)
        rw [lintegral_map hF (hB n)]
        change _ = ∫⁻ x, F (B n x) ∂(((nu y).prod (m n T)).withDensity (fun x => ρ y r x.1 n T x.2))
        rw [lintegral_withDensity_eq_lintegral_mul _
          (f := fun x : (E × E) × Prefix n T => ρ y r x.1 n T x.2)
          (g := fun x => F (B n x)) (hρ n) (hF.comp (hB n))]
        simp only [Pi.mul_apply]
        rw [lintegral_prod (f := fun x : (E × E) × Prefix n T =>
          ρ y r x.1 n T x.2 * F (B n x)) ((hρ n).mul (hF.comp (hB n))).aemeasurable]
        apply lintegral_congr
        intro z
        apply lintegral_congr
        intro t
        exact mul_comm _ _
      _ = ∫⁻ x, F x ∂Measure.sum L := (lintegral_sum_measure F L).symm
  have hsector (n : ℕ) : MeasurePreserving J (L n) (L n) :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector.actual_normalized_endpoint_sector_reversal
      hα hαβ hV hH hη hβη y r n T
  refine ⟨hsum, hQ, (hsector 0).measurable, ?_⟩
  rw [hsum, Measure.map_sum (hsector 0).measurable.aemeasurable]
  congr 1
  funext n
  exact (hsector n).map_eq

#print axioms actual_countable_endpoint_law
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw
