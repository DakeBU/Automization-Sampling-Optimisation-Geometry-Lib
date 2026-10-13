import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

theorem actual_positive_real_defect_root
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
        ∃ Γ : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
          Γ.IsPositive ∧ Γ*Γ = ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) ∧
          ∀ u : Lp ℝ 2 ν, ‖Γ u‖^2 = ‖u‖^2-‖T u‖^2 := by
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
  obtain ⟨Γ,hΓ,hΓSq,hEnergy⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot.exists_positive_real_square_root
      ν ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) hD
  refine ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,?_,hD,Γ,hΓ,hΓSq,?_⟩
  · intro u
    exact (hAll u).2.2
  · intro u
    rw [hEnergy]
    simp only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.one_apply,
      ContinuousLinearMap.mul_apply, inner_sub_left]
    have hs : inner ℝ (T (T u)) u = inner ℝ (T u) (T u) := hTs.isSymmetric (T u) u
    rw [hs,real_inner_self_eq_norm_sq,real_inner_self_eq_norm_sq]

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot.actual_positive_real_defect_root
