import AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

#check @AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath.ordered_heat_bath_invariant_not_reversible
#print axioms AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath.ordered_heat_bath_invariant_not_reversible

-- Bounded actual proof-body evidence, not theorem implication or full closure.
open Lean in
run_cmd do
  let env ← getEnv
  let root := `AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath.ordered_heat_bath_invariant_not_reversible
  let some body := (env.find? root).bind (fun i => i.value? (allowOpaque := true))
    | throwError "Missing compiled witness body"
  unless body.getUsedConstants.contains `ProbabilityTheory.Kernel.Invariant.comp do
    throwError "Missing actual invariant-composition call"
  let some fiber := body.getUsedConstants.find? (fun n => n.toString.endsWith ".reversible_of_fiber")
    | throwError "Missing actual fiber reversibility call"
  let some fiberBody := (env.find? fiber).bind (fun i => i.value? (allowOpaque := true))
    | throwError "Missing compiled fiber reversibility body"
  unless fiberBody.getUsedConstants.contains
      `AutoSamplingTheory.TechnicalLemmas.Probability.KernelReversibility.isReversible_of_singleton_balance do
    throwError "Missing owned atomic-balance call"
  logInfo "Compiled witness calls Mathlib Invariant.comp and, through its private fiber proof, ASTIS atomic balance."
