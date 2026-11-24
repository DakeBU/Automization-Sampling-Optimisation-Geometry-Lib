import GC13KnownMinimum

/-! Probability of the returned sample for a smooth potential and the one-dimensional
endpoint when a minimizer is supplied. -/
noncomputable section
open MeasureTheory InnerProductSpace
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional (E)
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass

universe u v
variable {d : ℕ} {Seed : Type u} {State : Type v} [MeasurableSpace Seed] [MeasurableSpace State]

theorem measurable_potential_sample (alg : Algorithm d Seed State) (q : ℕ)
    {V : E d → ℝ} (hV : ContDiff ℝ 2 V) :
    Measurable (fun s => alg.output (run alg.next alg.update (fun x => (V x,gradient V x))
      q (alg.start s)).1.1) := by
  have hg : Continuous (gradient V) :=
    (toDual ℝ (E d)).symm.continuous.comp (hV.continuous_fderiv (by norm_num))
  let oracle (_ : Unit) (x : E d) := (V x, gradient V x)
  have hm : Measurable (Function.uncurry oracle) :=
    (hV.continuous.measurable.prodMk hg.measurable).comp measurable_snd
  exact alg.measurable_output.comp
    ((alg.measurable_run_state oracle hm q).comp
      ((measurable_const : Measurable (fun _ : Seed => ())).prodMk alg.measurable_start))

theorem potentialOutputLaw_isProbability (ρ : Measure Seed) [IsProbabilityMeasure ρ]
    (alg : Algorithm d Seed State) (q : ℕ) {V : E d → ℝ} (hV : ContDiff ℝ 2 V) :
    IsProbabilityMeasure (potentialOutputLaw ρ alg q V) :=
  Measure.isProbabilityMeasure_map (measurable_potential_sample alg q hV).aemeasurable

/-- Even with the minimizer, zero queries cannot attain the endpoint accuracy in dimension one. -/
theorem known_min_dimension_one_positive :
    (1 : ℝ≥0∞) ≤ knownMinQueryComplexity.{u,v} 1 4 (1/16) := by
  apply le_iInf
  intro t
  obtain ⟨S,T,mS,mT,ρ,hρ,alg,hacc⟩ := gaussian_budget_of_known_min t.property
  have hb := positive_budget_of_accuracy (by decide : 1 ≤ 1) (by norm_num : (4 : ℝ) ≤ 4)
    (le_refl (1/16 : ℝ)) ρ alg hacc
  exact_mod_cast hb

#print axioms measurable_potential_sample
#print axioms potentialOutputLaw_isProbability
#print axioms known_min_dimension_one_positive
end AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass
