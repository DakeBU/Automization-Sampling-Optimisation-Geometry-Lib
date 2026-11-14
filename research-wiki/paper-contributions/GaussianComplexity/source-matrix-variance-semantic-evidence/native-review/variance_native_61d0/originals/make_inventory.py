from runner import *
p=json.loads((OUT/'preparation.json').read_text());c=Path(p['candidate'])
seal=json.loads((OUT/'inputs/research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json').read_text())
head='''import Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance
import Lean
open Lean Elab Command Meta MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder
set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option pp.universes true
set_option pp.explicit true
set_option pp.fullNames true
'''
for tag,key in [('P','producer'),('T','actual_private_consumer')]:
 sig=seal[key]['signature']; params,prop=sig.split(':\n',1)
 head+=f'\ndef {tag}Literal : Prop := ∀ {params.strip()},\n{prop}\n'
 head+=f'\ndef {tag}ZeroLiteral : Prop := ∀ {{d : ℕ}} (hq : 2 * 0 + 1 < d),\n'+prop.replace('q','0')+'\n'
code=r'''
private def refs (e : Expr) : Array String :=
  (e.getUsedConstants.toArray.map Name.toString).qsort (· < ·)

private def ownModule (env : Environment) (n : Name) : String :=
  match env.getModuleIdxFor? n with
  | some idx => env.header.moduleNames[idx.toNat]!.toString
  | none => "CURRENT"

private def record (j : Json) : CommandElabM Unit := do
  liftIO <| IO.println j.compress

elab "#independentInventory" : command => do
  let env ← getEnv
  let names := env.constants.toList.filterMap fun (n, _) =>
    let m := ownModule env n
    if m.startsWith "AutoSamplingTheory." || m.startsWith "Tests." then some n else none
  let names := names.toArray.qsort (fun a b => a.toString < b.toString)
  let mut roots : Array Name := #[]
  for n in names do
    if n.toString.endsWith ".actual_source_truncated_matrix_second_moments" ||
       n.toString.endsWith ".actual_source_centered_variance_bounds" then
      roots := roots.push n
  unless roots.size == 2 do throwError "expected precisely two real roots, got {roots}"
  for n in names do
    let ci := env.find? n |>.get!
    let v := ci.value?
    unless !ci.type.hasFVar && !ci.type.hasMVar && !ci.type.hasLooseBVars do
      throwError "open type {n}"
    let mut checked := false
    if let some value := v then
      unless !value.hasFVar && !value.hasMVar && !value.hasLooseBVars do
        throwError "open body {n}"
      -- Kernel receives the actual complete value as a typed let, not an opaque reference.
      let clone := Name.str `IndependentKernelRechecks n.toString
      let body := Expr.letE `actual_value ci.type value (.bvar 0) false
      match ci with
      | .thmInfo _ => addDecl <| .thmDecl { name := clone, levelParams := ci.levelParams, type := ci.type, value := body }
      | .defnInfo d => addDecl <| .defnDecl { name := clone, levelParams := ci.levelParams, type := ci.type, value := body, hints := .opaque, safety := d.safety }
      | .opaqueInfo _ => addDecl <| .opaqueDecl { name := clone, levelParams := ci.levelParams, type := ci.type, value := body, isUnsafe := false }
      | _ => throwError "unexpected value-bearing kind {n}"
      checked := true
    let axioms ← collectAxioms n
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "nonstandard axiom {ax} in {n}"
    record <| Json.mkObj [
      ("record", toJson "declaration"), ("name",toJson n.toString),
      ("module",toJson (ownModule env n)),
      ("kind",toJson (match ci with | .thmInfo _ => "theorem" | .defnInfo _ => "definition" | .opaqueInfo _ => "opaque" | .axiomInfo _ => "axiom" | .ctorInfo _ => "constructor" | .recInfo _ => "recursor" | .inductInfo _ => "inductive" | .quotInfo _ => "quotient")),
      ("levelParams",toJson (ci.levelParams.map Name.toString)),
      ("typeExpr",toJson (reprStr ci.type)), ("valueExpr",toJson (v.map reprStr)),
      ("typeConstants",toJson (refs ci.type)), ("valueConstants",toJson (v.map refs |>.getD #[])),
      ("closed",toJson true), ("kernel_actual_typed_let_checked",toJson checked),
      ("axioms",toJson (axioms.map Name.toString))]
  for n in roots do
    let ci := env.find? n |>.get!
    let isP := n.toString.endsWith ".actual_source_truncated_matrix_second_moments"
    let literal := if isP then `PLiteral else `TLiteral
    let zeroLiteral := if isP then `PZeroLiteral else `TZeroLiteral
    let fullType := (env.find? literal |>.get!).value!.instantiateLevelParams [] []
    let zeroType := (env.find? zeroLiteral |>.get!).value!.instantiateLevelParams [] []
    let actualValue := ci.value!
    let fullName := if isP then `IndependentSealChecks.PUniversal else `IndependentSealChecks.TUniversal
    addDecl <| .thmDecl { name := fullName, levelParams := [], type := fullType, value := actualValue }
    let zeroValue ← liftTermElabM <| forallTelescopeReducing zeroType fun xs _ => do
      unless xs.size == 2 do throwError "q0 expects d and hq"
      mkLambdaFVars xs (mkApp3 actualValue xs[0]! (mkNatLit 0) xs[1]!)
    let zeroName := if isP then `IndependentSealChecks.PZero else `IndependentSealChecks.TZero
    addDecl <| .thmDecl { name := zeroName, levelParams := [], type := zeroType, value := zeroValue }
    record <| Json.mkObj [("record",toJson "literal-root-value-check"),("actual_name",toJson n.toString),("universal",toJson true),("q0",toJson true)]

#independentInventory
'''
(c/'IndependentInventory.lean').write_text(head+code)
run('inventory-kernel-v1',[p['lean'],'IndependentInventory.lean'],c,p['env'])
