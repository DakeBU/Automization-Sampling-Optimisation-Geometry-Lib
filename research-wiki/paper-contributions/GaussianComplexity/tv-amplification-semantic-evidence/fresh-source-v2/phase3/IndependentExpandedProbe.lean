import AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification
import Lean.Util.FoldConsts
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
set_option autoImplicit false
-- Exact anonymous packet statement, checked without alias/surrogate hypotheses.
example :
∀ {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ),
    letI : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let B : Matrix.orthogonalGroup (Fin n) ℝ → Matrix (Fin n) (Fin n) ℝ :=
      fun O => ((κ + 1) / 2) • (1 : Matrix (Fin n) (Fin n) ℝ) -
        ((κ - 1) / 4) • ((O : Matrix (Fin n) (Fin n) ℝ) +
          (O : Matrix (Fin n) (Fin n) ℝ).transpose)
    let μ := (Measure.haarMeasure (⊤ : TopologicalSpace.PositiveCompacts (Matrix.orthogonalGroup (Fin n) ℝ)))
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let Dpos := (Measure.pi (fun _ : Fin (d / n) => νpos)).map (fun Os : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ => Matrix.reindex e e
      (Matrix.fromBlocks (Matrix.blockDiagonal (fun j => B (Os j))) 0 0
        (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ)))
    let Dneg := (Measure.pi (fun _ : Fin (d / n) => νneg)).map (fun Os : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ => Matrix.reindex e e
      (Matrix.fromBlocks (Matrix.blockDiagonal (fun j => B (Os j))) 0 0
        (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ)))
    let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
      fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
    let Mpos := Dpos.bind γ
    let Mneg := Dneg.bind γ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin d)),
      MeasurableSet B ∧ z = |Mpos.real B - Mneg.real B|}
    1 - Real.exp (-(((d / n : ℕ) : ℝ) / 8) *
      Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ)) ≤ δ := by
  exact AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification.actual_averaged_tv_lower_bound
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification.actual_averaged_tv_lower_bound
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.AffinityTensorization.actual_affinity_tensorization
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity.single_block_affinity_bound
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw.actual_averaged_block_product
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation.single_block_separation
#print axioms AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity.normalized_density_tv_affinity
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification.actual_averaged_tv_lower_bound | throwError "missing target"
  let some proof := info.value? (allowOpaque := true) | throwError "missing checked proof"
  logInfo m!"INDEPENDENT ELABORATED TYPE {info.type}"
  logInfo m!"INDEPENDENT ACTUAL ASTIS PARENTS {proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"}"
