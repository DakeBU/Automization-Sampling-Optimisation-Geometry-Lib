import GC31Mixture
import AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation

/-! # No zero-query algorithm uniformly attains accuracy 1/16

At budget zero the returned vector depends only on the algorithm's seed. The
identity precision and the admissible first-coordinate diagonal perturbation
have target probabilities differing by more than 1/8 on a closed event.
-/

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

private theorem admissible_diagonal_between {d : ℕ} {κ : ℝ} (a : Fin d → ℝ)
    (ha : ∀ i, 1 ≤ a i ∧ a i ≤ κ) : Admissible κ (Matrix.diagonal a) := by
  refine ⟨Matrix.isHermitian_diagonal a, fun x => ?_⟩
  simp only [dotProduct, Matrix.mulVec_diagonal, Finset.mul_sum]
  constructor <;> apply Finset.sum_le_sum <;> intro i _
  · nlinarith [mul_nonneg (sub_nonneg.mpr (ha i).1) (sq_nonneg (x i))]
  · nlinarith [mul_nonneg (sub_nonneg.mpr (ha i).2) (sq_nonneg (x i))]

/-- Section 3.3, zero-query case. Uniform TV accuracy at most 1/16 on the
centered Gaussian precision class forces every fixed query budget to be positive. -/
theorem positive_budget_of_accuracy {d T : ℕ} {κ ε : ℝ}
    {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]
    (hd : 1 ≤ d) (hκ : 4 ≤ κ) (hsmall : ε ≤ 1/16)
    (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State)
    (hacc : ∀ A, Admissible κ A → eventTV (alg.outputLaw ρ T A) (targetLaw A) ≤ ε) :
    1 ≤ T := by
  cases T with
  | succ T => omega
  | zero =>
    exfalso
    let A₀ : Precision d := 1
    let A₁ : Precision d := Matrix.diagonal (fun i => if i.val = 0 then κ else 1)
    have h₀ : Admissible κ A₀ := by
      change Admissible κ 1
      rw [← Matrix.diagonal_one]
      exact admissible_diagonal_between _ fun _ => ⟨le_rfl, by linarith⟩
    have h₁ : Admissible κ A₁ :=
      admissible_diagonal_between (fun i : Fin d => if i.val = 0 then κ else 1) fun i => by split_ifs <;> constructor <;> linarith
    let B : Set (E d) := {x | |WithLp.ofLp x (⟨0, hd⟩ : Fin d)| ≤ (1 : ℝ)/2}
    have hB : MeasurableSet B := by
      apply measurableSet_le _ measurable_const
      fun_prop
    let μ := ρ.map (fun s => alg.output (alg.start s))
    have hm (A : Precision d) : alg.outputLaw ρ 0 A = μ := by
      unfold Algorithm.outputLaw
      congr 1
      funext s
      dsimp only [Algorithm.sample]
      cases h : alg.next (alg.start s) <;> simp [run, h]
    let : IsProbabilityMeasure μ :=
      Measure.isProbabilityMeasure_map (alg.measurable_output.comp alg.measurable_start).aemeasurable
    have gap (A : Precision d) (hA : Admissible κ A) :
        |μ.real B - (targetLaw A).real B| ≤ ε := by
      exact (event_gap_le_tv μ (targetLaw A) hB).trans (hm A ▸ hacc A hA)
    have sep : (1 : ℝ)/8 < (targetLaw A₁).real B - (targetLaw A₀).real B :=
      actual_zero_query_gaussian_event_gap hd hκ
    have hg₀ := (abs_le.mp (gap A₀ h₀)).2
    have hg₁ := (abs_le.mp (gap A₁ h₁)).1
    linarith

#print axioms positive_budget_of_accuracy

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
