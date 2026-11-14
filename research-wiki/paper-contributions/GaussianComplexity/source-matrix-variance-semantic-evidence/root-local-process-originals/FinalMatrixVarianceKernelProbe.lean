import Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance
open MeasureTheory ProbabilityTheory Lean
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

def ExpectedProducer : Prop := ∀     {d q : ℕ} (hq : 2 * q + 1 < d),
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
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Y i ω * Y i ω) μ) ∧
    Matrix.PosSemidef
      (C • (1 : Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ) -
        ∑ i : Fin d, ∫ ω, Y i ω * Y i ω ∂μ)

def ExpectedConsumer : Prop := ∀     {d q : ℕ} (hq : 2 * q + 1 < d),
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
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Z i ω * Z i ω) μ) ∧
    (∀ i : Fin d, Integrable (fun ω => (w i • Z i ω) * (w i • Z i ω)) μ) ∧
    ‖∑ i : Fin d, ∫ ω, Z i ω * Z i ω ∂μ‖ ≤ C ∧
    ‖∑ i : Fin d, ∫ ω, (w i • Z i ω) * (w i • Z i ω) ∂μ‖ ≤ C

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let pTarget := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments
  let ts := env.constants.toList.filter fun (n, _) =>
    n.toString.endsWith ".actual_source_centered_variance_bounds"
  unless ts.length == 1 do throwError "Expected exactly one actual final private T root"
  let tTarget := ts.head!.1
  let isOwned := fun (n : Name) => pTarget.isPrefixOf n || tTarget.isPrefixOf n
  let owned := env.constants.toList.filter fun (n, _) => isOwned n
  unless owned.length == 7 do throwError "Actual R9 inventory changed: {owned.map Prod.fst}"
  let mut allReach : NameSet := {}
  for n in [pTarget,tTarget] do
    let some ci := env.find? n | throwError "Missing root {n}"
    let some body := ci.value? true | throwError "Missing actual root body {n}"
    unless ci.levelParams.isEmpty do throwError "Unexpected root universes {n}"
    let expected := if n == pTarget then `ExpectedProducer else `ExpectedConsumer
    let checked := if n == pTarget then `ActualProducerSealedTypeCheck else `ActualConsumerSealedTypeCheck
    let some literalInfo := env.find? expected | throwError "Missing sealed literal"
    let some literal := literalInfo.value? true | throwError "Missing literal body"
    Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
      name := checked
      levelParams := []
      type := mkConst expected
      value := body
    }
    logInfo m!"ACTUAL_FINAL_R9_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS {n}"
    logInfo m!"ACTUAL_FINAL_R9_RAW_LITERAL_EXPR_EQUALITY {n}: {ci.type == literal}"
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
          let some dep := env.find? u | throwError "Missing own provider {u}"
          let some v := dep.value? true | throwError "Missing own provider body {u}"
          pending := v.getUsedConstants.toList ++ dep.type.getUsedConstants.toList ++ pending
        else if u.toString.startsWith "AutoSamplingTheory." then
          parents := parents.insert u
    let required := if n == pTarget then [
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment.actual_radial_fourth_moment_matrix,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound.actual_weighted_cosine_coefficient_bound,
      `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef] else [
      pTarget,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means,
      `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef]
    unless parents.toList.length == required.length && required.all parents.contains do
      throwError "Actual final canonical parent mismatch {n}: {parents.toList}"
    logInfo m!"ACTUAL_FINAL_R9_PUBLIC_ASTIS_PARENTS {n}: {parents.toList}"
    allReach := seen.toList.foldl (fun z u => z.insert u) (allReach.insert n)
  for (n,ci) in owned do
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Owned provider is not theorem {n}"
    let some body := ci.value? true | throwError "Missing proof body {n}"
    unless !ci.type.hasLooseBVars && !ci.type.hasFVar && !ci.type.hasMVar &&
        !body.hasLooseBVars && !body.hasFVar && !body.hasMVar do
      throwError "Unclosed owned type or proof {n}"
    unless allReach.contains n do throwError "Unreachable new R9 proof {n}"
    let ax ← Lean.collectAxioms n
    unless ax.all ([`propext,`Classical.choice,`Quot.sound].contains) do
      throwError "Unexpected axioms {n}: {ax}"
    logInfo m!"ACTUAL_FINAL_R9_OWNED_CLOSED_REACHABLE {n} axioms={ax}"
  logInfo m!"ACTUAL_FINAL_R9_ALL_OWNED_KERNEL_INSPECTED {owned.length}"

#print axioms ActualProducerSealedTypeCheck
#print axioms ActualConsumerSealedTypeCheck
#check (ActualProducerSealedTypeCheck (d := 2) (q := 0) (by decide))
#check (ActualConsumerSealedTypeCheck (d := 2) (q := 0) (by decide))
