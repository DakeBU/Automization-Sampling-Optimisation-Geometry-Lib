import Tests.GaussianComplexityZeroQuerySeparation
open Matrix MeasureTheory ProbabilityTheory Set Lean
open scoped NNReal ENNReal
set_option autoImplicit false
def ExpectedProducer : Prop := ∀ {d : ℕ} (hd : 1 ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ),
  let A₁ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => if i.val = 0 then κ else 1)
  let ν₀ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d))
      (1 : Matrix (Fin d) (Fin d) ℝ)⁻¹
  let ν₁ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A₁⁻¹
  let B : Set (EuclideanSpace ℝ (Fin d)) :=
    {x | |WithLp.ofLp x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ) / 2}
  (1 : ℝ) / 8 < ν₁.real B - ν₀.real B

def ExpectedPrivate : Prop := ∀ {d : ℕ} (hd : 1 ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) (ρ : ProbabilityMeasure (EuclideanSpace ℝ (Fin d))),
  let A₁ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => if i.val = 0 then κ else 1)
  let ν₀ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d))
      (1 : Matrix (Fin d) (Fin d) ℝ)⁻¹
  let ν₁ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A₁⁻¹
  let Δ : Measure (EuclideanSpace ℝ (Fin d)) →
      Measure (EuclideanSpace ℝ (Fin d)) → ℝ := fun μ ν =>
    sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)),
      MeasurableSet B ∧ z = |μ.real B - ν.real B|}
  ¬ (Δ (ρ : Measure (EuclideanSpace ℝ (Fin d))) ν₀ ≤ (1 : ℝ) / 16 ∧
    Δ (ρ : Measure (EuclideanSpace ℝ (Fin d))) ν₁ ≤ (1 : ℝ) / 16)

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let target := `AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation.actual_zero_query_gaussian_event_gap
  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation." ||
    s.startsWith "_private.Tests.GaussianComplexityZeroQuerySeparation."
  let owned := env.constants.toList.filter (fun (n, _) => isOwned n)
  let wanted := owned.filter fun (n, _) => n == target ||
    n.toString.endsWith ".no_common_zero_query_output"
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
    let required := if n == target then [] else [target]
    unless publicParents.length == required.length && required.all publicParents.contains do
      throwError "Actual canonical parent mismatch for {n}: {publicParents}"
    let expected := if n == target then "ExpectedProducer" else "ExpectedPrivate"
    let checked := if n == target then "ActualProducerSealedTypeCheck" else "ActualPrivateSealedTypeCheck"
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
      name := Name.mkSimple checked
      levelParams := []
      type := mkConst (Name.mkSimple expected)
      value := mkConst n
    }
    logInfo m!"ACTUAL_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS {n}"
    logInfo m!"ACTUAL_PUBLIC_ASTIS_PARENTS {n}: {publicParents}"
    logInfo m!"ACTUAL_ALL_REACHABLE_OWNED {n}: {seen.toList.filter isOwned}"
  for (n, ci) in owned do
    let some body := ci.value? true | throwError "Owned declaration has no body: {n}"
    let ax ← Lean.collectAxioms n
    unless ax.all (fun a => allowed.contains a) do throwError "Unexpected axioms {n}: {ax}"
    logInfo m!"OWNED_DECL_TYPE {n}: {ci.type}"
    logInfo m!"OWNED_DECL_USED {n}: {body.getUsedConstants.toList}"
    logInfo m!"OWNED_DECL_AXIOMS {n}: {ax}"
    logInfo m!"OWNED_DECL_REACHABLE_FROM_ACTUAL_ROOT {n}: {allReach.contains n}"
    unless allReach.contains n do
      throwError "Unreachable owned declaration requires diagnosis: {n}"
  logInfo m!"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED {owned.length}"

#print axioms ActualProducerSealedTypeCheck
#print axioms ActualPrivateSealedTypeCheck
