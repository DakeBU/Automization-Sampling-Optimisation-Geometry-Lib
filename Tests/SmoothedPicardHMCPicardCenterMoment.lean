import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardCenterMoment

open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC
open PicardCenterMoment InnerProductSpace MeasureTheory ProbabilityTheory
open scoped NNReal

#check picard_center_gradient_moment
#print axioms picard_center_gradient_moment

-- A genuine two-node execution at eta > 1/2.  The zero-dimensional model makes
-- every phase-state and Gaussian moment exact while still exercising the actual
-- stopped proximal interpreter and both finite Picard layers.
example : ∃ N : EuclideanSpace ℝ (Fin 0) → ℕ,
    ApproximateProximalExecution.proximalQuery
      (gradient (fun _ : EuclideanSpace ℝ (Fin 0) => (0 : ℝ))) (3 / 4) (1 / 10)
      0 (N 0 + 1) 0 = some (0, N 0 + 1) := by
  let E := EuclideanSpace ℝ (Fin 0)
  let _ : MeasurableSpace E := borel E
  have hH : ∀ x v : E,
      ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖ ^ 2 ≤
        (fderiv ℝ (fderiv ℝ (fun _ : E => (0 : ℝ))) x v) v ∧
      (fderiv ℝ (fderiv ℝ (fun _ : E => (0 : ℝ))) x v) v ≤ ‖v‖ ^ 2 := by
    intro x v
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  obtain ⟨p, N, q, hp, hN, hq, heq, hrun, h0, hz, h1⟩ :=
    picard_center_gradient_moment
      (E := E) (Ω := Unit) (ι := Fin 2)
      (V := fun _ : E => (0 : ℝ)) (κ := 1) (by norm_num) contDiff_const hH
      (eta := 3 / 4) (c := 7 / 8) (eps := 1 / 10)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      (Measure.dirac ()) (fun _ => 0) (fun _ => 0) (by fun_prop) (by fun_prop)
      0 (by simp) (fun _ => 1) (by simp) (fun _ _ => 0) (by simp)
      (fun _ _ => 1) (M := 0) (S := 2) (by norm_num) (by norm_num)
      (by simp) (by simp) (by intro; simp) (by intro; simp) (by intro; norm_num)
  have hfirstLayer := h0 (0 : Fin 2)
  have hqueryLayer := hz (0 : Fin 2)
  have hsecondLayer := h1 (0 : Fin 2)
  have _ := hfirstLayer.2
  have _ := hqueryLayer.2
  have _ := hsecondLayer.1
  have _ := hsecondLayer.2
  refine ⟨N, ?_⟩
  have hh := (hrun (0 : E)).2
  simpa only [Subsingleton.elim (q 0) 0] using hh
