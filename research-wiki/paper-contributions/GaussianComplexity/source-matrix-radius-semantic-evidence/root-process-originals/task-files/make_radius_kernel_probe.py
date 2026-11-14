"""Kernel-check actual final root bodies against the original sealed literal Props."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
seal=json.loads((W/'statement-seal-v1.json').read_bytes())
code='''import Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius
open MeasureTheory ProbabilityTheory Lean
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false
'''
for label,key in [('Producer','producer'),('Consumer','actual_private_consumer')]:
    binders,result=seal[key]['signature'].split(' :\n',1)
    code+='\ndef Expected'+label+' : Prop := ∀ '+binders+',\n'+result
code+=r'''
run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let pTarget := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds
  let ts := env.constants.toList.filter fun (n, _) =>
    n.toString.endsWith ".actual_source_centered_summand_radius"
  unless ts.length == 1 do throwError "Expected exactly one real private radius consumer"
  let tTarget := ts.head!.1
  let isOwned := fun (n : Name) =>
    n.toString.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius." ||
    n.toString.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius." ||
    n.toString.startsWith "_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius."
  let owned := env.constants.toList.filter fun (n, _) => isOwned n
  let handwritten := owned.filter fun (n, _) =>
    n == pTarget || n == tTarget || n.toString.endsWith ".matrix_outer_norm" ||
    n.toString.endsWith ".rankone_tensor_norm" || n.toString.endsWith ".identity_rankone_norm"
  unless handwritten.length == 5 && owned.length >= 5 do
    throwError "Unexpected owned radius inventory: {owned.map Prod.fst}"
  let mut allReach : NameSet := {}
  for n in [pTarget,tTarget] do
    let some ci := env.find? n | throwError "Missing root {n}"
    let some body := ci.value? true | throwError "Missing actual root proof body {n}"
    unless ci.levelParams.isEmpty do throwError "Unexpected root universes {n}"
    let expected := if n == pTarget then `ExpectedProducer else `ExpectedConsumer
    let checked := if n == pTarget then `ActualRadiusProducerSealedKernelCheck else `ActualRadiusConsumerSealedKernelCheck
    let some literalInfo := env.find? expected | throwError "Missing sealed literal"
    let some literal := literalInfo.value? true | throwError "Missing literal body"
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
      name := checked, levelParams := [], type := mkConst expected, value := body }
    logInfo m!"ACTUAL_R10_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS {n}"
    logInfo m!"ACTUAL_R10_RAW_LITERAL_EXPR_EQUALITY {n}: {ci.type == literal}"
    let mut pending := body.getUsedConstants.toList
    let mut seen : NameSet := {}
    let mut parents : NameSet := {}
    while !pending.isEmpty do
      let u := pending.head!
      pending := pending.tail!
      unless seen.contains u do
        seen := seen.insert u
        if u == pTarget && n == tTarget then
          parents := parents.insert u
        else if isOwned u then
          let some dep := env.find? u | throwError "Missing internal provider {u}"
          let some v := dep.value? true | throwError "Missing internal body {u}"
          pending := v.getUsedConstants.toList ++ dep.type.getUsedConstants.toList ++ pending
        else if u.toString.startsWith "AutoSamplingTheory." then
          parents := parents.insert u
    let required := if n == pTarget then [
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram,
      `AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian] else [pTarget]
    unless parents.toList.length == required.length && required.all parents.contains do
      throwError "Actual canonical parent mismatch {n}: {parents.toList}"
    logInfo m!"ACTUAL_R10_CANONICAL_ASTIS_PARENTS {n}: {parents.toList}"
    allReach := seen.toList.foldl (fun z u => z.insert u) (allReach.insert n)
  for (n,ci) in owned do
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Unexpected owned non-theorem provider {n}"
    let some body := ci.value? true | throwError "Missing owned proof body {n}"
    unless !ci.type.hasLooseBVars && !ci.type.hasFVar && !ci.type.hasMVar &&
        !body.hasLooseBVars && !body.hasFVar && !body.hasMVar do
      throwError "Unclosed owned declaration {n}"
    unless allReach.contains n do throwError "Unreachable owned declaration {n}"
    let ax ← Lean.collectAxioms n
    unless ax.all ([`propext,`Classical.choice,`Quot.sound].contains) do
      throwError "Nonstandard axiom {n}: {ax}"
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
      name := Name.str `ActualRadiusOwnedKernel (toString n.hash),
      levelParams := ci.levelParams, type := ci.type, value := body }
    logInfo m!"ACTUAL_R10_OWNED_TYPE_BODY_KERNEL_PASS {n} axioms={ax}"
  logInfo m!"ACTUAL_R10_ALL_OWNED_KERNEL_INSPECTED {owned.length} HANDWRITTEN {handwritten.length} GENERATED {owned.length - handwritten.length}"

#print axioms ActualRadiusProducerSealedKernelCheck
#print axioms ActualRadiusConsumerSealedKernelCheck
#check (ActualRadiusProducerSealedKernelCheck (d := 2) (q := 0) (by decide))
#check (ActualRadiusConsumerSealedKernelCheck (d := 2) (q := 0) (by decide))
'''
p=W/'FinalRadiusKernelProbe.lean'
with p.open('x') as f:f.write(code)
print(json.dumps({'probe':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'actual_proof_values':True,'sealed_signature_changes':0}))
