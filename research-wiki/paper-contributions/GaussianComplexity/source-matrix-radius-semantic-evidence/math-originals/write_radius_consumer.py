"""Materially consume both actual producer estimates in the exact sealed radius outputs."""
from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
seal=json.loads((W/'statement-seal-v1.json').read_bytes())
sig=seal['actual_private_consumer']['signature']
prefix=sig[sig.index('  let D :='):sig.index('  (∀ i : Fin d, ∀ ω : Ω, ‖Z')]
body=prefix+r'''  change (∀ i : Fin d, ∀ ω : Ω, ‖Z i ω‖ ≤ Rstar) ∧
    (∀ i : Fin d, ∀ ω : Ω, ‖w i • Z i ω‖ ≤ Rstar)
  have bounds := FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds
    (d := d) (q := q) hq
  change (∀ i : Fin d, ∀ ω : Ω, ‖Y i ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ i : Fin d, ‖∫ ω, Y i ω ∂μ‖ ≤ 2 * r / (d : ℝ)) at bounds
  have hz (i : Fin d) (ω : Ω) : ‖Z i ω‖ ≤ Rstar := by
    dsimp only [Z, mean]
    calc
      ‖Y i ω - ∫ ω, Y i ω ∂μ‖ ≤ ‖Y i ω‖ + ‖∫ ω, Y i ω ∂μ‖ := norm_sub_le _ _
      _ ≤ 2 * r * L / (d : ℝ) + 2 * r / (d : ℝ) :=
        add_le_add (bounds.1 i ω) (bounds.2 i)
      _ = Rstar := by dsimp only [Rstar]; ring
  constructor
  · exact hz
  · intro i ω
    rw [norm_smul, Real.norm_eq_abs]
    calc
      |w i| * ‖Z i ω‖ ≤ 1 * ‖Z i ω‖ :=
        mul_le_mul_of_nonneg_right (Real.abs_cos_le_one _) (norm_nonneg _)
      _ = ‖Z i ω‖ := one_mul _
      _ ≤ Rstar := hz i ω
'''
header='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius

/-!
# Actual centered and cosine-weighted summand radius

This private mathematical consumer uses both actual norm estimates, the literal
Bochner mean, and the original product experiment. It is not a public API or a
matrix Bernstein/concentration theorem.
-/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius
'''
code=header+'\nprivate theorem actual_source_centered_summand_radius\n'+sig+' := by\n  classical\n  dsimp only\n'+body+'\nend AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius\n'
p=Path(seal['actual_private_consumer']['planned_file'])
with p.open('x') as f:f.write(code)
record={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'signature_sha256':seal['actual_private_consumer']['signature_sha256'],'statement_changed':False,'proof_status':'FIRST_ATTEMPT_NOT_YET_COMPILED'}
with (W/'consumer-first-attempt-source.json').open('x') as f:f.write(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
