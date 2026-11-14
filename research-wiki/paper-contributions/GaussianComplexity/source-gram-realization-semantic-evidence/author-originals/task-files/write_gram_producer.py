from pathlib import Path
import json
W=Path(__file__).resolve().parent
s=json.loads((W/'statement-seal-v1.unclaimed.json').read_bytes())['producer']['signature']
aliases=s[s.index('  let D :='):s.index('  ∀ ω : Ω, G ω →')]
# Canonical existing mean/frame APIs, finite linear assembly only. Retain the
# earlier private sum consumer; it is not imported/promoted into a public node.
old=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixMean.lean').read_text()
assembly=old[old.index('  let M :='):old.index('  have weighted_integrable')]
assembly='\n'.join(x for x in assembly.split('\n') if not x.startswith('  let w : Fin d → ℝ'))
proof=r'''  have inv_sqrt_square :
      (Real.sqrt (d : ℝ))⁻¹ * (Real.sqrt (d : ℝ))⁻¹ = (d : ℝ)⁻¹ := by
    calc
      _ = ((Real.sqrt (d : ℝ)) ^ 2)⁻¹ := by rw [pow_two, mul_inv]
      _ = _ := by rw [Real.sq_sqrt (by positivity)]
  have actual_row_outer (i : Fin d) (ω : Ω) (hi : ‖row i ω‖ ^ 2 ≤ L)
      (u v : Fin (q + 1) × Fin (q + 1)) :
      B ω i u * B ω i v = Y i ω u v := by
    calc
      _ = ((Real.sqrt (d : ℝ))⁻¹ * (Real.sqrt (d : ℝ))⁻¹) *
          ((row i ω u.1 * row i ω v.1) * (t i u.2 * t i v.2)) := by
        dsimp only [B]
        ring
      _ = _ := by
        rw [inv_sqrt_square]
        simp only [Y, if_pos hi, Matrix.smul_apply, Matrix.kronecker,
          Matrix.kroneckerMap_apply, Matrix.vecMulVec_apply, smul_eq_mul]
        rfl
  have actual_gram (ω : Ω) (hG : G ω) :
      (B ω).transpose * B ω = ∑ i : Fin d, Y i ω := by
    ext u v
    simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.sum_apply]
    apply Finset.sum_congr rfl
    intro i _
    exact actual_row_outer i ω (hG i) u v
  have actual_weighted_gram (ω : Ω) (hG : G ω) :
      (B ω).transpose * Matrix.diagonal w * B ω = ∑ i : Fin d, w i • Y i ω := by
    ext u v
    simp only [Matrix.mul_apply, Matrix.mul_diagonal, Matrix.transpose_apply,
      Matrix.sum_apply, Matrix.smul_apply, smul_eq_mul]
    apply Finset.sum_congr rfl
    intro i _
    calc
      B ω i u * w i * B ω i v = w i * (B ω i u * B ω i v) := by ring
      _ = w i * Y i ω u v := by rw [actual_row_outer i ω (hG i) u v]
  change ∀ ω : Ω, G ω →
    ((∑ i : Fin d, Z i ω) = (B ω).transpose * B ω - a • (1 : N)) ∧
    ((∑ i : Fin d, w i • Z i ω) = (B ω).transpose * Matrix.diagonal w * B ω)
  intro ω hG
  constructor
  · calc
      (∑ i : Fin d, Z i ω) = (∑ i : Fin d, Y i ω) - a • (1 : N) := by
        simp only [Z, mean, Finset.sum_sub_distrib, mean_sum]
      _ = _ := by rw [actual_gram ω hG]
  · calc
      (∑ i : Fin d, w i • Z i ω) =
          (∑ i : Fin d, w i • Y i ω) - (∑ i : Fin d, w i • mean i) := by
        simp only [Z, smul_sub, Finset.sum_sub_distrib]
      _ = (∑ i : Fin d, w i • Y i ω) := by
        change (∑ i : Fin d, w i • Y i ω) -
          (∑ i : Fin d, w i • (∫ ω, Y i ω ∂μ)) = _
        rw [weighted_mean_sum, sub_zero]
      _ = _ := (actual_weighted_gram ω hG).symm
'''
header='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram

/-! Actual original-experiment centered Gram realizations on the literal closed
all-row cutoff event. Actual means and cosine-frame sums are internal inputs;
no arbitrary B, mean, Gram, frame, bias or probability certificate is supplied. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceGramRealization

theorem actual_source_centered_gram_realizations
'''
out=header+s+' := by\n  classical\n  dsimp only\n'+aliases+assembly+proof+'\nend AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceGramRealization\n'
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceGramRealization.lean')
with P.open('x') as f:f.write(out)
print(json.dumps({'P_file':str(P),'lines':len(out.splitlines()),'exact_sealed_signature_retained':s in out,'new_proof_body_written':True}))
