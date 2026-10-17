import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHalfTurnReversibility
import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture
import AutoSamplingTheory.TechnicalLemmas.Probability.KernelTransport

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal

/-!
# Actual augmented PBPS one-step invariance

Source: Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Proposition 3.4,
equation (3.11), under standing hypotheses (1.1), (2.2), and fixed resampling
probability in (0,1). This constructs the actual transition, not an arbitrary
kernel supplied with invariance as a premise.

The literal clock/flight/half-turn witness is retained. The normalized generative
Gibbs augmentation is disintegrated using the same everywhere-defined R. A
retained-coordinate Tonelli argument lifts fiber invariance to the joint law;
the fixed probability mixture follows the auxiliary Gaussian reflection.

Only exact one-step invariance is proved: no process restart, semigroup,
augmented all-L2 realization, hypocoercivity, implementation error, cap, cost,
initialization, composition, or full-paper conclusion.
-/

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAugmentedKernelInvariance

private theorem retained_invariant {A B : Type*} [MeasurableSpace A] [MeasurableSpace B]
    (ν : Measure (A × B)) [IsProbabilityMeasure ν]
    (R : Kernel A B) [IsMarkovKernel R] [ν.IsCondKernel R]
    (F : Kernel (A × B) B) [IsMarkovKernel F]
    (hF : ∀ a, (F.comap (fun b => (a, b)) (by fun_prop)).Invariant (R a)) :
    ((Kernel.deterministic Prod.fst measurable_fst) ×ₖ F).Invariant ν := by
  let L := (Kernel.deterministic Prod.fst measurable_fst) ×ₖ F
  change ν.bind L = ν
  ext s hs
  calc
    (ν.bind L) s = ∫⁻ z, L z s ∂ν :=
      Measure.bind_apply hs L.aemeasurable
    _ = ∫⁻ a, ∫⁻ b, L (a, b) s ∂R a ∂ν.fst := by
      rw [← Measure.lintegral_compProd (L.measurable_coe hs), ν.disintegrate R]
    _ = ∫⁻ a, R a (Prod.mk a ⁻¹' s) ∂ν.fst := by
      apply lintegral_congr
      intro a
      simp_rw [show ∀ b, L (a, b) s = F (a, b) (Prod.mk a ⁻¹' s) from
        fun b => Kernel.deterministic_prod_apply' measurable_fst F (a, b) hs]
      have ht : MeasurableSet (Prod.mk a ⁻¹' s) := hs.preimage measurable_prodMk_left
      have hi := congrArg (fun m : Measure B => m (Prod.mk a ⁻¹' s)) (hF a).def
      rw [Measure.bind_apply ht (Kernel.aemeasurable _)] at hi
      exact hi
    _ = (ν.fst ⊗ₘ R) s := (Measure.compProd_apply hs).symm
    _ = ν s := congrArg (fun m : Measure (A × B) => m s) (ν.disintegrate R)

private theorem reflected_conditional_mixture
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (J : Measure (E × E)) [IsProbabilityMeasure J]
    (R : Kernel E E) [IsMarkovKernel R] [(J.map Prod.swap).IsCondKernel R]
    (H : Kernel (E × E) E) [IsMarkovKernel H]
    (hH : ∀ y, (H.comap (fun x => (y, x)) (by fun_prop)).Invariant (R y))
    (ρ : ℝ) (hρpos : 0 < ρ) (hρlt : ρ < 1)
    (hreflection : J.map (fun z => (z.1, (2 : ℝ) • z.1 - z.2)) = J) :
    ∃ K : Kernel (E × E) (E × E), IsMarkovKernel K ∧ K.Invariant J ∧
      ∀ z, K z = (ENNReal.ofReal ρ • R ((2 : ℝ) • z.1 - z.2) +
        ENNReal.ofReal (1 - ρ) • H ((2 : ℝ) • z.1 - z.2, z.1)).prod
        (Measure.dirac ((2 : ℝ) • z.1 - z.2)) := by
  classical
  let w : Fin 2 → ℝ≥0 := ![Real.toNNReal ρ, Real.toNNReal (1 - ρ)]
  have hw : ∑ i, w i = 1 := by
    apply NNReal.coe_injective
    simp only [Fin.sum_univ_two, w, Matrix.cons_val_zero, Matrix.cons_val_one,
      NNReal.coe_add, NNReal.coe_one, Real.coe_toNNReal ρ hρpos.le,
      Real.coe_toNNReal (1 - ρ) (sub_nonneg.mpr hρlt.le)]
    ring
  let A : Kernel (E × E) E := R.comap Prod.fst measurable_fst
  let ks : Fin 2 → Kernel (E × E) E := ![A, H]
  letI : ∀ i, IsMarkovKernel (ks i) := by
    intro i
    fin_cases i <;> dsimp [ks, A] <;> infer_instance
  let F := AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture.finiteMixture w ks
  letI : IsMarkovKernel F :=
    AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture.finiteMixture_isMarkovKernel w ks hw
  have hFlaw (z : E × E) : F z = ENNReal.ofReal ρ • R z.1 +
      ENNReal.ofReal (1 - ρ) • H z := by
    rw [AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture.finiteMixture_apply,
      Fin.sum_univ_two]
    rfl
  have hF (y : E) : (F.comap (fun x => (y, x)) (by fun_prop)).Invariant (R y) := by
    let sy : Fin 2 → Kernel E E :=
      ![Kernel.const E (R y), H.comap (fun x => (y, x)) (by fun_prop)]
    letI : ∀ i, IsMarkovKernel (sy i) := by
      intro i
      fin_cases i <;> dsimp [sy] <;> infer_instance
    have hsy : ∀ i, (sy i).Invariant (R y) := by
      intro i
      fin_cases i
      · change (R y).bind (fun _ => R y) = R y
        simp [Measure.bind_const]
      · exact hH y
    have heq : F.comap (fun x => (y, x)) (by fun_prop) =
        AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture.finiteMixture w sy := by
      ext x : 1
      rw [Kernel.comap_apply, hFlaw,
        AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture.finiteMixture_apply,
        Fin.sum_univ_two]
      rfl
    rw [heq]
    exact AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture.finiteMixture_invariant
      w sy (R y) hw hsy
  letI : IsProbabilityMeasure (J.map Prod.swap) :=
    Measure.isProbabilityMeasure_map measurable_swap.aemeasurable
  let L : Kernel (E × E) (E × E) :=
    (Kernel.deterministic Prod.fst measurable_fst) ×ₖ F
  have hL : L.Invariant (J.map Prod.swap) := retained_invariant (J.map Prod.swap) R F hF
  let B : Kernel (E × E) (E × E) := (L.comap Prod.swap measurable_swap).map Prod.swap
  letI : IsMarkovKernel B := Kernel.IsMarkovKernel.map _ measurable_swap
  have hB : B.Invariant J := by
    have ht := AutoSamplingTheory.TechnicalLemmas.Probability.KernelTransport.invariant_map_comap
      (MeasurableEquiv.prodComm : E × E ≃ᵐ E × E) hL
    change B.Invariant ((J.map Prod.swap).map Prod.swap) at ht
    rw [Measure.map_map measurable_swap measurable_swap] at ht
    simpa only [Prod.swap_swap_eq, Measure.map_id] using ht
  let U : E × E → E × E := fun z => (z.1, (2 : ℝ) • z.1 - z.2)
  have hU : Measurable U := by
    dsimp only [U]
    fun_prop
  have hUinv : (Kernel.deterministic U hU).Invariant J := by
    change (Kernel.deterministic U hU) ∘ₘ J = J
    rw [Measure.deterministic_comp_eq_map]
    exact hreflection
  let K := B ∘ₖ Kernel.deterministic U hU
  refine ⟨K, inferInstance, hB.comp hUinv, ?_⟩
  intro z
  change (B ∘ₖ Kernel.deterministic U hU) z = _
  rw [Kernel.comp_deterministic_eq_comap, Kernel.comap_apply, Kernel.map_apply _ measurable_swap,
    Kernel.comap_apply, Kernel.prod_apply, Kernel.deterministic_apply]
  rw [Measure.prod_swap, hFlaw]
  rfl


private def actual_augmented_kernel_invariance_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1)
    (ρ : ℝ) (hρpos : 0 < ρ) (hρlt : ρ < 1) : Prop :=
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
    let μ : Measure E := (volume : Measure E).tilted (fun x => -V x)
    let J : Measure (E × E) := Measure.map
      (fun z : E × E => (z.1, z.1 + Real.sqrt η • z.2)) (μ.prod γ)
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧
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
      (∀ y : E, (H.comap (fun x : E => (y, x)) (by fun_prop)).IsReversible (q y)) ∧
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
          Z y w.1.1 (x, w.1.2) tπ w.2 = Φ y w.1.1 ((tπ - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (J.map Prod.swap).IsCondKernel R ∧
      ∃ K : Kernel (E × E) (E × E), IsMarkovKernel K ∧ K.Invariant J ∧
        (∀ z : E × E, K z =
          (ENNReal.ofReal ρ • q ((2 : ℝ) • z.1 - z.2) +
            ENNReal.ofReal (1 - ρ) • H ((2 : ℝ) • z.1 - z.2, z.1)).prod
          (Measure.dirac ((2 : ℝ) • z.1 - z.2)))

/-- The literal reflected augmented actual-PBPS transition preserves its normalized Gibbs law.
All normalization and conditional-law obligations are conclusions or internal dependencies. -/
theorem actual_augmented_kernel_invariant
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1)
    (ρ : ℝ) (hρpos : 0 < ρ) (hρlt : ρ < 1) :
    actual_augmented_kernel_invariance_statement hα hαβ hV hH hη hβη ρ hρpos hρlt := by
  classical
  unfold actual_augmented_kernel_invariance_statement
  intro P ε c Φ S rate Λ τ next record eventTime q γ M tπ μ J
  obtain ⟨Z, hZM, hZa, hZf, hgood, R, hR, hRq, H, hHK, hrev, hHlaw, hH0, hHgood⟩ :=
    ActualHalfTurnReversibility.actual_half_turn_reversible hα hαβ hV hH hη hβη
  letI : IsMarkovKernel R := hR
  letI : IsMarkovKernel H := hHK
  have hnorm := GibbsAugmentation.normalized_augmentation_density
    hα hV (fun x v => (hH x v).1) hη
  have hi : Integrable (fun x : E => Real.exp (-V x)) (volume : Measure E) :=
    Integrable.of_integral_ne_zero hnorm.1.ne'
  letI : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hi
  letI : IsProbabilityMeasure J := hnorm.2.1
  obtain ⟨Rc, hRc, hRctilt, hcond⟩ :=
    TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  have hRcq (y : E) : Rc y = q y := by
    rw [hRctilt y, show μ = (volume : Measure E).tilted (fun x => -V x) from rfl,
      tilted_tilted hi]
    congr 1
    funext x
    dsimp only [Pi.add_apply]
    ring
  have hRcR : Rc = R := by
    ext y : 1
    rw [hRcq y, hRq y]
  subst Rc
  change (J.map Prod.swap).IsCondKernel R at hcond
  letI : (J.map Prod.swap).IsCondKernel R := hcond
  refine ⟨inferInstance, inferInstance, Z, hZM, hZa, hZf, hgood, R, hR, hRq,
    H, hHK, hrev, hHlaw, hH0, hHgood, hcond, ?_⟩
  have hHinv (y : E) : (H.comap (fun x => (y, x)) (by fun_prop)).Invariant (R y) := by
    rw [hRq y]
    exact (hrev y).invariant
  have href : J.map (fun z => (z.1, (2 : ℝ) • z.1 - z.2)) = J :=
    (GaussianReflection.reflection_preserves_augmentation μ η hη).2
  obtain ⟨K, hK, hKinv, hKlaw⟩ :=
    reflected_conditional_mixture J R H hHinv ρ hρpos hρlt href
  refine ⟨K, hK, hKinv, ?_⟩
  intro z
  simpa only [hRq] using hKlaw z

end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAugmentedKernelInvariance
