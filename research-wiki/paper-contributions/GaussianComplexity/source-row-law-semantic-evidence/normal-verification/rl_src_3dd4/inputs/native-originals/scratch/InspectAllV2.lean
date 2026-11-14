import Tests.GaussianComplexityFixedSpectrumSourceRowLaw
import Lean
open Lean Elab Command Meta
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.universes true
set_option pp.explicit true
set_option pp.proofs true
set_option pp.deepTerms true
set_option pp.maxSteps 100000000

private def modules : List String := ["AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw", "AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym", "AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity", "AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential", "Tests.GaussianComplexityFixedSpectrumSourceRowLaw"]
private def moduleOf (env : Environment) (n : Name) : String :=
  match env.getModuleIdxFor? n with
  | none => "NO_MODULE"
  | some idx => env.header.moduleNames[idx.toNat]!.toString
private def owned (env : Environment) (n : Name) : Bool := modules.contains (moduleOf env n)
private partial def reach (env : Environment) (todo : List Name) (seen : NameSet := {}) : NameSet :=
  match todo with
  | [] => seen
  | n :: rest =>
    if seen.contains n then reach env rest seen else
    let seen := seen.insert n
    match env.find? n with
    | none => reach env rest seen
    | some c => reach env (c.getUsedConstantsAsSet.toList ++ rest) seen
private def kind (c : ConstantInfo) : String :=
  match c with
  | .thmInfo _ => "theorem"
  | .defnInfo _ => "definition"
  | .opaqueInfo _ => "opaque"
  | .axiomInfo _ => "axiom"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient"
run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let allowed := [`propext, `Classical.choice, `Quot.sound]
  let mut rows : Array Json := #[]
  for (n,c) in env.constants.toList do
    if owned env n then
      unless !c.type.hasLooseBVars && !c.type.hasFVar && !c.type.hasMVar do
        throwError "Open owned type: {n}"
      let some body := c.value? true | throwError "Missing owned body: {n}"
      unless !body.hasLooseBVars && !body.hasFVar && !body.hasMVar do
        throwError "Open owned body: {n}"
      let axioms ← collectAxioms n
      unless axioms.all (fun a => allowed.contains a) do
        throwError "Unexpected owned axiom closure {n}: {axioms}"
      let all := c.getUsedConstantsAsSet.toList
      let closure := (reach env [n]).toList
      let typ ← liftTermElabM <| return (← ppExpr c.type).pretty
      let val ← liftTermElabM <| return (← ppExpr body).pretty
      rows := rows.push <| Json.mkObj [
        ("name",toJson n.toString),("module",toJson (moduleOf env n)),("kind",toJson (kind c)),
        ("type",toJson typ),("body",toJson val),
        ("direct",toJson (all.map Name.toString)),
        ("direct_owned",toJson ((all.filter (owned env)).map Name.toString)),
        ("transitive_owned",toJson ((closure.filter (owned env)).map Name.toString)),
        ("axioms",toJson (axioms.toList.map Name.toString)),
        ("type_closed",toJson true),("body_closed",toJson true)]
  liftIO <| IO.FS.writeFile "/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261112/rl_native_52e9/native-all-bodies-v2.json" (Json.pretty (toJson rows))
  logInfo m!"NATIVE_MODULE_OWNED_FULL_TYPES_BODIES_AXIOMS_EXPORTED {rows.size}"
#check @MeasureTheory.integral_map
