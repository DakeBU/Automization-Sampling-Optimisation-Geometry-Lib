import AutoSamplingTheory.ExampleCases.GaussianComplexity.AffinityTensorization
import AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity
import Lean.Util.FoldConsts

open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity
set_option autoImplicit false

-- This consumer bounds the intrinsic RN-affinity of the actual ambient
-- Gaussian-mixture laws for all source parameters, including d % n = 0.
-- The pre-existing scalar power estimate alone does not assert this quantity.
example {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) :
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
    let F : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      Real.sqrt (((Mpos.rnDeriv volume) x).toReal * ((Mneg.rnDeriv volume) x).toReal)
    (∫ x, F x) ≤ Real.exp
      (-(((d / n : ℕ) : ℝ) / 8) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) := by
  have ht := AffinityTensorization.actual_affinity_tensorization hn hnd hκ
  have hb := SingleBlockAffinity.single_block_affinity_bound hn hκ
  dsimp only at ht hb ⊢
  rw [ht.2.2.2]
  have ha := hb.2.2.2.2.1.trans hb.2.2.2.2.2
  calc
    _ ≤ (Real.exp (-(1 / 8 : ℝ) *
        Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ))) ^ (d / n) :=
      pow_le_pow_left₀ hb.2.1 ha (d / n)
    _ = _ := by
      rw [← Real.exp_nat_mul]
      congr 1
      ring

#print axioms AffinityTensorization.actual_affinity_tensorization
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.AffinityTensorization.actual_affinity_tensorization | throwError "Missing actual source target"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing actual proof"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL COMPILED SOURCE PARENTS {parents}"
