import Tests.StandardizedRGOKLFisher
import Mathlib.Util.PrintSorries

open Lean Elab Command

run_elab do
  let roots := #[
    ``AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLFisher.standardized_rgo_unique_prox_and_kl_le_fisher,
    ``Tests.StandardizedRGOKLFisher.actual_fixed_posterior,
    ``Tests.StandardizedRGOKLFisher.actual_variable_step_family,
    ``Tests.StandardizedRGOKLFisher.rank_zero_actual_canonical_kl]
  let localName := fun n : Name =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory." || s.startsWith "Tests." ||
      (s.splitOn ".AutoSamplingTheory.").length > 1 ||
      (s.splitOn ".Tests.").length > 1
  let env ← getEnv
  let mut todo := roots.toList
  let mut seen : NameSet := {}
  while !todo.isEmpty do
    let n := todo.head!
    todo := todo.tail!
    unless seen.contains n do
      seen := seen.insert n
      if let some info := env.find? n then
        let value := match info with
          | .defnInfo v => some v.value
          | .thmInfo v => some v.value
          | .opaqueInfo v => some v.value
          | _ => none
        let kind := match info with
          | .axiomInfo _ => "axiom"
          | .defnInfo _ => "definition"
          | .thmInfo _ => "theorem"
          | .opaqueInfo _ => "opaque"
          | _ => "type-or-instance"
        let deps := info.type.getUsedConstants ++
          (match value with | some v => v.getUsedConstants | none => #[])
        let direct := deps.filter localName
        logInfo m!"ASTIS_REACHABLE|{n}|{kind}|{String.intercalate ";" (direct.toList.map Name.toString)}"
        if n == roots[0]! then
          logInfo m!"PUBLIC_DIRECT_CONSTANTS|{String.intercalate ";" (deps.toList.map Name.toString)}"
        for d in direct do
          todo := d :: todo

#print sorries AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLFisher.standardized_rgo_unique_prox_and_kl_le_fisher
#print sorries Tests.StandardizedRGOKLFisher.rank_zero_actual_canonical_kl

#print axioms AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLFisher.standardized_rgo_unique_prox_and_kl_le_fisher
#print axioms Tests.StandardizedRGOKLFisher.actual_fixed_posterior
#print axioms Tests.StandardizedRGOKLFisher.actual_variable_step_family
#print axioms Tests.StandardizedRGOKLFisher.rank_zero_actual_canonical_kl

