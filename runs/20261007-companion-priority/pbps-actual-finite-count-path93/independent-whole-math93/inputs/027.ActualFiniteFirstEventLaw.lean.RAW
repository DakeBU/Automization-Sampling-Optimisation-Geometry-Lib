import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock
import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-! Actual first finite PBPS event, Appendix A.1
(A.1),(A.2) and the first density factor implicit in (A.7), arXiv2609.06905v1.
The finite subprobability and marked-test packaging is attributed ASTIS completion.
Literal actual Exp1 coordinate0, stopped wait and zero-normal identity reflection
are retained. F defaults to0 only outside the restricted positive finite event;
missing probability includes waits beyond T or infinite, without renormalization.
Full path law, unused-tail conditioning, reversal, invariance, semigroup/allL2,
implementation, error, unbounded expected query cost, main/composition remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_finite_first_event_law_statement
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
    let U : E → E → (E × E) → (ℕ → ℝ) → WithTop ℝ≥0 :=
      fun y xRef z sample => τ y xRef z (ε sample 0)
    let F : E → E → (E × E) → (ℕ → ℝ) → ℝ :=
      fun y xRef z sample => ((U y xRef z sample).untopD 0 : ℝ≥0)
    let A : E → E → (E × E) → ℝ≥0 → Set (ℕ → ℝ) :=
      fun y xRef z T => {sample | (0 : WithTop ℝ≥0) < U y xRef z sample ∧
        U y xRef z sample ≤ (T : WithTop ℝ≥0)}
    let d : E → E → (E × E) → ℝ → ℝ := fun y xRef z s =>
      rate xRef (Φ y xRef s z) * Real.exp (-Λ y xRef z (Real.toNNReal s))
    let ρ : E → E → (E × E) → ℝ≥0 → Measure ℝ := fun y xRef z T =>
      (volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))).withDensity
        (fun s => ENNReal.ofReal (d y xRef z s))
    let J : E → E → (E × E) → ℝ → (ℝ≥0 × (E × E)) :=
      fun y xRef z s => (Real.toNNReal s, S xRef (Φ y xRef s z))
    ∀ y xRef : E, ∀ z : E × E,
      Measurable (U y xRef z) ∧ Measurable (F y xRef z) ∧
      Measurable (J y xRef z) ∧
      (∀ T : ℝ≥0,
        MeasurableSet (A y xRef z T) ∧
        Measure.map (F y xRef z) (P.restrict (A y xRef z T)) = ρ y xRef z T ∧
        Measure.map (fun sample => J y xRef z (F y xRef z sample))
          (P.restrict (A y xRef z T)) = Measure.map (J y xRef z) (ρ y xRef z T) ∧
        IsFiniteMeasure (ρ y xRef z T) ∧
        (ρ y xRef z T).real Set.univ = 1 - Real.exp (-Λ y xRef z T) ∧
        ρ y xRef z T Set.univ ≤ 1 ∧
        (∀ h : (ℝ≥0 × (E × E)) → ℝ, Measurable h →
          ∀ M : ℝ, 0 ≤ M → (∀ a, |h a| ≤ M) →
            Integrable h (Measure.map (J y xRef z) (ρ y xRef z T)) ∧
            Integrable (fun sample => h (J y xRef z (F y xRef z sample)))
              (P.restrict (A y xRef z T)) ∧
            Integrable (fun s => h (J y xRef z s) * d y xRef z s)
              (volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))) ∧
            (∫ sample, h (J y xRef z (F y xRef z sample))
                ∂P.restrict (A y xRef z T)) =
              ∫ s, h (J y xRef z s) * d y xRef z s
                ∂volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))))

