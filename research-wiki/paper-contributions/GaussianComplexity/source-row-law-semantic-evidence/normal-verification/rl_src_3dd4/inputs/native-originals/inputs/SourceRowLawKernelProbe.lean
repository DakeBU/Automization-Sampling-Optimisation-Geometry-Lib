import Tests.GaussianComplexityFixedSpectrumSourceRowLaw
open MeasureTheory ProbabilityTheory Lean
set_option autoImplicit false

def ExpectedProducer : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun a : Fin (q + 1) => ω a i)
  ∀ i : Fin d, MeasurePreserving (row i) μ (stdGaussian E)

def ExpectedPrivate : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun a : Fin (q + 1) => ω a i)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let good : Set Ω := {ω | ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L}
  ENNReal.ofReal (999 / 1000 : ℝ) ≤ μ good

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let target := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law
  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw." ||
    s.startsWith "_private.Tests.GaussianComplexityFixedSpectrumSourceRowLaw."
  let owned := env.constants.toList.filter (fun (n, _) => isOwned n)
  let wanted := owned.filter fun (n, _) => n == target ||
    n.toString.endsWith ".actual_original_all_good_cutoff_probability"
  unless wanted.length == 2 do throwError "Expected exactly two actual roots: {wanted.map Prod.fst}"
  let allowed := [`propext, `Classical.choice, `Quot.sound]
  let mut allReach : NameSet := {}
  for (n, ci) in wanted do
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Root is not theorem: {n}"
    let some proof := ci.value? true | throwError "Missing actual proof {n}"
    let mut pending := proof.getUsedConstants.toList
    let mut seen : NameSet := {}
    let mut parents : NameSet := {}
    while !pending.isEmpty do
      let u := pending.head!
      pending := pending.tail!
      unless seen.contains u do
        seen := seen.insert u
        if u == target && n != target then
          parents := parents.insert u
        else if isOwned u then
          let some aci := env.find? u | throwError "Missing owned provider {u}"
          let some ap := aci.value? true | throwError "Missing owned body {u}"
          pending := ap.getUsedConstants.toList ++ aci.type.getUsedConstants.toList ++ pending
        else if u.toString.startsWith "AutoSamplingTheory." then
          parents := parents.insert u
    allReach := seen.toList.foldl (fun z k => z.insert k) (allReach.insert n)
    let publicParents := parents.toList
    let required := if n == target then [] else [target, `AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian]
    unless publicParents.length == required.length && required.all publicParents.contains do
      throwError "Actual canonical parent mismatch for {n}: {publicParents}"
    let expected := if n == target then "ExpectedProducer" else "ExpectedPrivate"
    let checked := if n == target then "ActualProducerSealedTypeCheck" else "ActualPrivateSealedTypeCheck"
    let some expectedInfo := env.find? (Name.mkSimple expected) |
      throwError "Missing independent literal Prop {expected}"
    let params := ci.levelParams
    let levels := params.map Level.param
    unless expectedInfo.levelParams.length == params.length do
      throwError "Literal universe arity differs from actual declaration {n}"
    let some literal := expectedInfo.value? true | throwError "Missing literal Prop body"
    let literal := literal.instantiateLevelParams expectedInfo.levelParams levels
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
      name := Name.mkSimple checked
      levelParams := params
      type := mkConst (Name.mkSimple expected) levels
      value := mkConst n levels
    }
    logInfo m!"ACTUAL_UNIVERSE_PARAMS {n}: {params}"
    logInfo m!"ACTUAL_RAW_LITERAL_EXPR_EQUALITY {n}: {ci.type == literal}"
    logInfo m!"ACTUAL_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS {n}"
    logInfo m!"ACTUAL_PUBLIC_ASTIS_PARENTS {n}: {publicParents}"
    logInfo m!"ACTUAL_ALL_REACHABLE_OWNED {n}: {seen.toList.filter isOwned}"
  for (n, ci) in owned do
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Owned provider is not a theorem (must audit separately): {n}"
    unless !ci.type.hasLooseBVars && !ci.type.hasFVar && !ci.type.hasMVar do
      throwError "Owned theorem type is not closed: {n}"
    let some body := ci.value? true | throwError "Owned declaration has no body: {n}"
    unless !body.hasLooseBVars && !body.hasFVar && !body.hasMVar do
      throwError "Owned theorem proof is not closed: {n}"
    let ax ← Lean.collectAxioms n
    unless ax.all (fun a => allowed.contains a) do throwError "Unexpected axioms {n}: {ax}"
    logInfo m!"OWNED_DECL_USED {n}: {body.getUsedConstants.toList.length} constants"
    logInfo m!"OWNED_DECL_AXIOMS {n}: {ax}"
    logInfo m!"OWNED_DECL_REACHABLE_FROM_ACTUAL_ROOT {n}: {allReach.contains n}"
    unless allReach.contains n do
      throwError "Unreachable owned declaration requires diagnosis: {n}"
  logInfo m!"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED {owned.length}"

#print axioms ActualProducerSealedTypeCheck
#print axioms ActualPrivateSealedTypeCheck
