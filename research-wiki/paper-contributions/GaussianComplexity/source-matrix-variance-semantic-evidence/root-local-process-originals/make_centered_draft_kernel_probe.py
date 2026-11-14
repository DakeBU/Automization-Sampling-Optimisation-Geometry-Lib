"""Kernel-apply the actual local centered draft to the original complete T Prop."""
from pathlib import Path
import hashlib
import json
W = Path(__file__).resolve().parent
signature = (W / 'consumer-signature.original.txt').read_text()
binders, result = signature.split(' :\n', 1)
code = (W / 'CenteredVarianceDraft.lean').read_text()
code += '\nopen Lean\ndef ExpectedCentered : Prop := ∀ ' + binders + ',\n' + result
code += r'''
run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let roots := env.constants.toList.filter (fun (n, _) =>
    n.toString.endsWith ".actual_source_centered_variance_bounds")
  unless roots.length == 1 do throwError "Actual centered private root not unique: {roots.map Prod.fst}"
  let (target, ci) := roots.head!
  match ci with
  | .thmInfo _ => pure ()
  | _ => throwError "Actual root is not a theorem"
  let some proof := ci.value? true | throwError "Actual proof absent"
  let isOwned := fun (n : Name) => target.isPrefixOf n
  let owned := env.constants.toList.filter fun (n, _) => isOwned n
  let some expected := env.find? `ExpectedCentered | throwError "Missing exact literal Prop"
  let some literal := expected.value? true | throwError "Missing exact literal body"
  unless ci.levelParams == [] && expected.levelParams == [] do
    throwError "Unexpected universe parameters"
  Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
    name := `ActualCenteredSealedTypeCheck
    levelParams := []
    type := mkConst `ExpectedCentered
    value := mkConst target
  }
  logInfo m!"ACTUAL_CENTERED_PRIVATE_ROOT {target}"
  logInfo m!"ACTUAL_CENTERED_SEALED_PROP_KERNEL_APPLICATION_PASS"
  logInfo m!"ACTUAL_CENTERED_RAW_LITERAL_EXPR_EQUALITY {ci.type == literal}"
  let mut pending := proof.getUsedConstants.toList
  let mut seen : NameSet := {}
  let mut parents : NameSet := {}
  while !pending.isEmpty do
    let u := pending.head!
    pending := pending.tail!
    unless seen.contains u do
      seen := seen.insert u
      if isOwned u then
        let some aci := env.find? u | throwError "Missing owned provider {u}"
        let some ap := aci.value? true | throwError "Missing owned body {u}"
        pending := ap.getUsedConstants.toList ++ aci.type.getUsedConstants.toList ++ pending
      else if u.toString.startsWith "AutoSamplingTheory." then
        parents := parents.insert u
  let allowed := [`propext, `Classical.choice, `Quot.sound]
  for (n, ci) in owned do
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Owned provider not theorem: {n}"
    let some body := ci.value? true | throwError "Owned proof absent: {n}"
    unless !ci.type.hasLooseBVars && !ci.type.hasFVar && !ci.type.hasMVar &&
        !body.hasLooseBVars && !body.hasFVar && !body.hasMVar do
      throwError "Unclosed owned theorem type/body {n}"
    unless n == target || seen.contains n do throwError "Unreachable owned provider {n}"
    let ax ← Lean.collectAxioms n
    unless ax.all allowed.contains do throwError "Unexpected axioms {n}: {ax}"
    logInfo m!"ACTUAL_CENTERED_OWNED_CLOSED_REACHABLE {n} axioms={ax}"
  let required := [
    `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef,
    `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments,
    `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means]
  unless parents.toList.length == required.length && required.all parents.contains do
    throwError "Unexpected actual ASTIS parent boundary: {parents.toList}"
  logInfo m!"ACTUAL_CENTERED_ASTIS_PARENTS {parents.toList}"
  logInfo m!"ACTUAL_CENTERED_ALL_OWNED_COUNT {owned.length}"

#print axioms ActualCenteredSealedTypeCheck
#check (AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance.actual_source_centered_variance_bounds (d := 2) (q := 0) (by decide))
'''
out = W/'CenteredVarianceDraftKernelProbe.lean'
with out.open('x') as f:
    f.write(code)
print(json.dumps({'probe': str(out), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'private_draft_only': True}))
