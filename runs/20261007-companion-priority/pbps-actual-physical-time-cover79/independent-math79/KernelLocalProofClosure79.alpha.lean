import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let proofStem := "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover"
  let mut todo := #[`AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover]
  let mut seen : Array Name := #[]
  let mut externalDeps : Array Name := #[]
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if !seen.contains name then
      seen := seen.push name
      logInfo m!"LOCAL_PROOF_CONSTANT {name}"
      let some ci := env.find? name | throwError "Missing local proof constant"
      let some value := ci.value? true | throwError "Missing local proof value"
      for dep in value.getUsedConstants do
        if dep.toString.startsWith proofStem then
          todo := todo.push dep
        else if dep.toString.startsWith "AutoSamplingTheory." && !externalDeps.contains dep then
          externalDeps := externalDeps.push dep
          logInfo m!"EXTERNAL_ASTIS_DEPENDENCY {dep}"
  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"
