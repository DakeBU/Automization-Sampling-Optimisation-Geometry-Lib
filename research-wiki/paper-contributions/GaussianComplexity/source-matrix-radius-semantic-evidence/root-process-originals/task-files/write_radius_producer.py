"""Assemble the unchanged sealed actual producer with existing real operator-norm APIs."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
seal=json.loads((W/'statement-seal-v1.json').read_bytes())
helpers=(W/'RankOneNormDraft.lean').read_text()
assert 'dsimp only [K, Matrix.kronecker]' in helpers
helpers=helpers.split('namespace RadiusNormDraft\n',1)[1].rsplit('end RadiusNormDraft',1)[0]
helpers=helpers.replace('\ntheorem ','\nprivate theorem ')
if helpers.startswith('theorem '):helpers='private '+helpers
sig=seal['producer']['signature']
prefix=sig[sig.index('  let D :='):sig.index('  (∀ i : Fin d, ∀ ω : Ω,')]
body=prefix+r'''  let S : Fin d → ℝ := fun i => ∑ k : Fin (q + 1), (t i k) ^ 2
  let F : Fin d → Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ :=
    fun i => Matrix.vecMulVec (t i) (t i)
  let K : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => Matrix.kronecker (1 : Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ) (F i)
  let a : ℝ := (∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
    (fun y => ‖y‖ ^ 2) x ∂stdGaussian E) / r
  change (∀ i : Fin d, ∀ ω : Ω, ‖Y i ω‖ ≤ 2 * r * L / (d : ℝ)) ∧
    (∀ i : Fin d, ‖∫ ω, Y i ω ∂μ‖ ≤ 2 * r / (d : ℝ))
  have hd : (0 : ℝ) < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hr : 0 < r := by dsimp [r]; positivity
  have hscale : (1 : ℝ) ≤ 1000 * (d : ℝ) := by
    have hd2 : (2 : ℝ) ≤ (d : ℝ) := by exact_mod_cast (show 2 ≤ d by omega)
    linarith
  have hL : 0 ≤ L := by
    have hlog := Real.log_nonneg hscale
    dsimp only [L]
    linarith
  have hS0 (i : Fin d) : 0 ≤ S i := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have frame := FixedSpectrumCosineGram.actual_cosine_frame_gram (d := d) (q := q) hq
  have hS (i : Fin d) : S i ≤ 2 * r := by
    simpa only [S, t, θ, r, Nat.cast_add, Nat.cast_one, add_sub_assoc,
      show (1 : ℝ) - 1 / 2 = 1 / 2 by norm_num] using frame.2.2 i
  have hm := FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means
    (d := d) (q := q) hq
  change (∀ i : Fin d, Integrable (Y i) μ) ∧
    (∀ i : Fin d, (∫ ω, Y i ω ∂μ) = (a / (d : ℝ)) • K i) at hm
  have moment := AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian
    (E := E)
  have hgood : MeasurableSet {y : E | ‖y‖ ^ 2 ≤ L} :=
    measurableSet_le (by fun_prop) measurable_const
  have hret := moment.1.indicator hgood
  have hret0 : 0 ≤ ∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
      (fun y => ‖y‖ ^ 2) x ∂stdGaussian E := by
    apply integral_nonneg
    intro x
    by_cases hx : ‖x‖ ^ 2 ≤ L
    · simp [Set.indicator, hx]
    · simp [Set.indicator, hx]
  have hretle : (∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
      (fun y => ‖y‖ ^ 2) x ∂stdGaussian E) ≤ r := by
    calc
      _ ≤ ∫ x : E, ‖x‖ ^ 2 ∂stdGaussian E := by
        apply integral_mono hret moment.1
        intro x
        by_cases hx : ‖x‖ ^ 2 ≤ L <;> simp [Set.indicator, hx]
      _ = r := by simpa [E, r] using moment.2
  have ha0 : 0 ≤ a := div_nonneg hret0 hr.le
  have ha1 : a ≤ 1 := (div_le_one hr).2 hretle
  have hK (i : Fin d) : ‖K i‖ = S i := identity_rankone_norm
    (m := Fin (q + 1)) (t i)
  constructor
  · intro i ω
    have htnorm : ‖(WithLp.toLp 2 (t i) : E)‖ ^ 2 = S i := by
      simp [EuclideanSpace.norm_sq_eq, S, Real.norm_eq_abs, sq_abs]
    have hTensor : ‖Matrix.kronecker
        (Matrix.vecMulVec (row i ω).ofLp (row i ω).ofLp)
        (Matrix.vecMulVec (t i) (t i))‖ = ‖row i ω‖ ^ 2 * S i := by
      simpa only [WithLp.ofLp_toLp, htnorm] using
        rankone_tensor_norm (row i ω) (WithLp.toLp 2 (t i) : E)
    by_cases hx : ‖row i ω‖ ^ 2 ≤ L
    · dsimp only [Y]
      rw [if_pos hx, norm_smul, Real.norm_eq_abs,
        abs_of_nonneg (inv_nonneg.mpr hd.le), hTensor]
      calc
        _ ≤ (d : ℝ)⁻¹ * (L * (2 * r)) :=
          mul_le_mul_of_nonneg_left (mul_le_mul hx (hS i) (hS0 i) hL)
            (inv_nonneg.mpr hd.le)
        _ = 2 * r * L / (d : ℝ) := by rw [div_eq_mul_inv]; ring
    · simp only [Y, if_neg hx, norm_zero]
      exact div_nonneg (mul_nonneg (mul_nonneg (by norm_num) hr.le) hL) hd.le
  · intro i
    rw [hm.2 i, norm_smul, Real.norm_eq_abs,
      abs_of_nonneg (div_nonneg ha0 hd.le), hK]
    calc
      _ ≤ (1 / (d : ℝ)) * (2 * r) :=
        mul_le_mul ((div_le_div_iff_of_pos_right hd).2 ha1) (hS i) (hS0 i)
          (div_nonneg zero_le_one hd.le)
      _ = 2 * r / (d : ℝ) := by ring
'''
header='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.LinearMap

/-!
# Actual truncated Gaussian summand and mean norms

The literal original product experiment and closed cutoff are unchanged.
All moment, sign and operator-norm estimates are internal proof obligations.
-/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
'''
code=header+helpers+'\ntheorem actual_source_truncated_matrix_norm_bounds\n'+sig+' := by\n  classical\n  dsimp only\n'+body+'\nend AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius\n'
p=Path(seal['producer']['planned_file'])
with p.open('x') as f:f.write(code)
record={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exact_producer_signature_sha256':seal['producer']['signature_sha256'],'statement_changed':False,'proof_status':'FIRST_ATTEMPT_NOT_YET_COMPILED'}
with (W/'producer-first-attempt-source.json').open('x') as f:f.write(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
