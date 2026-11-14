"""Implement the unchanged sealed actual Gaussian consumer of the shared PSD interface."""
from pathlib import Path
import hashlib
import json

workspace = Path(__file__).resolve().parent
runner = Path('.astis/huanjian-resume-20261103')
receipt = json.loads((runner / '20261112T145113476724Z-real-matrix-positive-integral-producer-real-star-import-v2.receipt.json').read_bytes())
assert receipt['exit_code'] == 0
assert hashlib.sha256(Path(receipt['log']).read_bytes()).hexdigest() == receipt['log_sha256']
signature = Path('.astis/huanjian-gc-source-matrix-variance-20261112/producer-signature.original.txt').read_text()
assert hashlib.sha256(signature.encode()).hexdigest() == 'd5ac54443c79ea7b35b09ddcd6b5e3c40bef081bbe4f196cae5ab3ead35aa2ea'
setup = signature.split(':\n', 1)[1].split('\n  (∀ i : Fin d, Integrable', 1)[0]
assert setup.startswith('  let D :=') and setup.endswith('2) / (d : ℝ)')
header = '''import AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound

/-! Actual source-experiment uncentered squared moments, arXiv2610.20492v1 C.2.
The original column-product law, physical rows and closed cutoff stay literal.
The shared positivity-integral node is used on a genuinely integrable pointwise
PSD majorant residual; no moment/positivity certificate is a source input. -/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
open AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
set_option autoImplicit false

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance

theorem actual_source_truncated_matrix_second_moments
'''
body = '''
  let ν : Measure E := stdGaussian E
  let M := Matrix (Fin (q + 1)) (Fin (q + 1)) ℝ
  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let G : E → M := fun x => Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)
  let weighted : E → M := fun x => R x • G x
  let feature : Fin d → M := fun i => Matrix.vecMulVec (t i) (t i)
  let S : Fin d → ℝ := fun i => ∑ k : Fin (q + 1), (t i k) ^ 2
  let K : Fin d → N := fun i => Matrix.kronecker (1 : M) (feature i)
  let α : ℝ := (r + 2) / (d : ℝ) ^ 2
  let B : N := α • (∑ i : Fin d, S i • K i)
  let good : Fin d → Set Ω := fun i => {ω | ‖row i ω‖ ^ 2 ≤ L}
  let squared : Fin d → Ω → N := fun i ω => Y i ω * Y i ω
  let c : Fin d → ℝ := fun i => S i / (d : ℝ) ^ 2
  let tensor : Fin d → M →ₗ[ℝ] N := fun i =>
    (Matrix.kroneckerBilinear : M →ₗ[ℝ] M →ₗ[ℝ] N).flip (feature i)
  let scaled : Fin d → M →L[ℝ] N := fun i => c i • (tensor i).toContinuousLinearMap
  let W : Fin d → Ω → N := fun i ω => scaled i (weighted (row i ω))

  -- Canonical fourth moment, transported by the actual physical row map.
  have moment := FixedSpectrumRadialFourthMoment.actual_radial_fourth_moment_matrix
    (d := d) (q := q) hq
  change Integrable weighted ν ∧ (∫ x, weighted x ∂ν) = (r + 2) • (1 : M) at moment
  have row_law (i : Fin d) : MeasurePreserving (row i) μ ν :=
    FixedSpectrumSourceRowLaw.actual_source_row_marginal_law hq i
  have actual_weighted_integrable (i : Fin d) :
      Integrable (fun ω => weighted (row i ω)) μ :=
    (row_law i).integrable_comp_of_integrable moment.1
  have actual_weighted_mean (i : Fin d) :
      (∫ ω, weighted (row i ω) ∂μ) = (r + 2) • (1 : M) := by
    have measurable_on_map : AEStronglyMeasurable weighted (Measure.map (row i) μ) := by
      rw [(row_law i).map_eq]
      exact moment.1.aestronglyMeasurable
    have transport := integral_map (row_law i).measurable.aemeasurable measurable_on_map
    rw [(row_law i).map_eq] at transport
    exact transport.symm.trans moment.2
  have W_integrable (i : Fin d) : Integrable (W i) μ :=
    (scaled i).integrable_comp (actual_weighted_integrable i)
  have good_measurable (i : Fin d) : MeasurableSet (good i) := by
    dsimp only [good]
    exact measurableSet_le ((row_law i).measurable.norm.pow_const 2) measurable_const

  -- Both ordinary rank-one squares, retaining the actual row's own cutoff.
  have rank_square (v : Fin (q + 1) → ℝ) :
      Matrix.vecMulVec v v * Matrix.vecMulVec v v =
        (∑ k : Fin (q + 1), (v k) ^ 2) • Matrix.vecMulVec v v := by
    rw [Matrix.vecMulVec_mul_vecMulVec, Matrix.vecMulVec_smul]
    congr 1
    simp [dotProduct, pow_two]
  have gram_square (x : E) : G x * G x = R x • G x := by
    have h := rank_square (WithLp.ofLp x)
    have radius_sum : (∑ k : Fin (q + 1), (x k) ^ 2) = R x :=
      (EuclideanSpace.real_norm_sq_eq x).symm
    simpa only [radius_sum] using h
  have feature_square (i : Fin d) : feature i * feature i = S i • feature i :=
    rank_square (t i)
  have squared_as_indicator (i : Fin d) : squared i = (good i).indicator (W i) := by
    funext ω
    by_cases hω : ω ∈ good i
    · have hcut : ‖row i ω‖ ^ 2 ≤ L := hω
      simp only [squared, Y, if_pos hcut, Set.indicator_of_mem hω]
      change ((d : ℝ)⁻¹ • Matrix.kronecker (G (row i ω)) (feature i)) *
        ((d : ℝ)⁻¹ • Matrix.kronecker (G (row i ω)) (feature i)) =
          c i • Matrix.kronecker (R (row i ω) • G (row i ω)) (feature i)
      dsimp only [Matrix.kronecker]
      rw [smul_mul_assoc, mul_smul_comm, ← Matrix.mul_kronecker_mul,
        gram_square (row i ω), feature_square i]
      ext a b
      change (d : ℝ)⁻¹ * ((d : ℝ)⁻¹ *
        ((R (row i ω) * G (row i ω) a.1 b.1) * (S i * feature i a.2 b.2))) =
          c i * ((R (row i ω) * G (row i ω) a.1 b.1) * feature i a.2 b.2)
      dsimp [c]
      simp only [div_eq_mul_inv]
      ring
    · have hcut : ¬ ‖row i ω‖ ^ 2 ≤ L := hω
      simp [squared, Y, hcut, Set.indicator_of_notMem hω]
  have squared_integrable (i : Fin d) : Integrable (squared i) μ := by
    rw [squared_as_indicator i]
    exact (W_integrable i).indicator (good_measurable i)

  -- The actual untruncated majorant is a nonnegative rank-one matrix.
  have W_positive (i : Fin d) (ω : Ω) : (W i ω).PosSemidef := by
    let x := row i ω
    let v : Fin (q + 1) × Fin (q + 1) → ℝ := fun a => x a.1 * t i a.2
    have rank_positive : (Matrix.vecMulVec v v).PosSemidef := by
      simpa only [star_trivial] using Matrix.posSemidef_vecMulVec_self_star v
    have W_rank : W i ω = (c i * R x) • Matrix.vecMulVec v v := by
      ext a b
      change c i * (R x * (x a.1 * x b.1) * (t i a.2 * t i b.2)) =
        (c i * R x) * ((x a.1 * t i a.2) * (x b.1 * t i b.2))
      ring
    rw [W_rank]
    exact rank_positive.smul (mul_nonneg
      (div_nonneg (Finset.sum_nonneg (fun _ _ => sq_nonneg _)) (sq_nonneg _))
      (sq_nonneg ‖x‖))
  have residual_positive (ω : Ω) :
      ((∑ i : Fin d, W i ω) - ∑ i : Fin d, squared i ω).PosSemidef := by
    rw [← Finset.sum_sub_distrib]
    apply Matrix.posSemidef_sum Finset.univ
    intro i _
    rw [squared_as_indicator i]
    by_cases hω : ω ∈ good i
    · simpa [Set.indicator_of_mem hω] using (Matrix.PosSemidef.zero : (0 : N).PosSemidef)
    · simpa [Set.indicator_of_notMem hω] using W_positive i ω
  have W_sum_integrable : Integrable (fun ω => ∑ i : Fin d, W i ω) μ :=
    integrable_finsetSum Finset.univ (fun i _ => W_integrable i)
  have squared_sum_integrable : Integrable (fun ω => ∑ i : Fin d, squared i ω) μ :=
    integrable_finsetSum Finset.univ (fun i _ => squared_integrable i)
  have integrated_residual :
      (∫ ω, (∑ i : Fin d, W i ω) - ∑ i : Fin d, squared i ω ∂μ).PosSemidef :=
    integral_posSemidef _ (W_sum_integrable.sub squared_sum_integrable)
      (Filter.Eventually.of_forall residual_positive)

  -- Exact tensor/scalar means and the existing canonical weighted-frame bound.
  have W_mean (i : Fin d) : (∫ ω, W i ω ∂μ) = α • (S i • K i) := by
    calc
      (∫ ω, W i ω ∂μ) = scaled i (∫ ω, weighted (row i ω) ∂μ) :=
        (scaled i).integral_comp_comm (actual_weighted_integrable i)
      _ = scaled i ((r + 2) • (1 : M)) := congrArg (scaled i) (actual_weighted_mean i)
      _ = α • (S i • K i) := by
        change c i • Matrix.kronecker ((r + 2) • (1 : M)) (feature i) =
          α • (S i • Matrix.kronecker (1 : M) (feature i))
        dsimp only [Matrix.kronecker]
        rw [Matrix.smul_kronecker, smul_smul, smul_smul]
        congr 1
        dsimp [c, α]
        simp only [div_eq_mul_inv]
        ring
  have W_sum_mean : (∫ ω, ∑ i : Fin d, W i ω ∂μ) = B := by
    rw [integral_finsetSum Finset.univ (fun i _ => W_integrable i)]
    simp_rw [W_mean]
    exact Finset.smul_sum.symm
  rw [integral_sub W_sum_integrable squared_sum_integrable, W_sum_mean,
    integral_finsetSum Finset.univ (fun i _ => squared_integrable i)] at integrated_residual
  have deterministic := FixedSpectrumWeightedFrameBound.actual_weighted_cosine_coefficient_bound
    (d := d) (q := q) hq
  have angle_old (i : Fin d) :
      ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ) = θ i := by
    dsimp [θ]
    ring
  dsimp only at deterministic
  simp_rw [angle_old] at deterministic
  change (C • (1 : N) - B).PosSemidef at deterministic
  change (∀ i : Fin d, Integrable (squared i) μ) ∧
    (C • (1 : N) - ∑ i : Fin d, ∫ ω, squared i ω ∂μ).PosSemidef
  refine ⟨squared_integrable, ?_⟩
  convert deterministic.add integrated_residual using 1
  abel

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance
'''
raw = (header + signature + ':= by\n  classical\n  dsimp only\n' + setup + '\n' + body).encode()
path = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean')
with path.open('xb') as out:
    out.write(raw)
print(json.dumps({'actual_consumer': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'exact_source_signature_unchanged': True, 'shared_producer_already_built': True}))
