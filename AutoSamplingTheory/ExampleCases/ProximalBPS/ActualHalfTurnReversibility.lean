import AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality
import Mathlib.Probability.Kernel.Invariance

/-!
# Detailed balance of the actual PBPS independent-reference half-turn

Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Proposition3.2 and
Appendix A.2 (832--853). The bounded-test adapter uses the actual signed
phase duality in Appendix A.1 (819--820), absorbs momentum flips in position
observables, and then averages an independent reference drawn from q_y.

All six original analytic assumptions and the exact returned-position kernel
are retained. Normalization, probability, bounded signed Fubini and conversion
from real indicator integrals to ENNReal fluxes are internal proof obligations.
The raw covered-arc/fallback laws identify the two process witnesses pointwise.

The private integration adapters are implementation, not extra public leaves.
This result is not a restart/semigroup law, an augmented all-L2 realization,
hypocoercive rate, implementation-error or expected-cost theorem. Local proof
compilation, independent source fidelity and integration remain separate gates.
-/

open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal
noncomputable section
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHalfTurnReversibility

/-- Convert a finite real indicator pairing to the exact ENNReal rectangle flux. -/
private theorem flux_ofReal
    {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
    (κ : Kernel X X) [IsMarkovKernel κ]
    {A B : Set X} (hA : MeasurableSet A) (hB : MeasurableSet B) :
    ENNReal.ofReal (∫ x, A.indicator (fun _ => (1 : ℝ)) x *
      (∫ z, B.indicator (fun _ => (1 : ℝ)) z ∂κ x) ∂μ) =
      ∫⁻ x in A, κ x B ∂μ := by
  have hi : Integrable (fun x => (κ x).real B) (μ.restrict A) := by
    apply Integrable.of_bound
      (κ.measurable_coe hB).ennreal_toReal.aestronglyMeasurable 1
    exact Eventually.of_forall fun x => by
      simpa only [Real.norm_eq_abs, abs_of_nonneg ENNReal.toReal_nonneg,
        Measure.real] using
        (measureReal_le_one (μ := κ x) (s := B))
  have hreal : (∫ x, A.indicator (fun _ => (1 : ℝ)) x *
      (∫ z, B.indicator (fun _ => (1 : ℝ)) z ∂κ x) ∂μ) =
      ∫ x in A, (κ x).real B ∂μ := by
    have hIB (x : X) : (∫ z, B.indicator (fun _ => (1 : ℝ)) z ∂κ x) =
        (κ x).real B := integral_indicator_one hB
    simp_rw [hIB]
    rw [← integral_indicator hA]
    congr 1
    funext x
    by_cases hx : x ∈ A <;> simp [hx]
  rw [hreal, ofReal_integral_eq_lintegral_ofReal hi
    (Eventually.of_forall fun _ => measureReal_nonneg)]
  apply lintegral_congr_ae
  exact Eventually.of_forall fun x => ENNReal.ofReal_toReal (measure_ne_top (κ x) B)

/-- Test symmetry on measurable indicators; no countability/singleton criterion. -/
private theorem reversible_of_bounded_pairing
    {X : Type*} [MeasurableSpace X] (μ : Measure X) [IsFiniteMeasure μ]
    (κ : Kernel X X) [IsMarkovKernel κ]
    (hsym : ∀ f g : X → ℝ, Measurable f → Measurable g →
      (∀ x, |f x| ≤ 1) → (∀ x, |g x| ≤ 1) →
      (∫ x, f x * (∫ z, g z ∂κ x) ∂μ) =
        ∫ x, g x * (∫ z, f z ∂κ x) ∂μ) : κ.IsReversible μ := by
  intro A B hA hB
  rw [← flux_ofReal μ κ hA hB, ← flux_ofReal μ κ hB hA]
  congr 1
  apply hsym _ _ (measurable_const.indicator hA) (measurable_const.indicator hB)
  · intro x
    by_cases hx : x ∈ A <;> simp [hx]
  · intro x
    by_cases hx : x ∈ B <;> simp [hx]

/-- All products are probability laws; bounded signed Fubini swaps input and independent reference. -/
private theorem pairing_eq_reference_average
    {X Y W : Type*} [MeasurableSpace X] [MeasurableSpace Y] [MeasurableSpace W]
    (q : Measure X) (γ : Measure Y) (P : Measure W)
    [IsProbabilityMeasure q] [IsProbabilityMeasure γ] [IsProbabilityMeasure P]
    (F : X → X → Y → W → X)
    (hF : Measurable (fun a : ((X × X) × Y) × W =>
      F a.1.1.2 a.1.1.1 a.1.2 a.2))
    (κ : Kernel X X)
    (hlaw : ∀ x, κ x = Measure.map
      (fun a : (X × Y) × W => F a.1.1 x a.1.2 a.2) ((q.prod γ).prod P))
    (f g : X → ℝ) (hf : Measurable f) (hg : Measurable g)
    (hfb : ∀ x, |f x| ≤ 1) (hgb : ∀ x, |g x| ≤ 1) :
    (∫ x, f x * (∫ z, g z ∂κ x) ∂q) =
      ∫ r, (∫ z : X × Y, f z.1 * (∫ w, g (F r z.1 z.2 w) ∂P)
        ∂q.prod γ) ∂q := by
  let op : X → X → Y → ℝ := fun x r p => ∫ w, g (F r x p w) ∂P
  have hopm : Measurable (fun a : (X × X) × Y => op a.1.1 a.1.2 a.2) :=
    (hg.comp hF).stronglyMeasurable.integral_prod_right'.measurable
  have hopb (x r : X) (p : Y) : |op x r p| ≤ 1 := by
    have hh := norm_integral_le_of_norm_le_const (μ := P)
      (f := fun w => g (F r x p w))
      (Eventually.of_forall fun w => by
        simpa only [Real.norm_eq_abs] using hgb (F r x p w))
    simpa [op] using hh
  have hdb (x r : X) (p : Y) : |f x * op x r p| ≤ 1 := by
    calc
      |f x * op x r p| = |f x| * |op x r p| := abs_mul _ _
      _ ≤ 1 * 1 := mul_le_mul (hfb x) (hopb x r p) (abs_nonneg _) zero_le_one
      _ = 1 := mul_one 1
  have hdm : Measurable (fun a : (X × X) × Y =>
      f a.1.1 * op a.1.1 a.1.2 a.2) := (hf.comp measurable_fst.fst).mul hopm
  have hdi : Integrable (fun a : (X × X) × Y =>
      f a.1.1 * op a.1.1 a.1.2 a.2) ((q.prod q).prod γ) :=
    Integrable.of_bound hdm.aestronglyMeasurable 1
      (Eventually.of_forall fun a => by
        simpa only [Real.norm_eq_abs] using hdb a.1.1 a.1.2 a.2)
  have hinner (x : X) : (∫ z, g z ∂κ x) = ∫ r, ∫ p, op x r p ∂γ ∂q := by
    have hfx : Measurable (fun a : (X × Y) × W => F a.1.1 x a.1.2 a.2) :=
      hF.comp (((measurable_const.prodMk measurable_fst.fst).prodMk
        measurable_fst.snd).prodMk measurable_snd)
    have hi : Integrable (fun a : (X × Y) × W => g (F a.1.1 x a.1.2 a.2))
        ((q.prod γ).prod P) :=
      Integrable.of_bound (hg.comp hfx).aestronglyMeasurable 1
        (Eventually.of_forall fun a => by
          simpa only [Real.norm_eq_abs] using hgb (F a.1.1 x a.1.2 a.2))
    rw [hlaw x, integral_map hfx.aemeasurable hg.aestronglyMeasurable,
      integral_prod _ hi]
    exact integral_prod _ hi.integral_prod_left
  calc
    (∫ x, f x * (∫ z, g z ∂κ x) ∂q) =
        ∫ x, ∫ r, ∫ p, f x * op x r p ∂γ ∂q ∂q := by
      simp_rw [hinner, ← integral_const_mul]
    _ = ∫ r, ∫ x, ∫ p, f x * op x r p ∂γ ∂q ∂q :=
      integral_integral_swap hdi.integral_prod_left
    _ = ∫ r, (∫ z : X × Y, f z.1 * (∫ w, g (F r z.1 z.2 w) ∂P)
        ∂q.prod γ) ∂q := by
      apply integral_congr_ae
      exact Eventually.of_forall fun r => by
        have hm : Measurable (fun z : X × Y => f z.1 * op z.1 r z.2) :=
          hdm.comp ((measurable_fst.prodMk measurable_const).prodMk measurable_snd)
        have hi : Integrable (fun z : X × Y => f z.1 * op z.1 r z.2)
            (q.prod γ) :=
          Integrable.of_bound hm.aestronglyMeasurable 1
            (Eventually.of_forall fun z => by
              simpa only [Real.norm_eq_abs] using hdb z.1 r z.2)
        exact (integral_prod _ hi).symm

/-- Combine the exact raw returned law with fixed-reference bounded position duality. -/
private theorem reversible_of_reference_average
    {X Y W : Type*} [MeasurableSpace X] [MeasurableSpace Y] [MeasurableSpace W]
    (q : Measure X) (γ : Measure Y) (P : Measure W)
    [IsProbabilityMeasure q] [IsProbabilityMeasure γ] [IsProbabilityMeasure P]
    (F : X → X → Y → W → X)
    (hF : Measurable (fun a : ((X × X) × Y) × W =>
      F a.1.1.2 a.1.1.1 a.1.2 a.2))
    (κ : Kernel X X) [IsMarkovKernel κ]
    (hlaw : ∀ x, κ x = Measure.map
      (fun a : (X × Y) × W => F a.1.1 x a.1.2 a.2) ((q.prod γ).prod P))
    (hdual : ∀ r : X, ∀ f g : X → ℝ, Measurable f → Measurable g →
      (∀ x, |f x| ≤ 1) → (∀ x, |g x| ≤ 1) →
      (∫ z : X × Y, f z.1 * (∫ w, g (F r z.1 z.2 w) ∂P) ∂q.prod γ) =
        ∫ z : X × Y, g z.1 * (∫ w, f (F r z.1 z.2 w) ∂P) ∂q.prod γ) :
    κ.IsReversible q := by
  apply reversible_of_bounded_pairing q κ
  intro f g hf hg hfb hgb
  rw [pairing_eq_reference_average q γ P F hF κ hlaw f g hf hg hfb hgb,
    pairing_eq_reference_average q γ P F hF κ hlaw g f hg hf hgb hfb]
  exact integral_congr_ae (Eventually.of_forall fun r => hdual r f g hf hg hfb hgb)

open InnerProductSpace
open scoped ContDiff NNReal Topology Interval BigOperators
set_option maxHeartbeats 1800000
set_option maxRecDepth 10000

private def actual_half_turn_reversibility_statement
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
          Z y w.1.1 (x, w.1.2) tπ w.2 = Φ y w.1.1 ((tπ - a.1 : ℝ≥0) : ℝ) a.2)

/-- The same actual returned-position half-turn satisfies detailed balance for every center.
The original six hypotheses suffice; initialization/raw-path outputs are retained. -/
theorem actual_half_turn_reversible
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_half_turn_reversibility_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_half_turn_reversibility_statement
  intro P ε c Φ S rate Λ τ next record eventTime q γ M tπ
  obtain ⟨Z, hZM, hZa, hZf, hgood, R, hR, hRq, H, hHK, hHlaw, hH0, hHgood⟩ :=
    IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel hα hαβ hV hH hη hβη
  refine ⟨Z, hZM, hZa, hZf, hgood, R, hR, hRq, H, hHK, ?_, hHlaw, hH0, hHgood⟩
  obtain ⟨Zb, _hZbm, hZba, hZbf, _hZb0, hD⟩ :=
    ActualBoundedGibbsDuality.actual_bounded_gibbs_duality hα hαβ hV hH hη hβη
  have hZd : Zb = Z := by
    funext y r z t w
    by_cases hw : ∃ n : ℕ, eventTime y r z (ε w) n ≤ (t : WithTop ℝ≥0) ∧
        (t : WithTop ℝ≥0) < eventTime y r z (ε w) (n + 1)
    · obtain ⟨n, hn, hn'⟩ := hw
      cases hr : record y r z (ε w) n with
      | inl a =>
          exact (hZba y r z w t n a (by exact ⟨hn, hn'⟩) hr).trans
            (hZa y r z w t n a hn hn' hr).symm
      | inr a =>
          have hnot : ¬ (⊤ : WithTop ℝ≥0) ≤ (t : WithTop ℝ≥0) :=
            WithTop.not_top_le_coe t
          apply False.elim
          apply hnot
          simpa only [eventTime, hr, Sum.elim_inr] using hn
    · exact (hZbf y r z w t hw).trans (hZf y r z w t hw).symm
  subst Zb
  letI : IsMarkovKernel R := hR
  letI : IsMarkovKernel H := hHK
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  letI : IsProbabilityMeasure γ := inferInstanceAs (IsProbabilityMeasure (stdGaussian E))
  intro y
  letI : IsProbabilityMeasure (q y) := by
    have he : R y = q y := hRq y
    rw [← he]
    infer_instance
  let κ : Kernel E E := H.comap (fun x : E => (y, x)) (by fun_prop)
  let F : E → E → E → (ℕ → ℝ) → E := fun r x p w => (Z y r (x, p) tπ w).1
  have hFM : Measurable (fun a : ((E × E) × E) × (ℕ → ℝ) =>
      F a.1.1.2 a.1.1.1 a.1.2 a.2) :=
    (hZM.comp (((measurable_const.prodMk measurable_fst.fst.snd).prodMk
      (measurable_fst.fst.fst.prodMk measurable_fst.snd)).prodMk
      (measurable_const.prodMk measurable_snd))).fst
  have hKl (x : E) : κ x = Measure.map
      (fun a : (E × E) × (ℕ → ℝ) => F a.1.1 x a.1.2 a.2)
      (((q y).prod γ).prod P) := hHlaw y x
  apply reversible_of_reference_average (q y) γ P F hFM κ hKl
  intro r f g hf hg hfb hgb
  have hbd := (hD y r tπ).2 (fun z : E × E => f z.1)
    (fun z : E × E => g z.1) 1 1 (hf.comp measurable_fst)
    (hg.comp measurable_fst) zero_le_one zero_le_one
    (fun z => hfb z.1) (fun z => hgb z.1)
  have hflux := hbd.2.2
  have hqeq : (volume : Measure E).tilted
      (fun x => -(V x + ‖x - y‖ ^ 2 / (2 * η))) = q y := by
    apply congrArg (fun U : E → ℝ => (volume : Measure E).tilted U)
    funext x
    ring
  change (∫ z : E × E, f z.1 * (∫ w, g (Z y r z tπ w).1 ∂P)
      ∂((volume : Measure E).tilted
        (fun x => -(V x + ‖x - y‖ ^ 2 / (2 * η)))).prod γ) =
    (∫ z : E × E, g z.1 * (∫ w, f (Z y r z tπ w).1 ∂P)
      ∂((volume : Measure E).tilted
        (fun x => -(V x + ‖x - y‖ ^ 2 / (2 * η)))).prod γ) at hflux
  rw [hqeq] at hflux
  exact hflux

end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHalfTurnReversibility
