import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.MeasureTheory.Group.Prod
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Tactic.Module
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring


/-!
Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1 (A5, A6)
and the elementary reversal mechanics used in A8. Volume means the product
of the canonical finite-dimensional real Hilbert-space volumes.
The affine harmonic map is factored into translations and volume-preserving
shears; no unscaled phase-space isometry is asserted.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume
open MeasureTheory InnerProductSpace
open scoped ContDiff NNReal ENNReal
noncomputable section
set_option autoImplicit false

private def actual_phase_reversal_volume_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop :=
    let c : E → E → E := fun y r => y - η • gradient V r
    let h : E → E → E := fun r x => gradient V x - gradient V r
    let B : E → E → E := fun n p => p - (2 * inner ℝ p n / ‖n‖ ^ 2) • n
    let S : E → (E × E) → (E × E) := fun r z => (z.1, B (h r z.1) z.2)
    let R : (E × E) → (E × E) := fun z => (z.1, -z.2)
    let Φ : E → E → ℝ → (E × E) → (E × E) := fun y r u z =>
      (c y r + Real.cos u • (z.1 - c y r) + (Real.sqrt η * Real.sin u) • z.2,
       (-Real.sin u / Real.sqrt η) • (z.1 - c y r) + Real.cos u • z.2)
    let rate : E → (E × E) → ℝ := fun r z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (h r z.1))
    let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
    Measurable (fun a : (E × E) × ℝ × (E × E) => Φ a.1.1 a.1.2 a.2.1 a.2.2) ∧
    Measurable (fun a : E × (E × E) => S a.1 a.2) ∧
    Measurable (fun a : E × (E × E) => rate a.1 a.2) ∧
    (∀ y r : E, ∀ u : ℝ, MeasurePreserving (Φ y r u) ell ell) ∧
    (∀ r : E, MeasurePreserving (S r) ell ell) ∧
    MeasurePreserving R ell ell ∧
    (∀ y r : E, ∀ u : ℝ, ∀ z : E × E,
      Φ y r (-u) (Φ y r u z) = z ∧ Φ y r u (Φ y r (-u) z) = z) ∧
    (∀ r : E, ∀ z : E × E, S r (S r z) = z) ∧
    (∀ z : E × E, R (R z) = z) ∧
    (∀ y r : E, ∀ u : ℝ, ∀ z : E × E, R (Φ y r u (R z)) = Φ y r (-u) z) ∧
    (∀ r : E, ∀ z : E × E, R (S r z) = S r (R z)) ∧
    (∀ r : E, ∀ z : E × E, rate r (R (S r z)) = rate r z) ∧
    (∀ r : E, ∀ F : (E × E) → ℝ, Integrable F ell →
      Integrable (fun z => F (S r z)) ell ∧
      (∫ z, F (S r z) ∂ell) = ∫ z, F z ∂ell)

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private theorem lower_shear (a : ℝ) :
    MeasurePreserving (fun z : E × E => (z.1, z.2 + a • z.1))
      ((volume : Measure E).prod volume) ((volume : Measure E).prod volume) := by
  exact (MeasurePreserving.id (volume : Measure E)).skew_product
    (measurable_snd.add (measurable_fst.const_smul a))
    (Filter.Eventually.of_forall fun x => (measurePreserving_add_right volume (a • x)).map_eq)

private theorem upper_shear (a : ℝ) :
    MeasurePreserving (fun z : E × E => (z.1 + a • z.2, z.2))
      ((volume : Measure E).prod volume) ((volume : Measure E).prod volume) := by
  simpa only [Function.comp_def, Prod.swap_prod_mk, Prod.fst_swap, Prod.snd_swap] using
    (Measure.measurePreserving_swap.comp (lower_shear (E := E) a)).comp Measure.measurePreserving_swap

private theorem negate_phase :
    MeasurePreserving (fun z : E × E => (-z.1, -z.2))
      ((volume : Measure E).prod volume) ((volume : Measure E).prod volume) := by
  exact (LinearIsometryEquiv.neg ℝ).measurePreserving.prod
    (LinearIsometryEquiv.neg ℝ).measurePreserving

private theorem reflect_fiber (n : E) :
    MeasurePreserving (fun p : E => p - (2 * inner ℝ p n / ‖n‖ ^ 2) • n)
      volume volume := by
  let : CompleteSpace E := FiniteDimensional.complete ℝ E
  have heq : (fun p : E => p - (2 * inner ℝ p n / ‖n‖ ^ 2) • n) =
      (fun p => (ℝ ∙ n)ᗮ.reflection p) := by
    funext p
    rw [Submodule.reflection_orthogonal_apply, Submodule.reflection_singleton_apply]
    simp only [two_smul, neg_sub, div_eq_mul_inv, mul_smul]
    rw [real_inner_comm n p]
    module
  rw [heq]
  exact ((ℝ ∙ n)ᗮ.reflection).measurePreserving

private theorem area_matrix (a b c : ℝ) (hd : a * a - b * c = 1)
    (ha : 1 + a ≠ 0) :
    MeasurePreserving (fun z : E × E => (a • z.1 + b • z.2, c • z.1 + a • z.2))
      ((volume : Measure E).prod volume) ((volume : Measure E).prod volume) := by
  let k : ℝ := b / (1 + a)
  have hk : c * k = a - 1 := by
    dsimp [k]
    rw [← mul_div_assoc]
    apply (div_eq_iff ha).2
    nlinarith [hd]
  have hb : k * (1 + a) = b := by dsimp [k]; exact div_mul_cancel₀ b ha
  have heq : (fun z : E × E => (a • z.1 + b • z.2, c • z.1 + a • z.2)) =
      (fun z : E × E => (z.1 + k • z.2, z.2)) ∘
      (fun z : E × E => (z.1, z.2 + c • z.1)) ∘
      (fun z : E × E => (z.1 + k • z.2, z.2)) := by
    funext z
    apply Prod.ext <;> dsimp only [Function.comp_def] <;> match_scalars <;>
      nlinarith [hk, hb, congrArg (fun x : ℝ => k * x) hk]
  rw [heq]
  exact (upper_shear k).comp ((lower_shear c).comp (upper_shear k))

private theorem harmonic_linear (η u : ℝ) (hη : 0 < η) :
    MeasurePreserving (fun z : E × E =>
      (Real.cos u • z.1 + (Real.sqrt η * Real.sin u) • z.2,
       (-Real.sin u / Real.sqrt η) • z.1 + Real.cos u • z.2))
      ((volume : Measure E).prod volume) ((volume : Measure E).prod volume) := by
  have hr : Real.sqrt η ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hη)
  by_cases ha : 1 + Real.cos u = 0
  · have hc : Real.cos u = -1 := by linarith
    have hs : Real.sin u = 0 := by nlinarith [Real.sin_sq_add_cos_sq u, sq_nonneg (Real.sin u)]
    simpa only [hc, hs, mul_zero, neg_zero, zero_div, zero_smul, add_zero, zero_add,
      neg_one_smul] using (negate_phase (E := E))
  · apply area_matrix _ _ _ _ ha
    field_simp [hr]
    nlinarith [Real.sin_sq_add_cos_sq u]

private theorem translate_position (d : E) :
    MeasurePreserving (fun z : E × E => (d + z.1, z.2))
      ((volume : Measure E).prod volume) ((volume : Measure E).prod volume) := by
  exact (measurePreserving_add_left volume d).prod (MeasurePreserving.id volume)

private theorem harmonic_affine (η u : ℝ) (hη : 0 < η) (d : E) :
    MeasurePreserving (fun z : E × E =>
      (d + Real.cos u • (z.1 - d) + (Real.sqrt η * Real.sin u) • z.2,
       (-Real.sin u / Real.sqrt η) • (z.1 - d) + Real.cos u • z.2))
      ((volume : Measure E).prod volume) ((volume : Measure E).prod volume) := by
  have heq : (fun z : E × E =>
      (d + Real.cos u • (z.1 - d) + (Real.sqrt η * Real.sin u) • z.2,
       (-Real.sin u / Real.sqrt η) • (z.1 - d) + Real.cos u • z.2)) =
      (fun z : E × E => (d + z.1, z.2)) ∘
      (fun z : E × E => (Real.cos u • z.1 + (Real.sqrt η * Real.sin u) • z.2,
        (-Real.sin u / Real.sqrt η) • z.1 + Real.cos u • z.2)) ∘
      (fun z : E × E => (-d + z.1, z.2)) := by
    funext z
    apply Prod.ext <;> dsimp only [Function.comp_def] <;> module
  rw [heq]
  exact (translate_position d).comp ((harmonic_linear η u hη).comp (translate_position (-d)))


theorem actual_phase_reversal_volume_laws
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_phase_reversal_volume_statement hα hαβ hV hH hη hβη := by
  let c : E → E → E := fun y r => y - η • gradient V r
  let h : E → E → E := fun r x => gradient V x - gradient V r
  let B : E → E → E := fun n p => p - (2 * inner ℝ p n / ‖n‖ ^ 2) • n
  let S : E → (E × E) → (E × E) := fun r z => (z.1, B (h r z.1) z.2)
  let R : (E × E) → (E × E) := fun z => (z.1, -z.2)
  let Φ : E → E → ℝ → (E × E) → (E × E) := fun y r u z =>
      (c y r + Real.cos u • (z.1 - c y r) + (Real.sqrt η * Real.sin u) • z.2,
       (-Real.sin u / Real.sqrt η) • (z.1 - c y r) + Real.cos u • z.2)
  let rate : E → (E × E) → ℝ := fun r z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (h r z.1))
  let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
  change
    Measurable (fun a : (E × E) × ℝ × (E × E) => Φ a.1.1 a.1.2 a.2.1 a.2.2) ∧
    Measurable (fun a : E × (E × E) => S a.1 a.2) ∧
    Measurable (fun a : E × (E × E) => rate a.1 a.2) ∧
    (∀ y r : E, ∀ u : ℝ, MeasurePreserving (Φ y r u) ell ell) ∧
    (∀ r : E, MeasurePreserving (S r) ell ell) ∧
    MeasurePreserving R ell ell ∧
    (∀ y r : E, ∀ u : ℝ, ∀ z : E × E,
      Φ y r (-u) (Φ y r u z) = z ∧ Φ y r u (Φ y r (-u) z) = z) ∧
    (∀ r : E, ∀ z : E × E, S r (S r z) = z) ∧
    (∀ z : E × E, R (R z) = z) ∧
    (∀ y r : E, ∀ u : ℝ, ∀ z : E × E, R (Φ y r u (R z)) = Φ y r (-u) z) ∧
    (∀ r : E, ∀ z : E × E, R (S r z) = S r (R z)) ∧
    (∀ r : E, ∀ z : E × E, rate r (R (S r z)) = rate r z) ∧
    (∀ r : E, ∀ F : (E × E) → ℝ, Integrable F ell →
      Integrable (fun z => F (S r z)) ell ∧
      (∫ z, F (S r z) ∂ell) = ∫ z, F z ∂ell)

  have hf := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws
    hα hαβ hV hH hη hβη
  have hb := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws
    hα hαβ hV hH hη hβη
  have hSm : Measurable (fun a : E × (E × E) => S a.1 a.2) := hb.1
  have hSi (r : E) : Function.Involutive (S r) := fun z => (hb.2.2.2.2.2.1 r z).2
  have hSmp (r : E) : MeasurePreserving (S r) ell ell := by
    exact (MeasurePreserving.id (volume : Measure E)).skew_product
      (hSm.comp (measurable_const.prodMk measurable_id)).snd
      (Filter.Eventually.of_forall fun x => (reflect_fiber (h r x)).map_eq)
  refine ⟨hf.2.1, hSm, hb.2.2.1, ?_, hSmp, ?_, hf.2.2.2.2.1, hSi, ?_, ?_, ?_, ?_, ?_⟩
  · intro y r u
    exact harmonic_affine η u hη (c y r)
  · exact (MeasurePreserving.id (volume : Measure E)).prod
      (LinearIsometryEquiv.neg ℝ).measurePreserving
  · intro z
    simp [R]
  · intro y r u z
    apply Prod.ext <;> dsimp [R, Φ] <;>
      simp only [Real.cos_neg, Real.sin_neg, neg_neg, neg_div] <;> module
  · intro r z
    apply Prod.ext
    · rfl
    · dsimp [R, S, B]
      simp only [inner_neg_left, mul_neg, neg_div, neg_smul]
      module
  · intro r z
    have hflip : inner ℝ (B (h r z.1) z.2) (h r z.1) = -inner ℝ z.2 (h r z.1) :=
      (hb.2.2.2.2.1 (h r z.1) z.2).2.2
    dsimp [rate, R, S]
    rw [inner_neg_left, hflip, neg_neg]
  · intro r F hF
    refine ⟨(hSmp r).integrable_comp_of_integrable hF, ?_⟩
    exact (hSmp r).integral_comp
      (MeasurableEquiv.ofInvolutive (S r) (hSi r) (hSmp r).measurable).measurableEmbedding F

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume
