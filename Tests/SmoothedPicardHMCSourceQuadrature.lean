import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SourceQuadratureWork

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC
open AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature

-- Actual two-node cardinal basis, constant-exact quadrature and sharp row bound.
example :
    let t := fun i : Fin 2 => (1/2 : ℝ)/2*(1-Real.cos ((i : ℝ)/(2-1 : ℝ)*Real.pi))
    let ell := fun j : Fin 2 => Lagrange.basis Finset.univ t j
    let Lambda := sSup ((fun s : ℝ => ∑ j : Fin 2, |(ell j).eval s|) '' Set.Icc 0 (1/2 : ℝ))
    let omega := fun i j : Fin 2 => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    (∀ i j, (ell i).eval (t j) = if i=j then 1 else 0) ∧
    1 ≤ Lambda ∧
    (∀ i, (∑ j : Fin 2, |omega i j|) ≤ (1/2 : ℝ)^2/2*Lambda) ∧
    (∑ j : Fin 2, ∫ s in 0..(1/2 : ℝ), (ell j).eval s) = 1/2 := by
  obtain ⟨_,_,_,hcard,_,hLambda,hrow,hmom⟩ :=
    chebyshev_lobatto_coefficients (J := 2) (h := 1/2) (by norm_num) (by norm_num)
  exact ⟨hcard,hLambda,(fun i => (hrow i).2),hmom⟩

-- One-dimensional full Gaussian phase at positive time with the actual source
-- arrays, not constant toy nodes or an assumed row envelope.
example (V : ℝ → ℝ) (hV : ContDiff ℝ 2 V) (hstar : gradient V 0 = 0)
    (hH : ∀ x v : ℝ, ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2) :
    let t := fun i : Fin 2 => (1/2 : ℝ)/2*(1-Real.cos ((i : ℝ)/(2-1 : ℝ)*Real.pi))
    let ell := fun j : Fin 2 => Lagrange.basis Finset.univ t j
    let Lambda := sSup ((fun s : ℝ => ∑ j : Fin 2, |(ell j).eval s|) '' Set.Icc 0 (1/2 : ℝ))
    let omega := fun i j : Fin 2 => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    let momentumWeight := fun j : Fin 2 => ∫ s in 0..(1/2 : ℝ), (ell j).eval s
    let gi := Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)
    let γ := ((stdGaussian ℝ).prod (stdGaussian ℝ)).prod (gi.prod gi)
    let μ := (Measure.dirac ((0,0) : ℝ × ℝ)).prod γ
    let MR := 1-Real.exp (-(1/2 : ℝ))
    let B := 6*MR+3*(1/10 : ℝ)^2+3*(3/4 : ℝ)
    let C := 2+(1+Real.log ((1-(7/8 : ℝ))⁻¹))/(-Real.log (7/8))
    ∃ N : ℝ → ℕ, ∃ Φ : ((ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)))) → ℝ × ℝ,
      ∃ T : ((ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)))) → ℕ,
      Measurable T ∧
      (∀ w, CountedPhaseProgram.phaseQuery (gradient V) (3/4) (1/10) (1/2)
        t omega (omega 1) momentumWeight (fun y => N y+1) w = some (Φ w,T w)) ∧
      Integrable (fun w => (T w : ℝ)) μ ∧
      (∫ w, (T w : ℝ) ∂μ) ≤ 2*(2+C*(1+Real.log (1+Real.sqrt (2*MR)/(1/10)))+
        C*(1+Real.log (1+Real.sqrt (4*MR+2*((1/2 : ℝ)^2/2*Lambda)^2*B)/(1/10)))) := by
  classical
  dsimp only
  have hH' : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2 := by simpa using hH
  obtain ⟨p,q,N,hp,hq,hN,hall,hΦ,hT,K,hprogram,hI,hbound⟩ :=
    SourceQuadratureWork.source_quadrature_phase_work
      (E := ℝ) (J := 2) (by norm_num) (κ := 1) (eta := 3/4) (c := 7/8) (eps := 1/10)
      (by norm_num) hV hH' (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      (Measure.dirac ((0,0) : ℝ × ℝ)) 0 hstar
      (h := 1/2) (M := 0) (by norm_num) (by norm_num) (by norm_num)
      (by apply integrable_dirac; simp) (by simp)
  refine ⟨N,_,_,hT,hprogram,hI,?_⟩
  simpa using hbound

#print axioms chebyshev_lobatto_coefficients
#print axioms SourceQuadratureWork.source_quadrature_phase_work
