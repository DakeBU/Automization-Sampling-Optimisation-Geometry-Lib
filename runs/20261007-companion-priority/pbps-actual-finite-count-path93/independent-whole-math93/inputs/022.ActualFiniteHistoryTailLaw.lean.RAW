import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/-! Source-implicit deterministic-depth probability bridge.
Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1 (A.1),(A.2),
the unused-input bridge implicit in (A.7), and Appendix A.2 Borel recursion.
The prefix/tail argument is an attributed ASTIS completion.
The actual stopped recursion is retained literally. History at depth n uses clocks
0,...,n-1; the unused raw real tail starts at n. No random-depth restart,
physical-time residual clock, conditional event density or full path law claim. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw
open InnerProductSpace MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_finite_history_tail_law_statement
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
    let tail : ℕ → (ℕ → ℝ) → (ℕ → ℝ) := fun n w k => w (n + k)
    let past : ℕ → MeasurableSpace (ℕ → ℝ) := fun n =>
      ⨆ k ∈ Set.Iio n, MeasurableSpace.comap (fun w : ℕ → ℝ => w k) inferInstance
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      Measurable (history y xRef z₀ n) ∧ Measurable (tail n) ∧
      (∀ (w w' : ℕ → ℝ), (∀ k < n, w k = w' k) →
        history y xRef z₀ n w = history y xRef z₀ n w') ∧
      Measurable[past n] (history y xRef z₀ n) ∧
      Measure.map (tail n) P = P ∧
      IndepFun (history y xRef z₀ n) (tail n) P ∧
      Measure.map (fun w => (history y xRef z₀ n w, tail n w)) P =
        (Measure.map (history y xRef z₀ n) P).prod P ∧
      (∀ A : Set (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)), MeasurableSet A →
        Measure.map (tail n) (P.restrict (history y xRef z₀ n ⁻¹' A)) =
          (P (history y xRef z₀ n ⁻¹' A)) • P)


set_option maxHeartbeats 1600000 in
theorem actual_finite_history_tail_law
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_finite_history_tail_law_statement hα hαβ hV hH hη hβη := by
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
  let tail : ℕ → (ℕ → ℝ) → (ℕ → ℝ) := fun n w k => w (n + k)
  let past : ℕ → MeasurableSpace (ℕ → ℝ) := fun n =>
    ⨆ k ∈ Set.Iio n, MeasurableSpace.comap (fun w : ℕ → ℝ => w k) inferInstance
  change
  ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      Measurable (history y xRef z₀ n) ∧ Measurable (tail n) ∧
      (∀ (w w' : ℕ → ℝ), (∀ k < n, w k = w' k) →
        history y xRef z₀ n w = history y xRef z₀ n w') ∧
      Measurable[past n] (history y xRef z₀ n) ∧
      Measure.map (tail n) P = P ∧
      IndepFun (history y xRef z₀ n) (tail n) P ∧
      Measure.map (fun w => (history y xRef z₀ n w, tail n w)) P =
        (Measure.map (history y xRef z₀ n) P).prod P ∧
      (∀ A : Set (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)), MeasurableSet A →
        Measure.map (tail n) (P.restrict (history y xRef z₀ n ⁻¹' A)) =
          (P (history y xRef z₀ n ⁻¹' A)) • P)

  have hrec := ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  have hR (j : ℕ) : Measurable (fun a : (E × E) × (E × E) × (ℕ → ℝ≥0) =>
      record a.1.1 a.1.2 a.2.1 a.2.2 j) := hrec.2.2.2.1 j
  have hinput := AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
  letI : IsProbabilityMeasure P := hinput.1
  letI : IsProbabilityMeasure (expMeasure (1 : ℝ)) :=
    isProbabilityMeasure_expMeasure zero_lt_one
  have hclock : iIndepFun (fun k (w : ℕ → ℝ) => w k) P := hinput.2.2.1
  intro y xRef z₀ n
  -- Deterministic causality: the mth record consumes exactly coordinates below m.
  have hcausal (e e' : ℕ → ℝ≥0) (m : ℕ)
      (he : ∀ k < m, e k = e' k) :
      record y xRef z₀ e m = record y xRef z₀ e' m := by
    induction m with
    | zero => rfl
    | succ m ih =>
      change next y xRef (e m) (record y xRef z₀ e m) =
        next y xRef (e' m) (record y xRef z₀ e' m)
      rw [he m (Nat.lt_succ_self m), ih (fun k hk => he k (Nat.lt_succ_of_lt hk))]
  have hprefix (w w' : ℕ → ℝ) (hw : ∀ k < n, w k = w' k) :
      history y xRef z₀ n w = history y xRef z₀ n w' := by
    funext j
    exact hcausal (ε w) (ε w') j.val (fun k hk =>
      congrArg Real.toNNReal (hw k (lt_of_lt_of_le hk (Nat.le_of_lt_succ j.isLt))))
  have hε : Measurable ε := measurable_pi_lambda _ (fun k =>
    measurable_real_toNNReal.comp (measurable_pi_apply k :
      Measurable (fun w : ℕ → ℝ => w k)))
  have hHmeas : Measurable (history y xRef z₀ n) :=
    measurable_pi_lambda _ (fun j => (hR j.val).comp
      ((measurable_const : Measurable (fun _ : ℕ → ℝ => (y, xRef))).prodMk
        ((measurable_const : Measurable (fun _ : ℕ → ℝ => z₀)).prodMk hε)))
  have hTmeas : Measurable (tail n) :=
    measurable_pi_lambda _ (fun k => measurable_pi_apply (n + k))
  -- Truncation is a proof factorization, never a replacement algorithm/input law.
  let truncated : (ℕ → ℝ) → ℕ → ℝ≥0 :=
    fun w k => if k < n then ε w k else 0
  have htruncated : Measurable[past n] truncated := by
    letI : MeasurableSpace (ℕ → ℝ) := past n
    apply measurable_pi_lambda
    intro k
    by_cases hk : k < n
    · have hx : Measurable[past n] (fun w : ℕ → ℝ => w k) := by
        apply measurable_iff_comap_le.mpr
        exact le_iSup_of_le k (le_iSup_of_le hk le_rfl)
      simpa only [truncated, hk, if_true, ε, Function.comp_def] using
        measurable_real_toNNReal.comp hx
    · simpa only [truncated, hk, if_false] using
        (measurable_const : Measurable[past n] (fun _ : ℕ → ℝ => (0 : ℝ≥0)))
  have hHp : Measurable[past n] (history y xRef z₀ n) := by
    letI : MeasurableSpace (ℕ → ℝ) := past n
    apply measurable_pi_lambda
    intro j
    have hm := (hR j.val).comp
      ((measurable_const : Measurable (fun _ : ℕ → ℝ => (y, xRef))).prodMk
        ((measurable_const : Measurable (fun _ : ℕ → ℝ => z₀)).prodMk htruncated))
    have heq : (fun w => record y xRef z₀ (truncated w) j.val) =
        (fun w => history y xRef z₀ n w j) := by
      funext w
      exact hcausal (truncated w) (ε w) j.val (fun k hk =>
        if_pos (lt_of_lt_of_le hk (Nat.le_of_lt_succ j.isLt)))
    rw [← heq]
    exact hm
  let future : ℕ → MeasurableSpace (ℕ → ℝ) := fun m =>
    ⨆ k ∈ Set.Ici m, MeasurableSpace.comap (fun w : ℕ → ℝ => w k) inferInstance
  have hTf : Measurable[future n] (tail n) := by
    letI : MeasurableSpace (ℕ → ℝ) := future n
    apply measurable_pi_lambda
    intro k
    apply measurable_iff_comap_le.mpr
    exact le_iSup_of_le (n + k) (le_iSup_of_le (Nat.le_add_right n k) le_rfl)
  have hdis : Disjoint (Set.Iio n) (Set.Ici n) := by
    rw [Set.disjoint_left]
    intro k hk hn
    exact (not_lt_of_ge (show n ≤ k from hn)) (show k < n from hk)
  have hblocks : Indep (past n) (future n) P :=
    indep_iSup_of_disjoint (fun k => (measurable_pi_apply k).comap_le)
      ((iIndepFun_iff_iIndep (fun _ : ℕ => inferInstance)
        (fun k (w : ℕ → ℝ) => w k) P).mp hclock) hdis
  have hindep : IndepFun (history y xRef z₀ n) (tail n) P :=
    indep_of_indep_of_le hblocks hHp.comap_le hTf.comap_le
  have htailLaw : Measure.map (tail n) P = P := by
    exact Measure.map_infinitePi_infinitePi_of_inj
      (P := fun _ : ℕ => expMeasure (1 : ℝ)) (f := fun k => n + k)
      (fun _ _ h => Nat.add_left_cancel h)
  have hjoint : Measure.map (fun w => (history y xRef z₀ n w, tail n w)) P =
      (Measure.map (history y xRef z₀ n) P).prod P := by
    rw [hindep.map_prod_eq_prod_map_map hHmeas.aemeasurable hTmeas.aemeasurable,
      htailLaw]
  refine ⟨hHmeas, hTmeas, hprefix, hHp, htailLaw, hindep, hjoint, ?_⟩
  intro A hA
  apply Measure.ext
  intro B hB
  rw [Measure.map_apply hTmeas hB, Measure.restrict_apply (hB.preimage hTmeas),
    Measure.smul_apply, Set.inter_comm,
    hindep.measure_inter_preimage_eq_mul A B hA hB]
  have hBtail : P (tail n ⁻¹' B) = P B := by
    rw [← Measure.map_apply hTmeas hB, htailLaw]
  rw [hBtail]
  rfl

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw
