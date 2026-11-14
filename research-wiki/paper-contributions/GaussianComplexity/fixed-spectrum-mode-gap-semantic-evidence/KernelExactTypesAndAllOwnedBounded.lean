import Tests.GaussianComplexityFixedSpectrumModeGap
open MeasureTheory ProbabilityTheory Lean
open scoped BigOperators
set_option autoImplicit false
def ExpectedProducer : Prop := ∀ {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1),
  ∃ d₀ : ℕ, ∀ (d : ℕ), d₀ ≤ d → ∀ (κ : ℝ), 2 ≤ κ →
    κ ≤ (d : ℝ) ^ (1 - δ) → ∀ (q : ℕ),
    (q : ℝ) ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) →
    let n : ℕ := 2 * q + 1
    2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ)

def ExpectedPrivate : Prop := ∀ {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1),
  ∃ d₀ : ℕ, ∀ (d : ℕ), d₀ ≤ d → ∀ (κ : ℝ), 2 ≤ κ →
    κ ≤ (d : ℝ) ^ (1 - δ) → ∀ (q : ℕ),
    (q : ℝ) ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) →
    let n : ℕ := 2 * q + 1
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
    let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
    let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
      multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
    let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
    let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
    let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
    0 < M ∧ 0 < (-1 : ℝ) ^ n * b ∧
      ((1 - Real.exp (-4)) * Real.exp (-3)) * (d : ℝ) ^ (-δ / 4) ≤ |b| / M


run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let target := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap.eventual_source_query_mode_gap
  let bias := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias.actual_diagonal_gaussian_exponential_bias
  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap." ||
    s.startsWith "_private.Tests.GaussianComplexityFixedSpectrumModeGap."
  let owned := env.constants.toList.filter (fun (n, _) => isOwned n)
  let wanted := owned.filter fun (n, _) => n == target ||
    n.toString.endsWith ".actual_gaussian_source_query_bias_power_lower"
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
    if n == target then
      unless publicParents.isEmpty do
        throwError "Pure scalar producer has unexpected ASTIS parents: {publicParents}"
    else
      unless publicParents.length == 2 && publicParents.contains target && publicParents.contains bias do
        throwError "Consumer exact canonical parents mismatch: {publicParents}"
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
    unless allReach.contains n || (n.toString.splitOn "._simp_").length > 1 do
      throwError "Unreachable owned declaration requires diagnosis: {n}"
  logInfo m!"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED {owned.length}"

#print axioms ActualProducerSealedTypeCheck
#print axioms ActualPrivateSealedTypeCheck
