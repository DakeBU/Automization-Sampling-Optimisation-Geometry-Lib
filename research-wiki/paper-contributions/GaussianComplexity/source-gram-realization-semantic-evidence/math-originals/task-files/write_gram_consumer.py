from pathlib import Path
import json
W=Path(__file__).resolve().parent
s=json.loads((W/'statement-seal-v1.unclaimed.json').read_bytes())['actual_private_consumer']['signature']
aliases=s[s.index('  let D :='):s.index('  ∀ Δ : ℝ,')]
header='''import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceGramRealization
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment

/-! Private real Ex126 consumer. On the literal original good event and actual
centered-sum deviation event, derive actual Gram norm bounds. The real threshold
is an explicit deterministic generalization; no event probability is claimed. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator
set_option autoImplicit false
namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceGramRealization

private theorem actual_source_gram_deviation_bounds
'''
proof=r'''  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  have hp := FixedSpectrumSourceGramRealization.actual_source_centered_gram_realizations
    (d := d) (q := q) hq
  change (∀ ω : Ω, G ω →
    ((∑ i : Fin d, Z i ω) = (B ω).transpose * B ω - a • (1 : N)) ∧
    ((∑ i : Fin d, w i • Z i ω) =
      (B ω).transpose * Matrix.diagonal w * B ω)) at hp
  have hr : 0 < r := by dsimp [r]; positivity
  have moment := AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian
    (E := E)
  have hgood : MeasurableSet {y : E | ‖y‖ ^ 2 ≤ L} :=
    measurableSet_le (by fun_prop) measurable_const
  have hret := moment.1.indicator hgood
  have hretle : (∫ x : E, {y : E | ‖y‖ ^ 2 ≤ L}.indicator
      (fun y => ‖y‖ ^ 2) x ∂stdGaussian E) ≤ r := by
    calc
      _ ≤ ∫ x : E, ‖x‖ ^ 2 ∂stdGaussian E := by
        apply integral_mono hret moment.1
        intro x
        by_cases hx : ‖x‖ ^ 2 ≤ L
        · simp [Set.indicator, hx]
        · simpa [Set.indicator, hx] using sq_nonneg ‖x‖
      _ = r := by simpa [E, r] using moment.2
  have ha1 : a ≤ 1 := (div_le_one hr).2 hretle
  have identity_norm : ‖(1 : N)‖ = 1 := norm_one
  have bias_norm : ‖(1 - a) • (1 : N)‖ = 1 - a := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (sub_nonneg.mpr ha1),
      identity_norm, mul_one]
  have actual_bias_identity (ω : Ω) (hG : G ω) :
      (B ω).transpose * B ω - (1 : N) =
        (∑ i : Fin d, Z i ω) - (1 - a) • (1 : N) := by
    rw [(hp ω hG).1]
    ext u v
    simp only [Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul]
    ring
  change ∀ Δ : ℝ, ∀ ω : Ω, G ω →
    ((‖∑ i : Fin d, Z i ω‖ ≤ Δ) ∧ (‖∑ i : Fin d, w i • Z i ω‖ ≤ Δ)) →
    ((‖(B ω).transpose * B ω - (1 : N)‖ ≤ Δ + (1 - a)) ∧
      (‖(B ω).transpose * Matrix.diagonal w * B ω‖ ≤ Δ))
  intro Δ ω hG hΔ
  constructor
  · calc
      ‖(B ω).transpose * B ω - (1 : N)‖ =
          ‖(∑ i : Fin d, Z i ω) - (1 - a) • (1 : N)‖ := by
        rw [actual_bias_identity ω hG]
      _ ≤ ‖∑ i : Fin d, Z i ω‖ + ‖(1 - a) • (1 : N)‖ := norm_sub_le _ _
      _ = ‖∑ i : Fin d, Z i ω‖ + (1 - a) := by rw [bias_norm]
      _ ≤ Δ + (1 - a) := add_le_add_right hΔ.1 _
  · rw [← (hp ω hG).2]
    exact hΔ.2
'''
out=header+s+' := by\n  classical\n  dsimp only\n'+aliases+proof+'\nend AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceGramRealization\n'
p=Path('Tests/GaussianComplexityFixedSpectrumSourceGramRealization.lean')
with p.open('x') as f:f.write(out)
print(json.dumps({'private_T_file':str(p),'lines':len(out.splitlines()),'exact_sealed_signature_retained':s in out,'probability_claim':False}))
