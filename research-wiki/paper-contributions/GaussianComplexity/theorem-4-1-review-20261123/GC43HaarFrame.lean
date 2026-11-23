import B4Frames
import B3HaarProduct

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

theorem haar_as_components (m : ℕ) :
    orthogonalHaar m = (2 : ℝ≥0∞)⁻¹ • (componentHaar m 1 + componentHaar m (-1)) := by
  have hc : (detFiber m 1)ᶜ = detFiber m (-1) := by
    ext W
    change (¬ W.val.det = 1) ↔ W.val.det = -1
    have h := congrArg Matrix.det ((Matrix.mem_orthogonalGroup_iff (Fin m) ℝ).mp W.property)
    rw [Matrix.det_mul, Matrix.det_transpose, Matrix.det_one] at h
    rcases mul_self_eq_one_iff.mp h with hp | hm <;> norm_num [*]
  rw [componentHaar, componentHaar, ← smul_add, smul_smul,
    ENNReal.inv_mul_cancel (by norm_num) (by norm_num), one_smul, ← hc,
    Measure.restrict_add_restrict_compl (measurableSet_detFiber m 1)]

/-- The query image (or preimage) and the unrevealed matrix have the product
of uniform direction and full residual Haar laws. -/
theorem full_haar_step_law {n : ℕ} (Q : S (n+2) → O (n+2)) (hQ : Measurable Q)
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (hdet : ∀ z, (Q z).val.det = 1) (back : Bool) (u : S (n+2)) :
    (orthogonalHaar (n+2)).map (selectedHaarStep Q hfirst back u) =
      (sphereProbability (n+2)).prod (orthogonalHaar (n+1)) := by
  have m := Measurable.of_uncurry_left (f := selectedHaarStep Q hfirst back)
    (measurable_selectedHaarStep Q hQ hfirst back) (x := u)
  have h (b : ℝ) (hb : b = -1 ∨ b = 1) :
      (componentHaar (n+2) b).map (selectedHaarStep Q hfirst back u) =
        (sphereProbability (n+2)).prod (componentHaar (n+1) b) := by
    have t := selected_block_residual_update_joint_law n b hb u Q hQ hfirst hdet
    cases back
    · exact t.1
    · exact t.2
  let := isProbabilityMeasure_sphereProbability (n+2)
  let := isProbabilityMeasure_componentHaar (Nat.succ_pos n) (Or.inr (rfl : (1:ℝ)=1))
  let := isProbabilityMeasure_componentHaar (Nat.succ_pos n) (Or.inl (rfl : (-1:ℝ)= -1))
  rw [haar_as_components (n+2), Measure.map_smul, Measure.map_add _ _ m, h 1 (Or.inr rfl),
    h (-1) (Or.inl rfl), haar_as_components (n+1), Measure.prod_smul_right, Measure.prod_add]

#print axioms full_haar_step_law
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
