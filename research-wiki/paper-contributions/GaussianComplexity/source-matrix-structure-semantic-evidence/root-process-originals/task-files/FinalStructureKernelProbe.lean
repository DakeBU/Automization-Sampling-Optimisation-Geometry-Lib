import Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure
open MeasureTheory ProbabilityTheory Lean
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false

def ExpectedProducer : Prop := ∀     {d q : ℕ} (hq : 2 * q + 1 < d),
  letI : MeasurableSpace
      (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) :=
    borel (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  (∀ i : Fin d, Measurable (Z i)) ∧
    iIndepFun Z μ ∧
    (∀ i : Fin d, Integrable (Z i) μ) ∧
    (∀ i : Fin d, (∫ ω, Z i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (Z i ω).IsHermitian)

def ExpectedConsumer : Prop := ∀     {d q : ℕ} (hq : 2 * q + 1 < d),
  letI : MeasurableSpace
      (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) :=
    borel (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let X : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => w i • Z i ω
  (∀ i : Fin d, Measurable (X i)) ∧
    iIndepFun X μ ∧
    (∀ i : Fin d, Integrable (X i) μ) ∧
    (∀ i : Fin d, (∫ ω, X i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (X i ω).IsHermitian)

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let pTarget := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure
  let ts := env.constants.toList.filter fun (n, _) =>
    n.toString.endsWith ".actual_source_weighted_centered_matrix_structure"
  unless ts.length == 1 do throwError "Expected exactly one real private radius consumer"
  let tTarget := ts.head!.1
  let isOwned := fun (n : Name) =>
    n.toString.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure." ||
    n.toString.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure." ||
    n.toString.startsWith "_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure."
  let owned := env.constants.toList.filter fun (n, _) => isOwned n
  let handwritten := owned.filter fun (n, _) =>
    n == pTarget || n == tTarget
  unless handwritten.length == 2 && owned.length >= 2 do
    throwError "Unexpected owned radius inventory: {owned.map Prod.fst}"
  let mut allReach : NameSet := {}
  for n in [pTarget,tTarget] do
    let some ci := env.find? n | throwError "Missing root {n}"
    let some body := ci.value? true | throwError "Missing actual root proof body {n}"
    unless ci.levelParams.isEmpty do throwError "Unexpected root universes {n}"
    let expected := if n == pTarget then `ExpectedProducer else `ExpectedConsumer
    let checked := if n == pTarget then `ActualStructureProducerSealedKernelCheck else `ActualStructureConsumerSealedKernelCheck
    let some literalInfo := env.find? expected | throwError "Missing sealed literal"
    let some literal := literalInfo.value? true | throwError "Missing literal body"
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
      name := checked, levelParams := [], type := mkConst expected, value := body }
    logInfo m!"ACTUAL_R11_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS {n}"
    logInfo m!"ACTUAL_R11_RAW_LITERAL_EXPR_EQUALITY {n}: {ci.type == literal}"
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
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence.actual_source_rows_independent] else [pTarget]
    unless parents.toList.length == required.length && required.all parents.contains do
      throwError "Actual canonical parent mismatch {n}: {parents.toList}"
    logInfo m!"ACTUAL_R11_CANONICAL_ASTIS_PARENTS {n}: {parents.toList}"
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
      name := Name.str `ActualStructureOwnedKernel (toString n.hash),
      levelParams := ci.levelParams, type := ci.type, value := body }
    logInfo m!"ACTUAL_R11_OWNED_TYPE_BODY_KERNEL_PASS {n} axioms={ax}"
  logInfo m!"ACTUAL_R11_ALL_OWNED_KERNEL_INSPECTED {owned.length} HANDWRITTEN {handwritten.length} GENERATED {owned.length - handwritten.length}"

#print axioms ActualStructureProducerSealedKernelCheck
#print axioms ActualStructureConsumerSealedKernelCheck
#check (ActualStructureProducerSealedKernelCheck (d := 2) (q := 0) (by decide))
#check (ActualStructureConsumerSealedKernelCheck (d := 2) (q := 0) (by decide))
