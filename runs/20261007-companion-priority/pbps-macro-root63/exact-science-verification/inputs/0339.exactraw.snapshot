import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
open MeasureTheory
open scoped InnerProductSpace
set_option backward.isDefEq.respectTransparency false
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {f : E → ℝ} (hf : ContDiff ℝ 1 f) (y x : E) :
    HasFDerivAt (fun z : E => f ((2:ℝ) • x-z))
      (-fderiv ℝ f ((2:ℝ) • x-y)) y := by
  have ha := (hasFDerivAt_id (𝕜 := ℝ) y).const_sub ((2:ℝ) • x)
  have ho := (hf.differentiable_one ((2:ℝ) • x-y)).hasFDerivAt.comp y ha
  convert ho using 1 <;> first | rfl | (ext v; simp)
