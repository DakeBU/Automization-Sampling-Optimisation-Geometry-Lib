import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Set MeasureTheory ProbabilityTheory InnerProductSpace
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential

namespace Tests.SmoothedPicardHMCSmoothedGibbsPotential

-- Derived nonconstant Hessian, not a supplied smoothed-potential certificate.
private def potential (x : ℝ) : ℝ := (3/8)*x^2 + (1/8)*Real.sin x
private theorem potential_curvature :
    ∀ z v : ℝ, (1/(2*(1:ℝ)))*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ potential) z v) v ∧
      (fderiv ℝ (fderiv ℝ potential) z v) v ≤ ‖v‖^2 := by
  have hder (z : ℝ) : HasDerivAt potential ((3/4)*z+(1/8)*Real.cos z) z := by
    convert (((hasDerivAt_id z).pow 2).const_mul (3/8)).add
      ((Real.hasDerivAt_sin z).const_mul (1/8)) using 1 <;> first | rfl | (simp [potential, Pi.add_apply, mul_comm]; ring)
  have hD : fderiv ℝ potential = fun z =>
      ((3/4)*z+(1/8)*Real.cos z) • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    rw [fderiv_eq_smul_deriv, (hder z).deriv]
    simp
  have hDD (z v : ℝ) : (fderiv ℝ (fderiv ℝ potential) z v) v =
      ((3/4)-(1/8)*Real.sin z)*v^2 := by
    have hd : HasDerivAt (fun w : ℝ => (3/4)*w+(1/8)*Real.cos w)
        ((3/4)-(1/8)*Real.sin z) z := by
      convert ((hasDerivAt_id z).const_mul (3/4)).add
        ((Real.hasDerivAt_cos z).const_mul (1/8)) using 1 <;> (try dsimp only [id]) <;> first | rfl | ring
    rw [hD, fderiv_eq_smul_deriv,
      (hd.smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv]
    simp
    ring
  intro z v
  rw [hDD]
  simp only [Real.norm_eq_abs, sq_abs]
  constructor <;> nlinarith [Real.sin_le_one z, Real.neg_one_le_sin z, sq_nonneg v]


-- Actual source Gibbs normalization and smooth potential join the genuine
-- everywhere-defined backward conditional law of the same augmentation.
theorem actual_source_target_and_backward {η : ℝ} (hη : 0 < η) :
    let ZV := ∫ x, Real.exp (-potential x) ∂(volume : Measure ℝ)
    let μ := (volume : Measure ℝ).tilted (fun x => -potential x)
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ ℝ
    let A := fun y : ℝ => C*∫ x, Real.exp (-potential x-‖y-x‖^2/(2*η)) ∂(volume : Measure ℝ)
    let J := (μ.prod (stdGaussian ℝ)).map (fun p => (p.1,p.1+Real.sqrt η • p.2))
    0 < ZV ∧ (∫ y, A y ∂(volume : Measure ℝ)) = ZV ∧
      (μ.prod (stdGaussian ℝ)).map (fun p => p.1+Real.sqrt η • p.2) =
        (volume : Measure ℝ).tilted (fun y => -(-Real.log (A y))) ∧
      ContDiff ℝ 2 (fun y => -Real.log (A y)) ∧
      ∃ R : Kernel ℝ ℝ, IsMarkovKernel R ∧
        (∀ y, R y = μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
        (J.map Prod.swap).IsCondKernel R := by
  have hf : ContDiff ℝ 2 potential := by unfold potential; fun_prop
  obtain ⟨hZ,hμ,_hlaw,_hiA,hInt,hTilt,_hA,hC2,_hshift⟩ :=
    smoothed_gibbs_potential (by norm_num : (0:ℝ) < 1/2) hf
      (fun x v => by simpa only [mul_one] using (potential_curvature x v).1) hη
  let μ := (volume : Measure ℝ).tilted (fun x => -potential x)
  have : IsProbabilityMeasure μ := hμ
  obtain ⟨R,hR,hfiber,hcond⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  exact ⟨hZ,hInt,hTilt,hC2,R,hR,hfiber,hcond⟩

#print axioms smoothed_gibbs_potential
#print axioms actual_source_target_and_backward

end Tests.SmoothedPicardHMCSmoothedGibbsPotential
