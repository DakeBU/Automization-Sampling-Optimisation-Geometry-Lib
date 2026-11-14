import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine
import Lean.Util.FoldConsts
open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity
set_option autoImplicit false

-- Actual two-hidden-rotation same-point precision-observation consumer.
-- The input matrices/replies are literal source objects; no assumed affine
-- identity or scalar stand-in. The equivalence is pointwise only, not a
-- Gaussian-target/TV/adaptive/deterministic-cap/expected-cost reduction.
example {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (O1 O2 : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let precision1 : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
      (O1 : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
        (O1 : Matrix (Fin d) (Fin d) ℝ).transpose
    let precision2 : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
      (O2 : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
        (O2 : Matrix (Fin d) (Fin d) ℝ).transpose
    let reply1 : ℝ → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun η x => WithLp.toLp 2 (precision1 η *ᵥ WithLp.ofLp x)
    let reply2 : ℝ → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun η x => WithLp.toLp 2 (precision2 η *ᵥ WithLp.ofLp x)
    ∀ x : EuclideanSpace ℝ (Fin d),
      reply1 κ x = reply2 κ x ↔ reply1 2 x = reply2 2 x := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let precision1 : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
    (O1 : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
      (O1 : Matrix (Fin d) (Fin d) ℝ).transpose
  let precision2 : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
    (O2 : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
      (O2 : Matrix (Fin d) (Fin d) ℝ).transpose
  let reply1 : ℝ → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun η x => WithLp.toLp 2 (precision1 η *ᵥ WithLp.ofLp x)
  let reply2 : ℝ → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun η x => WithLp.toLp 2 (precision2 η *ᵥ WithLp.ofLp x)
  intro x
  have h1 := FixedSpectrumAffine.actual_affine_precision_query hd hκ O1
  have h2 := FixedSpectrumAffine.actual_affine_precision_query hd hκ O2
  dsimp only at h1 h2
  constructor
  · intro h
    calc
      reply1 2 x = (κ - 1)⁻¹ • (reply1 κ x + (κ - 2) • x) := (h1 x).2
      _ = (κ - 1)⁻¹ • (reply2 κ x + (κ - 2) • x) :=
        congrArg (fun y : EuclideanSpace ℝ (Fin d) =>
          (κ - 1)⁻¹ • (y + (κ - 2) • x)) h
      _ = reply2 2 x := (h2 x).2.symm
  · intro h
    calc
      reply1 κ x = (κ - 1) • reply1 2 x - (κ - 2) • x := (h1 x).1
      _ = (κ - 1) • reply2 2 x - (κ - 2) • x :=
        congrArg (fun y : EuclideanSpace ℝ (Fin d) =>
          (κ - 1) • y - (κ - 2) • x) h
      _ = reply2 κ x := (h2 x).1.symm

#print axioms FixedSpectrumAffine.actual_affine_precision_query
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query | throwError "Missing actual fixed-spectrum reply theorem"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing actual fixed-spectrum proof"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL COMPILED ASTIS PARENTS {parents}"
