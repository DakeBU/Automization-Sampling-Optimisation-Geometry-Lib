import AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.CountedPhaseProgram

/-! Actual3.6/B1 quadrature arrays in Algorithm3.1's certified gradient-only
phase. No supplied node/row assumptions or silent m/J adapter. Logarithmic
Lebesgue bound, nonnegative weights and all run-wide/main claims remain open. -/
noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SourceQuadratureWork
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The source Chebyshev-Lobatto nodes and integral weights instantiate the
actual counted Gaussian phase, deriving the row budget from its true Lebesgue
supremum. All successful proximal/direct counts use the same full phase law. -/
theorem source_quadrature_phase_work {J : ℕ} (hJ : 2 ≤ J) {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps)
    (ν : Measure (E × E)) [IsProbabilityMeasure ν]
    (xstar : E) (hstar : gradient V xstar = 0)
    {h M : ℝ} (hh : 0 < h) (hh1 : h ≤ 1) (hM : 0 ≤ M)
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
    ∃ p q : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable q ∧ Measurable N ∧
      (∀ y, p y + eta • gradient V (p y) = y ∧ ‖q y-p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y+1) y =
          some (q y,N y+1)) ∧
      let P0 := fun w : (E × E) × ((E × E) × ((Fin J → E) × (Fin J → E))) =>
        a • w.1.2 + sigma • w.2.1.1
      let Y0 := fun i w => w.1.1 + t i • P0 w
      let Z0 := fun j w => gradient V (q (Y0 j w) + Real.sqrt eta • w.2.2.1 j)
      let Y1 := fun i w => Y0 i w - ∑ j, omega i j • Z0 j w
      let Z1 := fun j w => gradient V (q (Y1 j w) + Real.sqrt eta • w.2.2.2 j)
      let Φ := fun w => (w.1.1 + h • P0 w - ∑ j, positionWeight j • Z1 j w,
        a • (P0 w - ∑ j, momentumWeight j • Z1 j w) + sigma • w.2.1.2)
      let T := fun w => 2*J+∑ i, ((N (Y0 i w)+1)+(N (Y1 i w)+1))
      Measurable Φ ∧ Measurable T ∧
      (∃ K : Kernel (E × E) (E × E), IsMarkovKernel K ∧
        ∀ s, K s = γ.map (fun z => Φ (s,z))) ∧
      (∀ w, CountedPhaseProgram.phaseQuery (gradient V) eta eps h t omega positionWeight momentumWeight
        (fun y => N y+1) w = some (Φ w,T w)) ∧
      Integrable (fun w => (T w : ℝ)) μ ∧
      (∫ w, (T w : ℝ) ∂μ) ≤ (J : ℝ)*(2+L0+L1) := by
  classical
  dsimp only
  let t := fun i : Fin J => h/2*(1-Real.cos ((i : ℝ)/(J-1 : ℝ)*Real.pi))
  let ell := fun j : Fin J => Lagrange.basis Finset.univ t j
  let Lambda := sSup ((fun s : ℝ => ∑ j : Fin J, |(ell j).eval s|) '' Set.Icc 0 h)
  let omega := fun i j : Fin J => ∫ s in 0..t i, (t i-s)*(ell j).eval s
  let S := h^2/2*Lambda
  obtain ⟨ht,hinj,hlast,hcard,hpart,hLambda,hrow,hmom⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature.chebyshev_lobatto_coefficients hJ hh
  have ht' (i : Fin J) : |t i| ≤ 1 := by
    apply abs_le.mpr
    have hti : 0 ≤ t i := (ht i).1
    exact ⟨(by norm_num : (-1 : ℝ) ≤ 0).trans hti,(ht i).2.trans hh1⟩
  have hS : 0 ≤ S := by
    dsimp [S]
    exact mul_nonneg (by positivity) (by linarith : 0 ≤ Lambda)
  exact CountedPhaseProgram.implemented_phase_expected_query_work hκ hV hH heta hec hc heps
    ν xstar hstar hh.le hM hS hstateI hstate t ht' omega (fun i => (hrow i).2)
    (omega ⟨J-1,by omega⟩) (fun j => ∫ s in 0..h, (ell j).eval s)

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SourceQuadratureWork
