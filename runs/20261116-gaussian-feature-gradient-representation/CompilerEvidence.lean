import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient

open Lean

set_option pp.proofs false
set_option pp.fullNames false
set_option pp.universes false
set_option pp.funBinderTypes true
set_option format.width 120
set_option pp.maxSteps 1000000

#eval IO.println "BEGIN_NEW_TARGET"
#check @AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialFeatureGradient.gaussian_polynomial_joint_feature_gradient_representation
#eval IO.println "END_NEW_TARGET"

#eval IO.println "BEGIN_MATHLIB_DEFINITION_CONTEXT"
#print MeasureTheory.MemLp
#print MeasureTheory.AEEqFun
#print MeasureTheory.Lp
#print MeasureTheory.MemLp.toLp
#check @MeasureTheory.MemLp.coeFn_toLp
#check @MeasureTheory.L2.inner_def
#print MeasureTheory.integral
#print HasFDerivAtFilter
#print HasFDerivAt
#print HasGradientAtFilter
#print HasGradientAt
#print gradient
#print ContinuousLinearMap.adjoint
#check @ContinuousLinearMap.adjoint_inner_right
#print ProbabilityTheory.stdGaussian
#eval IO.println "END_MATHLIB_DEFINITION_CONTEXT"

#eval IO.println "BEGIN_AXIOMS"
#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialFeatureGradient.gaussian_polynomial_joint_feature_gradient_representation
#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient.gaussian_polynomial_joint_potential_projected_gradient_transport_control
#eval IO.println "END_AXIOMS"

run_cmd do
  let env ← getEnv
  let old := `AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient.gaussian_polynomial_joint_potential_projected_gradient_transport_control
  let new := `AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialFeatureGradient.gaussian_polynomial_joint_feature_gradient_representation
  let some oldInfo := env.find? old | throwError "Old target missing"
  let some newInfo := env.find? new | throwError "New target missing"
  let oldUses := (oldInfo.value! (allowOpaque := true)).getUsedConstants
  let newUses := (newInfo.value! (allowOpaque := true)).getUsedConstants
  unless oldUses.contains new do throwError "Old theorem does not directly consume the new representation"
  logInfo m!"OLD_CONSUMER_DIRECTLY_USES_NEW_PRODUCER: {oldUses.contains new}"
  let law := `AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient.quadratic_feature_law_gradient_angular_transport_control
  unless oldUses.contains law do throwError "Old theorem does not directly consume the law-gradient producer"
  logInfo m!"OLD_CONSUMER_DIRECTLY_USES_LAW_GRADIENT: {oldUses.contains law}"
  for parent in [
      `AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation.actual_gaussian_polynomial_ridge_L2_derivative_bounds,
      `AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging.gaussian_polynomial_parameter_average_L2,
      `AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient.quadratic_feature_potential_tangent_gradient] do
    unless newUses.contains parent do throwError m!"Expected actual producer dependency missing: {parent}"
    logInfo m!"NEW_PRODUCER_DIRECT_DEPENDENCY: {parent}"
