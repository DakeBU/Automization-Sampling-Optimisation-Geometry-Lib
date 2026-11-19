import B2MeasureCore
import HaarStabilizerBlock
import Mathlib.Tactic.Group

open Matrix MeasureTheory Metric Set
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional

set_option autoImplicit false

theorem rotate_one {n : ℕ} (z : S n) : rotate (1 : O n) z = z := by
  apply Subtype.ext
  apply (WithLp.equiv 2 (Fin n → ℝ)).injective
  change WithLp.ofLp (rotate (1 : O n) z).val = WithLp.ofLp z.val
  rw [rotate_val]
  exact Matrix.one_mulVec _

theorem rotate_inv_rotate {n : ℕ} (R : O n) (z : S n) :
    rotate R⁻¹ (rotate R z) = z := by
  rw [rotate_mul, inv_mul_cancel, rotate_one]

theorem first_column_iff_rotate_coordinate {n : ℕ} (j : Fin n) (R : O n) (z : S n) :
    R.val *ᵥ Pi.single j 1 = WithLp.ofLp z.val ↔
    rotate R (coordinatePoint j) = z := by
  constructor
  · intro h
    apply Subtype.ext
    apply (WithLp.equiv 2 (Fin n → ℝ)).injective
    change WithLp.ofLp (rotate R (coordinatePoint j)).val = WithLp.ofLp z.val
    rw [rotate_val]
    exact h
  · intro h
    change R.val *ᵥ WithLp.ofLp (coordinatePoint j).val = WithLp.ofLp z.val
    rw [← rotate_val, h]

noncomputable def assemble {n : ℕ} (Q : S (n + 2) → O (n + 2)) (u : S (n + 2))
    (z : S (n + 2)) (V : O (n + 1)) : O (n + 2) :=
  Q z * residualEmbed (n + 1) V * (Q u)⁻¹

theorem measurable_assemble {n : ℕ} {Q : S (n + 2) → O (n + 2)}
    (hQ : Measurable Q) (u : S (n + 2)) :
    Measurable (fun p : S (n + 2) × O (n + 1) => assemble Q u p.1 p.2) :=
  ((hQ.comp measurable_fst).mul
    ((continuous_residualEmbed (n + 1)).measurable.comp measurable_snd)).mul_const _

theorem assemble_rotate {n : ℕ} {Q : S (n + 2) → O (n + 2)}
    (hQ : ∀ z, rotate (Q z) (coordinatePoint 0) = z) (u z : S (n + 2)) (V : O (n + 1)) :
    rotate (assemble Q u z V) u = z := by
  have hV : rotate (residualEmbed (n + 1) V) (coordinatePoint 0) = coordinatePoint 0 :=
    (first_column_iff_rotate_coordinate 0 _ _).mp (residualEmbed_fixes V)
  have hu : rotate (Q u)⁻¹ u = coordinatePoint 0 := by
    simpa only [hQ u] using rotate_inv_rotate (Q u) (coordinatePoint 0)
  rw [assemble, ← rotate_mul, ← rotate_mul, hu, hV, hQ]

private theorem assemble_det {n : ℕ} {Q : S (n + 2) → O (n + 2)}
    (hQ : ∀ z, (Q z).val.det = 1) (u z : S (n + 2)) (V : O (n + 1)) :
    (assemble Q u z V).val.det = V.val.det := by
  change ((Q z).val * (residualEmbed (n + 1) V).val * ((Q u)⁻¹).val).det = _
  rw [Matrix.det_mul, Matrix.det_mul, det_inv, det_residualEmbed, hQ, hQ, one_mul, mul_one]

private noncomputable def cocycle {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (R : O (n + 2)) (z : S (n + 2)) : O (n + 2) :=
  (Q (rotate R z))⁻¹ * R * Q z

private theorem cocycle_fixes {n : ℕ} {Q : S (n + 2) → O (n + 2)}
    (hQ : ∀ z, rotate (Q z) (coordinatePoint 0) = z)
    (R : O (n + 2)) (z : S (n + 2)) :
    (cocycle Q R z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = Pi.single 0 1 := by
  apply (first_column_iff_rotate_coordinate 0 _ (coordinatePoint 0)).mpr
  rw [cocycle, ← rotate_mul, ← rotate_mul, hQ z]
  simpa only [hQ (rotate R z)] using
    rotate_inv_rotate (Q (rotate R z)) (coordinatePoint 0)

/-- The joint sphere and matrix law for any source-valid oriented completion. -/
theorem component_observation_joint_law_of_section (n : ℕ) (b : ℝ) (u : S (n + 2))
    (Q : S (n + 2) → O (n + 2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) :
    let target := ((sphereProbability (n + 2)).prod (componentHaar (n + 1) b)).map
      (fun p : S (n + 2) × O (n + 1) => (p.1, assemble Q u p.1 p.2))
    (componentHaar (n + 2) b).map (fun W => (rotate W u, W)) = target ∧
    (componentHaar (n + 2) b).map (fun W => (rotate W⁻¹ u, W⁻¹)) = target := by
  let : NeZero (n + 2) := ⟨by omega⟩
  let := isProbabilityMeasure_sphereProbability (n + 2)
  let σ := sphereProbability (n + 2)
  let F : S (n + 2) × O (n + 1) → O (n + 2) := fun p => assemble Q u p.1 p.2
  have hF : Measurable F := measurable_assemble hQ u
  have hQrot (z : S (n + 2)) : rotate (Q z) (coordinatePoint 0) = z :=
    (first_column_iff_rotate_coordinate 0 _ z).mp (hfirst z)
  let C (R : O (n + 2)) (z : S (n + 2)) : O (n + 1) :=
    ⟨lowerBlock (cocycle Q R z).val, lowerBlock_mem_orthogonal_of_fixes _ (cocycle_fixes hQrot R z)⟩
  have hc (R : O (n + 2)) : Measurable (C R) := by
    have hr := (measurePreserving_rotate (0 : Fin (n + 2)) R).measurable
    have hB : Measurable (cocycle Q R) :=
      (((hQ.comp hr).inv).mul_const R).mul hQ
    let Stab := {W : O (n + 2) | W.val *ᵥ
      Pi.single (0 : Fin (n + 2)) 1 = Pi.single 0 1}
    let split : Stab → O (n + 1) := fun W =>
      ⟨lowerBlock W.val.val, lowerBlock_mem_orthogonal_of_fixes W.val W.property⟩
    have hsplit : Continuous split := ((continuous_lowerBlock (n + 1)).comp
      (continuous_subtype_val.comp continuous_subtype_val)).subtype_mk _
    exact hsplit.measurable.comp (hB.subtype_mk
      (p := fun W => W.val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = Pi.single 0 1)
      (h := cocycle_fixes hQrot R))
  have hmul (R : O (n + 2)) (z : S (n + 2)) (V : O (n + 1)) :
      F (rotate R z, C R z * V) = R * F (z, V) := by
    have hC : residualEmbed (n + 1) (C R z) = cocycle Q R z :=
      residualEmbed_lowerBlock_of_fixes _ (cocycle_fixes hQrot R z)
    change Q (rotate R z) * residualEmbed (n + 1) (C R z * V) * (Q u)⁻¹ =
      R * (Q z * residualEmbed (n + 1) V * (Q u)⁻¹)
    rw [map_mul, hC, cocycle]
    group
  have hFfull : (σ.prod (orthogonalHaar (n + 1))).map F = orthogonalHaar (n + 2) :=
    map_prod_eq_haar_of_skew σ F hF rotate (measurePreserving_rotate 0) C hc hmul
  have hFb : (σ.prod (componentHaar (n + 1) b)).map F = componentHaar (n + 2) b :=
    map_prod_component σ F hF hFfull (fun p => by
      change (assemble Q u p.1 p.2).val.det = b ↔ p.2.val.det = b
      rw [assemble_det hdet])
  let observe : O (n + 2) → S (n + 2) × O (n + 2) := fun W => (rotate W u, W)
  have ho : Measurable observe := ((continuous_rotate.comp
    (continuous_id.prodMk continuous_const)).measurable).prodMk measurable_id
  have hpair :
      observe ∘ F = fun p => (p.1, F p) := by
    funext p
    exact Prod.ext (assemble_rotate hQrot u p.1 p.2) rfl
  have hforward : (componentHaar (n + 2) b).map observe =
      (σ.prod (componentHaar (n + 1) b)).map (fun p => (p.1, F p)) := by
    rw [← hFb, Measure.map_map ho hF, hpair]
  constructor
  · exact hforward
  · change (componentHaar (n + 2) b).map (observe ∘ Inv.inv) = _
    rw [← Measure.map_map ho measurable_inv, componentHaar_map_inv]
    exact hforward

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
