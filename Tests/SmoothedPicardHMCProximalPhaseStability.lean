import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalPhaseStability
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal ENNReal BigOperators
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC
open AutoSamplingTheory.TechnicalLemmas.Analysis

-- The source two-node basis has actual Lebesgue constant one: the small-step
-- test below does not assume a possibly inconsistent coefficient envelope.
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

-- Positive-dimensional full-range eta=3/4, actual source nodes/weights and
-- successful terminal-inclusive queries. Exercise all finite q>=1 and the
-- delta=0 exact-oracle boundary, with the true Euclidean phase cost.
example (V : ℝ → ℝ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : ℝ, ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2) :
    let W := fun (rho : ℝ) (μ ν : Measure (ℝ × ℝ)) =>
      (AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
        (fun z : (ℝ × ℝ) × (ℝ × ℝ) =>
          (ENNReal.ofReal (Real.sqrt (‖z.1.1-z.2.1‖^2+‖z.1.2-z.2.2‖^2)))^rho)
        μ ν)^(rho⁻¹)
    ∃ p q : ℝ → ℝ, ∃ N : ℝ → ℕ, ∃ Kp Kq Kr : Kernel (ℝ × ℝ) (ℝ × ℝ),
      Measurable p ∧ Measurable q ∧ Measurable N ∧ LipschitzWith 1 p ∧
      (∀ y, ApproximateProximalExecution.proximalQuery (gradient V) (3/4) (1/10)
        y (N y+1) y = some (q y,N y+1)) ∧
      IsMarkovKernel Kp ∧ IsMarkovKernel Kq ∧ IsMarkovKernel Kr ∧
      (∀ rho, 1 ≤ rho → W rho (Kq (0,0)) (Kp (0,0)) ≤ ENNReal.ofReal (3/20)) ∧
      (∀ rho, 1 ≤ rho → W rho (Kr (0,0)) (Kp (0,0)) = 0) := by
  dsimp only
  have hH' : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2 := by simpa using hH
  have hstep :
      (1/2 : ℝ)^2 * sSup ((fun s : ℝ => ∑ j : Fin 2,
        |(Lagrange.basis Finset.univ
          (fun i : Fin 2 => (1/2 : ℝ)/2*(1-Real.cos ((i : ℝ)/(2-1 : ℝ)*Real.pi))) j).eval s|) ''
            Set.Icc 0 (1/2 : ℝ)) ≤ 1 := by
    rw [two_node_lebesgue]
    norm_num
  obtain ⟨p,q,N,hp,hq,hN,hall,hpLip,Kp,Kq,hKp,hKq,hKppush,hKqpush,hbound,hgeneral⟩ :=
    ProximalPhaseStability.source_phase_proximal_stability (E := ℝ) (κ := 1)
      (by norm_num) hV hH' (eta := 3/4) (eps := 1/10) (by norm_num) (by norm_num)
      (by norm_num) (J := 2) (by norm_num) (h := 1/2) (by norm_num) hstep
  obtain ⟨Kr,hKr,hKrpush,hzero⟩ := hgeneral p hp 0 (by norm_num) (by simp)
  refine ⟨p,q,N,Kp,Kq,Kr,hp,hq,hN,hpLip,fun y => (hall y).2.2,hKp,hKq,hKr,?_,?_⟩
  · intro rho hrho
    have hb := hbound (0,0) rho hrho
    have hLeb := two_node_lebesgue
    dsimp only at hLeb
    simp only [Nat.cast_ofNat] at hb
    rw [hLeb] at hb
    norm_num at hb ⊢
    exact hb
  · intro rho hrho
    apply le_antisymm _ (zero_le)
    simpa using hzero (0,0) rho hrho

#print axioms MonotoneProximalMap.nonexpansive_of_monotone_optimality
#print axioms ChebyshevLobattoMomentum.momentum_absolute_sum_le
#print axioms ProximalPhaseStability.source_phase_proximal_stability
#print axioms ProximalEstimatorLipschitz.proximal_estimator_lipschitz
