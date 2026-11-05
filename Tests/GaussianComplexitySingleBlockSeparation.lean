import AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation
import Mathlib.Tactic.NormNum.RealSqrt
import Lean.Util.FoldConsts

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation
set_option autoImplicit false

-- Actual probability laws, inclusive source boundary, odd real half exponent.
example :
    let μ := orthogonalHaar 3
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 3) ℝ | (O : Matrix (Fin 3) (Fin 3) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 3) ℝ | (O : Matrix (Fin 3) (Fin 3) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin 3) ℝ → Measure (EuclideanSpace ℝ (Fin 3)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
        (singleBlockPrecision 4 O)⁻¹
    let Ppos := νpos.bind γ
    let Pneg := νneg.bind γ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin 3)),
      MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|}
    (1 / 126 : ℝ) ≤ δ ∧ Ppos ≠ Pneg := by
  dsimp only
  have h := (single_block_separation (n := 3) (κ := 4) (by decide) (by norm_num)).2
  norm_num at h
  refine ⟨h, ?_⟩
  intro heq
  rw [heq] at h
  simp only [sub_self, abs_zero] at h
  have hz : {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin 3)),
      MeasurableSet B ∧ z = 0} = {0} := by
    ext z
    simp only [Set.mem_ofPred_eq, Set.mem_singleton_iff]
    constructor
    · rintro ⟨_, _, hz⟩
      exact hz
    · intro hz
      exact ⟨∅, MeasurableSet.empty, hz⟩
  rw [hz, csSup_singleton] at h
  norm_num at h

-- Actual laws again, even dimension and non-boundary condition number.
example :
    let μ := orthogonalHaar 4
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 4) ℝ | (O : Matrix (Fin 4) (Fin 4) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin 4) ℝ | (O : Matrix (Fin 4) (Fin 4) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin 4) ℝ → Measure (EuclideanSpace ℝ (Fin 4)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin 4))
        (singleBlockPrecision 9 O)⁻¹
    let Ppos := νpos.bind γ
    let Pneg := νneg.bind γ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin 4)),
      MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|}
    (1 / 80 : ℝ) ≤ δ := by
  have h := (single_block_separation (n := 4) (κ := 9) (by decide) (by norm_num)).2
  norm_num at h
  exact h

#print axioms single_block_separation
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation.single_block_separation | throwError "Target missing"
  let some body := info.value? (allowOpaque := true) | throwError "Body missing"
  let parents := body.getUsedConstants.filter fun n =>
    n.toString.startsWith "AutoSamplingTheory" ||
    n.toString.contains "one_add_mul_self_le_rpow_one_add"
  logInfo m!"ACTUAL COMPILED PARENTS {parents}"
