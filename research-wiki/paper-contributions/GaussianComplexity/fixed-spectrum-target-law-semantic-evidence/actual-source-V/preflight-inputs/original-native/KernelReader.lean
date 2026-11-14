import Tests.GaussianComplexityFixedSpectrumTargetLaw
import Lean
open Lean Elab Command Meta Matrix MeasureTheory ProbabilityTheory
open scoped BigOperators RealInnerProductSpace
set_option autoImplicit false
set_option maxRecDepth 3000
set_option maxHeartbeats 1200000

def ExpectedProducer : Prop := ∀ {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ) (O : Matrix.orthogonalGroup (Fin d) ℝ),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let R : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun z => WithLp.toLp 2 ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z)
  (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹).map R =
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹


def ExpectedConsumer : Prop := ∀ {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ) (O : Matrix.orthogonalGroup (Fin d) ℝ),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
  Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
    (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) =
      ∑ i : Fin d, ((κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))⁻¹


def dependencies (ci : ConstantInfo) : Array Name :=
  ci.type.getUsedConstants ++ ((ci.value? (allowOpaque := true)).map Expr.getUsedConstants |>.getD #[])

def moduleOwner (env : Environment) (n : Name) : Name :=
  (env.getModuleIdxFor? n |>.bind fun i => env.header.moduleNames[i]?).getD .anonymous

def reachable (env : Environment) (root : Name) : CoreM NameSet := do
  let mut todo := [root]
  let mut seen : NameSet := {}
  let mut fuel := 200000
  while !todo.isEmpty do
    if fuel == 0 then throwError "reachability fuel exhausted"
    fuel := fuel - 1
    let n := todo.head!
    todo := todo.tail!
    if seen.contains n then continue
    seen := seen.insert n
    if let some ci := env.find? n then
      for dep in dependencies ci do
        if !seen.contains dep then todo := dep :: todo
  return seen

elab "readerAudit" : command => liftTermElabM do
  let env ← getEnv
  let p := ``AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw.actual_rotated_gaussian_target
  let pm := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw
  let tm := `Tests.GaussianComplexityFixedSpectrumTargetLaw
  let mut owned : Array Name := #[]
  let mut consumer : Array Name := #[]
  for (n, _) in env.constants.toList do
    let m := moduleOwner env n
    if m == pm || m == tm then
      owned := owned.push n
      logInfo m!"OWNED {m} {n}"
      if n.toString.endsWith ".actual_target_gaussian_norm_mean" then consumer := consumer.push n
  unless consumer.size == 1 do throwError "private consumer discovery size {consumer.size}"
  let c := consumer[0]!
  unless owned.size == 2 do throwError "owned inventory expected 2, actual {owned.size}"
  for (n, expectedName) in [(p, ``ExpectedProducer), (c, ``ExpectedConsumer)] do
    let ci ← getConstInfo n
    let ei ← getConstInfo expectedName
    let some expected := ei.value? | throwError "expected type body absent"
    unless (← isDefEq ci.type expected) do throwError "type mismatch for {n}"
    logInfo m!"EXACT_TYPE_PASS {n}"
    logInfo m!"ELABORATED_TYPE {n}\n{← ppExpr ci.type}"
    let some value := ci.value? (allowOpaque := true) | throwError "root body missing {n}"
    for dep in value.getUsedConstants do
      if dep.toString.startsWith "AutoSamplingTheory." || dep == p then
        logInfo m!"DIRECT_ASTIS {n} => {dep}"
    let reach ← reachable env n
    let mut count := 0
    let mut axioms : Array Name := #[]
    for dep in reach do
      count := count + 1
      if let some di := env.find? dep then
        if di matches .axiomInfo _ then axioms := axioms.push dep
      if dep.toString.startsWith "AutoSamplingTheory." || dep.toString.startsWith "_private.Tests.GaussianComplexityFixedSpectrumTargetLaw" then
        logInfo m!"REACHABLE_ASTIS {n} => {dep}"
    logInfo m!"REACHABILITY_COUNT {n} {count}"
    logInfo m!"RECURSIVE_AXIOMS {n} {axioms}"
    let stdAxioms := [``propext, ``Classical.choice, ``Quot.sound]
    for a in axioms do
      unless stdAxioms.contains a do throwError "nonstandard axiom {a}"
    for o in owned do
      if n == c then
        unless reach.contains o do throwError "owned declaration unreachable from private root {o}"
    if n == p then
      unless reach.contains ``AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility.actual_precision_admissible do throwError "missing actual admissibility"
    if n == c then
      unless reach.contains p do throwError "missing producer consumption"
      unless reach.contains ``AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments.actual_diagonal_gaussian_quadratic_means do throwError "missing moment consumption"
  logInfo "INDEPENDENT_KERNEL_READER_PASS"

readerAudit
