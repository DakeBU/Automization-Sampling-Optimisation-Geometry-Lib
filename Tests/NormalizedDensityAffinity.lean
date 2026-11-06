import AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity
import Mathlib.MeasureTheory.Integral.Bochner.SumMeasure
import Lean.Util.FoldConsts

open MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity
set_option autoImplicit false

-- Disjoint unit masses attain a=0, TV=1, detecting the normalized half factor.
example :
    let f : Fin 2 → ℝ := ![1, 0]
    let g : Fin 2 → ℝ := ![0, 1]
    let μ : Measure (Fin 2) := Measure.count
    let a := ∫ x, Real.sqrt (f x * g x) ∂μ
    let δ : ℝ := sSup {z | ∃ B : Set (Fin 2), MeasurableSet B ∧
      z = |(∫ x in B, f x ∂μ) - (∫ x in B, g x ∂μ)|}
    a = 0 ∧ δ = 1 := by
  classical
  dsimp only
  have h := normalized_density_tv_affinity (Measure.count : Measure (Fin 2))
    (f := ![1, 0]) (g := ![0, 1])
    (by intro x; fin_cases x <;> norm_num)
    (by intro x; fin_cases x <;> norm_num)
    (measurable_of_finite _) (measurable_of_finite _)
    Integrable.of_finite Integrable.of_finite
    (by simp [Fin.sum_univ_two]) (by simp [Fin.sum_univ_two])
  dsimp only at h
  constructor
  · simp [Fin.sum_univ_two]
  · rw [h.2.2.2.1]
    norm_num [Fin.sum_univ_two]

-- Identical normalized densities attain the opposite endpoint a=1, TV=0.
example :
    let f : Fin 2 → ℝ := ![1, 0]
    let μ : Measure (Fin 2) := Measure.count
    let a := ∫ x, Real.sqrt (f x * f x) ∂μ
    let δ : ℝ := sSup {z | ∃ B : Set (Fin 2), MeasurableSet B ∧
      z = |(∫ x in B, f x ∂μ) - (∫ x in B, f x ∂μ)|}
    a = 1 ∧ δ = 0 := by
  classical
  dsimp only
  have h := normalized_density_tv_affinity (Measure.count : Measure (Fin 2))
    (f := ![1, 0]) (g := ![1, 0])
    (by intro x; fin_cases x <;> norm_num)
    (by intro x; fin_cases x <;> norm_num)
    (measurable_of_finite _) (measurable_of_finite _)
    Integrable.of_finite Integrable.of_finite
    (by simp [Fin.sum_univ_two]) (by simp [Fin.sum_univ_two])
  dsimp only at h
  constructor
  · simp [Fin.sum_univ_two]
  · rw [h.2.2.2.1]
    simp

-- A.e. representative replacement preserves genuine affinity L1 and value,
-- without imposing pointwise positivity or measurability on the replacement.
example {α : Type*} [MeasurableSpace α] (μ : Measure α) {f g f' g' : α → ℝ}
    (hf0 : ∀ x, 0 ≤ f x) (hg0 : ∀ x, 0 ≤ g x)
    (hfm : Measurable f) (hgm : Measurable g)
    (hfi : Integrable f μ) (hgi : Integrable g μ)
    (hf1 : (∫ x, f x ∂μ) = 1) (hg1 : (∫ x, g x ∂μ) = 1)
    (hf' : f' =ᵐ[μ] f) (hg' : g' =ᵐ[μ] g) :
    Integrable (fun x => Real.sqrt (f' x * g' x)) μ ∧
    (∫ x, Real.sqrt (f' x * g' x) ∂μ) = (∫ x, Real.sqrt (f x * g x) ∂μ) ∧
    ∀ B : Set α, (∫ x in B, f' x ∂μ) = (∫ x in B, f x ∂μ) ∧
      (∫ x in B, g' x ∂μ) = (∫ x in B, g x ∂μ) := by
  have h := normalized_density_tv_affinity μ hf0 hg0 hfm hgm hfi hgi hf1 hg1
  have hae : (fun x => Real.sqrt (f' x * g' x)) =ᵐ[μ]
      (fun x => Real.sqrt (f x * g x)) := by
    filter_upwards [hf', hg'] with x hx hy
    rw [hx, hy]
  refine ⟨h.1.congr hae.symm, integral_congr_ae hae, ?_⟩
  intro B
  exact ⟨integral_congr_ae (ae_restrict_of_ae hf'),
    integral_congr_ae (ae_restrict_of_ae hg')⟩

#print axioms normalized_density_tv_affinity
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity.normalized_density_tv_affinity | throwError "Missing canonical node"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing canonical proof"
  let parents := proof.getUsedConstants.filter fun n =>
    n.toString.startsWith "AutoSamplingTheory" || n.toString.contains "integral_mul_le_Lp" ||
    n.toString.contains "integral_abs_eq_two" || n.toString.contains "memLp_two" ||
    n.toString.contains "integral_add_compl" || n.toString.contains "csSup"
  logInfo m!"ACTUAL COMPILED CANONICAL PARENTS {parents}"
