import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

open MeasureTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

theorem positive_square_commutation
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (G D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hG : G.IsPositive) (hD : D.IsPositive)
    (hCommute : Commute (G*G) D) : Commute G D
 := by
  letI := IsStarNormal.instNonUnitalContinuousFunctionalCalculus
    (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  letI : NonUnitalContinuousFunctionalCalculus ℂ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsStarNormal :=
    NonUnitalClosedEmbeddingContinuousFunctionalCalculus.toNonUnitalContinuousFunctionalCalculus
  letI : NonUnitalContinuousFunctionalCalculus ℝ
      (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) IsSelfAdjoint :=
    IsSelfAdjoint.instNonUnitalContinuousFunctionalCalculus
      (A := Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
  let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
  let R : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
  let Q : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
  obtain ⟨hNorm,_,Gc,hGc,hGf,hGi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ G hG
  obtain ⟨_,_,Dc,hDc,hDf,hDi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ D hD
  have hReal (u : Lp ℝ 2 μ) : G (G (D u)) = D (G (G u)) :=
    congrArg (fun A : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ => A u) hCommute.eq
  have hComplex : Commute (Gc*Gc) Dc := by
    apply ContinuousLinearMap.ext
    intro g
    change Gc (Gc (Dc g)) = Dc (Gc (Gc g))
    calc
      Gc (Gc (Dc g)) = ι (G (G (D (R g)))) + Complex.I • ι (G (G (D (Q g)))) := by
        rw [hDf g, map_add, map_smul, hGi, hGi, map_add, map_smul, hGi, hGi]
      _ = ι (D (G (G (R g)))) + Complex.I • ι (D (G (G (Q g)))) := by
        rw [hReal (R g),hReal (Q g)]
      _ = Dc (Gc (Gc g)) := by
        rw [hGf g,map_add,map_smul,hGi,hGi,map_add,map_smul,hDi,hDi]
  have hGcNonneg : 0 ≤ Gc := (ContinuousLinearMap.nonneg_iff_isPositive Gc).mpr hGc
  have hRoot : CFC.sqrt (Gc*Gc)=Gc := CFC.sqrt_unique rfl hGcNonneg
  have hLift : Commute Gc Dc := by
    have h := hComplex.cfcₙ_nnreal NNReal.sqrt
    change Commute (CFC.sqrt (Gc*Gc)) Dc at h
    rwa [hRoot] at h
  let e : Lp ℝ 2 μ →ₗᵢ[ℝ] Lp ℂ 2 μ :=
    { toLinearMap := ι.toLinearMap, norm_map' := hNorm }
  apply ContinuousLinearMap.ext
  intro u
  apply e.injective
  change ι (G (D u))=ι (D (G u))
  rw [← hGi (D u), ← hDi u, ← hDi (G u), ← hGi u]
  exact congrArg (fun A : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ => A (ι u)) hLift.eq

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute.positive_square_commutation
