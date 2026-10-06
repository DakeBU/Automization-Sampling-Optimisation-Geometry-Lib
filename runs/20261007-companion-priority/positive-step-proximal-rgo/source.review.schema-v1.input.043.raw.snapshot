import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
import Mathlib.MeasureTheory.Group.Integral
import Mathlib.Tactic

/-! A literal affine change of variables for normalized Lebesgue tilts.
The true Jacobian cancels between the partition and set numerator. This is
an identity of Mathlib tilted measures, not a probability assertion: applications
must produce actual finite positive partitions separately. Dimension zero is
allowed. The scaling-only private route in NormalizedReferenceCall was searched;
this canonical leaf adds arbitrary translations and nonzero real scales. -/

namespace AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs
open MeasureTheory Set
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Actual affine pushforward, with its inverse potential and Jacobian canceled.
No regularity, integrability, probability or moment certificate is assumed. -/
theorem map_affine_gibbs (F : E → ℝ) (p : E) {s : ℝ} (hs : s ≠ 0) :
    Measure.map (fun x : E => p+s • x)
      ((volume : Measure E).tilted (fun x => -F x)) =
      volume.tilted (fun x => -F (s⁻¹ • (x-p))) := by
  let T := fun x : E => p+s • x
  let H := fun x : E => s⁻¹ • (x-p)
  let J : ℝ := |(s^Module.finrank ℝ E)⁻¹|
  have hJ : J ≠ 0 := abs_ne_zero.mpr (inv_ne_zero (pow_ne_zero _ hs))
  have hm : Measurable T := by dsimp [T]; fun_prop
  have hHT (x : E) : H (T x) = x := by simp [H,T,smul_smul,hs]
  have change_variables (f : E → ℝ) : (∫ x, f (T x)) = J*(∫ x, f x) := by
    have h := Measure.integral_comp_smul (volume : Measure E) (fun x => f (p+x)) s
    simpa only [integral_add_left_eq_self,smul_eq_mul,T,J] using h
  have hZ : (∫ x, Real.exp (-F x)) = J*(∫ x, Real.exp (-F (H x))) := by
    simpa only [hHT] using change_variables (fun x => Real.exp (-F (H x)))
  ext B hB
  rw [Measure.map_apply hm hB,tilted_apply_eq_ofReal_integral' _ (hB.preimage hm),
    tilted_apply_eq_ofReal_integral' _ hB]
  congr 1
  rw [integral_div,integral_div]
  have hI : (∫ x in T ⁻¹' B, Real.exp (-F x)) =
      J*(∫ x in B, Real.exp (-F (H x))) := by
    have h := change_variables (B.indicator (fun x => Real.exp (-F (H x))))
    have he : (fun x => B.indicator (fun y => Real.exp (-F (H y))) (T x)) =
        (T ⁻¹' B).indicator (fun x => Real.exp (-F x)) := by
      funext x
      by_cases hx : T x ∈ B <;> simp [Set.indicator,hx,hHT]
    rw [he,integral_indicator (hB.preimage hm),integral_indicator hB] at h
    exact h
  rw [hI,hZ]
  exact mul_div_mul_left _ _ hJ

end
end AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs
