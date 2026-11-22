import B3ProductStep
import B3ResidualUpdate

/-!
Zhou–Suzuki, *On Complexity of Gaussian Sampling*, Appendix B, Lemma B.3.
At a fixed history with a nonzero residual query, expose one unit response
and update the residual tuple on the original block labels. Only the selected
dimension decreases. Both query polarities admit the same new product law.
-/

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 900000
set_option synthInstance.maxHeartbeats 180000

/-- Identify orthogonal matrices across an equality of dimensions. -/
def castOrthogonal {m m' : ℕ} (h : m = m') (W : O m) : O m' := h ▸ W

private theorem measurePreserving_castOrthogonal {m m' : ℕ} (h : m = m') (b : ℝ) :
    MeasurePreserving (castOrthogonal h) (componentHaar m b) (componentHaar m' b) := by
  cases h
  exact MeasurePreserving.id _

private theorem measurable_castOrthogonal {m m' : ℕ} (h : m = m') :
    Measurable (castOrthogonal h) := (measurePreserving_castOrthogonal h 1).measurable

/-- A forward query observes the image of the unit direction. A transpose
query uses the inverse matrix and returns the transpose of its extracted block. -/
noncomputable def selectedHaarStep {n : ℕ} (Q : S (n + 2) → O (n + 2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (transpose : Bool) (u : S (n + 2)) (W : O (n + 2)) : S (n + 2) × O (n + 1) :=
  if transpose then (rotate W⁻¹ u, (extractResidual Q hfirst u W⁻¹)⁻¹)
  else (rotate W u, extractResidual Q hfirst u W)

theorem measurable_selectedHaarStep {n : ℕ} (Q : S (n + 2) → O (n + 2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (transpose : Bool) :
    Measurable (fun p : S (n + 2) × O (n + 2) => selectedHaarStep Q hfirst transpose p.1 p.2) := by
  have hrot := (continuous_rotate (n := n + 2)).measurable
  have hext := measurable_extractResidual Q hQ hfirst
  cases transpose
  · exact (hrot.comp (measurable_snd.prodMk measurable_fst)).prodMk hext
  · exact (hrot.comp (measurable_snd.inv.prodMk measurable_fst)).prodMk
      ((hext.comp (measurable_fst.prodMk measurable_snd.inv)).inv)

private theorem finite_componentHaar (m : ℕ) (b : ℝ) : IsFiniteMeasure (componentHaar m b) := by
  let := (AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar.orthogonalHaar_spec m).1
  unfold componentHaar
  exact Measure.smul_finite _ (by norm_num)

private theorem measurePreserving_selectedHaarStep {n : ℕ} (b : ℝ) (hb : b = -1 ∨ b = 1)
    (Q : S (n + 2) → O (n + 2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) (transpose : Bool) (u : S (n + 2)) :
    MeasurePreserving (selectedHaarStep Q hfirst transpose u)
      (componentHaar (n + 2) b) ((sphereProbability (n + 2)).prod (componentHaar (n + 1) b)) := by
  constructor
  · exact Measurable.of_uncurry_left (f := selectedHaarStep Q hfirst transpose)
      (measurable_selectedHaarStep Q hQ hfirst transpose)
  · have laws := selected_block_residual_update_joint_law n b hb u Q hQ hfirst hdet
    cases transpose
    · rw [show selectedHaarStep Q hfirst false u =
          fun W => (rotate W u, extractResidual Q hfirst u W) by funext W; rfl]
      exact laws.1
    · rw [show selectedHaarStep Q hfirst true u =
          fun W => (rotate W⁻¹ u, (extractResidual Q hfirst u W⁻¹)⁻¹) by funext W; rfl]
      exact laws.2

variable {k : ℕ}

/-- The updated tuple has the original block labels. The selected index now
has dimension `n+1`. The other matrix entries only undergo type transport. -/
noncomputable def updateHaarTuple (dim : Fin (k + 1) → ℕ) (i : Fin (k + 1))
    (n : ℕ) (hi : dim i = n + 2) (Q : S (n + 2) → O (n + 2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (transpose : Bool) (u : S (n + 2)) (W : ∀ j, O (dim j)) :
    S (n + 2) × (∀ j, O ((Function.update dim i (n + 1)) j)) :=
  let step := selectedHaarStep Q hfirst transpose u (castOrthogonal hi (W i))
  (step.1, i.insertNth (α := fun j => O ((Function.update dim i (n + 1)) j))
    (castOrthogonal (by simp) step.2)
    (fun l => castOrthogonal (by simp [Fin.succAbove_ne]) (W (i.succAbove l))))

theorem measurable_updateHaarTuple (dim : Fin (k + 1) → ℕ) (i : Fin (k + 1))
    (n : ℕ) (hi : dim i = n + 2) (Q : S (n + 2) → O (n + 2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (transpose : Bool) :
    Measurable (fun p : S (n + 2) × (∀ j, O (dim j)) =>
      updateHaarTuple dim i n hi Q hfirst transpose p.1 p.2) := by
  have hread (j : Fin (k + 1)) : Measurable (fun p : S (n + 2) × (∀ l, O (dim l)) => p.2 j) :=
    (measurable_pi_apply j).comp measurable_snd
  have hsel := (measurable_selectedHaarStep Q hQ hfirst transpose).comp
    (measurable_fst.prodMk ((measurable_castOrthogonal hi).comp (hread i)))
  refine hsel.fst.prodMk (measurable_pi_iff.mpr (i.forall_iff_succAbove.mpr ⟨?_, ?_⟩))
  · simpa only [updateHaarTuple, Fin.insertNth_apply_same, Function.comp_def] using
      (measurable_castOrthogonal (show n + 1 = (Function.update dim i (n + 1)) i by simp)).comp
        hsel.snd
  · intro l
    simpa only [updateHaarTuple, Fin.insertNth_apply_succAbove, Function.comp_def] using
      (measurable_castOrthogonal (show dim (i.succAbove l) =
          (Function.update dim i (n + 1)) (i.succAbove l) by simp [Fin.succAbove_ne])).comp
        (hread (i.succAbove l))

/-- The observed direction is independent of the entire new residual tuple.
Its law is spherical for either orientation of the selected query. -/
theorem query_selected_haar_product (dim : Fin (k + 1) → ℕ) (i : Fin (k + 1))
    (n : ℕ) (hi : dim i = n + 2) (b : ℝ) (hb : b = -1 ∨ b = 1)
    (Q : S (n + 2) → O (n + 2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n + 2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) (transpose : Bool) (u : S (n + 2)) :
    MeasurePreserving (updateHaarTuple dim i n hi Q hfirst transpose u)
      (Measure.pi fun j => componentHaar (dim j) b)
      ((sphereProbability (n + 2)).prod
        (Measure.pi fun j => componentHaar ((Function.update dim i (n + 1)) j) b)) := by
  let newDim := Function.update dim i (n + 1)
  let := isProbabilityMeasure_sphereProbability (n + 2)
  let : ∀ j, IsFiniteMeasure (componentHaar (dim j) b) := fun j => finite_componentHaar _ _
  let : ∀ j, IsFiniteMeasure (componentHaar (newDim j) b) := fun j => finite_componentHaar _ _
  let := finite_componentHaar (n + 1) b
  have hstep := measurePreserving_selectedHaarStep b hb Q hQ hfirst hdet transpose u
  have hi' : n + 1 = newDim i := by simp [newDim]
  have hselected := ((MeasurePreserving.id (sphereProbability (n + 2))).prod
    (measurePreserving_castOrthogonal hi' b)).comp
      (hstep.comp (measurePreserving_castOrthogonal hi b))
  have hoff (l : Fin k) : dim (i.succAbove l) = newDim (i.succAbove l) := by
    simp [newDim, Fin.succAbove_ne]
  exact replace_selected_coordinate (fun j => componentHaar (dim j) b)
    (fun j => componentHaar (newDim j) b) i (sphereProbability (n + 2)) hselected
    (fun l => measurePreserving_castOrthogonal (hoff l) b)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
