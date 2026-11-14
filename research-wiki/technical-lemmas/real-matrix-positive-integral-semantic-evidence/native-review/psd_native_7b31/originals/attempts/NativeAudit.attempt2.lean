import Lean
import Tests.RealMatrixPositiveIntegral
open Lean Lean.Meta Lean.Elab Lean.Elab.Command
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem nativeLiteralS
    {n Ω : Type*} [Fintype n] [DecidableEq n] [MeasurableSpace Ω]
    {μ : Measure Ω} [IsProbabilityMeasure μ]
    (f : Ω → Matrix n n ℝ) (hf : Integrable f μ)
    (hpos : ∀ᵐ ω ∂μ, Matrix.PosSemidef (f ω)) :
    Matrix.PosSemidef (∫ ω, f ω ∂μ)
:= by
  exact AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef f hf hpos
theorem nativeEmptyS
    {Ω : Type*} [MeasurableSpace Ω]
    {μ : Measure Ω} [IsProbabilityMeasure μ]
    (f : Ω → Matrix (Fin 0) (Fin 0) ℝ) (hf : Integrable f μ)
    (hpos : ∀ᵐ ω ∂μ, Matrix.PosSemidef (f ω)) :
    Matrix.PosSemidef (∫ ω, f ω ∂μ)
:= by
  exact AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef f hf hpos
theorem nativeLiteralP
    {d q : ℕ} (hq : 2 * q + 1 < d) :
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
:= by
  exact AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments hq
theorem nativeZeroQueryP
    {d : ℕ} (hq : 2 * 0 + 1 < d) :
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
:= by
  exact AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments (q := 0) hq

private def ownedModules : Array Name := #[
  `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral,
  `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw,
  `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment,
  `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment,
  `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias,
  `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram,
  `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound,
  `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance,
  `Tests.RealMatrixPositiveIntegral]

private def owner (env : Environment) (name : Name) : Option Name := do
  let i ← env.getModuleIdxFor? name
  env.header.moduleNames[i.toNat]?

private partial def binderTypes (e : Expr) : Array Json := Id.run do
  match e with
  | .forallE n t b bi => return #[Json.mkObj [("name",toJson n.toString),("binder_info",toJson (reprStr bi)),("type",toJson (reprStr t))]] ++ binderTypes b
  | _ => return #[]

private def closed (e : Expr) : Bool := !e.hasMVar && !e.hasFVar && !e.hasLooseBVars

private def declKind : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _ => "quotient"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .inductInfo _ => "inductive"

-- The traversal below follows actual constants in types AND proof values.
-- Imports are used only to select the independently rebuilt module inventory.
private partial def reachable (env : Environment) (todo : List Name) (seen : NameSet := {}) : NameSet := Id.run do
  match todo with
  | [] => return seen
  | n :: rest =>
    if seen.contains n then return reachable env rest seen
    let seen := seen.insert n
    match env.find? n with
    | none => return reachable env rest seen
    | some ci =>
      let cs := ci.type.getUsedConstants.toList ++ ((ci.value? (allowOpaque := true)).map (·.getUsedConstants.toList)).getD []
      return reachable env (cs ++ rest) seen

elab "audit_native" : command => do
  liftTermElabM do
    let env := (← getEnv).setExporting false
    let all := env.constants.toList.filter fun (n, _) => ((owner env n).map ownedModules.contains).getD false
    let sorted := all.toArray.qsort (fun a b => Name.lt a.1 b.1)
    let dump ← IO.FS.Handle.mk "full-types-bodies.dump" .write
    let mut records : Array Json := #[]
    for (n, ci) in sorted do
      unless closed ci.type do throwError "open or meta type {n}"
      checkWithKernel ci.type
      dump.putStrLn s!"DECLARATION {n}\nTYPE\n{reprStr ci.type}\n"
      let mut bodyPresent := false
      let mut constants := ci.type.getUsedConstants
      if let some value := ci.value? (allowOpaque := true) then
        bodyPresent := true
        unless closed value do throwError "open or meta value {n}"
        -- A typed let forces the real proof value to have its recorded type.
        checkWithKernel (.letE n ci.type value (.bvar 0) false)
        dump.putStrLn s!"BODY\n{reprStr value}\n"
        constants := constants ++ value.getUsedConstants
      else
        dump.putStrLn "NO_BODY\n"
      let axs ← collectAxioms n
      for ax in axs do
        unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
          throwError "nonstandard axiom {ax} at {n}"
      let actualCalls := constants.filter fun dep => ((owner env dep).map ownedModules.contains).getD false
      records := records.push <| Json.mkObj [
        ("name",toJson n.toString), ("module",toJson ((owner env n).map Name.toString)),
        ("kind",toJson (declKind ci)), ("level_params",toJson (ci.levelParams.map Name.toString)),
        ("type_closed",toJson true),("body_present",toJson bodyPresent),("body_closed_and_kernel_checked",toJson bodyPresent),
        ("binders",toJson (binderTypes ci.type)),("axioms",toJson (axs.map Name.toString)),
        ("actual_ASTIS_type_and_body_calls",toJson (actualCalls.map Name.toString))]
    dump.flush
    let roots := #[
      `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef,
      `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments]
    let mut rootRecords : Array Json := #[]
    for root in roots do
      let reach := reachable env [root]
      let reached := sorted.filterMap fun (n, _) => if reach.contains n then some n.toString else none
      let rawAxioms := reach.toArray.filterMap fun n =>
        match env.find? n with
        | some (.axiomInfo _) => some n.toString
        | _ => none
      for ax in rawAxioms do
        unless #["propext", "Classical.choice", "Quot.sound"].contains ax do
          throwError "raw graph has nonstandard axiom {ax}"
      rootRecords := rootRecords.push <| Json.mkObj [("root",toJson root.toString),("all_raw_reachable_constant_count",toJson reach.size),("actual_reachable_ASTIS",toJson reached),("raw_axioms",toJson rawAxioms)]
    let mut literals : Array Json := #[]
    for n in #[`nativeLiteralS, `nativeEmptyS, `nativeLiteralP, `nativeZeroQueryP] do
      let ci ← getConstInfo n
      let some value := ci.value? | throwError "missing literal proof {n}"
      unless closed ci.type && closed value do throwError "open literal proof {n}"
      checkWithKernel (.letE n ci.type value (.bvar 0) false)
      -- Inline the real root proof values into the literal proposition application.
      let expanded := value.replace fun e =>
        match e with
        | .const name us =>
          if roots.contains name then
            match env.find? name with
            | some info => (info.value?).map fun v => v.instantiateLevelParams info.levelParams us
            | none => none
          else none
        | _ => none
      checkWithKernel (.letE n ci.type expanded (.bvar 0) false)
      dump.putStrLn s!"LITERAL {n}\nTYPE\n{reprStr ci.type}\nEXPANDED_ROOT_PROOF_APPLICATION\n{reprStr expanded}\n"
      literals := literals.push <| Json.mkObj [("name",toJson n.toString),("level_params",toJson (ci.levelParams.map Name.toString)),("literal_type",toJson (reprStr ci.type)),("expanded_actual_root_proof_value_kernel_checked",toJson true)]
    dump.flush
    IO.FS.writeFile "kernel-audit.json" <| (Json.mkObj [("declarations",toJson records),("roots",toJson rootRecords),("literals",toJson literals)]).pretty
    logInfo m!"NATIVE_KERNEL_AUDIT_OK declarations={sorted.size}; literal proof-value applications=4"

audit_native
