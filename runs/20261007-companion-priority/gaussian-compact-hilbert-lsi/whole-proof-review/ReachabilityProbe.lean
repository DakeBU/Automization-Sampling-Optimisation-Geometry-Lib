import Tests.GaussianCompactHilbertLogSobolev
import Mathlib.Util.PrintSorries

open Lean Elab Command

run_elab do
  let roots := #[
    ``AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev,
    ``Tests.GaussianCompactHilbertLogSobolev.zero_arbitrary_hilbert,
    ``Tests.GaussianCompactHilbertLogSobolev.negative_constant_rank_zero,
    ``Tests.GaussianCompactHilbertLogSobolev.actual_posterior_compact_lsi]
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

#print sorries AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev
#print sorries Tests.GaussianCompactHilbertLogSobolev.actual_posterior_compact_lsi