-- Internal FTC ingredient of the sealed finite-density anchor; not the public result.
private theorem first_density_setIntegral
    (l : ℝ → ℝ) (hl : Continuous l) (t : ℝ) (ht : 0 ≤ t) :
    (∫ s in Set.Ioc 0 t, l s * Real.exp (-(∫ u in (0 : ℝ)..s, l u))) =
      1 - Real.exp (-(∫ u in (0 : ℝ)..t, l u)) := by
  let L : ℝ → ℝ := fun s => ∫ u in (0 : ℝ)..s, l u
  have hL (s : ℝ) : HasDerivAt L (l s) s :=
    intervalIntegral.integral_hasDerivAt_right (hl.intervalIntegrable _ _)
      hl.stronglyMeasurable.stronglyMeasurableAtFilter hl.continuousAt
  have hcL : Continuous L := continuous_iff_continuousAt.mpr fun s => (hL s).continuousAt
  have hd (s : ℝ) :
      HasDerivAt (fun s => 1 - Real.exp (-L s))
        (l s * Real.exp (-L s)) s := by
    simpa only [Pi.neg_apply, mul_neg, neg_mul, neg_neg, mul_comm]
      using (hL s).neg.exp.const_sub 1
  have hdC : Continuous (fun s => l s * Real.exp (-L s)) :=
    hl.mul hcL.neg.rexp
  have hf := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le ht
    ((continuous_const.sub hcL.neg.rexp).continuousOn)
    (fun s _ => hd s) (hdC.intervalIntegrable _ _)
  rw [intervalIntegral.integral_of_le ht] at hf
  simpa [L] using hf

private theorem first_density_measure_mass
    (l : ℝ → ℝ) (hl : Continuous l) (hn : ∀ s, 0 ≤ l s)
    (t : ℝ) (ht : 0 ≤ t) :
    ((volume.restrict (Set.Ioc 0 t)).withDensity
      (fun s => ENNReal.ofReal (l s * Real.exp (-(∫ u in (0 : ℝ)..s, l u)))))
        Set.univ = ENNReal.ofReal (1 - Real.exp (-(∫ u in (0 : ℝ)..t, l u))) := by
  have hL : Continuous (fun s => ∫ u in (0 : ℝ)..s, l u) :=
    continuous_iff_continuousAt.mpr fun s =>
      (intervalIntegral.integral_hasDerivAt_right (hl.intervalIntegrable _ _)
        hl.stronglyMeasurable.stronglyMeasurableAtFilter hl.continuousAt).continuousAt
  have hd : Continuous (fun s => l s * Real.exp (-(∫ u in (0 : ℝ)..s, l u))) :=
    hl.mul hL.neg.rexp
  rw [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ,
    ← ofReal_integral_eq_lintegral_ofReal
      ((intervalIntegrable_iff_integrableOn_Ioc_of_le ht).mp (hd.intervalIntegrable _ _))
      (Filter.Eventually.of_forall fun s => mul_nonneg (hn s) (Real.exp_pos _).le),
    first_density_setIntegral l hl t ht]

private theorem first_density_measure_Iic
    (l : ℝ → ℝ) (hl : Continuous l) (hn : ∀ s, 0 ≤ l s)
    (t a : ℝ) (ht : 0 ≤ t) (ha : 0 ≤ a) :
    ((volume.restrict (Set.Ioc 0 t)).withDensity
      (fun s => ENNReal.ofReal (l s * Real.exp (-(∫ u in (0 : ℝ)..s, l u)))))
        (Set.Iic a) = ENNReal.ofReal (1 - Real.exp (-(∫ u in (0 : ℝ)..min t a, l u))) := by
  rw [withDensity_apply _ measurableSet_Iic,
    Measure.restrict_restrict measurableSet_Iic,
    Set.inter_comm (Set.Iic a), Set.Ioc_inter_Iic]
  have hh := first_density_measure_mass l hl hn (min t a) (le_min ht ha)
  simpa only [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ] using hh

