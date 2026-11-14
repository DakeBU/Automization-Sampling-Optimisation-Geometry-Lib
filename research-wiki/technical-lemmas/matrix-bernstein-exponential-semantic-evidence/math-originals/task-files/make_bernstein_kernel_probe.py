"""Recheck actual values at the pre-proof sealed types after the full Lake build."""
from pathlib import Path
import json, hashlib

W = Path(__file__).resolve().parent
seal = json.loads((W / 'statement-seal.unclaimed.v1.json').read_bytes())
code = '''import Tests.GaussianComplexityBernsteinMgf
open MeasureTheory ProbabilityTheory Lean
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder
set_option autoImplicit false
universe u
'''
for label, key in [('Producer', 'producer'), ('Consumer', 'actual_private_consumer')]:
    binders, result = seal[key]['signature'].split(' :\n', 1)
    code += '\ndef Expected' + label + ' : Prop := ∀ ' + binders + ',\n' + result
code += r'''
run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let pTarget := `AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential.bernstein_exponential_quadratic_bound
  let ts := env.constants.toList.filter fun (n, _) =>
    n.toString.endsWith ".actual_source_normalized_single_summand_mgf"
  unless ts.length == 1 do throwError "Expected exactly one actual private Gaussian MGF consumer"
  let tTarget := ts.head!.1
  let isOwned := fun (n : Name) =>
    n.toString.startsWith "AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential." ||
    n.toString.startsWith "_private.AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential." ||
    n.toString.startsWith "_private.Tests.GaussianComplexityBernsteinMgf."
  let owned := env.constants.toList.filter fun (n, _) => isOwned n
  unless owned.length >= 14 do throwError "Incomplete producer/consumer module inventory {owned.map Prod.fst}"
  let mut allReach : NameSet := {}
  for n in [pTarget, tTarget] do
    let some ci := env.find? n | throwError "Missing actual root {n}"
    let some body := ci.value? true | throwError "Missing actual root proof value {n}"
    let expected := if n == pTarget then `ExpectedProducer else `ExpectedConsumer
    let checked := if n == pTarget then `ActualBernsteinProducerSealedKernelCheck else `ActualBernsteinConsumerSealedKernelCheck
    let some literalInfo := env.find? expected | throwError "Missing sealed literal {expected}"
    let some literal := literalInfo.value? true | throwError "Missing sealed literal body"
    unless ci.levelParams == literalInfo.levelParams do throwError "Sealed universe mismatch {n}"
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
      name := checked, levelParams := ci.levelParams,
      type := mkConst expected (ci.levelParams.map Level.param), value := body }
    logInfo m!"ACTUAL_R13_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS {n}"
    logInfo m!"ACTUAL_R13_RAW_LITERAL_EXPR_EQUALITY {n}: {ci.type == literal}"
    let mut pending := body.getUsedConstants.toList ++ ci.type.getUsedConstants.toList
    let mut seen : NameSet := {}
    let mut parents : NameSet := {}
    while !pending.isEmpty do
      let x := pending.head!
      pending := pending.tail!
      unless seen.contains x do
        seen := seen.insert x
        if x == pTarget && n == tTarget then
          parents := parents.insert x
        else if isOwned x then
          let some dep := env.find? x | throwError "Missing owned provider {x}"
          let some val := dep.value? true | throwError "Missing owned provider value {x}"
          pending := val.getUsedConstants.toList ++ dep.type.getUsedConstants.toList ++ pending
        else if x.toString.startsWith "AutoSamplingTheory." then
          parents := parents.insert x
    let required := if n == pTarget then [] else [pTarget,
      `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure]
    unless parents.toList.length == required.length && required.all parents.contains do
      throwError "Actual canonical ASTIS parent mismatch {n}: {parents.toList}"
    logInfo m!"ACTUAL_R13_CANONICAL_ASTIS_PARENTS {n}: {parents.toList}"
    allReach := seen.toList.foldl (fun z x => z.insert x) (allReach.insert n)
  for (n, ci) in owned do
    let some body := ci.value? true | throwError "Missing owned value {n}"
    unless !ci.type.hasLooseBVars && !ci.type.hasFVar && !ci.type.hasMVar &&
        !body.hasLooseBVars && !body.hasFVar && !body.hasMVar do
      throwError "Unclosed owned declaration {n}"
    let ax ← Lean.collectAxioms n
    unless ax.all ([`propext, `Classical.choice, `Quot.sound].contains) do
      throwError "Nonstandard axiom {n}: {ax}"
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.defnDecl {
      name := Name.str `ActualBernsteinOwnedKernel (toString n.hash),
      levelParams := ci.levelParams, type := ci.type, value := body,
      hints := .opaque, safety := .safe }
    logInfo m!"ACTUAL_R13_OWNED_TYPE_VALUE_KERNEL_PASS {n} reachable={allReach.contains n} axioms={ax}"
  logInfo m!"ACTUAL_R13_ALL_NAMESPACE_OWNED_KERNEL_INSPECTED {owned.length}"

#print axioms ActualBernsteinProducerSealedKernelCheck
#print axioms ActualBernsteinConsumerSealedKernelCheck
#check (fun (d : ℕ) (hd : 1 < d) =>
  ActualBernsteinConsumerSealedKernelCheck (d := d) (q := 0) (by omega))
#check (ActualBernsteinConsumerSealedKernelCheck (d := 2) (q := 0) (by decide))
'''
p = W / 'FinalBernsteinKernelProbe.lean'
with p.open('x') as f:
    f.write(code)
print(json.dumps({'probe': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                  'sealed_signature_changes': 0, 'actual_proof_values': True,
                  'root_inventory_scope': 'namespace-owned; independent raw module-emission inventory still required'}))
