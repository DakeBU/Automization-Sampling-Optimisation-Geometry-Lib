"""Actual finite-sum expectation consumer of the new original-experiment means."""
from pathlib import Path
import json

workspace = Path(__file__).resolve().parent
seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
signature = seal['actual_private_consumer']['signature']
setup = signature.split(' :\n', 1)[1].split('  Integrable (fun ω => ∑', 1)[0]
header = '''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram

/-! Both actual finite sums are integrable and have the source Ex110 expectations.
The actual-Y producer and exact cosine-frame identities are material inputs;
no law, integrability, Gram, mean or independence certificate is a binder. -/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixMean

open AutoSamplingTheory.ExampleCases.GaussianComplexity

'''
body = '''  classical
  dsimp only
''' + setup + '''  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let feature : Fin d → M := fun i => Matrix.vecMulVec (t i) (t i)
  let tensor : M →ₗ[ℝ] N :=
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N) (1 : M)
  let K : Fin d → N := fun i => tensor (feature i)
  have moments := FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means
    (d := d) (q := q) hq
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    (∀ i : Fin d, (∫ ω, Y i ω ∂μ) = (a / (d : ℝ)) • K i) at moments
  have half_grid (i : Fin d) :
      ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ) = θ i := by
    dsimp only [θ]
    ring
  have frame := FixedSpectrumCosineGram.actual_cosine_frame_gram (d := d) (q := q) hq
  dsimp only at frame
  simp_rw [half_grid] at frame
  change t.transpose * t = (d : ℝ) • (1 : M) ∧
    t.transpose * Matrix.diagonal w * t = 0 ∧ _ at frame
  have gram : (∑ i : Fin d, feature i) = (d : ℝ) • (1 : M) := by
    ext j k
    calc
      (∑ i : Fin d, feature i) j k = ∑ i : Fin d, t i j * t i k :=
        Matrix.sum_apply j k Finset.univ feature
      _ = ((d : ℝ) • (1 : M)) j k := by
        simpa only [Matrix.mul_apply, Matrix.transpose_apply] using
          congrFun (congrFun frame.1 j) k
  have weighted_gram : (∑ i : Fin d, w i • feature i) = 0 := by
    ext j k
    have weighted_entry := congrFun (congrFun frame.2.1 j) k
    change (∑ i : Fin d, (t.transpose * Matrix.diagonal w) j i * t i k) = 0 at weighted_entry
    simp only [Matrix.mul_diagonal, Matrix.transpose_apply] at weighted_entry
    calc
      (∑ i : Fin d, w i • feature i) j k = ∑ i : Fin d, w i * (t i j * t i k) :=
        Matrix.sum_apply j k Finset.univ (fun i => w i • feature i)
      _ = ∑ i : Fin d, t i j * w i * t i k := by
        apply Finset.sum_congr rfl
        intro i _
        ring
      _ = (0 : M) j k := weighted_entry
  have tensor_one : tensor (1 : M) = (1 : N) := by
    change Matrix.kronecker (1 : M) (1 : M) = (1 : N)
    dsimp only [Matrix.kronecker]
    exact Matrix.one_kronecker_one
  have tensor_gram : (∑ i : Fin d, K i) = (d : ℝ) • (1 : N) := by
    calc
      (∑ i : Fin d, K i) = tensor (∑ i : Fin d, feature i) := (map_sum tensor _ _).symm
      _ = (d : ℝ) • tensor (1 : M) := by rw [gram, map_smul]
      _ = (d : ℝ) • (1 : N) := by rw [tensor_one]
  have weighted_tensor : (∑ i : Fin d, w i • K i) = 0 := by
    calc
      (∑ i : Fin d, w i • K i) = tensor (∑ i : Fin d, w i • feature i) := by
        simp only [map_sum, map_smul]
        rfl
      _ = 0 := by rw [weighted_gram, map_zero]
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by omega)
  have mean_sum : (∑ i : Fin d, ∫ ω, Y i ω ∂μ) = a • (1 : N) := by
    calc
      (∑ i : Fin d, ∫ ω, Y i ω ∂μ) = (a / (d : ℝ)) • (∑ i : Fin d, K i) := by
        simp_rw [moments.2]
        exact (Finset.smul_sum _ _ _).symm
      _ = a • (1 : N) := by
        rw [tensor_gram, smul_smul, div_mul_cancel₀ a hd]
  have weighted_mean_sum : (∑ i : Fin d, w i • (∫ ω, Y i ω ∂μ)) = 0 := by
    calc
      (∑ i : Fin d, w i • (∫ ω, Y i ω ∂μ)) =
          (a / (d : ℝ)) • (∑ i : Fin d, w i • K i) := by
        rw [Finset.smul_sum]
        apply Finset.sum_congr rfl
        intro i _
        rw [moments.2 i]
        exact smul_comm _ _ _
      _ = 0 := by rw [weighted_tensor, smul_zero]
  have weighted_integrable (i : Fin d) : Integrable (fun ω => w i • Y i ω) μ :=
    (moments.1 i).smul (w i)
  change Integrable (fun ω => ∑ i : Fin d, Y i ω) μ ∧
    Integrable (fun ω => ∑ i : Fin d, w i • Y i ω) μ ∧
    (∫ ω, ∑ i : Fin d, Y i ω ∂μ) = a • (1 : N) ∧
    (∫ ω, ∑ i : Fin d, w i • Y i ω ∂μ) = 0
  refine ⟨integrable_finsetSum _ (fun i _ => moments.1 i),
    integrable_finsetSum _ (fun i _ => weighted_integrable i), ?_, ?_⟩
  · rw [integral_finsetSum _ (fun i _ => moments.1 i)]
    exact mean_sum
  · rw [integral_finsetSum _ (fun i _ => weighted_integrable i)]
    simp_rw [integral_smul]
    exact weighted_mean_sum

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixMean
'''
path = Path(seal['actual_private_consumer']['planned_file'])
with path.open('x') as out:
    out.write(header + 'private theorem actual_source_truncated_sum_means\n' + signature + ':= by\n' + body)
print(str(path))
