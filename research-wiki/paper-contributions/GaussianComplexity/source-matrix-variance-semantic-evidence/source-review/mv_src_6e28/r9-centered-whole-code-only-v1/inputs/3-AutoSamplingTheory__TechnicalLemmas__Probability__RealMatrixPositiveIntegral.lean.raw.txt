import Mathlib.Algebra.Order.Star.Real
import Mathlib.Analysis.Convex.Integral
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.LinearAlgebra.Matrix.PosDef

/-! ASTIS-authored reusable background for positivity under expectation.
The full PSD cone geometry is proved here once. Concrete source applications
must derive integrability and AE positivity internally. Empty finite matrix
indices are permitted. This is not a printed generic theorem in the paper. -/

noncomputable section
open MeasureTheory
open scoped Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral

theorem integral_posSemidef
    {n Ω : Type*} [Fintype n] [DecidableEq n] [MeasurableSpace Ω]
    {μ : Measure Ω} [IsProbabilityMeasure μ]
    (f : Ω → Matrix n n ℝ) (hf : Integrable f μ)
    (hpos : ∀ᵐ ω ∂μ, Matrix.PosSemidef (f ω)) :
    Matrix.PosSemidef (∫ ω, f ω ∂μ)
:= by
  classical
  let M := Matrix n n ℝ
  have PSD_closed : IsClosed {A : M | A.PosSemidef} := by
    have hermitian_closed : IsClosed {A : M | A.IsHermitian} := by
      change IsClosed {A : M | star A = A}
      exact isClosed_eq continuous_star continuous_id
    have quadratic_closed (v : n → ℝ) :
        IsClosed {A : M | 0 ≤ dotProduct (star v) (Matrix.mulVec A v)} := by
      apply isClosed_le continuous_const
      change Continuous (fun A : M => ∑ a, star (v a) * ∑ b, A a b * v b)
      fun_prop
    convert hermitian_closed.inter (isClosed_iInter quadratic_closed) using 1
    ext A
    simp [Matrix.posSemidef_iff_dotProduct_mulVec]
  have PSD_convex : Convex ℝ {A : M | A.PosSemidef} := by
    intro A hA B hB a b ha hb hab
    exact (hA.smul ha).add (hB.smul hb)
  exact PSD_convex.integral_mem PSD_closed hpos hf

end AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
