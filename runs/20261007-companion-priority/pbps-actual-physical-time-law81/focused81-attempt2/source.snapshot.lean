import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import Mathlib.Probability.Kernel.Composition.Prod
import Mathlib.MeasureTheory.Measure.Prod
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false
private def ideal_half_turn_returned_position_kernel_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop :=
    let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
    let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun sample k => Real.toNNReal (sample k)
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
    let eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ e n => (record y xRef z₀ e n).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    let q : E → Measure E := fun y =>
      (volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))
    let γ : Measure E := stdGaussian E
    let M : E → Measure ((E × E) × (ℕ → ℝ)) := fun y => ((q y).prod γ).prod P
    let tπ : ℝ≥0 := ⟨Real.pi, Real.pi_pos.le⟩
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ sample : ℕ → ℝ, ∀ t : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E),
          eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) →
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1) →
          record y xRef z₀ (ε sample) n = Sum.inl a →
          Z y xRef z₀ t sample = Φ y xRef ((t - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ sample : ℕ → ℝ, ∀ t : ℝ≥0,
        (¬ ∃ n : ℕ, eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) ∧
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1)) →
          Z y xRef z₀ t sample = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ sample ∂P,
        (∀ t : ℝ≥0, ∃ n : ℕ, ∃ a : ℝ≥0 × (E × E),
          eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) ∧
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1) ∧
          record y xRef z₀ (ε sample) n = Sum.inl a ∧ a.1 ≤ t ∧
          ((t - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y xRef a.2 (ε sample n) ∧
          Z y xRef z₀ t sample = Φ y xRef ((t - a.1 : ℝ≥0) : ℝ) a.2) ∧
        Z y xRef z₀ 0 sample = z₀) ∧
      ∃ R : Kernel E E, IsMarkovKernel R ∧ (∀ y : E, R y = q y) ∧
      ∃ H : Kernel (E × E) E, IsMarkovKernel H ∧
      (∀ y x : E, H (y, x) = Measure.map
        (fun w : (E × E) × (ℕ → ℝ) => (Z y w.1.1 (x, w.1.2) tπ w.2).1)
        (M y)) ∧
      (∀ y x : E, Measure.map
        (fun w : (E × E) × (ℕ → ℝ) => Z y w.1.1 (x, w.1.2) 0 w.2)
        (M y) = (Measure.dirac x).prod γ) ∧
      (∀ y x : E, ∀ᵐ w ∂M y,
        Z y w.1.1 (x, w.1.2) 0 w.2 = (x, w.1.2) ∧
        ∃ n : ℕ, ∃ a : ℝ≥0 × (E × E),
          eventTime y w.1.1 (x, w.1.2) (ε w.2) n ≤ (tπ : WithTop ℝ≥0) ∧
          (tπ : WithTop ℝ≥0) < eventTime y w.1.1 (x, w.1.2) (ε w.2) (n + 1) ∧
          record y w.1.1 (x, w.1.2) (ε w.2) n = Sum.inl a ∧ a.1 ≤ tπ ∧
          ((tπ - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y w.1.1 a.2 (ε w.2 n) ∧
          Z y w.1.1 (x, w.1.2) tπ w.2 = Φ y w.1.1 ((tπ - a.1 : ℝ≥0) : ℝ) a.2)


set_option maxHeartbeats 1600000 in
/-- Ideal exact-reference PBPS returned law at pi. Kernel mass and initialization
are derived; no phase Markov property, invariance, implementation or cost claim. -/
theorem ideal_half_turn_returned_position_kernel
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    ideal_half_turn_returned_position_kernel_statement hα hαβ hV hH hη hβη := by
  classical
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun sample k => Real.toNNReal (sample k)
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
  let eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ e n => (record y xRef z₀ e n).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  let q : E → Measure E := fun y =>
    (volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))
  let γ : Measure E := stdGaussian E
  let M : E → Measure ((E × E) × (ℕ → ℝ)) := fun y => ((q y).prod γ).prod P
  let tπ : ℝ≥0 := ⟨Real.pi, Real.pi_pos.le⟩
  have h80 := ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase
    hα hαβ hV hH hη hβη
  obtain ⟨Z, hZM, hcovered, hfallback, hAE⟩ := h80
  have hZV := (GibbsAugmentation.normalized_augmentation_density
    hα hV (fun x v => (hH x v).1) hη).1
  have hi : Integrable (fun x : E => Real.exp (-V x)) (volume : Measure E) :=
    Integrable.of_integral_ne_zero hZV.ne'
  let μ : Measure E := (volume : Measure E).tilted (fun x => -V x)
  letI : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hi
  obtain ⟨R, hR, hRy, _⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  letI : IsMarkovKernel R := hR
  have hRq (y : E) : R y = q y := by
    rw [hRy y, show μ = (volume : Measure E).tilted (fun x => -V x) from rfl,
      tilted_tilted hi]
    congr 1
    funext z
    dsimp only [Pi.add_apply]
    ring
  have hqprob (y : E) : IsProbabilityMeasure (q y) := by
    rw [← hRq y]
    infer_instance
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  letI : IsProbabilityMeasure γ := inferInstanceAs (IsProbabilityMeasure (stdGaussian E))
  let Q : Kernel (E × E) ((E × E) × (ℕ → ℝ)) :=
    ((R.comap Prod.fst measurable_fst) ×ₖ Kernel.const (E × E) γ) ×ₖ
      Kernel.const (E × E) P
  have hQ (y x : E) : Q (y, x) = M y := by
    simp only [Q, Kernel.prod_apply, Kernel.comap_apply, Kernel.const_apply, hRq, M]
  let F : (E × E) × ((E × E) × (ℕ → ℝ)) → E :=
    fun a => (Z a.1.1 a.2.1.1 (a.1.2, a.2.1.2) tπ a.2.2).1
  have hFM : Measurable F :=
    (hZM.comp ((measurable_fst.fst.prodMk measurable_snd.fst.fst).prodMk
      (measurable_fst.snd.prodMk measurable_snd.fst.snd) |>.prodMk
        (measurable_const.prodMk measurable_snd.snd))).fst
  let H : Kernel (E × E) E := (Kernel.id ×ₖ Q).map F
  have hHkernel : IsMarkovKernel H := Kernel.IsMarkovKernel.map _ hFM
  have hHlaw (y x : E) : H (y, x) = Measure.map
      (fun w : (E × E) × (ℕ → ℝ) => (Z y w.1.1 (x, w.1.2) tπ w.2).1) (M y) := by
    dsimp only [H]
    rw [Kernel.map_apply _ hFM, Kernel.prod_apply, Kernel.id_apply, hQ,
      Measure.dirac_prod, Measure.map_map hFM (by fun_prop)]
    rfl
  have h76 := ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion
    hα hαβ hV hH hη hβη
  rcases h76 with ⟨_, _, _, hrecordM, htimeM, _, _, _, _, _⟩
  have hΦM : Measurable (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) :=
    (ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη).2.1
  have hτM : Measurable (fun a : (E × E) × (E × E) × ℝ≥0 =>
      τ a.1.1 a.1.2 a.2.1 a.2.2) := (ActualHazardClock.actual_integrated_hazard_clock_laws
    hα hαβ hV hH hη hβη).2.2.2.2.2.2.1
  have hεM : Measurable ε := measurable_pi_lambda _ fun n =>
    measurable_real_toNNReal.comp (measurable_pi_apply n)
  let W := (E × E) × (ℕ → ℝ)
  have hgood (y x : E) : ∀ᵐ w ∂M y,
      Z y w.1.1 (x, w.1.2) 0 w.2 = (x, w.1.2) ∧
      ∃ n : ℕ, ∃ a : ℝ≥0 × (E × E),
        eventTime y w.1.1 (x, w.1.2) (ε w.2) n ≤ (tπ : WithTop ℝ≥0) ∧
        (tπ : WithTop ℝ≥0) < eventTime y w.1.1 (x, w.1.2) (ε w.2) (n + 1) ∧
        record y w.1.1 (x, w.1.2) (ε w.2) n = Sum.inl a ∧ a.1 ≤ tπ ∧
        ((tπ - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y w.1.1 a.2 (ε w.2 n) ∧
        Z y w.1.1 (x, w.1.2) tπ w.2 = Φ y w.1.1 ((tπ - a.1 : ℝ≥0) : ℝ) a.2 := by
    letI : IsProbabilityMeasure (q y) := hqprob y
    let args : W → (E × E) × (E × E) × (ℕ → ℝ≥0) :=
      fun w => ((y, w.1.1), (x, w.1.2), ε w.2)
    have hargs : Measurable args := (measurable_const.prodMk measurable_fst.fst).prodMk
      ((measurable_const.prodMk measurable_fst.snd).prodMk (hεM.comp measurable_snd))
    have hrM (n : ℕ) : Measurable (fun w : W => record y w.1.1 (x, w.1.2) (ε w.2) n) :=
      (hrecordM n).comp hargs
    have htM (n : ℕ) : Measurable (fun w : W => eventTime y w.1.1 (x, w.1.2) (ε w.2) n) :=
      (htimeM n).comp hargs
    let L : ℕ → W → ℝ≥0 × (E × E) := fun n w =>
      (record y w.1.1 (x, w.1.2) (ε w.2) n).elim id (fun _ => (0, (0, 0)))
    have hLM (n : ℕ) : Measurable (L n) :=
      (measurable_id.sumElim measurable_const).comp (hrM n)
    have hzM (t : ℝ≥0) : Measurable (fun w : W => Z y w.1.1 (x, w.1.2) t w.2) :=
      hZM.comp (((measurable_const.prodMk measurable_fst.fst).prodMk
        (measurable_const.prodMk measurable_fst.snd)).prodMk
          (measurable_const.prodMk measurable_snd))
    have hwaitM (n : ℕ) : Measurable (fun w : W => τ y w.1.1 (L n w).2 (ε w.2 n)) :=
      hτM.comp ((measurable_const.prodMk measurable_fst.fst).prodMk
        ((hLM n).snd.prodMk ((measurable_pi_apply n).comp (hεM.comp measurable_snd))))
    have hbranchM (n : ℕ) : Measurable (fun w : W =>
        Φ y w.1.1 ((tπ - (L n w).1 : ℝ≥0) : ℝ) (L n w).2) :=
      hΦM.comp ((measurable_const.prodMk measurable_fst.fst).prodMk
        ((measurable_coe_nnreal_real.comp (measurable_const.sub (hLM n).fst)).prodMk
          (hLM n).snd))
    let D : ℕ → Set W := fun n => {w |
      eventTime y w.1.1 (x, w.1.2) (ε w.2) n ≤ (tπ : WithTop ℝ≥0) ∧
      (tπ : WithTop ℝ≥0) < eventTime y w.1.1 (x, w.1.2) (ε w.2) (n + 1) ∧
      record y w.1.1 (x, w.1.2) (ε w.2) n = Sum.inl (L n w) ∧ (L n w).1 ≤ tπ ∧
      ((tπ - (L n w).1 : ℝ≥0) : WithTop ℝ≥0) < τ y w.1.1 (L n w).2 (ε w.2 n) ∧
      Z y w.1.1 (x, w.1.2) tπ w.2 = Φ y w.1.1 ((tπ - (L n w).1 : ℝ≥0) : ℝ) (L n w).2}
    have hDM (n : ℕ) : MeasurableSet (D n) :=
      (measurableSet_le (htM n) measurable_const).inter
        ((measurableSet_lt measurable_const (htM (n + 1))).inter
          ((measurableSet_eq_fun (hrM n) ((measurable_inl).comp (hLM n))).inter
            ((measurableSet_le (hLM n).fst measurable_const).inter
              ((measurableSet_lt
                (WithTop.measurable_coe.comp (measurable_const.sub (hLM n).fst))
                (hwaitM n)).inter (measurableSet_eq_fun (hzM tπ) (hbranchM n))))))
    let G : Set W := {w | Z y w.1.1 (x, w.1.2) 0 w.2 = (x, w.1.2)} ∩ ⋃ n, D n
    have hGM : MeasurableSet G :=
      (measurableSet_eq_fun (hzM 0) (measurable_const.prodMk measurable_fst.snd)).inter
        (MeasurableSet.iUnion hDM)
    have hGAE : ∀ᵐ w ∂M y, w ∈ G := by
      apply (Measure.ae_prod_iff_ae_ae hGM).mpr
      filter_upwards with u
      filter_upwards [hAE y u.1 (x, u.2)] with sample hs
      refine ⟨hs.2, Set.mem_iUnion.mpr ?_⟩
      obtain ⟨n, a, hl, hu, hr, ha, hw, hz⟩ := hs.1 tπ
      have hLa : L n (u, sample) = a := by dsimp only [L]; rw [hr]; rfl
      refine ⟨n, ?_⟩
      change _ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _
      rw [hLa]
      exact ⟨hl, hu, hr, ha, hw, hz⟩
    filter_upwards [hGAE] with w hw
    obtain ⟨n, hn⟩ := Set.mem_iUnion.mp hw.2
    exact ⟨hw.1, n, L n w, hn⟩
  refine ⟨Z, hZM, hcovered, hfallback, hAE, R, hR, hRq, H, hHkernel, hHlaw, ?_, hgood⟩
  intro y x
  letI : IsProbabilityMeasure (q y) := hqprob y
  rw [Measure.map_congr_ae ((hgood y x).mono (fun w hw => hw.1)), Measure.dirac_prod]
  have hmarg : Measure.map (fun w : W => w.1.2) (M y) = γ := by
    change Measure.map (Prod.snd ∘ Prod.fst) (((q y).prod γ).prod P) = γ
    rw [← Measure.map_map measurable_snd measurable_fst]
    simp
  calc
    Measure.map (fun w : W => (x, w.1.2)) (M y) =
        Measure.map (Prod.mk x) (Measure.map (fun w : W => w.1.2) (M y)) :=
      (Measure.map_map (by fun_prop) (by fun_prop)).symm
    _ = Measure.map (Prod.mk x) γ := by rw [hmarg]

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel
