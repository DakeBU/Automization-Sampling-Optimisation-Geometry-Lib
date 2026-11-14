import Tests.GaussianComplexityFixedSpectrumExactMeans
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open Lean
set_option autoImplicit false

example {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
  Integrable Q μ ∧
  (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) =
    ((d : ℝ) / Real.sqrt κ) * ((1 - r ^ (2 * d)) / (1 + r ^ (2 * d))) ∧
  (-1 : ℝ) ^ n * (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
    ((d : ℝ) / Real.sqrt κ) * ((r ^ n - r ^ (2 * d - n)) / (1 + r ^ (2 * d))) := by
  exact AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans.actual_diagonal_gaussian_exact_means hd hκ n hn hnd

def ExpectedPrivate : Prop := ∀ {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let m : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  0 < m ∧ m ≤ (d : ℝ) / Real.sqrt κ ∧ 0 < (-1 : ℝ) ^ n * b ∧
  |b| / m = r ^ n * ((1 - r ^ (2 * (d - n))) / (1 - r ^ (2 * d)))


run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let target := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans.actual_diagonal_gaussian_exact_means
  let means := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments.actual_diagonal_gaussian_quadratic_means
  let c7 := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion.actual_inverse_spectrum_cosine_expansion
  let grid := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias.actual_midpoint_grid_cosine_alias
  let isOwned := fun (n : Name) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans." ||
    s.startsWith "_private.Tests.GaussianComplexityFixedSpectrumExactMeans."
  let owned := env.constants.toList.filter (fun (n, _) => isOwned n)
  let wanted := owned.filter fun (n, _) => n == target ||
    n.toString.endsWith ".actual_gaussian_closed_means_bias_ratio"
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
      unless publicParents.length == 3 && publicParents.contains means &&
        publicParents.contains c7 && publicParents.contains grid do
        throwError "Producer exact canonical parents mismatch: {publicParents}"
    else
      unless publicParents == [target] do
        throwError "Consumer must materially use exactly new closed means: {publicParents}"
      Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
        name := Name.mkSimple "ActualPrivateSealedTypeCheck"
        levelParams := []
        type := mkConst (Name.mkSimple "ExpectedPrivate")
        value := mkConst n
      }
      logInfo "ACTUAL_PRIVATE_SEALED_LITERAL_KERNEL_TYPE_APPLICATION_PASS"
    logInfo m!"ACTUAL_ROOT {n}"
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
    -- The kernel body is checked above; omit unbounded Expr pretty-printing.
    unless allReach.contains n || (n.toString.splitOn "._simp_").length > 1 do
      throwError "Unreachable owned declaration requires diagnosis: {n}"
  logInfo m!"ALL_OWNED_DECLARATIONS_KERNEL_INSPECTED {owned.length}"

#print axioms ActualPrivateSealedTypeCheck
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans.actual_diagonal_gaussian_exact_means
