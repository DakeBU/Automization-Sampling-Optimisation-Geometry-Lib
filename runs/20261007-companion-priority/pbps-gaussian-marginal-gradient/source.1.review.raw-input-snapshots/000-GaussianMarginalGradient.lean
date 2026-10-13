import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient

/-!
# Genuine gradient domain of the actual Gaussian marginal

Authored full-space background for PBPS arXiv:2609.06905v1 Appendix C.1,
which reduces B.13 to smooth compact tests using density and closedness.
The actual outer law is the second marginal of the independent Gaussian
augmentation. Its positive C2 density, L1 property and normalization are
derived inside the proof, before invoking the existing weighted gradient.

Any probability input and finite real Hilbert/rank-zero extensions are
explicit. This constructs the genuine smooth-compact graph, a dense domain,
closability and closed closure on the outer law. It does not assert literal
Tf membership, the full rough-input estimate, Gamma, mixing or query costs.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology

noncomputable section
set_option autoImplicit false

theorem gaussian_marginal_gradient_closable
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) :
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
    let ν := J.snd
    ∃ D : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
      Dense (D.domain : Set (Lp ℝ 2 ν)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
      ∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ D.graph ↔
        ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
          u =ᵐ[ν] f ∧ v =ᵐ[ν] gradient f := by
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
  let ν := J.snd
  change ∃ D : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
    Dense (D.domain : Set (Lp ℝ 2 ν)) ∧ D.IsClosable ∧ D.closure.IsClosed ∧
      ∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ D.graph ↔
        ∃ f : E → ℝ, ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
          u =ᵐ[ν] f ∧ v =ᵐ[ν] gradient f
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  let Z := fun y : E => ∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ
  let ρ := fun y : E => C*Z y
  let W := fun y : E => -Real.log (ρ y)
  have hpair : Measurable (fun p : E × E =>
      (p.1, p.1 + Real.sqrt η • p.2)) := by fun_prop
  let : IsProbabilityMeasure J := Measure.isProbabilityMeasure_map hpair.aemeasurable
  let : IsProbabilityMeasure ν := Measure.isProbabilityMeasure_map measurable_snd.aemeasurable
  have hmap : ν = (μ.prod (stdGaussian E)).map
      (fun p : E × E => p.1 + Real.sqrt η • p.2) :=
    Measure.map_map measurable_snd hpair
  obtain ⟨hdensity,hpos,hZ,hW⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_potential_c2 μ hη
  have hνdensity : ν = (volume : Measure E).withDensity
      (fun y => ENNReal.ofReal (ρ y)) := hmap.trans hdensity
  have hρ : Continuous ρ := continuous_const.mul hZ.continuous
  have hnn : 0 ≤ᵐ[(volume : Measure E)] ρ :=
    Filter.Eventually.of_forall fun y => (hpos y).le
  have hmass : (∫⁻ y, ENNReal.ofReal (ρ y) ∂(volume : Measure E)) = 1 := by
    have hm := congrArg (fun m : Measure E => m Set.univ) hνdensity
    rw [withDensity_apply _ MeasurableSet.univ] at hm
    simpa only [measure_univ,Measure.restrict_univ] using hm.symm
  have hI : Integrable ρ (volume : Measure E) :=
    (lintegral_ofReal_ne_top_iff_integrable hρ.aestronglyMeasurable hnn).mp
      (by rw [hmass]; exact ENNReal.one_ne_top)
  have hnorm : (∫ y, ρ y ∂(volume : Measure E)) = 1 :=
    ENNReal.ofReal_eq_one.mp ((ofReal_integral_eq_lintegral_ofReal hI hnn).trans hmass)
  have hexp (y : E) : Real.exp (-W y) = ρ y := by
    dsimp only [W]
    rw [neg_neg,Real.exp_log (hpos y)]
  have hWI : Integrable (fun y => Real.exp (-W y)) (volume : Measure E) := by
    simpa only [hexp] using hI
  have htilt : (volume : Measure E).tilted (fun y => -W y) = ν := by
    rw [Measure.tilted]
    simp_rw [hexp]
    rw [hnorm]
    simpa only [div_one] using hνdensity.symm
  rw [← htilt]
  exact WeightedGradient.compact_gradient_closable W
    (hW.of_le (by norm_num)) hWI

end
end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
