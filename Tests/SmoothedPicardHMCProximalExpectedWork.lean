import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalExpectedWork

open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC
open ProximalExpectedWork InnerProductSpace MeasureTheory
open scoped NNReal

#check approximate_proximal_expected_work
#print axioms approximate_proximal_expected_work

-- A deterministic input is a genuine probability law; no assumed cost bound.
-- The test exercises eta>1/2 and retains actual interpreter execution.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {κ : ℝ≥0} (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2) (y : E) :
    ∃ N : E → ℕ, Integrable (fun z => (N z : ℝ)+1) (Measure.dirac y) ∧
      (∃ out, ApproximateProximalExecution.proximalQuery (gradient V) (3/4) (1/10)
        y (N y+1) y = some (out, N y+1)) ∧
      (N y : ℝ)+1 ≤ (2+(1+Real.log ((1-(7/8 : ℝ))⁻¹))/(-Real.log (7/8))) *
        (1+Real.log (1+‖gradient V y‖/(1/10))) := by
  obtain ⟨p,N,_,_,_,hall,hi,hb⟩ := approximate_proximal_expected_work hκ hV hH
    (eta := 3/4) (c := 7/8) (eps := 1/10) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (Measure.dirac y) (integrable_dirac (by simp))
  refine ⟨N, hi, ⟨_, (hall y).2.2⟩, ?_⟩
  simpa only [integral_dirac, Real.sqrt_sq (norm_nonneg _)] using hb
