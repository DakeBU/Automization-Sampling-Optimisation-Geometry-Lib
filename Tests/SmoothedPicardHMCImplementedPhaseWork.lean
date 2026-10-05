import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseWork

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC

-- A one-dimensional, two-node, positive-time phase. All four innovation
-- factors are retained, and the query-center moment is a conclusion.
example (V : ℝ → ℝ) (hV : ContDiff ℝ 2 V) (hstar : gradient V 0 = 0)
    (hH : ∀ x v : ℝ, ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2) :
    let gi := Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)
    let γ := ((stdGaussian ℝ).prod (stdGaussian ℝ)).prod (gi.prod gi)
    let μ := (Measure.dirac ((0,0) : ℝ × ℝ)).prod γ
    let P0 := fun w : (ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ))) =>
      Real.exp (-1/2) • w.1.2 + Real.sqrt (1-Real.exp (-1)) • w.2.1.1
    let Y0 := fun (i : Fin 2) w => w.1.1 + (1/3 : ℝ) • P0 w
    ∃ q : ℝ → ℝ, ∃ N : ℝ → ℕ,
      (∀ y, ApproximateProximalExecution.proximalQuery (gradient V) (3/4) (1/10) y
        (N y+1) y = some (q y,N y+1)) ∧
      let Y1 := fun (i : Fin 2) w => Y0 i w - ∑ j : Fin 2, (1/4 : ℝ) •
        gradient V (q (Y0 j w) + Real.sqrt (3/4) • w.2.2.1 j)
      (∀ i, Integrable (fun w => ‖gradient V (Y0 i w)‖^2) μ ∧
        (∫ w, ‖gradient V (Y0 i w)‖^2 ∂μ) ≤ 2*(1-Real.exp (-1))) ∧
      (∀ i, Integrable (fun w => (N (Y0 i w) : ℝ)+1) μ ∧
        Integrable (fun w => (N (Y1 i w) : ℝ)+1) μ) := by
  classical
  dsimp only
  have hH' : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2 := by simpa using hH
  obtain ⟨p,q,N,hp,hq,hN,hall,hΦ,K,hK,hKlaw,hw0,hw1⟩ :=
    ImplementedPhaseWork.implemented_phase_query_moments_and_work
      (E := ℝ) (ι := Fin 2) (κ := 1) (eta := 3/4) (c := 7/8) (eps := 1/10)
      (by norm_num) hV hH' (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      (Measure.dirac ((0,0) : ℝ × ℝ)) 0 hstar
      (h := 1) (M := 0) (S := 1/2) (by norm_num) (by norm_num) (by norm_num)
      (by apply integrable_dirac; simp) (by simp) (fun _ => 1/3) (fun _ => by norm_num)
      (fun _ _ => 1/4) (fun _ => by norm_num [Fin.sum_univ_two])
      (fun _ => 1/3) (fun _ => 1/2)
  refine ⟨q,N,(fun y => (hall y).2.2),?_,?_⟩
  · intro i
    constructor
    · simpa using (hw0 i).1
    · simpa using (hw0 i).2.1
  · intro i
    exact ⟨(hw0 i).2.2.1,(hw1 i).2.2.1⟩

#print axioms ProximalExecutionIdentity.successful_query_unique
#print axioms ImplementedPhaseWork.implemented_phase_query_moments_and_work
