"""First actual producer proof after sealed-type and independent topology admission."""
from pathlib import Path
import json

workspace = Path(__file__).resolve().parent
seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
signature = seal['producer']['signature']
setup = signature.split(' :\n', 1)[1].split('  (∀ i : Fin d, Integrable', 1)[0]
header = '''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Analysis.CStarAlgebra.Matrix

/-! Exact first moments of the original-experiment closed-cutoff matrices.
The existing canonical row law and truncated radial moment remain shared nodes.
No row-law, integrability or mean certificate is a public premise. -/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean

'''
body = '''  classical
  dsimp only
''' + setup + '''  let ν : Measure E := stdGaussian E
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let good : Set E := {x | ‖x‖ ^ 2 ≤ L}
  let G : E → M := fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let kept : E → M := good.indicator G
  have moment := FixedSpectrumTruncatedRowMoment.actual_truncated_row_second_moment
    (d := d) (q := q) hq
  change Integrable kept ν ∧ (∫ x, kept x ∂ν) = a • (1 : M) at moment
  have row_law (i : Fin d) : MeasurePreserving (row i) μ ν :=
    FixedSpectrumSourceRowLaw.actual_source_row_marginal_law hq i
  have actual_kept_integrable (i : Fin d) :
      Integrable (fun ω => kept (row i ω)) μ :=
    (row_law i).integrable_comp_of_integrable moment.1
  have actual_kept_mean (i : Fin d) :
      (∫ ω, kept (row i ω) ∂μ) = a • (1 : M) := by
    have measurable_on_map : AEStronglyMeasurable kept (Measure.map (row i) μ) := by
      rw [(row_law i).map_eq]
      exact moment.1.aestronglyMeasurable
    have transport := integral_map (row_law i).measurable.aemeasurable measurable_on_map
    rw [(row_law i).map_eq] at transport
    exact transport.symm.trans moment.2
  let feature : Fin d → M := fun i => Matrix.vecMulVec (t i) (t i)
  let tensor : Fin d → M →ₗ[ℝ] N := fun i =>
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N).flip (feature i)
  let scaled : Fin d → M →L[ℝ] N := fun i => (d : ℝ)⁻¹ • (tensor i).toContinuousLinearMap
  have actual_image (i : Fin d) : Y i = fun ω => scaled i (kept (row i ω)) := by
    funext ω
    change (if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker (G (row i ω)) (feature i) else 0) =
        (d : ℝ)⁻¹ • Matrix.kronecker (kept (row i ω)) (feature i)
    by_cases hω : ‖row i ω‖ ^ 2 ≤ L
    · simp [hω, kept, good]
    · simp [hω, kept, good]
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    ∀ i : Fin d, (∫ ω, Y i ω ∂μ) =
      (a / (d : ℝ)) • Matrix.kronecker (1 : M) (feature i)
  refine ⟨?_, ?_⟩
  · intro i
    rw [actual_image]
    exact (scaled i).integrable_comp (actual_kept_integrable i)
  · intro i
    calc
      (∫ ω, Y i ω ∂μ) = scaled i (∫ ω, kept (row i ω) ∂μ) := by
        rw [actual_image]
        exact (scaled i).integral_comp_comm (actual_kept_integrable i)
      _ = scaled i (a • (1 : M)) := congrArg (scaled i) (actual_kept_mean i)
      _ = a • scaled i (1 : M) := (scaled i).map_smul a (1 : M)
      _ = (a / (d : ℝ)) • Matrix.kronecker (1 : M) (feature i) := by
        change a • ((d : ℝ)⁻¹ • Matrix.kronecker (1 : M) (feature i)) = _
        simp only [smul_smul, div_eq_mul_inv]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
'''
path = Path(seal['producer']['planned_file'])
with path.open('x') as out:
    out.write(header + 'theorem actual_source_truncated_matrix_means\n' + signature + ':= by\n' + body)
print(str(path))
