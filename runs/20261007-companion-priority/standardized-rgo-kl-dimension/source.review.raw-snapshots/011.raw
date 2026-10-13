import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLFisher
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher

/-!
Actual numerical canonical KL bound for the unique-prox standardized RGO.
The source Gaussian-LSI/Fisher ingredient is composed at the same actual law;
no coherence, domain or desired-bound certificate is supplied by the caller.
Measurable families and rank zero are explicit authored extensions.
Gaussian T2, W2/FIRST4.6, main samplers and expected-cost composition remain separate.
-/
namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLDimension
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false

theorem standardized_rgo_unique_prox_and_kl_le_dimension
    {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [MeasurableSpace S] {V : E → ℝ} {κ : ℝ}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    {eta : S → ℝ} {y : S → E} (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s) :
    ∃ p : S → E, Measurable p ∧
      (∀ s, p s+eta s • gradient V (p s)=y s) ∧
      (∀ s z, z+eta s • gradient V z=y s → z=p s) ∧
      let rho := fun s u => V (p s+Real.sqrt (eta s) • u)-V (p s)-
        Real.sqrt (eta s)*inner ℝ (gradient V (p s)) u
      let mu := (volume : Measure E).tilted (fun x => -V x)
      let R := fun s => mu.tilted (fun x => -‖x-y s‖^2/(2*eta s))
      let r := fun s => (R s).map (fun x => (Real.sqrt (eta s))⁻¹ • (x-p s))
      let gamma := stdGaussian E
      ∀ s, IsProbabilityMeasure (r s) ∧ r s ≪ gamma ∧
        _root_.InformationTheory.klDiv (r s) gamma ≠ ⊤ ∧
        MemLp (gradient (rho s)) 2 (r s) ∧
        (_root_.InformationTheory.klDiv (r s) gamma).toReal ≤
          (eta s)^2*(Module.finrank ℝ E : ℝ)/2 := by
  obtain ⟨p, hpm, hstat, huniq, hk⟩ :=
    StandardizedRGOKLFisher.standardized_rgo_unique_prox_and_kl_le_fisher
      hκ hV hH heta hy hpos
  obtain ⟨p', hpm', hstat', hd⟩ :=
    StandardizedRGOPositionFisher.standardized_rgo_position_and_fisher
      hκ hV hH heta hy hpos
  have hp : p'=p := funext (fun s => huniq s (p' s) (hstat' s))
  rw [hp] at hd
  let rho := fun s u => V (p s+Real.sqrt (eta s) • u)-V (p s)-
    Real.sqrt (eta s)*inner ℝ (gradient V (p s)) u
  let mu := (volume : Measure E).tilted (fun x => -V x)
  let R := fun s => mu.tilted (fun x => -‖x-y s‖^2/(2*eta s))
  let r := fun s => (R s).map (fun x => (Real.sqrt (eta s))⁻¹ • (x-p s))
  let gamma := stdGaussian E
  refine ⟨p, hpm, hstat, huniq, ?_⟩
  change ∀ s, IsProbabilityMeasure (r s) ∧ r s ≪ gamma ∧
    _root_.InformationTheory.klDiv (r s) gamma ≠ ⊤ ∧
    MemLp (gradient (rho s)) 2 (r s) ∧
    (_root_.InformationTheory.klDiv (r s) gamma).toReal ≤
      (eta s)^2*(Module.finrank ℝ E : ℝ)/2
  intro s
  obtain ⟨hprob, hac, hfin, hrho2, hkl⟩ := hk s
  obtain ⟨hprobR, hCrho, hCQ, hgrho0, hgQ0, hHrho, hHQ, hrtilt,
    hprobr, hposition2, hpositionint, hpositionbound, hscore2,
    hscoreposition, hscorebound⟩ := hd.2 s
  change (∫ u, ‖gradient (rho s) u‖^2 ∂r s) ≤
    (eta s)^2*(Module.finrank ℝ E : ℝ) at hscorebound
  refine ⟨hprob, hac, hfin, hrho2, ?_⟩
  calc
    _ ≤ (1/2 : ℝ)*(∫ u, ‖gradient (rho s) u‖^2 ∂r s) := hkl
    _ ≤ (1/2 : ℝ)*((eta s)^2*(Module.finrank ℝ E : ℝ)) :=
      mul_le_mul_of_nonneg_left hscorebound (by norm_num)
    _ = (eta s)^2*(Module.finrank ℝ E : ℝ)/2 := by ring

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLDimension
