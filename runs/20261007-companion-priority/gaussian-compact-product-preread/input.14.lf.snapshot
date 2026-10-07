import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Integral.Prod

/-!
# Product-measure coordinate replacement leaves

Small `Measure.pi` facts for replacing one coordinate by an independent sample.
These are the product-measure and Fubini leaves needed by tensorization and
coordinate-slice arguments.  They deliberately do not introduce conditional
expectations, entropy, LSI, kernels, or weak-Fokker--Planck statements.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace Product

open MeasureTheory

open scoped ENNReal BigOperators

variable {n : ℕ} {Ω : Type*} [MeasurableSpace Ω]
variable {μs : Fin n → Measure Ω} [∀ i, IsProbabilityMeasure (μs i)]

/-- The coordinate-replacement map `(y, x) ↦ Function.update x i y` is measurable. -/
theorem measurable_update_prod_pi (i : Fin n) :
    Measurable (fun p : Ω × (Fin n → Ω) => Function.update p.2 i p.1) := by
  have h : (fun p : Ω × (Fin n → Ω) => Function.update p.2 i p.1) =
      (fun q : (Fin n → Ω) × Ω => Function.update q.1 i q.2) ∘ Prod.swap := rfl
  rw [h]
  exact (measurable_update' (a := i)).comp measurable_swap

/-- Replacing one coordinate of a product sample by an independent sample from
that coordinate preserves the product law. -/
theorem map_update_prod_pi (i : Fin n) :
    Measure.map (fun p : Ω × (Fin n → Ω) => Function.update p.2 i p.1)
      ((μs i).prod (Measure.pi μs)) = Measure.pi μs := by
  symm
  apply Measure.pi_eq
  intro s hs
  rw [Measure.map_apply]
  · have preimage_eq :
        (fun p : Ω × (Fin n → Ω) => Function.update p.2 i p.1) ⁻¹' (Set.univ.pi s) =
          (s i) ×ˢ (Set.univ.pi (fun j => if j = i then Set.univ else s j)) := by
      ext ⟨y, x⟩
      simp only [Set.mem_preimage, Set.mem_pi, Set.mem_univ, true_implies, Set.mem_prod]
      constructor
      · intro h
        constructor
        · have := h i
          simp only [Function.update_self] at this
          exact this
        · intro j
          by_cases hj : j = i
          · simp [hj]
          · have := h j
            simp only [Function.update_of_ne hj] at this
            simp [hj, this]
      · intro ⟨hy, hx⟩ j
        by_cases hj : j = i
        · subst hj
          simp only [Function.update_self]
          exact hy
        · simp only [Function.update_of_ne hj]
          have := hx j
          simp only [hj, ↓reduceIte] at this
          exact this
    rw [preimage_eq, Measure.prod_prod]
    have pi_eq :
        Measure.pi μs (Set.univ.pi (fun j => if j = i then Set.univ else s j)) =
          ∏ j : Fin n, (if j = i then 1 else μs j (s j)) := by
      rw [Measure.pi_pi]
      congr 1 with j
      by_cases hj : j = i
      · subst hj
        simp only [↓reduceIte, measure_univ]
      · simp only [hj, ↓reduceIte]
    rw [pi_eq]
    have h_ite : ∀ j, (if j = i then (1 : ℝ≥0∞) else μs j (s j)) =
        (if j ∈ Finset.univ.erase i then μs j (s j) else 1) := by
      intro j
      by_cases hj : j = i
      · simp [hj]
      · simp [hj]
    simp_rw [h_ite]
    rw [Fintype.prod_extend_by_one, mul_comm,
      Finset.prod_erase_mul _ _ (Finset.mem_univ i)]
  · exact measurable_update_prod_pi i
  · exact MeasurableSet.univ_pi (fun j => hs j)

/-- Measure-preserving wrapper for coordinate replacement under a product law. -/
theorem measurePreserving_update_prod_pi (i : Fin n) :
    MeasurePreserving (fun p : Ω × (Fin n → Ω) => Function.update p.2 i p.1)
      ((μs i).prod (Measure.pi μs)) (Measure.pi μs) :=
  ⟨measurable_update_prod_pi i, map_update_prod_pi i⟩

/-- Averaging a function after one-coordinate replacement over the fresh
coordinate and the original product sample recovers its product-law integral. -/
theorem integral_update_prod_pi_eq_integral
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    (i : Fin n) {f : (Fin n → Ω) → E}
    (hf : Integrable f (Measure.pi μs)) :
    ∫ y, ∫ x, f (Function.update x i y) ∂(Measure.pi μs) ∂(μs i) =
      ∫ z, f z ∂(Measure.pi μs) := by
  set g : Ω × (Fin n → Ω) → E := fun p => f (Function.update p.2 i p.1) with hg_def
  have h1 :
      ∫ y, ∫ x, f (Function.update x i y) ∂(Measure.pi μs) ∂(μs i) =
        ∫ p, g p ∂((μs i).prod (Measure.pi μs)) := by
    rw [integral_prod]
    exact (measurePreserving_update_prod_pi (μs := μs) i).integrable_comp
      hf.aestronglyMeasurable |>.mpr hf
  rw [h1, hg_def, ← integral_map]
  · rw [map_update_prod_pi (μs := μs) i]
  · exact (measurable_update_prod_pi i).aemeasurable
  · rw [map_update_prod_pi (μs := μs) i]
    exact hf.aestronglyMeasurable

/-- If a function is integrable on a finite product law, then for almost every
base product sample, the one-coordinate replacement slice is integrable in the
fresh coordinate. -/
theorem integrable_update_slice_ae
    {E : Type*} [NormedAddCommGroup E]
    (i : Fin n) {f : (Fin n → Ω) → E}
    (hf : Integrable f (Measure.pi μs)) :
    ∀ᵐ x ∂Measure.pi μs, Integrable (fun y => f (Function.update x i y)) (μs i) := by
  set g : Ω × (Fin n → Ω) → E := fun p => f (Function.update p.2 i p.1) with hg_def
  have hg_int : Integrable g ((μs i).prod (Measure.pi μs)) := by
    rw [hg_def]
    exact (measurePreserving_update_prod_pi (μs := μs) i).integrable_comp_of_integrable hf
  simpa [hg_def] using hg_int.prod_left_ae

end Product
end Measure
end TechnicalLemmas
end AutoSamplingTheory
