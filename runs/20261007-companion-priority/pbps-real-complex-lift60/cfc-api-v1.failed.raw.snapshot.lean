import AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

open MeasureTheory
open scoped ENNReal

/- The complex CFC API is genuinely available after the positive L2 lift.
   This checks a complex square root only. Preservation of the real fixed
   subspace and descent to the paper's real Gamma remain separate obligations. -/
example {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive) :
    let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
    ∃ Dc : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ,
      Dc.IsPositive ∧ (∀ u : Lp ℝ 2 μ, Dc (ι u) = ι (D u)) ∧
      ∃ Rc : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ, 0 ≤ Rc ∧ Rc*Rc = Dc := by
  dsimp only
  obtain ⟨hι,hfixed,Dc,hpos,hformula,hintertwine,hconj⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator.exists_positive_complex_lift μ D hD
  have hnonneg : 0 ≤ Dc := (ContinuousLinearMap.nonneg_iff_isPositive Dc).mpr hpos
  exact ⟨Dc,hpos,hintertwine,CFC.sqrt Dc,CFC.sqrt_nonneg Dc,CFC.sqrt_mul_sqrt_self Dc hnonneg⟩

#check AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift.actual_positive_defect_complex_lift
