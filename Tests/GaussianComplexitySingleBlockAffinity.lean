import AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity
import Lean.Util.FoldConsts

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity
set_option autoImplicit false

-- A genuine scalar consumer of the actual affinity. This is not an assertion
-- about independent-block laws, coordinates, product densities or amplified TV.
example {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let qpos : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νpos
    let qneg : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νneg
    let a : ℝ := ∫ x, Real.sqrt (qpos x * qneg x)
    ∀ k : ℕ, a ^ k ≤ Real.exp
      (-((k : ℝ) / 8) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) := by
  dsimp only
  have h := single_block_affinity_bound hn hκ
  dsimp only at h
  intro k
  have ha := h.2.2.2.2.1.trans h.2.2.2.2.2
  calc
    _ ≤ (Real.exp (-(1 / 8 : ℝ) *
        Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ))) ^ k :=
      pow_le_pow_left₀ h.2.1 ha k
    _ = _ := by
      rw [← Real.exp_nat_mul]
      congr 1
      ring

#print axioms single_block_affinity_bound
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity.single_block_affinity_bound | throwError "Missing actual source target"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing actual proof"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL COMPILED SOURCE PARENTS {parents}"
