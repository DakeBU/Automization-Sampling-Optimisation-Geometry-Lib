import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseAccuracyWork
noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC
-- Reuse the earlier focused test's direct two-node basis calculation.
-- Test-only copy: no new shared lemma or mathematical-progress credit.
private theorem two_node_lebesgue :
    let t := fun i : Fin 2 => (1/2 : ℝ)/2*(1-Real.cos ((i : ℝ)/(2-1 : ℝ)*Real.pi))
    let ell := fun j : Fin 2 => Lagrange.basis Finset.univ t j
    sSup ((fun s : ℝ => ∑ j : Fin 2, |(ell j).eval s|) '' Set.Icc 0 (1/2 : ℝ)) = 1 := by
  classical
  dsimp only
  let t := fun i : Fin 2 => (1/2 : ℝ)/2*(1-Real.cos ((i : ℝ)/(2-1 : ℝ)*Real.pi))
  let ell := fun j : Fin 2 => Lagrange.basis Finset.univ t j
  have ht0 : t 0 = 0 := by norm_num [t]
  have ht1 : t 1 = 1/2 := by norm_num [t]
  have he0 (s : ℝ) : (ell 0).eval s = 1-2*s := by
    simp only [ell,Finset.univ_fin2,Lagrange.basis_pair_left (by decide : (0 : Fin 2) ≠ 1)]
    norm_num [Lagrange.basisDivisor,ht0,ht1]
    ring
  have he1 (s : ℝ) : (ell 1).eval s = 2*s := by
    simp only [ell,Finset.univ_fin2,Lagrange.basis_pair_right (by decide : (0 : Fin 2) ≠ 1)]
    norm_num [Lagrange.basisDivisor,ht0,ht1]
  have hc (s : ℝ) (hs : s ∈ Set.Icc 0 (1/2 : ℝ)) :
      (∑ j : Fin 2, |(ell j).eval s|) = 1 := by
    rw [Fin.sum_univ_two,he0,he1,abs_of_nonneg (by linarith [hs.2]),
      abs_of_nonneg (by linarith [hs.1])]
    ring
  have hr : ((fun s : ℝ => ∑ j : Fin 2, |(ell j).eval s|) '' Set.Icc 0 (1/2 : ℝ)) = {1} := by
    ext x
    constructor
    · rintro ⟨s,hs,rfl⟩
      exact Set.mem_singleton_iff.mpr (hc s hs)
    · intro hx
      have hx1 := Set.mem_singleton_iff.mp hx
      refine ⟨0,by norm_num,?_⟩
      exact (hc 0 (by norm_num)).trans hx1.symm
  rw [hr,csSup_singleton]

-- Same returned N and full output Phi now support the true kernel law,
-- all-rho precision and actual-law expected total returned query count.
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
    let W := fun (rho : ℝ) (μ ν : Measure (ℝ × ℝ)) =>
      (AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
        (fun z : (ℝ × ℝ) × (ℝ × ℝ) =>
          (ENNReal.ofReal (Real.sqrt (‖z.1.1-z.2.1‖^2+‖z.1.2-z.2.2‖^2)))^rho)
        μ ν)^(rho⁻¹)
    ∃ p q : ℝ → ℝ, ∃ N : ℝ → ℕ,
    ∃ Φ : ((ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)))) → ℝ × ℝ,
    ∃ T : ((ℝ × ℝ) × ((ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)))) → ℕ,
    ∃ Kp Kq : Kernel (ℝ × ℝ) (ℝ × ℝ),
      LipschitzWith 1 p ∧ Measurable T ∧ IsMarkovKernel Kp ∧ IsMarkovKernel Kq ∧
      (∀ y, ‖q y-p y‖ ≤ 1/10 ∧
        ApproximateProximalExecution.proximalQuery (gradient V) (3/4) (1/10) y
          (N y+1) y = some (q y,N y+1)) ∧
      (∀ s, Kq s = γ.map (fun z => Φ (s,z))) ∧
      (∀ w, CountedPhaseProgram.phaseQuery (gradient V) (3/4) (1/10) (1/2)
        t omega (omega 1) momentumWeight (fun y => N y+1) w = some (Φ w,T w)) ∧
      Integrable (fun w => (T w : ℝ)) μ ∧
      (∫ w, (T w : ℝ) ∂μ) ≤ 2*(2+C*(1+Real.log (1+Real.sqrt (2*MR)/(1/10)))+
        C*(1+Real.log (1+Real.sqrt (4*MR+2*((1/2 : ℝ)^2/2*Lambda)^2*B)/(1/10)))) ∧
      (∀ s rho, 1 ≤ rho → W rho (Kq s) (Kp s) ≤ ENNReal.ofReal (3/20)) := by
  classical
  dsimp only
  have hH' : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2 := by simpa using hH
  have hstep :
      (1/2 : ℝ)^2 * sSup ((fun s : ℝ => ∑ j : Fin 2,
        |(Lagrange.basis Finset.univ
          (fun i : Fin 2 => (1/2 : ℝ)/2*(1-Real.cos ((i : ℝ)/(2-1 : ℝ)*Real.pi))) j).eval s|) ''
            Set.Icc 0 (1/2 : ℝ)) ≤ 1 := by rw [two_node_lebesgue]; norm_num
  obtain ⟨p,q,N,hp,hq,hN,hall,hLip,hΦ,hT,Kp,Kq,hKp,hKq,hKppush,hKqpush,hprogram,hI,hbound,hW⟩ :=
    PhaseAccuracyWork.source_phase_accuracy_and_work
      (E := ℝ) (J := 2) (by norm_num) (κ := 1) (eta := 3/4) (c := 7/8) (eps := 1/10)
      (by norm_num) hV hH' (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      (Measure.dirac ((0,0) : ℝ × ℝ)) 0 hstar
      (h := 1/2) (M := 0) (by norm_num) (by norm_num)
      (by apply integrable_dirac; simp) (by simp) hstep
  refine ⟨p,q,N,_,_,Kp,Kq,hLip,hT,hKp,hKq,(fun y => (hall y).2),hKqpush,hprogram,hI,?_,?_⟩
  · simpa using hbound
  · intro s rho hrho
    have hb := hW s rho hrho
    have hLeb := two_node_lebesgue
    dsimp only at hLeb
    simp only [Nat.cast_ofNat] at hb
    rw [hLeb] at hb
    norm_num at hb ⊢
    exact hb

#print axioms PhaseAccuracyWork.source_phase_accuracy_and_work
