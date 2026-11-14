import Tests.GaussianComplexityFixedSpectrumCosineGram
open Matrix MeasureTheory ProbabilityTheory Set Lean
open scoped BigOperators NNReal ENNReal
set_option autoImplicit false
def ExpectedProducer : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  t.transpose * t = (d : ℝ) • (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) ∧
    t.transpose * D * t = 0 ∧
    ∀ i : Fin d, ∑ k : Fin (q + 1), (t i k) ^ 2 ≤ 2 * ((q : ℝ) + 1)

def ExpectedPrivate : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  let μ : Measure (EuclideanSpace ℝ (Fin d × Fin (q + 1))) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d × Fin (q + 1)))
      (1 : Matrix (Fin d × Fin (q + 1)) (Fin d × Fin (q + 1)) ℝ)
  let B : EuclideanSpace ℝ (Fin d × Fin (q + 1)) →
      Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun x i a =>
    (Real.sqrt (d : ℝ))⁻¹ * WithLp.ofLp x (i, a.1) * t i a.2
  ∀ a b : Fin (q + 1) × Fin (q + 1),
    Integrable (fun x => ((B x).transpose * B x) a b) μ ∧
    Integrable (fun x => ((B x).transpose * D * B x) a b) μ ∧
    (∫ x, ((B x).transpose * B x) a b ∂μ) = (if a = b then 1 else 0) ∧
    (∫ x, ((B x).transpose * D * B x) a b ∂μ) = 0

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let target := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram
  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram." ||
    s.startsWith "_private.Tests.GaussianComplexityFixedSpectrumCosineGram."
  let owned := env.constants.toList.filter (fun (n, _) => isOwned n)
  let wanted := owned.filter fun (n, _) => n == target ||
    n.toString.endsWith ".actual_gaussian_gram_means"
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
    let required := if n == target then [`AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias.actual_midpoint_grid_cosine_alias] else [target]
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
    logInfo m!"OWNED_DECL_USED {n}: {body.getUsedConstants.toList}"
    logInfo m!"OWNED_DECL_AXIOMS {n}: {ax}"
    logInfo m!"OWNED_DECL_REACHABLE_FROM_ACTUAL_ROOT {n}: {allReach.contains n}"
    unless allReach.contains n do
      throwError "Unreachable owned declaration requires diagnosis: {n}"
  logInfo m!"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED {owned.length}"

#print axioms ActualProducerSealedTypeCheck
#print axioms ActualPrivateSealedTypeCheck
