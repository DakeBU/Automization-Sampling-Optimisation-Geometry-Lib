import Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Integral.Lebesgue.Map
import Mathlib.MeasureTheory.Function.SpecialFunctions.Basic
import Mathlib.MeasureTheory.Measure.WithDensity

/-!
# Radon--Nikodym and `withDensity` leaves

Small measure-normalization wrappers used by Chewi-style Gibbs-density
formalization.  These leaves deliberately do not prove measurability or
integrability of a concrete Gibbs density; they expose the reusable measure
contracts once those analytic hypotheses are supplied.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace RadonNikodym

open scoped ENNReal NNReal

open MeasureTheory

variable {α : Type*} [MeasurableSpace α]

section PiWithDensity

variable {ι : Type*} [Fintype ι]

set_option backward.isDefEq.respectTransparency false in
/-- ENNReal Fubini for products of per-coordinate functions over `Fin n`. -/
theorem lintegral_fin_nat_prod_eq_prod {n : ℕ} {E : Fin n → Type*}
    {mE : ∀ i, MeasurableSpace (E i)} {μ : (i : Fin n) → Measure (E i)}
    [∀ i, SigmaFinite (μ i)] {f : (i : Fin n) → E i → ℝ≥0∞}
    (hf : ∀ i, Measurable (f i)) :
    ∫⁻ x : (i : Fin n) → E i, ∏ i, f i (x i) ∂Measure.pi μ =
      ∏ i, ∫⁻ x, f i x ∂μ i := by
  induction n with
  | zero => simp
  | succ n ih =>
      have mp := measurePreserving_piFinSuccAbove μ 0
      have hProdMeas : Measurable fun x : (i : Fin (n + 1)) → E i => ∏ i, f i (x i) :=
        Finset.measurable_prod _ (fun i _ => (hf i).comp (measurable_pi_apply i))
      have hf0AE : AEMeasurable (f 0) (μ 0) := (hf 0).aemeasurable
      have hTailAE :
          AEMeasurable (fun y : (i : Fin n) → E i.succ => ∏ i, f i.succ (y i))
            (Measure.pi (fun i => μ i.succ)) :=
        (Finset.measurable_prod _ (fun i _ =>
          (hf _).comp (measurable_pi_apply i))).aemeasurable
      have ih' :
          ∫⁻ y : (i : Fin n) → E i.succ, ∏ i, f i.succ (y i)
              ∂Measure.pi (fun i : Fin n => μ i.succ) =
            ∏ i : Fin n, ∫⁻ x, f i.succ x ∂μ i.succ :=
        ih (E := fun i : Fin n => E i.succ) (μ := fun i : Fin n => μ i.succ)
          (f := fun i : Fin n => f i.succ) (fun i => hf _)
      calc
        ∫⁻ x : (i : Fin (n + 1)) → E i, ∏ i, f i (x i) ∂Measure.pi μ
            = ∫⁻ z : E 0 × ((i : Fin n) → E i.succ),
                f 0 z.1 * ∏ i, f i.succ (z.2 i)
                ∂((μ 0).prod (Measure.pi (fun i => μ i.succ))) := by
              rw [← mp.symm.lintegral_comp hProdMeas]
              simp_rw [MeasurableEquiv.piFinSuccAbove_symm_apply, Fin.insertNthEquiv,
                Fin.prod_univ_succ, Fin.insertNth_zero, Equiv.coe_fn_mk, Fin.cons_succ,
                Fin.zero_succAbove, cast_eq, Fin.cons_zero]
        _ = (∫⁻ x, f 0 x ∂μ 0) *
              ∫⁻ y : (i : Fin n) → E i.succ, ∏ i, f i.succ (y i)
                ∂Measure.pi (fun i : Fin n => μ i.succ) :=
              lintegral_prod_mul hf0AE hTailAE
        _ = (∫⁻ x, f 0 x ∂μ 0) * ∏ i : Fin n, ∫⁻ x, f i.succ x ∂μ i.succ := by
              rw [ih']
        _ = ∏ i, ∫⁻ x, f i x ∂μ i := by
              rw [← Fin.prod_univ_succ (fun i : Fin (n + 1) => ∫⁻ x, f i x ∂μ i)]

/-- ENNReal Fubini for products of per-coordinate functions over a finite type. -/
theorem lintegral_fintype_prod_eq_prod {E : ι → Type*}
    {mE : ∀ i, MeasurableSpace (E i)} {μ : (i : ι) → Measure (E i)}
    [∀ i, SigmaFinite (μ i)] {f : (i : ι) → E i → ℝ≥0∞}
    (hf : ∀ i, Measurable (f i)) :
    ∫⁻ x : (i : ι) → E i, ∏ i, f i (x i) ∂Measure.pi μ =
      ∏ i, ∫⁻ x, f i x ∂μ i := by
  let e := (Fintype.equivFin ι).symm
  have mp := measurePreserving_piCongrLeft (fun i => μ i) e
  have hMeas : Measurable fun x : (i : ι) → E i => ∏ i, f i (x i) :=
    Finset.measurable_prod _ (fun i _ => (hf i).comp (measurable_pi_apply i))
  rw [← mp.lintegral_comp hMeas]
  simp_rw [← e.prod_comp, MeasurableEquiv.coe_piCongrLeft,
    Equiv.piCongrLeft_apply_apply]
  exact lintegral_fin_nat_prod_eq_prod (fun i => hf _)

/-- A finite product measure tilted by a product density decomposes coordinatewise. -/
theorem pi_withDensity_prod {E : ι → Type*}
    {mE : ∀ i, MeasurableSpace (E i)} {μ : (i : ι) → Measure (E i)}
    [∀ i, SigmaFinite (μ i)] {f : (i : ι) → E i → ℝ≥0∞}
    (hf : ∀ i, Measurable (f i))
    [∀ i, SigmaFinite ((μ i).withDensity (f i))] :
    (Measure.pi μ).withDensity (fun x => ∏ i, f i (x i)) =
      Measure.pi (fun i => (μ i).withDensity (f i)) := by
  classical
  refine (Measure.pi_eq (μ := fun i => (μ i).withDensity (f i)) fun s hs => ?_).symm
  rw [withDensity_apply _ (MeasurableSet.univ_pi hs),
    ← lintegral_indicator (MeasurableSet.univ_pi hs)]
  have hIndic : ∀ x : (i : ι) → E i,
      (Set.univ.pi s).indicator (fun x => ∏ i, f i (x i)) x =
        ∏ i, (s i).indicator (f i) (x i) := by
    intro x
    by_cases hx : x ∈ Set.univ.pi s
    · rw [Set.indicator_of_mem hx]
      refine Finset.prod_congr rfl (fun i _ => ?_)
      rw [Set.indicator_of_mem (hx i (Set.mem_univ _))]
    · rw [Set.indicator_of_notMem hx]
      rw [Set.mem_univ_pi] at hx
      push Not at hx
      obtain ⟨i, hi⟩ := hx
      exact (Finset.prod_eq_zero (Finset.mem_univ i)
        (Set.indicator_of_notMem hi _)).symm
  simp_rw [hIndic]
  rw [lintegral_fintype_prod_eq_prod (fun i => (hf i).indicator (hs i))]
  refine Finset.prod_congr rfl (fun i _ => ?_)
  rw [lintegral_indicator (hs i), ← withDensity_apply _ (hs i)]

end PiWithDensity

/-- The total mass of a `withDensity` measure is the lintegral of the density. -/
theorem withDensity_univ_eq_lintegral (μ : MeasureTheory.Measure α) (f : α → ℝ≥0∞) :
    (μ.withDensity f) Set.univ = ∫⁻ x, f x ∂μ := by
  rw [withDensity_apply _ MeasurableSet.univ, MeasureTheory.Measure.restrict_univ]

/-- A density with lintegral one defines a probability measure after
`withDensity`. -/
theorem isProbabilityMeasure_withDensity_of_lintegral_eq_one
    (μ : MeasureTheory.Measure α) (f : α → ℝ≥0∞)
    (hf : ∫⁻ x, f x ∂μ = 1) :
    IsProbabilityMeasure (μ.withDensity f) :=
  ⟨by simpa [withDensity_univ_eq_lintegral] using hf⟩

/-- A real exponential tilt with Bochner integral one defines a probability
measure through `withDensity`.

This is the small ASTIS-owned version of the exponential-tilt normalization
pattern used in entropy-duality and Girsanov arguments. -/
theorem isProbabilityMeasure_withDensity_ofReal_exp_of_integral_eq_one
    (μ : MeasureTheory.Measure α) {U : α → ℝ}
    (hU_int : Integrable (fun x => Real.exp (U x)) μ)
    (hU_mass : ∫ x, Real.exp (U x) ∂μ = 1) :
    IsProbabilityMeasure
      (μ.withDensity fun x => ENNReal.ofReal (Real.exp (U x))) := by
  refine isProbabilityMeasure_withDensity_of_lintegral_eq_one μ
    (fun x => ENNReal.ofReal (Real.exp (U x))) ?_
  rw [← ofReal_integral_eq_lintegral_ofReal hU_int
    (ae_of_all _ fun _ => (Real.exp_pos _).le), hU_mass]
  norm_num

/-- A density with finite lintegral defines a finite measure after
`withDensity`. -/
theorem isFiniteMeasure_withDensity_of_lintegral_ne_top
    (μ : MeasureTheory.Measure α) (f : α → ℝ≥0∞)
    (hf : ∫⁻ x, f x ∂μ ≠ ∞) :
    IsFiniteMeasure (μ.withDensity f) :=
  isFiniteMeasure_withDensity hf

/-- Normalizing a finite nonzero density by the reciprocal of its lintegral
gives lintegral one. -/
theorem lintegral_inv_lintegral_mul_eq_one
    (μ : MeasureTheory.Measure α) (f : α → ℝ≥0∞)
    (h0 : ∫⁻ x, f x ∂μ ≠ 0)
    (hfin : ∫⁻ x, f x ∂μ ≠ ∞) :
    ∫⁻ x, (∫⁻ y, f y ∂μ)⁻¹ * f x ∂μ = 1 := by
  rw [lintegral_const_mul' _ f (ENNReal.inv_ne_top.mpr h0)]
  exact ENNReal.inv_mul_cancel h0 hfin

/-- A finite nonzero density defines a probability measure after reciprocal
lintegral normalization and `withDensity`. -/
theorem isProbabilityMeasure_withDensity_normalized_lintegral
    (μ : MeasureTheory.Measure α) (f : α → ℝ≥0∞)
    (h0 : ∫⁻ x, f x ∂μ ≠ 0)
    (hfin : ∫⁻ x, f x ∂μ ≠ ∞) :
    IsProbabilityMeasure
      (μ.withDensity fun x => (∫⁻ y, f y ∂μ)⁻¹ * f x) :=
  isProbabilityMeasure_withDensity_of_lintegral_eq_one μ
    (fun x => (∫⁻ y, f y ∂μ)⁻¹ * f x)
    (lintegral_inv_lintegral_mul_eq_one μ f h0 hfin)

/-- `withDensity` is always absolutely continuous with respect to its base
measure. -/
theorem withDensity_absolutelyContinuous_base
    (μ : MeasureTheory.Measure α) (f : α → ℝ≥0∞) :
    μ.withDensity f ≪ μ :=
  withDensity_absolutelyContinuous μ f

/-- Transport an explicit `withDensity` measure through a measurable
equivalence. -/
theorem measurableEquiv_map_withDensity
    {β : Type*} [MeasurableSpace β] (e : α ≃ᵐ β)
    (μ : MeasureTheory.Measure α) {f : α → ℝ≥0∞} (hf : Measurable f) :
    (μ.withDensity f).map e = (μ.map e).withDensity (fun y => f (e.symm y)) := by
  ext s hs
  rw [Measure.map_apply e.measurable hs]
  rw [withDensity_apply _ (e.measurable hs)]
  rw [withDensity_apply _ hs]
  rw [setLIntegral_map hs]
  · refine setLIntegral_congr_fun (e.measurable hs) ?_
    intro x _
    simp
  · fun_prop
  · exact e.measurable

/-- Radon--Nikodym reconstruction of an absolutely continuous measure. -/
theorem withDensity_rnDeriv_eq_of_absolutelyContinuous
    (μ ν : MeasureTheory.Measure α)
    [MeasureTheory.Measure.HaveLebesgueDecomposition μ ν]
    (hμν : μ ≪ ν) :
    ν.withDensity (μ.rnDeriv ν) = μ :=
  MeasureTheory.Measure.withDensity_rnDeriv_eq μ ν hμν

end RadonNikodym
end Measure
end TechnicalLemmas
end AutoSamplingTheory
