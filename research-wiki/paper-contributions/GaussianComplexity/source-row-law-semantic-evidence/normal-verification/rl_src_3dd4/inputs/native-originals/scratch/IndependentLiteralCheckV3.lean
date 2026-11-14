import Tests.GaussianComplexityFixedSpectrumSourceRowLaw
import Lean
open MeasureTheory ProbabilityTheory Lean Elab Command
set_option autoImplicit false
def IndependentLiteralProducer : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun a : Fin (q + 1) => ω a i)
  ∀ i : Fin d, MeasurePreserving (row i) μ (stdGaussian E)

def IndependentLiteralConsumer : Prop := ∀ {d q : ℕ} (hq : 2 * q + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun a : Fin (q + 1) => ω a i)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let good : Set Ω := {ω | ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L}
  ENNReal.ofReal (999 / 1000 : ℝ) ≤ μ good


run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let producer := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law
  let roots := env.constants.toList.filter fun (n,_) => n == producer ||
    n.toString.endsWith ".actual_original_all_good_cutoff_probability"
  unless roots.length == 2 do throwError "Wrong roots {roots.map Prod.fst}"
  for (n,c) in roots do
    let key := if n == producer then "IndependentLiteralProducer" else "IndependentLiteralConsumer"
    let literal := Name.mkSimple key
    let some expected := env.find? literal | throwError "Missing literal"
    let some typ := expected.value? true | throwError "Missing literal body"
    unless c.levelParams == [] do throwError "Unexpected root universe parameters {n}"
    liftCoreM <| addDecl <| Declaration.thmDecl {
      name := Name.mkSimple (key ++ "AppliedActual")
      levelParams := []
      type := mkConst literal
      value := mkConst n
    }
    logInfo m!"INDEPENDENT_SEAL_KERNEL_APPLICATION_PASS {n}"
    logInfo m!"INDEPENDENT_RAW_EXPR_EQUAL {n}: {c.type == typ}"
#print axioms IndependentLiteralProducerAppliedActual
#print axioms IndependentLiteralConsumerAppliedActual
