import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian

open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian

#check @halfRayleighGradientExtension
#check @halfRayleighTangentHessian
#check @sphere_half_rayleigh_gradient_pairing
#check @sphere_half_rayleigh_tangent_hessian_apply
#check @sphere_half_rayleigh_second_order_stationary_min

#print halfRayleighGradientExtension
#print halfRayleighTangentHessian

open Lean in
run_cmd do
  let env ← getEnv
  let expected := #[
    (`AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian.sphere_half_rayleigh_gradient_pairing,
      `AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleigh.sphere_rayleigh_characterization),
    (`AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian.sphere_half_rayleigh_second_order_stationary_min,
      `AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian.sphere_half_rayleigh_tangent_hessian_apply)]
  for (src, dst) in expected do
    let some body := (env.find? src).bind (fun i => i.value? (allowOpaque := true))
      | throwError "Missing body for {src}"
    unless body.getUsedConstants.contains dst do
      throwError "Expected proof-body occurrence {src} → {dst}"
    logInfo m!"Direct proof-body occurrence: {src} → {dst}"
  let src := `AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian.sphere_half_rayleigh_tangent_hessian_apply
  let some body := (env.find? src).bind (fun i => i.value? (allowOpaque := true))
    | throwError "Missing body for {src}"
  let some derivative := body.getUsedConstants.find? fun k =>
      k.toString.startsWith "_private.AutoSamplingTheory.TechnicalLemmas.Geometry.SphereRayleighHessian." &&
        k.toString.endsWith ".half_rayleigh_gradient_extension_derivative"
    | throwError "Missing actual derivative helper in Hessian proof body"
  logInfo m!"Private proof-body occurrence: {src} → {derivative}"
