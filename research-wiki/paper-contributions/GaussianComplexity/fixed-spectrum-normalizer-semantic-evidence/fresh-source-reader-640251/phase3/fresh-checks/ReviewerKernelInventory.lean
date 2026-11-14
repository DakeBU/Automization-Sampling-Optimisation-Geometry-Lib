import Tests.GaussianComplexityFixedSpectrumNormalizer
open Lean in
run_cmd do
  let env ← getEnv
  let producer := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer.actual_normalizing_integral
  let producerEntries := env.constants.toList.filter fun (name, _) =>
    name.toString.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumNormalizer."
  let consumerEntries := env.constants.toList.filter fun (name, _) =>
    name.toString.startsWith "_private.Tests.GaussianComplexityFixedSpectrumNormalizer."
  unless producerEntries.length == 1 do throwError "Unexpected production declaration inventory"
  unless consumerEntries.length == 1 do throwError "Unexpected private Test declaration inventory"
  let consumer := consumerEntries.head!.1
  unless consumer.toString.endsWith ".actual_gaussian_density_consumer" do throwError "Unexpected Test consumer"
  let expected := [
    `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility.actual_precision_admissible,
    `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDeterminant.actual_precision_det,
    `AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity.multivariateGaussian_eq_withDensity_of_posDef]
  for (name, parents) in [(producer, expected), (consumer, producer :: expected)] do
    let some info := env.find? name | throwError "Missing actual declaration"
    let some proof := info.value? (allowOpaque := true) | throwError "Missing actual proof"
    let used := proof.getUsedConstants.toList.filter fun n => n.toString.startsWith "AutoSamplingTheory."
    unless used.length == parents.length && parents.all used.contains do
      throwError m!"Wrong direct ASTIS proof-term inventory: {name}: {used}"
    logInfo m!"REVIEWER_ACTUAL_DECL {name}"
    for dep in used do logInfo m!"REVIEWER_DIRECT_ASTIS_PARENT {dep}"
  logInfo "REVIEWER_INVENTORY_PASS: one production theorem, one private Test theorem, exactly 3/4 direct ASTIS proof parents."
