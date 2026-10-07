import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped RealInnerProductSpace BigOperators
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
namespace Tests.GaussianCompactHilbertLogSobolev

theorem zero_arbitrary_hilbert
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    Integrable (fun _ : E => (0 : ℝ)^2) (stdGaussian E) ∧
    (∫ _x : E, (0 : ℝ)^2 * Real.log ((0 : ℝ)^2) ∂stdGaussian E) -
      (∫ _x : E, (0 : ℝ)^2 ∂stdGaussian E) *
        Real.log (∫ _x : E, (0 : ℝ)^2 ∂stdGaussian E) ≤
      2 * ∫ x, ‖gradient (fun _ : E => (0 : ℝ)) x‖^2 ∂stdGaussian E := by
  have hs : HasCompactSupport (fun _ : E => (0 : ℝ)) :=
    HasCompactSupport.intro isCompact_empty (fun _ _ => rfl)
  have h := compact_stdGaussian_logSobolev (fun _ : E => (0 : ℝ)) contDiff_const hs
  exact ⟨h.1, h.2.2.2⟩

/-- Rank zero admits a nonzero signed observer with true mass four. -/
theorem negative_constant_rank_zero :
    let E := EuclideanSpace ℝ (Fin 0)
    Integrable (fun _ : E => (-2 : ℝ)^2) (stdGaussian E) ∧
    (∫ _x : E, (-2 : ℝ)^2 * Real.log ((-2 : ℝ)^2) ∂stdGaussian E) -
      (∫ _x : E, (-2 : ℝ)^2 ∂stdGaussian E) *
        Real.log (∫ _x : E, (-2 : ℝ)^2 ∂stdGaussian E) ≤
      2 * ∫ x, ‖gradient (fun _ : E => (-2 : ℝ)) x‖^2 ∂stdGaussian E := by
  dsimp only
  have hs : HasCompactSupport (fun _ : EuclideanSpace ℝ (Fin 0) => (-2 : ℝ)) :=
    HasCompactSupport.intro isCompact_univ (fun _ h => False.elim (h (Set.mem_univ _)))
  have h := compact_stdGaussian_logSobolev
    (fun _ : EuclideanSpace ℝ (Fin 0) => (-2 : ℝ)) contDiff_const hs
  exact ⟨h.1, h.2.2.2⟩

/-- The real standardized RGO square-root density is cut off, using its actual
canonical proximal witness. This tests a paper consumer, not a supplied C2
surrogate or an application to the still noncompact raw square-root density. -/
theorem actual_posterior_compact_lsi
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {κ η R : ℝ} (y : E)
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    (hη : 0 < η) (hR : 0 < R) :
    ∃ p : E, p + η • gradient V p = y ∧
      let ρ := fun u => V (p + Real.sqrt η • u) - V p -
        Real.sqrt η * inner ℝ (gradient V p) u
      let Z := ∫ u, Real.exp (-ρ u) ∂stdGaussian E
      let g := fun u => radialSmoothCutoff R u * Real.exp (-ρ u / 2) / Real.sqrt Z
      Integrable (fun u => (g u)^2) (stdGaussian E) ∧
      Integrable (fun u => (g u)^2 * Real.log ((g u)^2)) (stdGaussian E) ∧
      Integrable (fun u => ‖gradient g u‖^2) (stdGaussian E) ∧
      (∫ u, (g u)^2 * Real.log ((g u)^2) ∂stdGaussian E) -
        (∫ u, (g u)^2 ∂stdGaussian E) * Real.log (∫ u, (g u)^2 ∂stdGaussian E) ≤
        2 * ∫ u, ‖gradient g u‖^2 ∂stdGaussian E := by
  obtain ⟨p, _, hstat, hd⟩ :=
    AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity.standardized_rgo_sqrt_density_domain
      (S := Unit) hκ hV hH (eta := fun _ => η) (y := fun _ => y)
      measurable_const measurable_const (fun _ => hη)
  refine ⟨p (), hstat (), ?_⟩
  dsimp only
  let ρ := fun u => V (p () + Real.sqrt η • u) - V (p ()) -
    Real.sqrt η * inner ℝ (gradient V (p ())) u
  let Z := ∫ u, Real.exp (-ρ u) ∂stdGaussian E
  let f := fun u => Real.exp (-ρ u / 2) / Real.sqrt Z
  have hf : ContDiff ℝ 2 f := (hd ()).2.2.2.2.2.2.2.1
  have hc : ContDiff ℝ 2 (radialSmoothCutoff R : E → ℝ) :=
    (radialSmoothCutoff_contDiff hR).of_le
      (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))
  have hs : HasCompactSupport (fun u => radialSmoothCutoff R u * f u) :=
    (radialSmoothCutoff_hasCompactSupport hR).mul_right
  have h := compact_stdGaussian_logSobolev
    (fun u => radialSmoothCutoff R u * f u) (hc.mul hf) hs
  simpa only [f, div_eq_mul_inv, mul_assoc] using h

#print axioms compact_stdGaussian_logSobolev
#print axioms zero_arbitrary_hilbert
#print axioms negative_constant_rank_zero
#print axioms actual_posterior_compact_lsi

end Tests.GaussianCompactHilbertLogSobolev
