import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Series
import Mathlib.Tactic

/-! Even absolute moments from the standard two-sided subgaussian MGF bound. -/

open MeasureTheory ProbabilityTheory
open scoped BigOperators

namespace AutoSamplingTheory.TechnicalLemmas.Probability.SubgaussianEvenMoments

private theorem even_power_div_factorial_le_cosh (x : ℝ) (m : ℕ) :
    x^(2*m)/(Nat.factorial (2*m) : ℝ) ≤ Real.cosh x := by
  rw [Real.cosh_eq_tsum]
  simpa only [Finset.sum_singleton] using
    (Real.hasSum_cosh x).summable.sum_le_tsum {m} (fun n _ => by
      rw [pow_mul]
      positivity)

/-- The proxy `c` is the variance parameter in `exp (c*t²/2)`.
Both the zero proxy and the zeroth moment are included. -/
theorem integrable_even_moment_le_of_hasSubgaussianMGF
    {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (X : Ω → ℝ) (c : NNReal)
    (hX : HasSubgaussianMGF X c μ) (m : ℕ) :
    Integrable (fun ω => |X ω|^(2*m)) μ ∧
      (∫ ω, |X ω|^(2*m) ∂μ) ≤
        (Nat.factorial (2*m) : ℝ)*Real.exp (1/2)*(c : ℝ)^m := by
  have hi : Integrable (fun ω => |X ω|^(2*m)) μ := by
    have h : MemLp X (2*m : ℕ) μ := by
      simpa using hX.memLp ((2*m : ℕ) : NNReal)
    simpa only [Real.norm_eq_abs] using h.integrable_norm_pow'
  refine ⟨hi,?_⟩
  by_cases hm : m = 0
  · subst m
    simp only [mul_zero,pow_zero,Nat.factorial_zero,Nat.cast_one,one_mul,mul_one,
      integral_const,measureReal_def,measure_univ,ENNReal.toReal_one,one_smul]
    exact Real.one_le_exp (by norm_num)
  by_cases hc : c = 0
  · subst c
    have hz := hX.ae_eq_zero_of_hasSubgaussianMGF_zero
    have he : (fun ω => |X ω|^(2*m)) =ᵐ[μ] (fun _ => (0 : ℝ)) := by
      filter_upwards [hz] with ω hω
      simp [hω,hm]
    rw [integral_congr_ae he]
    simp [hm]
  have hcpos : 0 < (c : ℝ) := NNReal.coe_pos.mpr (pos_iff_ne_zero.mpr hc)
  let t := (Real.sqrt (c : ℝ))⁻¹
  have htc : t^2*(c : ℝ) = 1 := by
    dsimp [t]
    rw [inv_pow,Real.sq_sqrt hcpos.le]
    exact inv_mul_cancel₀ hcpos.ne'
  have hscale : t^(2*m)*(c : ℝ)^m = 1 := by
    rw [pow_mul,← mul_pow,htc,one_pow]
  have hp := hX.integrable_exp_mul t
  have hn := hX.integrable_exp_mul (-t)
  have hl : Integrable (fun ω => t^(2*m)*|X ω|^(2*m)/(Nat.factorial (2*m) : ℝ)) μ :=
    (hi.const_mul _).div_const _
  have hr : Integrable (fun ω => (Real.exp (t*X ω)+Real.exp ((-t)*X ω))/2) μ :=
    (hp.add hn).div_const 2
  have point (ω : Ω) :
      t^(2*m)*|X ω|^(2*m)/(Nat.factorial (2*m) : ℝ) ≤
        (Real.exp (t*X ω)+Real.exp ((-t)*X ω))/2 := by
    have ha : |X ω|^(2*m) = X ω^(2*m) := by rw [pow_mul,pow_mul,sq_abs]
    rw [ha,← mul_pow]
    simpa only [Real.cosh_eq,neg_mul] using even_power_div_factorial_le_cosh (t*X ω) m
  have hIntegral := integral_mono hl hr point
  rw [integral_div,integral_const_mul,integral_div,integral_add hp hn] at hIntegral
  change t^(2*m)*(∫ ω, |X ω|^(2*m) ∂μ)/(Nat.factorial (2*m) : ℝ) ≤
    (mgf X μ t+mgf X μ (-t))/2 at hIntegral
  have hpBound := hX.mgf_le t
  have hnBound := hX.mgf_le (-t)
  rw [mul_comm (c : ℝ) (t^2),htc] at hpBound
  rw [neg_sq,mul_comm (c : ℝ) (t^2),htc] at hnBound
  have hBound : t^(2*m)*(∫ ω, |X ω|^(2*m) ∂μ)/(Nat.factorial (2*m) : ℝ) ≤
      Real.exp (1/2) := by linarith
  have hf : 0 < (Nat.factorial (2*m) : ℝ) := Nat.cast_pos.mpr (Nat.factorial_pos _)
  have hBound' := (div_le_iff₀ hf).mp hBound
  calc
    (∫ ω, |X ω|^(2*m) ∂μ) =
        (c : ℝ)^m*(t^(2*m)*(∫ ω, |X ω|^(2*m) ∂μ)) := by
      rw [← mul_assoc,mul_comm ((c : ℝ)^m),hscale,one_mul]
    _ ≤ (c : ℝ)^m*(Real.exp (1/2)*(Nat.factorial (2*m) : ℝ)) :=
      mul_le_mul_of_nonneg_left hBound' (pow_nonneg hcpos.le m)
    _ = (Nat.factorial (2*m) : ℝ)*Real.exp (1/2)*(c : ℝ)^m := by ring

#print axioms even_power_div_factorial_le_cosh
#print axioms integrable_even_moment_le_of_hasSubgaussianMGF

end AutoSamplingTheory.TechnicalLemmas.Probability.SubgaussianEvenMoments
