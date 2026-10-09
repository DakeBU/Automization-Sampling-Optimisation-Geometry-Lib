import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean

/-!
# Literal PBPS reflected Gibbs law and compact-observer mean

Authored analytic integration for Chen, Chewi, Lu and Zhang,
arXiv:2609.06905v1, Appendix C.1 reflected density and normalized mean.
The source-volume S_y is identified at EVERY y with the actual posterior
reflection, using genuine Gibbs integrability and exported affine normalization.
This whole function equality transports actual compact mean C1, never an AE
conditional version or an assumed regularity/law certificate.

Lower C2 curvature/allpositive eta, compact C1 observer and finite real Hilbert
including rank zero are explicit sufficient-background extensions. Actual paper
consumers retain two-sided Hessian/capped eta/smooth compact source hypotheses.
Tf closed-gradient membership, rough B.13, Gamma, invariance/nonexplosion,
implementation errors, main results and expected costs remain separate.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean
open MeasureTheory
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 800000

/-- Literal every-y source reflection law and C1 mean, with normalization internal. -/
theorem reflected_gibbs_mean_c1
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α η : ℝ} (hα : 0 < α) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, α*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v)
    (hη : 0 < η) {f : E → ℝ} (hf : ContDiff ℝ 1 f) (hc : HasCompactSupport f) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    let S := fun y : E => (volume : Measure E).tilted
      (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    (∀ y, S y = (R y).map (fun x : E => (2:ℝ) • x-y)) ∧
      ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂S y)
 := by
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
  let S := fun y : E => (volume : Measure E).tilted
    (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
  change (∀ y, S y = (R y).map (fun x : E => (2:ℝ) • x-y)) ∧
    ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂S y)
  have hG := GibbsAugmentation.normalized_augmentation_density hα hV hH hη
  have hI : Integrable (fun x => Real.exp (-V x)) (volume : Measure E) :=
    Integrable.of_integral_ne_zero hG.1.ne'
  have : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  have hR (y : E) : R y = (volume : Measure E).tilted
      (fun x => -(V x + ‖x-y‖^2/(2*η))) := by
    dsimp only [R, μ]
    rw [tilted_tilted hI]
    congr 1
    funext x
    simp only [Pi.add_apply]
    ring
  have hS (y : E) : S y = (R y).map (fun x : E => (2:ℝ) • x-y) := by
    have hW (u : E) :
        V ((2:ℝ)⁻¹ • (u- -y)) + ‖(2:ℝ)⁻¹ • (u- -y)-y‖^2/(2*η) =
          V ((1/2:ℝ) • (y+u)) + ‖y-u‖^2/(8*η) := by
      have ha : (2:ℝ)⁻¹ • (u- -y) = (1/2:ℝ) • (y+u) := by
        simp [div_eq_mul_inv, sub_neg_eq_add, add_comm]
      have hb : (2:ℝ)⁻¹ • (u- -y)-y = (1/2:ℝ) • (u-y) := by
        norm_num
        module
      have hq : ‖(2:ℝ)⁻¹ • (u- -y)-y‖^2/(2*η) = ‖y-u‖^2/(8*η) := by
        rw [hb, norm_smul, norm_sub_rev u y]
        norm_num [Real.norm_eq_abs]
        field_simp
        ring
      rw [hq, ha]
    have haf := AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs.map_affine_gibbs
      (fun x : E => V x + ‖x-y‖^2/(2*η)) (-y) (s := 2) (by norm_num)
    have hm : (fun x : E => -y+(2:ℝ) • x) = (fun x : E => (2:ℝ) • x-y) :=
      funext fun x => by abel
    rw [hm] at haf
    rw [hR]
    calc
      S y = (volume : Measure E).tilted (fun u =>
          -(V ((2:ℝ)⁻¹ • (u- -y)) + ‖(2:ℝ)⁻¹ • (u- -y)-y‖^2/(2*η))) := by
        dsimp only [S]
        congr 1
        funext u
        rw [hW]
        ring
      _ = _ := haf.symm
  refine ⟨hS, ?_⟩
  simp_rw [hS]
  exact AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean.gaussian_reflected_mean_c1
    μ hη hf hc

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean
