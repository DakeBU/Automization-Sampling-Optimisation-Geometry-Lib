import AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification
import Lean.Util.FoldConsts
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity
set_option autoImplicit false

-- A true-law, fixed-accuracy separation consumer. The threshold is explicit
-- in the source parameters, and no scalar surrogate is substituted for TV.
example {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ)
    (hscale : Real.log 2 ≤ (((d / n : ℕ) : ℝ) / 8) *
      Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) :
    letI : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let Dpos := (Measure.pi (fun _ : Fin (d / n) => νpos)).map (blockPrecision κ)
    let Dneg := (Measure.pi (fun _ : Fin (d / n) => νneg)).map (blockPrecision κ)
    let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
      fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
    let Mpos := Dpos.bind γ
    let Mneg := Dneg.bind γ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)),
      MeasurableSet B ∧ z = |Mpos.real B - Mneg.real B|}
    (1 / 2 : ℝ) ≤ δ := by
  have h := TVAmplification.actual_averaged_tv_lower_bound hn hnd hκ
  dsimp only at h ⊢
  have he : Real.exp (-(((d / n : ℕ) : ℝ) / 8) *
      Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) ≤ (1 / 2 : ℝ) := by
    calc
      _ ≤ Real.exp (-Real.log 2) := Real.exp_le_exp.mpr (by linarith [hscale])
      _ = _ := by rw [Real.exp_neg, Real.exp_log (by norm_num : (0 : ℝ) < 2)]; norm_num
  linarith

#print axioms TVAmplification.actual_averaged_tv_lower_bound
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification.actual_averaged_tv_lower_bound | throwError "Missing actual source target"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing actual proof"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL COMPILED SOURCE PARENTS {parents}"
