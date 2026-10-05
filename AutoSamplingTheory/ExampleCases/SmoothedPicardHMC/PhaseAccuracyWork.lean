import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SourceQuadratureWork
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalPhaseStability
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalExecutionIdentity

/-! Same stopped interpreter and actual source phase: precision and expected
query work are proved for identical witnesses under the genuine driving law.
One phase only; neither main theorem nor TV-based unbounded cost transfer. -/
noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators
namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseAccuracyWork
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The actual source-coefficient stopped phase has both Euclidean all-rho
precision and integrable expected returned gradient counts for the same p,q,N. -/
theorem source_phase_accuracy_and_work {J : ℕ} (hJ : 2 ≤ J) {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps)
    (ν : Measure (E × E)) [IsProbabilityMeasure ν]
    (xstar : E) (hstar : gradient V xstar = 0)
    {h M : ℝ} (hh : 0 < h) (hM : 0 ≤ M)
    (hstateI : Integrable (fun s : E × E => ‖s.1-xstar‖^2 + ‖s.2‖^2) ν)
    (hstate : (∫ s : E × E, ‖s.1-xstar‖^2 + ‖s.2‖^2 ∂ν) ≤ M)
:
    let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
    let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
    let Lambda := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Set.Icc 0 h)
    let omega := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
    let positionWeight := omega ⟨J-1,by omega⟩
    let momentumWeight := fun j : Fin J => ∫ s in 0..h, (ell j).eval s
    let S := h^2/2*Lambda
    let a := Real.exp (-h/2)
    let sigma := Real.sqrt (1-Real.exp (-h))
    let gi := Measure.pi (fun _ : Fin J => stdGaussian E)
    let γ := ((stdGaussian E).prod (stdGaussian E)).prod (gi.prod gi)
    let μ := ν.prod γ
    let MR := M + (1-Real.exp (-h)) * (Module.finrank ℝ E : ℝ)
    let B := 6*MR + 3*eps^2 + 3*eta*(Module.finrank ℝ E : ℝ)
    let C := 2 + (1+Real.log ((1-c)⁻¹))/(-Real.log c)
    let L0 := C*(1+Real.log (1+Real.sqrt (2*MR)/eps))
    let L1 := C*(1+Real.log (1+Real.sqrt (4*MR+2*S^2*B)/eps))
    h^2*Lambda ≤ 1 →
    ∃ p q : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable q ∧ Measurable N ∧
      (∀ y, p y + eta • gradient V (p y) = y ∧ ‖q y-p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y+1) y =
          some (q y,N y+1)) ∧ LipschitzWith 1 p ∧
      let P0 := fun w : (E × E) × ((E × E) × ((Fin J → E) × (Fin J → E))) =>
        a • w.1.2 + sigma • w.2.1.1
      let Y0 := fun i w => w.1.1 + t i • P0 w
      let Z0 := fun j w => gradient V (q (Y0 j w) + Real.sqrt eta • w.2.2.1 j)
      let Y1 := fun i w => Y0 i w - ∑ j, omega i j • Z0 j w
      let Z1 := fun j w => gradient V (q (Y1 j w) + Real.sqrt eta • w.2.2.2 j)
      let Φ := fun w => (w.1.1 + h • P0 w - ∑ j, positionWeight j • Z1 j w,
        a • (P0 w - ∑ j, momentumWeight j • Z1 j w) + sigma • w.2.1.2)
      let T := fun w => 2*J+∑ i, ((N (Y0 i w)+1)+(N (Y1 i w)+1))
      let Z0p := fun j w => gradient V (p (Y0 j w) + Real.sqrt eta • w.2.2.1 j)
      let Y1p := fun i w => Y0 i w - ∑ j, omega i j • Z0p j w
      let Z1p := fun j w => gradient V (p (Y1p j w) + Real.sqrt eta • w.2.2.2 j)
      let Φp := fun w => (w.1.1 + h • P0 w - ∑ j, positionWeight j • Z1p j w,
        a • (P0 w - ∑ j, momentumWeight j • Z1p j w) + sigma • w.2.1.2)
      let W := fun (rho : ℝ) (μ ν : Measure (E × E)) =>
        (TechnicalLemmas.Measure.Transport.transportCost
          (fun z : (E × E) × (E × E) =>
            (ENNReal.ofReal (Real.sqrt (‖z.1.1-z.2.1‖^2+‖z.1.2-z.2.2‖^2)))^rho)
          μ ν)^(rho⁻¹)
      Measurable Φ ∧ Measurable T ∧
      ∃ Kp Kq : Kernel (E × E) (E × E), IsMarkovKernel Kp ∧ IsMarkovKernel Kq ∧
      (∀ s, Kp s = γ.map (fun z => Φp (s,z))) ∧
      (∀ s, Kq s = γ.map (fun z => Φ (s,z))) ∧
      (∀ w, CountedPhaseProgram.phaseQuery (gradient V) eta eps h t omega positionWeight momentumWeight
        (fun y => N y+1) w = some (Φ w,T w)) ∧
      Integrable (fun w => (T w : ℝ)) μ ∧
      (∫ w, (T w : ℝ) ∂μ) ≤ (J : ℝ)*(2+L0+L1) ∧
      ∀ s rho, 1 ≤ rho → W rho (Kq s) (Kp s) ≤ ENNReal.ofReal (3*h*Lambda*eps) := by
  classical
  dsimp only
  intro hstep
  obtain ⟨_,_,_,_,_,hLambda,_,_⟩ :=
    TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature.chebyshev_lobatto_coefficients hJ hh
  have hh1 : h ≤ 1 := by
    have hsq : h^2 ≤ 1 := (le_mul_of_one_le_right (sq_nonneg h) hLambda).trans hstep
    nlinarith only [hsq,hh]
  have heta1 : eta < 1 := hec.trans_lt hc
  obtain ⟨p1,q1,N1,hp1,hq1,hN1,hall1,hPhi1,hT1,_,hrun1,hTI1,hcost1⟩ :=
    SourceQuadratureWork.source_quadrature_phase_work hJ hκ hV hH heta hec hc heps
      ν xstar hstar hh hh1 hM hstateI hstate
  obtain ⟨p2,q2,N2,hp2,hq2,hN2,hall2,hLip2,Kp,Kq,hKp,hKq,hKppush,hKqpush,hW,_⟩ :=
    ProximalPhaseStability.source_phase_proximal_stability hκ hV hH heta heta1 heps hJ hh hstep
  have hH' : ∀ x v : E, ((κ⁻¹ : ℝ≥0) : ℝ)*‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (1 : ℝ≥0)*‖v‖^2 := by
    simpa only [NNReal.coe_inv,NNReal.coe_one,one_mul] using hH
  have hreg := TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    (r := 0) hV hH' (0 : E)
  have hg : LipschitzWith 1 (gradient V) := by simpa using hreg.2
  have hpEq : p1 = p2 := by
    funext y
    have hop1 := (hall1 y).1
    have hop2 := (hall2 y).1
    have hd : p1 y-p2 y = eta • (gradient V (p2 y)-gradient V (p1 y)) := by
      calc
        p1 y-p2 y = (p1 y+eta • gradient V (p1 y)) -
            (p2 y+eta • gradient V (p2 y)) +
            eta • (gradient V (p2 y)-gradient V (p1 y)) := by module
        _ = eta • (gradient V (p2 y)-gradient V (p1 y)) := by rw [hop1,hop2]; simp
    have hn : ‖p1 y-p2 y‖ ≤ eta*‖p1 y-p2 y‖ := by
      calc
        ‖p1 y-p2 y‖ = eta*‖gradient V (p2 y)-gradient V (p1 y)‖ := by
          rw [hd,norm_smul,Real.norm_eq_abs,abs_of_pos heta]
        _ ≤ eta*‖p1 y-p2 y‖ := by
          have hb := hg.norm_sub_le (p2 y) (p1 y)
          simpa only [NNReal.coe_one,one_mul,norm_sub_rev] using
            mul_le_mul_of_nonneg_left hb heta.le
    have hz : ‖p1 y-p2 y‖ = 0 := by
      nlinarith only [hn,norm_nonneg (p1 y-p2 y),heta1]
    exact sub_eq_zero.mp (norm_eq_zero.mp hz)
  have hpair (y : E) : (q1 y,N1 y+1) = (q2 y,N2 y+1) :=
    ProximalExecutionIdentity.successful_query_unique (gradient V) eta eps y
      (hall1 y).2.2 (hall2 y).2.2
  have hqEq : q1 = q2 := by funext y; exact congrArg Prod.fst (hpair y)
  have hNEq : N1 = N2 := by
    funext y
    exact Nat.add_right_cancel (congrArg Prod.snd (hpair y))
  subst p2
  subst q2
  subst N2
  exact ⟨p1,q1,N1,hp1,hq1,hN1,hall1,hLip2,hPhi1,hT1,Kp,Kq,hKp,hKq,
    hKppush,hKqpush,hrun1,hTI1,hcost1,hW⟩

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PhaseAccuracyWork
