import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.RealizedProximalWork
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseKernel

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC

-- The actual positive-dimensional, two-node phase supplies q and N.
-- The input's moment remains the explicit D.7 boundary; no cost premise is used.
example (V : ℝ → ℝ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : ℝ, ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2)
    (hmoment :
      let γ := ((stdGaussian ℝ).prod (stdGaussian ℝ)).prod
        ((Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)).prod
          (Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)))
      let Y := fun w : (ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)) =>
        (1 : ℝ) + (1/3) * (Real.exp (-1/2) * 2 + Real.sqrt (1-Real.exp (-1)) * w.1.1)
      Integrable (fun w => ‖gradient V (Y w)‖^2) γ) :
    let γ := ((stdGaussian ℝ).prod (stdGaussian ℝ)).prod
      ((Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)).prod
        (Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)))
    let Y := fun w : (ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)) =>
      (1 : ℝ) + (1/3) * (Real.exp (-1/2) * 2 + Real.sqrt (1-Real.exp (-1)) * w.1.1)
    ∃ q : ℝ → ℝ, ∃ N : ℝ → ℕ,
      (∀ y, ApproximateProximalExecution.proximalQuery (gradient V) (3/4) (1/10) y
        (N y+1) y = some (q y,N y+1)) ∧
      Integrable (fun w => (N (Y w) : ℝ)+1) γ ∧
      (∫ w, (N (Y w) : ℝ)+1 ∂γ) ≤
        (2 + (1+Real.log ((1-(7/8 : ℝ))⁻¹))/(-Real.log (7/8))) *
        (1+Real.log (1+Real.sqrt (∫ w, ‖gradient V (Y w)‖^2 ∂γ)/(1/10))) := by
  dsimp only at hmoment ⊢
  have hH' : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2 := by simpa using hH
  obtain ⟨p,q,N,hp,hq,hN,hall,hphase⟩ :=
    ImplementedPhaseKernel.implemented_phase_kernel (E := ℝ) (ι := Fin 2)
      (κ := 1) (eta := 3/4) (c := 7/8) (eps := 1/10)
      (by norm_num) hV hH' (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      1 (by norm_num) (fun _ => 1/3) (fun _ _ => 1/4) (fun _ => 1/3) (fun _ => 1/2)
  have hrun := fun y => (hall y).2.2
  refine ⟨q,N,hrun,?_⟩
  exact RealizedProximalWork.realized_proximal_expected_work _
    (κ := 1) (eta := 3/4) (c := 7/8) (eps := 1/10)
    (by norm_num) hV hH' (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    q N hrun _ (by fun_prop) hmoment

#print axioms RealizedProximalWork.realized_proximal_expected_work
