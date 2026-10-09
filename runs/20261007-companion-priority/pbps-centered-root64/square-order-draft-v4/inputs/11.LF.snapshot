import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Order

open MeasureTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1000000

theorem positive_square_order
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (A B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hA : A.IsPositive) (hB : B.IsPositive)
    (hSquareOrder : (B*B-A*A).IsPositive) :
    (B-A).IsPositive := by
  letI : NormedSpace ℝ (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ) :=
    NormedSpace.restrictScalars ℝ ℂ (Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ)
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
  obtain ⟨_,_,Dc,hDc,hDf,hDi,_⟩ :=
    L2RealComplexOperator.exists_positive_complex_lift μ (B*B-A*A) hSquareOrder
  have hAi' (u : Lp ℝ 2 μ) : Ac (ι u)=ι (A u) := hAi u
  have hBi' (u : Lp ℝ 2 μ) : Bc (ι u)=ι (B u) := hBi u
  have hComplexDiff : Bc*Bc-Ac*Ac=Dc := by
    apply ContinuousLinearMap.ext
    intro g
    change Bc (Bc g) - Ac (Ac g)=Dc g
    rw [hBf g,hAf g,map_add,map_smul,map_add,map_smul,hBi,hBi,hAi,hAi,hDf g]
    simp only [ContinuousLinearMap.sub_apply,ContinuousLinearMap.mul_apply,map_sub,smul_sub]
    abel
  have hAcNonneg : 0 ≤ Ac := (ContinuousLinearMap.nonneg_iff_isPositive Ac).mpr hAc
  have hBcNonneg : 0 ≤ Bc := (ContinuousLinearMap.nonneg_iff_isPositive Bc).mpr hBc
  have hSqLe : Ac*Ac ≤ Bc*Bc := by
    apply (ContinuousLinearMap.le_def _ _).mpr
    rw [hComplexDiff]
    exact hDc
  have hLe : Ac ≤ Bc := by
    have h := CFC.sqrt_le_sqrt (Ac*Ac) (Bc*Bc) hSqLe
    simpa only [CFC.sqrt_mul_self Ac hAcNonneg,CFC.sqrt_mul_self Bc hBcNonneg] using h
  have hDiff : (Bc-Ac).IsPositive := (ContinuousLinearMap.le_def _ _).mp hLe
  letI : InnerProductSpace ℝ (Lp ℂ 2 μ) := InnerProductSpace.rclikeToReal ℂ (Lp ℂ 2 μ)
  let e : Lp ℝ 2 μ →ₗᵢ[ℝ] Lp ℂ 2 μ :=
    { toLinearMap := ι.toLinearMap, norm_map' := hNorm }
  have hInner (v w : Lp ℝ 2 μ) : RCLike.re (inner ℂ (ι v) (ι w))=inner ℝ v w := by
    rw [← real_inner_eq_re_inner]
    exact e.inner_map_map v w
  refine ⟨hB.isSymmetric.sub hA.isSymmetric,?_⟩
  intro u
  have h := hDiff.re_inner_nonneg_left (ι u)
  have hAction : (Bc-Ac) (ι u)=ι ((B-A) u) := by
    simp only [ContinuousLinearMap.sub_apply,hBi',hAi',map_sub]
  rw [hAction,hInner] at h
  exact h

end
end AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order
