
open ProbabilityTheory.Kernel

namespace MeasureTheory

variable [NormedSpace ℝ E]

set_option backward.isDefEq.respectTransparency.types false in
omit [IsSFiniteKernel κ] in
@[fun_prop]
theorem StronglyMeasurable.integral_kernel ⦃f : β → E⦄
    (hf : StronglyMeasurable f) : StronglyMeasurable fun x ↦ ∫ y, f y ∂κ x := by
