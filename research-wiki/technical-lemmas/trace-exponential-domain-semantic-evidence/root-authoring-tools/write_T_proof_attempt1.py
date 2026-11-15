from pathlib import Path
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
statement=(w/'T.candidate.v2.txt').read_text()
lets=statement.split('\n',1)[1].split('  ∀ s : ℝ,')[0]
old=(r/'Tests/GaussianComplexityLaplaceTail.lean').read_text()
structure=old[old.index('  have hstructure :='):old.index('  have hd2 :')]
bounds=old[old.index('  have hnormZ ('):old.index('  intro s hs a useCos minus')].replace('ρ','Rstar')
header='''import AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder ENNReal
noncomputable section
namespace AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain

private theorem actual_source_four_trace_mgfs_integrable_positive_and_bounded :
'''
proof=''' := by
  classical
  intro d q hq
  dsimp only
'''+lets+'''  letI : MeasurableSpace M := borel M
  letI : BorelSpace M := ⟨rfl⟩
  letI : IsProbabilityMeasure μ := by
    dsimp only [μ]
    infer_instance
  change ∀ s : ℝ, ∀ useCos minus : Bool,
    let f : Ω → ℝ := fun ω => Matrix.trace (NormedSpace.exp (s • S useCos minus ω))
    let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
    Integrable f μ ∧ (∀ ω, 0 < f ω ∧ f ω ≤ B) ∧
      0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B
'''+structure+bounds+'''  intro s useCos minus
  let f : Ω → ℝ := fun ω => Matrix.trace (NormedSpace.exp (s • S useCos minus ω))
  let B : ℝ := r ^ 2 * Real.exp (|s| * ((d : ℝ) * Rstar))
  change Integrable f μ ∧ (∀ ω, 0 < f ω ∧ f ω ≤ B) ∧
    0 < ∫ ω, f ω ∂μ ∧ (∫ ω, f ω ∂μ) ≤ B
  have hcard : (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) = r ^ 2 := by
    simp [r, Fintype.card_prod, pow_two]
  have hpoint (ω : Ω) : 0 < f ω ∧ f ω ≤ B := by
    have hp :=
      AutoSamplingTheory.TechnicalLemmas.Analysis.MatrixTraceExponentialBounds.trace_exp_pos_and_le_card_mul_exp_abs_mul_norm
        (S useCos minus ω) (hhermS useCos minus ω) s
    refine ⟨hp.1, ?_⟩
    calc
      f ω ≤ (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) *
          Real.exp (|s| * ‖S useCos minus ω‖) := hp.2
      _ ≤ (Fintype.card (Fin (q + 1) × Fin (q + 1)) : ℝ) *
          Real.exp (|s| * ((d : ℝ) * Rstar)) :=
        mul_le_mul_of_nonneg_left
          (Real.exp_le_exp.mpr
            (mul_le_mul_of_nonneg_left (hnormS useCos minus ω) (abs_nonneg s)))
          (by positivity)
      _ = B := by rw [hcard]
  have hcontExp : Continuous (NormedSpace.exp : M → M) :=
    continuous_iff_continuousAt.mpr fun A =>
      (NormedSpace.exp_analytic (𝕂 := ℝ) A).continuousAt
  have hmeasf : Measurable f :=
    (Matrix.traceLinearMap _ ℝ ℝ).toContinuousLinearMap.continuous.measurable.comp
      (hcontExp.measurable.comp ((hmeasS useCos minus).const_smul s))
  have hint : Integrable f μ := by
    apply Integrable.of_bound hmeasf.aestronglyMeasurable B
    exact ae_of_all _ fun ω => by
      rw [Real.norm_eq_abs, abs_of_pos (hpoint ω).1]
      exact (hpoint ω).2
  have hsupport : Function.support f = Set.univ := by
    ext ω
    simp only [Function.mem_support, Set.mem_univ, iff_true]
    exact ne_of_gt (hpoint ω).1
  have hintpos : 0 < ∫ ω, f ω ∂μ := by
    apply (integral_pos_iff_support_of_nonneg (fun ω => (hpoint ω).1.le) hint).mpr
    rw [hsupport]
    simp
  have hintle : (∫ ω, f ω ∂μ) ≤ B := by
    simpa using integral_mono_ae hint (integrable_const B)
      (ae_of_all μ fun ω => (hpoint ω).2)
  exact ⟨hint, hpoint, hintpos, hintle⟩

end AutoSamplingTheory.Tests.GaussianComplexityTraceMgfDomain
'''
p=w/'TProof.attempt1.lean';assert not p.exists();p.write_text(header+statement+proof)
print({'file':str(p.relative_to(r)),'lines':len((header+statement+proof).splitlines()),'exact_admitted_statement_unchanged':statement in p.read_text()})
