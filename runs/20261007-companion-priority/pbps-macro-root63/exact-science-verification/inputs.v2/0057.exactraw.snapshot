import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1600000

theorem actual_positive_defect_complex_lift
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let ι : Lp ℝ 2 ν →L[ℝ] Lp ℂ 2 ν := Complex.ofRealCLM.compLpL 2 ν
    let R : Lp ℂ 2 ν →L[ℝ] Lp ℝ 2 ν := Complex.reCLM.compLpL 2 ν
    let Q : Lp ℂ 2 ν →L[ℝ] Lp ℝ 2 ν := Complex.imCLM.compLpL 2 ν
    let C : Lp ℂ 2 ν →L[ℝ] Lp ℂ 2 ν := Complex.conjCLE.toContinuousLinearMap.compLpL 2 ν
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        IsSelfAdjoint T ∧
        (∀ u : Lp ℝ 2 ν, ‖T u‖ ≤ ‖u‖ ∧
          (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
          (∫ y, T u y ∂ν) = ∫ y, u y ∂ν) ∧
        ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T).IsPositive ∧
        (∀ u : Lp ℝ 2 ν, ‖ι u‖ = ‖u‖) ∧
        (∀ g : Lp ℂ 2 ν, C g = g ↔ ∃ u : Lp ℝ 2 ν, ι u = g) ∧
        ∃ Dc : Lp ℂ 2 ν →L[ℂ] Lp ℂ 2 ν,
          Dc.IsPositive ∧
          (∀ g : Lp ℂ 2 ν, Dc g =
            ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) (R g)) +
            Complex.I • ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) (Q g))) ∧
          (∀ u : Lp ℝ 2 ν, Dc (ι u) = ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) u)) ∧
          (∀ g : Lp ℂ 2 ν, C (Dc g) = Dc (C g)) := by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  have hBase := CenteredDefectOperator.actual_centered_selfadjoint_defect
    hα hαβ hV hH hη hβη
  rcases hBase with ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hTs,hAll,
    q,hq,hTq,hqi,hzero,hD,hRest⟩
  obtain ⟨hι,hfixed,Dc,hpos,hformula,hintertwine,hconj⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator.exists_positive_complex_lift
      ν ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) hD
  refine ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,?_,hD,hι,hfixed,Dc,hpos,
    hformula,hintertwine,hconj⟩
  intro u
  exact (hAll u).2.2

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift.actual_positive_defect_complex_lift
