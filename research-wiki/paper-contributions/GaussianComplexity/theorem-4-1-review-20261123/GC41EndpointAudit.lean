import GC41LowerBound

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior (precisionReply)
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.EndpointAudit

/-- A sampler that either stops at the seed point immediately or queries there,
stores the returned gradient, and stops. Both the query and the output depend on the seed. -/
def gradientOrStop (d : ℕ) : Algorithm d (Bool × Space d) (Bool × Space d) where
  start := id
  next := fun s => if s.1 then Sum.inl () else Sum.inr s.2
  update := fun _ _ r => (true,r.2)
  output := Prod.snd
  measurable_start := measurable_id
  measurable_next := Measurable.ite (measurable_fst (measurableSet_singleton true))
    measurable_const (measurable_inr.comp measurable_snd)
  measurable_update := measurable_const.prodMk (measurable_snd.comp (measurable_snd.comp measurable_snd))
  measurable_output := measurable_snd

/-- At positive budgets stopping is exact and the query branch returns the matrix-vector product. -/
theorem sample_gradientOrStop {d : ℕ} (A : Precision d) (q : ℕ) (s : Bool × Space d) :
    (gradientOrStop d).sample (q+1) A s =
      if s.1 then s.2 else WithLp.toLp 2 (A *ᵥ WithLp.ofLp s.2) := by
  rcases s with ⟨b,x⟩
  cases b <;> simp [Algorithm.sample,gradientOrStop,run,precisionReply]

/-- Boundary 2q+1=d and q=1. The extension has two iid Gaussian starts and preserves the
actual orientation jointly with either the seed point or its observed gradient. -/
theorem three_dimensional_representation (κ : ℝ) (ρ : Measure (Bool × Space 3))
    [IsProbabilityMeasure ρ] :
    HasKrylovRepresentation (q := 1) κ ((ρ.prod (orthogonalHaar 3)).map
      (fun p : (Bool × Space 3) × Orientation 3 =>
        (p.2, if p.1.1 then p.1.2 else
          WithLp.toLp 2 ((hiddenPrecision κ p.2) *ᵥ WithLp.ofLp p.1.2)))) := by
  have h := actual_output_representation (q := 1) κ (by decide : 2*1+1 ≤ 3) ρ (gradientOrStop 3)
  have he : experimentPair κ 1 (gradientOrStop 3) = fun p : (Bool × Space 3) × Orientation 3 =>
      (p.2, if p.1.1 then p.1.2 else WithLp.toLp 2 ((hiddenPrecision κ p.2) *ᵥ WithLp.ofLp p.1.2)) := by
    funext p
    exact congrArg (Prod.mk p.2) (sample_gradientOrStop _ 0 p.1)
  simpa only [experimentLaw,he] using h

/-- At the moving upper endpoint, the finite real minimax bound applies both to samplers chosen
after learning the spectrum and to samplers given only the condition-number cap. -/
theorem upper_endpoint_finite_real :
    ∃ D : ℕ, ∀ d ≥ D,
      Real.sqrt (Real.sqrt (d : ℝ)) * Real.log (d : ℝ) / 512 ≤
        (disclosedQueryComplexity.{0,0} d (Real.sqrt (d : ℝ)) (1/10)).toReal ∧
      Real.sqrt (Real.sqrt (d : ℝ)) * Real.log (d : ℝ) / 512 ≤
        (gaussianQueryComplexity.{0,0} d (Real.sqrt (d : ℝ)) (1/10)).toReal := by
  obtain ⟨K,hK⟩ := gaussian_query_lower_bound_real (δ := 1/2) (by norm_num) (by norm_num)
  refine ⟨max 4 K, ?_⟩
  intro d hd
  have hd4 : (4 : ℝ) ≤ d := by exact_mod_cast (le_max_left 4 K).trans hd
  have hk : 2 ≤ Real.sqrt (d : ℝ) := Real.le_sqrt_of_sq_le (by linarith)
  have hc : Real.sqrt (d : ℝ) ≤ (d : ℝ)^(1-(1/2:ℝ)) := by
    rw [show 1-(1/2:ℝ) = 1/2 by norm_num, Real.sqrt_eq_rpow]
  have h := hK d ((le_max_right 4 K).trans hd) _ hk hc (1/10) (by norm_num) le_rfl
  constructor <;> linarith [h.1,h.2]

#print axioms three_dimensional_representation
#print axioms upper_endpoint_finite_real
end AutoSamplingTheory.ExampleCases.GaussianComplexity.EndpointAudit
