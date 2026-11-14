import Tests.GaussianComplexityFixedSpectrumKrylovRange
open Matrix Lean
open scoped BigOperators
set_option autoImplicit false
def ExpectedProducer : Prop := ∀ {d q : ℕ} (κ : ℝ) (hκ : 2 ≤ κ) (hq : 2 * q + 1 < d)
    (x : EuclideanSpace ℝ (Fin d × Fin (q + 1))),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let g : Fin (q + 1) → Fin d → ℝ := fun a i => WithLp.ofLp x (i, a)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let B : Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i a =>
    (Real.sqrt (d : ℝ))⁻¹ * g a.1 i * t i a.2
  let K : Submodule ℝ (Fin d → ℝ) :=
    Submodule.span ℝ (Set.range (fun a : Fin (q + 1) × Fin (q + 1) =>
      (Λ ^ a.2.val).mulVec (g a.1)))
  Set.range (fun c : Fin (q + 1) × Fin (q + 1) → ℝ => B.mulVec c) =
    (K : Set (Fin d → ℝ))

def ExpectedPrivate : Prop := ∀ {d q : ℕ} (κ : ℝ) (hκ : 2 ≤ κ) (hq : 2 * q + 1 < d)
    (x : EuclideanSpace ℝ (Fin d × Fin (q + 1))),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let g : Fin (q + 1) → Fin d → ℝ := fun a i => WithLp.ofLp x (i, a)
  let t : Matrix (Fin d) (Fin (q + 1)) ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let B : Matrix (Fin d) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i a =>
    (Real.sqrt (d : ℝ))⁻¹ * g a.1 i * t i a.2
  let K : Submodule ℝ (Fin d → ℝ) :=
    Submodule.span ℝ (Set.range (fun a : Fin (q + 1) × Fin (q + 1) =>
      (Λ ^ a.2.val).mulVec (g a.1)))
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i))
  ∀ v : Fin d → ℝ, v ∈ K →
    ∃ c : Fin (q + 1) × Fin (q + 1) → ℝ,
      B.mulVec c = v ∧
      ‖(WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))‖ ^ 2 =
        (∑ a : Fin (q + 1) × Fin (q + 1), c a * ((B.transpose * B).mulVec c) a) ∧
      (inner ℝ (WithLp.toLp 2 v : EuclideanSpace ℝ (Fin d))
        (WithLp.toLp 2 (D.mulVec v) : EuclideanSpace ℝ (Fin d))) =
        (∑ a : Fin (q + 1) × Fin (q + 1), c a * ((B.transpose * D * B).mulVec c) a)

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let target := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange.actual_cosine_feature_krylov_range
  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange." ||
    s.startsWith "_private.Tests.GaussianComplexityFixedSpectrumKrylovRange."
  let owned := env.constants.toList.filter (fun (n, _) => isOwned n)
  let wanted := owned.filter fun (n, _) => n == target ||
    n.toString.endsWith ".actual_krylov_quadratic_coordinates"
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
    logInfo m!"OWNED_DECL_USED {n}: {body.getUsedConstants.toList}"
    logInfo m!"OWNED_DECL_AXIOMS {n}: {ax}"
    logInfo m!"OWNED_DECL_REACHABLE_FROM_ACTUAL_ROOT {n}: {allReach.contains n}"
    unless allReach.contains n do
      throwError "Unreachable owned declaration requires diagnosis: {n}"
  logInfo m!"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED {owned.length}"

#print axioms ActualProducerSealedTypeCheck
#print axioms ActualPrivateSealedTypeCheck
