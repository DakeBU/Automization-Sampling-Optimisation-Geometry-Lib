import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
import Mathlib.Tactic.Ring

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
set_option autoImplicit false

/-- Source one-based i-1/2 equals the actual Fin d half-grid. This is a
meaning adapter, not an extra public premise or a new Registry lemma. -/
example {d : ℕ} (i : Fin d) :
    ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ) =
      (((i.val : ℝ) + 1) - 1 / 2) * Real.pi / (d : ℝ) := by
  ring

/-- A genuine actual Gaussian consumer. Its only mathematical inputs are the
source d/kappa/full-O; positivity is obtained from the new producer, never
supplied as an hPD or correct-density premise. -/
example {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹ =
      (volume : Measure (EuclideanSpace ℝ (Fin d))).withDensity (fun x =>
        ENNReal.ofReal (Real.sqrt A.det / (2 * Real.pi) ^ ((d : ℝ) / 2) *
          Real.exp (-((WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x)) / 2))) := by
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  change ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹ =
    (volume : Measure (EuclideanSpace ℝ (Fin d))).withDensity (fun x =>
      ENNReal.ofReal (Real.sqrt A.det / (2 * Real.pi) ^ ((d : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x)) / 2)))
  have hA : A.PosDef :=
    (FixedSpectrumAdmissibility.actual_precision_admissible (d := d) hd (κ := κ) hκ O).1
  show_term exact multivariateGaussian_eq_withDensity_of_posDef (n := d) A hA

#print axioms FixedSpectrumAdmissibility.actual_precision_admissible
#print axioms multivariateGaussian_eq_withDensity_of_posDef
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility.actual_precision_admissible | throwError "Missing actual cosine precision admissibility theorem"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing actual admissibility proof"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL COMPILED ASTIS PARENTS {parents}"
