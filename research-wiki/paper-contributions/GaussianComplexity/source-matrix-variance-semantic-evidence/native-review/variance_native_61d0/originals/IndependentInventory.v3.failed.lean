import all AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import all AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance
import all AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment
import all AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import all Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance
import Lean
open Lean Elab Command Meta MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder
set_option maxHeartbeats 0
set_option maxRecDepth 100000
set_option pp.universes true
set_option pp.explicit true
set_option pp.fullNames true

def PLiteral : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
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


def PZeroLiteral : Prop := ∀ {d : ℕ} (hq : 2 * 0 + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (0 + 1))
  let Ω := Fin (0 + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (0 + 1) => stdGaussian D)
  let r : ℝ := ((0 + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (0 + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (0 + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (0 + 1) × Fin (0 + 1)) (Fin (0 + 1) × Fin (0 + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Y i ω * Y i ω) μ) ∧
    Matrix.PosSemidef
      (C • (1 : Matrix (Fin (0 + 1) × Fin (0 + 1)) (Fin (0 + 1) × Fin (0 + 1)) ℝ) -
        ∑ i : Fin d, ∫ ω, Y i ω * Y i ω ∂μ)


def TLiteral : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
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


def TZeroLiteral : Prop := ∀ {d : ℕ} (hq : 2 * 0 + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (0 + 1))
  let Ω := Fin (0 + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (0 + 1) => stdGaussian D)
  let r : ℝ := ((0 + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (0 + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (0 + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (0 + 1) × Fin (0 + 1)) (Fin (0 + 1) × Fin (0 + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (0 + 1) × Fin (0 + 1)) (Fin (0 + 1) × Fin (0 + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (0 + 1) × Fin (0 + 1)) (Fin (0 + 1) × Fin (0 + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * 0 + 1 : ℕ) : ℝ) * θ i)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Z i ω * Z i ω) μ) ∧
    (∀ i : Fin d, Integrable (fun ω => (w i • Z i ω) * (w i • Z i ω)) μ) ∧
    ‖∑ i : Fin d, ∫ ω, Z i ω * Z i ω ∂μ‖ ≤ C ∧
    ‖∑ i : Fin d, ∫ ω, (w i • Z i ω) * (w i • Z i ω) ∂μ‖ ≤ C


private def refs (e : Expr) : Array String :=
  (e.getUsedConstants.map Name.toString).qsort (· < ·)

private def ownModule (env : Environment) (n : Name) : String :=
  match env.getModuleIdxFor? n with
  | some idx => env.header.moduleNames[idx.toNat]!.toString
  | none => "CURRENT"

private def record (j : Json) : CommandElabM Unit := do
  liftIO <| IO.println j.compress

elab "#independentInventory" : command => do
  let env ← getEnv
  let names := env.constants.toList.filterMap fun (n, _) =>
    let m := ownModule env n
    if m.startsWith "AutoSamplingTheory." || m.startsWith "Tests." then some n else none
  let names := names.toArray.qsort (fun a b => a.toString < b.toString)
  let mut roots : Array Name := #[]
  for n in names do
    if n.toString.endsWith ".actual_source_truncated_matrix_second_moments" ||
       n.toString.endsWith ".actual_source_centered_variance_bounds" then
      roots := roots.push n
  unless roots.size == 2 do throwError "expected precisely two real roots, got {roots}"
  for n in names do
    let ci := env.find? n |>.get!
    let v := ci.value? (allowOpaque := true)
    unless !ci.type.hasFVar && !ci.type.hasMVar && !ci.type.hasLooseBVars do
      throwError "open type {n}"
    let mut checked := false
    if let some value := v then
      unless !value.hasFVar && !value.hasMVar && !value.hasLooseBVars do
        throwError "open body {n}"
      -- Kernel receives the actual complete value as a typed let, not an opaque reference.
      let clone := Name.str `IndependentKernelRechecks n.toString
      let body := Expr.letE `actual_value ci.type value (.bvar 0) false
      match ci with
      | .thmInfo _ => liftCoreM <| addDecl <| .thmDecl { name := clone, levelParams := ci.levelParams, type := ci.type, value := body }
      | .defnInfo d => liftCoreM <| addDecl <| .defnDecl { name := clone, levelParams := ci.levelParams, type := ci.type, value := body, hints := .opaque, safety := d.safety }
      | .opaqueInfo _ => liftCoreM <| addDecl <| .opaqueDecl { name := clone, levelParams := ci.levelParams, type := ci.type, value := body, isUnsafe := false }
      | _ => throwError "unexpected value-bearing kind {n}"
      checked := true
    let axioms ← collectAxioms n
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "nonstandard axiom {ax} in {n}"
    record <| Json.mkObj [
      ("record", toJson "declaration"), ("name",toJson n.toString),
      ("module",toJson (ownModule env n)),
      ("kind",toJson (match ci with | .thmInfo _ => "theorem" | .defnInfo _ => "definition" | .opaqueInfo _ => "opaque" | .axiomInfo _ => "axiom" | .ctorInfo _ => "constructor" | .recInfo _ => "recursor" | .inductInfo _ => "inductive" | .quotInfo _ => "quotient")),
      ("levelParams",toJson (ci.levelParams.map Name.toString)),
      ("typeExpr",toJson (reprStr ci.type)), ("valueExpr",toJson (v.map reprStr)),
      ("typeConstants",toJson (refs ci.type)), ("valueConstants",toJson (v.map refs |>.getD #[])),
      ("closed",toJson true), ("kernel_actual_typed_let_checked",toJson checked),
      ("axioms",toJson (axioms.map Name.toString))]
  for n in roots do
    let ci := env.find? n |>.get!
    let isP := n.toString.endsWith ".actual_source_truncated_matrix_second_moments"
    let literal := if isP then `PLiteral else `TLiteral
    let zeroLiteral := if isP then `PZeroLiteral else `TZeroLiteral
    let fullType := (env.find? literal |>.get!).value!.instantiateLevelParams [] []
    let zeroType := (env.find? zeroLiteral |>.get!).value!.instantiateLevelParams [] []
    let actualValue := ci.value! (allowOpaque := true)
    let fullName := if isP then `IndependentSealChecks.PUniversal else `IndependentSealChecks.TUniversal
    liftCoreM <| addDecl <| .thmDecl { name := fullName, levelParams := [], type := fullType, value := actualValue }
    let zeroValue ← liftTermElabM <| forallTelescopeReducing zeroType fun xs _ => do
      unless xs.size == 2 do throwError "q0 expects d and hq"
      mkLambdaFVars xs (mkApp3 actualValue xs[0]! (mkNatLit 0) xs[1]!)
    let zeroName := if isP then `IndependentSealChecks.PZero else `IndependentSealChecks.TZero
    liftCoreM <| addDecl <| .thmDecl { name := zeroName, levelParams := [], type := zeroType, value := zeroValue }
    record <| Json.mkObj [("record",toJson "literal-root-value-check"),("actual_name",toJson n.toString),("universal",toJson true),("q0",toJson true)]

#independentInventory
