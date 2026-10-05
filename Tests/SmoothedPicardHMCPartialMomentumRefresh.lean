import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardInputLaw
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardCenterMoment

open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC
open PartialMomentumRefresh PicardInputLaw PicardCenterMoment InnerProductSpace MeasureTheory
  ProbabilityTheory
open scoped NNReal

#check AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian
#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian
#check partial_momentum_refresh_second_moment
#print axioms partial_momentum_refresh_second_moment
#check partial_refresh_with_picard_innovations
#print axioms partial_refresh_with_picard_innovations

-- A positive-dimensional check prevents the product-law theorem from being
-- exercised only in the degenerate zero-dimensional consumer below.
example :
    let ν : Measure (ℝ × ℝ) := Measure.dirac (0, 0)
    let μ := (ν.prod (stdGaussian ℝ)).prod
      (Measure.pi (fun _ : Fin 2 => stdGaussian ℝ))
    (∫ w : ((ℝ × ℝ) × ℝ) × (Fin 2 → ℝ), ‖w.2 (0 : Fin 2)‖ ^ 2 ∂μ) = 1 := by
  dsimp only
  let ν : Measure (ℝ × ℝ) := Measure.dirac (0, 0)
  have hinputI : Integrable
      (fun s : ℝ × ℝ => ‖s.1 - (0 : ℝ)‖ ^ 2 + ‖s.2‖ ^ 2) ν := by
    exact integrable_dirac (by simp)
  have hinput : (∫ s : ℝ × ℝ, ‖s.1 - (0 : ℝ)‖ ^ 2 + ‖s.2‖ ^ 2 ∂ν) ≤ 0 := by
    simp [ν]
  have href := partial_refresh_with_picard_innovations
    (E := ℝ) (ι := Fin 2) ν 0 (h := 1) (M := 0)
      (by norm_num) (by norm_num) hinputI hinput
  dsimp only at href
  exact (href.2.2.2.2.2.2.2 (0 : Fin 2)).trans (by simp)

-- The refreshed product-law state is passed to the actual two-layer Picard
-- theorem.  This exercises the intended consumer rather than merely checking
-- the OU identity in isolation.
example : ∃ N : EuclideanSpace ℝ (Fin 0) → ℕ,
    ApproximateProximalExecution.proximalQuery
      (gradient (fun _ : EuclideanSpace ℝ (Fin 0) => (0 : ℝ))) (3 / 4) (1 / 10)
      0 (N 0 + 1) 0 = some (0, N 0 + 1) := by
  let E := EuclideanSpace ℝ (Fin 0)
  let _ : MeasurableSpace E := borel E
  let ν : Measure (E × E) := Measure.dirac (0, 0)
  have hinputI : Integrable (fun s : E × E => ‖s.1 - (0 : E)‖ ^ 2 + ‖s.2‖ ^ 2) ν := by
    simp [ν]
  have hinput : (∫ s : E × E, ‖s.1 - (0 : E)‖ ^ 2 + ‖s.2‖ ^ 2 ∂ν) ≤ 0 := by
    simp [ν]
  have href := partial_refresh_with_picard_innovations
    (E := E) (ι := Fin 2) ν 0 (h := 1) (M := 0)
      (by norm_num) (by norm_num) hinputI hinput
  dsimp only at href
  rcases href with ⟨hB, hX, hP0, hrefI, hrefBound, hG, hnoiseI, hnoise⟩
  have hH : ∀ x v : E,
      ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖ ^ 2 ≤
        (fderiv ℝ (fderiv ℝ (fun _ : E => (0 : ℝ))) x v) v ∧
      (fderiv ℝ (fderiv ℝ (fun _ : E => (0 : ℝ))) x v) v ≤ ‖v‖ ^ 2 := by
    intro x v
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  have hbudget : (0 : ℝ) + (1 - Real.exp (-1)) * (Module.finrank ℝ E : ℝ) = 0 := by
    simp [E]
  have hrefBound0' : (∫ w : (((E × E) × E) × (Fin 2 → E)),
      ‖w.1.1.1 - (0 : E)‖ ^ 2 +
        ‖Real.exp (-(1 : ℝ) / 2) • w.1.1.2 +
          Real.sqrt (1 - Real.exp (-(1 : ℝ))) • w.1.2‖ ^ 2
      ∂(ν.prod (stdGaussian E)).prod
        (Measure.pi (fun _ : Fin 2 => stdGaussian E))) ≤ 0 := by
    simpa only [hbudget] using hrefBound
  obtain ⟨p, N, q, hp, hN, hq, heqP, hrun, h0, hz, h1⟩ :=
    picard_center_gradient_moment
      (E := E) (Ω := ((E × E) × E) × (Fin 2 → E)) (ι := Fin 2)
      (V := fun _ : E => (0 : ℝ)) (κ := 1) (by norm_num) contDiff_const hH
      (eta := 3 / 4) (c := 7 / 8) (eps := 1 / 10)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      ((ν.prod (stdGaussian E)).prod (Measure.pi (fun _ : Fin 2 => stdGaussian E)))
      (fun w => w.1.1.1)
      (fun w => Real.exp (-(1 : ℝ) / 2) • w.1.1.2 +
        Real.sqrt (1 - Real.exp (-(1 : ℝ))) • w.1.2)
      hX hP0 0 (by simp) (fun _ => 1) (by simp)
      (fun j w => w.2 j) hG (fun _ _ => 1)
      (M := 0) (S := 2) (by norm_num) (by norm_num)
      hrefI hrefBound0' hnoiseI (by intro j; rw [hnoise j])
      (by intro; norm_num)
  have _ := hB
  have _ := h0 (0 : Fin 2)
  have _ := hz (0 : Fin 2)
  have _ := h1 (0 : Fin 2)
  refine ⟨N, ?_⟩
  simpa only [Subsingleton.elim (q 0) 0] using (hrun (0 : E)).2
