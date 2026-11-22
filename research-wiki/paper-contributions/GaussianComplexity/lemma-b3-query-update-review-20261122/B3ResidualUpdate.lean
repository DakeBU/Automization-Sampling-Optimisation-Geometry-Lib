import B2JointLaw
import Mathlib.Tactic.Group

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

set_option autoImplicit false

private noncomputable def frameResidual {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (u : S (n + 2)) (W : O (n + 2)) : O (n + 2) :=
  (Q (rotate W u))⁻¹ * W * Q u

private theorem frameResidual_fixes {n : ℕ} {Q : S (n + 2) → O (n + 2)}
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (u : S (n + 2)) (W : O (n + 2)) :
    (frameResidual Q u W).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = Pi.single 0 1 := by
  have hQ (z : S (n + 2)) : rotate (Q z) (coordinatePoint 0) = z :=
    (first_column_iff_rotate_coordinate 0 _ z).mp (hfirst z)
  apply (first_column_iff_rotate_coordinate 0 _ (coordinatePoint 0)).mpr
  rw [frameResidual, ← rotate_mul, ← rotate_mul, hQ u]
  simpa only [hQ (rotate W u)] using rotate_inv_rotate (Q (rotate W u)) (coordinatePoint 0)

/-- Extract the lower orthogonal block after using the actual observation
to choose the range frame and the query direction to choose the domain frame. -/
noncomputable def extractResidual {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (u : S (n + 2)) (W : O (n + 2)) : O (n + 1) :=
  ⟨lowerBlock (frameResidual Q u W).val,
    lowerBlock_mem_orthogonal_of_fixes _ (frameResidual_fixes hfirst u W)⟩

set_option backward.isDefEq.respectTransparency false in
set_option maxHeartbeats 850000 in
/-- Extraction is Borel jointly in the direction and the original orthogonal draw. -/
theorem measurable_extractResidual {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val) :
    Measurable (fun p : S (n + 2) × O (n + 2) => extractResidual Q hfirst p.1 p.2) := by
  have hSw : Continuous (Prod.swap : S (n + 2) × O (n + 2) → O (n + 2) × S (n + 2)) :=
    continuous_swap
  have hRot : Continuous (fun p : O (n + 2) × S (n + 2) => rotate p.1 p.2) :=
    continuous_rotate
  have hObs : Measurable (fun p : S (n + 2) × O (n + 2) => rotate p.2 p.1) := by
    change Measurable ((fun p : O (n + 2) × S (n + 2) => rotate p.1 p.2) ∘ Prod.swap)
    exact (hRot.comp hSw).measurable
  have hFrame : Measurable (fun p : S (n + 2) × O (n + 2) => frameResidual Q p.1 p.2) :=
    (((hQ.comp hObs).inv).mul measurable_snd).mul (hQ.comp measurable_fst)
  let Stab := {R : O (n + 2) | R.val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = Pi.single 0 1}
  let split : Stab → O (n + 1) := fun R =>
    ⟨lowerBlock R.val.val, lowerBlock_mem_orthogonal_of_fixes R.val R.property⟩
  have hSplit : Continuous split := ((continuous_lowerBlock (n + 1)).comp
    (continuous_subtype_val.comp continuous_subtype_val)).subtype_mk _
  exact hSplit.measurable.comp (hFrame.subtype_mk
    (p := fun R => R.val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = Pi.single 0 1)
    (h := fun p => frameResidual_fixes hfirst p.1 p.2))

theorem residualEmbed_extractResidual {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (u : S (n + 2)) (W : O (n + 2)) :
    residualEmbed (n + 1) (extractResidual Q hfirst u W) =
      (Q (rotate W u))⁻¹ * W * Q u :=
  residualEmbed_lowerBlock_of_fixes _ (frameResidual_fixes hfirst u W)

theorem residualEmbed_extractResidual_inverse {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (u : S (n + 2)) (W : O (n + 2)) :
    residualEmbed (n + 1) (extractResidual Q hfirst u W⁻¹)⁻¹ =
      (Q u)⁻¹ * W * Q (rotate W⁻¹ u) := by
  rw [map_inv, residualEmbed_extractResidual]
  simp only [_root_.mul_inv_rev, inv_inv, mul_assoc]

private theorem extractResidual_assemble {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (u z : S (n + 2)) (V : O (n + 1)) :
    extractResidual Q hfirst u (assemble Q u z V) = V := by
  have hQ (z : S (n + 2)) : rotate (Q z) (coordinatePoint 0) = z :=
    (first_column_iff_rotate_coordinate 0 _ z).mp (hfirst z)
  have hFrame : frameResidual Q u (assemble Q u z V) = residualEmbed (n + 1) V := by
    rw [frameResidual, assemble_rotate hQ, assemble]
    group
  apply Subtype.ext
  change lowerBlock (frameResidual Q u (assemble Q u z V)).val = V.val
  rw [hFrame, lowerBlock_residualEmbed]

set_option backward.isDefEq.respectTransparency false in
set_option maxHeartbeats 850000 in
/-- The updated selected block and its newly exposed unit direction are
independent, with laws given by the sphere and the smaller same-sign Haar
component. The inverse update uses the transpose of the extracted block. -/
theorem selected_block_residual_update_joint_law (n : ℕ) (b : ℝ) (hb : b = -1 ∨ b = 1)
    (u : S (n + 2)) (Q : S (n + 2) → O (n + 2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) :
    let μ := componentHaar (n + 2) b
    let target := (sphereProbability (n + 2)).prod (componentHaar (n + 1) b)
    μ.map (fun W => (rotate W u, extractResidual Q hfirst u W)) = target ∧
    μ.map (fun W => (rotate W⁻¹ u, (extractResidual Q hfirst u W⁻¹)⁻¹)) = target := by
  let : NeZero (n + 2) := ⟨by omega⟩
  let σ := sphereProbability (n + 2)
  let ν := componentHaar (n + 1) b
  let μ := componentHaar (n + 2) b
  let := isProbabilityMeasure_sphereProbability (n + 2)
  let := isProbabilityMeasure_componentHaar (n := n + 1) (by omega) hb
  let F : S (n + 2) × O (n + 1) → S (n + 2) × O (n + 2) :=
    fun p => (p.1, assemble Q u p.1 p.2)
  let read : S (n + 2) × O (n + 2) → S (n + 2) × O (n + 1) :=
    fun p => (p.1, extractResidual Q hfirst u p.2)
  let transposeResidual : S (n + 2) × O (n + 1) → S (n + 2) × O (n + 1) :=
    Prod.map id Inv.inv
  have hF : Measurable F :=
    measurable_fst.prodMk (measurable_assemble hQ u)
  have hExtractJoint : Measurable (Function.uncurry (extractResidual Q hfirst)) :=
    measurable_extractResidual Q hQ hfirst
  have hExtract : Measurable (extractResidual Q hfirst u) := hExtractJoint.of_uncurry_left
  have hRead : Measurable read :=
    measurable_fst.prodMk (hExtract.comp measurable_snd)
  have hTranspose : Measurable transposeResidual :=
    measurable_id.prodMap measurable_inv
  have hForward : Measurable (fun W : O (n + 2) => (rotate W u, W)) :=
    (continuous_rotate.measurable.comp (measurable_id.prodMk measurable_const)).prodMk measurable_id
  have hInverse : Measurable (fun W : O (n + 2) => (rotate W⁻¹ u, W⁻¹)) :=
    hForward.comp measurable_inv
  have hReadF : read ∘ F = id := by
    funext p
    exact Prod.ext rfl (extractResidual_assemble Q hfirst u p.1 p.2)
  have hTransposeLaw : (σ.prod ν).map transposeResidual = σ.prod ν := by
    change (σ.prod ν).map (Prod.map id Inv.inv) = σ.prod ν
    rw [← Measure.map_prod_map σ ν measurable_id measurable_inv, Measure.map_id,
      componentHaar_map_inv]
  obtain ⟨hFwd, hInv⟩ := component_observation_joint_law_of_section n b u Q hQ hfirst hdet
  change (μ.map (fun W => (rotate W u, W)) = (σ.prod ν).map F) at hFwd
  change (μ.map (fun W => (rotate W⁻¹ u, W⁻¹)) = (σ.prod ν).map F) at hInv
  constructor
  · change μ.map (read ∘ fun W => (rotate W u, W)) = σ.prod ν
    rw [← Measure.map_map hRead hForward, hFwd, Measure.map_map hRead hF,
      hReadF, Measure.map_id]
  · change μ.map (transposeResidual ∘ read ∘ fun W => (rotate W⁻¹ u, W⁻¹)) = σ.prod ν
    rw [← Measure.map_map hTranspose (hRead.comp hInverse),
      ← Measure.map_map hRead hInverse, hInv, Measure.map_map hRead hF,
      hReadF, Measure.map_id, hTransposeLaw]

#print axioms selected_block_residual_update_joint_law
#print axioms residualEmbed_extractResidual_inverse

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
