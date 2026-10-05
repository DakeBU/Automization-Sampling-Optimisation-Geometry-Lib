import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.CountedPhaseProgram

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC

-- Insufficient fuel gives no successful phase count; no nominal count is returned.
example (w : (ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)))) :
    CountedPhaseProgram.phaseQuery (fun x : ℝ => x) (3/4) (1/10) 1
      (fun _ => 1/3) (fun _ _ => 1/4) (fun _ => 1/3) (fun _ => 1/2)
      (fun _ => 0) w = none := by rfl

-- Positive-dimensional, positive-time, two-node full driving law. The actual
-- program succeeds and its returned count has the proved numerical L1 bound.
example (V : ℝ → ℝ) (hV : ContDiff ℝ 2 V) (hstar : gradient V 0 = 0)
    (hH : ∀ x v : ℝ, ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2) :
    let gi := Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)
    let γ := ((stdGaussian ℝ).prod (stdGaussian ℝ)).prod (gi.prod gi)
    let μ := (Measure.dirac ((0,0) : ℝ × ℝ)).prod γ
    let MR := 1-Real.exp (-1)
    let B := 6*MR+3*(1/10 : ℝ)^2+3*(3/4 : ℝ)
    let C := 2+(1+Real.log ((1-(7/8 : ℝ))⁻¹))/(-Real.log (7/8))
    ∃ N : ℝ → ℕ, ∃ Φ : ((ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)))) → ℝ × ℝ,
      ∃ T : ((ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)))) → ℕ,
      Measurable T ∧
      (∀ w, CountedPhaseProgram.phaseQuery (gradient V) (3/4) (1/10) 1
        (fun _ => 1/3) (fun _ _ => 1/4) (fun _ => 1/3) (fun _ => 1/2)
        (fun y => N y+1) w = some (Φ w,T w)) ∧
      Integrable (fun w => (T w : ℝ)) μ ∧
      (∫ w, (T w : ℝ) ∂μ) ≤ 2*(2+C*(1+Real.log (1+Real.sqrt (2*MR)/(1/10)))+
        C*(1+Real.log (1+Real.sqrt (4*MR+2*(1/2 : ℝ)^2*B)/(1/10)))) := by
  classical
  dsimp only
  have hH' : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2 := by simpa using hH
  obtain ⟨p,q,N,hp,hq,hN,hall,hΦ,hT,K,hprogram,hI,hbound⟩ :=
    CountedPhaseProgram.implemented_phase_expected_query_work
      (E := ℝ) (m := 2) (κ := 1) (eta := 3/4) (c := 7/8) (eps := 1/10)
      (by norm_num) hV hH' (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      (Measure.dirac ((0,0) : ℝ × ℝ)) 0 hstar
      (h := 1) (M := 0) (S := 1/2) (by norm_num) (by norm_num) (by norm_num)
      (by apply integrable_dirac; simp) (by simp) (fun _ => 1/3) (fun _ => by norm_num)
      (fun _ _ => 1/4) (fun _ => by norm_num [Fin.sum_univ_two])
      (fun _ => 1/3) (fun _ => 1/2)
  refine ⟨N,_,_,hT,hprogram,hI,?_⟩
  simpa using hbound

#print axioms CountedPhaseProgram.implemented_phase_expected_query_work