private theorem finite_wait_mass
    {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (U : Ω → WithTop ℝ≥0) (hU : Measurable U) (L : ℝ≥0 → ℝ)
    (hL0 : L 0 = 0)
    (hsurv : ∀ t : ℝ≥0, P.real {sample | (t : WithTop ℝ≥0) < U sample} = Real.exp (-L t))
    (t : ℝ≥0) :
    P {sample | (0 : WithTop ℝ≥0) < U sample ∧ U sample ≤ (t : WithTop ℝ≥0)} =
      ENNReal.ofReal (1 - Real.exp (-L t)) := by
  have heq : {sample | (0 : WithTop ℝ≥0) < U sample ∧ U sample ≤ (t : WithTop ℝ≥0)} =
      {sample | (0 : WithTop ℝ≥0) < U sample} \ {sample | (t : WithTop ℝ≥0) < U sample} := by
    ext sample
    simp only [Set.mem_ofPred_eq, Set.mem_sdiff, not_lt]
  have hsub : {sample | (t : WithTop ℝ≥0) < U sample} ⊆
      {sample | (0 : WithTop ℝ≥0) < U sample} :=
    fun sample hsample => lt_of_le_of_lt
      (show (0 : WithTop ℝ≥0) ≤ (t : WithTop ℝ≥0) from
        WithTop.coe_le_coe.mpr (show (0 : ℝ≥0) ≤ t from bot_le)) hsample
  have hz : P.real {sample | (0 : WithTop ℝ≥0) < U sample} = 1 := by
    simpa only [WithTop.coe_zero, hL0, neg_zero, Real.exp_zero] using hsurv 0
  rw [heq, ← ofReal_measureReal,
    measureReal_sdiff hsub (measurableSet_Ioi.preimage hU), hz, hsurv t]

private theorem finite_wait_real_cdf
    {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (U : Ω → WithTop ℝ≥0) (hU : Measurable U) (L : ℝ≥0 → ℝ)
    (hL0 : L 0 = 0)
    (hsurv : ∀ t : ℝ≥0, P.real {sample | (t : WithTop ℝ≥0) < U sample} = Real.exp (-L t))
    (t : ℝ≥0) (a : ℝ) (ha : 0 ≤ a) :
    (P.restrict {sample | (0 : WithTop ℝ≥0) < U sample ∧ U sample ≤ (t : WithTop ℝ≥0)}).map
      (fun sample => (((U sample).untopD 0 : ℝ≥0) : ℝ))
      (Set.Iic a) = ENNReal.ofReal (1 - Real.exp (-L (min t (Real.toNNReal a)))) := by
  have hF : Measurable (fun sample => (((U sample).untopD 0 : ℝ≥0) : ℝ)) :=
    measurable_subtype_coe.comp (hU.untopD 0)
  rw [Measure.map_apply hF measurableSet_Iic,
    Measure.restrict_apply (measurableSet_Iic.preimage hF)]
  have heq : (fun sample => (((U sample).untopD 0 : ℝ≥0) : ℝ)) ⁻¹' Set.Iic a ∩
      {sample | (0 : WithTop ℝ≥0) < U sample ∧ U sample ≤ (t : WithTop ℝ≥0)} =
      {sample | (0 : WithTop ℝ≥0) < U sample ∧
        U sample ≤ ((min t (Real.toNNReal a) : ℝ≥0) : WithTop ℝ≥0)} := by
    ext sample
    cases hh : U sample using WithTop.recTopCoe with
    | top =>
      simp only [hh, Set.mem_inter_iff, Set.mem_preimage, Set.mem_Iic, Set.mem_ofPred_eq]
      constructor
      · intro hs
        exact (not_le_of_gt (WithTop.coe_lt_top t) hs.2.2).elim
      · intro hs
        exact (not_le_of_gt (WithTop.coe_lt_top (min t (Real.toNNReal a))) hs.2).elim
    | coe s =>
      simp only [hh, Set.mem_inter_iff, Set.mem_preimage, Set.mem_Iic,
        Set.mem_ofPred_eq, WithTop.untopD_coe, WithTop.coe_le_coe, le_min_iff,
        Real.le_toNNReal_iff_coe_le ha]
      tauto
  rw [heq]
  exact finite_wait_mass P U hU L hL0 hsurv _

set_option maxHeartbeats 1000000 in
theorem actual_finite_first_event_law
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_finite_first_event_law_statement hα hαβ hV hH hη hβη := by
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
  let U : E → E → (E × E) → (ℕ → ℝ) → WithTop ℝ≥0 :=
    fun y xRef z sample => τ y xRef z (ε sample 0)
  let F : E → E → (E × E) → (ℕ → ℝ) → ℝ :=
    fun y xRef z sample => ((U y xRef z sample).untopD 0 : ℝ≥0)
  let A : E → E → (E × E) → ℝ≥0 → Set (ℕ → ℝ) :=
    fun y xRef z T => {sample | (0 : WithTop ℝ≥0) < U y xRef z sample ∧
      U y xRef z sample ≤ (T : WithTop ℝ≥0)}
  let d : E → E → (E × E) → ℝ → ℝ := fun y xRef z s =>
    rate xRef (Φ y xRef s z) * Real.exp (-Λ y xRef z (Real.toNNReal s))
  let ρ : E → E → (E × E) → ℝ≥0 → Measure ℝ := fun y xRef z T =>
    (volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))).withDensity
      (fun s => ENNReal.ofReal (d y xRef z s))
  let J : E → E → (E × E) → ℝ → (ℝ≥0 × (E × E)) :=
    fun y xRef z s => (Real.toNNReal s, S xRef (Φ y xRef s z))
  change
  ∀ y xRef : E, ∀ z : E × E,
    Measurable (U y xRef z) ∧ Measurable (F y xRef z) ∧
    Measurable (J y xRef z) ∧
    (∀ T : ℝ≥0,
      MeasurableSet (A y xRef z T) ∧
      Measure.map (F y xRef z) (P.restrict (A y xRef z T)) = ρ y xRef z T ∧
      Measure.map (fun sample => J y xRef z (F y xRef z sample))
        (P.restrict (A y xRef z T)) = Measure.map (J y xRef z) (ρ y xRef z T) ∧
      IsFiniteMeasure (ρ y xRef z T) ∧
      (ρ y xRef z T).real Set.univ = 1 - Real.exp (-Λ y xRef z T) ∧
      ρ y xRef z T Set.univ ≤ 1 ∧
      (∀ h : (ℝ≥0 × (E × E)) → ℝ, Measurable h →
        ∀ M : ℝ, 0 ≤ M → (∀ a, |h a| ≤ M) →
          Integrable h (Measure.map (J y xRef z) (ρ y xRef z T)) ∧
          Integrable (fun sample => h (J y xRef z (F y xRef z sample)))
            (P.restrict (A y xRef z T)) ∧
          Integrable (fun s => h (J y xRef z s) * d y xRef z s)
            (volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))) ∧
          (∫ sample, h (J y xRef z (F y xRef z sample))
              ∂P.restrict (A y xRef z T)) =
            ∫ s, h (J y xRef z s) * d y xRef z s
              ∂volume.restrict (Set.Ioc (0 : ℝ) (T : ℝ))))
  rcases ActualHazardClock.actual_integrated_hazard_clock_laws hα hαβ hV hH hη hβη with
    ⟨hΛC, _, _, hΛbasic, _, _, hτM, hW, _, _⟩
  change Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
    Λ a.1.1.1 a.1.1.2 a.1.2 a.2) at hΛC
  change Measurable (fun a : (E × E) × (E × E) × ℝ≥0 =>
    τ a.1.1 a.1.2 a.2.1 a.2.2) at hτM
  have hflow := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hb := ActualBounceRate.actual_bounce_rate_energy_laws hα hαβ hV hH hη hβη
  have hinput :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
  letI : IsProbabilityMeasure P := hinput.1
  intro y xRef z
  have hφ : Continuous (fun s : ℝ => Φ y xRef s z) := by
    have hargs : Continuous (fun s : ℝ => ((y, xRef), s, z)) :=
      continuous_const.prodMk (continuous_id.prodMk continuous_const)
    exact hflow.1.comp hargs
  let l : ℝ → ℝ := fun s => rate xRef (Φ y xRef s z)
  have hl : Continuous l := by
    have hargs : Continuous (fun s : ℝ => (xRef, Φ y xRef s z)) :=
      continuous_const.prodMk hφ
    exact hb.2.1.comp hargs
  have hn (s : ℝ) : 0 ≤ l s := hb.2.2.2.2.2.2.2.1 xRef (Φ y xRef s z) |>.1
  let g : ℝ → WithTop ℝ≥0 := fun e => τ y xRef z (Real.toNNReal e)
  have hgM : Measurable g := by
    have hargs : Measurable (fun e : ℝ => ((y, xRef), z, Real.toNNReal e)) :=
      measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal)
    have hc := hτM.comp hargs
    exact hc
  have hUM : Measurable (U y xRef z) := hgM.comp (measurable_pi_apply 0)
  have hFM : Measurable (F y xRef z) := measurable_subtype_coe.comp (hUM.untopD 0)
  have hJM : Measurable (J y xRef z) := by
    have hargs : Measurable (fun s : ℝ => (xRef, Φ y xRef s z)) :=
      measurable_const.prodMk hφ.measurable
    exact measurable_real_toNNReal.prodMk (hb.1.comp hargs)
  have hUlaw : P.map (U y xRef z) = (expMeasure (1 : ℝ)).map g := by
    calc
      P.map (U y xRef z) = (P.map (fun sample : ℕ → ℝ => sample 0)).map g :=
        (Measure.map_map hgM (measurable_pi_apply 0)).symm
      _ = (expMeasure (1 : ℝ)).map g := by rw [(hinput.2.1 0).2.2]
  have hsurv (t : ℝ≥0) :
      P.real {sample | (t : WithTop ℝ≥0) < U y xRef z sample} =
        Real.exp (-Λ y xRef z t) := by
    calc
      P.real {sample | (t : WithTop ℝ≥0) < U y xRef z sample} =
          (P.map (U y xRef z)).real (Set.Ioi (t : WithTop ℝ≥0)) :=
        (map_measureReal_apply hUM measurableSet_Ioi).symm
      _ = Real.exp (-Λ y xRef z t) := by
        rw [hUlaw]
        exact (hW y xRef z).2 t
  have hLC : Continuous (Λ y xRef z) := by
    have hargs : Continuous (fun t : ℝ≥0 => (((y, xRef), z), t)) :=
      continuous_const.prodMk continuous_id
    exact hΛC.comp hargs
  have hdC : Continuous (d y xRef z) :=
    hl.mul (hLC.comp continuous_real_toNNReal).neg.rexp
  have hdn (s : ℝ) : 0 ≤ d y xRef z s := mul_nonneg (hn s) (Real.exp_pos _).le
  refine ⟨hUM, hFM, hJM, ?_⟩
  intro T
  have hAM : MeasurableSet (A y xRef z T) :=
    (measurableSet_Ioi.preimage hUM).inter (measurableSet_Iic.preimage hUM)
  let D : Measure ℝ := (volume.restrict (Set.Ioc 0 (T : ℝ))).withDensity
    (fun s => ENNReal.ofReal (l s * Real.exp (-(∫ u in (0 : ℝ)..s, l u))))
  have hρD : ρ y xRef z T = D := by
    apply withDensity_congr_ae
    filter_upwards [ae_restrict_mem measurableSet_Ioc] with s hs
    simp only [d, Λ, Real.coe_toNNReal s hs.1.le, l]
  have hmap : (P.restrict (A y xRef z T)).map (F y xRef z) = ρ y xRef z T := by
    apply Measure.ext_of_Iic
    intro a
    by_cases ha : 0 ≤ a
    · rw [finite_wait_real_cdf P (U y xRef z) hUM (Λ y xRef z)
        (hΛbasic y xRef z).1 hsurv T a ha, hρD]
      rw [first_density_measure_Iic l hl hn (T : ℝ) a T.coe_nonneg ha]
      congr 2
      simp only [Λ, l, NNReal.coe_min, Real.coe_toNNReal a ha]
    · have hneg : a < 0 := lt_of_not_ge ha
      have hpre : (F y xRef z) ⁻¹' Set.Iic a = ∅ := by
        apply Set.eq_empty_iff_forall_notMem.mpr
        intro sample hs
        exact (not_le_of_gt hneg) (le_trans (NNReal.coe_nonneg _) hs)
      have hint : Set.Iic a ∩ Set.Ioc (0 : ℝ) (T : ℝ) = ∅ := by
        apply Set.eq_empty_iff_forall_notMem.mpr
        intro s hs
        exact (not_lt_of_ge hs.2.1.le) (lt_of_le_of_lt hs.1 hneg)
      rw [Measure.map_apply hFM measurableSet_Iic, hpre]
      rw [hρD, withDensity_apply _ measurableSet_Iic,
        Measure.restrict_restrict measurableSet_Iic, hint]
      simp
  letI : IsFiniteMeasure (ρ y xRef z T) := by rw [← hmap]; infer_instance
  have hmarked : (P.restrict (A y xRef z T)).map
      (fun sample => J y xRef z (F y xRef z sample)) = (ρ y xRef z T).map (J y xRef z) := by
    rw [← hmap, Measure.map_map hJM hFM]
    rfl
  have hmass : (ρ y xRef z T) Set.univ =
      ENNReal.ofReal (1 - Real.exp (-Λ y xRef z T)) := by
    rw [hρD]
    exact first_density_measure_mass l hl hn (T : ℝ) T.coe_nonneg
  have hmassnn : 0 ≤ 1 - Real.exp (-Λ y xRef z T) := by
    exact sub_nonneg.mpr
      (Real.exp_le_one_iff.mpr (neg_nonpos.mpr ((hΛbasic y xRef z).2.1 T)))
  have hmassreal : (ρ y xRef z T).real Set.univ =
      1 - Real.exp (-Λ y xRef z T) := by
    rw [measureReal_def, hmass, ENNReal.toReal_ofReal hmassnn]
  have hmassle : (ρ y xRef z T) Set.univ ≤ 1 := by
    rw [hmass]
    exact (ENNReal.ofReal_le_one).mpr (sub_le_self _ (Real.exp_pos _).le)
  refine ⟨hAM, hmap, hmarked, inferInstance, hmassreal, hmassle, ?_⟩
  intro h hh M hM hbound
  have hIntMark : Integrable h ((ρ y xRef z T).map (J y xRef z)) :=
    Integrable.of_bound hh.aestronglyMeasurable M
      (Filter.Eventually.of_forall fun a => by simpa only [Real.norm_eq_abs] using hbound a)
  have hIntP : Integrable (fun sample => h (J y xRef z (F y xRef z sample)))
      (P.restrict (A y xRef z T)) :=
    Integrable.of_bound ((hh.comp hJM).comp hFM).aestronglyMeasurable M
      (Filter.Eventually.of_forall fun sample => by
        simpa only [Real.norm_eq_abs] using hbound (J y xRef z (F y xRef z sample)))
  have hIntρ : Integrable (fun s => h (J y xRef z s)) (ρ y xRef z T) :=
    Integrable.of_bound (hh.comp hJM).aestronglyMeasurable M
      (Filter.Eventually.of_forall fun s => by
        simpa only [Real.norm_eq_abs] using hbound (J y xRef z s))
  have hWeightM : Measurable (fun s => ENNReal.ofReal (d y xRef z s)) :=
    hdC.measurable.ennreal_ofReal
  have hWeightTop : ∀ᵐ s ∂volume.restrict (Set.Ioc 0 (T : ℝ)),
      ENNReal.ofReal (d y xRef z s) < ⊤ :=
    Filter.Eventually.of_forall fun _ => ENNReal.ofReal_lt_top
  have hIntWeighted : Integrable (fun s => h (J y xRef z s) * d y xRef z s)
      (volume.restrict (Set.Ioc 0 (T : ℝ))) := by
    have hc := (integrable_withDensity_iff_integrable_smul' hWeightM hWeightTop).mp hIntρ
    simpa only [ENNReal.toReal_ofReal (hdn _), smul_eq_mul, mul_comm] using hc
  refine ⟨hIntMark, hIntP, hIntWeighted, ?_⟩
  calc
    (∫ sample, h (J y xRef z (F y xRef z sample)) ∂P.restrict (A y xRef z T)) =
        ∫ a, h a ∂((ρ y xRef z T).map (J y xRef z)) := by
      rw [← hmarked]
      exact (integral_map (hJM.comp hFM).aemeasurable hh.aestronglyMeasurable).symm
    _ = ∫ s, h (J y xRef z s) ∂ρ y xRef z T :=
      integral_map hJM.aemeasurable hh.aestronglyMeasurable
    _ = ∫ s, h (J y xRef z s) * d y xRef z s ∂volume.restrict (Set.Ioc 0 (T : ℝ)) := by
      rw [integral_withDensity_eq_integral_toReal_smul hWeightM hWeightTop]
      simp only [ENNReal.toReal_ofReal (hdn _), smul_eq_mul, mul_comm]


end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw
