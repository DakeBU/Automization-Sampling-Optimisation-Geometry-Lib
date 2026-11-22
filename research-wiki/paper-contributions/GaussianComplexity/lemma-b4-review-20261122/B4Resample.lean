import B3HaarProduct

/-!
# Rebuild a tuple from one spherical response and its smaller Haar blocks

This is the resampling operation in the finite-horizon proof of Zhou–Suzuki,
Lemma B.4. The selected matrix is assembled from the unit vectors and the
smaller matrix. For a transpose query the smaller block and assembled matrix
are both transposed. Every unqueried label keeps its original value.
-/

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 800000
set_option synthInstance.maxHeartbeats 120000

private theorem cast_cancel {a b : ℕ} (h : a = b) (g : b = a) (w : O a) :
    castOrthogonal g (castOrthogonal h w) = w := by subst b; rfl

private theorem measurable_dim_cast {a b : ℕ} (h : a = b) : Measurable (castOrthogonal h) := by
  subst b; exact measurable_id

/-- Reconstruct the selected old matrix from the observed direction and the
new residual in the original domain/range orientation. -/
noncomputable def rebuildSelected {n : ℕ} (Q : S (n+2) → O (n+2)) (back : Bool)
    (u z : S (n+2)) (V : O (n+1)) : O (n+2) :=
  if back then (assemble Q u z V⁻¹)⁻¹ else assemble Q u z V

theorem measurable_rebuildSelected {n : ℕ} (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (back : Bool) (u : S (n+2)) :
    Measurable (fun p : S (n+2) × O (n+1) => rebuildSelected Q back u p.1 p.2) := by
  cases back
  · exact measurable_assemble hQ u
  · exact ((measurable_assemble hQ u).comp (measurable_fst.prodMk measurable_snd.inv)).inv

private theorem assemble_read {n : ℕ} (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (u : S (n+2)) (W : O (n+2)) :
    assemble Q u (rotate W u) (extractResidual Q hc u W) = W := by
  rw [assemble, residualEmbed_extractResidual]
  group

private theorem read_assemble {n : ℕ} (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (u z : S (n+2)) (V : O (n+1)) :
    selectedHaarStep Q hc false u (assemble Q u z V) = (z,V) := by
  have hc' (s : S (n+2)) : rotate (Q s) (coordinatePoint 0) = s :=
    (first_column_iff_rotate_coordinate 0 _ _).mp (hc s)
  have hz := assemble_rotate hc' u z V
  apply Prod.ext hz
  have he := residualEmbed_extractResidual Q hc u (assemble Q u z V)
  rw [hz] at he
  have hblock : residualEmbed (n+1) (extractResidual Q hc u (assemble Q u z V)) =
      residualEmbed (n+1) V := he.trans (by rw [assemble]; group)
  change extractResidual Q hc u (assemble Q u z V) = V
  apply Subtype.ext
  simpa only [lowerBlock_residualEmbed] using congrArg (fun A : O (n+2) => lowerBlock A.val) hblock

theorem rebuildSelected_update {n : ℕ} (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (u : S (n+2)) (W : O (n+2)) :
    let p := selectedHaarStep Q hc back u W
    rebuildSelected Q back u p.1 p.2 = W := by
  cases back
  · exact assemble_read Q hc u W
  · simp only [selectedHaarStep, rebuildSelected, if_true, inv_inv, assemble_read]

theorem update_rebuildSelected {n : ℕ} (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (u z : S (n+2)) (V : O (n+1)) :
    selectedHaarStep Q hc back u (rebuildSelected Q back u z V) = (z,V) := by
  cases back
  · exact read_assemble Q hc u z V
  · obtain ⟨hz, hv⟩ := Prod.ext_iff.mp (read_assemble Q hc u z V⁻¹)
    change rotate (assemble Q u z V⁻¹) u = z at hz
    change extractResidual Q hc u (assemble Q u z V⁻¹) = V⁻¹ at hv
    simp only [rebuildSelected, selectedHaarStep, if_true, inv_inv, hz, hv]

variable {k : ℕ} (d : Fin (k+1) → ℕ) (i : Fin (k+1)) (n : ℕ) (hi : d i = n+2)

/-- Dimensions after an informative query at index i. -/
abbrev resampleDim := Function.update d i (n+1)

/-- Reinsert the assembled matrix at its original index and transport the
other matrices only across the equality of their dimensions. -/
noncomputable def rebuildHaarTuple (Q : S (n+2) → O (n+2)) (back : Bool) (u z : S (n+2))
    (V : ∀ j, O (resampleDim d i n j)) (j : Fin (k+1)) : O (d j) :=
  if hj : j = i then
    castOrthogonal ((congrArg d hj).trans hi).symm
      (rebuildSelected Q back u z (castOrthogonal (Function.update_self i (n+1) d) (V i)))
  else castOrthogonal (Function.update_of_ne hj (n+1) d) (V j)

theorem rebuildHaarTuple_selected (Q : S (n+2) → O (n+2)) (back : Bool) (u z : S (n+2))
    (V : ∀ j, O (resampleDim d i n j)) :
    castOrthogonal hi (rebuildHaarTuple d i n hi Q back u z V i) =
      rebuildSelected Q back u z (castOrthogonal (Function.update_self i (n+1) d) (V i)) := by
  rw [rebuildHaarTuple, dif_pos rfl, cast_cancel]

theorem rebuildHaarTuple_other (Q : S (n+2) → O (n+2)) (back : Bool) (u z : S (n+2))
    (V : ∀ j, O (resampleDim d i n j)) (j : Fin (k+1)) (hj : j ≠ i) :
    rebuildHaarTuple d i n hi Q back u z V j =
      castOrthogonal (Function.update_of_ne hj (n+1) d) (V j) := dif_neg hj

theorem measurable_rebuildHaarTuple (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (back : Bool) (u : S (n+2)) :
    Measurable (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
      rebuildHaarTuple d i n hi Q back u p.1 p.2) := by
  have hsel : Measurable (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
      rebuildSelected Q back u p.1 (castOrthogonal (Function.update_self i (n+1) d) (p.2 i))) := by
    have hVi : Measurable (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) => p.2 i) :=
      (measurable_pi_apply i).comp measurable_snd
    let select := fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
      (p.1, castOrthogonal (Function.update_self i (n+1) d) (p.2 i))
    have hsmall : Measurable (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
        castOrthogonal (Function.update_self i (n+1) d) (p.2 i)) :=
      (measurable_dim_cast (Function.update_self i (n+1) d)).comp hVi
    have hselect : Measurable select := measurable_fst.prodMk hsmall
    change Measurable ((fun p : S (n+2) × O (n+1) => rebuildSelected Q back u p.1 p.2) ∘ select)
    exact Measurable.comp (measurable_rebuildSelected Q hQ back u) hselect
  refine measurable_pi_iff.mpr ?_
  intro j
  by_cases h : j = i
  · subst j
    have heq : (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
      rebuildHaarTuple d i n hi Q back u p.1 p.2 i) =
        fun p => castOrthogonal hi.symm (rebuildSelected Q back u p.1
          (castOrthogonal (Function.update_self i (n+1) d) (p.2 i))) :=
      funext fun _ => dif_pos rfl
    rw [heq]
    exact (measurable_dim_cast hi.symm).comp hsel
  · have heq : (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
      rebuildHaarTuple d i n hi Q back u p.1 p.2 j) =
        fun p => castOrthogonal (Function.update_of_ne h (n+1) d) (p.2 j) :=
      funext fun p => rebuildHaarTuple_other d i n hi Q back u p.1 p.2 j h
    rw [heq]
    have hVj : Measurable (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) => p.2 j) :=
      (measurable_pi_apply j).comp measurable_snd
    exact (measurable_dim_cast (Function.update_of_ne h (n+1) d)).comp hVj

private theorem cast_injective {a b : ℕ} (h : a = b) : Function.Injective (castOrthogonal h) := by
  subst b; exact Function.injective_id

theorem updateHaarTuple_selected (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (u : S (n+2)) (W : ∀ j, O (d j)) :
    let p := updateHaarTuple d i n hi Q hc back u W
    (p.1, castOrthogonal (Function.update_self i (n+1) d) (p.2 i)) =
      selectedHaarStep Q hc back u (castOrthogonal hi (W i)) := by
  simp only [updateHaarTuple, Fin.insertNth_apply_same, cast_cancel, Prod.mk.eta]

theorem updateHaarTuple_other (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (u : S (n+2)) (W : ∀ j, O (d j)) (j : Fin (k+1)) (hj : j ≠ i) :
    (updateHaarTuple d i n hi Q hc back u W).2 j =
      castOrthogonal (Function.update_of_ne hj (n+1) d).symm (W j) := by
  obtain ⟨l, rfl⟩ := Fin.exists_succAbove_eq hj
  simp only [updateHaarTuple, Fin.insertNth_apply_succAbove]

theorem rebuildHaarTuple_update (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (u : S (n+2)) (W : ∀ j, O (d j)) :
    let p := updateHaarTuple d i n hi Q hc back u W
    rebuildHaarTuple d i n hi Q back u p.1 p.2 = W := by
  funext j
  by_cases hj : j = i
  · subst j
    apply cast_injective hi
    rw [rebuildHaarTuple_selected]
    exact (congrArg (fun p : S (n+2) × O (n+1) => rebuildSelected Q back u p.1 p.2)
      (updateHaarTuple_selected d i n hi Q hc back u W)).trans (rebuildSelected_update Q hc back u _)
  · rw [rebuildHaarTuple_other d i n hi Q back u _ _ j hj,
      updateHaarTuple_other d i n hi Q hc back u _ j hj, cast_cancel]

theorem update_rebuildHaarTuple (Q : S (n+2) → O (n+2))
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (u z : S (n+2)) (V : ∀ j, O (resampleDim d i n j)) :
    updateHaarTuple d i n hi Q hc back u (rebuildHaarTuple d i n hi Q back u z V) = (z,V) := by
  let W := rebuildHaarTuple d i n hi Q back u z V
  have hs := updateHaarTuple_selected d i n hi Q hc back u W
  have hs' : selectedHaarStep Q hc back u (castOrthogonal hi (W i)) =
      (z, castOrthogonal (Function.update_self i (n+1) d) (V i)) := by
    rw [show castOrthogonal hi (W i) = _ from rebuildHaarTuple_selected d i n hi Q back u z V,
      update_rebuildSelected]
  have heq := hs.trans hs'
  apply Prod.ext
  · exact congrArg (fun p : S (n+2) × O (n+1) => p.1) heq
  funext j
  by_cases hj : j = i
  · subst j
    exact cast_injective (Function.update_self i (n+1) d) (congrArg Prod.snd heq)
  · rw [updateHaarTuple_other d i n hi Q hc back u _ j hj,
      rebuildHaarTuple_other d i n hi Q back u z V j hj, cast_cancel]

/-- Sphere noise and the smaller independent same-sign residuals reconstruct
the old independent component Haar tuple. -/
theorem measurePreserving_rebuildHaarTuple (b : ℝ) (hb : b = -1 ∨ b = 1)
    (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (hc : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) (back : Bool) (u : S (n+2)) :
    MeasurePreserving (fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
      rebuildHaarTuple d i n hi Q back u p.1 p.2)
      ((sphereProbability (n+2)).prod (Measure.pi fun j => componentHaar (resampleDim d i n j) b))
      (Measure.pi fun j => componentHaar (d j) b) := by
  let read := updateHaarTuple d i n hi Q hc back u
  let rebuild := fun p : S (n+2) × (∀ j, O (resampleDim d i n j)) =>
    rebuildHaarTuple d i n hi Q back u p.1 p.2
  have hm : Measurable rebuild := measurable_rebuildHaarTuple d i n hi Q hQ back u
  have hr := query_selected_haar_product d i n hi b hb Q hQ hc hdet back u
  have hcomp : rebuild ∘ read = id := funext (rebuildHaarTuple_update d i n hi Q hc back u)
  constructor
  · exact hm
  · change Measure.map rebuild _ = _
    rw [← hr.map_eq, Measure.map_map hm hr.measurable]
    change Measure.map (rebuild ∘ read) _ = _
    rw [hcomp, Measure.map_id]

#print axioms update_rebuildHaarTuple
#print axioms measurePreserving_rebuildHaarTuple

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
