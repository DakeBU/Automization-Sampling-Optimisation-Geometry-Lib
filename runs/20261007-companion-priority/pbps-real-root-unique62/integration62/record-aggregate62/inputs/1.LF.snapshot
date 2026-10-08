import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot
import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

theorem actual_unique_positive_real_defect_root
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
          (∀ u : Lp ℝ 2 ν, ‖Γ u‖^2 = ‖u‖^2-‖T u‖^2) ∧
            ∀ Γ' : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
              Γ'.IsPositive →
              Γ'*Γ' = ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) → Γ'=Γ := by
  dsimp only
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,hAll,hD,Γ,hΓ,hΓSq,hEnergy⟩ :=
    RealDefectRoot.actual_positive_real_defect_root hα hαβ hV hH hη hβη
  refine ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,T,hTs,hAll,hD,Γ,hΓ,hΓSq,hEnergy,?_⟩
  intro Γ' hΓ' hΓ'Sq
  exact AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.positive_square_roots_unique
    _ Γ' Γ hΓ' hΓ (hΓ'Sq.trans hΓSq.symm)

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique.actual_unique_positive_real_defect_root
