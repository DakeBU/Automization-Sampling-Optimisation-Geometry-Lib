import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz

#check AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz.proximal_estimator_lipschitz
#print axioms AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz.proximal_estimator_lipschitz

open InnerProductSpace
open scoped NNReal

-- Exercise the actual constructor at both the zero-dimensional and eta=1/2 boundaries.
example : ∃ p : EuclideanSpace ℝ (Fin 0) → EuclideanSpace ℝ (Fin 0),
    LipschitzWith 1 p ∧ ∀ y, p y = y := by
  have hH : ∀ x v : EuclideanSpace ℝ (Fin 0),
      ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖ ^ 2 ≤
        (fderiv ℝ (fderiv ℝ (fun _ : EuclideanSpace ℝ (Fin 0) => (0 : ℝ))) x v) v ∧
      (fderiv ℝ (fderiv ℝ (fun _ : EuclideanSpace ℝ (Fin 0) => (0 : ℝ))) x v) v ≤ ‖v‖ ^ 2 := by
    intro x v
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  obtain ⟨p, _, _, _, hpLip, _, _⟩ :=
    AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz.proximal_estimator_lipschitz
      (V := fun _ : EuclideanSpace ℝ (Fin 0) => (0 : ℝ)) (κ := 1) (by norm_num)
      contDiff_const hH (eta := 1 / 2) (by norm_num) (by norm_num)
  exact ⟨p, hpLip, fun _ => Subsingleton.elim _ _⟩
