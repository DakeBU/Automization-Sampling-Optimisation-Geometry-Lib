import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

open MeasureTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

theorem positive_square_roots_unique
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (A B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hA : A.IsPositive) (hB : B.IsPositive) (hSq : A*A=B*B) :
    A=B := by
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
  obtain ⟨hNorm,_,Ac,hAc,hAf,hAi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ A hA
  obtain ⟨_,_,Bc,hBc,hBf,hBi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ B hB
  have hReal (u : Lp ℝ 2 μ) : A (A u) = B (B u) :=
    congrArg (fun D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ => D u) hSq
  have hComplexSquare : Ac*Ac = Bc*Bc := by
    apply ContinuousLinearMap.ext
    intro g
    change Ac (Ac g) = Bc (Bc g)
    calc
      Ac (Ac g) = ι (A (A (R g))) + Complex.I • ι (A (A (Q g))) := by
        rw [hAf g, map_add, map_smul, hAi, hAi]
      _ = ι (B (B (R g))) + Complex.I • ι (B (B (Q g))) := by
        rw [hReal (R g),hReal (Q g)]
      _ = Bc (Bc g) := by rw [hBf g, map_add, map_smul, hBi, hBi]
  have hAcNonneg : 0 ≤ Ac := (ContinuousLinearMap.nonneg_iff_isPositive Ac).mpr hAc
  have hBcNonneg : 0 ≤ Bc := (ContinuousLinearMap.nonneg_iff_isPositive Bc).mpr hBc
  have hSame : Ac = Bc :=
    (CFC.sqrt_unique hComplexSquare hAcNonneg).symm.trans (CFC.sqrt_unique rfl hBcNonneg)
  let e : Lp ℝ 2 μ →ₗᵢ[ℝ] Lp ℂ 2 μ :=
    { toLinearMap := ι.toLinearMap
      norm_map' := hNorm }
  apply ContinuousLinearMap.ext
  intro u
  apply e.injective
  change ι (A u) = ι (B u)
  rw [← hAi u, ← hBi u, hSame]

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique.positive_square_roots_unique
