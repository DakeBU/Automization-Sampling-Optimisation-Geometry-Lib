from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
seal=json.loads((W/'statement-seal-v2.json').read_bytes())
matrix='Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ'
def setup(sig):
    lets=sig[sig.index('  letI :'):sig.index('  (∀ i : Fin d, Measurable')]
    return lets+'  letI : BorelSpace ('+matrix+') := ⟨rfl⟩\n'
header='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowIndependence
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean

/-! Actual original-experiment centered matrix structure. All measurability,
integrability, independence, zero-mean and Hermitian obligations are discharged
internally under the sole original source condition. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure

theorem actual_source_centered_matrix_structure
'''
sig=seal['producer']['signature']
body=setup(sig)+r'''
  letI : IsProbabilityMeasure μ := by dsimp only [μ]; infer_instance
  change (∀ i : Fin d, Measurable (Z i)) ∧ iIndepFun Z μ ∧
    (∀ i : Fin d, Integrable (Z i) μ) ∧
    (∀ i : Fin d, (∫ ω, Z i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (Z i ω).IsHermitian)
  let F : Fin d → E → Matrix (Fin (q + 1) × Fin (q + 1))
      (Fin (q + 1) × Fin (q + 1)) ℝ := fun i x =>
    if ‖x‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec x.ofLp x.ofLp) (Matrix.vecMulVec (t i) (t i))
    else 0
  have row_law (i : Fin d) : MeasurePreserving (row i) μ (stdGaussian E) :=
    FixedSpectrumSourceRowLaw.actual_source_row_marginal_law hq i
  have row_independent : iIndepFun row μ :=
    FixedSpectrumSourceRowIndependence.actual_source_rows_independent hq
  have cutoff : MeasurableSet {x : E | ‖x‖ ^ 2 ≤ L} :=
    measurableSet_le (by fun_prop) measurable_const
  have F_measurable (i : Fin d) : Measurable (F i) := by
    apply Measurable.ite cutoff
    · apply Continuous.measurable
      apply continuous_pi
      intro u
      apply continuous_pi
      intro v
      change Continuous (fun x : E =>
        (d : ℝ)⁻¹ * ((x u.1 * x v.1) * (t i u.2 * t i v.2)))
      fun_prop
    · exact measurable_const
  have translated_measurable (i : Fin d) :
      Measurable (fun x : E => F i x - mean i) :=
    (F_measurable i).sub measurable_const
  have Z_measurable (i : Fin d) : Measurable (Z i) :=
    (translated_measurable i).comp (row_law i).measurable
  have Z_independent : iIndepFun Z μ :=
    row_independent.comp (fun i x => F i x - mean i) translated_measurable
  let a : ℝ := (∫ x : E, Set.indicator {y : E | ‖y‖ ^ 2 ≤ L}
    (fun y : E => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  have hm := FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means
    (d := d) (q := q) hq
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    (∀ i : Fin d, mean i = (a / (d : ℝ)) • Matrix.kronecker
      (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ)
      (Matrix.vecMulVec (t i) (t i))) at hm
  have Y_hermitian (i : Fin d) (ω : Ω) : (Y i ω).IsHermitian := by
    change (Y i ω).conjTranspose = Y i ω
    by_cases hx : ‖row i ω‖ ^ 2 ≤ L
    · ext u v
      simp only [Y, if_pos hx, Matrix.conjTranspose_apply, Matrix.smul_apply,
        Matrix.kronecker, Matrix.kroneckerMap_apply, Matrix.vecMulVec_apply,
        smul_eq_mul, star_trivial]
      ring
    · simp [Y, hx]
  have mean_hermitian (i : Fin d) : (mean i).IsHermitian := by
    rw [hm.2 i]
    change ((a / (d : ℝ)) • Matrix.kronecker
      (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ)
      (Matrix.vecMulVec (t i) (t i))).conjTranspose = _
    ext u v
    simp [Matrix.conjTranspose_apply, Matrix.kronecker, Matrix.kroneckerMap,
      Matrix.vecMulVec, eq_comm, mul_comm]
  have Z_integrable (i : Fin d) : Integrable (Z i) μ :=
    (hm.1 i).sub (integrable_const _)
  have Z_mean_zero (i : Fin d) : (∫ ω, Z i ω ∂μ) = 0 := by
    change (∫ ω, Y i ω - mean i ∂μ) = 0
    rw [integral_sub (hm.1 i) (integrable_const _)]
    simp [mean]
  exact ⟨Z_measurable, Z_independent, Z_integrable, Z_mean_zero,
    fun i ω => (Y_hermitian i ω).sub (mean_hermitian i)⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
'''
p=Path(seal['producer']['planned_file']);assert not p.exists();p.write_text(header+sig+' := by\n  classical\n  dsimp only\n'+body)
tsig=seal['actual_private_consumer']['signature']
thead='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure

/-! Private genuine consumer: the literal deterministic cosine-weighted family
retains all five actual centered structural properties. No combined-family
independence, nonzero/sign weight assumption or concentration is claimed. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure

private theorem actual_source_weighted_centered_matrix_structure
'''
tbody=setup(tsig)+r'''
  change (∀ i : Fin d, Measurable (X i)) ∧ iIndepFun X μ ∧
    (∀ i : Fin d, Integrable (X i) μ) ∧
    (∀ i : Fin d, (∫ ω, X i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (X i ω).IsHermitian)
  have hp := FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure
    (d := d) (q := q) hq
  change (∀ i : Fin d, Measurable (Z i)) ∧ iIndepFun Z μ ∧
    (∀ i : Fin d, Integrable (Z i) μ) ∧
    (∀ i : Fin d, (∫ ω, Z i ω ∂μ) = 0) ∧
    (∀ i : Fin d, ∀ ω : Ω, (Z i ω).IsHermitian) at hp
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro i
    exact measurable_const.smul (hp.1 i)
  · exact hp.2.1.comp (fun i A => w i • A)
      (fun _ => measurable_const.smul measurable_id)
  · intro i
    exact (hp.2.2.1 i).const_smul (w i)
  · intro i
    dsimp only [X]
    rw [integral_smul, hp.2.2.2.1 i, smul_zero]
  · intro i ω
    exact (hp.2.2.2.2 i ω).smul (isSelfAdjoint_iff.mpr rfl)

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure
'''
t=Path(seal['actual_private_consumer']['planned_file']);assert not t.exists();t.write_text(thead+tsig+' := by\n  classical\n  dsimp only\n'+tbody)
out=[{'file':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'lines':len(x.read_text().splitlines())} for x in [p,t]]
(W/'first-attempt-source.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
