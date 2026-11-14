import Tests.GaussianComplexityFixedSpectrumRadialFourthMoment
import Lean
open Lean Elab Command
set_option maxRecDepth 1000000
set_option maxHeartbeats 0
run_elab do
  let env := (← getEnv).setExporting false
  let modules := #[`AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment,
    `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment,
    `Tests.GaussianComplexityFixedSpectrumRadialFourthMoment]
  let mut rows : Array Json := #[]
  for (n, ci) in env.constants.toList do
    let mod := match env.getModuleIdxFor? n with
      | some i => env.header.moduleNames[i]!
      | none => Name.anonymous
    if modules.contains mod then
      let ax ← collectAxioms n
      let body := ci.value? (allowOpaque := true)
      let kind := match ci with
        | .axiomInfo _ => "axiom" | .thmInfo _ => "theorem"
        | .defnInfo _ => "definition" | .opaqueInfo _ => "opaque"
        | .inductInfo _ => "inductive" | .ctorInfo _ => "constructor"
        | .recInfo _ => "recursor" | .quotInfo _ => "quotient"
      rows := rows.push <| Json.mkObj [
        ("name", toJson n.toString), ("module", toJson mod.toString),
        ("kind", toJson kind), ("unsafe", toJson ci.isUnsafe),
        ("partial", toJson ci.isPartial),
        ("type", toJson (reprStr ci.type)),
        ("body", toJson (body.map reprStr)),
        ("typeConstants", toJson (ci.type.getUsedConstants.map Name.toString)),
        ("bodyConstants", toJson ((body.map Expr.getUsedConstants).getD #[] |>.map Name.toString)),
        ("axioms", toJson (ax.map Name.toString))]
  liftM <| IO.FS.writeFile "/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261111/r4_native_7f24/local-private/declaration-environment.v2.json" (Json.arr rows |>.pretty)
