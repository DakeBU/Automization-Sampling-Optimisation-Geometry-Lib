import Tests.GaussianComplexityFixedSpectrumSourceGramRealization
open Lean
run_cmd do
  let env ← getEnv
  for n in [`LinearMap.map_sum, `LinearMap.map_smul, `map_sum, `map_smul] do
    logInfo m!"ACTUAL_DECLARATION_NAME {n}: {env.contains n}"
