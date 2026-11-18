import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereAntipodalGenerator

open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereAntipodalGenerator

-- An even ambient observable has an even extrinsic sphere-Laplacian expression.
-- This exercises the reflected point and reflected test together.
example {I : Type*} [Fintype I] [DecidableEq I]
    (f : EuclideanSpace ℝ I → ℝ) (hEven : ∀ x, f (-x) = f x)
    (w : EuclideanSpace ℝ I) : sphereLaplacian f (-w) = sphereLaplacian f w := by
  have hfun : (fun x => f (-x)) = f := funext hEven
  simpa only [hfun] using (sphere_differential_operators_comp_neg f w).2.symm

#check @sphere_differential_operators_comp_neg
#print axioms sphere_differential_operators_comp_neg
