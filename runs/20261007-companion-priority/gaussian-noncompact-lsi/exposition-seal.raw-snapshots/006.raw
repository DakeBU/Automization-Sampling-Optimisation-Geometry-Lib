import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianLogSobolev
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped RealInnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianLogSobolev
namespace Tests.GaussianLogSobolev

theorem zero_arbitrary_hilbert
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    (∫ _x : E, (0:ℝ)^2 * Real.log ((0:ℝ)^2) ∂stdGaussian E) -
      (∫ _x : E, (0:ℝ)^2 ∂stdGaussian E) *
        Real.log (∫ _x : E, (0:ℝ)^2 ∂stdGaussian E) ≤
      2 * ∫ x, ‖gradient (fun _ : E => (0:ℝ)) x‖^2 ∂stdGaussian E := by
  apply gaussian_logSobolev_of_contDiff (fun _ : E => (0:ℝ)) contDiff_const
  · exact memLp_const 0
  · rw [gradient_fun_const']
    exact MemLp.zero
  · simp

/-- A noncompact signed constant has true mass four, in every dimension including zero. -/
theorem negative_constant_arbitrary_hilbert
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    (∫ _x : E, (-2:ℝ)^2 ∂stdGaussian E) = 4 ∧
    (∫ _x : E, (-2:ℝ)^2 * Real.log ((-2:ℝ)^2) ∂stdGaussian E) -
      (∫ _x : E, (-2:ℝ)^2 ∂stdGaussian E) *
        Real.log (∫ _x : E, (-2:ℝ)^2 ∂stdGaussian E) ≤
      2 * ∫ x, ‖gradient (fun _ : E => (-2:ℝ)) x‖^2 ∂stdGaussian E := by
  refine ⟨by norm_num, ?_⟩
  apply gaussian_logSobolev_of_contDiff (fun _ : E => (-2:ℝ)) contDiff_const
  · exact memLp_const _
  · rw [gradient_fun_const']
    exact MemLp.zero
  · exact integrable_const _

/-- The actual uncut standardized RGO sqrt-density supplies every analytic input.
Its proximal witness is the one produced by the real posterior-domain theorem;
identification with the distinct canonical KL consumer remains a later edge. -/
theorem actual_posterior_noncompact_lsi
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {κ η : ℝ} (y : E)
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    (hη : 0 < η) :
    ∃ p : E, p + η • gradient V p = y ∧
      let ρ := fun u => V (p + Real.sqrt η • u) - V p -
        Real.sqrt η * inner ℝ (gradient V p) u
      let Z := ∫ u, Real.exp (-ρ u) ∂stdGaussian E
      let f := fun u => Real.exp (-ρ u / 2) / Real.sqrt Z
      (∫ u, (f u)^2 * Real.log ((f u)^2) ∂stdGaussian E) -
        (∫ u, (f u)^2 ∂stdGaussian E) * Real.log (∫ u, (f u)^2 ∂stdGaussian E) ≤
        2 * ∫ u, ‖gradient f u‖^2 ∂stdGaussian E := by
  obtain ⟨p, _, hstat, hd⟩ :=
    AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity.standardized_rgo_sqrt_density_domain
      (S := Unit) hκ hV hH (eta := fun _ => η) (y := fun _ => y)
      measurable_const measurable_const (fun _ => hη)
  refine ⟨p (), hstat (), ?_⟩
  dsimp only
  let ρ := fun u => V (p () + Real.sqrt η • u) - V (p ()) -
    Real.sqrt η * inner ℝ (gradient V (p ())) u
  let Z := ∫ u, Real.exp (-ρ u) ∂stdGaussian E
  let q := fun u => Real.exp (-ρ u) / Z
  let f := fun u => Real.exp (-ρ u / 2) / Real.sqrt Z
  obtain ⟨_, _, _, _, _, hq, _, hf, hf2, hgrad2, _, hent, _, _, _⟩ := hd ()
  have hsq (u : E) : (f u)^2 = q u := (hq u).2
  have hentf : Integrable (fun u => (f u)^2 * Real.log ((f u)^2)) (stdGaussian E) := by
    simpa only [hsq] using hent
  exact gaussian_logSobolev_of_contDiff f hf hf2 hgrad2 hentf

#print axioms gaussian_logSobolev_of_contDiff
#print axioms zero_arbitrary_hilbert
#print axioms negative_constant_arbitrary_hilbert
#print axioms actual_posterior_noncompact_lsi

end Tests.GaussianLogSobolev
