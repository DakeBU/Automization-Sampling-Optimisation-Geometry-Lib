import Tests.GaussianComplexityFixedSpectrumDetector
open Matrix MeasureTheory ProbabilityTheory Lean
open scoped BigOperators
set_option autoImplicit false
def ExpectedProducer : Prop := ∀ {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) (n : ℕ),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let B : Matrix (Fin d) (Fin d) ℝ :=
    (κ - 1)⁻¹ • ((2 : ℝ) • A - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))
  Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ)) =
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => Real.cos ((n : ℝ) * θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose

def ExpectedPrivate : Prop := ∀ {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) (n : ℕ) (τ : ℝ),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let R : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun z => WithLp.toLp 2 ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let B : Matrix (Fin d) (Fin d) ℝ :=
    (κ - 1)⁻¹ • ((2 : ℝ) • A - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))
  let S : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (-1 : ℝ) ^ n *
      ((WithLp.ofLp x) ⬝ᵥ ((Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ))) *ᵥ WithLp.ofLp x)) -
      2 * τ * ‖x‖ ^ 2
  MeasurableSet {x | 0 < S x} ∧
    (μ.map R) {x | 0 < S x} =
      μ {z | 0 < (-1 : ℝ) ^ n *
        (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp z i) ^ 2) -
        2 * τ * ‖z‖ ^ 2}

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let target := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector.actual_chebyshev_matrix_cosine
  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector." ||
    s.startsWith "_private.Tests.GaussianComplexityFixedSpectrumDetector."
  let owned := env.constants.toList.filter (fun (n, _) => isOwned n)
  let wanted := owned.filter fun (n, _) => n == target ||
    n.toString.endsWith ".actual_rotated_gaussian_detector_event"
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
    unless allReach.contains n || (n.toString.splitOn "._simp_").length > 1 do
      throwError "Unreachable owned declaration requires diagnosis: {n}"
  logInfo m!"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED {owned.length}"

#print axioms ActualProducerSealedTypeCheck
#print axioms ActualPrivateSealedTypeCheck
