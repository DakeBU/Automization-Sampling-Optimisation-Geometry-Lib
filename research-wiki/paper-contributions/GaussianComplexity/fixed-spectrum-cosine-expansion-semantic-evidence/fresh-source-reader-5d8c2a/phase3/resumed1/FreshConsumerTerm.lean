import Tests.GaussianComplexityFixedSpectrumCosineExpansion
import Lean

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let targets := env.constants.toList.filter fun (n, _) =>
    n.toString.startsWith "_private.Tests.GaussianComplexityFixedSpectrumCosineExpansion." &&
    n.toString.endsWith ".actual_inverse_grid_cosine_series"
  unless targets.length == 1 do throwError "Consumer declaration count mismatch"
  for (n, ci) in targets do
    let .thmInfo ti := ci | throwError "Consumer not a theorem"
    logInfo m!"CONSUMER_COMPILED_TERM {n}\n{ti.value}"
