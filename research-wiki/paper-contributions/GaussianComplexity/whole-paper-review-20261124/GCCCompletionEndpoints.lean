import GCCIntrinsicSupport

/-! Two checks using raw matrix data at both ends of the rank interval. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

attribute [local instance] matrixMeasurable matrixBorel matrixSecond

theorem completion_zero_pair (N : ℕ) : completionKernel N (0,0) = orthogonalHaar N := by
  have hb : front N 0 = ⊥ := by
    apply bot_unique
    intro x hx
    change x = 0
    ext i
    exact hx i (Nat.zero_le _)
  have hp : projectionMatrix (front N 0) = 0 := by
    simp [projectionMatrix,hb,Submodule.starProjection_bot]
  have he : observationOf (BlockFrame.initial N) = (0,0) := by
    change (_ * projectionMatrix (front N 0) * _,_ * projectionMatrix (front N 0) * _) = _
    simp [hp]
  rw [← he]
  exact completion_initial N

theorem completion_identity_projector {N : ℕ} (A : O N) :
    completionKernel N (1,A.val) = Measure.dirac A := by
  have ht : front N N = ⊤ := by
    apply top_unique
    intro x _ i hi
    omega
  have hp : projectionMatrix (front N N) = 1 := by
    simp [projectionMatrix,ht,Submodule.starProjection_top']
  let F : BlockFrame N 0 := ⟨N,Nat.zero_add _,1,A⟩
  have he : observationOf F = (1,A.val) := by
    change ((1 : O N).val * projectionMatrix (front N N) * (1 : O N)⁻¹.val,
      A.val * projectionMatrix (front N N) * (1 : O N)⁻¹.val) = _
    simp [hp]
  have hr : F.realize 1 ∈ range F.realize := mem_range_self _
  rw [range_realize_eq_compatible] at hr
  change (F.realize 1).val * (observationOf F).1 = (observationOf F).2 at hr
  have ha : F.realize 1 = A := Subtype.ext (by simpa only [he,mul_one] using hr)
  rw [← he,completion_full,ha]

#print axioms completion_zero_pair
#print axioms completion_identity_projector
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
