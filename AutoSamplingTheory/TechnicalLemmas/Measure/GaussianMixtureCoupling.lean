import AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# A concrete coupling for reweighted Gaussian mixtures

The upper hint of Statistical Optimal Transport, Chapter 1 §1.8 Exercise 6
(printed p.44, PDF p.50), asks for a feasible plan. We match the shared mass
at each center using a common normal draw, and translate the remaining left
quarter to the right center using the same draw. This is the explicit
Samplinglib construction, not an optimal-plan claim.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureCoupling

open MeasureTheory ProbabilityTheory
open scoped ENNReal

/-- The prescribed real Gaussian mixtures have a feasible plan of exact
quadratic cost `m ^ 2`. The witness also works at zero and for negative `m`. -/
theorem exists_gaussian_mixture_coupling_cost (m : ℝ) :
    ∃ γ : Measure (ℝ × ℝ),
      Transport.IsCoupling γ
        ((1 / 2 : ℝ≥0∞) • gaussianReal (-m) 1 + (1 / 2 : ℝ≥0∞) • gaussianReal m 1)
        ((1 / 4 : ℝ≥0∞) • gaussianReal (-m) 1 + (3 / 4 : ℝ≥0∞) • gaussianReal m 1) ∧
      (∫⁻ z, WassersteinSpace.quadraticCost z ∂γ) = ENNReal.ofReal (m ^ 2) := by
  let Q (a b : ℝ) : Measure (ℝ × ℝ) :=
    (gaussianReal 0 1).map (fun z : ℝ => (z + a, z + b))
  have hfst (a b : ℝ) : (Q a b).fst = gaussianReal a 1 := by
    change ((gaussianReal 0 1).map (fun z : ℝ => (z + a, z + b))).fst = _
    have hb : Measurable (fun z : ℝ => z + b) := by fun_prop
    rw [Measure.fst_map_prodMk (X := fun z : ℝ => z + a) hb, gaussianReal_map_add_const, zero_add]
  have hsnd (a b : ℝ) : (Q a b).snd = gaussianReal b 1 := by
    change ((gaussianReal 0 1).map (fun z : ℝ => (z + a, z + b))).snd = _
    have ha : Measurable (fun z : ℝ => z + a) := by fun_prop
    rw [Measure.snd_map_prodMk (Y := fun z : ℝ => z + b) ha, gaussianReal_map_add_const, zero_add]
  have fst_smul (w : ℝ≥0∞) (ρ : Measure (ℝ × ℝ)) : (w • ρ).fst = w • ρ.fst :=
    Measure.map_smul w ρ Prod.fst
  have snd_smul (w : ℝ≥0∞) (ρ : Measure (ℝ × ℝ)) : (w • ρ).snd = w • ρ.snd :=
    Measure.map_smul w ρ Prod.snd
  have hmeas : Measurable (WassersteinSpace.quadraticCost (E := ℝ)) := by
    unfold WassersteinSpace.quadraticCost
    fun_prop
  have hcost (a b : ℝ) : (∫⁻ z, WassersteinSpace.quadraticCost z ∂Q a b) =
      ENNReal.ofReal ((a - b) ^ 2) := by
    change (∫⁻ z, WassersteinSpace.quadraticCost z ∂
      (gaussianReal 0 1).map (fun x : ℝ => (x + a, x + b))) = _
    rw [lintegral_map hmeas (by fun_prop)]
    have heq (z : ℝ) : z + a - (z + b) = a - b := by ring
    simp [WassersteinSpace.quadraticCost, heq, Real.norm_eq_abs, sq_abs]
  have h2 : (2 : NNReal) ≠ 0 := by norm_num
  have h4 : (4 : NNReal) ≠ 0 := by norm_num
  have hleft : (1 / 4 : ℝ≥0∞) + 1 / 4 = 1 / 2 := by
    simpa only [ENNReal.coe_add, ENNReal.coe_div h2, ENNReal.coe_div h4,
      ENNReal.coe_one, ENNReal.coe_ofNat] using
      congrArg (fun x : NNReal => (x : ℝ≥0∞)) (show (1 / 4 : NNReal) + 1 / 4 = 1 / 2 by norm_num)
  have hright : (1 / 4 : ℝ≥0∞) + 1 / 2 = 3 / 4 := by
    simpa only [ENNReal.coe_add, ENNReal.coe_div h2, ENNReal.coe_div h4,
      ENNReal.coe_one, ENNReal.coe_ofNat] using
      congrArg (fun x : NNReal => (x : ℝ≥0∞)) (show (1 / 4 : NNReal) + 1 / 2 = 3 / 4 by norm_num)
  refine ⟨(1 / 4 : ℝ≥0∞) • Q (-m) (-m) + (1 / 4 : ℝ≥0∞) • Q (-m) m +
    (1 / 2 : ℝ≥0∞) • Q m m, ⟨?_, ?_⟩, ?_⟩
  · simp only [Measure.fst_add, fst_smul, hfst, ← add_smul, hleft]
  · simp only [Measure.snd_add, snd_smul, hsnd, add_assoc]
    rw [← add_smul, hright]
  · simp only [lintegral_add_measure, lintegral_smul_measure, hcost, sub_self,
      zero_pow (by decide : 2 ≠ 0), ENNReal.ofReal_zero, smul_eq_mul, mul_zero, add_zero, zero_add]
    rw [show (-m - m) ^ 2 = 4 * m ^ 2 by ring, ENNReal.ofReal_mul (by norm_num),
      ENNReal.ofReal_ofNat, ← mul_assoc, ENNReal.div_mul_cancel (by norm_num) (by simp), one_mul]

end AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureCoupling
